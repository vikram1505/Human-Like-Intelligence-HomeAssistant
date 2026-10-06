import json, pathlib, yaml
r=pathlib.Path(__file__).parents[1]
def test_json_and_yaml_parse():
 for p in r.rglob("*.json"): json.loads(p.read_text())
 for p in r.rglob("*.yaml"): yaml.safe_load(p.read_text())
def test_manifest():
 m=json.loads((r/"custom_components/hli/manifest.json").read_text()); assert m["domain"]=="hli" and m["config_flow"] is True and m["version"]
