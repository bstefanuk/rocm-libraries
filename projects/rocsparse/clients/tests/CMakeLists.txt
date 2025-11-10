# Copyright Advanced Micro Devices, Inc., or its affiliates.
# SPDX-License-Identifier: MIT

find_package(GTest 1.11.0 REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

# Client matrices setup
if(NOT EXISTS "${CMAKE_MATRICES_DIR}")
    set(CMAKE_MATRICES_DIR ${PROJECT_BINARY_DIR}/matrices CACHE STRING "Matrices directory")
    file(MAKE_DIRECTORY ${CMAKE_MATRICES_DIR})

    set(CONVERT_SOURCE ${PROJECT_SOURCE_DIR}/deps/convert.cpp CACHE STRING "Convert tool mtx2csr")
    include(${PROJECT_SOURCE_DIR}/cmake/ClientMatrices.cmake)
else()
    # Copy existing matrices
    if(NOT CMAKE_MATRICES_DIR STREQUAL "${PROJECT_BINARY_DIR}/matrices")
        message(STATUS "Copying matrix files from ${CMAKE_MATRICES_DIR} to ${PROJECT_BINARY_DIR}/matrices")
        execute_process(
            COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_MATRICES_DIR} ${PROJECT_BINARY_DIR}/matrices
            RESULT_VARIABLE STATUS
        )
        if(STATUS AND NOT STATUS EQUAL 0)
            message(FATAL_ERROR "Failed to copy matrix .csr files")
        endif()
    endif()
endif()

