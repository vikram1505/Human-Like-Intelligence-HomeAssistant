"""Constants for Human-Like Intelligence."""

DOMAIN = "hli"
NAME = "Human-Like Intelligence"
VERSION = "0.1.1"
PLATFORMS = ["sensor", "binary_sensor"]
CONF_MIN_CONFIDENCE = "min_confidence"
DEFAULT_MIN_CONFIDENCE = 0.80
UPDATE_SECONDS = 15
UNKNOWN_STATES = frozenset({"unknown", "unavailable", "none", ""})
