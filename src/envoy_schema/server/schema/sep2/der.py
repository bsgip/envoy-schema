from typing import Optional

from pydantic_xml import element

from envoy_schema.server.schema.sep2 import primitive_types, types
from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.der_control_types import (
    ActivePower,
    FixedVar,
    PowerFactorWithExcitation,
    ReactivePower,
)
from envoy_schema.server.schema.sep2.event import RandomizableEvent
from envoy_schema.server.schema.sep2.identification import IdentifiedObject, Link
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.identification import ListLink, SubscribableIdentifiedObject, SubscribableList
from envoy_schema.server.schema.sep2.pricing import PrimacyType


class DERControlBase(BaseXmlModelWithNS):
    """Distributed Energy Resource (DER) control values."""

    opModConnect: Optional[bool] = element(default=None)  # Set DER as connected (true) or disconnected (false).
    opModEnergize: Optional[bool] = element(default=None)  # Set DER as energized (true) or de-energized (false).
    opModFixedPFAbsorbW: Optional[PowerFactorWithExcitation] = element(
        default=None
    )  # requested PF when AP is being absorbed
    opModFixedPFInjectW: Optional[PowerFactorWithExcitation] = element(
        default=None
    )  # requested PF when AP is being injected
    opModFixedVar: Optional[FixedVar] = element(default=None)  # specifies the delivered or received RP setpoint.
    opModFixedW: Optional[types.SignedPerCent] = element(
        default=None
    )  # specifies a requested charge/discharge mode setpoint
    opModFreqDroop: Optional[int] = element(default=None)  # Specifies a frequency-watt operation
    opModFreqWatt: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 0
    opModHFRTMayTrip: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 1
    opModHFRTMustTrip: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 2
    opModHVRTMayTrip: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 3
    opModHVRTMomentaryCessation: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 4
    opModHVRTMustTrip: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 5
    opModLFRTMayTrip: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 6
    opModLFRTMustTrip: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 7
    opModLVRTMayTrip: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 8
    opModLVRTMomentaryCessation: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 9
    opModLVRTMustTrip: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 10
    opModMaxLimW: Optional[types.PerCent] = element(
        default=None
    )  # max active power generation level at electrical coupling point
    opModTargetVar: Optional[ReactivePower] = element(default=None)  # Target reactive power, in var
    opModTargetW: Optional[ActivePower] = element(default=None)  # Target active power, in Watts
    opModVoltVar: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 11
    opModVoltWatt: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 12
    opModWattPF: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 13
    opModWattVar: Optional[Link] = element(default=None)  # Specify DERCurveLink for curveType == 14
    rampTms: Optional[int] = element(default=None)  # Requested ramp time, in hundredths of a second

    # CSIP Aus Extensions (encoded here as it makes decoding a whole lot simpler)
    opModImpLimW: Optional[ActivePower] = element(
        ns="csipaus", default=None
    )  # constraint on the imported AP at the connection point
    opModExpLimW: Optional[ActivePower] = element(
        ns="csipaus", default=None
    )  # constraint on the exported AP at the connection point
    opModGenLimW: Optional[ActivePower] = element(
        ns="csipaus", default=None
    )  # max limit on discharge watts for a single DER
    opModLoadLimW: Optional[ActivePower] = element(
        ns="csipaus", default=None
    )  # max limit on charge watts for a single DER


class DefaultDERControl(SubscribableIdentifiedObject):
    """Contains control mode information to be used if no active DERControl is found."""

    setESDelay: Optional[int] = element(default=None)  # Enter service delay, in hundredths of a second.
    setESHighFreq: Optional[int] = element(default=None)  # Enter service frequency high. Specified in hundredths of Hz
    setESHighVolt: Optional[int] = element(
        default=None
    )  # Enter service voltage high. Specified as an effective percent voltage,
    setESLowFreq: Optional[int] = element(default=None)  # Enter service frequency low. Specified in hundredths of Hz
    setESLowVolt: Optional[int] = element(
        default=None
    )  # Enter service voltage low. Specified as an effective percent voltage,
    setESRampTms: Optional[int] = element(default=None)  # Enter service ramp time, in hundredths of a second
    setESRandomDelay: Optional[int] = element(
        default=None
    )  # Enter service randomized delay, in hundredths of a second.
    setGradW: Optional[int] = element(default=None)  # Set default rate of change (ramp rate) of active power output
    setSoftGradW: Optional[int] = element(
        default=None
    )  # Set soft-start rate of change (soft-start ramp rate) of AP output
    DERControlBase_: DERControlBase = element(tag="DERControlBase")


class DERControlResponse(RandomizableEvent, tag="DERControl"):
    """Distributed Energy Resource (DER) time/event-based control."""

    deviceCategory: Optional[primitive_types.HexBinary32] = element(
        default=None
    )  # the bitmap indicating device categories that SHOULD respond.
    DERControlBase_: DERControlBase = element(tag="DERControlBase")


class DERControlListResponse(SubscribableList, tag="DERControlList"):
    DERControl: Optional[list[DERControlResponse]] = element(default=None)


class DERProgramResponse(SubscribableIdentifiedObject, tag="DERProgram"):
    """sep2 DERProgram"""

    primacy: PrimacyType = element()
    DefaultDERControlLink: Optional[Link] = element(default=None)
    ActiveDERControlListLink: Optional[ListLink] = element(default=None)
    DERControlListLink: Optional[ListLink] = element(default=None)
    DERCurveListLink: Optional[ListLink] = element(default=None)


class DERProgramListResponse(SubscribableList, tag="DERProgramList"):
    DERProgram: Optional[list[DERProgramResponse]] = element(default=None)
    pollRate: Optional[int] = element(
        default=None
    )  # The default polling rate for this resource and all resources below in seconds


class DemandResponseProgramResponse(IdentifiedObject, tag="DemandResponseProgram"):
    """sep2 Demand response program"""

    availabilityUpdatePercentChangeThreshold: Optional[types.PerCent] = element(default=None)
    availabilityUpdatePowerChangeThreshold: Optional[ActivePower] = element(default=None)
    primacy: PrimacyType = element()
    ActiveEndDeviceControlListLink: Optional[ListLink] = element(default=None)
    EndDeviceControlListLink: Optional[ListLink] = element(default=None)


class DemandResponseProgramListResponse(Sep2List, tag="DemandResponseProgramList"):
    DemandResponseProgram: list[DemandResponseProgramResponse] = element(default_factory=list)


class EndDeviceControlResponse(RandomizableEvent, tag="EndDeviceControl"):
    """Instructs an EndDevice to perform a specified action."""

    deviceCategory: types.DeviceCategory = element()
    drProgramMandatory: bool = element()
    loadShiftForward: bool = element()
    overrideDuration: Optional[int] = element(default=None)
