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


import os
import json
import glob


def extract_products():

    products = []

    location = get_location_data()

    files = glob.glob(
        "data/raw/*/products.json"
    )

    print(
        "Files found:",
        len(files)
    )

    for file in files:

        try:
            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            # fallback category
            folder_category = os.path.basename(
                os.path.dirname(file)
            )

            # raw data already stored as list
            snippets = (
                data
                if isinstance(
                    data,
                    list
                )
                else (
                    data
                    .get(
                        "response",
                        {}
                    )
                    .get(
                        "snippets",
                        []
                    )
                )
            )

            for item in snippets:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                # --------------------
                # HANDLE BOTH FORMATS
                # --------------------

                # flattened product
                if item.get(
                    "product_id"
                ):

                    product = item

                # raw blinkit snippet
                else:

                    product = item.get(
                        "data",
                        {}
                    )

                product_id = product.get(
                    "product_id"
                )

                if not product_id:
                    continue

                # category fallback
                category = (
                    product.get(
                        "category"
                    )
                    or folder_category
                )

                extracted_product = {

                    "product_id":
                        product_id,

                    "merchant_id":
                        product.get(
                            "merchant_id"
                        ),

                    "category":
                        category,

                    "parent_category":
                        product.get(
                            "parent_category"
                        ),

                    "ptype":
                        product.get(
                            "ptype"
                        ),

                    "name":
                        (
                            product.get(
                                "name",
                                {}
                            ).get(
                                "text"
                            )
                            if isinstance(
                                product.get(
                                    "name"
                                ),
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
                            ).get(
                                "text"
                            )
                            if isinstance(
                                product.get(
                                    "brand_name"
                                ),
                                dict
                            )
                            else (
                                product.get(
                                    "brand_name"
                                )
                                or product.get(
                                    "brand"
                                )
                            )
                        ),

                    "price":
                        float(
                            str(
                                product.get(
                                    "price",
                                    product.get(
                                        "normal_price",
                                        ""
                                    )
                                )
                            )
                            .replace(
                                "₹",
                                ""
                            )
                            .strip()
                            or 0
                        ),

                    "inventory":
                        product.get(
                            "inventory",
                            0
                        ),

                    "rating":
                        (
                            float(
                                product.get(
                                    "rating",
                                    0
                                ) or 0
                            )
                            if not isinstance(
                                product.get(
                                    "rating"
                                ),
                                dict
                            )
                            else float(
                                product.get(
                                    "rating",
                                    {}
                                )
                                .get(
                                    "bar",
                                    {}
                                )
                                .get(
                                    "value",
                                    0
                                ) or 0
                            )
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
                        (
                            product.get(
                                "in_stock"
                            )
                            if (
                                "in_stock"
                                in product
                            )
                            else not product.get(
                                "is_sold_out",
                                False
                            )
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
                }

                products.append(
                    extracted_product
                )

        except Exception as e:

            print(
                f"Error reading "
                f"{file}: {e}"
            )

    # --------------------
    # REMOVE DUPLICATES
    # --------------------

    unique = {}

    for p in products:

        unique[
            p["product_id"]
        ] = p

    extracted = list(
        unique.values()
    )

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