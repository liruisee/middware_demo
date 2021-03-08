cmake_minimum_required(VERSION 3.9)
project(middware_demo)

set(CMAKE_CXX_STANDARD 11)
set(SOURCE_FILES demo1/demo1.cpp)

#add_executable(helloWorld module.cpp num_operator.h solibs/SoDemoTest.h solibs/SoDemoTest.cpp solibs/main.cpp solibs/one.cpp solibs/two.cpp solibs/three.cpp hello/hello.cpp hello/main.cpp)
add_executable(middware_demo main.cpp demo1/demo1.cpp)
