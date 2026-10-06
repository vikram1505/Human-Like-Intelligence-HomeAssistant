from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
class HLIEntity(CoordinatorEntity):
    _attr_has_entity_name=True
    def __init__(self, coordinator, entry_id: str, key: str):
        super().__init__(coordinator); self._attr_unique_id=f"{entry_id}_{key}"
        self._attr_device_info={"identifiers":{(DOMAIN,entry_id)},"name":"Human-Like Intelligence","manufacturer":"HLI Project","model":"Local Intelligence Engine"}
