# inventory_system/auth.py

# VULNERABILITY: Hardcoded credentials in plaintext.
# Bandit will raise a high-severity issue (B105:hardcoded_password_string).

ADMIN_USER = "admin"
ADMIN_PASS = "supersecretpassword123"  # Hardcoded password

def is_admin(username, password):
    """
    A terribly insecure function to check for admin credentials.
    """
    return username == ADMIN_USER and password == ADMIN_PASS