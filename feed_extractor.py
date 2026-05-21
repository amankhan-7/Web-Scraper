import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

from clean_utils import clean

OUTPUT_FILE = Path("data/feed.json")

TARGET_KEYWORDS = [
    "layout",
    "feed",
    "home",
    "listing",
    "products"
]


def is_useful(url: str) -> bool:
    return any(k in url for k in TARGET_KEYWORDS)


async def fetch():
    print("🚀 Starting scraper...")

    captured = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            locale="en-IN",
        )

        page = await context.new_page()

        async def on_response(response):
            url = response.url

            if is_useful(url):
                try:
                    data = await response.json()
                except:
                    return

                captured.append({
                    "url": url,
                    "data": data
                })

                print("📡 captured:", url)

        page.on("response", on_response)

        await page.goto("https://blinkit.com", wait_until="domcontentloaded")
        await page.wait_for_timeout(20000)

        await browser.close()

    # ✅ SAVE RAW FIRST
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(captured, f, indent=2, ensure_ascii=False)

    print(f"📦 Saved RAW → {OUTPUT_FILE}")

    # ✅ CLEAN AFTER CAPTURE COMPLETES
    cleaned = clean(captured)

    clean_path = Path("data/clean_feed.json")
    with open(clean_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved CLEAN → {clean_path}")


if __name__ == "__main__":
    asyncio.run(fetch())