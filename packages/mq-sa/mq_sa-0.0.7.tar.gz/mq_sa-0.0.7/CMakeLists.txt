# 3.25.2 is latest here https://github.com/scikit-build/cmake-python-distributions
cmake_minimum_required(VERSION 3.25.2)

project(mq_sa)

find_package(PythonExtensions REQUIRED)

find_package(Boost REQUIRED python)

# message("Boost_LIBRARY_DIRS: ${Boost_LIBRARY_DIRS}")

add_library(_mq_sa MODULE mq_sa/_mq_sa.cpp)

target_link_libraries(_mq_sa ${Boost_PYTHON_LIBRARY})

target_include_directories(_mq_sa PRIVATE ${Boost_INCLUDE_DIRS})

python_extension_module(_mq_sa
  LINKED_MODULES_VAR linked_module_list
  FORWARD_DECL_MODULES_VAR fdecl_module_list
)
install(TARGETS _mq_sa LIBRARY DESTINATION mq_sa)
