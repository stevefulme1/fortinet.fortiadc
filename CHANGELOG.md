# Changelog

All notable changes to **fortinet.fortiadc** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2026-05-18

### Security

- Sanitize response body before logging in httpapi `send_request` to prevent credential exposure
- Add confirmation log for session_key retrieval without exposing the key value

## [2.0.0] - 2026-05-15

### Added

- Firewall, logging, certificate, and content routing modules
- Pre-commit and linting configuration
- YAML document-start markers for lint compliance

### Fixed

- CI lint failures resolved

## [1.0.0] - 2026-05-15

### Added

- Initial release of fortinet.fortiadc Ansible collection
- httpapi connection plugin for FortiADC REST API
- CI workflow with lint, sanity, and unit tests
- Auto-merge workflow for owner PRs

### Fixed

- Cleartext credential logging in httpapi plugin

### Security

- Fix cleartext credential logging in httpapi plugin
