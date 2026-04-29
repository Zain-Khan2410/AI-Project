import os
from groq import Groq
from config import get_settings

settings = get_settings()
groq_api_key = settings.groq_api_key

client = Groq(api_key=groq_api_key)

def build_system_prompt():
    return """You are an expert travel planner with strict verification rules.

FIRST AND MOST IMPORTANT RULE:
Before generating any itinerary, you must verify if the destination is a real, 
visitable place on Earth. 

If the destination is NOT a real city, town, country, or tourist destination 
(for example: a person's name, a random word, a fictional place, gibberish), 
you must REFUSE to generate an itinerary and instead respond ONLY with:

"❌ INVALID DESTINATION: '[destination]' does not appear to be a real travel 
destination. Please enter a valid city or country (e.g. Tokyo, Paris, Dubai, 
Karachi)."

Do NOT try to be creative or assume it could be a place. If you are not 
confident it is a real destination, refuse it.

Only if the destination IS a real place, create a detailed day-by-day itinerary 
with Morning, Afternoon, and Evening sections. Use Markdown formatting with ## 
for day headings and ### for time sections. End with a Quick Tips section."""


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
