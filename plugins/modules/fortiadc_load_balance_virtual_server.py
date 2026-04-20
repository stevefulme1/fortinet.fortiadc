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
module: fortiadc_load_balance_virtual_server
short_description: Configure virtual servers in Fortinet FortiADC.
description:
    - This module is able to configure a FortiADC appliance by allowing the
      user to set and modify load_balance feature and virtual_server category.
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
            - Virtual domain, among those defined previously. A vdom is a
              virtual instance of the FortiADC that can be configured and
              used as a different unit.
        type: str
        default: root
    member_path:
        type: str
        description:
            - Member attribute path to operate on.
            - Delimited by a slash character if there are more than one attribute.
    member_state:
        type: str
        description:
            - Add or delete a member under specified attribute path.
            - When member_state is specified, the state option is ignored.
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
    load_balance_virtual_server:
        description:
            - Configure virtual server.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - Virtual server name.
                type: str
                required: true
            status:
                description:
                    - Enable/disable virtual server.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            type:
                description:
                    - Virtual server type.
                type: str
                choices:
                    - 'l4-load-balance'
                    - 'l7-load-balance'
                    - 'l2-load-balance'
            address_type:
                description:
                    - Address type for the virtual server.
                type: str
                choices:
                    - 'ipv4'
                    - 'ipv6'
            address:
                description:
                    - IP address of the virtual server.
                type: str
            port:
                description:
                    - Service port for the virtual server.
                type: int
            interface:
                description:
                    - Network interface to bind.
                type: str
            profile:
                description:
                    - Virtual server profile name.
                type: str
            method:
                description:
                    - Load balancing method.
                type: str
                choices:
                    - 'LB_METHOD_ROUND_ROBIN'
                    - 'LB_METHOD_LEAST_CONNECTION'
                    - 'LB_METHOD_FASTEST_RESPONSE'
                    - 'LB_METHOD_HASH_SOURCE_ADDRESS'
                    - 'LB_METHOD_HASH_DESTINATION_ADDRESS'
                    - 'LB_METHOD_HASH_URI'
                    - 'LB_METHOD_HASH_HTTP_HEADER'
                    - 'LB_METHOD_HASH_HOST'
            pool:
                description:
                    - Real server pool name.
                type: str
            client_ssl_profile:
                description:
                    - Client SSL profile name.
                type: str
            server_ssl_profile:
                description:
                    - Server SSL profile name.
                type: str
            content_routing_list:
                description:
                    - Content routing list name.
                type: str
            connection_limit:
                description:
                    - Connection limit. 0 means unlimited.
                type: int
            connection_rate_limit:
                description:
                    - Connection rate limit. 0 means unlimited.
                type: int
            packet_fwd_method:
                description:
                    - Packet forwarding method.
                type: str
                choices:
                    - 'NAT'
                    - 'FullNAT'
                    - 'DirectRouting'
                    - 'Tunnel'
            persistence:
                description:
                    - Persistence profile name.
                type: str
            error_page:
                description:
                    - Error page profile name.
                type: str
            error_msg:
                description:
                    - Custom error message.
                type: str
            comments:
                description:
                    - Comments or description.
                type: str
            traffic_log:
                description:
                    - Enable/disable traffic logging.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            waf_profile:
                description:
                    - WAF profile name.
                type: str
            http2https:
                description:
                    - Enable/disable HTTP to HTTPS redirect.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            scripting_flag:
                description:
                    - Enable/disable scripting.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            scripting_list:
                description:
                    - Scripting rule list.
                type: str
"""

EXAMPLES = """
- name: Create a Layer 7 virtual server
  fortinet.fortiadc.fortiadc_load_balance_virtual_server:
    vdom: root
    state: present
    load_balance_virtual_server:
      name: "vs_web"
      status: "enable"
      type: "l7-load-balance"
      address: "10.0.1.100"
      port: 443
      pool: "web_pool"
      method: "LB_METHOD_ROUND_ROBIN"
      client_ssl_profile: "client_ssl_web"
      traffic_log: "enable"

