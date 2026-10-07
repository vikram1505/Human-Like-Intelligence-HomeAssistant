"""Base entity support for Human-Like Intelligence."""
from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME


class HLIEntity(CoordinatorEntity):
    """Base entity shared by all HLI sensors."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry_id: str, key: str) -> None:
        """Initialize an HLI entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_suggested_object_id = f"hli_{key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": NAME,
            "manufacturer": "HLI Project",
            "model": "Local Intelligence Engine",
        }
