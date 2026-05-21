import json
import glob
import os

from dotenv import load_dotenv

load_dotenv()


def get_location_data():
    return {
        "city": os.getenv("CITY"),

        "latitude": float(
            os.getenv("LATITUDE", 0)
        ),

        "longitude": float(
            os.getenv("LONGITUDE", 0)
        )
    }


def extract_products():

    products = []

    location = get_location_data()

    # Search inside all category folders
    files = glob.glob(
        "data/raw/*/products.json"
    )

    print("Files found:", files)

    for file in files:

        try:
            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:
                data = json.load(f)

            # Your scraper saves a list directly
            # not response.snippets
            if isinstance(data, list):
                snippets = data
            else:
                snippets = (
                    data
                    .get("response", {})
                    .get("snippets", [])
                )

            for item in snippets:

                # Handle both formats
                product = (
                    item.get("data", {})
                    if isinstance(item, dict)
                    else item
                )

                if not product.get(
                    "product_id"
                ):
                    continue

                products.append({

                    "product_id":
                        product.get(
                            "product_id"
                        ),

                    "merchant_id":
                        product.get(
                            "merchant_id"
                        ),

                    "category":
                        product.get(
                          "category"
                        ),
                        
                    "parent_category":
                       product.get(
                         "parent_category"
                        ),
       

                    "name":
                        (
                            product.get(
                                "name",
                                {}
                            ).get("text")
                            if isinstance(
                                product.get("name"),
                                dict
                            )
                            else product.get(
                                "name"
                            )
                        ),

                    "brand":
                        (
                            product.get(
                                "brand_name",
                                {}
                            ).get("text")
                            if isinstance(
                                product.get(
                                    "brand_name"
                                ),
                                dict
                            )
                            else product.get(
                                "brand_name"
                            )
                        ),

                    "price":
                        str(
                            product.get(
                                "normal_price",
                                ""
                            )
                        )
                        .replace("₹", "")
                        .strip(),

                    "inventory":
                        product.get(
                            "inventory",
                            0
                        ),

                    "rating":
                        (
                            product.get(
                                "rating",
                                {}
                            )
                            .get(
                                "bar",
                                {}
                            )
                            .get(
                                "value"
                            )
                            if isinstance(
                                product.get(
                                    "rating"
                                ),
                                dict
                            )
                            else None
                        ),

                    "image_url":
                        (
                            product.get(
                                "image",
                                {}
                            ).get(
                                "url"
                            )
                            if isinstance(
                                product.get(
                                    "image"
                                ),
                                dict
                            )
                            else product.get(
                                "image_url"
                            )
                        ),

                    "in_stock":
                        not product.get(
                            "is_sold_out",
                            False
                        ),

                    "city":
                        location[
                            "city"
                        ],

                    "latitude":
                        location[
                            "latitude"
                        ],

                    "longitude":
                        location[
                            "longitude"
                        ]
                })

        except Exception as e:
            print(
                f"Error reading {file}: {e}"
            )

    # Remove duplicates
    unique = {}

    for p in products:
        unique[
            p["product_id"]
        ] = p

    extracted = list(
        unique.values()
    )

    # Save extracted data
    os.makedirs(
        "data/extracted",
        exist_ok=True
    )

    with open(
        "data/extracted/extracted_products.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            extracted,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Saved extracted data "
        f"({len(extracted)} products)"
    )

    return extracted