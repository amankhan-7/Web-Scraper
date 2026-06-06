import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_visibility():
    url = "https://blinkit.com/visibility"

    latitude = float(os.getenv("LATITUDE", 27.16))
    longitude = float(os.getenv("LONGITUDE", 77.98))

    params = {"latitude": latitude, "longitude": longitude}

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://blinkit.com/",
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
    except Exception:
        return _empty(latitude, longitude)

    if response.status_code != 200:
        return _empty(latitude, longitude)

    try:
        data = response.json()
    except Exception:
        return _empty(latitude, longitude)

    # -----------------------------
    # SAFE SEARCH (ALL LEVELS)
    # -----------------------------

    city = None
    state = None
    city_id = None

    # 1. direct root level
    city = data.get("cityName") or data.get("city_name")
    state = data.get("stateName") or data.get("state_name")
    city_id = data.get("cityId") or data.get("city_id")

    # 2. fallback: data object
    if not city:
        city = (data.get("data") or {}).get("cityName") or (data.get("data") or {}).get("city_name")

    if not state:
        state = (data.get("data") or {}).get("stateName") or (data.get("data") or {}).get("state_name")

    # 3. fallback: merchants (MOST RELIABLE)
    merchants = data.get("merchants") or []
    if merchants:
        m = merchants[0]
        city = city or m.get("city_name")
        state = state or m.get("state_name")
        city_id = city_id or m.get("city_id")

    result = {
        "city": city,
        "state": state,
        "city_id": city_id,
        "latitude": latitude,
        "longitude": longitude,
        "merchant_id": (merchants[0].get("id") if merchants else None),
        "serviceable": data.get("serviceable", False),
    }

    print("\nVISIBILITY RESULT:", result)

    return result


def _empty(latitude, longitude):
    return {
        "city": None,
        "state": None,
        "city_id": None,
        "latitude": latitude,
        "longitude": longitude,
        "merchant_id": None,
        "serviceable": False,
    }