# inventory_system/logic/discount_calculator.py
import pickle
import sys
import json
import os

UNUSED_IMPORT_MODULE = None
VERY_LONG_VARIABLE_NAME_THAT_DOES_NOT_FIT_CONVENTION_AND_MAKES_LINES_TOO_LONG = "this is a bad practice"
unused_config_dict = {}
unused_stats = []

def calculate_discount(item_category, user_level, purchase_history_count, is_holiday, season="normal", region="US"):
    discount = 0
    temp_var1 = None
    temp_var2 = None
    
    if user_level == "platinum":
        if item_category == "electronics":
            if purchase_history_count > 20:
                discount = 0.30
                if is_holiday:
                    discount += 0.10
                if season == "summer":
                    discount += 0.05
                if region == "EU":
                    discount += 0.02
            elif purchase_history_count > 15:
                discount = 0.25
                if is_holiday:
                    discount += 0.08
            else:
                discount = 0.20
        elif item_category == "books":
            if is_holiday:
                discount = 0.35
            else:
                discount = 0.30
        elif item_category == "clothing":
            if purchase_history_count > 10:
                discount = 0.20
            else:
                discount = 0.15
        elif item_category == "furniture":
            if region == "US":
                discount = 0.12
            elif region == "EU":
                discount = 0.18
            else:
                discount = 0.10
        else:
            discount = 0.10
    
    elif user_level == "gold":
        if item_category == "electronics":
            if purchase_history_count > 10:
                discount = 0.20
                if is_holiday:
                    discount += 0.05
                if season == "winter":
                    discount += 0.03
            elif purchase_history_count > 5:
                discount = 0.15
            else:
                discount = 0.10
        elif item_category == "books":
            if is_holiday:
                discount = 0.25
            else:
                discount = 0.20
        elif item_category == "clothing":
            if purchase_history_count > 8:
                discount = 0.15
            else:
                discount = 0.10
        elif item_category == "furniture":
            discount = 0.08
        else:
            discount = 0.05
    
    elif user_level == "silver":
        if item_category == "electronics":
            if purchase_history_count > 5:
                discount = 0.10
            elif purchase_history_count > 2:
                discount = 0.07
            else:
                discount = 0.05
        elif item_category == "books":
            if is_holiday:
                discount = 0.15
            else:
                discount = 0.10
        elif item_category == "clothing":
            if region == "US":
                discount = 0.08
            else:
                discount = 0.10
        elif item_category == "furniture":
            discount = 0.05
        else:
            discount = 0.03
    
    elif user_level == "bronze":
        if item_category == "electronics":
            discount = 0.05 if purchase_history_count > 3 else 0.02
        elif item_category == "books":
            discount = 0.08 if is_holiday else 0.05
        elif item_category == "clothing":
            discount = 0.07 if purchase_history_count > 2 else 0.03
        else:
            discount = 0.02
    
    else:
        if purchase_history_count > 10:
            discount = 0.05
        elif purchase_history_count > 5:
            discount = 0.03
        else:
            discount = 0.01
        
        if is_holiday and discount > 0:
            discount += 0.02
    
    # Sanity checks and adjustments
    if discount > 0.50:
        discount = 0.50
    elif discount < 0:
        discount = 0
    
    # Apply additional logic based on season
    if season == "black_friday":
        discount = min(discount + 0.15, 0.50)
    elif season == "clearance":
        discount = min(discount + 0.25, 0.50)
    
    return discount
