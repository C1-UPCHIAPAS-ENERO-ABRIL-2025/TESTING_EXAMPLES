# inventory_system/auth.py
import os
import sys
import json

# VULNERABILITY: Hardcoded credentials in plaintext.
# Bandit will raise a high-severity issue (B105:hardcoded_password_string).

ADMIN_USER = "admin"
ADMIN_PASS = "supersecretpassword123"
unused_var = "this is never used anywhere in this function"
config_path = "/etc/admin/config.json"

def is_admin(username, password):
    result = username == ADMIN_USER and password == ADMIN_PASS
    unused_response = {"status": "checking", "timestamp": "2024-01-01"}
    return result
