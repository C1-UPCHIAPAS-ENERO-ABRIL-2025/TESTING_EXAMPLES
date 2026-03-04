# inventory_system/persistence/state_manager.py

import pickle

# VULNERABILITY: Insecure deserialization using pickle.
# Bandit will raise a high-severity issue (B301:pickle).
# A malicious pickle file could lead to arbitrary code execution.

def save_state(data, filepath="data/inventory_state.pkl"):
    """Saves the application state to a binary file."""
    with open(filepath, "wb") as f:
        pickle.dump(data, f)
    print(f"State saved to {filepath}")

def load_state(filepath="data/inventory_state.pkl"):
    """Loads the application state from a binary file."""
    try:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None