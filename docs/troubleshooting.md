# Troubleshooting

**A room is missing** — Create/assign the Area in Home Assistant, then reload HLI.

**A sensor is ignored** — Check its Home Assistant device class and Area. HLI intentionally ignores ambiguous entities rather than guessing.

**Occupancy looks wrong** — Open the room occupancy entity and inspect `explanation` and `confidence`.

**Need help** — Download HLI diagnostics from Devices & services and attach them to a GitHub issue. Diagnostics report capability counts, not your raw entity IDs.
