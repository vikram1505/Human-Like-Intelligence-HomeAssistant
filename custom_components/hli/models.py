"""Data models used by Human-Like Intelligence."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Evidence:
    """Describe one Home Assistant entity used as HLI evidence."""

    entity_id: str
    capability: str
    confidence: float
    reason: str


@dataclass(slots=True)
class RoomModel:
    """Describe a discovered or conservatively inferred room."""

    key: str
    name: str
    area_id: str | None = None
    floor_id: str | None = None
    evidence: list[Evidence] = field(default_factory=list)

    def entities(self, capability: str) -> list[str]:
        """Return entity IDs that provide the requested capability."""
        return [item.entity_id for item in self.evidence if item.capability == capability]

    def confidence(self, capability: str) -> float:
        """Return the strongest discovery confidence for a capability."""
        values = [
            item.confidence for item in self.evidence if item.capability == capability
        ]
        return max(values, default=0.0)


@dataclass(slots=True)
class HouseModel:
    """Represent the read-only semantic model discovered by HLI."""

    rooms: dict[str, RoomModel] = field(default_factory=dict)
    unassigned: list[Evidence] = field(default_factory=list)