# Define test executable
add_executable(rocsparse-test
    rocsparse_test_main.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_axpby.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_axpyi.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_doti.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dotci.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gather.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_scatter.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gthr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gthrz.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_rot.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_roti.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sctr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsrmv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsrxmv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsrsv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_coomv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrmv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrmv_managed.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrsv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csritsv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_ellmv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_hybmv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gebsrmv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsrmm.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gebsrmm.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrmm.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrsm.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsrsm.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gemmi.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsrgeam.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsrgemm.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrgeam.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrgemm.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrgemm_reuse.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsric0.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsrilu0.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csric0.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrilu0.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csritilu0.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csritilu0_ex.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gtsv_no_pivot.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gtsv_no_pivot_strided_batch.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gtsv_interleaved_batch.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gpsv_interleaved_batch.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csr2coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csr2csc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gebsr2gebsc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csr2ell.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csr2hyb.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csr2bsr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csr2gebsr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_coo2csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_ell2csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_hyb2csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsr2csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gebsr2csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gebsr2gebsr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csr2csr_compress.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_prune_csr2csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_prune_csr2csr_by_percentage.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_identity.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_inverse_permutation.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrsort.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_cscsort.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_coosort.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csricsv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrilusv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_nnz.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dense2csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dense2coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_prune_dense2csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_prune_dense2csr_by_percentage.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dense2csc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csr2dense.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csc2dense.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_coo2dense.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spvec_descr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmat_descr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dnvec_descr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dnmat_descr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_const_spvec_descr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_const_spmat_descr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_const_dnvec_descr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_const_dnmat_descr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmv_bsr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmv_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmv_coo_aos.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmv_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmv_csc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmv_ell.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_v2_spmv_bsr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_v2_spmv_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_v2_spmv_coo_aos.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_v2_spmv_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_v2_spmv_csc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_v2_spmv_ell.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_v2_spmv_sell.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spsv_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sptrsv_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spitsv_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spsv_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sptrsv_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spsm_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spsm_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sptrsm_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sptrsm_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmm_bsr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmm_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmm_csc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmm_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmm_bell.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmm_batched_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmm_batched_csc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmm_batched_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spmm_batched_bell.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spvv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sparse_to_dense_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sparse_to_dense_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sparse_to_dense_csc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dense_to_sparse_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dense_to_sparse_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dense_to_sparse_csc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sparse_to_sparse.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_extract.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spgemm_bsr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spgemm_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spgemm_reuse_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spgeam_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spgeam_reuse_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spgeam_csr_2.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_spgeam_reuse_csr_2.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gtsv.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_gemvi.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_sddmm.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_csrcolor.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_copy_info.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_check_matrix_csr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_check_matrix_coo.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_check_matrix_gebsr.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_check_matrix_gebsc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_check_matrix_csc.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_check_matrix_ell.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_check_matrix_hyb.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_check_spmat.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test_bsrpad_value.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/rocsparse_test_listeners.cpp
    # Testing implementations
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_axpby.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_axpyi.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_doti.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_dotci.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gather.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_scatter.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gthr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gthrz.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_rot.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_roti.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_sctr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsrmv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsrxmv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsrsv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_coomv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrmv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrmv_managed.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrsv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csritsv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_ellmv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_hybmv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gebsrmv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsrmm.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gebsrmm.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrmm.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrsm.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsrsm.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gemmi.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsrgeam.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsrgemm.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrgeam.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrgemm.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrgemm_reuse.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsric0.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsrilu0.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csric0.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrilu0.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csritilu0.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csritilu0_ex.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gtsv_no_pivot.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gtsv_no_pivot_strided_batch.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gtsv_interleaved_batch.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gpsv_interleaved_batch.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csr2coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csr2csc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gebsr2gebsc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gebsr2gebsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csr2ell.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csr2hyb.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csr2bsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csr2gebsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_coo2csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_ell2csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_hyb2csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsr2csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gebsr2csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csr2csr_compress.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_prune_csr2csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_prune_csr2csr_by_percentage.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_identity.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_inverse_permutation.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrsort.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_cscsort.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_coosort.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csricsv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrilusv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_nnz.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_dense2csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_dense2coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_prune_dense2csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_prune_dense2csr_by_percentage.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_dense2csc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csr2dense.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csc2dense.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_coo2dense.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spvec_descr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmat_descr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_dnvec_descr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_dnmat_descr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_const_spvec_descr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_const_spmat_descr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_const_dnvec_descr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_const_dnmat_descr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmv_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmv_coo_aos.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmv_bsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmv_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmv_csc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmv_ell.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_v2_spmv_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_v2_spmv_coo_aos.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_v2_spmv_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_v2_spmv_bsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_v2_spmv_csc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_v2_spmv_ell.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_v2_spmv_sell.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spsv_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_sptrsv_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spitsv_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spsv_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_sptrsm_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_sptrsm_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spsm_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spsm_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmm_bsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmm_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmm_csc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmm_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmm_bell.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmm_batched_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmm_batched_csc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmm_batched_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spmm_batched_bell.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spvv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_sparse_to_dense_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_sparse_to_dense_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_sparse_to_dense_csc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_dense_to_sparse_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_dense_to_sparse_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_dense_to_sparse_csc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_sparse_to_sparse.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_extract.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spgemm_bsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spgemm_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spgemm_reuse_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spgeam_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spgeam_reuse_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spgeam_csr_2.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_spgeam_reuse_csr_2.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gtsv.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_gemvi.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_sddmm.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_csrcolor.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_copy_info.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_check_matrix_csr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_check_matrix_coo.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_check_matrix_gebsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_check_matrix_gebsc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_check_matrix_csc.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_check_matrix_ell.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_check_matrix_hyb.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_check_spmat.cpp
    ${PROJECT_SOURCE_DIR}/clients/testings/testing_bsrpad_value.cpp
    # Common utilities
    ${PROJECT_SOURCE_DIR}/clients/common/utility.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_random.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_reproducibility.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_reproducibility_test.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_reproducibility_test_data.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_reproducibility_results.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_check.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_parse_data.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_enum.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_enum_name.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_enum_from_name.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_init.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_host.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_vector_utils.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_matrix_factory.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_matrix_factory_laplace2d.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_matrix_factory_laplace3d.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_matrix_factory_zero.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_matrix_factory_random.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_matrix_factory_tridiagonal.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_matrix_factory_pentadiagonal.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_matrix_factory_file.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_exporter_rocsparseio.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_exporter_rocalution.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_exporter_matrixmarket.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_exporter_ascii.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_exporter_format_t.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_type_conversion.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_importer_rocalution.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_importer_rocsparseio.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_importer_matrixmarket.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_importer_mlbsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_importer_mlcsr.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_importer_format_t.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_clients_envariables.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_clients_matrices_dir.cpp
    ${PROJECT_SOURCE_DIR}/clients/common/rocsparseio.cpp
)

# Target compile definitions
target_compile_definitions(rocsparse-test PRIVATE GOOGLE_TEST)

if(ROCSPARSE_ENABLE_MEMSTAT)
    target_compile_definitions(rocsparse-test PRIVATE ROCSPARSE_WITH_MEMSTAT)
endif()

if(ROCSPARSE_ENABLE_ILP64)
    target_compile_definitions(rocsparse-test PRIVATE rocsparse_ILP64)
endif()

