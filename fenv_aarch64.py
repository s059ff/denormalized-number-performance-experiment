import platform
from ctypes import CDLL, POINTER, Structure, c_int, c_uint
from ctypes.util import find_library

assert platform.machine() == "aarch64"

# typedef struct
# {
#     unsigned int __fpcr;
#     unsigned int __fpsr;
# }
# fenv_t;


class fenv_t(Structure):

    _fields_ = [("__fpcr", c_uint), ("__fpsr", c_uint)]

    def _init_(self, __fpcr, __fpsr):
        self.__fpcr = __fpcr
        self.__fpsr = __fpsr


libm = CDLL(find_library("m"))
libm.fesetenv.argtypes = [POINTER(fenv_t)]
libm.fesetenv.restype = c_int
libm.fegetenv.argtypes = [POINTER(fenv_t)]
libm.fegetenv.restype = c_int

FZ = 0x1000000


def set_ftz():
    fenv = fenv_t()
    assert 0 == libm.fegetenv(fenv)
    fenv.__fpcr |= FZ
    assert 0 == libm.fesetenv(fenv)


def unset_ftz():
    fenv = fenv_t()
    assert 0 == libm.fegetenv(fenv)
    fenv.__fpcr &= ~FZ
    assert 0 == libm.fesetenv(fenv)
