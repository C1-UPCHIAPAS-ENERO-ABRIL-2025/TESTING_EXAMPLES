# inventory_system/logic/discount_calculator.py

# VULNERABILITY: High cyclomatic complexity and deeply nested code.
# Radon will report a very high complexity score.
# Pylint will complain about too many branches and statements.

def calculate_discount(item_category, user_level, purchase_history_count, is_holiday):
    """
    Calculates a discount based on a convoluted set of rules.
    This function is intentionally complex and hard to maintain.
    """
    discount = 0
    if user_level == "gold":
        if item_category == "electronics":
            if purchase_history_count > 10:
                discount = 0.20
                if is_holiday:
                    discount += 0.05
            else:
                discount = 0.15
        elif item_category == "books":
            discount = 0.25
    elif user_level == "silver":
        if item_category == "electronics":
            if purchase_history_count > 5:
                discount = 0.10
            else:
                discount = 0.05
        elif item_category == "clothing":
            discount = 0.15
    return discount