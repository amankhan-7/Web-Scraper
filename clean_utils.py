import json
from pathlib import Path

INPUT_FILE = Path("data/feed.json")
OUTPUT_FILE = Path("data/clean_feed.json")


def extract_widget(widget):
    """Convert SDUI widget → clean structure"""

    wtype = widget.get("type")

    # CATEGORY GRID
    if wtype == 52:
        items = widget.get("data", {}).get("items", [])
        return {
            "type": "category_grid",
            "items": [
                {
                    "title": i.get("image_title"),
                    "image": i.get("image"),
                    "deeplink": i.get("deeplink"),
                }
                for i in items
            ]
        }

    # BANNER
    if wtype == 55:
        return {
            "type": "banner",
            "image": widget.get("data", {}).get("image"),
            "deeplink": widget.get("action", {}).get("default_uri"),
        }

    # PRODUCT / COLLECTION SECTION
    if wtype == 77:
        header = widget.get("header_config", {})
        objects = widget.get("objects", [])

        return {
            "type": "product_collection",
            "title": header.get("title"),
            "deeplink": header.get("button_deeplink"),
            "collection_uuid": extract_collection(objects),
        }

    return None


def extract_collection(objects):
    for obj in objects:
        data = obj.get("data", {})
        if "collection_uuid" in data:
            return data["collection_uuid"]
    return None



def clean(captured):
    cleaned = []

    for item in captured:
        url = item.get("url")
        data = item.get("data", {})

        if "feed" not in url:
            continue

        objects = data.get("objects", [])
        if not objects:
            continue

        widgets = []

        for w in objects:
            parsed = extract_widget(w)
            if parsed:
                widgets.append(parsed)

        cleaned.append({
            "url": url,
            "widgets_count": len(widgets),
            "widgets": widgets
        })

    return cleaned



if __name__ == "__main__":
    clean()