from enum import IntEnum, IntFlag, auto

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
from envoy_schema.server.schema.sep2.identification import (
    IdentifiedObject,
    Link,
    List,
    ListLink,
    Resource,
    SubscribableIdentifiedObject,
    SubscribableList,
    SubscribableResource,
)
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.types import PrimacyType


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

    # Additional DRED Values
    DRED_DRM_0 = 100
    DRED_DRM_1 = 101
    DRED_DRM_2 = 102
    DRED_DRM_3 = 103
    DRED_DRM_4 = 104
    DRED_DRM_5 = 105
    DRED_DRM_6 = 106
    DRED_DRM_7 = 107
    DRED_DRM_8 = 108


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


class VPPControlType(IntFlag):
    """Bitmap indicating the VPP controls supported by and enabled on the device. Bit positions SHALL be defined as
    follows:
    0 - opModStorageTargetW (Storage Target Active Power)

    All other values reserved."""

    OP_MOD_STORAGE_TARGET_W = auto()


class FreqDroopType(BaseXmlModelWithNS):
    """Type for Frequency-Droop (Frequency-Watt) operation."""

    dBOF: int = element()  # Frequency droop dead band for over-frequency conditions.
    dBUF: int = element()  # Frequency droop dead band for under-frequency conditions.
    kOF: int = element()  # droop per-unit frequency change OF conditions corresponding to 1 power output change.
    kUF: int = element()  # # droop per-unit frequency change UF conditions corresponding to 1 power output change.
    openLoopTms: int = element()  # Open loop response time


class DERControlBase(BaseXmlModelWithNS):
    """Distributed Energy Resource (DER) control values."""

    opModConnect: bool | None = element(default=None)  # Set DER as connected (true) or disconnected (false).
    opModEnergize: bool | None = element(default=None)  # Set DER as energized (true) or de-energized (false).
    opModFixedPFAbsorbW: PowerFactorWithExcitation | None = element(
        default=None
    )  # requested PF when AP is being absorbed
    opModFixedPFInjectW: PowerFactorWithExcitation | None = element(
        default=None
    )  # requested PF when AP is being injected
    opModFixedVar: FixedVar | None = element(default=None)  # specifies the delivered or received RP setpoint.
    opModFixedW: types.SignedPerCent | None = element(
        default=None
    )  # specifies a requested charge/discharge mode setpoint
    opModFreqDroop: FreqDroopType | None = element(default=None)  # Specifies a frequency-watt operation
    opModFreqWatt: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 0
    opModHFRTMayTrip: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 1
    opModHFRTMustTrip: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 2
    opModHVRTMayTrip: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 3
    opModHVRTMomentaryCessation: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 4
    opModHVRTMustTrip: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 5
    opModLFRTMayTrip: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 6
    opModLFRTMustTrip: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 7
    opModLVRTMayTrip: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 8
    opModLVRTMomentaryCessation: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 9
    opModLVRTMustTrip: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 10
    opModMaxLimW: types.PerCent | None = element(
        default=None
    )  # max active power generation level at electrical coupling point
    opModTargetVar: ReactivePower | None = element(default=None)  # Target reactive power, in var
    opModTargetW: ActivePower | None = element(default=None)  # Target active power, in Watts
    opModVoltVar: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 11
    opModVoltWatt: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 12
    opModWattPF: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 13
    opModWattVar: Link | None = element(default=None)  # Specify DERCurveLink for curveType == 14
    rampTms: int | None = element(default=None)  # Requested ramp time, in hundredths of a second

    # CSIP Aus Extensions (encoded here as it makes decoding a whole lot simpler)
    opModImpLimW: ActivePower | None = element(
        ns="csipaus", default=None
    )  # constraint on the imported AP at the connection point
    opModExpLimW: ActivePower | None = element(
        ns="csipaus", default=None
    )  # constraint on the exported AP at the connection point
    opModGenLimW: ActivePower | None = element(
        ns="csipaus", default=None
    )  # max limit on discharge watts for a single DER
    opModLoadLimW: ActivePower | None = element(
        ns="csipaus", default=None
    )  # max limit on charge watts for a single DER
    opModStorageTargetW: ActivePower | None = element(
        ns="csipaus", default=None
    )  # This is a target aggregate output, in Watts, for one or more storage components within an EndDevice


