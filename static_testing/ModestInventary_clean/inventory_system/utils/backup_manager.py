"""Safe file backup using shutil instead of shell commands.

This module provides safe file backup operations without executing shell commands,
which prevents command injection vulnerabilities.
"""

import shutil
from pathlib import Path
from typing import Optional

from inventory_system.persistence.state_manager import DEFAULT_STATE_FILE


def create_backup(destination_path: str) -> Optional[Path]:
    """Create a backup by safely copying the state file.

    Uses shutil for cross-platform, injection-safe file operations.
    Never executes shell commands that could be vulnerable to injection.

    Args:
        destination_path: Path where backup will be created

    Returns:
        Path to created backup file if successful, None otherwise
    """
    try:
        source = DEFAULT_STATE_FILE.expanduser().resolve()
        destination = Path(destination_path).expanduser().resolve()

        if destination.exists() and destination.is_dir():
            target = destination / source.name
        else:
            target = destination

        target.parent.mkdir(parents=True, exist_ok=True)

        if not source.exists():
            msg = f"Source state file does not exist: {source}"
            raise FileNotFoundError(msg)

        shutil.copy2(source, target)
        return target
    except (FileNotFoundError, IOError, shutil.Error) as error:
        print(f"Error creating backup: {error}")
        return None


def verify_backup(
    backup_path: str, original_path: str | None = None
) -> bool:
    """Verify backup integrity by comparing file contents.

    Args:
        backup_path: Path to backup file
        original_path: Path to original file (None to use DEFAULT_STATE_FILE)

    Returns:
        True if backup matches original, False otherwise
    """
    try:
        backup = Path(backup_path).expanduser().resolve()
        original = (
            Path(original_path).expanduser().resolve()
            if original_path
            else DEFAULT_STATE_FILE
        )

        if not backup.exists() or not original.exists():
            return False

        # Compare files byte-by-byte
        with open(original, "rb") as orig_f:
            original_content = orig_f.read()

        with open(backup, "rb") as backup_f:
            backup_content = backup_f.read()

        return original_content == backup_content
    except (IOError, OSError) as error:
        print(f"Error verifying backup: {error}")
        return False
