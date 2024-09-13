from enum import IntEnum, IntFlag, auto
from typing import Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import primitive_types, types
from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.der_control_types import (
    ActivePower,
    AmpereHour,
    ApparentPower,
    CurrentRMS,
    FixedVar,
    PowerFactor,
    PowerFactorWithExcitation,
    ReactivePower,
    ReactiveSusceptance,
    VoltageRMS,
    WattHour,
)
from envoy_schema.server.schema.sep2.event import RandomizableEvent
from envoy_schema.server.schema.sep2.identification import IdentifiedObject, Link
from envoy_schema.server.schema.sep2.identification import List
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


class AbnormalCategoryType(IntEnum):
    """Abnormal operating performance category as defined by IEEE 1547-2018. One of:"""

    NOT_SPECIFIED = 0
    CATEGORY_1 = 1
    CATEGORY_2 = 2
    CATEGORY_3 = 3


class NormalCategoryType(IntEnum):
    """Normal operating performance category as defined by IEEE 1547-2018."""

    NOT_SPECIFIED = 0
    CATEGORY_A = 1
    CATEGORY_B = 2


class DOESupportedMode(IntFlag):
    """Series of bit flags: What CSIP Aus DOE capabilities are enabled"""

    OP_MOD_EXPORT_LIMIT_W = auto()
    OP_MOD_IMPORT_LIMIT_W = auto()
    OP_MOD_GENERATION_LIMIT_W = auto()
    OP_MOD_LOAD_LIMIT_W = auto()


class FreqDroopType(BaseXmlModelWithNS):
    """Type for Frequency-Droop (Frequency-Watt) operation."""

    dBOF: int = element()  # Frequency droop dead band for over-frequency conditions.
    dBUF: int = element()  # Frequency droop dead band for under-frequency conditions.
    kOF: int = element()  # droop per-unit frequency change OF conditions corresponding to 1 power output change.
    kUF: int = element()  # # droop per-unit frequency change UF conditions corresponding to 1 power output change.
    openLoopTms: int = element()  # Open loop response time


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
    opModFreqDroop: Optional[FreqDroopType] = element(default=None)  # Specifies a frequency-watt operation
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

    DERControlBase_: DERControlBase = element(tag="DERControlBase")
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


class DERControlResponse(RandomizableEvent, tag="DERControl"):
    """Distributed Energy Resource (DER) time/event-based control."""

    DERControlBase_: DERControlBase = element(tag="DERControlBase")
    deviceCategory: Optional[primitive_types.HexBinary32] = element(
        default=None,
    )  # the bitmap indicating device categories that SHOULD respond.


class DERControlListResponse(SubscribableList, tag="DERControlList"):
    DERControl: Optional[list[DERControlResponse]] = element(default=None)


class DERProgramResponse(SubscribableIdentifiedObject, tag="DERProgram"):
    """sep2 DERProgram"""

    ActiveDERControlListLink: Optional[ListLink] = element(default=None)
    DefaultDERControlLink: Optional[Link] = element(default=None)
    DERControlListLink: Optional[ListLink] = element(default=None)
    DERCurveListLink: Optional[ListLink] = element(default=None)
    primacy: PrimacyType = element()


class DERProgramListResponse(SubscribableList, tag="DERProgramList"):
    DERProgram: Optional[list[DERProgramResponse]] = element(default=None)
    pollRate: Optional[int] = attr(
        default=None
    )  # The default polling rate for this resource and all resources below in seconds


class DemandResponseProgramResponse(IdentifiedObject, tag="DemandResponseProgram"):
    """sep2 Demand response program"""

    ActiveEndDeviceControlListLink: Optional[ListLink] = element(default=None)
    availabilityUpdatePercentChangeThreshold: Optional[types.PerCent] = element(default=None)
    availabilityUpdatePowerChangeThreshold: Optional[ActivePower] = element(default=None)
    EndDeviceControlListLink: Optional[ListLink] = element(default=None)
    primacy: PrimacyType = element()


class DemandResponseProgramListResponse(Sep2List, tag="DemandResponseProgramList"):
    DemandResponseProgram: list[DemandResponseProgramResponse] = element(default_factory=list)


class EndDeviceControlResponse(RandomizableEvent, tag="EndDeviceControl"):
    """Instructs an EndDevice to perform a specified action."""

    deviceCategory: primitive_types.HexBinary32 = element()  # HexBinary Encoded types.DeviceCategory enum
    drProgramMandatory: bool = element()
    loadShiftForward: bool = element()
    overrideDuration: Optional[int] = element(default=None)