# Target compile options
target_compile_options(rocsparse-test PRIVATE
    -ffp-contract=on
    -mfma
    -Wno-deprecated
    -Wno-unused-command-line-argument
    -Wall
)

# Target compile features
target_compile_features(rocsparse-test PRIVATE cxx_std_17)

# Include directories
target_include_directories(rocsparse-test PRIVATE
    $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/clients/include>
)

# OpenMP RPATH handling for hip-clang
if(NOT WIN32 AND OPENMP_FOUND)
    if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        if(TARGET OpenMP::OpenMP_CXX)
            set_target_properties(rocsparse-test PROPERTIES
                BUILD_RPATH "${HIP_CLANG_ROOT}/lib"
                INSTALL_RPATH "$ORIGIN/../llvm/lib"
            )
        elseif(TARGET OpenMP::omp)
            if(DEFINED openmp_LIB_DIR)
                set_target_properties(rocsparse-test PROPERTIES
                    BUILD_RPATH "${HIP_CLANG_ROOT}/${openmp_LIB_DIR}"
                    INSTALL_RPATH "$ORIGIN/../llvm/${openmp_LIB_DIR}"
                )
            endif()
        endif()
    endif()
endif()

# Link libraries
target_link_libraries(rocsparse-test PRIVATE
    roc::rocsparse
    GTest::gtest
    hip::host
    hip::device
)

# Link OpenMP if found
if(OPENMP_FOUND)
    if(TARGET OpenMP::omp)
        target_link_libraries(rocsparse-test PRIVATE OpenMP::omp)
    elseif(TARGET OpenMP::OpenMP_CXX)
        target_link_libraries(rocsparse-test PRIVATE OpenMP::OpenMP_CXX)
    endif()
endif()

# rocTX support
if(NOT WIN32 AND ROCSPARSE_ENABLE_MARKER)
    if(ROCTRACER_INCLUDE_DIR AND ROCTX_LIBRARY)
        target_include_directories(rocsparse-test PRIVATE ${ROCTRACER_INCLUDE_DIR})
        target_link_libraries(rocsparse-test PRIVATE ${ROCTX_LIBRARY})
        target_compile_definitions(rocsparse-test PRIVATE ROCSPARSE_CLIENTS_WITH_ROCTX)
    endif()
endif()

# Prepare testing data
set(ROCSPARSE_TEST_DATA "${PROJECT_BINARY_DIR}/staging/rocsparse_test.data")
string(REGEX REPLACE ".cpp" ".yaml" ROCSPARSE_TEST_YAMLS "${ROCSPARSE_TEST_SOURCES}")

add_custom_command(
    OUTPUT "${ROCSPARSE_TEST_DATA}"
    COMMAND ${Python3_EXECUTABLE} ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_gentest.py
            -m ${PROJECT_BINARY_DIR}/matrices
            -I ${PROJECT_SOURCE_DIR}/clients/include
            rocsparse_test.yaml
            -o "${ROCSPARSE_TEST_DATA}"
    DEPENDS
        ${PROJECT_SOURCE_DIR}/clients/common/rocsparse_gentest.py
        rocsparse_test.yaml
        ${PROJECT_SOURCE_DIR}/clients/include/rocsparse_common.yaml
        ${ROCSPARSE_TEST_YAMLS}
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
)

add_custom_target(rocsparse-test-data DEPENDS "${ROCSPARSE_TEST_DATA}")
add_dependencies(rocsparse-test rocsparse-test-data rocsparse-common)

# Install test executable and data
rocm_install(TARGETS rocsparse-test COMPONENT tests DESTINATION "${CMAKE_INSTALL_BINDIR}")
rocm_install(FILES ${ROCSPARSE_TEST_DATA} DESTINATION "${CMAKE_INSTALL_DATADIR}/rocsparse/test" COMPONENT tests)

# Windows: Copy DLLs
if(WIN32)
    file(GLOB third_party_dlls
        LIST_DIRECTORIES OFF
        CONFIGURE_DEPENDS
        $ENV{HIP_DIR}/bin/*.dll
        $ENV{HIP_DIR}/bin/hipinfo.exe
        ${PROJECT_SOURCE_DIR}/rtest.*
        $ENV{rocblas_DIR}/bin/*.dll
        C:/Windows/System32/libomp140*.dll
    )
    foreach(file_i ${third_party_dlls})
        add_custom_command(TARGET rocsparse-test POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy ${file_i} ${PROJECT_BINARY_DIR}/staging/
        )
    endforeach()
endif()
