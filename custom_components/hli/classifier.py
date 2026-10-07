"""Conservative capability classification for Home Assistant entities."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Classification:
    """A capability classification and the evidence supporting it."""

    capability: str
    confidence: float
    reason: str


DOMAIN_RULES = {
    "light": Classification("light", 1.0, "Home Assistant light domain"),
    "media_player": Classification("media", 1.0, "Home Assistant media_player domain"),
    "person": Classification("person", 1.0, "Home Assistant person domain"),
    "device_tracker": Classification(
        "tracker", 0.95, "Home Assistant device_tracker domain"
    ),
}

DEVICE_CLASS_RULES = {
    "occupancy": "presence",
    "motion": "presence",
    "presence": "presence",
    "door": "contact",
    "garage_door": "contact",
    "opening": "contact",
    "window": "contact",
    "battery": "battery",
    "illuminance": "illuminance",
    "power": "power",
    "temperature": "temperature",
    "humidity": "humidity",
}

HIGH_CONFIDENCE_CLASSES = frozenset(
    {"battery", "illuminance", "temperature", "humidity"}
)


def classify(
    entity_id: str,
    domain: str,
    device_class: str | None,
    original_name: str | None = None,
) -> Classification | None:
    """Classify an entity without guessing potentially dangerous actuators."""
    if domain in DOMAIN_RULES:
        return DOMAIN_RULES[domain]

    normalized_class = (device_class or "").lower()
    if normalized_class in DEVICE_CLASS_RULES:
        capability = DEVICE_CLASS_RULES[normalized_class]
        confidence = 0.99 if normalized_class in HIGH_CONFIDENCE_CLASSES else 0.98
        if normalized_class == "power":
            confidence = 0.95
        return Classification(
            capability,
            confidence,
            f"device_class={normalized_class}",
        )

    searchable_name = f"{entity_id} {original_name or ''}".lower()
    if domain == "binary_sensor" and any(
        word in searchable_name
        for word in ("motion", "occupancy", "presence", "pir", "mmwave")
    ):
        return Classification(
            "presence",
            0.72,
            "name suggests presence; confirmation recommended",
        )

    if domain == "sensor" and any(
        word in searchable_name for word in ("illuminance", "lux", "light_level")
    ):
        return Classification(
            "illuminance",
            0.70,
            "name suggests illuminance; confirmation recommended",
        )

    # Generic switches are intentionally not classified as lights. HLI v0.1.x is
    # read-only and must never infer actuator purpose from a friendly name alone.
    return None