- name: Delete a virtual server
  fortinet.fortiadc.fortiadc_load_balance_virtual_server:
    vdom: root
    state: absent
    load_balance_virtual_server:
      name: "vs_web"
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
mkey:
  description: Master key (id) used in the last call to FortiADC.
  returned: success
  type: str
  sample: "vs_web"
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
        "name", "status", "type", "address_type", "address", "port",
        "interface", "profile", "method", "pool", "client_ssl_profile",
        "server_ssl_profile", "content_routing_list", "connection_limit",
        "connection_rate_limit", "packet_fwd_method", "persistence",
        "error_page", "error_msg", "comments", "traffic_log", "waf_profile",
        "http2https", "scripting_flag", "scripting_list",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def load_balance_virtual_server(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    vs_data = data["load_balance_virtual_server"]
    filtered_data = filter_data(vs_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        diff = {"before": "", "after": filtered_data}
        mkey = fos.get_mkey("load-balance", "virtual-server", filtered_data, vdom=vdom)
        current_data = fos.get("load-balance", "virtual-server", vdom=vdom, mkey=mkey)
        is_existed = (
            current_data
            and current_data.get("http_status") == 200
            and isinstance(current_data.get("results"), list)
            and len(current_data["results"]) > 0
        )
        if state == "present":
            return False, True, filtered_data, diff
        elif state == "absent" and is_existed:
            return False, True, {}, diff
        return False, False, current_data, {}

    if state == "present":
        return (
            False,
            True,
            fos.set("load-balance", "virtual-server", data=converted_data, vdom=vdom),
            {},
        )
    elif state == "absent":
        return (
            False,
            True,
            fos.delete(
                "load-balance", "virtual-server", data=converted_data, vdom=vdom
            ),
            {},
        )


def fortiadc_load_balance(data, fos, check_mode):
    if data["load_balance_virtual_server"]:
        resp = load_balance_virtual_server(data, fos, check_mode)
    else:
        fos._module.fail_json(
            msg="missing task body: %s" % ("load_balance_virtual_server")
        )
    if isinstance(resp, tuple) and len(resp) == 4:
        return resp
    return (
        not is_successful_status(resp),
        is_successful_status(resp)
        and (resp.get("revision_changed", True)),
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
            "type": "str",
            "required": False,
            "choices": ["present", "absent"],
        },
        "state": {"required": True, "type": "str", "choices": ["present", "absent"]},
        "load_balance_virtual_server": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "status": {
                    "required": False,
                    "type": "str",
                    "choices": ["enable", "disable"],
                },
                "type": {
                    "required": False,
                    "type": "str",
                    "choices": [
                        "l4-load-balance",
                        "l7-load-balance",
                        "l2-load-balance",
                    ],
                },
                "address_type": {
                    "required": False,
                    "type": "str",
                    "choices": ["ipv4", "ipv6"],
                },
                "address": {"required": False, "type": "str"},
                "port": {"required": False, "type": "int"},
                "interface": {"required": False, "type": "str"},
                "profile": {"required": False, "type": "str"},
                "method": {
                    "required": False,
                    "type": "str",
                    "choices": [
                        "LB_METHOD_ROUND_ROBIN",
                        "LB_METHOD_LEAST_CONNECTION",
                        "LB_METHOD_FASTEST_RESPONSE",
                        "LB_METHOD_HASH_SOURCE_ADDRESS",
                        "LB_METHOD_HASH_DESTINATION_ADDRESS",
                        "LB_METHOD_HASH_URI",
                        "LB_METHOD_HASH_HTTP_HEADER",
                        "LB_METHOD_HASH_HOST",
                    ],
                },
                "pool": {"required": False, "type": "str"},
                "client_ssl_profile": {"required": False, "type": "str"},
                "server_ssl_profile": {"required": False, "type": "str"},
                "content_routing_list": {"required": False, "type": "str"},
                "connection_limit": {"required": False, "type": "int"},
                "connection_rate_limit": {"required": False, "type": "int"},
                "packet_fwd_method": {
                    "required": False,
                    "type": "str",
                    "choices": ["NAT", "FullNAT", "DirectRouting", "Tunnel"],
                },
                "persistence": {"required": False, "type": "str"},
                "error_page": {"required": False, "type": "str"},
                "error_msg": {"required": False, "type": "str"},
                "comments": {"required": False, "type": "str"},
                "traffic_log": {
                    "required": False,
                    "type": "str",
                    "choices": ["enable", "disable"],
                },
                "waf_profile": {"required": False, "type": "str"},
                "http2https": {
                    "required": False,
                    "type": "str",
                    "choices": ["enable", "disable"],
                },
                "scripting_flag": {
                    "required": False,
                    "type": "str",
                    "choices": ["enable", "disable"],
                },
                "scripting_list": {"required": False, "type": "str"},
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
            connection.set_custom_option(
                "access_token", module.params["access_token"]
            )
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
