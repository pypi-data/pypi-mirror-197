"""Ingestor for netmiko_cisco_nxos_show_mac_address_table."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__date__ = "2022-09-07"
__version__ = "0.9.25"

from netdoc.schemas import interface, macaddresstableentry
from netdoc import utils


def ingest(log):
    """Processing parsed output."""
    device_o = log.discoverable.device

    for item in log.parsed_output:
        # See https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_nxos/show_mac_address-table # pylint: disable=line-too-long
        interface_name = item.get("ports")
        label = utils.normalize_interface_label(interface_name)
        vlan_id = int(item.get("vlan"))
        mac_address = utils.normalize_mac_address(item.get("mac"))

        interface_o = interface.get(device_id=device_o.id, label=label)
        if not interface_o:
            interface_data = {
                "name": label,
                "device_id": device_o.id,
            }
            interface_o = interface.create(**interface_data)

        macaddresstableentry_o = macaddresstableentry.get(
            interface_id=interface_o.id, vvid=vlan_id, mac_address=mac_address
        )
        if not macaddresstableentry_o:
            data = {
                "interface_id": interface_o.id,
                "vvid": vlan_id,
                "mac_address": mac_address,
            }
            macaddresstableentry.create(**data)

    # Update the log
    log.ingested = True
    log.save()
