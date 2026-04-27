"""
planner/places.py
─────────────────
Fetches top places using OpenStreetMap Overpass API.
Completely FREE - no API key required!
"""

import requests

def get_top_places(city: str, limit: int = 8):
    """
    Fetch tourist attractions using OpenStreetMap.
    No API key needed - completely free!
    """
    try:
        # First get city coordinates using Nominatim
        nominatim_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": city,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "TravelPlannerApp/1.0"
        }

        response = requests.get(nominatim_url, params=params, 
                                headers=headers, timeout=10)
        response.raise_for_status()
        location_data = response.json()

        if not location_data:
            return None

        lat = float(location_data[0]["lat"])
        lon = float(location_data[0]["lon"])

        # Now fetch tourist attractions near those coordinates
        overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Search within 10km radius
        radius = 10000
        
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node["tourism"="attraction"]
              (around:{radius},{lat},{lon});
          node["tourism"="museum"]
              (around:{radius},{lat},{lon});
          node["tourism"="viewpoint"]
              (around:{radius},{lat},{lon});
          node["historic"="monument"]
              (around:{radius},{lat},{lon});
          node["amenity"="place_of_worship"]
              (around:{radius},{lat},{lon});
        );
        out body {limit};
        """

        overpass_response = requests.post(
    overpass_url,
    data={"data": overpass_query},
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    timeout=30
)
        overpass_response.raise_for_status()
        data = overpass_response.json()

        # Extract place names
        places = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name:en") or tags.get("name")
            if name and name not in places:
                places.append(name)

        return places[:limit] if places else None

    except Exception as e:
        print(f"[OpenStreetMap] Request failed: {e}")
        return None


def get_place_details(place_id: str):
    return None