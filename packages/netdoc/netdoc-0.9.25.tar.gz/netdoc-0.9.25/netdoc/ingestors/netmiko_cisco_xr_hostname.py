"""Ingestor for netmiko_cisco_xr_hostname."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__date__ = "2022-09-07"
__version__ = "0.9.25"

import re

from netdoc.schemas import device, discoverable
from netdoc import utils


def ingest(log):
    """Processing parsed output."""
    # See https://github.com/netbox-community/devicetype-library/tree/master/device-types
    vendor = "Cisco"
    name = log.parsed_output

    # Parsing hostname
    try:
        name = re.match(r".*hostname\ (\S+)$", name, re.MULTILINE | re.DOTALL).group(1)
    except AttributeError as exc:
        raise AttributeError(f"Failed to match HOSTNAME regex on {name}") from exc
    name = utils.normalize_hostname(name)

    # Get or create Device
    data = {
        "name": name,
        "site_id": log.discoverable.site.id,
        "manufacturer": vendor,
    }
    device_o = device.get(name=data.get("name"))
    if not device_o:
        device_o = device.create(**data)

    # Link Device to Discoverable
    discoverable.update(log.discoverable, device_id=device_o.id)

    # Update the log
    log.ingested = True
    log.save()
