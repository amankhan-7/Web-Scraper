from playwright.sync_api import sync_playwright
import json
import os


counter = 1


def main():
    global counter

    # Create folder if not exists
    os.makedirs("data", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        # Listen to API responses
        def handle_response(response):
            global counter

            url = response.url

            if "listing_widgets" in url:
                print("\nFOUND API:")
                print(url)

                try:
                    data = response.json()

                    file_path = (
                        f"data/api_{counter}.json"
                    )

                    with open(
                        file_path,
                        "w",
                        encoding="utf-8"
                    ) as f:
                        json.dump(
                            data,
                            f,
                            indent=2,
                            ensure_ascii=False
                        )

                    print(
                        f"Saved {file_path}"
                    )

                    counter += 1

                except Exception as e:
                    print("Error:", e)

        page.on(
            "response",
            handle_response
        )

        # Open Blinkit
        page.goto(
            "https://blinkit.com"
        )

        page.wait_for_timeout(5000)

        # Open category
        page.goto(
            "https://blinkit.com/cn/dairy-breakfast/milk/cid/14/922"
        )

        # Wait for APIs
        page.wait_for_timeout(10000)

        browser.close()


main()