"""Discount calculation with composable, type-safe rules.

This module implements discount rules using a functional approach with
composable functions, avoiding deep nesting and improving maintainability.
"""

from typing import Final

# User level base discounts (0.0 to 1.0)
LEVEL_BASE_DISCOUNT: Final[dict[str, float]] = {
    "platinum": 0.30,
    "gold": 0.20,
    "silver": 0.10,
    "bronze": 0.05,
}

# Category-specific bonuses
CATEGORY_BONUS: Final[dict[str, float]] = {
    "electronics": 0.05,
    "books": 0.08,
    "clothing": 0.04,
    "furniture": 0.03,
}

# Purchase history thresholds for additional discounts
PURCHASE_THRESHOLDS: Final[dict[int, float]] = {
    20: 0.05,  # Very frequent customer
    15: 0.04,
    10: 0.03,
    5: 0.02,
}

# Seasonal multipliers (applied as additional discount)
SEASON_BONUS: Final[dict[str, float]] = {
    "black_friday": 0.15,
    "clearance": 0.25,
    "summer": 0.05,
    "winter": 0.03,
}

# Regional adjustments
REGION_BONUS: Final[dict[str, float]] = {
    "US": 0.00,
    "EU": 0.02,
    "ASIA": 0.01,
}

# Constants
MAX_DISCOUNT_CAP: Final[float] = 0.50
MIN_DISCOUNT_FLOOR: Final[float] = 0.00


def _calculate_purchase_history_bonus(purchase_count: int) -> float:
    """Calculate bonus based on purchase history.

    Args:
        purchase_count: Total number of purchases

    Returns:
        Discount bonus (0.0 to 0.05)
    """
    for threshold, bonus in sorted(
        PURCHASE_THRESHOLDS.items(), reverse=True
    ):
        if purchase_count >= threshold:
            return bonus
    return 0.0


def _get_level_discount(user_level: str) -> float:
    """Get base discount for user level.

    Args:
        user_level: User tier (platinum, gold, silver, bronze, or other)

    Returns:
        Base discount for this level
    """
    normalized_level = user_level.strip().lower()
    return LEVEL_BASE_DISCOUNT.get(normalized_level, 0.0)


def _get_category_bonus(item_category: str) -> float:
    """Get category-specific bonus.

    Args:
        item_category: Product category

    Returns:
        Category bonus discount
    """
    normalized_category = item_category.strip().lower()
    return CATEGORY_BONUS.get(normalized_category, 0.0)


def _get_seasonal_bonus(season: str) -> float:
    """Get seasonal adjustment.

    Args:
        season: Season name

    Returns:
        Seasonal bonus discount
    """
    normalized_season = season.strip().lower()
    default = 0.02 if normalized_season else 0.0
    return SEASON_BONUS.get(normalized_season, default)


def _get_regional_bonus(region: str) -> float:
    """Get regional adjustment.

    Args:
        region: Geographic region code

    Returns:
        Regional bonus discount
    """
    normalized_region = region.strip().upper()
    return REGION_BONUS.get(normalized_region, 0.0)


def _apply_holiday_bonus(
    current_discount: float, is_holiday: bool
) -> float:
    """Apply holiday bonus if applicable.

    Args:
        current_discount: Current discount value
        is_holiday: Whether today is a holiday

    Returns:
        Updated discount with holiday bonus applied
    """
    if is_holiday:
        return current_discount + 0.05
    return current_discount


def _clamp_discount(discount: float) -> float:
    """Ensure discount is within valid bounds.

    Args:
        discount: Raw discount value

    Returns:
        Discount clamped between MIN_DISCOUNT_FLOOR and MAX_DISCOUNT_CAP
    """
    return max(MIN_DISCOUNT_FLOOR, min(discount, MAX_DISCOUNT_CAP))


def calculate_discount(
    item_category: str,
    user_level: str,
    purchase_history_count: int,
    is_holiday: bool,
    season: str = "normal",
    region: str = "US",
) -> float:
    """Calculate final discount using composable rule functions.

    This function combines multiple discount sources using a sum-and-clamp
    approach, avoiding deep nesting by delegating to specialized functions.

    Args:
        item_category: Product category (electronics, books, clothing)
        user_level: Customer tier (platinum, gold, silver, bronze)
        purchase_history_count: Number of past purchases
        is_holiday: Whether this is a holiday
        season: Seasonal context (normal, black_friday, clearance)
        region: Geographic region (US, EU, ASIA)

    Returns:
        Final discount percentage (0.0 to 0.50)
    """
    # Build discount by combining all components
    discount = (
        _get_level_discount(user_level)
        + _get_category_bonus(item_category)
        + _calculate_purchase_history_bonus(purchase_history_count)
        + _get_seasonal_bonus(season)
        + _get_regional_bonus(region)
    )

    # Apply conditional bonuses
    discount = _apply_holiday_bonus(discount, is_holiday)

    # Ensure within valid bounds
    return _clamp_discount(discount)