class DER(SubscribableResource):
    """sep2 DER: Contains links to DER resources."""

    AssociatedDERProgramListLink: Optional[ListLink] = element(
        default=None
    )  # Link to List of DERPrograms having the DERControls for this DER
    AssociatedUsagePointLink: Optional[Link] = element(
        default=None
    )  # If present, this is the submeter that monitors the DER output.

    CurrentDERProgramLink: Optional[Link] = element(
        default=None
    )  # If set, this is the DERProgram containing the currently active DERControl

    DERAvailabilityLink: Optional[Link] = element(
        default=None
    )  # SHALL contain a Link to an instance of DERAvailability.
    DERCapabilityLink: Optional[Link] = element(default=None)  # SHALL contain a Link to an instance of DERCapability.
    DERSettingsLink: Optional[Link] = element(default=None)  # SHALL contain a Link to an instance of DERSettings.

    DERStatusLink: Optional[Link] = element(default=None)  # SHALL contain a Link to an instance of DERStatus.


class ConnectStatusTypeValue(BaseXmlModelWithNS, tag="ConnectStatusType"):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: primitive_types.HexBinary8 = element()  # Should have bits set from ConnectStatusType


class InverterStatusTypeValue(BaseXmlModelWithNS, tag="InverterStatusType"):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: InverterStatusType = element()


class LocalControlModeStatusTypeValue(BaseXmlModelWithNS, tag="LocalControlModeStatusType"):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: LocalControlModeStatusType = element()


class OperationalModeStatusTypeValue(BaseXmlModelWithNS, tag="OperationalModeStatusType"):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: OperationalModeStatusType = element()


class StorageModeStatusTypeValue(BaseXmlModelWithNS, tag="StorageModeStatusType"):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: StorageModeStatusType = element()


class ManufacturerStatusValue(BaseXmlModelWithNS, tag="ManufacturerStatusType"):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: primitive_types.String6 = element()  # The manufacturer status value


class StateOfChargeStatusValue(BaseXmlModelWithNS, tag="StateOfChargeStatusType"):
    dateTime: types.TimeType = element()  # The date and time at which the state applied.
    value: types.PerCent = element()


class DERStatus(SubscribableResource):
    """DER status information"""

    # Pydantic looks for tags in subclasses if one isnt explicitly defined. Hence redundant tags are placed here,
    # e.g. genConnectStatus, otherwise they will be renamed. Removing the tags in the subclasses would remove them
    # from xsd validation

    alarmStatus: Optional[primitive_types.HexBinary32] = element(default=None)  # AlarmStatusType encoded HexBinary str
    genConnectStatus: Optional[ConnectStatusTypeValue] = element(
        default=None, tag="genConnectStatus"
    )  # Connection status for generator
    inverterStatus: Optional[InverterStatusTypeValue] = element(default=None, tag="inverterStatus")
    localControlModeStatus: Optional[LocalControlModeStatusTypeValue] = element(
        default=None, tag="localControlModeStatus"
    )
    manufacturerStatus: Optional[ManufacturerStatusValue] = element(default=None, tag="manufacturerStatus")
    operationalModeStatus: Optional[OperationalModeStatusTypeValue] = element(default=None, tag="operationalModeStatus")
    readingTime: types.TimeType = element()
    stateOfChargeStatus: Optional[StateOfChargeStatusValue] = element(default=None, tag="stateOfChargeStatus")
    storageModeStatus: Optional[StorageModeStatusTypeValue] = element(default=None, tag="storageModeStatus")
    storConnectStatus: Optional[ConnectStatusTypeValue] = element(
        default=None, tag="storConnectStatus"
    )  # Connection status for storage


class DERAvailability(SubscribableResource):
    """Indicates current reserve generation status"""

    availabilityDuration: Optional[int] = element(
        default=None
    )  # Indicates number of seconds the DER will be able to deliver active power at the reservePercent level.
    maxChargeDuration: Optional[int] = element(
        default=None
    )  # Indicates number of seconds the DER will be able to receive active power at the reserveChargePercent level.
    readingTime: types.TimeType = element()  # The timestamp when the DER availability was last updated.
    reserveChargePercent: Optional[types.PerCent] = element(
        default=None
    )  # Percent of continuous received active power (%setMaxChargeRateW) that is estimated to be available in reserve.
    reservePercent: Optional[types.PerCent] = element(
        default=None
    )  # Percent of continuous delivered active power (%setMaxW) that is estimated to be available in reserve.
    statVarAvail: Optional[ReactivePower] = element(
        default=None
    )  # Estimated reserve reactive power, in var.  Represents the lesser of received or delivered reactive power.
    statWAvail: Optional[ActivePower] = element(default=None)  # Estimated reserve active power, in watts.


