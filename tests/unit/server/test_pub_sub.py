import pytest

from envoy_schema.server.schema.sep2.pub_sub import (
    ConditionAttributeIdentifier,
    Notification,
    NotificationListResponse,
    NotificationStatus,
    Subscription,
    SubscriptionEncoding,
    SubscriptionListResponse,
)
from envoy_schema.server.schema.sep2.types import TOUType


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert not SubscriptionListResponse.model_validate({"all_": 0, "results": 0}).subscriptions
    assert not NotificationListResponse.model_validate({"all_": 0, "results": 0}).notifications


def test_subscription():
    """Simple validation to ensure we can read basic XML"""
    with open("tests/data/subscription.xml", "r") as fp:
        raw_xml = fp.read()

    parsed_sub: Subscription = Subscription.from_xml(raw_xml)

    assert parsed_sub.subscribedResource == "/upt/0/mr/4/r"
    assert parsed_sub.encoding == SubscriptionEncoding.XML
    assert parsed_sub.level == "+S1"
    assert parsed_sub.limit == 1
    assert parsed_sub.notificationURI == "http://example.com:8001/note"
    assert parsed_sub.condition is None


def test_subscription_no_relative_uri():
    """Checks that validation disallows relative notification uris"""

    # load as per normal but change the URI
    with open("tests/data/subscription.xml", "r") as fp:
        raw_xml = fp.read()
    raw_xml = raw_xml.replace("http://example.com:8001/note", "/invalid/relative/uri")
    with pytest.raises(ValueError):
        Subscription.from_xml(raw_xml)


def test_subscription_conditions():
    """Simple validation to ensure we can read basic XML"""
    with open("tests/data/subscription_condition.xml", "r") as fp:
        raw_xml = fp.read()

    parsed_sub: Subscription = Subscription.from_xml(raw_xml)

    assert parsed_sub.subscribedResource == "/upt/0/mr/4/r"
    assert parsed_sub.encoding == SubscriptionEncoding.XML
    assert parsed_sub.level == "+S1"
    assert parsed_sub.limit == 1
    assert parsed_sub.notificationURI == "http://example.com:8001/note"
    assert parsed_sub.condition is not None
    assert parsed_sub.condition.lowerThreshold == 100
    assert parsed_sub.condition.upperThreshold == 200
    assert parsed_sub.condition.attributeIdentifier == ConditionAttributeIdentifier.READING_VALUE


def test_notification_xml_reading():
    """Simple validation to ensure we can read basic XML"""
    with open("tests/data/notification.xml", "r") as fp:
        raw_xml = fp.read()

    parsed_notif: Notification = Notification.from_xml(raw_xml)

    assert parsed_notif.subscribedResource == "/upt/0/mr/4/r"
    assert parsed_notif.resource is not None
    assert parsed_notif.resource.all_ == 1
    assert parsed_notif.resource.results == 1
    assert len(parsed_notif.resource.Readings) == 1
    assert parsed_notif.resource.Readings[0].value == 1001
    assert parsed_notif.resource.Readings[0].timePeriod.start == 12987364
    assert parsed_notif.resource.Readings[0].timePeriod.duration == 0
    assert parsed_notif.status == NotificationStatus.DEFAULT
    assert parsed_notif.subscriptionURI == "/edev/8/sub/5"


def test_notification_xml_doe():
    """Simple validation to ensure we can read basic XML"""

    with open("tests/data/notification_doe.xml", "r") as fp:
        original_xml = fp.read()

    notif = Notification.from_xml(original_xml)
    assert notif.resource is not None
    assert notif.resource.DERControl is not None
    assert len(notif.resource.DERControl) == 1
    assert notif.resource.DERControl[0].interval.start == 456
    assert notif.resource.DERControl[0].interval.duration == 789
    assert notif.resource.DERControl[0].DERControlBase_.opModImpLimW.value == 100
    assert notif.resource.DERControl[0].DERControlBase_.opModExpLimW.value == 200
    assert notif.resource.DERControl[0].DERControlBase_.opModGenLimW.value == 300
    assert notif.resource.DERControl[0].DERControlBase_.opModLoadLimW.value == 400


