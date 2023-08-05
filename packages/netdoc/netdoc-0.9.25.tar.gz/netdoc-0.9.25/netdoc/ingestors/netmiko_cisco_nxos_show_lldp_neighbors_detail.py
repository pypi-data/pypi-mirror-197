"""Ingestor for netmiko_cisco_nxos_show_lldp_neighbors_detail."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__date__ = "2022-09-07"
__version__ = "0.9.25"

from netdoc.schemas import interface, device, discoverable, cable
from netdoc import utils


def ingest(log):
    """Processing parsed output."""
    device_o = log.discoverable.device
    neighbors_per_interface = utils.count_interface_neighbors(
        log.parsed_output, "local_interface"
    )

    for item in log.parsed_output:
        # See https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_nxos/show_lldp_neighbors_detail # pylint: disable=line-too-long
        local_interface_name = item.get("local_interface")
        local_interface_label = utils.normalize_interface_label(local_interface_name)
        remote_management_ip = item.get("mgmt_address")
        remote_name = utils.normalize_hostname(item.get("neighbor"))
        remote_interface_name = item.get("neighbor_interface")
        remote_interface_label = utils.normalize_interface_label(remote_interface_name)

        if neighbors_per_interface.get(local_interface_label) > 1:
            # Skip interfaces with multiple neighbors
            continue

        # Get or create local Interface
        local_interface_o = interface.get(
            device_id=device_o.id, label=local_interface_label
        )
        if not local_interface_o:
            local_interface_data = {
                "name": local_interface_name,
                "device_id": device_o.id,
            }
            local_interface_o = interface.create(**local_interface_data)

        # Get or create remote Device
        remote_device_o = device.get(remote_name)
        if not remote_device_o:
            remote_device_data = {
                "name": remote_name,
                "site_id": device_o.site.id,
            }
            remote_device_o = device.create(**remote_device_data)

        # Get or create remote Interface
        remote_interface_o = interface.get(
            device_id=remote_device_o.id, label=remote_interface_label
        )
        if not remote_interface_o:
            remote_interface_data = {
                "name": remote_interface_name,
                "device_id": remote_device_o.id,
            }
            remote_interface_o = interface.create(**remote_interface_data)

        # Create remote Discoverable if not exist
        if remote_management_ip:
            # List by device name
            remote_discoverable_list = discoverable.get_list(device__name=remote_name)
            # Add list by IP address
            remote_discoverable_list += discoverable.get_list(
                address=remote_management_ip
            )
            if not remote_discoverable_list:
                remote_discoverable_data = {
                    "site_id": log.discoverable.site.id,
                    "mode": log.discoverable.mode,
                    "address": remote_management_ip,
                    "credential_id": log.discoverable.credential.id,
                    "device_id": remote_device_o.id,
                }
                discoverable.create(**remote_discoverable_data)

        # Link
        cable.link(
            left_interface_id=local_interface_o.id,
            right_interface_id=remote_interface_o.id,
        )

    # Update the log
    log.ingested = True
    log.save()
