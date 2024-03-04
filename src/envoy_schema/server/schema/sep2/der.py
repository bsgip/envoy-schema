from enum import IntEnum, IntFlag, auto
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
from envoy_schema.server.schema.sep2.identification import (
    ListLink,
    SubscribableIdentifiedObject,
    SubscribableList,
    SubscribableResource,
)
from envoy_schema.server.schema.sep2.pricing import PrimacyType


class DERType(IntEnum):
    NOT_APPLICABLE = 0
    VIRTUAL_OR_MIXED = 1
    RECIPROCATING_ENGINE = 2
    FUEL_CELL = 3
    PHOTOVOLTAIC_SYSTEM = 4
    COMBINED_HEAT_POWER = 5
    OTHER_GENERATION_SYSTEM = 6
    OTHER_STORAGE_SYSTEM = 80
    ELECTRIC_VEHICLE = 81
    EVSE = 82
    COMBINED_PV_AND_STORAGE = 83


class DERControlType(IntFlag):
    """Series of bit flags: Control modes supported by the DER"""

    CHARGE_MODE = auto()
    DISCHARGE_MODE = auto()
    OP_MOD_CONNECT = auto()  # Connect/Disconnect - implies galvanic isolation
    OP_MOD_ENERGIZE = auto()  # Energize/De-Energize
    OP_MOD_FIXED_PF_ABSORB_W = auto()  # Fixed Power Factor Setpoint when absorbing active power
    OP_MOD_FIXED_PF_INJECT_W = auto()  # Fixed Power Factor Setpoint when injecting active power
    OP_MOD_FIXED_VAR = auto()  # Reactive power setpoint
    OP_MOD_FIXED_W = auto()  # Charge / Discharge Setpoint
    OP_MOD_FREQ_DROOP = auto()  # Frequency-Watt Parameterized Mode
    OP_MOD_FREQ_WATT = auto()  # Frequency-Watt Curve Mode
    OP_MOD_HFRT_MAY_TRIP = auto()  # High Frequency Ride Through, May Trip Mode
    OP_MOD_HFRT_MUST_TRIP = auto()  # High Frequency Ride Through, Must Trip Mode
    OP_MOD_HVRT_MAY_TRIP = auto()  # High Voltage Ride Through, May Trip Mode
    OP_MOD_HVRT_MOMENTARY_CESSATION = auto()  # High Frequency Ride Through, Momentary cessation Mode
    OP_MOD_HVRT_MUST_TRIP = auto()  # High Voltage Ride Through, Must Trip Mode
    OP_MOD_LFRT_MAY_TRIP = auto()  # Low Frequency Ride Through, May Trip Mode
    OP_MOD_LFRT_MUST_TRIP = auto()  # Low Frequency Ride Through, Must Trip Mode
    OP_MOD_LVRT_MAY_TRIP = auto()  # Low Voltage Ride Through, May Trip Mode
    OP_MOD_LVRT_MOMENTARY_CESSATION = auto()  # Low Frequency Ride Through, Momentary cessation Mode
    OP_MOD_LVRT_MUST_TRIP = auto()  # Low Voltage Ride Through, Must Trip Mode
    OP_MOD_MAX_LIM_W = auto()  # Maximum Active Power
    OP_MOD_TARGET_VAR = auto()  # Target Reactive Power
    OP_MOD_TARGET_W = auto()  # Target Active Power
    OP_MOD_VOLT_VAR = auto()  # Volt-Var Mode
    OP_MOD_VOLT_WATT = auto()  # Volt-Watt Mode
    OP_MOD_WATT_PF = auto()  # Watt-PowerFactor Mode
    OP_MOD_WATT_VAR = auto()  # Watt-Var Mode


class InverterStatusType(IntEnum):
    """DER InverterStatus value"""

    NOT_APPLICABLE = 0
    OFF = 1
    SLEEPING = 2  # sleeping (auto-shutdown) or DER is at low output power/voltage
    STARTING = 3  # starting up or ON but not producing power
    TRACKING_MPPT_POWER_POINT = 4  # tracking MPPT power point
    FORCED_POWER_REDUCTION = 5  # forced power reduction/derating
    SHUTTING_DOWN = 6
    ONE_OR_MORE_FAULTS = 7
    STANDBY = 8  # standby (service on unit) - DER may be at high output voltage/power
    TEST_MODE = 9
    MANUFACTURER_STATUS = 10  # as defined in manufacturer status


