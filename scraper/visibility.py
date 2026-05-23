import os
import requests

from dotenv import load_dotenv

load_dotenv()


def get_visibility():

    url = (
        "https://blinkit.com/visibility"
    )

    latitude = float(
        os.getenv("LATITUDE")
    )

    longitude = float(
        os.getenv("LONGITUDE")
    )

    params = {
        "latitude": latitude,
        "longitude": longitude
    }

    headers = {
        "User-Agent":
            "Mozilla/5.0",

        "Accept":
            "application/json",

        "Referer":
            "https://blinkit.com/"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    print(
        "Status:",
        response.status_code
    )

    print("Response text:")
    print(
        response.text[:500]
    )

    data = response.json()

    return data