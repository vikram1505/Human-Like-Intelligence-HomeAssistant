"""Tests for conservative HLI entity classification."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

PATH = Path(__file__).parents[1] / "custom_components/hli/classifier.py"
SPEC = importlib.util.spec_from_file_location("hli_classifier_standalone", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_metadata_first() -> None:
    """Device metadata should produce strong classifications."""
    presence = MODULE.classify("binary_sensor.x", "binary_sensor", "occupancy")
    illuminance = MODULE.classify("sensor.x", "sensor", "illuminance")
    assert presence.capability == "presence"
    assert illuminance.confidence == 0.99


def test_generic_switch_is_not_assumed_to_be_a_light() -> None:
    """Names alone must never turn generic switches into light actuators."""
    assert MODULE.classify("switch.bedroom_light", "switch", None) is None


def test_name_fallback_is_uncertain() -> None:
    """Name-only presence classification must remain below auto-use threshold."""
    result = MODULE.classify("binary_sensor.room_motion", "binary_sensor", None)
    assert result.confidence < 0.8
