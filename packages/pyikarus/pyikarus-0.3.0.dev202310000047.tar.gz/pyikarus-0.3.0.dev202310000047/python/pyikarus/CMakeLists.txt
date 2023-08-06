# SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later

add_subdirectory(assembler)
add_subdirectory(finite_elements)
add_subdirectory(utils)

# set(CXX_MAX_STANDARD 20)
add_python_targets(pyikarus __init__ dirichletValues materials)

dune_add_pybind11_module(NAME _pyikarus)
set_property(
  TARGET _pyikarus
  PROPERTY LINK_LIBRARIES dunecommon pyikarus
  APPEND
)
if(SKBUILD)
  install(TARGETS _pyikarus LIBRARY DESTINATION python/pyikarus)
endif()