class DefaultDERControl(SubscribableIdentifiedObject):
    """Contains control mode information to be used if no active DERControl is found."""

    DERControlBase_: DERControlBase = element(tag="DERControlBase")
    setESDelay: int | None = element(default=None)  # Enter service delay, in hundredths of a second.
    setESHighFreq: int | None = element(default=None)  # Enter service frequency high. Specified in hundredths of Hz
    setESHighVolt: int | None = element(
        default=None
    )  # Enter service voltage high. Specified as an effective percent voltage,
    setESLowFreq: int | None = element(default=None)  # Enter service frequency low. Specified in hundredths of Hz
    setESLowVolt: int | None = element(
        default=None
    )  # Enter service voltage low. Specified as an effective percent voltage,
    setESRampTms: int | None = element(default=None)  # Enter service ramp time, in hundredths of a second
    setESRandomDelay: int | None = element(default=None)  # Enter service randomized delay, in hundredths of a second.
    setGradW: int | None = element(default=None)  # Set default rate of change (ramp rate) of active power output
    setSoftGradW: int | None = element(
        default=None
    )  # Set soft-start rate of change (soft-start ramp rate) of AP output


class DERControlResponse(RandomizableEvent, tag="DERControl"):
    """Distributed Energy Resource (DER) time/event-based control."""

    DERControlBase_: DERControlBase = element(tag="DERControlBase")
    deviceCategory: primitive_types.HexBinary32 | None = element(
        default=None,
    )  # the bitmap indicating device categories that SHOULD respond.


class DERControlListResponse(SubscribableList, tag="DERControlList"):
    DERControl: list[DERControlResponse] | None = element(default=None)


class DERProgramResponse(SubscribableIdentifiedObject, tag="DERProgram"):
    """sep2 DERProgram"""

    ActiveDERControlListLink: ListLink | None = element(default=None)
    DefaultDERControlLink: Link | None = element(default=None)
    DERControlListLink: ListLink | None = element(default=None)
    DERCurveListLink: ListLink | None = element(default=None)
    primacy: int = element()  # Encodes a value from PrimacyType


class DERProgramListResponse(SubscribableList, tag="DERProgramList"):
    DERProgram: list[DERProgramResponse] | None = element(default=None)
    pollRate: int | None = attr(
        default=None
    )  # The default polling rate for this resource and all resources below in seconds


class DemandResponseProgramResponse(IdentifiedObject, tag="DemandResponseProgram"):
    """sep2 Demand response program"""

    ActiveEndDeviceControlListLink: ListLink | None = element(default=None)
    availabilityUpdatePercentChangeThreshold: types.PerCent | None = element(default=None)
    availabilityUpdatePowerChangeThreshold: ActivePower | None = element(default=None)
    EndDeviceControlListLink: ListLink | None = element(default=None)
    primacy: PrimacyType = element()


class DemandResponseProgramListResponse(Sep2List, tag="DemandResponseProgramList"):
    DemandResponseProgram: list[DemandResponseProgramResponse] | None = element(default=None)


class EndDeviceControlResponse(RandomizableEvent, tag="EndDeviceControl"):
    """Instructs an EndDevice to perform a specified action."""

    deviceCategory: primitive_types.HexBinary32 = element()  # HexBinary Encoded types.DeviceCategory enum
    drProgramMandatory: bool = element()
    loadShiftForward: bool = element()
    overrideDuration: int | None = element(default=None)


