"""Validate repository syntax, metadata, and public-safety invariants."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).parents[1]
PRIVATE_IPV4 = re.compile(
    r"(?<![\w.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![\w.])"
)
SECRET_PATTERNS = (
    re.compile(r"(?i)(?:password|passwd|api[_-]?key|access[_-]?token)\s*[:=]\s*['\"]?[^\s'\"]+"),
    re.compile(r"(?i)bearer\s+[a-z0-9._-]{16,}"),
)


def _text_files() -> list[Path]:
    """Return repository files safe to inspect as text."""
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.suffix != ".pyc"
    ]


def validate_python() -> None:
    """Parse every Python file."""
    for path in ROOT.rglob("*.py"):
        if ".git" not in path.parts:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def validate_metadata() -> None:
    """Parse JSON/YAML and verify required integration manifest keys."""
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    for path in ROOT.rglob("*.yaml"):
        yaml.safe_load(path.read_text(encoding="utf-8"))

    manifest = json.loads(
        (ROOT / "custom_components/hli/manifest.json").read_text(encoding="utf-8")
    )
    required = {
        "domain",
        "name",
        "version",
        "config_flow",
        "documentation",
        "issue_tracker",
        "integration_type",
        "iot_class",
    }
    missing = required - set(manifest)
    if missing:
        raise SystemExit(f"Manifest keys missing: {sorted(missing)}")


def validate_privacy() -> None:
    """Reject common private-network addresses and obvious embedded secrets."""
    repository_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore") for path in _text_files()
    )
    if PRIVATE_IPV4.search(repository_text):
        raise SystemExit("Private IPv4 address found in repository")
    for pattern in SECRET_PATTERNS:
        if pattern.search(repository_text):
            raise SystemExit("Possible credential or token found in repository")


def main() -> None:
    """Run all repository validations."""
    validate_python()
    validate_metadata()
    validate_privacy()
    print("HLI repository validation: PASS")


if __name__ == "__main__":
    main()
