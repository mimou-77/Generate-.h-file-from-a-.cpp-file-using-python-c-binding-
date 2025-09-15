cmake_minimum_required(VERSION 3.13)
project(HeaderGenerator CXX)


include_directories("/usr/include/x86_64-linux-gnu/bits")

add_executable(generate_header_tool main.cpp)
