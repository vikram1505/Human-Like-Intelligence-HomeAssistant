"""Replace repository URL placeholders with the public GitHub repository."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).parents[1]
PLACEHOLDER = "vikram1505/Human-Like-Intelligence-HomeAssistant"
REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def main() -> None:
    """Update public repository links in files that contain the placeholder."""
    if len(sys.argv) != 2 or not REPOSITORY_PATTERN.fullmatch(sys.argv[1]):
        raise SystemExit(
            "Usage: python scripts/set_repository.py GITHUB_USER/REPOSITORY"
        )

    repository = sys.argv[1]
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix == ".pyc":
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        if PLACEHOLDER not in content:
            continue
        path.write_text(
            content.replace(PLACEHOLDER, repository),
            encoding="utf-8",
        )
        changed += 1

    print(f"Updated {changed} file(s) for https://github.com/{repository}")


if __name__ == "__main__":
    main()
