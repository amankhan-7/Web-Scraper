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

from scraper.categories import main as scrape_categories

logger = (
    setup_logger()
)

def main():

    logger.info(
        "Starting Blinkit scraper..."
    )

    # STEP 1: scrape raw data
    scrape_categories()

    # STEP 2: extract files
    raw_products = (
        extract_products()
    )

    logger.info(
        f"Extracted "
        f"{len(raw_products)} "
        f"raw products"
    )

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

    save_products(cleaned)

    logger.info(
        f"Inserted "
        f"{len(cleaned)} "
        f"products into Neon DB"
    )

if __name__ == "__main__":
    main()