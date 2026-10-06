from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .entity import HLIEntity

async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
    c=entry.runtime_data
    entities=[HLIOverview(c,entry.entry_id), HLIPrimaryRoom(c,entry.entry_id), HLISecondaryRoom(c,entry.entry_id)]
    for room in c.model.rooms.values(): entities.extend([HLIRoomOccupancy(c,entry.entry_id,room.key,room.name), HLIRoomIntent(c,entry.entry_id,room.key,room.name)])
    async_add_entities(entities)

class HLIOverview(HLIEntity,SensorEntity):
    _attr_name="Overview"; _attr_icon="mdi:brain"
    def __init__(self,c,e): super().__init__(c,e,"overview")
    @property
    def native_value(self): return "occupied" if self.coordinator.data.get("occupied") else "quiet"
    @property
    def extra_state_attributes(self):
        rooms=self.coordinator.data.get("rooms",{})
        return {"primary_room":self.coordinator.data.get("primary_room"),"secondary_room":self.coordinator.data.get("secondary_room"),"rooms":{k:{"occupancy":v.occupancy,"intent":v.intent,"confidence":v.confidence,"explanation":v.explanation} for k,v in rooms.items()},"discovered_rooms":len(self.coordinator.model.rooms),"unassigned_entities":len(self.coordinator.model.unassigned)}
class HLIPrimaryRoom(HLIEntity,SensorEntity):
    _attr_name="Primary room"; _attr_icon="mdi:home-map-marker"
    def __init__(self,c,e): super().__init__(c,e,"primary_room")
    @property
    def native_value(self): return self.coordinator.data.get("primary_room","none")
class HLISecondaryRoom(HLIEntity,SensorEntity):
    _attr_name="Secondary room"; _attr_icon="mdi:home-map-marker"
    def __init__(self,c,e): super().__init__(c,e,"secondary_room")
    @property
    def native_value(self): return self.coordinator.data.get("secondary_room","none")
class HLIRoomOccupancy(HLIEntity,SensorEntity):
    _attr_native_unit_of_measurement=PERCENTAGE; _attr_icon="mdi:account-radar"
    def __init__(self,c,e,key,name): self.room_key=key; self._attr_name=f"{name} occupancy"; super().__init__(c,e,f"{key}_occupancy")
    @property
    def native_value(self): return self.coordinator.data["rooms"][self.room_key].occupancy
    @property
    def extra_state_attributes(self):
        r=self.coordinator.data["rooms"][self.room_key]; return {"confidence":r.confidence,"explanation":r.explanation,"intent":r.intent}
class HLIRoomIntent(HLIEntity,SensorEntity):
    _attr_icon="mdi:thought-bubble"
    def __init__(self,c,e,key,name): self.room_key=key; self._attr_name=f"{name} intent"; super().__init__(c,e,f"{key}_intent")
    @property
    def native_value(self): return self.coordinator.data["rooms"][self.room_key].intent
