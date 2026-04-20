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
module: fortiadc_load_balance_content_routing
short_description: Configure content routing in Fortinet FortiADC.
description:
    - This module configures FortiADC content routing rules that direct traffic
      to specific server pools based on HTTP request attributes.
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
    load_balance_content_routing:
        description:
            - Configure content routing.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - Content routing name.
                type: str
                required: true
            type:
                description:
                    - Content routing type.
                type: str
                choices:
                    - 'l7-content-routing'
                    - 'l4-content-routing'
            pool:
                description:
                    - Default server pool.
                type: str
            comments:
                description:
                    - Comments or description.
                type: str
            content_routing_match_list:
                description:
                    - List of content routing match conditions.
                type: list
                elements: dict
                suboptions:
                    id:
                        description:
                            - Match entry ID.
                        type: int
                    match_type:
                        description:
                            - Match condition type.
                        type: str
                        choices:
                            - 'host'
                            - 'path'
                            - 'http-header'
                            - 'source-address'
                            - 'cookie'
                            - 'sni'
                    match_object:
                        description:
                            - Match object string (header name, cookie name, etc.).
                        type: str
                    match_condition:
                        description:
                            - Match condition.
                        type: str
                        choices:
                            - 'match-beginning'
                            - 'match-end'
                            - 'match-contain'
                            - 'match-domain-name'
                            - 'match-exact'
                            - 'match-regex'
                    match_expression:
                        description:
                            - Match expression string.
                        type: str
                    pool:
                        description:
                            - Server pool for matched traffic.
                        type: str
                    persistence:
                        description:
                            - Persistence profile.
                        type: str
                    method:
                        description:
                            - Load balancing method override.
                        type: str
"""

EXAMPLES = """
- name: Create content routing for API traffic
  fortinet.fortiadc.fortiadc_load_balance_content_routing:
    vdom: root
    state: present
    load_balance_content_routing:
      name: "cr_api"
      type: "l7-content-routing"
      pool: "api_pool"
      content_routing_match_list:
        - id: 1
          match_type: "path"
          match_condition: "match-beginning"
          match_expression: "/api/"
          pool: "api_pool"
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
        "name", "type", "pool", "comments", "content_routing_match_list",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def load_balance_content_routing(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    cr_data = data["load_balance_content_routing"]
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


def fortiadc_load_balance(data, fos, check_mode):
    if data["load_balance_content_routing"]:
        resp = load_balance_content_routing(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: load_balance_content_routing")
    if isinstance(resp, tuple) and len(resp) == 4:
        return resp
    return (
        not is_successful_status(resp),
        is_successful_status(resp) and resp.get("revision_changed", True),
        resp,
        {},
    )


def main():
    match_spec = {
        "id": {"required": False, "type": "int"},
        "match_type": {
            "required": False,
            "type": "str",
            "choices": ["host", "path", "http-header", "source-address", "cookie", "sni"],
        },
        "match_object": {"required": False, "type": "str"},
        "match_condition": {
            "required": False,
            "type": "str",
            "choices": [
                "match-beginning", "match-end", "match-contain",
                "match-domain-name", "match-exact", "match-regex",
            ],
        },
        "match_expression": {"required": False, "type": "str"},
        "pool": {"required": False, "type": "str"},
        "persistence": {"required": False, "type": "str"},
        "method": {"required": False, "type": "str"},
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
        "load_balance_content_routing": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "type": {
                    "required": False,
                    "type": "str",
                    "choices": ["l7-content-routing", "l4-content-routing"],
                },
                "pool": {"required": False, "type": "str"},
                "comments": {"required": False, "type": "str"},
                "content_routing_match_list": {
                    "required": False,
                    "type": "list",
                    "elements": "dict",
                    "options": match_spec,
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