class DER(SubscribableResource):
    """sep2 DER: Contains links to DER resources."""

    AssociatedDERProgramListLink: ListLink | None = element(
        default=None
    )  # Link to List of DERPrograms having the DERControls for this DER
    AssociatedUsagePointLink: Link | None = element(
        default=None
    )  # If present, this is the submeter that monitors the DER output.

    CurrentDERProgramLink: Link | None = element(
        default=None
    )  # If set, this is the DERProgram containing the currently active DERControl

    DERAvailabilityLink: Link | None = element(default=None)  # SHALL contain a Link to an instance of DERAvailability.
    DERCapabilityLink: Link | None = element(default=None)  # SHALL contain a Link to an instance of DERCapability.
    DERSettingsLink: Link | None = element(default=None)  # SHALL contain a Link to an instance of DERSettings.

    DERStatusLink: Link | None = element(default=None)  # SHALL contain a Link to an instance of DERStatus.


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

    alarmStatus: primitive_types.HexBinary32 | None = element(default=None)  # AlarmStatusType encoded HexBinary str
    genConnectStatus: ConnectStatusTypeValue | None = element(
        default=None, tag="genConnectStatus"
    )  # Connection status for generator
    inverterStatus: InverterStatusTypeValue | None = element(default=None, tag="inverterStatus")
    localControlModeStatus: LocalControlModeStatusTypeValue | None = element(default=None, tag="localControlModeStatus")
    manufacturerStatus: ManufacturerStatusValue | None = element(default=None, tag="manufacturerStatus")
    operationalModeStatus: OperationalModeStatusTypeValue | None = element(default=None, tag="operationalModeStatus")
    readingTime: types.TimeType = element()
    stateOfChargeStatus: StateOfChargeStatusValue | None = element(default=None, tag="stateOfChargeStatus")
    storageModeStatus: StorageModeStatusTypeValue | None = element(default=None, tag="storageModeStatus")
    storConnectStatus: ConnectStatusTypeValue | None = element(
        default=None, tag="storConnectStatus"
    )  # Connection status for storage


class DERAvailability(SubscribableResource):
    """Indicates current reserve generation status"""

    availabilityDuration: int | None = element(
        default=None
    )  # Indicates number of seconds the DER will be able to deliver active power at the reservePercent level.
    maxChargeDuration: int | None = element(
        default=None
    )  # Indicates number of seconds the DER will be able to receive active power at the reserveChargePercent level.
    readingTime: types.TimeType = element()  # The timestamp when the DER availability was last updated.
    reserveChargePercent: types.PerCent | None = element(
        default=None
    )  # Percent of continuous received active power (%setMaxChargeRateW) that is estimated to be available in reserve.
    reservePercent: types.PerCent | None = element(
        default=None
    )  # Percent of continuous delivered active power (%setMaxW) that is estimated to be available in reserve.
    statVarAvail: ReactivePower | None = element(
        default=None
    )  # Estimated reserve reactive power, in var.  Represents the lesser of received or delivered reactive power.
    statWAvail: ActivePower | None = element(default=None)  # Estimated reserve active power, in watts.