class DERCapability(SubscribableResource):
    """Distributed energy resource type and nameplate ratings. Intentionally differs from sep which is defined with a
    Resource base class rather than SubscribableResource."""

    modesSupported: primitive_types.HexBinary32 = element()  # HexBinary encoded DERControlType flags
    rtgAbnormalCategory: Optional[AbnormalCategoryType] = element(default=None)  #
    rtgMaxA: Optional[CurrentRMS] = element(default=None)  # Maximum continuous AC current capability of the DER
    rtgMaxAh: Optional[AmpereHour] = element(default=None)  # Usable energy storage capacity of the DER, in AmpHours.
    rtgMaxChargeRateVA: Optional[ApparentPower] = element(
        default=None
    )  # Maximum apparent power charge rating in Volt-Amperes. May differ from the maximum apparent power rating.
    rtgMaxChargeRateW: Optional[ActivePower] = element(
        default=None
    )  # Maximum rate of energy transfer received by the storage DER, in Watts.
    rtgMaxDischargeRateVA: Optional[ApparentPower] = element(
        default=None
    )  # Maximum apparent power discharge rating in Volt-Amperes. May differ from the maximum apparent power rating.
    rtgMaxDischargeRateW: Optional[ActivePower] = element(
        default=None
    )  # Maximum rate of energy transfer delivered by the storage DER, in Watts. Required for DERType == 83
    rtgMaxV: Optional[VoltageRMS] = element(default=None)  # AC voltage maximum rating.
    rtgMaxVA: Optional[ApparentPower] = element(default=None)  # Maximum cont' apparent power output capability, in VA.
    rtgMaxVar: Optional[ReactivePower] = element(default=None)  # Max cont' reactive power delivered by the DER (var)
    rtgMaxVarNeg: Optional[ReactivePower] = element(
        default=None
    )  # Maximum continuous reactive power received by the DER, in var. If absent, defaults to negative rtgMaxVar.
    rtgMaxW: ActivePower = (
        element()
    )  # Max cont' AP output capability of the DER, in watts. Combined gen plus storage output if DERType == 83.
    rtgMaxWh: Optional[WattHour] = element(default=None)  # Maximum energy storage capacity of the DER, in WattHours.
    rtgMinPFOverExcited: Optional[PowerFactor] = element(
        default=None
    )  # Minimum Power Factor displacement capability of the DER when injecting reactive power (over-excited)
    # SHALL be a positive value between 0.0 (typically > 0.7) and 1.0. If absent, defaults to unity.
    rtgMinPFUnderExcited: Optional[PowerFactor] = element(
        default=None
    )  # Minimum Power Factor displacement capability of the DER when absorbing reactive power (under-excited);
    # SHALL be a positive value between 0.0 (typically > 0.7) and 0.9999.  If absent, defaults to rtgMinPFOverExcited.
    rtgMinV: Optional[VoltageRMS] = element(default=None)  # AC voltage minimum rating.
    rtgNormalCategory: Optional[NormalCategoryType] = element(default=None)
    rtgOverExcitedPF: Optional[PowerFactor] = element(default=None)  # Specified over-excited power factor.
    rtgOverExcitedW: Optional[ActivePower] = element(
        default=None
    )  # AP rating in Watts at specified over-excited PF (rtgOverExcitedPF). If set rtgOverExcitedPF SHALL be present.
    rtgReactiveSusceptance: Optional[ReactiveSusceptance] = element(
        default=None
    )  # Reactive susceptance that remains connected to the Area EPS in the cease to energize and trip state.
    rtgUnderExcitedPF: Optional[PowerFactor] = element(default=None)  # Specified under-excited power factor.
    rtgUnderExcitedW: Optional[ActivePower] = element(default=None)  # Specified under-excited power factor.

    rtgVNom: Optional[VoltageRMS] = element(default=None)  # AC voltage nominal rating.
    type_: DERType = element(tag="type")  # Type of DER; see DERType object

    # CSIP Aus Extensions (encoded here as it makes decoding a whole lot simpler)
    # This is an encoded version of DOESupportedMode
    doeModesSupported: primitive_types.HexBinary8 = element(ns="csipaus", default=None)


