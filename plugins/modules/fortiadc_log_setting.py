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
module: fortiadc_log_setting
short_description: Configure logging in Fortinet FortiADC.
description:
    - This module configures FortiADC logging settings including
      remote syslog, disk logging, and log severity filters.
version_added: "1.0.0"
author:
    - Ansible Content Engineering (@ansible)
notes:
    - Requires httpapi connection plugin.
    - The module supports check_mode.
    - This is a singleton resource (no state/name parameters needed).
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
    log_setting:
        description:
            - Configure log settings.
        default: null
        type: dict
        suboptions:
            remote_log:
                description:
                    - Enable/disable remote logging.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            remote_log_server:
                description:
                    - Remote syslog server address.
                type: str
            remote_log_port:
                description:
                    - Remote syslog server port.
                type: int
            remote_log_facility:
                description:
                    - Syslog facility.
                type: str
            remote_log_csv:
                description:
                    - Enable/disable CSV format for remote logs.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            disk_log:
                description:
                    - Enable/disable disk logging.
                type: str
                choices:
                    - 'enable'
                    - 'disable'
            severity:
                description:
                    - Minimum severity level.
                type: str
                choices:
                    - 'emergency'
                    - 'alert'
                    - 'critical'
                    - 'error'
                    - 'warning'
                    - 'notification'
                    - 'information'
                    - 'debug'
"""

EXAMPLES = """
- name: Configure remote syslog logging
  fortinet.fortiadc.fortiadc_log_setting:
    vdom: root
    log_setting:
      remote_log: "enable"
      remote_log_server: "10.0.1.100"
      remote_log_port: 514
      severity: "warning"

- name: Enable disk logging
  fortinet.fortiadc.fortiadc_log_setting:
    vdom: root
    log_setting:
      disk_log: "enable"
      severity: "information"
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
        "remote_log", "remote_log_server", "remote_log_port",
        "remote_log_facility", "remote_log_csv", "disk_log", "severity",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def log_setting(data, fos, check_mode=False):
    vdom = data["vdom"]
    setting_data = data["log_setting"]
    filtered_data = filter_data(setting_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    return (
        False, True,
        fos.set("log", "setting", data=converted_data, vdom=vdom),
        {},
    )


def fortiadc_log(data, fos, check_mode):
    if data["log_setting"]:
        resp = log_setting(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: log_setting")
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
        "log_setting": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "remote_log": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "remote_log_server": {"required": False, "type": "str"},
                "remote_log_port": {"required": False, "type": "int"},
                "remote_log_facility": {"required": False, "type": "str"},
                "remote_log_csv": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "disk_log": {
                    "required": False, "type": "str", "choices": ["enable", "disable"],
                },
                "severity": {
                    "required": False, "type": "str",
                    "choices": [
                        "emergency", "alert", "critical", "error",
                        "warning", "notification", "information", "debug",
                    ],
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
        is_error, has_changed, result, diff = fortiadc_log(
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