def test_notification_encode_resource_DERControlListResponse():
    """tests whether the Resource element can encode various descendent Resources in a notification"""

    with open("tests/data/notification.xml", "r") as fp:
        original_xml = fp.read()

    # Replace the resource (in dict form) with a descendent type (we have to do it in dict form as updating a
    # constructed pydantic xml model directly causes headaches)
    # We will roundtrip that via XML to ensure all of our values are preserved
    notif_dict = Notification.from_xml(original_xml).model_dump()
    notif_dict["resource"] = {
        "all_": 1,
        "results": 1,
        "type": "DERControlList",
        "href": "/my/list",
        "DERControl": [
            {
                "mRID": "abc",
                "creationTime": 123,
                "interval": {
                    "start": 456,
                    "duration": 789,
                },
                "EventStatus_": {
                    "currentStatus": 1,
                    "dateTime": 2,
                    "potentiallySuperseded": False,
                },
                "DERControlBase_": {
                    "opModImpLimW": {"value": 100, "multiplier": 1},
                    "opModExpLimW": {"value": 200, "multiplier": 1},
                    "opModGenLimW": {"value": 300, "multiplier": 1},
                    "opModLoadLimW": {"value": 400, "multiplier": 1},
                },
            }
        ],
    }

    # Quick sanity check on the raw XML
    updated_xml = (
        Notification.model_validate(notif_dict).to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    )
    assert 'xsi:type="DERControlList"' in updated_xml
    assert 'href="/my/list"' in updated_xml
    assert "<value>100</value>" in updated_xml

    # Now return to the original type and see if everything is there
    notif: Notification = Notification.from_xml(updated_xml)
    assert notif.resource is not None
    assert notif.resource.DERControl is not None
    assert len(notif.resource.DERControl) == 1
    assert notif.resource.DERControl[0].DERControlBase_.opModImpLimW.value == 100
    assert notif.resource.DERControl[0].DERControlBase_.opModExpLimW.value == 200
    assert notif.resource.DERControl[0].DERControlBase_.opModGenLimW.value == 300
    assert notif.resource.DERControl[0].DERControlBase_.opModLoadLimW.value == 400


def test_notification_encode_resource_DERStatus():
    """tests whether the Resource element can encode various descendent Resources in a notification"""

    with open("tests/data/notification.xml", "r") as fp:
        original_xml = fp.read()

    # Replace the resource (in dict form) with a descendent type (we have to do it in dict form as updating a
    # constructed pydantic xml model directly causes headaches)
    # We will roundtrip that via XML to ensure all of our values are preserved
    notif_dict = Notification.from_xml(original_xml).model_dump()
    notif_dict["resource"] = {
        "type": "DERStatus",
        "href": "/my/der/status",
        "alarmStatus": "deadbeef",
        "genConnectStatus": {"dateTime": 1700001, "value": "1"},
        "inverterStatus": {"dateTime": 1700002, "value": "2"},
        "localControlModeStatus": {"dateTime": 1700003, "value": "1"},
        "manufacturerStatus": {"dateTime": 1700004, "value": "4"},
        "operationalModeStatus": {"dateTime": 1700005, "value": "1"},
        "readingTime": 1700006,
        "stateOfChargeStatus": {"dateTime": 1700007, "value": "7"},
        "storageModeStatus": {"dateTime": 1700008, "value": "2"},
        "storConnectStatus": {"dateTime": 1700009, "value": "9"},
    }

    # Quick sanity check on the raw XML
    updated_xml = (
        Notification.model_validate(notif_dict).to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    )
    assert 'xsi:type="DERStatus"' in updated_xml
    assert 'href="/my/der/status"' in updated_xml
    assert "<dateTime>1700009</dateTime>" in updated_xml

    # Now return to the original type and see if everything is there
    notif: Notification = Notification.from_xml(updated_xml)
    assert notif.resource.alarmStatus == "deadbeef"
    assert notif.resource.genConnectStatus.value == "1"
    assert notif.resource.inverterStatus.value == 2
    assert notif.resource.localControlModeStatus.dateTime == 1700003
    assert notif.resource.storConnectStatus.value == "9"


def test_notification_encode_resource_DERAvailability():
    """tests whether the Resource element can encode various descendent Resources in a notification"""

    with open("tests/data/notification.xml", "r") as fp:
        original_xml = fp.read()

    # Replace the resource (in dict form) with a descendent type (we have to do it in dict form as updating a
    # constructed pydantic xml model directly causes headaches)
    # We will roundtrip that via XML to ensure all of our values are preserved
    notif_dict = Notification.from_xml(original_xml).model_dump()
    notif_dict["resource"] = {
        "type": "DERAvailability",
        "href": "/my/der/avail",
        "availabilityDuration": 123,
        "maxChargeDuration": 456,
        "readingTime": 1700002,
        "reserveChargePercent": 789,
        "reservePercent": 1011,
        "statVarAvail": {"multiplier": 2, "value": 7},
        "statWAvail": {"multiplier": 3, "value": 8},
    }

    # Quick sanity check on the raw XML
    updated_xml = (
        Notification.model_validate(notif_dict).to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    )
    assert 'xsi:type="DERAvailability"' in updated_xml
    assert 'href="/my/der/avail"' in updated_xml
    assert "<readingTime>1700002</readingTime>" in updated_xml

    # Now return to the original type and see if everything is there
    notif: Notification = Notification.from_xml(updated_xml)
    assert notif.resource.availabilityDuration == 123
    assert notif.resource.maxChargeDuration == 456
    assert notif.resource.readingTime == 1700002
    assert notif.resource.statVarAvail.value == 7


