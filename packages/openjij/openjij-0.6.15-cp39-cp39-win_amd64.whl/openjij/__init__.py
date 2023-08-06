

""""""# start delvewheel patch
def _delvewheel_init_patch_1_3_4():
    import ctypes
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'openjij.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    load_order_filepath = os.path.join(libs_dir, '.load-order-openjij-0.6.15')
    if not is_pyinstaller or os.path.isfile(load_order_filepath):
        with open(os.path.join(libs_dir, '.load-order-openjij-0.6.15')) as file:
            load_order = file.read().split()
        for lib in load_order:
            lib_path = os.path.join(libs_dir, lib)
            if not is_pyinstaller or os.path.isfile(lib_path):
                ctypes.WinDLL(lib_path)


_delvewheel_init_patch_1_3_4()
del _delvewheel_init_patch_1_3_4
# end delvewheel patch

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

from openjij import cxxjij

from openjij.model.model import BinaryPolynomialModel, BinaryQuadraticModel
from openjij.sampler.csqa_sampler import CSQASampler
from openjij.sampler.response import Response
from openjij.sampler.sa_sampler import SASampler
from openjij.sampler.sqa_sampler import SQASampler
from openjij.utils.benchmark import solver_benchmark
from openjij.utils.res_convertor import convert_response
from openjij.variable_type import BINARY, SPIN, Vartype, cast_vartype

__all__ = [
    "cxxjij",
    "SPIN",
    "BINARY",
    "Vartype",
    "cast_vartype",
    "Response",
    "SASampler",
    "SQASampler",
    "CSQASampler",
    "BinaryQuadraticModel",
    "BinaryPolynomialModel",
    "solver_benchmark",
    "convert_response",
]
