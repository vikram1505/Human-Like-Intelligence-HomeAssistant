# Privacy & safety

HLI is local and read-only. It does not require a cloud service and does not contain telemetry code.

The core integration never calls light, switch, lock, climate, cover, or other actuator services. Generic switches are not assumed to be lights.

Diagnostics are deliberately aggregate: room/capability counts and HLI state. Raw entity IDs, device IDs, addresses, credentials and network identifiers are not included.
