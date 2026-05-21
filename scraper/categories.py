from playwright.sync_api import sync_playwright
import json
import os


categories = [
    "https://blinkit.com/cn/dairy-breakfast/milk/cid/14/922",
    "https://blinkit.com/cn/dairy-breakfast/bread-pav/cid/14/953",
    # "https://blinkit.com/cn/dairy-breakfast/eggs/cid/14/1200",
    # "https://blinkit.com/cn/dairy-breakfast/flakes-kids-cereals/cid/14/954",
    # "https://blinkit.com/cn/dairy-breakfast/muesli-granola/cid/14/614",
    # "https://blinkit.com/cn/dairy-breakfast/oats/cid/14/584",
]


def get_category_name(url):
    return url.split("/")[-4]


def main():

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        context = browser.new_context()

        for category_url in categories:

            category = (
                get_category_name(
                    category_url
                )
            )

            print(
                f"\nScraping: "
                f"{category}"
            )

            page = context.new_page()

            collected_products = []

            def handle_response(response):

                if (
                    "listing_widgets"
                    not in response.url
                ):
                    return

                try:

                    data = (
                        response.json()
                    )

                    snippets = (
                        data
                        .get(
                            "response",
                            {}
                        )
                        .get(
                            "snippets",
                            []
                        )
                    )

                    if snippets:

                        print(
                            f"Fetched "
                            f"{len(snippets)} "
                            f"products"
                        )

                        collected_products.extend(
                            snippets
                        )

                except Exception as e:
                    print(
                        f"Response error: {e}"
                    )

            page.on(
                "response",
                handle_response
            )

            try:

                page.goto(
                    category_url,
                    wait_until="networkidle",
                    timeout=60000
                )

                page.wait_for_timeout(
                    4000
                )

                # Scroll to trigger API pagination
                for _ in range(12):

                    page.mouse.wheel(
                        0,
                        6000
                    )

                    page.wait_for_timeout(
                        2000
                    )

            except Exception as e:

                print(
                    f"Page error "
                    f"for {category}: "
                    f"{e}"
                )

            # Remove duplicates safely
            unique_products = []

            seen = set()

            for product in collected_products:

                # Try different id fields
                product_id = (
                    product.get("id")
                    or product.get("product_id")
                    or str(product)
                )

                if product_id not in seen:
                    seen.add(
                        product_id
                    )

                    unique_products.append(
                        product
                    )

            category_folder = (
                f"data/raw/"
                f"{category}"
            )

            os.makedirs(
                category_folder,
                exist_ok=True
            )

            file_path = (
                f"{category_folder}/"
                f"products.json"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    unique_products,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            print(
                f"Saved "
                f"{len(unique_products)} "
                f"products → "
                f"{file_path}"
            )

            page.close()

        browser.close()