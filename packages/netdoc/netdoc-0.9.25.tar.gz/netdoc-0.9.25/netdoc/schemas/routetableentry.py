"""Schema validation for RouteTableEntry."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__date__ = "2022-09-19"
__version__ = "0.9.25"

from jsonschema import validate, FormatChecker

from dcim.models import Interface, Device
from ipam.models import VRF

from netdoc.models import RouteTableEntry, RouteTypeChoices
from netdoc import utils


def get_schema():
    """Return the JSON schema to validate RouteTableEntry data."""
    return {
        "type": "object",
        "properties": {
            "device_id": {
                "type": "integer",
                "enum": list(Device.objects.all().values_list("id", flat=True)),
            },
            "destination": {
                "type": "string",  # IP Network
            },
            "nexthop_ip": {
                "type": "string",  # IP Address
            },
            "nexthop_if_id": {
                "type": "integer",
                "enum": list(Interface.objects.all().values_list("id", flat=True)),
            },
            "vrf_id": {
                "type": "integer",
                "enum": list(VRF.objects.all().values_list("id", flat=True)),
            },
            "distance": {
                "type": "integer",
            },
            "metric": {
                "type": "integer",
            },
            "protocol": {
                "type": "string",
                "enum": [key for key, value in RouteTypeChoices()],
            },
        },
    }


def get_schema_create():
    """Return the JSON schema to validate new RouteTableEntry objects."""
    schema = get_schema()
    schema["required"] = [
        "device_id",
        "destination",
        "protocol",
    ]
    return schema


def create(**kwargs):
    """Create an RouteTableEntry."""
    kwargs = utils.delete_empty_keys(kwargs)
    validate(kwargs, get_schema_create(), format_checker=FormatChecker())
    # At least one of nexthop_ip or nexthop_if should be set
    if not kwargs.get("nexthop_ip") and not kwargs.get("nexthop_if_id"):
        raise ValueError("Even one of nexthop_ip or nexthop_if_id should have a value.")

    obj = utils.object_create(RouteTableEntry, **kwargs)
    return obj


def get(
    device_id=None,
    destination=None,
    distance=None,
    metric=None,
    protocol=None,
    discovered=True,
):
    """Return an RouteTableEntry."""
    obj = utils.object_get_or_none(
        RouteTableEntry,
        device_id=device_id,
        destination=destination,
        distance=distance,
        metric=metric,
        protocol=protocol,
    )
    if obj and discovered:
        # Update updated_at
        obj.save()
    return obj


def get_list(**kwargs):
    """Get a list of RouteTableEntry objects."""
    validate(kwargs, get_schema(), format_checker=FormatChecker())
    result = utils.object_list(RouteTableEntry, **kwargs)
    return result
