from abc import ABC, abstractmethod

import numpy as np
from pandas import DataFrame
from collections.abc import Iterable

from arcana.utils.classes_utils import validate_classes_names
from arcana.price_data.dev_types import PriceDataColumns
from .c_definitions import ma_lib
from .adapters import ma_prepare_data_to_c, ma_numpy_to_dataframe
from .cfg import *
from arcana.utils.RegistryTree import RegistryTree
from arcana.utils.df_utils import stack_data


class Indicator(ABC):
    """
    Abstract class for every indicator.

    """
    __slots__ = ()

    _registry = RegistryTree("Indicator")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        bases_names =  [base.name() for base in cls.__mro__[::-1] if base not in (ABC, object)]
        for i in range(1, len(bases_names)):
            cls._registry.add_key(bases_names[i], parent=bases_names[i-1])

    @classmethod
    @abstractmethod
    def compute(cls, *args, **kwargs):
        pass

    @classmethod
    def registered(cls):
        return cls._registry.render_tree()

    @classmethod
    def name(cls):
        return cls.__name__

class MovingAverage(Indicator):
    __slots__ = ()

    _user_moving_averages = RegistryTree("MovingAverage")

    @classmethod
    def compute(cls, df: list[DataFrame], * ,ma_cfg: MovingAverageCfg) -> list[DataFrame]:
        raise NotImplementedError

    @classmethod
    def calculate(cls, df: DataFrame, *, ma, src, period, user_name, extra: dict = None) -> DataFrame:
        data_to_prepare = dict()

        data = df[src].to_numpy(dtype=np.float64)
        ind = np.zeros_like(data)
        data_to_prepare["to_d_ptr"] = [data, ind]

        length = len(data)
        data_to_prepare["to_i"] = [length, period]

        if extra:
            for key, val in extra.items():
                if key not in data_to_prepare:
                    data_to_prepare[key] = []
                if not isinstance(val, Iterable):
                    data_to_prepare[key].append(val)
                else:
                    data_to_prepare[key].extend(val)
        print(data_to_prepare)
        res = ma_prepare_data_to_c(**data_to_prepare)
        ma(*res)

        symbol = df[PriceDataColumns.SYMBOL].iloc[0]
        ind = ma_numpy_to_dataframe(ind, df.index, symbol, user_name)
        return ind

    @classmethod
    def _validate_names(cls, other: IndicatorCfg):
        if other.name not in (cls.__name__, cls.__base__.__name__):
            raise ValueError(f"Cfg should be compatible with Indicator. For {cls.__name__} use {cls.__base__.__name__}Cfg")

    @classmethod
    def _register_user_moving_average(cls, family_name: str, name: str, ind_data: list[DataFrame]):
        cls._user_moving_averages.add_key(family_name)
        cls._user_moving_averages.add_key(name, parent=family_name, ind_data=ind_data)

    @classmethod
    def get_registered_user_moving_averages(cls):
        return cls._user_moving_averages.all_registered()

    @classmethod
    def show_registered_moving_averages(cls):
        return cls._user_moving_averages.render_tree()

    @classmethod
    def get_raw_data(cls, user_indicator_name: str):
        return cls._user_moving_averages.get_data(user_indicator_name, "ind_data")

    @classmethod
    def get_data(cls, user_indicator_name: str):
        raw_data = cls._user_moving_averages.get_data(user_indicator_name, "ind_data")
        symbols = [df[PriceDataColumns.SYMBOL].iloc[0] for df in raw_data]
        data = stack_data(raw_data, symbols)
        return data

class BaseMovingAverage(MovingAverage):
    __slots__ = ()
    ma = None

    @classmethod
    def compute(cls, df_list: list[DataFrame], *, ma_cfg: MovingAverageCfg) -> list[DataFrame]:
        validate_classes_names(cls.name(), ma_cfg.name)
        indicators = []
        for df in df_list:
            indicator = cls.calculate(df, ma=cls.ma, src=ma_cfg.src, period=ma_cfg.period, user_name=ma_cfg.user_name, extra=cls.extra(df=df, ma_cfg=ma_cfg))
            indicators.append(indicator)

        cls._register_user_moving_average(cls.__name__, ma_cfg.user_name, indicators)
        return indicators

    @staticmethod
    def extra(*, df, ma_cfg) -> dict:
        return dict()

class ExtraMovingAverage(BaseMovingAverage):
    __slots__ = ()

    @staticmethod
    def extra(*, df, ma_cfg) -> dict:
        raise NotImplementedError

class SMA(BaseMovingAverage):
    __slots__ = ()
    ma = ma_lib.sma

class ESMA(ExtraMovingAverage):
    __slots__ = ()
    ma = ma_lib.esma

    @staticmethod
    def extra(ma_cfg: ESMACfg, **kwargs):
        return {"to_d": ma_cfg.alpha}

class EMA(BaseMovingAverage):
    __slots__ = ()
    ma = ma_lib.ema

class WMA(BaseMovingAverage):
    __slots__ = ()
    ma = ma_lib.wma

class HMA(BaseMovingAverage):
    __slots__ = ()
    ma = ma_lib.hma

class RMA(BaseMovingAverage):
    __slots__ = ()
    ma = ma_lib.rma

class TEMA(BaseMovingAverage):
    __slots__ = ()
    ma = ma_lib.tema

class DEMA(BaseMovingAverage):
    __slots__ = ()
    ma = ma_lib.dema

class KAMA(ExtraMovingAverage):
    __slots__ = ()
    ma = ma_lib.kama

    @staticmethod
    def extra(ma_cfg: KAMACfg, **kwargs):
        return {"to_i": [ma_cfg.n_fast, ma_cfg.n_slow]}

class FRAMA(ExtraMovingAverage):
    __slots__ = ()
    ma = ma_lib.frama

    @staticmethod
    def extra(df: DataFrame, **kwargs):
        high = df[PriceDataColumns.HIGH].to_numpy(dtype=np.float64)
        low = df[PriceDataColumns.LOW].to_numpy(dtype=np.float64)
        return {"to_d_ptr": [high, low]}