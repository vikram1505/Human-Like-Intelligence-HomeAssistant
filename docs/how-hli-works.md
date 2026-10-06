# How HLI works

HLI reads Home Assistant's Area, Device and Entity registries and builds a local semantic model.

**Evidence order:** Home Assistant domain/device class → Area/device relationship → conservative name fallback.

Room evidence is fused into an occupancy score and an intent such as `vacant`, `passive_presence`, `occupied`, or `media_focus`. Each room occupancy entity includes confidence and a short explanation.

Missing capabilities degrade gracefully. A room does not need mmWave, media, or illuminance to exist.
