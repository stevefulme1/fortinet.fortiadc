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
module: fortiadc_load_balance_health_check_info
short_description: Get health check info from Fortinet FortiADC.
description:
    - This module retrieves health checks information from FortiADC.
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
    name:
        description:
            - Name of a specific resource to retrieve.
            - If not specified, all resources are returned.
        type: str
"""

EXAMPLES = """
- name: Get all health checks
  fortinet.fortiadc.fortiadc_load_balance_health_check_info:
    vdom: root
  register: result

- name: Get a specific health check
  fortinet.fortiadc.fortiadc_load_balance_health_check_info:
    vdom: root
    name: "example_name"
  register: result
"""

RETURN = """
health_checks:
  description: List of health checks objects.
  returned: always
  type: list
  elements: dict
"""


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortiadc.plugins.module_utils.fortiadc.fortiadc import (
    FortiADCHandler,
    check_legacy_fortiadcapi,
)
from ansible_collections.fortinet.fortiadc.plugins.module_utils.common.type_utils import (
    FAIL_SOCKET_MSG,
)


def main():
    fields = {
        "access_token": {"required": False, "type": "str", "no_log": True},
        "enable_log": {"required": False, "type": "bool", "default": False},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "name": {"required": False, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)
    check_legacy_fortiadcapi(module)

    if module._socket_path:
        connection = Connection(module._socket_path)
        if "access_token" in module.params:
            connection.set_custom_option(
                "access_token", module.params["access_token"],
            )
        if "enable_log" in module.params:
            connection.set_custom_option(
                "enable_log", module.params["enable_log"],
            )
        else:
            connection.set_custom_option("enable_log", False)
        fos = FortiADCHandler(connection, module, mkeyname="name")

        try:
            vdom = module.params["vdom"]
            if module.params.get("name"):
                resp = fos.get(
                    "load-balance", "health-check",
                    vdom=vdom, mkey=module.params["name"],
                )
            else:
                resp = fos.get("load-balance", "health-check", vdom=vdom)
            module.exit_json(
                changed=False,
                health_checks=resp.get("results", [resp]),
            )
        except Exception as e:
            module.fail_json(
                msg="Failed to get health checks: %s" % str(e),
            )
    else:
        module.fail_json(**FAIL_SOCKET_MSG)


if __name__ == "__main__":
    main()
