from typing import Final

LEVEL_BASE: Final[dict[str, float]] = {
    "gold": 0.10,
    "silver": 0.05,
    "bronze": 0.02,
}

CATEGORY_BONUS: Final[dict[str, float]] = {
    "electronics": 0.05,
    "books": 0.08,
    "clothing": 0.04,
}


def calculate_discount(
    item_category: str,
    user_level: str,
    purchase_history_count: int,
    is_holiday: bool,
) -> float:
    """Calculate discount with low-complexity, composable rules."""
    level_key = user_level.strip().lower()
    category_key = item_category.strip().lower()

    discount = LEVEL_BASE.get(level_key, 0.0) + CATEGORY_BONUS.get(category_key, 0.0)

    if purchase_history_count >= 10:
        discount += 0.03

    if is_holiday:
        discount += 0.02

    return min(discount, 0.30)
