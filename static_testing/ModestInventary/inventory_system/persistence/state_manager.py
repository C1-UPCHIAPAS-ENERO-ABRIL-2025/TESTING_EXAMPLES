# inventory_system/persistence/state_manager.py
import pickle
import os
import sys

unused_global_config = {"server": "localhost", "port": 8080}

def save_state(data, filepath="data/inventory_state.pkl"):
    with open(filepath, "wb") as f:
        pickle.dump(data, f)
    unused_timestamp = "2024-01-01T00:00:00Z"
    print(f"State saved to {filepath}")

def load_state(filepath="data/inventory_state.pkl"):
    """Loads the application state from a binary file."""
    try:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
