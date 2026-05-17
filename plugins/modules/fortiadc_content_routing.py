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
module: fortiadc_content_routing
short_description: Manage content routing rules in Fortinet FortiADC.
description:
    - This module manages FortiADC content routing rules for directing
      traffic based on URI, host, headers, and other HTTP attributes.
    - Provides a simplified interface compared to
      C(fortiadc_load_balance_content_routing).
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
    content_routing:
        description:
            - Configure content routing rule.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - Content routing rule name.
                type: str
                required: true
            type:
                description:
                    - Routing type.
                type: str
                choices:
                    - 'l7-content-routing'
                    - 'l4-content-routing'
            pool:
                description:
                    - Default server pool.
                type: str
            ip:
                description:
                    - Source IP address filter.
                type: str
            ip6:
                description:
                    - Source IPv6 address filter.
                type: str
            comments:
                description:
                    - Comments or description.
                type: str
            connection_pool:
                description:
                    - Connection pool profile.
                type: str
            connection_pool_inherit:
                description:
                    - Inherit connection pool from virtual server.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            schedule_pool:
                description:
                    - Schedule pool profile.
                type: str
            schedule_pool_inherit:
                description:
                    - Inherit schedule pool from virtual server.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            persistence:
                description:
                    - Persistence profile.
                type: str
            persistence_inherit:
                description:
                    - Inherit persistence from virtual server.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            method:
                description:
                    - Load balancing method.
                type: str
            method_inherit:
                description:
                    - Inherit method from virtual server.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
"""

EXAMPLES = """
- name: Create content routing rule
  fortinet.fortiadc.fortiadc_content_routing:
    vdom: root
    state: present
    content_routing:
      name: "cr_static_assets"
      type: "l7-content-routing"
      pool: "static_pool"
      comments: "Route static asset requests"

- name: Remove content routing rule
  fortinet.fortiadc.fortiadc_content_routing:
    vdom: root
    state: absent
    content_routing:
      name: "cr_static_assets"
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
        "name", "type", "pool", "ip", "ip6", "comments",
        "connection_pool", "connection_pool_inherit",
        "schedule_pool", "schedule_pool_inherit",
        "persistence", "persistence_inherit",
        "method", "method_inherit",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def content_routing(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    cr_data = data["content_routing"]
    filtered_data = filter_data(cr_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    if state == "present":
        return (
            False, True,
            fos.set("load-balance", "content-routing", data=converted_data, vdom=vdom),
            {},
        )
    elif state == "absent":
        return (
            False, True,
            fos.delete("load-balance", "content-routing", data=converted_data, vdom=vdom),
            {},
        )


def fortiadc_content_routing_handler(data, fos, check_mode):
    if data["content_routing"]:
        resp = content_routing(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: content_routing")
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
        "content_routing": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "type": {
                    "required": False, "type": "str",
                    "choices": ["l7-content-routing", "l4-content-routing"],
                },
                "pool": {"required": False, "type": "str"},
                "ip": {"required": False, "type": "str"},
                "ip6": {"required": False, "type": "str"},
                "comments": {"required": False, "type": "str"},
                "connection_pool": {"required": False, "type": "str"},
                "connection_pool_inherit": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "schedule_pool": {"required": False, "type": "str"},
                "schedule_pool_inherit": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "persistence": {"required": False, "type": "str"},
                "persistence_inherit": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "method": {"required": False, "type": "str"},
                "method_inherit": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
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
        is_error, has_changed, result, diff = fortiadc_content_routing_handler(
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
