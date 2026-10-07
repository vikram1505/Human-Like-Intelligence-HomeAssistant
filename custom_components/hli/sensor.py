"""Sensors exposed by Human-Like Intelligence."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import HLIEntity


async def async_setup_entry(_hass, entry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up HLI sensors for a config entry."""
    coordinator = entry.runtime_data
    entities = [
        HLIOverview(coordinator, entry.entry_id),
        HLIPrimaryRoom(coordinator, entry.entry_id),
        HLISecondaryRoom(coordinator, entry.entry_id),
    ]
    for room in coordinator.model.rooms.values():
        entities.extend(
            [
                HLIRoomOccupancy(
                    coordinator, entry.entry_id, room.key, room.name
                ),
                HLIRoomIntent(coordinator, entry.entry_id, room.key, room.name),
            ]
        )
    async_add_entities(entities)


class HLIOverview(HLIEntity, SensorEntity):
    """Provide a compact whole-house HLI overview."""

    _attr_name = "Overview"
    _attr_icon = "mdi:brain"

    def __init__(self, coordinator, entry_id: str) -> None:
        """Initialize the HLI overview sensor."""
        super().__init__(coordinator, entry_id, "overview")

    @property
    def native_value(self) -> str:
        """Return the inferred whole-house activity state."""
        return "occupied" if self.coordinator.data.get("occupied") else "quiet"

    @property
    def extra_state_attributes(self) -> dict:
        """Return room intelligence used by the portable dashboard."""
        rooms = self.coordinator.data.get("rooms", {})
        return {
            "primary_room": self.coordinator.data.get("primary_room"),
            "secondary_room": self.coordinator.data.get("secondary_room"),
            "rooms": {
                key: {
                    "occupancy": value.occupancy,
                    "intent": value.intent,
                    "confidence": value.confidence,
                    "explanation": value.explanation,
                }
                for key, value in rooms.items()
            },
            "discovered_rooms": len(self.coordinator.model.rooms),
            "unassigned_entities": len(self.coordinator.model.unassigned),
        }


class HLIPrimaryRoom(HLIEntity, SensorEntity):
    """Expose the room with the strongest current occupancy evidence."""

    _attr_name = "Primary room"
    _attr_icon = "mdi:home-map-marker"

    def __init__(self, coordinator, entry_id: str) -> None:
        """Initialize the primary-room sensor."""
        super().__init__(coordinator, entry_id, "primary_room")

    @property
    def native_value(self) -> str:
        """Return the current primary room key."""
        return self.coordinator.data.get("primary_room", "none")


class HLISecondaryRoom(HLIEntity, SensorEntity):
    """Expose the room with the second-strongest occupancy evidence."""

    _attr_name = "Secondary room"
    _attr_icon = "mdi:home-map-marker"

    def __init__(self, coordinator, entry_id: str) -> None:
        """Initialize the secondary-room sensor."""
        super().__init__(coordinator, entry_id, "secondary_room")

    @property
    def native_value(self) -> str:
        """Return the current secondary room key."""
        return self.coordinator.data.get("secondary_room", "none")


class HLIRoomOccupancy(HLIEntity, SensorEntity):
    """Expose explainable occupancy confidence for one room."""

    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:account-radar"

    def __init__(self, coordinator, entry_id: str, key: str, name: str) -> None:
        """Initialize a room occupancy sensor."""
        self.room_key = key
        self._attr_name = f"{name} occupancy"
        super().__init__(coordinator, entry_id, f"{key}_occupancy")

    @property
    def native_value(self) -> int:
        """Return the current occupancy score."""
        return self.coordinator.data["rooms"][self.room_key].occupancy

    @property
    def extra_state_attributes(self) -> dict:
        """Return confidence, intent, and human-readable evidence."""
        room = self.coordinator.data["rooms"][self.room_key]
        return {
            "confidence": room.confidence,
            "explanation": room.explanation,
            "intent": room.intent,
        }


class HLIRoomIntent(HLIEntity, SensorEntity):
    """Expose the current inferred intent for one room."""

    _attr_icon = "mdi:thought-bubble"

    def __init__(self, coordinator, entry_id: str, key: str, name: str) -> None:
        """Initialize a room intent sensor."""
        self.room_key = key
        self._attr_name = f"{name} intent"
        super().__init__(coordinator, entry_id, f"{key}_intent")

    @property
    def native_value(self) -> str:
        """Return the current inferred room intent."""
        return self.coordinator.data["rooms"][self.room_key].intent
