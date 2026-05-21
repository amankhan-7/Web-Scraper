# db/neon.py

import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()


def save_products(products):

    print("Connecting to Neon DB...")

    database_url = os.getenv(
        "DATABASE_URL"
    )

    if not database_url:
        print(
            "ERROR: DATABASE_URL "
            "not found in .env"
        )
        return

    try:
        connection = psycopg2.connect(
            database_url
        )

        print(
            "Connected to Neon DB"
        )

        cursor = (
            connection.cursor()
        )

        query = """
        INSERT INTO blinkit_products (
            product_id,
            merchant_id,
            name,
            brand,
            price,
            inventory,
            rating,
            image_url,
            in_stock,
            city,
            latitude,
            longitude
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s
        )

        ON CONFLICT (product_id)

        DO UPDATE SET
            merchant_id = EXCLUDED.merchant_id,
            name = EXCLUDED.name,
            brand = EXCLUDED.brand,
            price = EXCLUDED.price,
            inventory = EXCLUDED.inventory,
            rating = EXCLUDED.rating,
            image_url = EXCLUDED.image_url,
            in_stock = EXCLUDED.in_stock,
            city = EXCLUDED.city,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            updated_at = NOW();
        """

        inserted = 0

        for product in products:

            try:
                cursor.execute(
                    query,
                    (
                        product.get(
                            "product_id"
                        ),
                        product.get(
                            "merchant_id"
                        ),
                        product.get(
                            "name"
                        ),
                        product.get(
                            "brand"
                        ),
                        product.get(
                            "price"
                        ),
                        product.get(
                            "inventory"
                        ),
                        product.get(
                            "rating"
                        ),
                        product.get(
                            "image_url"
                        ),
                        product.get(
                            "in_stock"
                        ),
                        product.get(
                            "city"
                        ),
                        product.get(
                            "latitude"
                        ),
                        product.get(
                            "longitude"
                        )
                    )
                )

                inserted += 1

            except Exception as e:
                print(
                    f"Insert failed "
                    f"for "
                    f"{product.get('name')}"
                )
                print(e)

        connection.commit()

        cursor.close()
        connection.close()

        print(
            f"Saved "
            f"{inserted} "
            f"products to Neon DB"
        )

    except Exception as e:
        print(
            "DATABASE ERROR:"
        )
        print(e)