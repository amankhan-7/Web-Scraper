import json
import glob
import os

from dotenv import load_dotenv

load_dotenv()


def get_location_data():

    return {

        "city":
            os.getenv(
                "CITY"
            ),

        "latitude":
            float(
                os.getenv(
                    "LATITUDE",
                    0
                )
            ),

        "longitude":
            float(
                os.getenv(
                    "LONGITUDE",
                    0
                )
            )
    }


def extract_products():

    products = []

    files = glob.glob(
        "data/raw/*.json"
    )

    print(
        "Files found:",
        files
    )

    for file in files:

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        snippets = (
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

        for item in snippets:

            product = item.get(
                "data",
                {}
            )

            # Skip non-product widgets
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

                "name":
                    product.get(
                        "name",
                        {}
                    ).get("text"),

                "brand":
                    product.get(
                        "brand_name",
                        {}
                    ).get("text"),

                "price":
                    product.get(
                        "normal_price",
                        {}
                    )
                    .get("text", "")
                    .replace("₹", ""),

                "inventory":
                    product.get(
                        "inventory",
                        0
                    ),

                "rating":
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
                    ),

                "image_url":
                    product.get(
                        "image",
                        {}
                    ).get(
                        "url"
                    ),

                "in_stock":
                    not product.get(
                        "is_sold_out",
                        False
                    ),

                "city":
                    os.getenv(
                        "CITY"
                    ),

                "latitude":
                    os.getenv(
                        "LATITUDE"
                    ),

                "longitude":
                    os.getenv(
                        "LONGITUDE"
                    )
            })

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
        "Saved extracted data"
    )

    return extracted

    products = []

    location = (
        get_location_data()
    )

    files = glob.glob(
        "data/raw/*.json"
    )

    print(
        "Files found:",
        files
    )

    for file in files:

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        snippets = (
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

        for item in snippets:

            product = item.get(
                "data",
                {}
            )

            # Skip non-product widgets
            if not product.get(
                "product_id"
            ):
                continue

            products.append({

                "product_id":
                    product.get(
                        "product_id"
                    ),

                "name":
                    product.get(
                        "name",
                        {}
                    ).get(
                        "text"
                    ),

                "brand":
                    product.get(
                        "brand_name",
                        {}
                    ).get(
                        "text"
                    ),

                "price":
                    product.get(
                        "normal_price",
                        {}
                    )
                    .get(
                        "text",
                        ""
                    )
                    .replace(
                        "₹",
                        ""
                    ),

                "inventory":
                    product.get(
                        "inventory",
                        0
                    ),

                "merchant_id":
                    product.get(
                        "merchant_id"
                    ),

                "rating":
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
                    ),

                "image_url":
                    product.get(
                        "image",
                        {}
                    ).get(
                        "url"
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

    # Remove duplicates
    unique = {}

    for p in products:

        unique[
            p[
                "product_id"
            ]
        ] = p

    return list(
        unique.values()
    )