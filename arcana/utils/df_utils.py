from arcana.price_data.dev_types import PriceDataColumns

from pandas import DataFrame, concat
from collections.abc import Iterable


def stack_data(df_: Iterable[DataFrame], symbols: Iterable[str]) -> DataFrame:
    data = concat(df_, keys=symbols, axis=1)
    data = data.swaplevel(axis=1)
    data = data.stack(future_stack=True)
    data = data.drop(columns=PriceDataColumns.SYMBOL)
    return data
