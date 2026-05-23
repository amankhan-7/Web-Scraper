import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
load_dotenv()
import os


def insert_products():

    with open(
        "data/cleaned/cleaned_products.json",
        "r",
        encoding="utf-8"
    ) as f:

        products = json.load(f)
        
    
    connection = psycopg2.connect(
        os.getenv(
            "DATABASE_URL"
        )
    )

    cur = connection.cursor()

    # category slug -> id
    cur.execute(
        """
        SELECT
            id,
            slug
        FROM categories
        """
    )

    category_map = {
        slug: cat_id
        for cat_id, slug
        in cur.fetchall()
    }

    rows = []

    for product in products:

        category_slug = (
            product.get(
                "category",
                ""
            )
            .strip()
            .lower()
        )

        category_id = (
            category_map.get(
                category_slug
            )
        )

        rows.append((

            product.get(
                "product_id"
            ),

            product.get(
                "merchant_id"
            ),

            category_id,

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
                "in_stock",
                True
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
        ))

    execute_values(
        cur,
        """
        INSERT INTO
        blinkit_products (

            product_id,
            merchant_id,
            category_id,

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

        VALUES %s

        ON CONFLICT
        (product_id)

        DO UPDATE SET

            merchant_id =
            EXCLUDED.merchant_id,

            category_id =
            EXCLUDED.category_id,

            name =
            EXCLUDED.name,

            brand =
            EXCLUDED.brand,

            price =
            EXCLUDED.price,

            inventory =
            EXCLUDED.inventory,

            rating =
            EXCLUDED.rating,

            image_url =
            EXCLUDED.image_url,

            in_stock =
            EXCLUDED.in_stock,

            city =
            EXCLUDED.city,

            latitude =
            EXCLUDED.latitude,

            longitude =
            EXCLUDED.longitude,

            updated_at =
            NOW()
        """,
        rows
    )

    connection.commit()

    print(
        f"Inserted "
        f"{len(rows)} products"
    )

    connection.close()
    connection.close()


insert_products()