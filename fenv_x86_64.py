import platform
from ctypes import CDLL, POINTER, Structure, c_int, c_uint
from ctypes.util import find_library

assert platform.machine() == "x86_64"

# typedef struct
# {
#     unsigned short int __control_word;            16
#     unsigned short int __glibc_reserved1;         16
#     unsigned short int __status_word;             16
#     unsigned short int __glibc_reserved2;         16
#     unsigned short int __tags;                    16
#     unsigned short int __glibc_reserved3;         16
#     unsigned int __eip;                           32
#     unsigned short int __cs_selector;             16
#     unsigned int __opcode:11;                     11
#     unsigned int __glibc_reserved4:5;             5
#     unsigned int __data_offset;                   32
#     unsigned short int __data_selector;           16
#     unsigned short int __glibc_reserved5;         16
# #ifdef __x86_64__                                 224
#     unsigned int __mxcsr;                         32
# #endif
# }
# fenv_t;


class fenv_t(Structure):

    _fields_ = [
        ("_1", c_uint),
        ("_2", c_uint),
        ("_3", c_uint),
        ("_4", c_uint),
        ("_5", c_uint),
        ("_6", c_uint),
        ("_7", c_uint),
        ("__mxcsr", c_uint),
    ]

    def _init_(self, _1, _2, _3, _4, _5, _6, _7, __mxcsr):
        self._1 = _1
        self._2 = _2
        self._3 = _3
        self._4 = _4
        self._5 = _5
        self._6 = _6
        self._7 = _7
        self.__mxcsr = __mxcsr


libm = CDLL(find_library("m"))
libm.fesetenv.argtypes = [POINTER(fenv_t)]
libm.fesetenv.restype = c_int
libm.fegetenv.argtypes = [POINTER(fenv_t)]
libm.fegetenv.restype = c_int

FZ = 0x8000
DAZ = 0x0040


def set_ftz():
    fenv = fenv_t()
    assert 0 == libm.fegetenv(fenv)
    fenv.__mxcsr |= FZ
    fenv.__mxcsr |= DAZ
    assert 0 == libm.fesetenv(fenv)


def unset_ftz():
    fenv = fenv_t()
    assert 0 == libm.fegetenv(fenv)
    fenv.__mxcsr &= ~(FZ | DAZ)
    assert 0 == libm.fesetenv(fenv)
