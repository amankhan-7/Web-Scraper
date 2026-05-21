import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def main():

    connection = psycopg2.connect(
        os.getenv("DATABASE_URL")
    )

    cursor = connection.cursor()

    raw_path = "data/raw"

    categories = []

    for folder in os.listdir(raw_path):

        folder_path = os.path.join(
            raw_path,
            folder
        )

        if os.path.isdir(folder_path):

            categories.append(folder)

    print(
        f"Found {len(categories)} categories"
    )

    query = """
    INSERT INTO product_categories (name)
    VALUES (%s)
    ON CONFLICT (name)
    DO NOTHING
    """

    for category in categories:

        cursor.execute(
            query,
            (category,)
        )

        print(f"Inserted: {category}")

    connection.commit()

    cursor.close()
    connection.close()

    print("Categories saved to DB")


if __name__ == "__main__":
    main()