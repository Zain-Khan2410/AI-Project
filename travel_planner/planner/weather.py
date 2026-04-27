"""
planner/weather.py
──────────────────
Fetches current weather for the destination city using WeatherAPI.com.

Sign up free at: https://www.weatherapi.com
Add WEATHER_API_KEY=your_key to your .env file.

API docs: https://www.weatherapi.com/docs/
"""

import os
import requests


WEATHER_API_BASE = "http://api.weatherapi.com/v1"


def get_weather(city: str) -> dict | None:
    """
    Fetch current weather conditions for a given city.

    Returns a dict like:
        {
            "city": "Tokyo",
            "country": "Japan",
            "temp_c": 24.0,
            "temp_f": 75.2,
            "condition": "Partly cloudy",
            "humidity": 72,
            "wind_kph": 18.0,
            "feels_like_c": 26.1,
        }

    Returns None if the API key is missing or the request fails.
    """

    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        # Gracefully skip if key not configured
        return None

    url = f"{WEATHER_API_BASE}/current.json"

    # Build query params
    params = {
        "key": api_key,
        "q": city,          # City name or coordinates ("lat,lon")
        "aqi": "no",        # We don't need air quality data
    }

    try:
        # Make the GET request
        response = requests.get(url, params=params, timeout=10)

        # Raise an exception for HTTP error codes (4xx, 5xx)
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        # Extract the fields we care about
        return {
            "city":         data["location"]["name"],
            "country":      data["location"]["country"],
            "temp_c":       data["current"]["temp_c"],
            "temp_f":       data["current"]["temp_f"],
            "condition":    data["current"]["condition"]["text"],
            "humidity":     data["current"]["humidity"],
            "wind_kph":     data["current"]["wind_kph"],
            "feels_like_c": data["current"]["feelslike_c"],
        }

    except requests.exceptions.RequestException as e:
        print(f"[WeatherAPI] Request failed: {e}")
        return None

    except KeyError as e:
        print(f"[WeatherAPI] Unexpected response format: {e}")
        return None
