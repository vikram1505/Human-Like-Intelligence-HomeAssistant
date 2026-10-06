"""Explainable HLI evidence-fusion engine."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .models import HouseModel, RoomModel

ACTIVE_MEDIA={"playing", "on", "paused", "buffering"}
ON_STATES={"on", "open", "detected", "occupied", "motion"}
BAD={"unknown", "unavailable", "none", ""}

@dataclass(slots=True)
class RoomState:
    occupancy: int
    intent: str
    low_light: bool | None
    confidence: int
    explanation: str

def _state(hass: Any, entity_id: str): return hass.states.get(entity_id)
def _is_active(hass: Any, entity_ids: list[str], active: set[str]=ON_STATES) -> bool:
    return any((s:=_state(hass,e)) is not None and str(s.state).lower() in active for e in entity_ids)
def _lux(hass: Any, ids: list[str]) -> float | None:
    vals=[]
    for e in ids:
        s=_state(hass,e)
        if s and str(s.state).lower() not in BAD:
            try: vals.append(float(s.state))
            except (TypeError,ValueError): pass
    return min(vals) if vals else None

def evaluate_room(hass: Any, room: RoomModel) -> RoomState:
    presence=room.entities("presence"); media=room.entities("media"); lux_ids=room.entities("illuminance")
    active_presence=_is_active(hass,presence); active_media=_is_active(hass,media,ACTIVE_MEDIA); lux=_lux(hass,lux_ids)
    score=0
    if active_presence: score += 70
    if active_media: score += 20
    if lux is not None and lux < 120 and (active_presence or active_media): score += 5
    score=min(score,100)
    low_light=None if lux is None else lux < 120
    if active_media and score >= 20: intent="media_focus"
    elif score >= 60: intent="occupied"
    elif score >= 20: intent="passive_presence"
    else: intent="vacant"
    available=sum(bool(room.entities(c)) for c in ("presence","illuminance","media"))
    confidence=min(100, 45 + available*15 + (15 if active_presence else 0)) if available else 0
    reasons=[]
    if active_presence: reasons.append("presence detected")
    if active_media: reasons.append("media active")
    if lux is not None: reasons.append(f"illuminance {lux:.0f} lx")
    if not reasons: reasons.append("no active evidence")
    return RoomState(score,intent,low_light,confidence,", ".join(reasons))

def evaluate_house(hass: Any, model: HouseModel) -> dict[str, Any]:
    rooms={r.key:evaluate_room(hass,r) for r in model.rooms.values()}
    ordered=sorted(rooms.items(), key=lambda x:x[1].occupancy, reverse=True)
    primary=ordered[0][0] if ordered and ordered[0][1].occupancy>0 else "none"
    secondary=ordered[1][0] if len(ordered)>1 and ordered[1][1].occupancy>0 else "none"
    occupied=any(v.occupancy>=20 for v in rooms.values())
    return {"rooms":rooms,"primary_room":primary,"secondary_room":secondary,"occupied":occupied}
