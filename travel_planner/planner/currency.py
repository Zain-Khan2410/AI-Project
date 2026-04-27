"""
planner/currency.py
───────────────────
Fetches live exchange rates using ExchangeRate-API (free tier).

Free tier: https://www.exchangerate-api.com
No API key needed for the open endpoint (limited but works for demos).

Or sign up for a free key at exchangerate-api.com and add:
EXCHANGE_API_KEY=your_key to your .env file.
"""

import os
import requests


# Mapping common destination cities to their local currency codes
CITY_TO_CURRENCY = {
    "tokyo": "JPY", "osaka": "JPY", "kyoto": "JPY",
    "paris": "EUR", "rome": "EUR", "berlin": "EUR", "madrid": "EUR",
    "london": "GBP",
    "dubai": "AED",
    "bangkok": "THB",
    "istanbul": "TRY",
    "new york": "USD", "los angeles": "USD", "chicago": "USD",
    "karachi": "PKR", "lahore": "PKR", "islamabad": "PKR",
    "mumbai": "INR", "delhi": "INR",
    "toronto": "CAD", "vancouver": "CAD",
    "sydney": "AUD", "melbourne": "AUD",
    "singapore": "SGD",
    "kuala lumpur": "MYR",
    "cairo": "EGP",
    "nairobi": "KES",
    "amsterdam": "EUR", "vienna": "EUR", "prague": "CZK",
    "barcelona": "EUR", "lisbon": "EUR",
    "beijing": "CNY", "shanghai": "CNY",
    "seoul": "KRW",
}


def guess_currency_for_city(city: str) -> str | None:
    """
    Try to map a city name to its local currency code.
    Returns None if not found in the lookup table.
    """
    return CITY_TO_CURRENCY.get(city.lower().strip())


def get_exchange_rate(from_currency: str, destination_city: str) -> dict | None:
    """
    Get the exchange rate from the user's home currency to the destination's currency.

    Parameters:
        from_currency    : e.g. "PKR", "USD", "GBP"
        destination_city : e.g. "Tokyo" — will be mapped to "JPY"

    Returns a dict like:
        {"from": "PKR", "to": "JPY", "rate": 0.4123}

    Returns None if the city currency isn't known or the request fails.
    """

    to_currency = guess_currency_for_city(destination_city)
    if not to_currency:
        return None  # We don't know this city's currency

    if from_currency == to_currency:
        return {"from": from_currency, "to": to_currency, "rate": 1.0}

    api_key = os.getenv("EXCHANGE_API_KEY")

    # Try the free (keyless) endpoint first
    if api_key:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
    else:
        # Open endpoint — no key required, but rate-limited
        url = f"https://open.er-api.com/v6/latest/{from_currency}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if api_key:
            # Keyed endpoint returns direct conversion_rate
            rate = data.get("conversion_rate")
        else:
            # Open endpoint returns all rates
            rates = data.get("rates", {})
            rate = rates.get(to_currency)

        if rate is None:
            return None

        return {
            "from": from_currency,
            "to":   to_currency,
            "rate": round(rate, 4),
        }

    except requests.exceptions.RequestException as e:
        print(f"[CurrencyAPI] Request failed: {e}")
        return None
