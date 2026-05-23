import json
from pathlib import Path
from urllib.parse import (
    urlparse,
    parse_qs
)

INPUT_FILE = Path("data/feed.json")
OUTPUT_FILE = Path(
    "data/clean_feed.json"
)


def slugify(text):
    """milk -> milk
    Cheese Slices -> cheese-slices
    """

    if not text:
        return None

    return (
        text.strip()
        .lower()
        .replace("&", "and")
        .replace(",", "")
        .replace(" ", "-")
    )


def extract_widget(widget):
    """
    Convert SDUI widget
    → clean structure
    """

    wtype = widget.get("type")

    # -----------------
    # CATEGORY GRID
    # -----------------
    if wtype == 52:

        items = (
            widget
            .get("data", {})
            .get("items", [])
        )

        return {
            "type":
                "category_grid",

            "items": [
                {
                    "title":
                        i.get(
                            "image_title"
                        ),

                    "image":
                        i.get(
                            "image"
                        ),

                    "deeplink":
                        i.get(
                            "deeplink"
                        ),
                }
                for i in items
            ]
        }

    # -----------------
    # BANNER
    # -----------------
    if wtype == 55:

        return {
            "type":
                "banner",

            "image":
                widget.get(
                    "data",
                    {}
                ).get(
                    "image"
                ),

            "deeplink":
                widget.get(
                    "action",
                    {}
                ).get(
                    "default_uri"
                ),
        }

    # -----------------
    # PRODUCT SECTION
    # -----------------
    if wtype == 77:

        header = (
            widget.get(
                "header_config",
                {}
            )
        )

        objects = (
            widget.get(
                "objects",
                []
            )
        )

        return {
            "type":
                "product_collection",

            "title":
                header.get(
                    "title"
                ),

            "deeplink":
                header.get(
                    "button_deeplink"
                ),

            "collection_uuid":
                extract_collection(
                    objects
                ),
        }

    return None


def extract_collection(
    objects
):
    """
    Get collection UUID
    """

    for obj in objects:

        data = obj.get(
            "data",
            {}
        )

        if (
            "collection_uuid"
            in data
        ):
            return data[
                "collection_uuid"
            ]

    return None


def extract_categories(
    raw_item
):
    """
    Extract real category
    mapping from products

    Example:
    14_922 -> milk
    """

    category_map = {}

    data = (
        raw_item.get(
            "data",
            {}
        )
    )

    objects = (
        data.get(
            "objects",
            []
        )
    )

    for widget in objects:

        widget_objects = (
            widget.get(
                "objects",
                []
            )
        )

        for obj in widget_objects:

            products = (
                obj.get(
                    "data",
                    {}
                )
                .get(
                    "products",
                    []
                )
            )

            for group in products:

                if not group:
                    continue

                product = group[0]

                category_type = (
                    product.get(
                        "type"
                    )
                )

                l0 = (
                    product.get(
                        "level0_category",
                        [{}]
                    )[0]
                    .get("id")
                )

                l1 = (
                    product.get(
                        "level1_category",
                        [{}]
                    )[0]
                    .get("id")
                )

                if (
                    not category_type
                    or not l0
                    or not l1
                ):
                    continue

                key = (
                    f"{l0}_{l1}"
                )

                if (
                    key
                    not in category_map
                ):

                    category_map[
                        key
                    ] = {
                        "category":
                            slugify(
                                category_type
                            ),

                        "display_name":
                            category_type,

                        "l0_cat":
                            str(l0),

                        "l1_cat":
                            str(l1),

                        "url":
                            (
                                "https://blinkit.com/"
                                f"cn/"
                                f"{slugify(category_type)}"
                                f"/cid/"
                                f"{l0}/"
                                f"{l1}"
                            )
                    }

    return list(
        category_map.values()
    )


def clean(captured):

    cleaned = []

    for item in captured:

        url = item.get(
            "url",
            ""
        )

        data = item.get(
            "data",
            {}
        )

        if (
            "feed"
            not in url
        ):
            continue

        objects = (
            data.get(
                "objects",
                []
            )
        )

        if not objects:
            continue

        widgets = []

        for w in objects:

            parsed = (
                extract_widget(
                    w
                )
            )

            if parsed:
                widgets.append(
                    parsed
                )

        categories = (
            extract_categories(
                item
            )
        )

        cleaned.append({
            "url":
                url,

            "widgets_count":
                len(widgets),

            "widgets":
                widgets,

            "categories":
                categories
        })

    return cleaned


if __name__ == "__main__":

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        captured = (
            json.load(f)
        )

    cleaned = clean(
        captured
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cleaned,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Saved "
        f"{len(cleaned)} "
        f"feeds → "
        f"{OUTPUT_FILE}"
    )