"""Safe state persistence using JSON serialization.

This module handles application state persistence using JSON format,
which is safe from arbitrary code execution unlike pickle.
"""

import json
from pathlib import Path
from typing import Any, Optional

DEFAULT_STATE_FILE: Path = Path(__file__).resolve().parents[2] / "data" / "inventory_state.json"


def _resolve_path(filepath: str | Path | None = None) -> Path:
    """Resolve and create directories for state file path.

    Args:
        filepath: Optional custom path for state file

    Returns:
        Resolved absolute Path object with parent directories created
    """
    path = Path(filepath) if filepath else DEFAULT_STATE_FILE
    resolved_path = path.expanduser().resolve()
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    return resolved_path


def save_state(data: dict[str, Any], filepath: str | Path | None = None) -> Optional[Path]:
    """Save application state to a JSON file.

    Args:
        data: Dictionary containing application state
        filepath: Optional custom path where state will be saved

    Returns:
        Path to saved file if successful, None if error occurred
    """
    try:
        target_path = _resolve_path(filepath)
        with target_path.open("w", encoding="utf-8") as file_obj:
            json.dump(data, file_obj, ensure_ascii=False, indent=2, default=str)
        return target_path
    except (IOError, ValueError, TypeError) as error:
        print(f"Error saving state: {error}")
        return None


def load_state(filepath: str | Path | None = None) -> dict[str, Any] | None:
    """Load state from a JSON file.

    Args:
        filepath: Optional custom path to state file

    Returns:
        Dictionary containing state if file exists and is valid, None otherwise
    """
    try:
        target_path = _resolve_path(filepath)
        if not target_path.exists():
            return None

        with target_path.open("r", encoding="utf-8") as file_obj:
            return json.load(file_obj)
    except (IOError, json.JSONDecodeError) as error:
        print(f"Error loading state: {error}")
        return None
