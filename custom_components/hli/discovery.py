"""Build a read-only semantic model from Home Assistant registries."""
from __future__ import annotations
import re
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar, device_registry as dr, entity_registry as er
from .classifier import classify
from .models import Evidence, HouseModel, RoomModel

_CAPABILITY_WORDS = re.compile(r"\b(motion|occupancy|presence|sensor|illuminance|lux|temperature|humidity|battery|power|media|player|light|door|window)\b", re.I)

_slug_re=re.compile(r"[^a-z0-9]+")
def _key(value: str) -> str:
    return _slug_re.sub("_", value.lower()).strip("_") or "room"

def _effective_area(entity, device) -> str | None:
    # Entity assignment has priority. Device assignment is the safe fallback.
    return entity.area_id or (device.area_id if device else None)

async def async_discover(hass: HomeAssistant, min_confidence: float) -> HouseModel:
    areas=ar.async_get(hass); devices=dr.async_get(hass); entities=er.async_get(hass)
    model=HouseModel()
    for area in areas.async_list_areas():
        model.rooms[area.id]=RoomModel(key=_key(area.name), name=area.name, area_id=area.id, floor_id=getattr(area, "floor_id", None))
    for ent in entities.entities.values():
        state=hass.states.get(ent.entity_id)
        domain=ent.entity_id.split('.',1)[0]
        device=devices.async_get(ent.device_id) if ent.device_id else None
        dc=(getattr(ent, "device_class", None) or (state.attributes.get("device_class") if state else None))
        c=classify(ent.entity_id, domain, dc, getattr(ent, "original_name", None))
        if not c: continue
        ev=Evidence(ent.entity_id, c.capability, c.confidence, c.reason)
        area_id=_effective_area(ent, device)
        if area_id and area_id in model.rooms and c.confidence >= min_confidence:
            model.rooms[area_id].evidence.append(ev)
        else:
            # Keep uncertain/unassigned evidence out of established rooms. A second
            # pass may form a conservative inferred room from repeated naming.
            model.unassigned.append(ev)

    # Conservative room inference for installations that have not configured Areas.
    # We never write Areas back to Home Assistant. At least two distinct capabilities
    # must agree on the same cleaned name before HLI creates an inferred room.
    candidates: dict[str, list[Evidence]] = {}
    for ent in entities.entities.values():
        candidate_device = devices.async_get(ent.device_id) if ent.device_id else None
        if _effective_area(ent, candidate_device):
            continue
        state = hass.states.get(ent.entity_id)
        domain = ent.entity_id.split('.', 1)[0]
        dc = getattr(ent, "device_class", None) or (state.attributes.get("device_class") if state else None)
        c = classify(ent.entity_id, domain, dc, getattr(ent, "original_name", None))
        if not c or c.confidence < min_confidence:
            continue
        raw = getattr(ent, "original_name", None) or ent.entity_id.split('.', 1)[1].replace('_', ' ')
        cleaned = _CAPABILITY_WORDS.sub(' ', raw)
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" -_")
        if len(cleaned) < 3:
            continue
        candidates.setdefault(cleaned.lower(), []).append(Evidence(ent.entity_id, c.capability, c.confidence, c.reason + "; inferred-room candidate"))
    for label, evidence in candidates.items():
        if len({e.capability for e in evidence}) < 2:
            continue
        room_key = _key(label)
        if any(r.key == room_key for r in model.rooms.values()):
            continue
        inferred_id = f"inferred:{room_key}"
        model.rooms[inferred_id] = RoomModel(key=room_key, name=label.title(), evidence=evidence)
        inferred_entities = {e.entity_id for e in evidence}
        model.unassigned = [e for e in model.unassigned if e.entity_id not in inferred_entities]
    return model
