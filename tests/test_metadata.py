"""Repository metadata tests."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]


def test_json_and_yaml_parse() -> None:
    """All JSON and YAML repository files should parse."""
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    for path in ROOT.rglob("*.yaml"):
        yaml.safe_load(path.read_text(encoding="utf-8"))


def test_manifest() -> None:
    """The integration manifest should expose required HLI metadata."""
    manifest = json.loads(
        (ROOT / "custom_components/hli/manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["domain"] == "hli"
    assert manifest["config_flow"] is True
    assert manifest["version"]
