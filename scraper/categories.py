from playwright.sync_api import sync_playwright
import json
import os
import traceback

FEED_FILE = "data/clean_feed.json"


# -----------------------------
# LOAD CATEGORIES
# -----------------------------
def load_categories_from_feed():

    with open(FEED_FILE, "r", encoding="utf-8") as f:
        feeds = json.load(f)

    categories = []
    seen = set()

    for feed in feeds:
        for category in feed.get("categories", []):

            l0_cat = category.get("l0_cat")
            l1_cat = category.get("l1_cat")
            url = category.get("url")

            if not l0_cat or not l1_cat or not url:
                continue

            key = (l0_cat, l1_cat)

            if key in seen:
                continue

            seen.add(key)

            categories.append(
                {
                    "title": category.get("display_name", category.get("category", "")),
                    "category": category.get("category", ""),
                    "url": url,
                    "l0_cat": l0_cat,
                    "l1_cat": l1_cat,
                }
            )

    print(f"\nLoaded {len(categories)} categories")
    return categories


# -----------------------------
# SAFE FOLDER NAME
# -----------------------------
def safe_folder_name(text):
    return (
        text.lower()
        .replace("&", "and")
        .replace(",", "")
        .replace(" ", "-")
        .replace("/", "-")
    )


# -----------------------------
# CATEGORY INFO PARSER
# -----------------------------
def get_category_info(page, category_obj):

    page.goto(category_obj["url"], wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    final_url = page.url

    print("\nResolved URL:")
    print(final_url)

    parts = final_url.split("?")[0].split("/")

    try:
        cid_index = parts.index("cid")

        parent_category = parts[cid_index - 2]
        category = parts[cid_index - 1]

        info = {
            "parent_category": parent_category,
            "category": category,
            "l0_cat": parts[cid_index + 1],
            "l1_cat": parts[cid_index + 2],
            "category_path": f"{parts[cid_index + 1]}/{parts[cid_index + 2]}",
            "url": final_url,
        }

        print(json.dumps(info, indent=2))
        return info

    except Exception:
        raise Exception(f"Could not parse URL: {final_url}")


# -----------------------------
# MAIN SCRAPER
# -----------------------------
def main():

    os.makedirs("data/raw", exist_ok=True)

    categories = load_categories_from_feed()

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        for category_obj in categories:

            page = context.new_page()
            collected_products = []

            try:

                # -----------------------------
                # RESPONSE HANDLER
                # -----------------------------
                def handle_response(response):

                    if "listing_widgets" not in response.url:
                        return

                    try:
                        content_type = response.headers.get("content-type", "")

                        if "application/json" not in content_type:
                            return

                        # SAFE JSON PARSING
                        try:
                            data = response.json()
                        except Exception:
                            try:
                                data = json.loads(response.text())
                            except Exception:
                                return

                    except Exception:
                        return

                    snippets = data.get("response", {}).get("snippets", [])

                    if not snippets:
                        return

                    print(f"Fetched {len(snippets)} products")

                    for product in snippets:

                        product_data = product.get("data", {})

                        # ENRICH DATA
                        product_data.update(
                            {
                                "category": category_obj["category"],
                                "parent_category": category_obj["category"],
                                "l0_cat": category_obj["l0_cat"],
                                "l1_cat": category_obj["l1_cat"],
                                "category_path": f"{category_obj['l0_cat']}/{category_obj['l1_cat']}",
                            }
                        )

                        collected_products.append(product_data)

                    print(f"Collected: {len(collected_products)}")

                # attach listener
                page.on("response", handle_response)

                # open category
                page.goto(
                    category_obj["url"], wait_until="domcontentloaded", timeout=60000
                )
                page.wait_for_timeout(5000)

                # -----------------------------
                # IMPROVED SCROLL LOGIC
                # -----------------------------
                last_height = 0

                for i in range(20):

                    print(f"Scroll {i + 1}/20")

                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(3000)

                    new_height = page.evaluate("document.body.scrollHeight")

                    if new_height == last_height:
                        print("No more content → stopping scroll")
                        break

                    last_height = new_height

            except Exception as e:
                print("\nPAGE ERROR:")
                print(str(e))
                traceback.print_exc()

            finally:
                # IMPORTANT cleanup
                page.remove_listener("response", handle_response)

            # -----------------------------
            # DEDUPLICATION
            # -----------------------------
            unique_products = []
            seen_ids = set()

            for product in collected_products:

                product_id = product.get("product_id") or product.get(
                    "identity", {}
                ).get("id")

                if not product_id or product_id in seen_ids:
                    continue

                seen_ids.add(product_id)
                unique_products.append(product)

            # -----------------------------
            # SAVE OUTPUT
            # -----------------------------
            category_folder = f"data/raw/{safe_folder_name(category_obj['category'])}"
            os.makedirs(category_folder, exist_ok=True)

            file_path = f"{category_folder}/products.json"

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(unique_products, f, indent=2, ensure_ascii=False)

            print(f"\nSaved {len(unique_products)} products → {file_path}")

            page.close()

        browser.close()


if __name__ == "__main__":
    main()
