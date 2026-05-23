from scraper.extractor import (
    extract_products
)

from scraper.cleaner import (
    clean_products
)

from db.neon import (
    save_products
)

from utils.loggers import (
    setup_logger
)

from scraper.categories import (
    main as scrape_categories
)

from layout.feed_extractor import (
    fetch
)

from layout.fill_categories import (
    main as fill_categories
)

from layout.fill_categories_slug import (
    insert_products
)


logger = setup_logger()


def main():

    logger.info(
        "Starting Blinkit scraper..."
    )

    # STEP 1:
    # Fetch feed/category data
    fetch()

    logger.info(
        "Feed extracted"
    )

    # STEP 2:
    # Scrape raw products
    scrape_categories()

    logger.info(
        "Raw scraping complete"
    )

    # STEP 3:
    # Extract files
    raw_products = (
        extract_products()
    )

    logger.info(
        f"Extracted "
        f"{len(raw_products)} "
        f"raw products"
    )

    # STEP 4:
    # Clean products
    cleaned = (
        clean_products(
            raw_products
        )
    )

    logger.info(
        f"Cleaned "
        f"{len(cleaned)} "
        f"products"
    )

    # STEP 5:
    # Save products
    save_products(
        cleaned
    )

    logger.info(
        f"Inserted "
        f"{len(cleaned)} "
        f"products into Neon DB"
    )

    # STEP 6:
    # Fill categories table
    fill_categories()

    logger.info(
        "Category table created"
    )

    # STEP 7:
    # Add category_id FK
    insert_products()

    logger.info(
        "category.id inserted "
        "in blinkit_products"
    )


if __name__ == "__main__":
    main()