class DERCapability(Resource):
    """Distributed energy resource type and nameplate ratings."""

    modesSupported: primitive_types.HexBinary32 = element()  # HexBinary encoded DERControlType flags
    rtgAbnormalCategory: AbnormalCategoryType | None = element(default=None)  #
    rtgMaxA: CurrentRMS | None = element(default=None)  # Maximum continuous AC current capability of the DER
    rtgMaxAh: AmpereHour | None = element(default=None)  # Usable energy storage capacity of the DER, in AmpHours.
    rtgMaxChargeRateVA: ApparentPower | None = element(
        default=None
    )  # Maximum apparent power charge rating in Volt-Amperes. May differ from the maximum apparent power rating.
    rtgMaxChargeRateW: ActivePower | None = element(
        default=None
    )  # Maximum rate of energy transfer received by the storage DER, in Watts.
    rtgMaxDischargeRateVA: ApparentPower | None = element(
        default=None
    )  # Maximum apparent power discharge rating in Volt-Amperes. May differ from the maximum apparent power rating.
    rtgMaxDischargeRateW: ActivePower | None = element(
        default=None
    )  # Maximum rate of energy transfer delivered by the storage DER, in Watts. Required for DERType == 83
    rtgMaxV: VoltageRMS | None = element(default=None)  # AC voltage maximum rating.
    rtgMaxVA: ApparentPower | None = element(default=None)  # Maximum cont' apparent power output capability, in VA.
    rtgMaxVar: ReactivePower | None = element(default=None)  # Max cont' reactive power delivered by the DER (var)
    rtgMaxVarNeg: ReactivePower | None = element(
        default=None
    )  # Maximum continuous reactive power received by the DER, in var. If absent, defaults to negative rtgMaxVar.
    rtgMaxW: ActivePower = (
        element()
    )  # Max cont' AP output capability of the DER, in watts. Combined gen plus storage output if DERType == 83.
    rtgMaxWh: WattHour | None = element(default=None)  # Maximum energy storage capacity of the DER, in WattHours.
    rtgMinPFOverExcited: PowerFactor | None = element(
        default=None
    )  # Minimum Power Factor displacement capability of the DER when injecting reactive power (over-excited)
    # SHALL be a positive value between 0.0 (typically > 0.7) and 1.0. If absent, defaults to unity.
    rtgMinPFUnderExcited: PowerFactor | None = element(
        default=None
    )  # Minimum Power Factor displacement capability of the DER when absorbing reactive power (under-excited);
    # SHALL be a positive value between 0.0 (typically > 0.7) and 0.9999.  If absent, defaults to rtgMinPFOverExcited.
    rtgMinV: VoltageRMS | None = element(default=None)  # AC voltage minimum rating.
    rtgNormalCategory: NormalCategoryType | None = element(default=None)
    rtgOverExcitedPF: PowerFactor | None = element(default=None)  # Specified over-excited power factor.
    rtgOverExcitedW: ActivePower | None = element(
        default=None
    )  # AP rating in Watts at specified over-excited PF (rtgOverExcitedPF). If set rtgOverExcitedPF SHALL be present.
    rtgReactiveSusceptance: ReactiveSusceptance | None = element(
        default=None
    )  # Reactive susceptance that remains connected to the Area EPS in the cease to energize and trip state.
    rtgUnderExcitedPF: PowerFactor | None = element(default=None)  # Specified under-excited power factor.
    rtgUnderExcitedW: ActivePower | None = element(default=None)  # Specified under-excited power factor.

    rtgVNom: VoltageRMS | None = element(default=None)  # AC voltage nominal rating.
    type_: DERType = element(tag="type")  # Type of DER; see DERType object

    # CSIP Aus Extensions (encoded here as it makes decoding a whole lot simpler)
    # This is an encoded version of DOESupportedMode
    doeModesSupported: primitive_types.HexBinary8 = element(ns="csipaus")

    # CSIP Aus Extensions (encoded here as it makes decoding a whole lot simpler)
    # This is an encoded version of VPPControlType
    vppModesSupported: primitive_types.HexBinary8 | None = element(ns="csipaus", default=None)


