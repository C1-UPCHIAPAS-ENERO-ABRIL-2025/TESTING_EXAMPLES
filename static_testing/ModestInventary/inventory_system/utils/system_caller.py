# inventory_system/utils/system_caller.py

import os

# VULNERABILITY: Command injection via unsanitized input to os.system.
# Bandit will raise a high-severity issue (B605:start_process_with_a_shell).

def create_backup(destination_path):
    """
    Creates a 'backup' by copying the state file using a system command.
    This is highly vulnerable to command injection.
    """
    command = f"copy data\\inventory_state.pkl {destination_path}" # For Windows
    # command = f"cp data/inventory_state.pkl {destination_path}" # For Linux/macOS
    os.system(command)
    print(f"Executed: {command}")