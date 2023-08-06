

""""""# start delvewheel patch
def _delvewheel_init_patch_1_3_4():
    import ctypes
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'jij_cimod.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    load_order_filepath = os.path.join(libs_dir, '.load-order-jij_cimod-1.4.52')
    if not is_pyinstaller or os.path.isfile(load_order_filepath):
        with open(os.path.join(libs_dir, '.load-order-jij_cimod-1.4.52')) as file:
            load_order = file.read().split()
        for lib in load_order:
            lib_path = os.path.join(libs_dir, lib)
            if not is_pyinstaller or os.path.isfile(lib_path):
                ctypes.WinDLL(lib_path)


_delvewheel_init_patch_1_3_4()
del _delvewheel_init_patch_1_3_4
# end delvewheel patch

# Copyright 2022 Jij Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

from cimod import cxxcimod

from cimod.model.binary_polynomial_model import (
    BinaryPolynomialModel,
    make_BinaryPolynomialModel,
    make_BinaryPolynomialModel_from_JSON,
)
from cimod.model.binary_quadratic_model import (
    BinaryQuadraticModel,
    make_BinaryQuadraticModel,
    make_BinaryQuadraticModel_from_JSON,
)
from cimod.vartype import BINARY, SPIN, Vartype

__all__ = [
        "cxxcimod",
        "SPIN",
        "BINARY",
        "Vartype",
        "make_BinaryQuadraticModel",
        "make_BinaryQuadraticModel_from_JSON",
        "BinaryQuadraticModel",
        "make_BinaryPolynomialModel",
        "make_BinaryPolynomialModel_from_JSON",
        "BinaryPolynomialModel",
]
