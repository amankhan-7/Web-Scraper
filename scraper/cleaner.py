import json
import os
import ast
import re


# -------------------------
# SAFE FLOAT
# -------------------------
def safe_float(value):
    if value is None:
        return None

    try:
        return float(value)
    except (ValueError, TypeError):
        pass

    try:
        if isinstance(value, dict):
            value = value.get("text") or value.get("value")

        if isinstance(value, str):
            value = re.sub(r"[^\d.]", "", value)
            return float(value) if value else None

    except Exception:
        pass

    return None


# -------------------------
# SAFE INT
# -------------------------
def safe_int(value):
    if value is None:
        return None

    try:
        if isinstance(value, dict):
            value = value.get("text")

        return int(float(value))
    except:
        return None


# -------------------------
# EXTRACT TEXT FROM NESTED OBJECT
# -------------------------
def extract_text(value):
    if isinstance(value, dict):
        return value.get("text")
    return value


# -------------------------
# EXTRACT RATING
# -------------------------
def extract_rating(value):
    if isinstance(value, dict):
        try:
            return float(
                value.get("bar", {}).get("value")
            )
        except:
            return None

    return safe_float(value)


# -------------------------
# EXTRACT PRICE (₹ handling)
# -------------------------
def extract_price(value):
    if value is None:
        return None

    if isinstance(value, dict):
        value = value.get("text") or value.get("value")

    if isinstance(value, str):
        value = re.sub(r"[^\d.]", "", value)
        return float(value) if value else None

    try:
        return float(value)
    except:
        return None


# -------------------------
# CLEAN PRODUCTS
# -------------------------
def clean_products(raw_products):

    cleaned = []

    for product in raw_products:

        cleaned_product = {
            # IDs
            "product_id": safe_int(product.get("product_id")),
            "merchant_id": safe_int(product.get("merchant_id")),

            # CATEGORY
            "category": product.get("category"),
            "parent_category": product.get("parent_category"),
            "ptype": product.get("ptype"),

            # TEXT FIELDS
            "name": extract_text(product.get("name")),
            "brand": extract_text(product.get("brand") or product.get("brand_name")),

            # PRICES
            "price": extract_price(product.get("price")),
            "normal_price": extract_price(product.get("normal_price")),
            "mrp": extract_price(product.get("mrp")),

            # STOCK
            "inventory": safe_int(product.get("inventory")),

            # RATING
            "rating": extract_rating(product.get("rating")),

            # IMAGE
            "image_url": (
                product.get("image_url")
                or (product.get("image", {}).get("url")
                    if isinstance(product.get("image"), dict)
                    else None)
            ),

            # BOOLEAN FIX
            "in_stock": (
                product.get("in_stock")
                if product.get("in_stock") is not None
                else not product.get("is_sold_out", False)
            ),

            # LOCATION
            "city": product.get("city"),
            "state": product.get("state"),
            "latitude": safe_float(product.get("latitude")),
            "longitude": safe_float(product.get("longitude")),
        }

        # VALIDATION
        if not cleaned_product["product_id"]:
            continue

        cleaned.append(cleaned_product)

    # SAVE
    os.makedirs("data/cleaned", exist_ok=True)

    with open("data/cleaned/cleaned_products.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Saved cleaned data ({len(cleaned)} products)")

    return cleaned