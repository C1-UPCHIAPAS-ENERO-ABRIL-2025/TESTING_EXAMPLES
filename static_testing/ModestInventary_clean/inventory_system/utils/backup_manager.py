import shutil
from pathlib import Path

from inventory_system.persistence.state_manager import DEFAULT_STATE_FILE


def create_backup(destination_path: str) -> Path:
    """Copy the state file to a safe destination without shell execution."""
    source = DEFAULT_STATE_FILE.expanduser().resolve()
    destination = Path(destination_path).expanduser().resolve()

    if destination.exists() and destination.is_dir():
        target = destination / source.name
    else:
        target = destination

    target.parent.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        raise FileNotFoundError(f"Source state file does not exist: {source}")

    shutil.copy2(source, target)
    return target
