from arcana.price_data.dev_types import PriceDataColumns

from numpy import ndarray
from collections.abc import Iterable
from pandas import DataFrame, Index
import ctypes

CONVERSION_MAP = {
    "to_d_ptr": lambda x: x.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
    "to_i": ctypes.c_int,
    "to_d": ctypes.c_double,
}
SUP_CONVERSION_MAP = {
    "to_d_ptr": Iterable | ndarray,
    "to_i": Iterable | int,
    "to_d": Iterable | float,
}
def ma_prepare_data_to_c(**kwargs):
    res = []
    for key in kwargs.keys():
        if key not in SUP_CONVERSION_MAP.keys():
            raise KeyError(f"Conversion {key} is not valid. Use at least one of {list(SUP_CONVERSION_MAP.keys())}.")
        elif not isinstance(kwargs[key], SUP_CONVERSION_MAP[key]):
            raise TypeError(f"The {kwargs[key]} <{type(kwargs[key])}> is not valid type. For '{key}' pleas use {SUP_CONVERSION_MAP[key]} type.")


        if not isinstance(kwargs[key], Iterable):
            to_change = [kwargs[key]]
        else:
            to_change = kwargs[key]

        for to_ in to_change:
            res.append(CONVERSION_MAP[key](to_))

    return res

def ma_numpy_to_dataframe(data: Iterable, index: Index, symbol: str, name: str) -> DataFrame:
    df = DataFrame(data, columns=[name])
    df[PriceDataColumns.DATE] = index
    df = df.set_index(PriceDataColumns.DATE, drop=True)
    df[PriceDataColumns.SYMBOL] = symbol
    df = df.reindex(columns=[PriceDataColumns.SYMBOL, name])
    return df
