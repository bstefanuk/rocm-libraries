#!/usr/bin/env python3
"""Compare DVC-tracked logic files between branches."""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


class DVCDiffer:
    """Handles DVC logic file comparison between branches."""

    def __init__(self, base_branch, output_format='text'):
        self.base_branch = base_branch
        self.output_format = output_format
        self.worktree_dir = None
        self.changes_found = 0
        self.dvc_files = []
        self.markdown_sections = []

    def run_command(self, cmd, cwd=None, check=True, capture=True):
        """Execute shell command and return result."""
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=isinstance(cmd, str),
            capture_output=capture,
            text=True,
            check=False
        )
        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
        return result

    def check_prerequisites(self):
        """Verify git repo and DVC installation."""
        # Check git repo
        result = self.run_command('git rev-parse --is-inside-work-tree', check=False)
        if result.returncode != 0:
            print('Error: Not in a git repository')
            return False

        # Check DVC installation
        result = self.run_command('dvc version', check=False)
        if result.returncode != 0:
            print('Error: DVC is not installed')
            return False

        return True

    def get_changed_dvc_files(self):
        """Get list of .dvc files changed between base and current branch."""
        print(f'Detecting changed .dvc files against {self.base_branch}...')

        # Fetch base branch
        self.run_command(f'git fetch origin {self.base_branch}', check=False)

        # Get changed .dvc files
        cmd = f'git diff --name-only origin/{self.base_branch}...HEAD'
        result = self.run_command(cmd, check=False)

        if result.returncode != 0:
            # Try without origin prefix
            cmd = f'git diff --name-only {self.base_branch}...HEAD'
            result = self.run_command(cmd, check=False)

        if result.returncode != 0:
            print(f'Error: Could not diff against {self.base_branch}')
            return []

        dvc_files = [f for f in result.stdout.strip().split('\n') if f.endswith('.dvc')]
        return [f for f in dvc_files if f]  # Filter empty strings

    def create_worktree(self):
        """Create temporary worktree for base branch."""
        self.worktree_dir = tempfile.mkdtemp(prefix='dvc_worktree_')
        print(f'Creating worktree for {self.base_branch}...')

        result = self.run_command(
            f'git worktree add {self.worktree_dir} {self.base_branch}',
            check=False
        )

        if result.returncode != 0:
            # Try with origin prefix
            result = self.run_command(
                f'git worktree add {self.worktree_dir} origin/{self.base_branch}',
                check=False
            )

        if result.returncode != 0:
            print(f'Error: Could not create worktree for {self.base_branch}')
            return False

        print(f'Worktree created at {self.worktree_dir}')
        return True

    def cleanup_worktree(self):
        """Remove temporary worktree."""
        if self.worktree_dir:
            print('Cleaning up worktree...')
            self.run_command(f'git worktree remove {self.worktree_dir} --force', check=False)
            if os.path.exists(self.worktree_dir):
                shutil.rmtree(self.worktree_dir)

    def pull_changed_files(self, dvc_files):
        """Pull changed files from dev remote."""
        print(f'\nPulling {len(dvc_files)} changed file(s) from hipblaslt-dev remote...')

        for dvc_file in dvc_files:
            print(f'  Pulling {dvc_file}')
            result = self.run_command(f'dvc pull {dvc_file} -r hipblaslt-dev', check=False)
            if result.returncode != 0:
                print(f'  Warning: Failed to pull {dvc_file}')

    def compare_file(self, dvc_file, prod_dir):
        """Compare single file between prod and dev versions."""
        actual_file = dvc_file[:-4]  # Remove .dvc extension

        if self.output_format == 'text':
            print(f'\n{"=" * 70}')
            print(f'Processing: {actual_file}')

        # Check if actual file exists locally
        if not os.path.exists(actual_file):
            if self.output_format == 'text':
                print(f'  Warning: {actual_file} not found locally')
            return

        # Check if .dvc file exists in base branch
        base_dvc_file = os.path.join(self.worktree_dir, f'{actual_file}.dvc')
        if not os.path.exists(base_dvc_file):
            self.changes_found += 1
            if self.output_format == 'text':
                print(f'  NEW FILE (doesn\'t exist in {self.base_branch})')
            else:
                self.markdown_sections.append(f'### \u2728 `{actual_file}` (New File)\n\nThis file is newly added in this PR.\n')
            return

        if self.output_format == 'text':
            print(f'  .dvc file exists in {self.base_branch}')
            print(f'  Pulling production version from hipblaslt-prod remote...')

        # Pull from production remote
        result = self.run_command(
            f'dvc pull {actual_file} -r hipblaslt-prod',
            cwd=self.worktree_dir,
            check=False,
            capture=(self.output_format == 'markdown')
        )

        if result.returncode != 0:
            if self.output_format == 'text':
                print('  Error: Could not pull from hipblaslt-prod remote')
                print('  The file may not exist in production remote yet')
            else:
                self.markdown_sections.append(f'### \u26a0\ufe0f `{actual_file}` (Could not retrieve from production)\n\nUnable to fetch this file from the production remote for comparison.\n')
            return

        # Copy production version
        prod_file = os.path.join(prod_dir, os.path.basename(actual_file))
        base_file = os.path.join(self.worktree_dir, actual_file)
        shutil.copy2(base_file, prod_file)

        if self.output_format == 'text':
            print('  Retrieved production version')

        # Compare files
        result = self.run_command(f'diff -u {prod_file} {actual_file}', check=False)
        if result.returncode != 0:
            self.changes_found += 1
            if self.output_format == 'text':
                print('  Differences found:')
                print()
                print(result.stdout)
            else:
                self.markdown_sections.append(f'### `{actual_file}`\n\n```diff\n{result.stdout}```\n')
        else:
            if self.output_format == 'text':
                print('  No content differences (hash may have changed)')

    def run(self):
        """Execute the diff workflow."""
        if self.output_format == 'text':
            print('DVC Logic Diff')
            print(f'Base branch: {self.base_branch}\n')

        if not self.check_prerequisites():
            return 1

        # Get changed files
        self.dvc_files = self.get_changed_dvc_files()
        if not self.dvc_files:
            if self.output_format == 'text':
                print(f'\nNo .dvc files changed between {self.base_branch} and current branch')
            else:
                print('## Logic Files Diff Report\n')
                print(f'No .dvc files were modified in this PR.\n')
            return 0

        if self.output_format == 'text':
            print(f'\nChanged .dvc files:')
            for f in self.dvc_files:
                print(f'  {f}')

        # Pull changed files
        self.pull_changed_files(self.dvc_files)

        # Create worktree
        if not self.create_worktree():
            return 1

        try:
            # Compare files
            with tempfile.TemporaryDirectory(prefix='dvc_prod_files_') as prod_dir:
                if self.output_format == 'text':
                    print(f'\n{"=" * 70}')
                    print('Fetching production versions and generating diffs')
                    print(f'{"=" * 70}')

                for dvc_file in self.dvc_files:
                    self.compare_file(dvc_file, prod_dir)

            # Output results
            if self.output_format == 'text':
                print(f'\n{"=" * 70}')
                print('Summary')
                print(f'{"=" * 70}')
                print(f'Base branch: {self.base_branch}')
                print(f'Changed .dvc files: {len(self.dvc_files)}')
                print(f'Files with content changes: {self.changes_found}')

                if self.changes_found == 0:
                    print()
                    print('No content differences detected in logic files.')
                    print('(The .dvc file hashes may have changed, but contents are identical)')

                print('\nTest complete!')
            else:
                self._output_markdown()

        finally:
            self.cleanup_worktree()

        return 0

    def _output_markdown(self):
        """Generate markdown report for CI."""
        print('## Logic Files Diff Report\n')
        print(f'**Base branch:** `{self.base_branch}`\n')

        if self.changes_found > 0:
            print(f'**Files with changes:** {self.changes_found}\n')

        if self.markdown_sections:
            for section in self.markdown_sections:
                print(section)
        else:
            print('No content differences detected in logic files.\n')
            print('The .dvc file hashes may have changed, but the actual file contents are identical.\n')


def main():
    parser = argparse.ArgumentParser(
        description='Compare DVC-tracked logic files between branches',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'base_branch',
        nargs='?',
        default='dummy_develop',
        help='Base branch to compare against (default: dummy_develop)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    differ = DVCDiffer(args.base_branch, args.format)
    return differ.run()


if __name__ == '__main__':
    sys.exit(main())
