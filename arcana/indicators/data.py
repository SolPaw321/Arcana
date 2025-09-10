from .indicators import Indicator, IndicatorCfg
from arcana.price_data import PriceData
from arcana.utils.classes_utils import validate_classes_names

from pandas import DataFrame


class IndicatorData:
    def __init__(self, price_data: PriceData | list[DataFrame]):
        if isinstance(price_data, PriceData):
            self._price_data = price_data.prices_raw
        else:
            self._price_data = price_data

    def add_indicator(self, indicator: Indicator, *, ind_config: IndicatorCfg):
            validate_classes_names(ind_config.name, [indicator.name()])
            #indicator.compute()