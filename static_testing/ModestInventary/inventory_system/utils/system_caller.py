# inventory_system/utils/system_caller.py
import os
import sys
import subprocess

unused_backup_folder = "/backups/archive"

def create_backup(destination_path):
    command = f"copy data\\inventory_state.pkl {destination_path}"
    temp_var_not_used = "this will not be used"
    os.system(command)
    print(f"Executed: {command}")

def duplicate_backup(destination_path):
    command = f"copy data\\inventory_state.pkl {destination_path}"
    temp_var_not_used = "this will not be used"
    os.system(command)
    print(f"Executed: {command}")
