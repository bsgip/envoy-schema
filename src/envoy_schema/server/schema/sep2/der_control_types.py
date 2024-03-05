from pydantic_xml import element

from envoy_schema.server.schema.sep2 import types
from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS


class FixedVar(BaseXmlModelWithNS):
    """Specifies a signed setpoint for reactive power."""

    refType: types.DERUnitRefType = element()  # Signed setpoint for reactive power
    value: types.SignedPerCent = element()  # Specify a signed setpoint for reactive power in %


class PowerFactorWithExcitation(BaseXmlModelWithNS):
    """Specifies a setpoint for Displacement Power Factor, the ratio between apparent and active powers at the
    fundamental frequency (e.g. 60 Hz) and includes an excitation flag."""

    displacement: int = element()  # Significand of an unsigned value of cos(theta) between 0 and 1.0.
    excitation: bool = element()  # True = DER absorbing, False = DER injecting reactive power
    multiplier: int = element()  # Specifies exponent of 'displacement'.


class PowerFactor(BaseXmlModelWithNS):
    """Specifies a setpoint for Displacement Power Factor, the ratio between apparent and active powers at the
    fundamental frequency (e.g. 60 Hz)."""

    displacement: int = (
        element()
    )  # A setpoint for Displacement PF, the ratio between apparent/active powers at the fundamental frequency eg: 60 Hz
    multiplier: int = element()  # Specifies exponent of 'displacement'.


class ReactivePower(BaseXmlModelWithNS):
    """The reactive power Q"""

    value: int = element()  # Value in volt-amperes reactive (var) (uom 63)
    multiplier: int = element()  # Specifies exponent of 'value'.


class ActivePower(BaseXmlModelWithNS):
    """The active/real power P"""

    value: int = element()  # Value in volt-amperes reactive (var) (uom 63)
    multiplier: int = element()  # Specifies exponent of 'value'.


class CurrentRMS(BaseXmlModelWithNS):
    """Average flow of charge through a conductor."""

    value: int = element()  # Value in amperes RMS (uom 5)
    multiplier: int = element()  # Specifies exponent of 'value'.


class VoltageRMS(BaseXmlModelWithNS):
    """Average electric potential difference between two points."""

    value: int = element()  # Value in volts RMS (uom 29)
    multiplier: int = element()  # Specifies exponent of 'value'.


class AmpereHour(BaseXmlModelWithNS):
    """Available electric charge"""

    value: int = element()  # Value in ampere-hours (uom 106)
    multiplier: int = element()  # Specifies exponent of 'value'.


class WattHour(BaseXmlModelWithNS):
    """Active (real) energy"""

    value: int = element()  # Value in watt-hours (uom 72)
    multiplier: int = element()  # Specifies exponent of 'value'.


class ApparentPower(BaseXmlModelWithNS):
    """The apparent power S (in VA) is the product of root mean square (RMS) voltage and RMS current."""

    value: int = element()  # Value in volt-amperes (uom 61)
    multiplier: int = element()  # Specifies exponent of 'value'.


class ReactiveSusceptance(BaseXmlModelWithNS):
    """Reactive susceptance"""

    value: int = element()  # Value in siemens (uom 53)
    multiplier: int = element()  # Specifies exponent of 'value'.