def test_notification_encode_resource_DERSettings():
    """tests whether the Resource element can encode various descendent Resources in a notification"""

    with open("tests/data/notification.xml", "r") as fp:
        original_xml = fp.read()

    # Replace the resource (in dict form) with a descendent type (we have to do it in dict form as updating a
    # constructed pydantic xml model directly causes headaches)
    # We will roundtrip that via XML to ensure all of our values are preserved
    notif_dict = Notification.from_xml(original_xml).model_dump()
    notif_dict["resource"] = {
        "type": "DERSettings",
        "href": "/my/der/settings",
        # Non exhaustive subset
        "modesEnabled": "feed",
        "setESDelay": 11,
        "setESHighFreq": 22,
        "setESHighVolt": 33,
        "setMaxW": {"multiplier": 1, "value": 44},
        "statVarAvail": {"multiplier": 2, "value": 7},
        "statWAvail": {"multiplier": 3, "value": 8},
        "updatedTime": 17000001,
        "doeModesEnabled": "be",
    }

    # Quick sanity check on the raw XML
    updated_xml = (
        Notification.model_validate(notif_dict).to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    )
    assert 'xsi:type="DERSettings"' in updated_xml
    assert 'href="/my/der/settings"' in updated_xml
    assert "<updatedTime>17000001</updatedTime>" in updated_xml

    # Now return to the original type and see if everything is there
    notif: Notification = Notification.from_xml(updated_xml)
    assert notif.resource.modesEnabled == "feed"
    assert notif.resource.setMaxW.value == 44
    assert notif.resource.updatedTime == 17000001
    assert notif.resource.doeModesEnabled == "be"


def test_notification_encode_resource_DERCapability():
    """tests whether the Resource element can encode various descendent Resources in a notification"""

    with open("tests/data/notification.xml", "r") as fp:
        original_xml = fp.read()

    # Replace the resource (in dict form) with a descendent type (we have to do it in dict form as updating a
    # constructed pydantic xml model directly causes headaches)
    # We will roundtrip that via XML to ensure all of our values are preserved
    notif_dict = Notification.from_xml(original_xml).model_dump()
    notif_dict["resource"] = {
        "type": "DERCapability",
        "href": "/my/der/cap",
        # Non exhaustive subset
        "modesSupported": "dead",
        "rtgMaxV": {"multiplier": 1, "value": 11},
        "rtgMaxW": {"multiplier": 2, "value": 22},
        "doeModesSupported": "1",
    }

    # Quick sanity check on the raw XML
    updated_xml = (
        Notification.model_validate(notif_dict).to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    )
    assert 'xsi:type="DERCapability"' in updated_xml
    assert 'href="/my/der/cap"' in updated_xml
    assert "<multiplier>2</multiplier>" in updated_xml

    # Now return to the original type and see if everything is there
    notif: Notification = Notification.from_xml(updated_xml)
    assert notif.resource.modesSupported == "dead"
    assert notif.resource.rtgMaxV.value == 11
    assert notif.resource.rtgMaxW.value == 22
    assert notif.resource.doeModesSupported == "1"


