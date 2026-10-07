"""Build a read-only semantic model from Home Assistant registries."""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from .classifier import Classification, classify
from .models import Evidence, HouseModel, RoomModel

_CAPABILITY_WORDS = re.compile(
    r"\b(motion|occupancy|presence|sensor|illuminance|lux|temperature|humidity|"
    r"battery|power|media|player|light|door|window)\b",
    re.IGNORECASE,
)
_SLUG_RE = re.compile(r"[^a-z0-9]+")


@dataclass(slots=True)
class DiscoveredEntity:
    """Internal normalized representation of one classified HA entity."""

    registry_entry: Any
    classification: Classification
    area_id: str | None
    evidence: Evidence


def _key(value: str) -> str:
    """Create a stable lowercase key from a room label."""
    return _SLUG_RE.sub("_", value.lower()).strip("_") or "room"


def _effective_area(entity: Any, device: Any) -> str | None:
    """Return the effective area, preferring explicit entity assignment."""
    return entity.area_id or (device.area_id if device else None)


def _device_class(hass: HomeAssistant, entity: Any) -> str | None:
    """Return registry or current-state device class for an entity."""
    registry_class = getattr(entity, "device_class", None)
    if registry_class:
        return str(registry_class)
    state = hass.states.get(entity.entity_id)
    if state is None:
        return None
    return state.attributes.get("device_class")


def _collect_entities(
    hass: HomeAssistant,
    devices: Any,
    entities: Any,
) -> list[DiscoveredEntity]:
    """Classify registry entities into normalized HLI evidence records."""
    discovered: list[DiscoveredEntity] = []
    for entity in entities.entities.values():
        domain = entity.entity_id.split(".", 1)[0]
        device = devices.async_get(entity.device_id) if entity.device_id else None
        classification = classify(
            entity.entity_id,
            domain,
            _device_class(hass, entity),
            getattr(entity, "original_name", None),
        )
        if classification is None:
            continue
        evidence = Evidence(
            entity.entity_id,
            classification.capability,
            classification.confidence,
            classification.reason,
        )
        discovered.append(
            DiscoveredEntity(
                entity,
                classification,
                _effective_area(entity, device),
                evidence,
            )
        )
    return discovered


def _candidate_room_name(entity: Any) -> str | None:
    """Return a conservative room-name candidate from an unassigned entity."""
    raw_name = getattr(entity, "original_name", None)
    if not raw_name:
        raw_name = entity.entity_id.split(".", 1)[1].replace("_", " ")
    cleaned = _CAPABILITY_WORDS.sub(" ", raw_name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -_")
    return cleaned if len(cleaned) >= 3 else None


def _infer_rooms(
    model: HouseModel,
    discovered: list[DiscoveredEntity],
    min_confidence: float,
) -> None:
    """Infer rooms only when multiple independent capabilities agree on a name."""
    candidates: dict[str, list[Evidence]] = {}
    for item in discovered:
        if item.area_id or item.classification.confidence < min_confidence:
            continue
        label = _candidate_room_name(item.registry_entry)
        if label is None:
            continue
        candidates.setdefault(label.lower(), []).append(item.evidence)

    for label, evidence in candidates.items():
        if len({item.capability for item in evidence}) < 2:
            continue
        room_key = _key(label)
        if any(room.key == room_key for room in model.rooms.values()):
            continue
        inferred_id = f"inferred:{room_key}"
        model.rooms[inferred_id] = RoomModel(
            key=room_key,
            name=label.title(),
            evidence=evidence,
        )
        inferred_entities = {item.entity_id for item in evidence}
        model.unassigned = [
            item for item in model.unassigned if item.entity_id not in inferred_entities
        ]


async def async_discover(hass: HomeAssistant, min_confidence: float) -> HouseModel:
    """Discover areas and capabilities without modifying Home Assistant."""
    areas = ar.async_get(hass)
    devices = dr.async_get(hass)
    entities = er.async_get(hass)
    model = HouseModel()

    for area in areas.async_list_areas():
        model.rooms[area.id] = RoomModel(
            key=_key(area.name),
            name=area.name,
            area_id=area.id,
            floor_id=getattr(area, "floor_id", None),
        )

    discovered = _collect_entities(hass, devices, entities)
    for item in discovered:
        if (
            item.area_id
            and item.area_id in model.rooms
            and item.classification.confidence >= min_confidence
        ):
            model.rooms[item.area_id].evidence.append(item.evidence)
        else:
            model.unassigned.append(item.evidence)

    _infer_rooms(model, discovered, min_confidence)
    return model
