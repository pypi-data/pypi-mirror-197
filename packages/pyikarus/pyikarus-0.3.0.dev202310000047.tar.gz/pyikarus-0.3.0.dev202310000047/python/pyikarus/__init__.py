# SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later
try:
    from dune.packagemetadata import registerExternalModule
    import pathlib

    # register pyikarus to be recognized by dune-py (code generation module)
    # as a module of the dune universe
    registerExternalModule(
        moduleName="pyikarus",
        modulePath=str(pathlib.Path(__file__).parent.resolve()),
    )

except ImportError:
    pass

from ._pyikarus import *
from .dirichletValues import dirichletValues
from .materials import *
