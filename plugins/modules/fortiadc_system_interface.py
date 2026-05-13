from __future__ import absolute_import, division, print_function

# Copyright (c) 2024 Fortinet
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

__metaclass__ = type

ANSIBLE_METADATA = {
    "status": ["preview"],
    "supported_by": "community",
    "metadata_version": "1.1",
}

DOCUMENTATION = """
---
module: fortiadc_system_interface
short_description: Configure network interfaces in Fortinet FortiADC.
description:
    - This module configures FortiADC network interfaces including
      physical, VLAN, and loopback interfaces.
version_added: "1.0.0"
author:
    - Ansible Content Engineering (@ansible)
notes:
    - Requires httpapi connection plugin.
    - The module supports check_mode.
requirements:
    - ansible>=2.15
options:
    access_token:
        description:
            - Token-based authentication. Generated from GUI of FortiADC.
        type: str
        required: false
    enable_log:
        description:
            - Enable/Disable logging for task.
        type: bool
        required: false
        default: false
    vdom:
        description:
            - Virtual domain.
        type: str
        default: root
    member_path:
        type: str
        description:
            - Member attribute path to operate on.
    member_state:
        type: str
        description:
            - Add or delete a member under specified attribute path.
        choices:
            - 'present'
            - 'absent'
    state:
        description:
            - Indicates whether to create or remove the object.
        type: str
        required: true
        choices:
            - 'present'
            - 'absent'
    system_interface:
        description:
            - Configure system interface.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - Interface name.
                type: str
                required: true
            status:
                description:
                    - Enable/disable interface.
                type: str
                choices:
                    - 'up'
                    - 'down'
            type:
                description:
                    - Interface type.
                type: str
                choices:
                    - 'physical'
                    - 'vlan'
                    - 'loopback'
                    - 'aggregate'
                    - 'redundant'
            ip:
                description:
                    - IP address and netmask.
                type: str
            ip6:
                description:
                    - IPv6 address and prefix.
                type: str
            allowaccess:
                description:
                    - Allowed access protocols.
                type: str
            vlanid:
                description:
                    - VLAN ID (1-4094).
                type: int
            interface:
                description:
                    - Parent interface for VLAN.
                type: str
            mtu:
                description:
                    - Maximum transmission unit.
                type: int
            speed:
                description:
                    - Interface speed.
                type: str
                choices:
                    - 'auto'
                    - '10full'
                    - '10half'
                    - '100full'
                    - '100half'
                    - '1000full'
                    - '10000full'
                    - '25000full'
                    - '40000full'
                    - '100000full'
            aggregate_mode:
                description:
                    - Aggregate mode.
                type: str
                choices:
                    - '802.3ad'
                    - 'balance-xor'
                    - 'broadcast'
                    - 'round-robin'
            aggregate_algorithm:
                description:
                    - Aggregate hash algorithm.
                type: str
                choices:
                    - 'L2'
                    - 'L3'
                    - 'L4'
            redundant_member:
                description:
                    - Redundant interface members.
                type: str
            description:
                description:
                    - Description.
                type: str
            default_gw:
                description:
                    - Default gateway IP address.
                type: str
            dhcp:
                description:
                    - Enable/disable DHCP on this interface.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            dns_server_override:
                description:
                    - Enable/disable DNS server override from DHCP.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            floating_ip:
                description:
                    - Floating IP for HA.
                type: str
            floating_ip6:
                description:
                    - Floating IPv6 for HA.
                type: str
            traffic_group:
                description:
                    - Traffic group name for HA.
                type: str
"""

EXAMPLES = """
- name: Configure management interface
  fortinet.fortiadc.fortiadc_system_interface:
    vdom: root
    state: present
    system_interface:
      name: "port1"
      status: "up"
      ip: "192.168.1.1/24"
      allowaccess: "ping https ssh"
      mtu: 1500

- name: Create VLAN interface
  fortinet.fortiadc.fortiadc_system_interface:
    vdom: root
    state: present
    system_interface:
      name: "vlan100"
      type: "vlan"
      vlanid: 100
      interface: "port1"
      ip: "10.100.0.1/24"
      allowaccess: "ping"
"""

