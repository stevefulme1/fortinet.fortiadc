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
module: fortiadc_certificate
short_description: Manage certificates in Fortinet FortiADC.
description:
    - This module manages local certificates on FortiADC for SSL
      offloading, server authentication, and client verification.
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
    certificate:
        description:
            - Configure local certificate.
        default: null
        type: dict
        suboptions:
            name:
                description:
                    - Certificate name.
                type: str
                required: true
            type:
                description:
                    - Certificate type.
                type: str
                choices:
                    - 'local'
                    - 'ca'
                    - 'crl'
            cert:
                description:
                    - PEM-encoded certificate content.
                type: str
            key:
                description:
                    - PEM-encoded private key content.
                type: str
            passwd:
                description:
                    - Password for encrypted private key.
                type: str
            comments:
                description:
                    - Comments or description.
                type: str
"""

EXAMPLES = """
- name: Import a local certificate
  fortinet.fortiadc.fortiadc_certificate:
    vdom: root
    state: present
    certificate:
      name: "web_cert"
      type: "local"
      cert: "{{ lookup('file', 'cert.pem') }}"
      key: "{{ lookup('file', 'key.pem') }}"

- name: Remove a certificate
  fortinet.fortiadc.fortiadc_certificate:
    vdom: root
    state: absent
    certificate:
      name: "web_cert"
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
        "name", "type", "cert", "key", "passwd", "comments",
    ]
    dictionary = {}
    for attribute in option_list:
        if attribute in json_data and json_data[attribute] is not None:
            dictionary[attribute] = json_data[attribute]
    return dictionary


def certificate_config(data, fos, check_mode=False):
    state = data.get("state", None)
    vdom = data["vdom"]
    cert_data = data["certificate"]
    filtered_data = filter_data(cert_data)
    converted_data = underscore_to_hyphen(filtered_data)

    if check_mode:
        return False, True, filtered_data, {"before": "", "after": filtered_data}

    if state == "present":
        return (
            False, True,
            fos.set("system", "certificate-local", data=converted_data, vdom=vdom),
            {},
        )
    elif state == "absent":
        return (
            False, True,
            fos.delete("system", "certificate-local", data=converted_data, vdom=vdom),
            {},
        )


def fortiadc_certificate(data, fos, check_mode):
    if data["certificate"]:
        resp = certificate_config(data, fos, check_mode)
    else:
        fos._module.fail_json(msg="missing task body: certificate")
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
        "certificate": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {
                "name": {"required": True, "type": "str"},
                "type": {
                    "required": False, "type": "str",
                    "choices": ["local", "ca", "crl"],
                },
                "cert": {"required": False, "type": "str"},
                "key": {"required": False, "type": "str", "no_log": True},
                "passwd": {"required": False, "type": "str", "no_log": True},
                "comments": {"required": False, "type": "str"},
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
        is_error, has_changed, result, diff = fortiadc_certificate(
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
