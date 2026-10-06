"""Capability classifier. Metadata wins; names are only supporting evidence."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Classification:
    capability: str
    confidence: float
    reason: str

PRESENCE_CLASSES = {"occupancy", "motion", "presence"}
CONTACT_CLASSES = {"door", "garage_door", "opening", "window"}
BATTERY_CLASSES = {"battery"}
ILLUMINANCE_CLASSES = {"illuminance"}
POWER_CLASSES = {"power"}
TEMP_CLASSES = {"temperature"}
HUMIDITY_CLASSES = {"humidity"}

def classify(entity_id: str, domain: str, device_class: str | None, original_name: str | None = None) -> Classification | None:
    dc=(device_class or "").lower()
    name=f"{entity_id} {original_name or ''}".lower()
    if domain == "light": return Classification("light", 1.0, "Home Assistant light domain")
    if domain == "media_player": return Classification("media", 1.0, "Home Assistant media_player domain")
    if domain == "person": return Classification("person", 1.0, "Home Assistant person domain")
    if domain == "device_tracker": return Classification("tracker", 0.95, "Home Assistant device_tracker domain")
    if dc in PRESENCE_CLASSES: return Classification("presence", 0.98, f"device_class={dc}")
    if dc in CONTACT_CLASSES: return Classification("contact", 0.98, f"device_class={dc}")
    if dc in BATTERY_CLASSES: return Classification("battery", 0.99, "device_class=battery")
    if dc in ILLUMINANCE_CLASSES: return Classification("illuminance", 0.99, "device_class=illuminance")
    if dc in POWER_CLASSES: return Classification("power", 0.95, "device_class=power")
    if dc in TEMP_CLASSES: return Classification("temperature", 0.99, "device_class=temperature")
    if dc in HUMIDITY_CLASSES: return Classification("humidity", 0.99, "device_class=humidity")
    if domain == "binary_sensor" and any(w in name for w in ("motion", "occupancy", "presence", "pir", "mmwave")):
        return Classification("presence", 0.72, "name suggests presence; confirmation recommended")
    if domain == "sensor" and any(w in name for w in ("illuminance", "lux", "light_level")):
        return Classification("illuminance", 0.70, "name suggests illuminance; confirmation recommended")
    # Generic switches are intentionally NOT classified as lights. Public HLI must not guess actuators.
    return None