RETURN = """
status:
  description: Indication of the operation's result.
  returned: always
  type: str
  sample: "success"
http_status:
  description: HTTP status code from FortiADC API.
  returned: always
  type: int
  sample: 200
"""


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortiadc.plugins.module_utils.fortiadc.fortiadc import (
    FortiADCHandler,
    check_legacy_fortiadcapi,
    is_successful_status,
)
from ansible_collections.fortinet.fortiadc.plugins.module_utils.common.type_utils import (
    FAIL_SOCKET_MSG,
)
from ansible_collections.fortinet.fortiadc.plugins.module_utils.common.type_utils import (
    underscore_to_hyphen,
)


def filter_data(json_data):
    option_list = [
        "name", "status", "type", "ip", "ip6", "allowaccess", "vlanid",
        "interface", "mtu", "speed", "aggregate_mode", "aggregate_algorithm",
        "redundant_member", "description", "default_gw", "dhcp",
        "dns_server_override", "floating_ip", "floating_ip6", "traffic_group",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def system_interface(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    iface_data = data["system_interface"]
    filtered_data = filter_data(iface_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    if state == "present":
        return (
            False, True,
            fos.set("system", "interface", data=converted_data, vdom=vdom),
            {},
        )
    elif state == "absent":
        return (
            False, True,
            fos.delete("system", "interface", data=converted_data, vdom=vdom),
            {},
        )


def fortiadc_system(data, fos, check_mode):
    if data["system_interface"]:
        resp = system_interface(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: system_interface")
    if isinstance(resp, tuple) and len(resp) == 4:
        return resp
    return (
        not is_successful_status(resp),
        is_successful_status(resp) and resp.get("revision_changed", True),
        resp,
        {},
    )


def main():
    fields = {
        "access_token": {"required": False, "type": "str", "no_log": True},
        "enable_log": {"required": False, "type": "bool", "default": False},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "member_path": {"required": False, "type": "str"},
        "member_state": {
            "type": "str", "required": False, "choices": ["present", "absent"],
        },
        "state": {"required": True, "type": "str", "choices": ["present", "absent"]},
        "system_interface": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "status": {
                    "required": False, "type": "str", "choices": ["up", "down"],
                },
                "type": {
                    "required": False, "type": "str",
                    "choices": ["physical", "vlan", "loopback", "aggregate", "redundant"],
                },
                "ip": {"required": False, "type": "str"},
                "ip6": {"required": False, "type": "str"},
                "allowaccess": {"required": False, "type": "str"},
                "vlanid": {"required": False, "type": "int"},
                "interface": {"required": False, "type": "str"},
                "mtu": {"required": False, "type": "int"},
                "speed": {
                    "required": False, "type": "str",
                    "choices": [
                        "auto", "10full", "10half", "100full", "100half",
                        "1000full", "10000full", "25000full", "40000full", "100000full",
                    ],
                },
                "aggregate_mode": {
                    "required": False, "type": "str",
                    "choices": ["802.3ad", "balance-xor", "broadcast", "round-robin"],
                },
                "aggregate_algorithm": {
                    "required": False, "type": "str", "choices": ["L2", "L3", "L4"],
                },
                "redundant_member": {"required": False, "type": "str"},
                "description": {"required": False, "type": "str"},
                "default_gw": {"required": False, "type": "str"},
                "dhcp": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "dns_server_override": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "floating_ip": {"required": False, "type": "str"},
                "floating_ip6": {"required": False, "type": "str"},
                "traffic_group": {"required": False, "type": "str"},
            },
        },
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)
    check_legacy_fortiadcapi(module)

    is_error = False
    has_changed = False
    result = None
    diff = None

    if module._socket_path:
        connection = Connection(module._socket_path)
        if "access_token" in module.params:
            connection.set_custom_option("access_token", module.params["access_token"])
        if "enable_log" in module.params:
            connection.set_custom_option("enable_log", module.params["enable_log"])
        else:
            connection.set_custom_option("enable_log", False)
        fos = FortiADCHandler(connection, module, mkeyname="name")
        is_error, has_changed, result, diff = fortiadc_system(
            module.params, fos, module.check_mode
        )
    else:
        module.fail_json(**FAIL_SOCKET_MSG)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result, diff=diff)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == "__main__":
    main()
