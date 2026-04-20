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
module: fortiadc_load_balance_pool
short_description: Configure real server pools in Fortinet FortiADC.
description:
    - This module configures FortiADC real server pools used by virtual servers
      for load balancing backend services.
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
    load_balance_pool:
        description:
            - Configure real server pool.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - Pool name.
                type: str
                required: true
            type:
                description:
                    - Address type.
                type: str
                choices:
                    - 'ipv4'
                    - 'ipv6'
            health_check:
                description:
                    - Health check object name.
                type: str
            health_check_relationship:
                description:
                    - Health check relationship.
                type: str
                choices:
                    - 'AND'
                    - 'OR'
            health_check_list:
                description:
                    - Health check list.
                type: str
            rs_profile:
                description:
                    - Real server SSL profile.
                type: str
            real_server_ssl_profile:
                description:
                    - Real server SSL profile for pool.
                type: str
            pool_member:
                description:
                    - Pool member list.
                type: list
                elements: dict
                suboptions:
                    id:
                        description:
                            - Pool member ID.
                        type: int
                    status:
                        description:
                            - Enable/disable pool member.
                        type: str
                        choices:
                            - 'enable'
                            - 'disable'
                    address:
                        description:
                            - IP address of the real server.
                        type: str
                    port:
                        description:
                            - Port number.
                        type: int
                    weight:
                        description:
                            - Weight for weighted load balancing.
                        type: int
                    connection_limit:
                        description:
                            - Connection limit for this member.
                        type: int
                    connection_rate_limit:
                        description:
                            - Connection rate limit for this member.
                        type: int
                    recover:
                        description:
                            - Recovery time in seconds.
                        type: int
                    warmup:
                        description:
                            - Warmup time in seconds.
                        type: int
                    warmrate:
                        description:
                            - Warmup rate (connections per second).
                        type: int
                    rs_profile_inherit:
                        description:
                            - Inherit real server profile from pool.
                        type: str
                        choices:
                            - 'enable'
                            - 'disable'
"""

EXAMPLES = """
- name: Create a real server pool
  fortinet.fortiadc.fortiadc_load_balance_pool:
    vdom: root
    state: present
    load_balance_pool:
      name: "web_pool"
      type: "ipv4"
      health_check: "hc_http"
      pool_member:
        - id: 1
          status: "enable"
          address: "10.0.2.10"
          port: 80
          weight: 100
        - id: 2
          status: "enable"
          address: "10.0.2.11"
          port: 80
          weight: 100
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
from ansible_collections.fortinet.fortiadc.plugins.module_utils.common import (
    FAIL_SOCKET_MSG,
)
from ansible_collections.fortinet.fortiadc.plugins.module_utils.common.type_utils import (
    underscore_to_hyphen,
)


def filter_data(json_data):
    option_list = [
        "name", "type", "health_check", "health_check_relationship",
        "health_check_list", "rs_profile", "real_server_ssl_profile",
        "pool_member",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def load_balance_pool(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    pool_data = data["load_balance_pool"]
    filtered_data = filter_data(pool_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    if state == "present":
        return (
            False, True,
            fos.set("load-balance", "pool", data=converted_data, vdom=vdom),
            {},
        )
    elif state == "absent":
        return (
            False, True,
            fos.delete("load-balance", "pool", data=converted_data, vdom=vdom),
            {},
        )


def fortiadc_load_balance(data, fos, check_mode):
    if data["load_balance_pool"]:
        resp = load_balance_pool(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: load_balance_pool")
    if isinstance(resp, tuple) and len(resp) == 4:
        return resp
    return (
        not is_successful_status(resp),
        is_successful_status(resp) and resp.get("revision_changed", True),
        resp,
        {},
    )


def main():
    pool_member_spec = {
        "id": {"required": False, "type": "int"},
        "status": {"required": False, "type": "str", "choices": ["enable", "disable"]},
        "address": {"required": False, "type": "str"},
        "port": {"required": False, "type": "int"},
        "weight": {"required": False, "type": "int"},
        "connection_limit": {"required": False, "type": "int"},
        "connection_rate_limit": {"required": False, "type": "int"},
        "recover": {"required": False, "type": "int"},
        "warmup": {"required": False, "type": "int"},
        "warmrate": {"required": False, "type": "int"},
        "rs_profile_inherit": {
            "required": False, "type": "str", "choices": ["enable", "disable"],
        },
    }

    fields = {
        "access_token": {"required": False, "type": "str", "no_log": True},
        "enable_log": {"required": False, "type": "bool", "default": False},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "member_path": {"required": False, "type": "str"},
        "member_state": {
            "type": "str", "required": False, "choices": ["present", "absent"],
        },
        "state": {"required": True, "type": "str", "choices": ["present", "absent"]},
        "load_balance_pool": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "type": {
                    "required": False, "type": "str", "choices": ["ipv4", "ipv6"],
                },
                "health_check": {"required": False, "type": "str"},
                "health_check_relationship": {
                    "required": False, "type": "str", "choices": ["AND", "OR"],
                },
                "health_check_list": {"required": False, "type": "str"},
                "rs_profile": {"required": False, "type": "str"},
                "real_server_ssl_profile": {"required": False, "type": "str"},
                "pool_member": {
                    "required": False,
                    "type": "list",
                    "elements": "dict",
                    "options": pool_member_spec,
                },
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
        is_error, has_changed, result, diff = fortiadc_load_balance(
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
