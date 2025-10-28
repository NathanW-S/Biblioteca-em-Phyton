from pathlib import Path
import json
from typing import Any, Dict


def load_json(path: Path, default: Any) -> Any:
    """Carrega JSON de `path`. Se o arquivo não existir, retorna `default`."""
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    """Salva `data` em `path` como JSON (pretty printed)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)