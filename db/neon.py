# db/neon.py

import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()


def save_products(products):

    connection = psycopg2.connect(
        os.getenv("DATABASE_URL")
    )

    cursor = connection.cursor()

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

    for product in products:

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

    connection.commit()

    cursor.close()

    connection.close()

    print(
        "Saved to Neon DB"
    )