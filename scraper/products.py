import requests
from utils.headers import HEADERS


BASE_URL = (
    "https://blinkit.com/"
    "v1/layout/listing_widgets"
)


def fetch_products(
        l0_cat=14,
        l1_cat=922
):

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

        response = requests.post(
            url,
            headers=HEADERS
        )

        data = response.json()

        snippets = (
            data
            .get("response", {})
            .get("snippets", [])
        )

        if not snippets:
            break

        all_products.extend(snippets)

        print(
            f"Fetched {len(snippets)}"
        )

        offset += limit

    return all_products