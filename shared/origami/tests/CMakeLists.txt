# Copyright Advanced Micro Devices, Inc., or its affiliates.
# SPDX-License-Identifier: MIT

find_package(Catch2 3 QUIET CONFIG)
if(NOT Catch2_FOUND)
    if(ORIGAMI_ENABLE_FETCH)
        include(FetchContent)
        fetchcontent_declare(
            Catch2 GIT_REPOSITORY https://github.com/catchorg/Catch2.git GIT_TAG devel
        )
        fetchcontent_makeavailable(Catch2)
    else()
        message(FATAL_ERROR "Failed to find Catch2")
    endif()
endif()

add_executable(origami-tests)

target_sources(
    origami-tests PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/test_gemm.cpp"
                          "${CMAKE_CURRENT_SOURCE_DIR}/test_origami.cpp"
)

target_include_directories(origami-tests PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/include")

target_link_libraries(origami-tests PRIVATE roc::origami Catch2::Catch2WithMain)

include(CTest)
include(Catch)

# --- Build-time test discovery ---
# CTestTestfile.cmake is auto-generated when `enable_testing()` is called.
# Note that `catch_discover_tests` and `add_test` both append test declarations
# directly to <curr_bin_dir>/CTestTestfile.cmake.
catch_discover_tests(origami-tests DISCOVERY_MODE PRE_TEST PROPERTIES LABELS "cpp")

if(ORIGAMI_ENABLE_PYTHON)
    find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
    set(_pydir "${CMAKE_CURRENT_SOURCE_DIR}/../python")
    set(_pypath "${CMAKE_BINARY_DIR}/python:${_pydir}:$ENV{PYTHONPATH}")

    add_test(NAME origami_test COMMAND "${Python_EXECUTABLE}" origami_test.py WORKING_DIRECTORY ${_pydir})
    add_test(NAME origami_grid_test COMMAND "${Python_EXECUTABLE}" origami_grid_test.py WORKING_DIRECTORY ${_pydir})
    set_tests_properties(origami_test origami_grid_test PROPERTIES LABELS "python" ENVIRONMENT "PYTHONPATH=${_pypath}")
endif()

# --- Install-time test discovery ---
# CTestTestfile.cmake is manually written to support ctest invocations post-installation.
# This is required because, natively, ctest isn't intended for use with installed
# packages, but rather post-build testing, thus its built-in test discovery uses absolute
# build paths.
set(_ctest "${CMAKE_CURRENT_BINARY_DIR}/CTestTestfile.install.cmake")

set(_ctest_content [=[

# Copyright Advanced Micro Devices, Inc., or its affiliates.
# SPDX-License-Identifier: MIT

# Run tests with by pointing ctest to this file
# Example: `ctest --test-dir=/opt/rocm/bin/origami/CTestTestfile.cmake`

# C++ tests: run with `ctest -L cpp`
add_test(origami-tests "../origami-tests")
set_tests_properties(origami-tests PROPERTIES LABELS "cpp")

]=])

if(ORIGAMI_ENABLE_PYTHON)
    string(APPEND _ctest_content [=[

# Python tests: run with `ctest -L python`
add_test(origami_test python origami_test.py)
add_test(origami_grid_test python origami_grid_test.py)
set_tests_properties(origami_test origami_grid_test PROPERTIES
    LABELS "python"
    ENVIRONMENT "LD_LIBRARY_PATH=@CMAKE_INSTALL_FULL_LIBDIR@:$ENV{LD_LIBRARY_PATH};PYTHONPATH=@CMAKE_INSTALL_FULL_BINDIR@/origami:$ENV{PYTHONPATH}")

]=])
    install(FILES ${_pydir}/origami_test.py ${_pydir}/origami_grid_test.py
     DESTINATION "${CMAKE_INSTALL_BINDIR}/origami" COMPONENT tests )
    
endif()

string(CONFIGURE "${_ctest_content}" _ctest_content @ONLY ESCAPE_QUOTES)
file(WRITE ${_ctest} "${_ctest_content}")

install(FILES ${_ctest} DESTINATION "${CMAKE_INSTALL_BINDIR}/origami" COMPONENT tests RENAME CTestTestfile.cmake)
