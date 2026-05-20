# scraper/visibility.py

import requests


def get_visibility():
    url = "https://blinkit.com/visibility"

    params = {
        "latitude": 27.1606595,
        "longitude": 77.9874933
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://blinkit.com/"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    print("Status:", response.status_code)
    print("Response text:")
    print(response.text[:500])  # print first 500 chars

    data = response.json()

    return data