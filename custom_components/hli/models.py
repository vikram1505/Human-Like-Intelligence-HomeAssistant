"""Small, serialisable HLI house model."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(slots=True)
class Evidence:
    entity_id: str
    capability: str
    confidence: float
    reason: str

@dataclass(slots=True)
class RoomModel:
    key: str
    name: str
    area_id: str | None = None
    floor_id: str | None = None
    evidence: list[Evidence] = field(default_factory=list)

    def entities(self, capability: str) -> list[str]:
        return [e.entity_id for e in self.evidence if e.capability == capability]

    def confidence(self, capability: str) -> float:
        values = [e.confidence for e in self.evidence if e.capability == capability]
        return max(values, default=0.0)

@dataclass(slots=True)
class HouseModel:
    rooms: dict[str, RoomModel] = field(default_factory=dict)
    unassigned: list[Evidence] = field(default_factory=list)
