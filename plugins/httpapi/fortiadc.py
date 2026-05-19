# Copyright (c) 2024 Fortinet
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
name: fortiadc
short_description: HttpApi Plugin for Fortinet FortiADC Appliance or VM
description:
  - This HttpApi plugin provides methods to connect to Fortinet FortiADC Appliance or VM via REST API
author:
  - Ansible Content Engineering (@ansible)
version_added: "1.0.0"
"""

import json
import os
from datetime import datetime

from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.basic import to_text
from ansible.module_utils.six.moves import urllib


class HttpApi(HttpApiBase):
    def __init__(self, connection):
        super(HttpApi, self).__init__(connection)
        self._conn = connection
        self._system_version = None
        self._ansible_fortiadc_version = "v7.0.0"
        self._ansible_galaxy_version = "1.0.0"
        self._log = None
        self._logged_in = False
        self._api_login = False
        self._session_key = None
        self._cookie = None
        self._ccsrf_token = None

    def set_custom_option(self, k, v):
        self._options[k] = v

    _SENSITIVE_KEYS = frozenset((
        "password", "secretkey", "secret", "token", "access_token",
        "api_key", "private_key", "session_key",
    ))

    @staticmethod
    def _sanitize(data):
        if isinstance(data, dict):
            return {
                k: "********" if k.lower() in HttpApi._SENSITIVE_KEYS else HttpApi._sanitize(v)
                for k, v in data.items()
            }
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
                if isinstance(parsed, dict):
                    return json.dumps(HttpApi._sanitize(parsed))
            except (json.JSONDecodeError, TypeError):
                pass
            if "=" in data and "&" in data:
                parts = data.split("&")
                sanitized = []
                for part in parts:
                    if "=" in part:
                        k, v = part.split("=", 1)
                        if k.lower() in HttpApi._SENSITIVE_KEYS:
                            sanitized.append("%s=********" % k)
                            continue
                    sanitized.append(part)
                return "&".join(sanitized)
        return data

    def log(self, msg):
        log_enabled = self._options.get("enable_log", False)
        if not log_enabled:
            return
        if not self._log:
            log_path = os.path.join(
                os.environ.get("TMPDIR", "/tmp"),
                "fortiadc.ansible.log",
            )
            fd = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            self._log = os.fdopen(fd, "w")
            safe_opts = self._sanitize(dict(self.get_options()))
            self._log.write("All set options:")
            self._log.write(str(safe_opts) + "\n")
        log_message = str(datetime.now())
        log_message += ": " + str(msg) + "\n"
        self._log.write(log_message)
        self._log.flush()

    def get_access_token(self):
        token = self._options.get("access_token", None)
        if token:
            return token
        if self._conn.get_option("session_key"):
            token_from_session = self._conn.get_option("session_key").get(
                "access_token", None
            )
            if token_from_session:
                return token_from_session
        return self._session_key

    def set_become(self, become_context):
        return None

    def login(self, username, password):
        if self._logged_in:
            self.log("Already logged in, skipping")
            return

        if (username is None or password is None) and self.get_access_token() is None:
            raise Exception(
                "Please provide access token or username/password to login"
            )

        if self.get_access_token() is not None:
            self.log("login with access token")
            self._logged_in = True
            status, dummy = self.send_request(
                url="/api/v2/monitor/system/status",
                should_pre_login=False,
            )
            if status == 401:
                raise Exception("Invalid access token. Please check")
            self.log("login with access token succeeded")
            return

        self.log("login with username and password, try API based auth first")
        auth_payload = {
            "username": username,
            "secretkey": str(password),
            "password": str(password),
            "ack_post_disclaimer": True,
            "ack_pre_disclaimer": True,
            "request_key": True,
        }
        status_code, result_data = self.send_request(
            url="/api/v2/authentication",
            should_pre_login=False,
            data=json.dumps(auth_payload),
            method="POST",
        )
        self.log(
            "API based auth returned status code %s" % status_code
        )
        if status_code in [401, 404]:
            self.log("API based auth failed, fall back to /logincheck")
            data = (
                "username="
                + urllib.parse.quote(username)
                + "&secretkey="
                + urllib.parse.quote(password)
                + "&ajax=1"
            )
            dummy, result_data = self.send_request(
                url="/logincheck",
                should_pre_login=False,
                data=data,
                method="POST",
            )
            self.log(
                "/logincheck with user: %s %s"
                % (
                    username,
                    "succeeds" if result_data[0] == "1" else "fails",
                )
            )
            if result_data[0] != "1":
                raise Exception("Wrong credentials. Please check")
            self._logged_in = True
        else:
            self.log(
                "API based auth with user: %s %s"
                % (
                    username,
                    "succeeds" if "LOGIN_SUCCESS" in result_data else "fails",
                )
            )
            if "LOGIN_SUCCESS" not in result_data:
                raise Exception(
                    "API based auth failed: wrong credentials. Please check"
                )
            self._logged_in = True
            self._api_login = True
            try:
                json_result_data = json.loads(result_data)
                self._session_key = json_result_data["session_key"]
                self.log("session_key obtained from response body")
            except Exception:
                self.log(
                    "no session_key obtained from response body, fallback to parse headers"
                )

        self.update_system_version()

    def logout(self):
        if self._api_login:
            self.log("logout with API based auth")
            self.send_request(url="/api/v2/authentication", method="DELETE")
        else:
            self.send_request(url="/logout", method="POST")
            self.log("logout with basic based auth")

    def update_auth(self, response, response_text):
        headers = {
            "Accept": "application/json",
        }

        access_token = self.get_access_token()
        if access_token is not None:
            headers["Authorization"] = "Bearer " + access_token
            return headers

        if self._cookie or self._ccsrf_token:
            headers["Cookie"] = self._cookie
            headers["x-csrftoken"] = self._ccsrf_token
            return headers

        raw_cookies = []
        for attr, val in response.getheaders():
            if attr.lower() == "set-cookie" and "APSCOOKIE_" in val:
                headers["Cookie"] = val
            elif attr.lower() == "set-cookie" and (
                "ccsrftoken" in val or "ccsrf_token" in val
            ):
                token = val.split(";")[0].split("=")[1]
                headers["x-csrftoken"] = token
                self._ccsrf_token = token
            elif attr.lower() == "set-cookie":
                raw_cookies.append(val.split(";")[0])

        if raw_cookies:
            raw_cookie = "; ".join(raw_cookies)
            if "Cookie" in headers:
                raw_cookie += "; " + headers["Cookie"]
            headers["Cookie"] = raw_cookie
            self._cookie = headers["Cookie"]

        return headers

    def handle_httperror(self, exc):
        self.log("Exception thrown from handling http: " + to_text(exc))
        return exc

    def _concat_params(self, url, params):
        if not params or not len(params):
            return url
        url = url + "?" if "?" not in url else url
        for param_key in params:
            param_value = params[param_key]
            if url[-1] == "?":
                url += "%s=%s" % (param_key, param_value)
            else:
                url += "&%s=%s" % (param_key, param_value)
        return url

    def send_request(self, **message_kwargs):
        if not self._logged_in and message_kwargs.get("should_pre_login", True):
            self.log("perform pre request login")
            self.connection.send(
                "/api/v2/monitor/system/status", data={}, method="GET"
            )

        url = message_kwargs.get("url", "/")
        data = message_kwargs.get("data", "")
        method = message_kwargs.get("method", "GET")
        params = message_kwargs.get("params", {})
        headers = message_kwargs.get("headers") or {}

        if self.get_access_token() is not None:
            headers["Authorization"] = "Bearer %s" % self.get_access_token()

        url = self._concat_params(url, params)
        safe_data = self._sanitize(data) if data else ""
        self.log(
            "Sending request: METHOD:%s URL:%s DATA:%s" % (method, url, safe_data)
        )

        try:
            response, response_data = self.connection.send(
                url, data, method=method, headers=headers
            )
            json_formatted = to_text(response_data.getvalue())
            safe_response = self._sanitize(json_formatted)
            self.log(
                "response status: %s, data: %s...<truncated>"
                % (to_text(response.status), safe_response[:200])
            )
            return response.status, json_formatted
        except Exception as err:
            raise Exception("Error in send_request", err)

    def update_system_version(self):
        self.log("checking system_version")
        if self._system_version:
            return
        url = "/api/v2/monitor/system/status"
        status, result = self.send_request(url=url)
        self.log("system status returned status code %s" % status)
        result_json = json.loads(result)
        self._system_version = result_json.get("version", "undefined")
        self.log("system version: %s" % self._system_version)

    def get_system_version(self):
        self.update_system_version()
        return self._system_version
