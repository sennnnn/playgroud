# cmake 最低版本号要求
cmake_minimum_required(VERSION 2.8)

# set(3rdparty_include_directories ${CMAKE_SOURCE_DIR}/3rdparty/pdcurses/include)
# set(3rdparty_linking_directories ${CMAKE_SOURCE_DIR}/3rdparty/pdcurses/bin)

# 项目信息
project(calculator)

# 是否静态链接
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static")

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libgcc -static-libstdc++")

# 查找指定目录下的所有源文件，获取其路径并存到指定变量中
aux_source_directory(${CMAKE_SOURCE_DIR}/src SRC_DIR)

# 设置 include 文件路径
include_directories(${CMAKE_SOURCE_DIR}/include)

# 添加需要链接的库文件目录
link_directories(${CMAKE_SOURCE_DIR}/lib)

link_libraries(pdcurses.lib)

# 指定生成目标
add_executable(temp ${SRC_DIR})

# target_link_libraries(a pdcurses)

