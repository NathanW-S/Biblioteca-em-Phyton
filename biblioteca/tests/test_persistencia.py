from pathlib import Path
from persistencia import save_json, load_json

def test_save_and_load(tmp_path: Path):
    p = tmp_path / "x.json"
    data = {"a": 1}
    save_json(p, data)
    assert load_json(p, None) == data
    assert load_json(tmp_path / "missing.json", {"default": True}) == {"default": True}