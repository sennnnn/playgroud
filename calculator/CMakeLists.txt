# cmake 最低版本号要求
cmake_minimum_required(VERSION 2.8)

# 项目信息
project(calculator)

# 查找指定目录下的所有源文件，获取其路径并存到指定变量中
aux_source_directory(${CMAKE_SOURCE_DIR}/src SRC_DIR)

# 设置 include 文件路径
include_directories(${CMAKE_SOURCE_DIR}/include)

# 指定生成目标
add_executable(a ${SRC_DIR})