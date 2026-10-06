from pathlib import Path
import ast,json,yaml,re
ROOT=Path(__file__).parents[1]
for p in ROOT.rglob('*.py'):
    if '.git' not in p.parts: ast.parse(p.read_text(),filename=str(p))
for p in ROOT.rglob('*.json'): json.loads(p.read_text())
for p in ROOT.rglob('*.yaml'): yaml.safe_load(p.read_text())
paths=[p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and p.suffix != '.pyc']
text='\n'.join(p.read_text(errors='ignore') for p in paths)
private_ip=re.search(r'(?<![\w.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![\w.])',text)
if private_ip: raise SystemExit('Private IPv4 address found in repository')
manifest=json.loads((ROOT/'custom_components/hli/manifest.json').read_text())
required={'domain','name','version','config_flow','documentation','issue_tracker','integration_type','iot_class'}
missing=required-set(manifest)
if missing: raise SystemExit(f'Manifest keys missing: {sorted(missing)}')
print('HLI repository validation: PASS')
