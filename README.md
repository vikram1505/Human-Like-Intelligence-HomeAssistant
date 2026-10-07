# HLI — Human-Like Intelligence for Home Assistant

**Your sensors know what happened. HLI helps Home Assistant understand what it means.**

HLI is a local, read-only intelligence layer that discovers your Home Assistant areas and sensor capabilities, then creates explainable occupancy and room-intent entities automatically.

## What you get

- Automatic room discovery from Home Assistant Areas
- Capability discovery for presence, illuminance, media, contacts, batteries and environment sensors
- Explainable room occupancy scores and intent
- Primary/secondary room and house-occupied entities
- Confidence-first classification: ambiguous devices are not silently trusted
- No cloud account, no telemetry, no entity renaming
- **No physical device control in the core integration**

## Install

### HACS custom repository
1. Add this GitHub repository to HACS as an **Integration** custom repository.
2. Install **Human-Like Intelligence**.
3. Restart Home Assistant.
4. Go to **Settings → Devices & services → Add integration → Human-Like Intelligence**.
5. Add the dashboard in `dashboards/hli-dashboard.yaml` if you want the included overview.

### Manual
Copy `custom_components/hli` to `<config>/custom_components/hli`, restart Home Assistant, then add the integration from the UI.

## How it works

`HA registries → capability classification → room evidence → occupancy/intent → HLI entities`

Metadata and Home Assistant device classes are preferred over names. Generic switches are **not** guessed to be lights.

## Documentation

- [Getting started](docs/getting-started.md)
- [How HLI works](docs/how-hli-works.md)
- [Entities](docs/entities.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Privacy & safety](docs/privacy-and-safety.md)

## Status

`0.1.0` is the safe foundation release. It intentionally focuses on discovery and room intelligence before optional behaviour/actuation layers are added.

## Privacy

HLI processes Home Assistant state locally. The repository contains no household-specific entity IDs, hostnames, addresses, credentials, device identifiers or personal names.

MIT licensed. Contributions are welcome.
