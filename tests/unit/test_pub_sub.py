from typing import Optional

import pytest
from pydantic import AnyUrl
from pydantic_xml import element

from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.identification import Resource
from envoy_schema.server.schema.sep2.primitive_types import HttpUri, LocalAbsoluteUri
from envoy_schema.server.schema.sep2.pub_sub import (
    ConditionAttributeIdentifier,
    Notification,
    NotificationStatus,
    Subscription,
    SubscriptionEncoding,
)
from envoy_schema.server.schema.sep2.types import TOUType


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


def test_notification():
    """Simple validation to ensure we can read basic XML"""
    with open("tests/data/notification.xml", "r") as fp:
        raw_xml = fp.read()

    parsed_notif: Notification = Notification.from_xml(raw_xml)

    assert parsed_notif.subscribedResource == "/upt/0/mr/4/r"
    assert parsed_notif.resource is not None
    assert type(parsed_notif.resource) == Resource
    assert parsed_notif.status == NotificationStatus.DEFAULT
    assert parsed_notif.subscriptionURI == "/edev/8/sub/5"


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
        ],
    }

    # Quick sanity check on the raw XML
    updated_xml = Notification.model_validate(notif_dict).to_xml(skip_empty=True).decode()
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
    updated_xml = Notification.model_validate(notif_dict).to_xml(skip_empty=True).decode()
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
                "creationTime": 123,
                "mRID": "abc",
                "interval": {
                    "start": 456,
                    "duration": 789,
                },
                "touTier": TOUType.NOT_APPLICABLE,
                "ConsumptionTariffIntervalListLink": {"all_": 1, "href": "/my/price/at/time/554433"},
            }
        ],
    }

    # Quick sanity check on the raw XML
    updated_xml = Notification.model_validate(notif_dict).to_xml(skip_empty=True).decode()
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
    updated_xml = Notification.model_validate(notif_dict).to_xml(skip_empty=True).decode()
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
