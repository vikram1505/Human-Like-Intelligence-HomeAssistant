from __future__ import annotations
from homeassistant.components.diagnostics import async_redact_data
TO_REDACT={"entity_id","device_id","area_id","identifiers","connections","name","unique_id"}
async def async_get_config_entry_diagnostics(hass,entry):
    c=entry.runtime_data
    data={"version":1,"room_count":len(c.model.rooms),"unassigned_count":len(c.model.unassigned),"rooms":[{"key":r.key,"capabilities":sorted({e.capability for e in r.evidence}),"evidence_count":len(r.evidence)} for r in c.model.rooms.values()],"state":{"occupied":c.data.get("occupied"),"room_count":len(c.data.get("rooms",{}))}}
    return async_redact_data(data,TO_REDACT)
