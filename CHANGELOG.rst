===========================
fortinet.fortiadc Release Notes
===========================

.. contents:: Topics

v1.0.0
======

Release Summary
---------------

Initial release of the ``fortinet.fortiadc`` Ansible collection.

Major Changes
-------------

- Added httpapi connection plugin for FortiADC REST API authentication (token and username/password).
- Added ``fortiadc_load_balance_virtual_server`` module for managing virtual servers.
- Added ``fortiadc_load_balance_pool`` module for managing real server pools.
- Added ``fortiadc_load_balance_health_check`` module for managing health check monitors.
- Added ``fortiadc_load_balance_content_routing`` module for managing content routing rules.
- Added ``fortiadc_load_balance_client_ssl_profile`` module for managing client SSL/TLS profiles.
- Added ``fortiadc_waf_profile`` module for managing WAF profiles.
- Added ``fortiadc_system_interface`` module for managing network interfaces.
- Added ``fortiadc_system_setting`` module for managing global system settings.
