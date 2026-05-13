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
module: fortiadc_waf_profile
short_description: Configure WAF profiles in Fortinet FortiADC.
description:
    - This module configures FortiADC Web Application Firewall (WAF) profiles
      that provide application-layer security for virtual servers.
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
    waf_profile:
        description:
            - Configure WAF profile.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - WAF profile name.
                type: str
                required: true
            sql_injection_detection:
                description:
                    - Enable/disable SQL injection detection.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            xss_detection:
                description:
                    - Enable/disable cross-site scripting detection.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            csrf_protection:
                description:
                    - Enable/disable CSRF protection.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            cookie_security:
                description:
                    - Enable/disable cookie security.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            xml_validation:
                description:
                    - Enable/disable XML validation.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            json_validation:
                description:
                    - Enable/disable JSON validation.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            input_validation_policy:
                description:
                    - Input validation policy name.
                type: str
            brute_force_login:
                description:
                    - Enable/disable brute force login protection.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            http_protocol_constraint:
                description:
                    - Enable/disable HTTP protocol constraint checking.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            data_leak_prevention:
                description:
                    - Enable/disable data leak prevention.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            url_protection:
                description:
                    - URL protection policy name.
                type: str
            web_attack_signature:
                description:
                    - Enable/disable web attack signature detection.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            bot_detection:
                description:
                    - Enable/disable bot detection.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            api_gateway_policy:
                description:
                    - API gateway policy name.
                type: str
            exception_list:
                description:
                    - WAF exception list name.
                type: str
"""

EXAMPLES = """
- name: Create WAF profile with common protections
  fortinet.fortiadc.fortiadc_waf_profile:
    vdom: root
    state: present
    waf_profile:
      name: "waf_standard"
      sql_injection_detection: "enable"
      xss_detection: "enable"
      csrf_protection: "enable"
      cookie_security: "enable"
      http_protocol_constraint: "enable"
      web_attack_signature: "enable"
      bot_detection: "enable"
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
        "name", "sql_injection_detection", "xss_detection", "csrf_protection",
        "cookie_security", "xml_validation", "json_validation",
        "input_validation_policy", "brute_force_login",
        "http_protocol_constraint", "data_leak_prevention", "url_protection",
        "web_attack_signature", "bot_detection", "api_gateway_policy",
        "exception_list",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def waf_profile(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    waf_data = data["waf_profile"]
    filtered_data = filter_data(waf_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    if state == "present":
        return (
            False, True,
            fos.set("waf", "profile", data=converted_data, vdom=vdom),
            {},
        )
    elif state == "absent":
        return (
            False, True,
            fos.delete("waf", "profile", data=converted_data, vdom=vdom),
            {},
        )


def fortiadc_waf(data, fos, check_mode):
    if data["waf_profile"]:
        resp = waf_profile(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: waf_profile")
    if isinstance(resp, tuple) and len(resp) == 4:
        return resp
    return (
        not is_successful_status(resp),
        is_successful_status(resp) and resp.get("revision_changed", True),
        resp,
        {},
    )


def main():
    enable_disable = {"required": False, "type": "str", "choices": ["enable", "disable"]}

    fields = {
        "access_token": {"required": False, "type": "str", "no_log": True},
        "enable_log": {"required": False, "type": "bool", "default": False},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "member_path": {"required": False, "type": "str"},
        "member_state": {
            "type": "str", "required": False, "choices": ["present", "absent"],
        },
        "state": {"required": True, "type": "str", "choices": ["present", "absent"]},
        "waf_profile": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "sql_injection_detection": dict(enable_disable),
                "xss_detection": dict(enable_disable),
                "csrf_protection": dict(enable_disable),
                "cookie_security": dict(enable_disable),
                "xml_validation": dict(enable_disable),
                "json_validation": dict(enable_disable),
                "input_validation_policy": {"required": False, "type": "str"},
                "brute_force_login": dict(enable_disable),
                "http_protocol_constraint": dict(enable_disable),
                "data_leak_prevention": dict(enable_disable),
                "url_protection": {"required": False, "type": "str"},
                "web_attack_signature": dict(enable_disable),
                "bot_detection": dict(enable_disable),
                "api_gateway_policy": {"required": False, "type": "str"},
                "exception_list": {"required": False, "type": "str"},
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
        is_error, has_changed, result, diff = fortiadc_waf(
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
