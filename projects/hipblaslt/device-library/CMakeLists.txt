# Copyright Advanced Micro Devices, Inc., or its affiliates.
# SPDX-License-Identifier:  MIT

include(tensilelite_create_device_libraries)

set(HIPBLASLT_LIBLOGIC_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../library"
    CACHE PATH "Path to the Tensile library logic"
)
set(HIPBLASLT_TENSILE_LIBPATH "${CMAKE_CURRENT_BINARY_DIR}/../Tensile"
    CACHE STRING "Path to output the device gemm libraries."
)

message(STATUS "HIPBLASLT_PYTHON_COMMAND: ${HIPBLASLT_PYTHON_COMMAND}")
message(STATUS "HIPBLASLT_PYTHON_DEPS: ${HIPBLASLT_PYTHON_DEPS}")
message(STATUS "HIPBLASLT_LIBLOGIC_PATH: ${HIPBLASLT_LIBLOGIC_PATH}")
message(STATUS "HIPBLASLT_TENSILE_LIBPATH: ${HIPBLASLT_TENSILE_LIBPATH}")
message(STATUS "GPU_TARGETS: ${GPU_TARGETS}")

tensilelite_create_device_libraries(
    "${HIPBLASLT_PYTHON_COMMAND}" "${HIPBLASLT_PYTHON_DEPS}" "${HIPBLASLT_LIBLOGIC_PATH}"
    "${HIPBLASLT_TENSILE_LIBPATH}" "${GPU_TARGETS}"
)

add_subdirectory(extops)
add_subdirectory(matrix-transform)
