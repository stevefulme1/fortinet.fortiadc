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
module: fortiadc_load_balance_health_check
short_description: Configure health checks in Fortinet FortiADC.
description:
    - This module configures FortiADC health check objects used to monitor
      real server availability in server pools.
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
    load_balance_health_check:
        description:
            - Configure health check.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - Health check name.
                type: str
                required: true
            type:
                description:
                    - Health check type.
                type: str
                choices:
                    - 'icmp'
                    - 'tcp'
                    - 'http'
                    - 'https'
                    - 'dns'
                    - 'smtp'
                    - 'pop3'
                    - 'imap'
                    - 'radius'
                    - 'ldap'
                    - 'snmp'
                    - 'mysql'
                    - 'script'
                    - 'sip'
                    - 'l2-detection'
            interval:
                description:
                    - Interval between health checks in seconds.
                type: int
            timeout:
                description:
                    - Timeout for each health check in seconds.
                type: int
            up_retry:
                description:
                    - Number of successful checks to mark server as up.
                type: int
            down_retry:
                description:
                    - Number of failed checks to mark server as down.
                type: int
            dest_addr_type:
                description:
                    - Destination address type.
                type: str
                choices:
                    - 'ipv4'
                    - 'ipv6'
            dest_addr:
                description:
                    - Destination IP address.
                type: str
            port:
                description:
                    - Port number to check.
                type: int
            http_method:
                description:
                    - HTTP method for HTTP/HTTPS health checks.
                type: str
                choices:
                    - 'http_get'
                    - 'http_head'
                    - 'http_connect'
            http_url:
                description:
                    - URL path for HTTP/HTTPS health checks.
                type: str
            http_status_code:
                description:
                    - Expected HTTP status code.
                type: str
            http_body:
                description:
                    - Expected HTTP response body content.
                type: str
            send_string:
                description:
                    - String to send to the server.
                type: str
            receive_string:
                description:
                    - Expected string in server response.
                type: str
            domain_name:
                description:
                    - Domain name for DNS health checks.
                type: str
            host_addr:
                description:
                    - Host header for HTTP health checks.
                type: str
            match_type:
                description:
                    - Match type for response checking.
                type: str
                choices:
                    - 'match_status'
                    - 'match_string'
                    - 'match_all'
"""

EXAMPLES = """
- name: Create HTTP health check
  fortinet.fortiadc.fortiadc_load_balance_health_check:
    vdom: root
    state: present
    load_balance_health_check:
      name: "hc_http"
      type: "http"
      interval: 10
      timeout: 5
      up_retry: 3
      down_retry: 3
      port: 80
      http_method: "http_get"
      http_url: "/health"
      http_status_code: "200"
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
        "name", "type", "interval", "timeout", "up_retry", "down_retry",
        "dest_addr_type", "dest_addr", "port", "http_method", "http_url",
        "http_status_code", "http_body", "send_string", "receive_string",
        "domain_name", "host_addr", "match_type",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def load_balance_health_check(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    hc_data = data["load_balance_health_check"]
    filtered_data = filter_data(hc_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    if state == "present":
        return (
            False, True,
            fos.set("load-balance", "health-check", data=converted_data, vdom=vdom),
            {},
        )
    elif state == "absent":
        return (
            False, True,
            fos.delete("load-balance", "health-check", data=converted_data, vdom=vdom),
            {},
        )


def fortiadc_load_balance(data, fos, check_mode):
    if data["load_balance_health_check"]:
        resp = load_balance_health_check(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: load_balance_health_check")
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
        "load_balance_health_check": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "type": {
                    "required": False,
                    "type": "str",
                    "choices": [
                        "icmp", "tcp", "http", "https", "dns", "smtp",
                        "pop3", "imap", "radius", "ldap", "snmp", "mysql",
                        "script", "sip", "l2-detection",
                    ],
                },
                "interval": {"required": False, "type": "int"},
                "timeout": {"required": False, "type": "int"},
                "up_retry": {"required": False, "type": "int"},
                "down_retry": {"required": False, "type": "int"},
                "dest_addr_type": {
                    "required": False, "type": "str", "choices": ["ipv4", "ipv6"],
                },
                "dest_addr": {"required": False, "type": "str"},
                "port": {"required": False, "type": "int"},
                "http_method": {
                    "required": False,
                    "type": "str",
                    "choices": ["http_get", "http_head", "http_connect"],
                },
                "http_url": {"required": False, "type": "str"},
                "http_status_code": {"required": False, "type": "str"},
                "http_body": {"required": False, "type": "str"},
                "send_string": {"required": False, "type": "str"},
                "receive_string": {"required": False, "type": "str"},
                "domain_name": {"required": False, "type": "str"},
                "host_addr": {"required": False, "type": "str"},
                "match_type": {
                    "required": False,
                    "type": "str",
                    "choices": ["match_status", "match_string", "match_all"],
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
