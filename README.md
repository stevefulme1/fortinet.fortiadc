# Fortinet FortiADC Collection for Ansible

This collection provides Ansible modules for managing Fortinet FortiADC application delivery controllers via the REST API.

## Requirements

- Ansible >= 2.15
- FortiADC appliance with REST API enabled
- `ansible.netcommon` collection

## Installation

```bash
ansible-galaxy collection install fortinet.fortiadc
```

## Connection Setup

FortiADC modules use the `httpapi` connection plugin. Configure your inventory:

```ini
[fortiadc]
fortiadc01 ansible_host=192.168.1.1

[fortiadc:vars]
ansible_network_os=fortinet.fortiadc.fortiadc
ansible_connection=httpapi
ansible_httpapi_use_ssl=true
ansible_httpapi_validate_certs=false
ansible_httpapi_port=443
```

### Authentication

**Token-based (recommended):**
```yaml
- name: Configure with token
  fortinet.fortiadc.fortiadc_system_setting:
    access_token: "your-api-token"
    system_setting:
      hostname: "fortiadc-01"
```

**Username/password:**
```ini
ansible_user=admin
ansible_password=your_password
```

## Modules

| Module | Description |
| :----- | :---------- |
| `fortiadc_load_balance_virtual_server` | Configure virtual servers (L4/L7 load balancing) |
| `fortiadc_load_balance_pool` | Configure real server pools |
| `fortiadc_load_balance_health_check` | Configure health check monitors |
| `fortiadc_load_balance_content_routing` | Configure content routing rules |
| `fortiadc_load_balance_client_ssl_profile` | Configure client SSL/TLS profiles |
| `fortiadc_waf_profile` | Configure Web Application Firewall profiles |
| `fortiadc_system_interface` | Configure network interfaces |
| `fortiadc_system_setting` | Configure global system settings |

## Example Playbook

```yaml
---
- name: Configure FortiADC load balancing
  hosts: fortiadc
  gather_facts: false
  tasks:
    - name: Create health check
      fortinet.fortiadc.fortiadc_load_balance_health_check:
        vdom: root
        state: present
        load_balance_health_check:
          name: "hc_http"
          type: "http"
          interval: 10
          timeout: 5
          up_retry: 3
          down_retry: 3
          port: 80
          http_method: "http_get"
          http_url: "/health"
          http_status_code: "200"

    - name: Create server pool
      fortinet.fortiadc.fortiadc_load_balance_pool:
        vdom: root
        state: present
        load_balance_pool:
          name: "web_pool"
          type: "ipv4"
          health_check: "hc_http"
          pool_member:
            - id: 1
              status: "enable"
              address: "10.0.2.10"
              port: 80
              weight: 100
            - id: 2
              status: "enable"
              address: "10.0.2.11"
              port: 80
              weight: 100

    - name: Create SSL profile
      fortinet.fortiadc.fortiadc_load_balance_client_ssl_profile:
        vdom: root
        state: present
        load_balance_client_ssl_profile:
          name: "client_ssl_web"
          ssl_min_version: "tlsv1.2"
          ssl_max_version: "tlsv1.3"
          ssl_certificate: "wildcard_cert"
          ssl_session_cache_flag: "enable"

    - name: Create virtual server
      fortinet.fortiadc.fortiadc_load_balance_virtual_server:
        vdom: root
        state: present
        load_balance_virtual_server:
          name: "vs_web"
          status: "enable"
          type: "l7-load-balance"
          address: "10.0.1.100"
          port: 443
          pool: "web_pool"
          method: "LB_METHOD_ROUND_ROBIN"
          client_ssl_profile: "client_ssl_web"
          traffic_log: "enable"
```

## License

GPL-3.0-or-later