def test_notification_encode_resource_DefaultDERControl():
    """tests whether the Resource element can encode various descendent Resources in a notification"""

    with open("tests/data/notification.xml", "r") as fp:
        original_xml = fp.read()

    # Replace the resource (in dict form) with a descendent type (we have to do it in dict form as updating a
    # constructed pydantic xml model directly causes headaches)
    # We will roundtrip that via XML to ensure all of our values are preserved
    notif_dict = Notification.from_xml(original_xml).model_dump()
    notif_dict["resource"] = {
        "type": "DefaultDERControl",
        "creationTime": 123,
        "mRID": "abc",
        "interval": {
            "start": 456,
            "duration": 789,
        },
        "DERControlBase_": {
            "opModImpLimW": {"value": 100, "multiplier": 1},
            "opModExpLimW": {"value": 200, "multiplier": 1},
            "opModGenLimW": {"value": 300, "multiplier": 1},
            "opModLoadLimW": {"value": 400, "multiplier": 1},
        },
    }

    # Quick sanity check on the raw XML
    updated_xml = (
        Notification.model_validate(notif_dict).to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    )
    assert 'xsi:type="DefaultDERControl"' in updated_xml
    assert "<value>100</value>" in updated_xml

    # Now return to the original type and see if everything is there
    notif: Notification = Notification.from_xml(updated_xml)
    assert notif.resource is not None
    assert notif.resource.DERControlBase_ is not None
    assert notif.resource.DERControlBase_.opModImpLimW.value == 100
    assert notif.resource.DERControlBase_.opModExpLimW.value == 200
    assert notif.resource.DERControlBase_.opModGenLimW.value == 300
    assert notif.resource.DERControlBase_.opModLoadLimW.value == 400


def test_notification_encode_resource_TimeTariffIntervalListResponse():
    """tests whether the Resource element can encode various descendent Resources in a notification"""

    with open("tests/data/notification.xml", "r") as fp:
        original_xml = fp.read()

    # Replace the resource (in dict form) with a descendent type (we have to do it in dict form as updating a
    # constructed pydantic xml model directly causes headaches)
    # We will roundtrip that via XML to ensure all of our values are preserved
    notif_dict = Notification.from_xml(original_xml).model_dump()
    notif_dict["resource"] = {
        "all_": 1,
        "results": 1,
        "type": "TimeTariffIntervalList",
        "href": "/my/list",
        "TimeTariffInterval": [
            {
                "EventStatus_": {
                    "currentStatus": 1,
                    "dateTime": 2,
                    "potentiallySuperseded": False,
                },
                "creationTime": 123,
                "mRID": "AABB",
                "interval": {
                    "duration": 789,
                    "start": 456,
                },
                "touTier": TOUType.NOT_APPLICABLE,
                "ConsumptionTariffIntervalListLink": {"all_": 1, "href": "/my/price/at/time/554433"},
            }
        ],
    }

    # Quick sanity check on the raw XML
    updated_xml = (
        Notification.model_validate(notif_dict).to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    )
    assert 'xsi:type="TimeTariffIntervalList"' in updated_xml
    assert 'href="/my/list"' in updated_xml
    assert 'href="/my/price/at/time/554433"' in updated_xml

    # Now return to the original type and see if everything is there
    notif: Notification = Notification.from_xml(updated_xml)
    assert notif.resource is not None
    assert notif.resource.TimeTariffInterval is not None
    assert len(notif.resource.TimeTariffInterval) == 1
    assert notif.resource.TimeTariffInterval[0].ConsumptionTariffIntervalListLink.href == "/my/price/at/time/554433"


def test_notification_encode_resource_EndDeviceListResponse():
    """tests whether the Resource element can encode various descendent Resources in a notification"""

    with open("tests/data/notification.xml", "r") as fp:
        original_xml = fp.read()

    # Replace the resource (in dict form) with a descendent type (we have to do it in dict form as updating a
    # constructed pydantic xml model directly causes headaches)
    # We will roundtrip that via XML to ensure all of our values are preserved
    notif_dict = Notification.from_xml(original_xml).model_dump()
    notif_dict["resource"] = {
        "all_": 1,
        "results": 1,
        "type": "EndDeviceListResponse",
        "href": "/my/list",
        "EndDevice": [
            {
                "lFDI": "lfdi-111",
                "sFDI": 111,
                "changedTime": 123,
                "ConnectionPointLink": {"href": "/href/cp"},
                "DERListLink": {"href": "/href/der"},
            }
        ],
    }

    # Quick sanity check on the raw XML
    updated_xml = (
        Notification.model_validate(notif_dict).to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    )
    assert 'xsi:type="EndDeviceListResponse"' in updated_xml
    assert 'href="/href/cp"' in updated_xml

    # Now return to the original type and see if everything is there
    notif: Notification = Notification.from_xml(updated_xml)
    assert notif.resource is not None
    assert notif.resource.EndDevice is not None
    assert len(notif.resource.EndDevice) == 1
    assert notif.resource.EndDevice[0].lFDI == "lfdi-111"
    assert notif.resource.EndDevice[0].sFDI == 111
    assert notif.resource.EndDevice[0].ConnectionPointLink.href == "/href/cp"
    assert notif.resource.EndDevice[0].DERListLink.href == "/href/der"
