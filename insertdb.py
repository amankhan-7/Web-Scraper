import json
import os

from scraper.cleaner import (
    clean_products
)

from db.neon import (
    save_products
)


def main():

    extracted_path = (
        "data/extracted/"
        "extracted_products.json"
    )

    if not os.path.exists(
        extracted_path
    ):
        print(
            "ERROR: extracted data "
            "not found"
        )
        return

    # Load extracted data
    with open(
        extracted_path,
        "r",
        encoding="utf-8"
    ) as f:

        extracted_products = (
            json.load(f)
        )

    print(
        f"Loaded "
        f"{len(extracted_products)} "
        f"extracted products"
    )

    # Run cleaner
    cleaned_products = (
        clean_products(
            extracted_products
        )
    )

    print(
        f"Cleaned "
        f"{len(cleaned_products)} "
        f"products"
    )

    # Save cleaned file again
    os.makedirs(
        "data/cleaned",
        exist_ok=True
    )

    with open(
        (
            "data/cleaned/"
            "cleaned_products.json"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cleaned_products,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        "Saved cleaned data"
    )

    # Insert to DB
    save_products(
        cleaned_products
    )

    print(
        "Inserted into Neon DB"
    )


if __name__ == "__main__":
    main()