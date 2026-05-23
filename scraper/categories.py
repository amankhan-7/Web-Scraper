from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, parse_qs

import json
import os
import traceback


FEED_FILE = "data/clean_feed.json"


def load_categories_from_feed():

    with open(
        FEED_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        feeds = json.load(f)

    categories = []
    seen = set()

    for feed in feeds:

        for category in feed.get(
            "categories",
            []
        ):

            l0_cat = category.get(
                "l0_cat"
            )

            l1_cat = category.get(
                "l1_cat"
            )

            url = category.get(
                "url"
            )

            if (
                not l0_cat
                or not l1_cat
                or not url
            ):
                continue

            key = (
                l0_cat,
                l1_cat
            )

            if key in seen:
                continue

            seen.add(key)

            categories.append({
                "title":
                    category.get(
                        "display_name",
                        category.get(
                            "category",
                            ""
                        )
                    ),

                "category":
                    category.get(
                        "category",
                        ""
                    ),

                "url":
                    url,

                "l0_cat":
                    l0_cat,

                "l1_cat":
                    l1_cat
            })

    print(
        f"\nLoaded "
        f"{len(categories)} "
        f"categories"
    )

    return categories


def get_category_info(
    page,
    category_obj
):

    page.goto(
        category_obj["url"],
        wait_until=
        "domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(
        3000
    )

    final_url = page.url

    print(
        "\nResolved URL:"
    )

    print(final_url)

    parts = (
        final_url
        .split("?")[0]
        .split("/")
    )

    try:

        cid_index = (
            parts.index(
                "cid"
            )
        )

        parent_category = (
            parts[
                cid_index - 2
            ]
        )

        category = (
            parts[
                cid_index - 1
            ]
        )

        info = {

            "parent_category":
                parent_category,

            "category":
                category,

            "l0_cat":
                parts[
                    cid_index + 1
                ],

            "l1_cat":
                parts[
                    cid_index + 2
                ],

            "category_path":
                f"{parts[cid_index + 1]}/"
                f"{parts[cid_index + 2]}",

            "url":
                final_url
        }

        print(
            json.dumps(
                info,
                indent=2
            )
        )

        return info

    except Exception:

        raise Exception(
            f"Could not parse "
            f"URL: {final_url}"
        )


def safe_folder_name(
    text
):

    return (
        text.lower()
        .replace("&", "and")
        .replace(",", "")
        .replace(" ", "-")
        .replace("/", "-")
    )


def main():

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    categories = (
        load_categories_from_feed()
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

        for category_obj in categories:

            page = (
                context.new_page()
            )

            collected_products = []

            try:

                category_info = (
                    get_category_info(
                        page,
                        category_obj
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
                    f"{category_info['url']}"
                )

                print(
                    "=================="
                )

                def handle_response(
                    response
                ):

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

                        if (
                            not snippets
                        ):
                            return

                        print(
                            f"Fetched "
                            f"{len(snippets)} "
                            f"products"
                        )

                        for product in snippets:

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

                        collected_products.extend(
                            snippets
                        )

                        print(
                            f"Collected: "
                            f"{len(collected_products)}"
                        )

                    except Exception:

                        traceback.print_exc()

                page.on(
                    "response",
                    handle_response
                )

                page.goto(
                    category_info[
                        "url"
                    ],
                    wait_until=
                    "domcontentloaded",
                    timeout=60000
                )

                page.wait_for_timeout(
                    5000
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
                    f"\nPAGE ERROR:"
                )

                print(str(e))

            print(
                "\nRemoving duplicates..."
            )

            unique_products = []
            seen_ids = set()

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
                    in seen_ids
                ):
                    continue

                seen_ids.add(
                    product_id
                )

                unique_products.append(
                    product
                )

            category_folder = (
                f"data/raw/"
                f"{safe_folder_name(category)}"
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