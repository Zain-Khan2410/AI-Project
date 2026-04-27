import os
from groq import Groq
from config import get_settings

settings = get_settings()
groq_api_key = settings.groq_api_key

client = Groq(api_key=groq_api_key)

def build_system_prompt():
    return """You are an expert travel planner. Create detailed, practical 
day-by-day travel itineraries. For each day include Morning, Afternoon, 
and Evening sections with specific real places. Use Markdown formatting 
with ## for day headings and ### for time sections. End with a Quick Tips section."""

def build_user_prompt(destination, num_days, budget, travel_style,
                      traveler_type, weather_info=None, places_info=None):
    style_str = ", ".join(travel_style) if travel_style else "general sightseeing"

    enrichment = ""
    if weather_info:
        enrichment += f"\nCurrent weather: {weather_info['condition']}, {weather_info['temp_c']}°C"
    if places_info:
        enrichment += f"\nPopular spots: {', '.join(places_info[:5])}"

    return f"""Create a detailed {num_days}-day travel itinerary for:
Destination: {destination}
Budget: {budget}
Travel Style: {style_str}
Traveler Type: {traveler_type}
{enrichment}

Give specific real recommendations with day-by-day breakdown."""

def generate_itinerary(destination, num_days, budget, travel_style,
                       traveler_type, weather_info=None, places_info=None, **kwargs):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Free, very powerful model
        messages=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": build_user_prompt(
                destination, num_days, budget, travel_style,
                traveler_type, weather_info, places_info
            )}
        ],
        temperature=0.8,
        max_tokens=4096,
    )
    return response.choices[0].message.content