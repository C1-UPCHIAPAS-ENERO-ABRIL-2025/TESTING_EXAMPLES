"""Secure authentication using environment variables and constant-time comparison.

This module handles admin authentication using environment variables for credentials
and HMAC constant-time comparison to prevent timing attacks.
"""

import hmac
import os
from typing import Final

# Default admin user (can be overridden via environment variable)
DEFAULT_ADMIN_USER: Final[str] = "admin"


def validate_credentials(username: str, password: str) -> bool:
    """Validate admin credentials using environment variables.
    
    Credentials are loaded from environment variables and compared using
    constant-time comparison to prevent timing attacks.
    
    Required environment variables:
    - INVENTORY_ADMIN_USER: Admin username
    - INVENTORY_ADMIN_PASSWORD: Admin password
    
    If environment variables are not set, admin authentication is disabled
    for security reasons (fail-safe behavior).
    
    Args:
        username: Provided username
        password: Provided password
        
    Returns:
        True if credentials are valid, False otherwise
    """
    expected_user = os.getenv("INVENTORY_ADMIN_USER")
    expected_password = os.getenv("INVENTORY_ADMIN_PASSWORD")

    # Fail-safe: if credentials are not configured, deny access
    if not expected_user or not expected_password:
        return False

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(username, expected_user) and hmac.compare_digest(
        password, expected_password
    )


def is_admin(username: str, password: str) -> bool:
    """Check if provided credentials belong to an admin user.
    
    This is a compatibility wrapper around validate_credentials.
    
    Args:
        username: Provided username
        password: Provided password
        
    Returns:
        True if credentials are valid, False otherwise
    """
    return validate_credentials(username, password)
