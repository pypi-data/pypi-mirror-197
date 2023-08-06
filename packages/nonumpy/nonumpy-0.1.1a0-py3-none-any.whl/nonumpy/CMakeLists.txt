cmake_minimum_required(VERSION 3.20)

project(nonumpy)

add_library(${PROJECT_NAME}
    SHARED
    nonumpy_filters.c
    nonumpy_ema.c
)

target_include_directories(${PROJECT_NAME} PRIVATE .)

target_compile_definitions(${PROJECT_NAME} PRIVATE NONUMPY_FLOAT_T=float)

target_compile_options(${PROJECT_NAME} PRIVATE "-save-temps=obj")

set_target_properties(${PROJECT_NAME} PROPERTIES PUBLIC_HEADER nonumpy.h)

# add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
# COMMAND gcc -E -DNONUMPY_FLOAT_T=float
# ${CMAKE_CURRENT_SOURCE_DIR}/nonumpy_filters.h
# ${CMAKE_CURRENT_SOURCE_DIR}/nonumpy_ema.h > nonumpy.cdef.h
# VERBATIM)
install(TARGETS ${PROJECT_NAME})