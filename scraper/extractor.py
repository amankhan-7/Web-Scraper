import json
import glob
import os

from scraper.visibility import get_visibility


def extract_text(value):
    if isinstance(value, dict):
        return value.get("text")
    return value


def extract_price(product):
    """
    RAW extraction ONLY (no conversion)
    """
    if product.get("price") is not None:
        return product.get("price")

    if isinstance(product.get("normal_price"), dict):
        return product["normal_price"].get("text")

    if isinstance(product.get("mrp"), dict):
        return product["mrp"].get("text")

    return None


def extract_products():

    products = []

    try:
        location = get_visibility()
        print("\nLOCATION RECEIVED:", location)

    except Exception as e:
        print(f"Visibility failed: {e}")
        location = {
            "city": None,
            "state": None,
            "city_id": None,
            "latitude": float(os.getenv("LATITUDE", 0)),
            "longitude": float(os.getenv("LONGITUDE", 0)),
        }

    files = glob.glob("data/raw/*/products.json")
    print("Files found:", len(files))

    for file in files:

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            folder_category = os.path.basename(os.path.dirname(file))

            snippets = (
                data
                if isinstance(data, list)
                else data.get("response", {}).get("snippets", [])
            )

            for item in snippets:

                if not isinstance(item, dict):
                    continue

                product = item.get("data") if item.get("data") else item

                if not isinstance(product, dict):
                    continue

                product_id = product.get("product_id")
                if not product_id:
                    continue

                extracted_product = {
                    "product_id": product_id,
                    "merchant_id": product.get("merchant_id"),

                    "category": product.get("category") or folder_category,
                    "parent_category": product.get("parent_category"),
                    "ptype": product.get("ptype"),

                    # raw text OR dict preserved
                    "name": product.get("name"),
                    "brand": product.get("brand_name") or product.get("brand"),

                    # 🔥 FIXED: correct raw price extraction
                    "price": extract_price(product),
                    "normal_price": product.get("normal_price"),
                    "mrp": product.get("mrp"),

                    "inventory": product.get("inventory"),
                    "rating": product.get("rating"),

                    "image_url": (
                        product.get("image", {}).get("url")
                        if isinstance(product.get("image"), dict)
                        else product.get("image_url")
                    ),

                    "in_stock": product.get("in_stock"),
                    "is_sold_out": product.get("is_sold_out"),

                    # location (raw)
                    "city": location.get("city"),
                    "state": location.get("state"),
                    "city_id": location.get("city_id"),
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude"),
                }

                products.append(extracted_product)

        except Exception as e:
            print(f"Error reading {file}: {e}")

    # dedupe
    unique = {}
    for p in products:
        unique[p["product_id"]] = p

    extracted = list(unique.values())

    os.makedirs("data/extracted", exist_ok=True)

    with open("data/extracted/extracted_products.json", "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2, ensure_ascii=False)

    print(f"Saved extracted data ({len(extracted)} products)")

    return extracted