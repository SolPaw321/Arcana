import ctypes

ma_lib = ctypes.CDLL(r"D:\Arcana\arcana\indicators\c_definitions\moving_averages.dll")

_D_PTR = [ctypes.POINTER(ctypes.c_double)]
_I = [ctypes.c_int]
_D = [ctypes.c_double]

_BASE_MA_ARGS = 2*_D_PTR + 2*_I

ma_lib.sma.argtypes = _BASE_MA_ARGS
ma_lib.sma.restype = None

ma_lib.esma.argtypes = _BASE_MA_ARGS + _D
ma_lib.esma.restype = None

ma_lib.ema.argtypes = _BASE_MA_ARGS
ma_lib.ema.restype = None

ma_lib.wma.argtypes = _BASE_MA_ARGS
ma_lib.wma.restype = None

ma_lib.hma.argtypes = _BASE_MA_ARGS
ma_lib.hma.restype = None

ma_lib.rma.argtypes = _BASE_MA_ARGS
ma_lib.rma.restype = None

ma_lib.tema.argtypes = _BASE_MA_ARGS
ma_lib.tema.restype = None

ma_lib.dema.argtypes = _BASE_MA_ARGS
ma_lib.dema.restype = None

ma_lib.kama.argtypes = _BASE_MA_ARGS + 2*_I
ma_lib.kama.restype = None

ma_lib.frama.argtypes = 4*_D_PTR + 2*_I
ma_lib.frama.restype = None

import numpy as np
from arcana.indicators.adapters import ma_prepare_data_to_c

#data = np.array([10,11,12,13,15,20], dtype=np.float64)
close = np.array([100.0, 101.0, 102.0,  99.0,  98.0, 100.0, 103.0, 105.0, 104.0, 106.0, 108.0, 107.0])
high  = np.array([100.5, 101.5, 102.3, 100.0,  99.2, 100.8, 103.8, 105.6, 104.7, 106.9, 108.4, 107.3])
low   = np.array([ 99.4, 100.2, 101.1,  98.1,  97.5,  99.1, 102.0, 104.2, 103.6, 105.2, 107.1, 106.4])
period = 5
length = len(close)
ind = np.zeros_like(close)

res = ma_prepare_data_to_c(to_d_ptr=[close, ind, high, low], to_i=[length, period])
ma_lib.frama(*res)
print(ind)