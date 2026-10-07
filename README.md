# HLI — Human-Like Intelligence for Home Assistant

[![Validate](https://github.com/vikram1505/Human-Like-Intelligence-HomeAssistant/actions/workflows/validate.yml/badge.svg)](https://github.com/vikram1505/Human-Like-Intelligence-HomeAssistant/actions/workflows/validate.yml)
[![Hassfest](https://github.com/vikram1505/Human-Like-Intelligence-HomeAssistant/actions/workflows/hassfest.yml/badge.svg)](https://github.com/vikram1505/Human-Like-Intelligence-HomeAssistant/actions/workflows/hassfest.yml)
[![HACS](https://github.com/vikram1505/Human-Like-Intelligence-HomeAssistant/actions/workflows/hacs.yml/badge.svg)](https://github.com/vikram1505/Human-Like-Intelligence-HomeAssistant/actions/workflows/hacs.yml)

[![Open your Home Assistant instance and add this repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=vikram1505&repository=Human-Like-Intelligence-HomeAssistant&category=integration)

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

Click the **Open your Home Assistant instance** button above to open this repository in HACS, then:

1. Confirm the repository is added as an **Integration**.
2. Install **Human-Like Intelligence**.
3. Restart Home Assistant.
4. Go to **Settings → Devices & services → Add integration → Human-Like Intelligence**.
5. Add the dashboard in `dashboards/hli-dashboard.yaml` if you want the included overview.

Until HLI is accepted into the HACS default repository list, the button adds this GitHub repository as a custom HACS repository.

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
- [CI troubleshooting](docs/ci-troubleshooting.md)
- [Privacy & safety](docs/privacy-and-safety.md)

## Status

`0.1.2` is the safe foundation release. It intentionally focuses on discovery and room intelligence before optional behaviour/actuation layers are added.

## Privacy

HLI processes Home Assistant state locally. The repository contains no household-specific entity IDs, hostnames, addresses, credentials, device identifiers or personal names.

MIT licensed. Contributions are welcome.
