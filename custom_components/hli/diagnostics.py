"""Privacy-preserving diagnostics for Human-Like Intelligence."""
from __future__ import annotations

from collections import Counter


def _capability_counts(room) -> dict[str, int]:
    """Return anonymous capability counts for a room."""
    return dict(Counter(item.capability for item in room.evidence))


async def async_get_config_entry_diagnostics(_hass, entry) -> dict:
    """Return diagnostics without entity IDs, room names, IDs, or network data."""
    coordinator = entry.runtime_data
    room_summaries = [
        {
            "capabilities": _capability_counts(room),
            "evidence_count": len(room.evidence),
            "is_inferred": room.area_id is None,
        }
        for room in coordinator.model.rooms.values()
    ]
    return {
        "schema_version": 2,
        "room_count": len(coordinator.model.rooms),
        "unassigned_count": len(coordinator.model.unassigned),
        "rooms": room_summaries,
        "state": {
            "occupied": bool(coordinator.data.get("occupied")),
            "evaluated_room_count": len(coordinator.data.get("rooms", {})),
        },
    }
