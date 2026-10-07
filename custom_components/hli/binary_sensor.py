"""Binary sensors exposed by Human-Like Intelligence."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import HLIEntity


async def async_setup_entry(_hass, entry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up HLI binary sensors for a config entry."""
    async_add_entities([HLIHouseOccupied(entry.runtime_data, entry.entry_id)])


class HLIHouseOccupied(HLIEntity, BinarySensorEntity):
    """Represent HLI's inferred whole-house occupancy state."""

    _attr_name = "House occupied"
    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    def __init__(self, coordinator, entry_id: str) -> None:
        """Initialize the house occupied sensor."""
        super().__init__(coordinator, entry_id, "house_occupied")

    @property
    def is_on(self) -> bool:
        """Return whether HLI currently considers the house occupied."""
        return bool(self.coordinator.data.get("occupied"))