class DERSettings(SubscribableResource):
    """Distributed energy resource settings"""

    modesEnabled: Optional[primitive_types.HexBinary32] = element(default=None)  # Hex encoded DERControlType flags
    setESDelay: Optional[int] = element(default=None)  # Enter service delay, in hundredths of a second.
    setESHighFreq: Optional[int] = element(default=None)  # Enter service frequency high. Specified in hundredths of Hz.
    setESHighVolt: Optional[int] = element(
        default=None
    )  # Enter service voltage high. Specified as an effective percent voltage in hundredths of a percent.
    setESLowFreq: Optional[int] = element(default=None)  # Enter service frequency low. Specified in hundredths of Hz.
    setESLowVolt: Optional[int] = element(
        default=None
    )  # Enter service voltage low. Specified as an effective percent voltage in hundredths of a percent.
    setESRampTms: Optional[int] = element(default=None)  # Enter service ramp time, in hundredths of a second.
    setESRandomDelay: Optional[int] = element(
        default=None
    )  # Enter service randomized delay, in hundredths of a second.
    setGradW: int = (
        element()
    )  # Set default rate of change (ramp rate) of active power output due to command or internal action,
    # defined in %setWMax / second.  Resolution is in hundredths of a percent/second.
    # A value of 0 means there is no limit. Interpreted as a percentage change in output capability limit
    # per second when used as a default ramp rate.
    setMaxA: Optional[CurrentRMS] = element(default=None)  # AC current maximum. Maximum AC current in RMS Amperes.
    setMaxAh: Optional[AmpereHour] = element(
        default=None
    )  # Max usable energy storage capacity of the DER, in AmpHours. This may be different from physical capability.
    setMaxChargeRateVA: Optional[ApparentPower] = element(
        default=None
    )  # Apparent power charge maximum. Maximum apparent power the DER can absorb from the grid in Volt-Amperes.
    # May differ from the apparent power maximum (setMaxVA).
    setMaxChargeRateW: Optional[ActivePower] = element(
        default=None
    )  # Maximum rate of energy transfer received by the storage device, in Watts. Defaults to rtgMaxChargeRateW.
    setMaxDischargeRateVA: Optional[ApparentPower] = element(
        default=None
    )  # Apparent power discharge maximum. Maximum apparent power the DER can deliver to the grid in Volt-Amperes.
    # May differ from the apparent power maximum (setMaxVA).
    setMaxDischargeRateW: Optional[ActivePower] = element(
        default=None
    )  # Maximum rate of energy transfer delivered by the storage device, in Watts. Defaults to rtgMaxDischargeRateW.
    setMaxV: Optional[VoltageRMS] = element(default=None)  # AC voltage maximum setting.
    setMaxVar: Optional[ReactivePower] = element(
        default=None
    )  # Set limit for maximum apparent power capability of the DER (in VA). Defaults to rtgMaxVA.
    setMaxVarNeg: Optional[ReactivePower] = element(
        default=None
    )  # Set limit for maximum reactive power received by the DER (in var).
    # If present, SHALL be a negative value >= rtgMaxVarNeg (default). If absent, defaults to negative setMaxVar.
    setMaxW: ActivePower = (
        element()
    )  # Set limit for maximum active power capability of the DER (in W). Defaults to rtgMaxW.
    setMaxWh: Optional[WattHour] = element(
        default=None
    )  # Maximum energy storage capacity of the DER, in WattHours. Note: this may be different from physical capability.
    setMinPFOverExcited: Optional[PowerFactor] = element(
        default=None
    )  # Set minimum Power Factor displacement limit of the DER when injecting reactive power (over-excited);
    # SHALL be a positive value between 0.0 (typically > 0.7) and 1.0.  SHALL be >= rtgMinPFOverExcited (default).
    setMinPFUnderExcited: Optional[PowerFactor] = element(
        default=None
    )  # Set minimum Power Factor displacement limit of the DER when absorbing reactive power (under-excited);
    # SHALL be a positive value between 0.0 (typically > 0.7) and 0.9999.
    # If present, SHALL be >= rtgMinPFUnderExcited (default).  If absent, defaults to setMinPFOverExcited.
    setMinV: Optional[VoltageRMS] = element(default=None)  # AC voltage min setting.
    setSoftGradW: Optional[int] = element(
        default=None
    )  # Set soft-start rate of change (soft-start ramp rate) of active power output due to command or internal action
    # defined in %setWMax / second.  Resolution is in hundredths of a percent/second.
    # 0 means there is no limit. Interpreted as a % change in output capability limit/second when used as a ramp rate.
    setVNom: Optional[VoltageRMS] = element(default=None)  # AC voltage nominal setting.
    setVRef: Optional[VoltageRMS] = element(
        default=None
    )  # The nominal AC voltage (RMS) at the utility's point of common coupling.
    setVRefOfs: Optional[VoltageRMS] = element(
        default=None
    )  # The nominal AC voltage (RMS) offset between the DER's electrical CP and the utility's point of common coupling.
    updatedTime: types.TimeType = element()  # Specifies the time at which the DER information was last updated.

    # CSIP Aus Extensions (encoded here as it makes decoding a whole lot simpler)
    # This is an encoded version of DOESupportedMode
    doeModesEnabled: Optional[primitive_types.HexBinary8] = element(ns="csipaus", default=None)


class DERListResponse(List, tag="DERList"):
    DER_: Optional[list[DER]] = element(default=None, tag="DER")

    pollRate: Optional[int] = attr(default=types.DEFAULT_POLLRATE_SECONDS)
