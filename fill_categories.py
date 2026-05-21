import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def main():

    connection = psycopg2.connect(
        os.getenv(
            "DATABASE_URL"
        )
    )

    cursor = (
        connection.cursor()
    )

    raw_path = "data/raw"

    categories = []

    for folder in os.listdir(
        raw_path
    ):

        folder_path = (
            os.path.join(
                raw_path,
                folder
            )
        )

        if os.path.isdir(
            folder_path
        ):
            categories.append(
                folder
            )

    print(
        f"Found "
        f"{len(categories)} "
        f"categories"
    )

    query = """
    INSERT INTO categories (
        name
    )
    VALUES (%s)

    ON CONFLICT (name)
    DO NOTHING
    """

    for category in categories:

        cursor.execute(
            query,
            (
                category,
            )
        )

        print(
            f"Inserted: "
            f"{category}"
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        "Categories saved "
        "to Neon DB"
    )


if __name__ == "__main__":
    main()