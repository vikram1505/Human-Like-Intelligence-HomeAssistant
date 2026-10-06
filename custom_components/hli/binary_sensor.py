from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .entity import HLIEntity
async def async_setup_entry(hass,entry,async_add_entities:AddEntitiesCallback): async_add_entities([HLIHouseOccupied(entry.runtime_data,entry.entry_id)])
class HLIHouseOccupied(HLIEntity,BinarySensorEntity):
    _attr_name="House occupied"; _attr_device_class=BinarySensorDeviceClass.OCCUPANCY
    def __init__(self,c,e): super().__init__(c,e,"house_occupied")
    @property
    def is_on(self): return bool(self.coordinator.data.get("occupied"))
