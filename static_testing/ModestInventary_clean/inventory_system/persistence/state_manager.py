import json
from pathlib import Path
from typing import Any

DEFAULT_STATE_FILE = Path(__file__).resolve().parents[2] / "data" / "inventory_state.json"


def _resolve_path(filepath: str | Path | None = None) -> Path:
    path = Path(filepath) if filepath else DEFAULT_STATE_FILE
    resolved_path = path.expanduser().resolve()
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    return resolved_path


def save_state(data: dict[str, Any], filepath: str | Path | None = None) -> Path:
    """Save application state as JSON."""
    target_path = _resolve_path(filepath)
    with target_path.open("w", encoding="utf-8") as file_obj:
        json.dump(data, file_obj, ensure_ascii=False, indent=2)
    return target_path


def load_state(filepath: str | Path | None = None) -> dict[str, Any] | None:
    """Load application state from JSON file."""
    target_path = _resolve_path(filepath)
    if not target_path.exists():
        return None

    with target_path.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)
