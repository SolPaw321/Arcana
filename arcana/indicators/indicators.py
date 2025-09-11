from abc import ABC, abstractmethod
from typing import Type
import numpy as np
from pandas import DataFrame
from collections.abc import Iterable

from arcana.utils.classes_utils import validate_classes_names
from arcana.price_data.dev_types import PriceDataColumns
from .c_definitions import ma_lib
from .adapters import ma_prepare_data_to_c, ma_numpy_to_dataframe
from .cfg import *
from arcana.utils.RegistryTree import RegistryTree


class Indicator(ABC):
    """
    Abstract base class for all indicators.

    Each subclass of `Indicator` is automatically registered
    in a hierarchical registry tree (`RegistryTree`).

    Attributes
    ----------
    registry : RegistryTree
        Registry containing the inheritance tree of all defined indicators.
    """
    __slots__ = ()
    registry = RegistryTree("Indicator")
    user_registry = RegistryTree("Indicator")

    def __init_subclass__(cls, **kwargs):
        """
        Automatically called when a subclass of `Indicator` is created.
        Adds the new subclass into the registry tree according to its MRO.
        """
        super().__init_subclass__(**kwargs)
        bases_names =  [base.name() for base in cls.__mro__[::-1] if base not in (ABC, object) and not base.name().endswith("_")]
        for i in range(1, len(bases_names)):
            cls.registry.add_key(bases_names[i], parent=bases_names[i - 1])

    @classmethod
    @abstractmethod
    def compute(cls, *args, **kwargs):
        """
        Abstract method to compute an indicator.

        Must be implemented by subclasses.

        Returns
        -------
        Any
            Indicator result (usually a pandas DataFrame).
        """

    @classmethod
    def name(cls) -> str:
        """Return the class name of the indicator."""
        return cls.__name__

class MovingAverage(Indicator):
    """
    Abstract base class for all moving averages.
    Handles data preparation, validation, and registry for user-defined indicators.

    Attributes
    ----------
    user_registry : RegistryTree
        Stores registered user-defined moving averages.
    """
    __slots__ = ()

    Indicator.user_registry.add_key("MovingAverage", parent="Indicator")

    @classmethod
    def compute(cls, df: list[DataFrame], * ,ma_cfg: MovingAverageCfg) -> list[DataFrame]:
        """
        Abstract method for computing moving averages on a list of DataFrames.
        This method is a driver for calculation method.

        Parameters
        ----------
        df : list[pandas.DataFrame]
            List of OHLCV data.
        ma_cfg : MovingAverageCfg
            Configuration object for the moving average.

        Returns
        -------
        list[pandas.DataFrame]
            List of DataFrames containing computed indicator.
        """
        raise NotImplementedError

    @classmethod
    def calculate(cls, df: DataFrame, *, ma, src, period, user_name, extra: dict = None) -> DataFrame:
        """
        Prepare data, call the C backend function, and return the result as DataFrame.

        Parameters
        ----------
        df : DataFrame
            Input OHLCV data.
        ma : Callable
            C function implementing the moving average.
        src : str
            Column name used as source data (e.g. "close").
        period : int
            Period (window) of the moving average.
        user_name : str
            Name under which the indicator will be registered.
        extra : dict, optional
            Additional parameters passed to the C function.

        Returns
        -------
        DataFrame
            Pandas DataFrame containing the calculated indicator values.
        """
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
        res = ma_prepare_data_to_c(**data_to_prepare)
        ma(*res)

        symbol = df[PriceDataColumns.SYMBOL].iloc[0]
        ind = ma_numpy_to_dataframe(ind, df.index, symbol, user_name)
        return ind

    @classmethod
    def _validate_names(cls, other: IndicatorCfg):
        """Ensure that configuration name matches expected class family."""
        if other.name not in (cls.__name__, cls.__base__.__name__):
            raise ValueError(f"Cfg should be compatible with Indicator. For {cls.__name__} use {cls.__base__.__name__}Cfg")


class BaseMovingAverage_(MovingAverage):
    """Base implementation of a moving average that integrates with the C backend."""
    __slots__ = ()
    ma = None

    @classmethod
    def compute(cls, df_list: list[DataFrame], *, ma_cfg: MovingAverageCfg) -> list[DataFrame]:
        """
        Compute moving average for each OHLCV data in the input list.

        Validates class name against config, runs calculation,
        and registers the result.

        Parameters
        ----------
        df_list : list[pandas.DataFrame]
            List of OHLCV DataFrames.
        ma_cfg : MovingAverageCfg
            Configuration object containing parameters for computation.

        Returns
        -------
        list[pandas.DataFrame]
            List of DataFrames with computed moving average values.
        """
        validate_classes_names(cls.name(), ma_cfg.name)
        indicators = []
        for df in df_list:
            indicator = cls.calculate(df, ma=cls.ma, src=ma_cfg.src, period=ma_cfg.period, user_name=ma_cfg.user_name, extra=cls.extra(df=df, ma_cfg=ma_cfg))
            indicators.append(indicator)

        cls.user_registry.add_key(ma_cfg.user_name, parent="MovingAverage", raw_data=indicators)
        return indicators

    @staticmethod
    def extra(*, df, ma_cfg) -> dict:
        """Return extra parameters required by some indicators (default: empty)."""
        return dict()

class ExtraMovingAverage_(BaseMovingAverage_):
    """
    Abstract base for moving averages that require additional parameters.
    Subclasses must implement `extra` method.
    """
    __slots__ = ()

    @staticmethod
    def extra(*, df, ma_cfg) -> dict:
        raise NotImplementedError

class SMA(BaseMovingAverage_):
    """Simple Moving Average (SMA)."""
    __slots__ = ()
    ma = ma_lib.sma
    is_in_registry = True

class ESMA(ExtraMovingAverage_):
    __slots__ = ()
    ma = ma_lib.esma

    @staticmethod
    def extra(ma_cfg: ESMACfg, **kwargs):
        return {"to_d": ma_cfg.alpha}

class EMA(BaseMovingAverage_):
    __slots__ = ()
    ma = ma_lib.ema

class WMA(BaseMovingAverage_):
    __slots__ = ()
    ma = ma_lib.wma

class HMA(BaseMovingAverage_):
    __slots__ = ()
    ma = ma_lib.hma

class RMA(BaseMovingAverage_):
    __slots__ = ()
    ma = ma_lib.rma

class TEMA(BaseMovingAverage_):
    __slots__ = ()
    ma = ma_lib.tema

class DEMA(BaseMovingAverage_):
    __slots__ = ()
    ma = ma_lib.dema

class KAMA(ExtraMovingAverage_):
    __slots__ = ()
    ma = ma_lib.kama

    @staticmethod
    def extra(ma_cfg: KAMACfg, **kwargs):
        return {"to_i": [ma_cfg.n_fast, ma_cfg.n_slow]}

class FRAMA(ExtraMovingAverage_):
    __slots__ = ()
    ma = ma_lib.frama

    @staticmethod
    def extra(df: DataFrame, **kwargs):
        high = df[PriceDataColumns.HIGH].to_numpy(dtype=np.float64)
        low = df[PriceDataColumns.LOW].to_numpy(dtype=np.float64)
        return {"to_d_ptr": [high, low]}