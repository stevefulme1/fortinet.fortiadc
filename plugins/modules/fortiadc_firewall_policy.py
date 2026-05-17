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
module: fortiadc_firewall_policy
short_description: Manage firewall policies in Fortinet FortiADC.
description:
    - This module manages FortiADC firewall policies that control traffic
      filtering, access control, and network security enforcement.
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
    firewall_policy:
        description:
            - Configure firewall policy.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - Policy name.
                type: str
                required: true
            status:
                description:
                    - Enable/disable the policy.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            action:
                description:
                    - Policy action.
                type: str
                choices:
                    - 'accept'
                    - 'deny'
            srcintf:
                description:
                    - Source interface.
                type: str
            dstintf:
                description:
                    - Destination interface.
                type: str
            srcaddr:
                description:
                    - Source address object name.
                type: str
            dstaddr:
                description:
                    - Destination address object name.
                type: str
            service:
                description:
                    - Service object name.
                type: str
            schedule:
                description:
                    - Schedule object name.
                type: str
            log:
                description:
                    - Enable/disable traffic logging.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            comments:
                description:
                    - Comments or description.
                type: str
"""

EXAMPLES = """
- name: Create a firewall policy
  fortinet.fortiadc.fortiadc_firewall_policy:
    vdom: root
    state: present
    firewall_policy:
      name: "allow_web"
      status: "enable"
      action: "accept"
      srcintf: "port1"
      dstintf: "port2"
      srcaddr: "all"
      dstaddr: "webservers"
      service: "HTTP"
      log: "enable"

- name: Remove a firewall policy
  fortinet.fortiadc.fortiadc_firewall_policy:
    vdom: root
    state: absent
    firewall_policy:
      name: "allow_web"
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
        "name", "status", "action", "srcintf", "dstintf",
        "srcaddr", "dstaddr", "service", "schedule", "log", "comments",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def firewall_policy(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    policy_data = data["firewall_policy"]
    filtered_data = filter_data(policy_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    if state == "present":
        return (
            False, True,
            fos.set("firewall", "policy", data=converted_data, vdom=vdom),
            {},
        )
    elif state == "absent":
        return (
            False, True,
            fos.delete("firewall", "policy", data=converted_data, vdom=vdom),
            {},
        )


def fortiadc_firewall(data, fos, check_mode):
    if data["firewall_policy"]:
        resp = firewall_policy(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: firewall_policy")
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
        "firewall_policy": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "status": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "action": {
                    "required": False, "type": "str", "choices": ["accept", "deny"],
                },
                "srcintf": {"required": False, "type": "str"},
                "dstintf": {"required": False, "type": "str"},
                "srcaddr": {"required": False, "type": "str"},
                "dstaddr": {"required": False, "type": "str"},
                "service": {"required": False, "type": "str"},
                "schedule": {"required": False, "type": "str"},
                "log": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "comments": {"required": False, "type": "str"},
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
        is_error, has_changed, result, diff = fortiadc_firewall(
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
