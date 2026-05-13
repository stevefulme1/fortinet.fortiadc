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
module: fortiadc_system_setting
short_description: Configure system settings in Fortinet FortiADC.
description:
    - This module configures FortiADC global system settings including
      hostname, time zone, administration, and HA configuration.
version_added: "1.0.0"
author:
    - Ansible Content Engineering (@ansible)
notes:
    - Requires httpapi connection plugin.
    - The module supports check_mode.
    - This is a singleton resource (no state/name parameters).
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
    system_setting:
        description:
            - Configure system settings.
        default: null
        type: dict
        suboptions:
            hostname:
                description:
                    - System hostname.
                type: str
            timezone:
                description:
                    - System time zone.
                type: str
            idle_timeout:
                description:
                    - Admin session idle timeout in seconds.
                type: int
            admin_sport:
                description:
                    - HTTPS administration port.
                type: int
            admin_port:
                description:
                    - HTTP administration port.
                type: int
            admin_ssh_port:
                description:
                    - SSH administration port.
                type: int
            admin_server_cert:
                description:
                    - Administration server certificate.
                type: str
            config_sync:
                description:
                    - Enable/disable configuration sync.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            language:
                description:
                    - GUI language.
                type: str
                choices:
                    - 'english'
                    - 'chinese'
                    - 'japanese'
                    - 'korean'
                    - 'french'
            intermediate_ca_group:
                description:
                    - Intermediate CA group name.
                type: str
            gui_log:
                description:
                    - Enable/disable GUI log display.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            vdom_admin:
                description:
                    - Enable/disable VDOM administration.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
"""

EXAMPLES = """
- name: Configure system settings
  fortinet.fortiadc.fortiadc_system_setting:
    vdom: root
    system_setting:
      hostname: "fortiadc-01"
      timezone: "US/Eastern"
      idle_timeout: 300
      admin_sport: 443
      admin_ssh_port: 22
      language: "english"
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
        "hostname", "timezone", "idle_timeout", "admin_sport", "admin_port",
        "admin_ssh_port", "admin_server_cert", "config_sync", "language",
        "intermediate_ca_group", "gui_log", "vdom_admin",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def system_setting(data, fos, check_mode=False):
    vdom = data["vdom"]
    setting_data = data["system_setting"]
    filtered_data = filter_data(setting_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    return (
        False, True,
        fos.set("system", "setting", data=converted_data, vdom=vdom),
        {},
    )


def fortiadc_system(data, fos, check_mode):
    if data["system_setting"]:
        resp = system_setting(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: system_setting")
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
        "system_setting": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "hostname": {"required": False, "type": "str"},
                "timezone": {"required": False, "type": "str"},
                "idle_timeout": {"required": False, "type": "int"},
                "admin_sport": {"required": False, "type": "int"},
                "admin_port": {"required": False, "type": "int"},
                "admin_ssh_port": {"required": False, "type": "int"},
                "admin_server_cert": {"required": False, "type": "str"},
                "config_sync": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "language": {
                    "required": False, "type": "str",
                    "choices": ["english", "chinese", "japanese", "korean", "french"],
                },
                "intermediate_ca_group": {"required": False, "type": "str"},
                "gui_log": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "vdom_admin": {
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
        fos = FortiADCHandler(connection, module, mkeyname=None)
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
