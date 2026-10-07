"""Explainable evidence-fusion engine for Human-Like Intelligence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import HouseModel, RoomModel

ACTIVE_MEDIA = frozenset({"playing", "on", "paused", "buffering"})
ON_STATES = frozenset({"on", "open", "detected", "occupied", "motion"})
BAD_STATES = frozenset({"unknown", "unavailable", "none", ""})


@dataclass(slots=True)
class RoomState:
    """Calculated intelligence state for one room."""

    occupancy: int
    intent: str
    low_light: bool | None
    confidence: int
    explanation: str


def _state(hass: Any, entity_id: str) -> Any:
    """Return a Home Assistant state object for an entity."""
    return hass.states.get(entity_id)


def _is_active(
    hass: Any,
    entity_ids: list[str],
    active_states: frozenset[str] | None = None,
) -> bool:
    """Return whether any supplied entity currently has an active state."""
    accepted_states = ON_STATES if active_states is None else active_states
    for entity_id in entity_ids:
        state = _state(hass, entity_id)
        if state is not None and str(state.state).lower() in accepted_states:
            return True
    return False


def _lux(hass: Any, entity_ids: list[str]) -> float | None:
    """Return the lowest valid illuminance reading from the supplied entities."""
    values: list[float] = []
    for entity_id in entity_ids:
        state = _state(hass, entity_id)
        if state is None or str(state.state).lower() in BAD_STATES:
            continue
        try:
            values.append(float(state.state))
        except (TypeError, ValueError):
            continue
    return min(values) if values else None


def evaluate_room(hass: Any, room: RoomModel) -> RoomState:
    """Evaluate explainable occupancy and intent for one room."""
    presence_entities = room.entities("presence")
    media_entities = room.entities("media")
    illuminance_entities = room.entities("illuminance")

    active_presence = _is_active(hass, presence_entities)
    active_media = _is_active(hass, media_entities, ACTIVE_MEDIA)
    illuminance = _lux(hass, illuminance_entities)

    score = 0
    if active_presence:
        score += 70
    if active_media:
        score += 20
    if illuminance is not None and illuminance < 120 and (active_presence or active_media):
        score += 5
    score = min(score, 100)

    low_light = None if illuminance is None else illuminance < 120
    if active_media and score >= 20:
        intent = "media_focus"
    elif score >= 60:
        intent = "occupied"
    elif score >= 20:
        intent = "passive_presence"
    else:
        intent = "vacant"

    available = sum(
        bool(room.entities(capability))
        for capability in ("presence", "illuminance", "media")
    )
    confidence = 0
    if available:
        confidence = min(100, 45 + (available * 15) + (15 if active_presence else 0))

    reasons: list[str] = []
    if active_presence:
        reasons.append("presence detected")
    if active_media:
        reasons.append("media active")
    if illuminance is not None:
        reasons.append(f"illuminance {illuminance:.0f} lx")
    if not reasons:
        reasons.append("no active evidence")

    return RoomState(score, intent, low_light, confidence, ", ".join(reasons))


def evaluate_house(hass: Any, model: HouseModel) -> dict[str, Any]:
    """Evaluate all rooms and determine primary/secondary room state."""
    rooms = {room.key: evaluate_room(hass, room) for room in model.rooms.values()}
    ordered = sorted(rooms.items(), key=lambda item: item[1].occupancy, reverse=True)

    primary = "none"
    secondary = "none"
    if ordered and ordered[0][1].occupancy > 0:
        primary = ordered[0][0]
    if len(ordered) > 1 and ordered[1][1].occupancy > 0:
        secondary = ordered[1][0]

    return {
        "rooms": rooms,
        "primary_room": primary,
        "secondary_room": secondary,
        "occupied": any(room.occupancy >= 20 for room in rooms.values()),
    }
