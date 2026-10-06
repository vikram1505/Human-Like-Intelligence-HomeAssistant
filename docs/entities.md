# Entities

| Entity | Meaning |
|---|---|
| `sensor.hli_overview` | House summary plus room data in attributes |
| `sensor.hli_primary_room` | Highest-scoring active room |
| `sensor.hli_secondary_room` | Second active room, when present |
| `binary_sensor.hli_house_occupied` | At least one room has meaningful occupancy evidence |
| `sensor.hli_<room>_occupancy` | Explainable occupancy score (0–100%) |
| `sensor.hli_<room>_intent` | Current room intent |

Room occupancy attributes include `confidence`, `intent`, and `explanation`.
