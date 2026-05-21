import requests
from utils.headers import HEADERS


BASE_URL = (
    "https://blinkit.com/"
    "v1/layout/listing_widgets"
)


def fetch_products(l0_cat, l1_cat):
    offset = 0
    limit = 15
    all_products = []

    while True:
        url = (
            f"{BASE_URL}"
            f"?offset={offset}"
            f"&limit={limit}"
            f"&exclude_combos=false"
            f"&l0_cat={l0_cat}"
            f"&l1_cat={l1_cat}"
            f"&page_index=1"
        )

        print(f"\nCalling API:")
        print(url)

        try:
            response = requests.post(
                url,
                headers=HEADERS,
                timeout=30
            )

            print(
                f"Status Code: "
                f"{response.status_code}"
            )

            print(
                f"Response preview: "
                f"{response.text[:300]}"
            )

            response.raise_for_status()

            data = response.json()

            snippets = (
                data
                .get("response", {})
                .get("snippets", [])
            )

            print(
                f"Snippets found: "
                f"{len(snippets)}"
            )

            if not snippets:
                print(
                    "No more snippets."
                )
                break

            all_products.extend(
                snippets
            )

            offset += limit

        except Exception as e:
            print(
                f"ERROR: {e}"
            )
            break

    return all_products