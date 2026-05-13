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
module: fortiadc_load_balance_client_ssl_profile
short_description: Configure client SSL profiles in Fortinet FortiADC.
description:
    - This module configures FortiADC client SSL profiles that define SSL/TLS
      termination settings between clients and the FortiADC virtual server.
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
    load_balance_client_ssl_profile:
        description:
            - Configure client SSL profile.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - Client SSL profile name.
                type: str
                required: true
            ssl_allowed_versions:
                description:
                    - Allowed SSL/TLS versions.
                type: str
                choices:
                    - 'tlsv1.0'
                    - 'tlsv1.1'
                    - 'tlsv1.2'
                    - 'tlsv1.3'
                    - 'sslv3'
            ssl_min_version:
                description:
                    - Minimum SSL/TLS version.
                type: str
                choices:
                    - 'tlsv1.0'
                    - 'tlsv1.1'
                    - 'tlsv1.2'
                    - 'tlsv1.3'
            ssl_max_version:
                description:
                    - Maximum SSL/TLS version.
                type: str
                choices:
                    - 'tlsv1.0'
                    - 'tlsv1.1'
                    - 'tlsv1.2'
                    - 'tlsv1.3'
            ssl_ciphers:
                description:
                    - SSL cipher suite configuration.
                type: str
            ssl_custom_ciphers:
                description:
                    - Custom cipher suite string.
                type: str
            ssl_renegotiate_period:
                description:
                    - SSL renegotiation period in seconds.
                type: int
            ssl_renegotiate_size:
                description:
                    - SSL renegotiation data size in MB.
                type: int
            ssl_renegotiation:
                description:
                    - Enable/disable SSL renegotiation.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            ssl_secure_renegotiation:
                description:
                    - Enable/disable secure renegotiation.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            ssl_session_cache_flag:
                description:
                    - Enable/disable SSL session cache.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            ssl_certificate:
                description:
                    - Local certificate name.
                type: str
            ssl_certificate_verify:
                description:
                    - CA certificate name for client certificate verification.
                type: str
            ssl_client_certificate_verify:
                description:
                    - Enable/disable client certificate verification.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            ssl_sni:
                description:
                    - Enable/disable SNI support.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            backend_ssl:
                description:
                    - Enable/disable backend SSL.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            http_forward_client_certificate:
                description:
                    - Enable/disable forwarding client certificate to backend.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            http_forward_client_certificate_header:
                description:
                    - Header name for forwarded client certificate.
                type: str
"""

EXAMPLES = """
- name: Create client SSL profile with TLS 1.2+
  fortinet.fortiadc.fortiadc_load_balance_client_ssl_profile:
    vdom: root
    state: present
    load_balance_client_ssl_profile:
      name: "client_ssl_web"
      ssl_min_version: "tlsv1.2"
      ssl_max_version: "tlsv1.3"
      ssl_certificate: "wildcard_cert"
      ssl_session_cache_flag: "enable"
      ssl_renegotiation: "enable"
      ssl_secure_renegotiation: "enable"
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
        "name", "ssl_allowed_versions", "ssl_min_version", "ssl_max_version",
        "ssl_ciphers", "ssl_custom_ciphers", "ssl_renegotiate_period",
        "ssl_renegotiate_size", "ssl_renegotiation", "ssl_secure_renegotiation",
        "ssl_session_cache_flag", "ssl_certificate", "ssl_certificate_verify",
        "ssl_client_certificate_verify", "ssl_sni", "backend_ssl",
        "http_forward_client_certificate", "http_forward_client_certificate_header",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def load_balance_client_ssl_profile(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    ssl_data = data["load_balance_client_ssl_profile"]
    filtered_data = filter_data(ssl_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    if state == "present":
        return (
            False, True,
            fos.set("load-balance", "client-ssl-profile", data=converted_data, vdom=vdom),
            {},
        )
    elif state == "absent":
        return (
            False, True,
            fos.delete("load-balance", "client-ssl-profile", data=converted_data, vdom=vdom),
            {},
        )


def fortiadc_load_balance(data, fos, check_mode):
    if data["load_balance_client_ssl_profile"]:
        resp = load_balance_client_ssl_profile(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: load_balance_client_ssl_profile")
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
        "load_balance_client_ssl_profile": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "ssl_allowed_versions": {
                    "required": False, "type": "str",
                    "choices": ["tlsv1.0", "tlsv1.1", "tlsv1.2", "tlsv1.3", "sslv3"],
                },
                "ssl_min_version": {
                    "required": False, "type": "str",
                    "choices": ["tlsv1.0", "tlsv1.1", "tlsv1.2", "tlsv1.3"],
                },
                "ssl_max_version": {
                    "required": False, "type": "str",
                    "choices": ["tlsv1.0", "tlsv1.1", "tlsv1.2", "tlsv1.3"],
                },
                "ssl_ciphers": {"required": False, "type": "str"},
                "ssl_custom_ciphers": {"required": False, "type": "str"},
                "ssl_renegotiate_period": {"required": False, "type": "int"},
                "ssl_renegotiate_size": {"required": False, "type": "int"},
                "ssl_renegotiation": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "ssl_secure_renegotiation": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "ssl_session_cache_flag": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "ssl_certificate": {"required": False, "type": "str"},
                "ssl_certificate_verify": {"required": False, "type": "str"},
                "ssl_client_certificate_verify": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "ssl_sni": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "backend_ssl": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "http_forward_client_certificate": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "http_forward_client_certificate_header": {
                    "required": False, "type": "str",
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
