from .indicators import Indicator, MovingAverage, MovingAverageCfg
from typing import Type

from pandas import DataFrame
from arcana.price_data import PriceData, PriceDataColumns
from arcana.utils.classes_utils import validate_classes_names
from arcana.utils.df_utils import stack_data


class IndicatorData:
    """The interface for handling indicators."""
    def __init__(self, price_data: PriceData | list[DataFrame]):
        if isinstance(price_data, PriceData):
            self._raw_price_data = price_data.prices_raw
        else:
            self._raw_price_data = price_data

    @property
    def raw_price_data(self):
        return self._raw_price_data

    def add_moving_average(self, indicator: Type[MovingAverage], *, ind_config: MovingAverageCfg):
        """
        Add moving average.

        :param indicator: any moving average indicator
        :param ind_config: the indicator Cfg
        """
        validate_classes_names(ind_config.name, indicator.name())
        indicator.compute(self._raw_price_data, ma_cfg=ind_config)

    @staticmethod
    def get_ind_raw_data(ind_name: str) -> list[DataFrame]:
        """
        Get indicator raw data (list of DataFrames) for every symbol.

        :param ind_name: the indicator name
        :return: list of indicator data for every symbol
        """
        raw_data = Indicator.user_registry.get_data(ind_name, "raw_data")
        return raw_data

    @staticmethod
    def get_ind_data(ind_name: str) -> DataFrame:
        """
        Get indicator stacked data.

        :param ind_name: the indicator name
        :return: stacked indicator data
        """
        raw_data = Indicator.user_registry.get_data(ind_name, "raw_data")
        symbols = [df[PriceDataColumns.SYMBOL].iloc[0] for df in raw_data]
        data = stack_data(raw_data, symbols)
        return data

    @staticmethod
    def get_supported_indicators() -> tuple[str]:
        """Return all supported indicators names."""
        return Indicator.registry.all_registered()

    @staticmethod
    def get_user_indicators() -> tuple[str]:
        """Return all user  indicators names."""
        return Indicator.user_registry.all_registered()

    @staticmethod
    def show_supported_indicators():
        """Render the tree of all supported indicators."""
        Indicator.registry.render_tree()

    @staticmethod
    def show_user_indicators():
        """Render the tree of user indicators."""
        Indicator.user_registry.render_tree()