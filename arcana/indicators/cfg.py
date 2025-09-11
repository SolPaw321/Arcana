from dataclasses import field

import attrs

from .converters import src_converter


@attrs.define(slots=True, kw_only=True)
class IndicatorCfg:
    """Configuration base class for every indicator."""
    user_name = attrs.field(validator=attrs.validators.instance_of(str))

    @property
    def name(self):
        """Return the configuration name."""
        return self.__class__.__name__.removesuffix("Cfg")


@attrs.define(slots=True, kw_only=True)
class MovingAverageCfg(IndicatorCfg):
    """Configuration base class for every moving average indicator."""
    src = attrs.field(validator=attrs.validators.instance_of(str), converter=src_converter)
    period = attrs.field(validator=[attrs.validators.instance_of(int), attrs.validators.gt(0)])

@attrs.define(slots=True, kw_only=True)
class SMACfg(MovingAverageCfg):
    """Configuration for Simple Moving Average (SMA)."""
    pass

@attrs.define(slots=True, kw_only=True)
class ESMACfg(MovingAverageCfg):
    """Configuration for ???"""
    alpha = attrs.field(validator=[attrs.validators.instance_of(float), attrs.validators.gt(0.0)])

@attrs.define(slots=True, kw_only=True)
class EMACfg(MovingAverageCfg):
    """Configuration for Exponential Moving Average (EMA)."""
    pass

@attrs.define(slots=True, kw_only=True)
class WMACfg(MovingAverageCfg):
    """Configuration for Weighted Moving Average (WMA)."""
    pass

@attrs.define(slots=True, kw_only=True)
class HMACgf(MovingAverageCfg):
    """Configuration for Hull Moving Average (HMA)."""
    pass

@attrs.define(slots=True, kw_only=True)
class RMACfg(MovingAverageCfg):
    """Configuration for Rolling Moving Average (RMA)."""
    pass

@attrs.define(slots=True, kw_only=True)
class TEMACfg(MovingAverageCfg):
    """Configuration for Triple Exponential Moving Average (TEMA)."""
    pass

@attrs.define(slots=True, kw_only=True)
class DEMACfg(MovingAverageCfg):
    """Configuration for Double Exponential Moving Average (DEAMA)."""
    pass

@attrs.define(slots=True, kw_only=True)
class KAMACfg(MovingAverageCfg):
    """Configuration for Kaufman Adaptive Moving Average (KAMA)."""
    n_fast = attrs.field(validator=attrs.validators.instance_of(int))
    n_slow = attrs.field(validator=attrs.validators.instance_of(int))

@attrs.define(slots=True, kw_only=True)
class FRAMACfg(MovingAverageCfg):
    """Configuration for Fractal Adaptive Moving Average (FRAMA)."""
    pass
