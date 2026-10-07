"""Static safety tests for the HLI intelligence engine."""
from __future__ import annotations

import ast
from pathlib import Path

PATH = Path(__file__).parents[1] / "custom_components/hli/engine.py"


def test_engine_has_no_service_calls() -> None:
    """The public HLI engine must remain read-only."""
    tree = ast.parse(PATH.read_text(encoding="utf-8"))
    attributes = [node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)]
    assert "async_call" not in attributes
