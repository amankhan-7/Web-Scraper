import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def format_name(slug: str) -> str:
    """
    full-cream-milk
    ->
    Full Cream Milk
    """
    return (
        slug
        .replace("-", " ")
        .title()
    )


def main():

    connection = psycopg2.connect(
        os.getenv(
            "DATABASE_URL"
        )
    )

    cursor = connection.cursor()

    raw_path = "data/raw"

    categories = []

    for folder in os.listdir(
        raw_path
    ):

        folder_path = os.path.join(
            raw_path,
            folder
        )

        if not os.path.isdir(
            folder_path
        ):
            continue

        slug = (
            folder
            .strip()
            .lower()
        )

        name = format_name(
            slug
        )

        url = (
            "https://blinkit.com/"
            f"cn/{slug}"
        )

        categories.append((
            name,
            slug,
            url
        ))

    print(
        f"Found "
        f"{len(categories)} "
        f"categories"
    )

    query = """
    INSERT INTO categories
    (
        name,
        slug,
        url
    )
    VALUES (
        %s,
        %s,
        %s
    )
    ON CONFLICT (slug)
    DO NOTHING
    """

    cursor.executemany(
        query,
        categories
    )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        "Categories "
        "saved to DB"
    )


if __name__ == "__main__":
    main()