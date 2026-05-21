import os
import json
import psycopg2

from dotenv import load_dotenv

load_dotenv()


def main():

    connection = psycopg2.connect(
        os.getenv(
            "DATABASE_URL"
        )
    )

    cursor = connection.cursor()

    raw_path = "data/raw"

    for category_name in os.listdir(
        raw_path
    ):

        category_folder = (
            os.path.join(
                raw_path,
                category_name
            )
        )

        if not os.path.isdir(
            category_folder
        ):
            continue

        json_path = (
            os.path.join(
                category_folder,
                "products.json"
            )
        )

        if not os.path.exists(
            json_path
        ):
            continue

        print(
            f"Processing "
            f"{category_name}"
        )

        # get category_id
        cursor.execute(
            """
            SELECT id
            FROM categories
            WHERE name = %s
            """,
            (
                category_name,
            )
        )

        result = (
            cursor.fetchone()
        )

        if not result:
            print(
                f"Category not found: "
                f"{category_name}"
            )
            continue

        category_id = result[0]

        # load products
        with open(
            json_path,
            "r",
            encoding="utf-8"
        ) as f:

            products = json.load(f)

        for product in products:

            product_id = product.get(
                "product_id"
            )

            if not product_id:
                continue

            try:

                cursor.execute(
                    """
                    INSERT INTO
                    product_categories (
                        product_id,
                        category_id
                    )
                    VALUES (%s, %s)

                    ON CONFLICT DO NOTHING
                    """,
                    (
                        product_id,
                        category_id
                    )
                )

            except Exception as e:

                print(
                    f"Error for "
                    f"{product_id}: {e}"
                )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        "product_categories filled"
    )


if __name__ == "__main__":
    main()