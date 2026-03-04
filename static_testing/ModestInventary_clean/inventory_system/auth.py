import hmac
import os


def is_admin(username: str, password: str) -> bool:
    """Validate credentials using environment variables.

    Required environment variables:
    - INVENTORY_ADMIN_USER
    - INVENTORY_ADMIN_PASSWORD
    """
    expected_user = os.getenv("INVENTORY_ADMIN_USER")
    expected_password = os.getenv("INVENTORY_ADMIN_PASSWORD")

    if not expected_user or not expected_password:
        return False

    return hmac.compare_digest(username, expected_user) and hmac.compare_digest(
        password, expected_password
    )
