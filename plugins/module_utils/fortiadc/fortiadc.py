# Copyright (c) 2024 Fortinet
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils._text import to_text

try:
    import urllib.parse as urlencoding
except ImportError:
    import urllib as urlencoding


SECRET_FIELDS = [
    "password", "passwd", "private_key", "secret", "secret_key",
    "access_token", "api_key", "client_secret", "preshared_key",
]


def is_secret_field(key_name):
    if key_name in SECRET_FIELDS:
        return True
    secret_suffixes = (
        "_password", "_passwd", "_private_key", "_api_key",
        "_client_secret", "_secret", "_secret_key", "_access_token",
    )
    for suffix in secret_suffixes:
        if key_name.endswith(suffix) and len(key_name) > len(suffix):
            return True
    return False


def schema_to_module_spec(schema):
    rdata = dict()
    if "type" not in schema:
        raise AssertionError("Invalid Schema")
    if schema["type"] == "dict" or (schema["type"] == "list" and "children" in schema):
        if "children" not in schema:
            raise AssertionError()
        rdata["type"] = schema["type"]
        if schema["type"] == "list":
            rdata["elements"] = schema.get("elements")
        rdata["required"] = schema.get("required", False)
        rdata["options"] = dict()
        for child in schema["children"]:
            child_value = schema["children"][child]
            rdata["options"][child] = schema_to_module_spec(child_value)
            if is_secret_field(child):
                rdata["options"][child]["no_log"] = True
    elif schema["type"] in ["integer", "string"] or (
        schema["type"] == "list" and "children" not in schema
    ):
        if schema["type"] == "integer":
            rdata["type"] = "int"
        elif schema["type"] == "string":
            rdata["type"] = "str"
        elif schema["type"] == "list":
            rdata["type"] = "list"
            rdata["elements"] = schema.get("elements")
        else:
            raise AssertionError()
        rdata["required"] = schema.get("required", False)
        if "options" in schema:
            rdata["choices"] = [option["value"] for option in schema["options"]]
    else:
        raise AssertionError()
    return rdata


def check_legacy_fortiadcapi(module):
    legacy_schemas = ["host", "username", "password", "ssl_verify", "https"]
    legacy_params = []
    for param in legacy_schemas:
        if param in module.params:
            legacy_params.append(param)
    if len(legacy_params):
        module.fail_json(
            msg="Legacy fortiadcapi parameters %s detected, please use HTTPAPI instead!"
            % (str(legacy_params))
        )


def is_successful_status(resp):
    return (
        "status" in resp
        and resp["status"] == "success"
        or "http_status" in resp
        and resp["http_status"] == 200
        or "http_method" in resp
        and resp["http_method"] == "DELETE"
        and resp["http_status"] == 404
    )


class FortiADCHandler(object):

    def __init__(self, conn, mod, module_mkeyname=None):
        self._conn = conn
        self._module = mod
        self._mkeyname = module_mkeyname

    def cmdb_url(self, path, name, vdom=None, mkey=None):
        url = "/api/v2/cmdb/" + path + "/" + name
        if mkey is not None:
            url = url + "/" + urlencoding.quote(str(mkey), safe="")
        if vdom is not None:
            if vdom == "global":
                url += "?global=1"
            elif vdom == "":
                url += "?vdom=root"
            else:
                url += "?vdom=" + vdom
        return url

    def mon_url(self, path, name, vdom=None, mkey=None):
        url = "/api/v2/monitor/" + path + "/" + name
        if mkey is not None:
            url = url + "/" + urlencoding.quote(str(mkey), safe="")
        if vdom is not None:
            if vdom == "global":
                url += "?global=1"
            elif vdom == "":
                url += "?vdom=root"
            else:
                url += "?vdom=" + vdom
        return url

    def get_mkeyname(self, path, name, vdom=None):
        return self._mkeyname

    def get_mkey(self, path, name, data, vdom=None):
        keyname = self.get_mkeyname(path, name, vdom)
        if not keyname:
            return None
        try:
            mkey = (
                data[keyname]
                if keyname in data
                else data[keyname.replace("_", "-")]
            )
        except KeyError:
            return None
        return mkey

    def get(self, path, name, vdom=None, mkey=None, parameters=None):
        url = self.cmdb_url(path, name, vdom, mkey=mkey)
        http_status, result_data = self._conn.send_request(
            url=url, params=parameters, method="GET"
        )
        return self.formatresponse(result_data, http_status, vdom=vdom)

    def set(self, path, name, data, mkey=None, vdom=None, parameters=None):
        if mkey is None:
            mkey = self.get_mkey(path, name, data, vdom=vdom)
        url = self.cmdb_url(path, name, vdom, mkey)

        http_get_status, dummy = self._conn.send_request(
            url=url, params=parameters, method="GET"
        )
        if http_get_status != 200:
            return self.post(path, name, data, vdom, mkey)

        http_status, result_data = self._conn.send_request(
            url=url,
            params=parameters,
            data=json.dumps(data),
            method="PUT",
        )
        return self.formatresponse(result_data, http_status, vdom=vdom)

    def post(self, path, name, data, vdom=None, mkey=None, parameters=None):
        if mkey:
            mkeyname = self.get_mkeyname(path, name, vdom)
            data[mkeyname] = mkey
        url = self.cmdb_url(path, name, vdom, mkey=None)
        http_status, result_data = self._conn.send_request(
            url=url,
            params=parameters,
            data=json.dumps(data),
            method="POST",
        )
        return self.formatresponse(result_data, http_status, vdom=vdom)

    def delete(self, path, name, vdom=None, mkey=None, parameters=None, data=None):
        if not mkey:
            mkey = self.get_mkey(path, name, data, vdom=vdom)
        url = self.cmdb_url(path, name, vdom, mkey)
        http_status, result_data = self._conn.send_request(
            url=url,
            params=parameters,
            data=json.dumps(data),
            method="DELETE",
        )
        return self.formatresponse(result_data, http_status, vdom=vdom)

    def formatresponse(self, res, http_status=200, vdom=None):
        try:
            resp = json.loads(to_text(res))
        except Exception:
            resp = {"raw": to_text(res)}
        if "status" not in resp:
            resp["status"] = "success" if http_status == 200 else "error"
        resp["http_status"] = http_status
        if vdom:
            resp["vdom"] = vdom
        return resp
