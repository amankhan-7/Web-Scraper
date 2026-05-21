from playwright.sync_api import (
    sync_playwright
)

import json
import os
import traceback


categories = [
    "https://blinkit.com/cn/dairy-breakfast/milk/cid/14/922",
    "https://blinkit.com/cn/dairy-breakfast/bread-pav/cid/14/953",
    "https://blinkit.com/cn/dairy-breakfast/eggs/cid/14/1200",
    "https://blinkit.com/cn/dairy-breakfast/flakes-kids-cereals/cid/14/954",
    "https://blinkit.com/cn/dairy-breakfast/muesli-granola/cid/14/614",
    "https://blinkit.com/cn/dairy-breakfast/oats/cid/14/584",
    "https://blinkit.com/cn/dairy-breakfast/paneer-tofu/cid/14/923",
    "https://blinkit.com/cn/dairy-breakfast/curd-yogurt/cid/14/123",
    "https://blinkit.com/cn/dairy-breakfast/butter-more/cid/14/952",
    "https://blinkit.com/cn/dairy-breakfast/cheese/cid/14/2253",
    "https://blinkit.com/cn/dairy-breakfast/cream-whitener/cid/14/1092",
    "https://blinkit.com/cn/dairy-breakfast/condensed-milk/cid/14/130",
    "https://blinkit.com/cn/dairy-breakfast/vermicelli/cid/14/1140",
    "https://blinkit.com/cn/dairy-breakfast/poha-daliya-other-grains/cid/14/1295",
    "https://blinkit.com/cn/dairy-breakfast/peanut-butter/cid/14/644",
    "https://blinkit.com/cn/dairy-breakfast/energy-bars/cid/14/2557",
    "https://blinkit.com/cn/dairy-breakfast/lassi-shakes-more/cid/14/1184",
    "https://blinkit.com/cn/dairy-breakfast/breakfast-mixes/cid/14/1612",
    "https://blinkit.com/cn/dairy-breakfast/honey-chyawanprash/cid/14/609",
    "https://blinkit.com/cn/dairy-breakfast/sausage-salami-ham/cid/14/1388",
    "https://blinkit.com/cn/dairy-breakfast/batter/cid/14/1425"
]


def get_category_info(url):

    parts = url.split("/")

    info = {
        "parent_category":
            parts[-5],

        "category":
            parts[-4],

        "cid_label":
            parts[-3],

        "l0_cat":
            parts[-2],

        "l1_cat":
            parts[-1],

        "category_path":
            f"{parts[-2]}/"
            f"{parts[-1]}"
    }

    print(
        "\nParsed category "
        "info:"
    )

    print(
        json.dumps(
            info,
            indent=2
        )
    )

    return info


def main():

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    with sync_playwright() as p:

        browser = (
            p.chromium.launch(
                headless=False
            )
        )

        context = (
            browser.new_context()
        )

        for category_url in categories:

            category_info = (
                get_category_info(
                    category_url
                )
            )

            category = (
                category_info[
                    "category"
                ]
            )

            print(
                "\n=================="
            )

            print(
                f"Scraping: "
                f"{category}"
            )

            print(
                f"URL: "
                f"{category_url}"
            )

            print(
                "=================="
            )

            page = (
                context.new_page()
            )

            collected_products = []

            def handle_response(
                response
            ):

                if (
                    "listing_widgets"
                    not in response.url
                ):
                    return

                print(
                    "\nAPI response hit:"
                )

                print(
                    response.url
                )

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

                    print(
                        f"Fetched "
                        f"{len(snippets)} "
                        f"products"
                    )

                    if (
                        not snippets
                    ):
                        return

                    # Debug first product
                    print(
                        "\nFirst "
                        "product BEFORE:"
                    )

                    print(
                        json.dumps(
                            snippets[0],
                            indent=2,
                            ensure_ascii=False
                        )[:500]
                    )

                    # Add category metadata
                    for product in snippets:

                        # Actual product lives
                        # inside data
                        product_data = (
                            product.get(
                                "data",
                                {}
                            )
                        )

                        product_data[
                            "category"
                        ] = (
                            category_info[
                                "category"
                            ]
                        )

                        product_data[
                            "parent_category"
                        ] = (
                            category_info[
                                "parent_category"
                            ]
                        )

                        product_data[
                            "l0_cat"
                        ] = (
                            category_info[
                                "l0_cat"
                            ]
                        )

                        product_data[
                            "l1_cat"
                        ] = (
                            category_info[
                                "l1_cat"
                            ]
                        )

                        product_data[
                            "category_path"
                        ] = (
                            category_info[
                                "category_path"
                            ]
                        )

                    print(
                        "\nFirst "
                        "product AFTER:"
                    )

                    print(
                        json.dumps(
                            snippets[0],
                            indent=2,
                            ensure_ascii=False
                        )[:700]
                    )

                    collected_products.extend(
                        snippets
                    )

                    print(
                        f"\nCollected "
                        f"total: "
                        f"{len(collected_products)}"
                    )

                except Exception as e:

                    print(
                        "\nRESPONSE ERROR:"
                    )

                    print(str(e))

                    traceback.print_exc()

            page.on(
                "response",
                handle_response
            )

            try:

                print(
                    "\nOpening page..."
                )

                # Blinkit keeps
                # network active
                page.goto(
                    category_url,
                    wait_until=
                    "domcontentloaded",
                    timeout=60000
                )

                page.wait_for_timeout(
                    5000
                )

                print(
                    "\nScrolling..."
                )

                for i in range(12):

                    print(
                        f"Scroll "
                        f"{i + 1}/12"
                    )

                    page.mouse.wheel(
                        0,
                        6000
                    )

                    page.wait_for_timeout(
                        2000
                    )

            except Exception as e:

                print(
                    f"\nPAGE ERROR "
                    f"for {category}:"
                )

                print(str(e))

            print(
                "\nRemoving duplicates..."
            )

            unique_products = []

            seen = set()

            for product in (
                collected_products
            ):

                product_data = (
                    product.get(
                        "data",
                        {}
                    )
                )

                product_id = (
                    product_data.get(
                        "product_id"
                    )
                    or product_data
                    .get(
                        "identity",
                        {}
                    )
                    .get("id")
                )

                if (
                    not product_id
                ):
                    continue

                if (
                    product_id
                    not in seen
                ):

                    seen.add(
                        product_id
                    )

                    unique_products.append(
                        product
                    )

            print(
                f"Unique products: "
                f"{len(unique_products)}"
            )

            if unique_products:

                print(
                    "\nSample saved "
                    "product:"
                )

                print(
                    json.dumps(
                        unique_products[
                            0
                        ],
                        indent=2,
                        ensure_ascii=False
                    )[:1000]
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
                f"\nSaved "
                f"{len(unique_products)} "
                f"products → "
                f"{file_path}"
            )

            page.close()

        browser.close()


if __name__ == "__main__":
    main()