import ctypes
import numpy as np

lib = ctypes.CDLL(r"D:\Arcana\arcana\indicators\c_indicators.dll")
lib.sma.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
lib.sma.restype = None
lib.ema.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
lib.ema.restype = None


arr = np.array([1,2,3,5,63,23,4235], dtype=np.float64)
ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

out_arr = np.array([0.0 for i in arr], dtype=np.float64)
ptr_out = out_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
lib.sma(ptr, ptr_out, ctypes.c_int(len(arr)), ctypes.c_int(3))
print(f"SMA: {out_arr} {type(out_arr)}")
out_arr = np.array([0.0 for i in arr], dtype=np.float64)
ptr_out = out_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
print(f"EMA: {lib.ema(ptr, ptr_out, ctypes.c_int(len(arr)), ctypes.c_int(3))}")



