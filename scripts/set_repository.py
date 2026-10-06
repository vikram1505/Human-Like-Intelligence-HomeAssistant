from pathlib import Path
import sys
if len(sys.argv)!=2 or "/" not in sys.argv[1]: raise SystemExit("Usage: python scripts/set_repository.py GITHUB_USER/REPO")
repo=sys.argv[1]; root=Path(__file__).parents[1]
for rel in ["custom_components/hli/manifest.json","README.md"]:
 p=root/rel; s=p.read_text().replace("OWNER/home-assistant-hli",repo); p.write_text(s)
print(f"Repository links set to https://github.com/{repo}")
