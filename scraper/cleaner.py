import json
import os
import ast


def safe_float(value):

    if value is None:
        return None

    try:
        # normal number/string case
        return float(value)

    except (
        ValueError,
        TypeError
    ):

        try:
            # handle stringified dict
            if isinstance(
                value,
                str
            ) and value.startswith("{"):

                parsed = (
                    ast.literal_eval(
                        value
                    )
                )

                if isinstance(
                    parsed,
                    dict
                ):
                    text = parsed.get(
                        "text"
                    )

                    if text:
                        return float(
                            text
                        )

        except Exception:
            pass

    return None


def safe_int(value):
    """
    Convert value to int safely
    """

    if value is None:
        return 0

    # if dict like {"text": "12"}
    if isinstance(value, dict):
        value = value.get("text")

    try:
        return int(float(value))
    except:
        return 0


def clean_products(raw_products):

    cleaned = []

    for product in raw_products:

        cleaned_product = {

            "product_id":
                safe_int(
                    product.get(
                        "product_id"
                    )
                ),

            "merchant_id":
                safe_int(
                    product.get(
                        "merchant_id"
                    )
                ),

            "name":
                str(
                    product.get(
                        "name",
                        ""
                    )
                ).strip(),

            "brand":
                str(
                    product.get(
                        "brand",
                        ""
                    )
                ).strip(),

            "price":
                safe_float(
                    product.get(
                        "price"
                    )
                ),

            "inventory":
                safe_int(
                    product.get(
                        "inventory"
                    )
                ),

            "rating":
                safe_float(
                    product.get(
                        "rating"
                    )
                ),

            "image_url":
                product.get(
                    "image_url"
                ),

            "in_stock":
                bool(
                    product.get(
                        "in_stock",
                        True
                    )
                ),

            "city":
                product.get(
                    "city"
                ),

            "latitude":
                safe_float(
                    product.get(
                        "latitude"
                    )
                ),

            "longitude":
                safe_float(
                    product.get(
                        "longitude"
                    )
                )
        }

        # Skip invalid products
        if not cleaned_product["product_id"]:
            continue

        cleaned.append(
            cleaned_product
        )

    # Save cleaned data
    os.makedirs(
        "data/cleaned",
        exist_ok=True
    )

    with open(
        "data/cleaned/cleaned_products.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cleaned,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Saved cleaned data "
        f"({len(cleaned)} products)"
    )

    return cleaned