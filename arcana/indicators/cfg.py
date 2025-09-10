from dataclasses import field

import attrs

from .converters import src_converter


@attrs.define(slots=True, kw_only=True)
class IndicatorCfg:
    user_name = attrs.field(validator=attrs.validators.instance_of(str))

    @property
    def name(self):
        return self.__class__.__name__.removesuffix("Cfg")


@attrs.define(slots=True, kw_only=True)
class MovingAverageCfg(IndicatorCfg):
    src = attrs.field(validator=attrs.validators.instance_of(str), converter=src_converter)
    period = attrs.field(validator=[attrs.validators.instance_of(int), attrs.validators.gt(0)])

@attrs.define(slots=True, kw_only=True)
class SMACfg(MovingAverageCfg):
    pass

@attrs.define(slots=True, kw_only=True)
class ESMACfg(MovingAverageCfg):
    alpha = attrs.field(validator=[attrs.validators.instance_of(float), attrs.validators.gt(0.0)])

@attrs.define(slots=True, kw_only=True)
class EMACfg(MovingAverageCfg):
    pass

@attrs.define(slots=True, kw_only=True)
class WMACfg(MovingAverageCfg):
    pass

@attrs.define(slots=True, kw_only=True)
class HMACgf(MovingAverageCfg):
    pass

@attrs.define(slots=True, kw_only=True)
class RMACfg(MovingAverageCfg):
    pass

@attrs.define(slots=True, kw_only=True)
class TEMACfg(MovingAverageCfg):
    pass

@attrs.define(slots=True, kw_only=True)
class DEMACfg(MovingAverageCfg):
    pass

@attrs.define(slots=True, kw_only=True)
class KAMACfg(MovingAverageCfg):
    n_fast = attrs.field(validator=attrs.validators.instance_of(int))
    n_slow = attrs.field(validator=attrs.validators.instance_of(int))

@attrs.define(slots=True, kw_only=True)
class FRAMACfg(MovingAverageCfg):
    pass
