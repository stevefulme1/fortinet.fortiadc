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
module: fortiadc_certificate_info
short_description: Get certificate info from Fortinet FortiADC.
description:
    - This module retrieves local certificate information from FortiADC.
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
            - Name of a specific certificate to retrieve.
            - If not specified, all certificates are returned.
        type: str
    type:
        description:
            - Filter certificates by type.
        type: str
        choices:
            - 'local'
            - 'ca'
            - 'crl'
"""

EXAMPLES = """
- name: Get all local certificates
  fortinet.fortiadc.fortiadc_certificate_info:
    vdom: root
  register: result

- name: Get a specific certificate
  fortinet.fortiadc.fortiadc_certificate_info:
    vdom: root
    name: "web_cert"
  register: result
"""

RETURN = """
certificates:
  description: List of certificate objects.
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
        "type": {
            "required": False, "type": "str",
            "choices": ["local", "ca", "crl"],
        },
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)
    check_legacy_fortiadcapi(module)

    if module._socket_path:
        connection = Connection(module._socket_path)
        if "access_token" in module.params:
            connection.set_custom_option("access_token", module.params["access_token"])
        if "enable_log" in module.params:
            connection.set_custom_option("enable_log", module.params["enable_log"])
        else:
            connection.set_custom_option("enable_log", False)
        fos = FortiADCHandler(connection, module, mkeyname="name")

        try:
            vdom = module.params["vdom"]
            cert_type = module.params.get("type", "local") or "local"
            resource_map = {
                "local": "certificate-local",
                "ca": "certificate-ca",
                "crl": "certificate-crl",
            }
            resource = resource_map.get(cert_type, "certificate-local")

            if module.params.get("name"):
                resp = fos.get("system", resource, vdom=vdom, mkey=module.params["name"])
            else:
                resp = fos.get("system", resource, vdom=vdom)
            module.exit_json(changed=False, certificates=resp.get("results", [resp]))
        except Exception as e:
            module.fail_json(msg="Failed to get certificates: %s" % str(e))
    else:
        module.fail_json(**FAIL_SOCKET_MSG)


if __name__ == "__main__":
    main()