class OperationalModeStatusType(IntEnum):
    """DER OperationalModeStatus value"""

    NOT_APPLICABLE = 0
    OFF = 1
    OPERATIONAL_MODEL = 2
    TEST_MODE = 3


class StorageModeStatusType(IntEnum):
    """DER StorageModeStatus value"""

    STORAGE_CHARGING = 0
    STORAGE_DISCHARGING = 1
    STORAGE_HOLDING = 2


class LocalControlModeStatusType(IntEnum):
    """DER LocalControlModeStatus/value"""

    LOCAL_CONTROL = 0
    REMOTE_CONTROL = 1


class ConnectStatusType(IntFlag):
    """Bit map of DER ConnectStatus values"""

    CONNECTED = auto()
    AVAILABLE = auto()
    OPERATING = auto()
    TEST = auto()
    FAULT_ERROR = auto()


class AlarmStatusType(IntFlag):
    """Bitmap indicating the status of DER alarms (see DER LogEvents for more details)."""

    DER_FAULT_OVER_CURRENT = auto()
    DER_FAULT_OVER_VOLTAGE = auto()
    DER_FAULT_UNDER_VOLTAGE = auto()
    DER_FAULT_OVER_FREQUENCY = auto()
    DER_FAULT_UNDER_FREQUENCY = auto()
    DER_FAULT_VOLTAGE_IMBALANCE = auto()
    DER_FAULT_CURRENT_IMBALANCE = auto()
    DER_FAULT_EMERGENCY_LOCAL = auto()
    DER_FAULT_EMERGENCY_REMOTE = auto()
    DER_FAULT_LOW_POWER_INPUT = auto()
    DER_FAULT_PHASE_ROTATION = auto()


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


class DER(SubscribableResource):
    """sep2 DER: Contains links to DER resources."""

    AssociatedUsagePointLink: Optional[Link]  # If present, this is the submeter that monitors the DER output.
    AssociatedDERProgramListLink: Optional[ListLink]  # Link to List of DERPrograms having the DERControls for this DER
    CurrentDERProgramLink: Optional[Link]  # If set, this is the DERProgram containing the currently active DERControl
    DERStatusLink: Optional[Link]  # SHALL contain a Link to an instance of DERStatus.
    DERCapabilityLink: Optional[Link]  # SHALL contain a Link to an instance of DERCapability.
    DERSettingsLink: Optional[Link]  # SHALL contain a Link to an instance of DERSettings.
    DERAvailabilityLink: Optional[Link]  # SHALL contain a Link to an instance of DERAvailability.


class ConnectStatusTypeValue(BaseXmlModelWithNS):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: primitive_types.HexBinary8 = element()  # Should have bits set from ConnectStatusType


class InverterStatusTypeValue(BaseXmlModelWithNS):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: InverterStatusType = element()


class LocalControlModeStatusTypeValue(BaseXmlModelWithNS):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: LocalControlModeStatusType = element()


class OperationalModeStatusTypeValue(BaseXmlModelWithNS):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: OperationalModeStatusType = element()


class StorageModeStatusTypeValue(BaseXmlModelWithNS):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: StorageModeStatusType = element()


class ManufacturerStatusValue(BaseXmlModelWithNS):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: primitive_types.String6  # The manufacturer status value


class StateOfChargeStatusValue(BaseXmlModelWithNS):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: types.PerCent = element()


class DERStatus(SubscribableResource):
    """DER status information"""

    alarmStatus: Optional[primitive_types.HexBinary32] = element(default=None)  # AlarmStatusType encoded HexBinary str
    genConnectStatus: Optional[ConnectStatusTypeValue] = element(default=None)  # Connection status for generator
    inverterStatus: Optional[InverterStatusTypeValue] = element(default=None)
    localControlModeStatus: Optional[LocalControlModeStatusTypeValue] = element(default=None)
    manufacturerStatus: Optional[ManufacturerStatusValue] = element(default=None)
    operationalModeStatus: Optional[OperationalModeStatusTypeValue] = element(default=None)
    readingTime: types.TimeType = element()
    stateOfChargeStatus: Optional[StateOfChargeStatusValue] = element(default=None)
    storageModeStatus: Optional[StorageModeStatusTypeValue] = element(default=None)
    storConnectStatus: Optional[ConnectStatusTypeValue] = element(default=None)  # Connection status for storage
