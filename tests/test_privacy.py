from pathlib import Path
import re
ROOT=Path(__file__).parents[1]

def test_no_private_network_addresses_or_credentials():
    paths=[p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and p.suffix not in {'.pyc'}]
    text='\n'.join(p.read_text(errors='ignore') for p in paths)
    assert not re.search(r'(?<![\w.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![\w.])', text)