class DERSettings(SubscribableResource):
    """Distributed energy resource settings"""

    modesEnabled: primitive_types.HexBinary32 | None = element(default=None)  # Hex encoded DERControlType flags
    setESDelay: int | None = element(default=None)  # Enter service delay, in hundredths of a second.
    setESHighFreq: int | None = element(default=None)  # Enter service frequency high. Specified in hundredths of Hz.
    setESHighVolt: int | None = element(
        default=None
    )  # Enter service voltage high. Specified as an effective percent voltage in hundredths of a percent.
    setESLowFreq: int | None = element(default=None)  # Enter service frequency low. Specified in hundredths of Hz.
    setESLowVolt: int | None = element(
        default=None
    )  # Enter service voltage low. Specified as an effective percent voltage in hundredths of a percent.
    setESRampTms: int | None = element(default=None)  # Enter service ramp time, in hundredths of a second.
    setESRandomDelay: int | None = element(default=None)  # Enter service randomized delay, in hundredths of a second.
    setGradW: int = (
        element()
    )  # Set default rate of change (ramp rate) of active power output due to command or internal action,
    # defined in %setWMax / second.  Resolution is in hundredths of a percent/second.
    # A value of 0 means there is no limit. Interpreted as a percentage change in output capability limit
    # per second when used as a default ramp rate.
    setMaxA: CurrentRMS | None = element(default=None)  # AC current maximum. Maximum AC current in RMS Amperes.
    setMaxAh: AmpereHour | None = element(
        default=None
    )  # Max usable energy storage capacity of the DER, in AmpHours. This may be different from physical capability.
    setMaxChargeRateVA: ApparentPower | None = element(
        default=None
    )  # Apparent power charge maximum. Maximum apparent power the DER can absorb from the grid in Volt-Amperes.
    # May differ from the apparent power maximum (setMaxVA).
    setMaxChargeRateW: ActivePower | None = element(
        default=None
    )  # Maximum rate of energy transfer received by the storage device, in Watts. Defaults to rtgMaxChargeRateW.
    setMaxDischargeRateVA: ApparentPower | None = element(
        default=None
    )  # Apparent power discharge maximum. Maximum apparent power the DER can deliver to the grid in Volt-Amperes.
    # May differ from the apparent power maximum (setMaxVA).
    setMaxDischargeRateW: ActivePower | None = element(
        default=None
    )  # Maximum rate of energy transfer delivered by the storage device, in Watts. Defaults to rtgMaxDischargeRateW.
    setMaxV: VoltageRMS | None = element(default=None)  # AC voltage maximum setting.
    setMaxVA: ApparentPower | None = element(
        default=None
    )  # Set limit for maximum apparent power capability of the DER (in VA).
    setMaxVar: ReactivePower | None = element(
        default=None
    )  # Set limit for maximum apparent power capability of the DER (in VA). Defaults to rtgMaxVA.
    setMaxVarNeg: ReactivePower | None = element(
        default=None
    )  # Set limit for maximum reactive power received by the DER (in var).
    # If present, SHALL be a negative value >= rtgMaxVarNeg (default). If absent, defaults to negative setMaxVar.
    setMaxW: ActivePower = (
        element()
    )  # Set limit for maximum active power capability of the DER (in W). Defaults to rtgMaxW.
    setMaxWh: WattHour | None = element(
        default=None
    )  # Maximum energy storage capacity of the DER, in WattHours. Note: this may be different from physical capability.
    setMinPFOverExcited: PowerFactor | None = element(
        default=None
    )  # Set minimum Power Factor displacement limit of the DER when injecting reactive power (over-excited);
    # SHALL be a positive value between 0.0 (typically > 0.7) and 1.0.  SHALL be >= rtgMinPFOverExcited (default).
    setMinPFUnderExcited: PowerFactor | None = element(
        default=None
    )  # Set minimum Power Factor displacement limit of the DER when absorbing reactive power (under-excited);
    # SHALL be a positive value between 0.0 (typically > 0.7) and 0.9999.
    # If present, SHALL be >= rtgMinPFUnderExcited (default).  If absent, defaults to setMinPFOverExcited.
    setMinV: VoltageRMS | None = element(default=None)  # AC voltage min setting.
    setSoftGradW: int | None = element(
        default=None
    )  # Set soft-start rate of change (soft-start ramp rate) of active power output due to command or internal action
    # defined in %setWMax / second.  Resolution is in hundredths of a percent/second.
    # 0 means there is no limit. Interpreted as a % change in output capability limit/second when used as a ramp rate.
    setVNom: VoltageRMS | None = element(default=None)  # AC voltage nominal setting.
    setVRef: VoltageRMS | None = element(
        default=None
    )  # The nominal AC voltage (RMS) at the utility's point of common coupling.
    setVRefOfs: VoltageRMS | None = element(
        default=None
    )  # The nominal AC voltage (RMS) offset between the DER's electrical CP and the utility's point of common coupling.
    updatedTime: types.TimeType = element()  # Specifies the time at which the DER information was last updated.

    # CSIP Aus Extensions (encoded here as it makes decoding a whole lot simpler)
    # This is an encoded version of DOESupportedMode
    doeModesEnabled: primitive_types.HexBinary8 | None = element(ns="csipaus", default=None)

    # CSIP Aus Extensions (encoded here as it makes decoding a whole lot simpler)
    # This is an encoded version of VPPControlType
    vppModesEnabled: primitive_types.HexBinary8 | None = element(ns="csipaus", default=None)

    setMinWh: WattHour | None = element(ns="csipaus", default=None)


class DERListResponse(List, tag="DERList"):
    DER_: list[DER] | None = element(default=None, tag="DER")

    pollRate: int | None = attr(default=types.DEFAULT_POLLRATE_SECONDS)
