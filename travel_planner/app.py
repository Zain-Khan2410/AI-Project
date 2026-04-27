"""
AI-Powered Travel Planner
Main Streamlit application entry point.
Run with: python -m streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv
import os

from planner.llm import generate_itinerary
from planner.weather import get_weather
from planner.places import get_top_places
from planner.currency import get_exchange_rate
# Note: format_itinerary_for_display and validate_inputs are kept 
# as per your original structure.
from utils.validators import validate_inputs

# ─────────────────────────────────────────────
# Load environment variables (Improved for Windows)
# ─────────────────────────────────────────────
# This ensures .env is found even if the terminal is in a different folder
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# ─────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS for a cleaner look
# ─────────────────────────────────────────────
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 2rem;
    }
   .info-card {
        background: #1e3a5f;
        border-left: 4px solid #4361ee;
        padding: 1rem 1.2rem;
        border-radius: 4px;
        margin-bottom: 1rem;
        color: #FFFFFF;
    }
    .weather-card {
        background: #3d2800;
        border-left: 4px solid #f4a261;
        padding: 1rem 1.2rem;
        border-radius: 4px;
        color: #FFFFFF;
    }
     .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #FFFFFF;
        border-bottom: 2px solid #4361ee;
        padding-bottom: 0.4rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar — User Inputs
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈️ Plan Your Trip")
    st.divider()

    destination = st.text_input(
        "🌍 Destination City",
        placeholder="e.g. Tokyo, Paris, Istanbul",
        help="Enter the city you want to visit."
    )

    num_days = st.slider(
        "📅 Number of Days",
        min_value=1,
        max_value=14,
        value=3,
        help="How many days is your trip?"
    )

    budget = st.selectbox(
        "💰 Budget Level",
        options=["Budget (Under $50/day)", "Mid-range ($50–150/day)", "Luxury ($150+/day)"],
        index=1,
        help="Choose your daily spending comfort level."
    )

    travel_style = st.multiselect(
        "🎯 Travel Style / Interests",
        options=["Culture & History", "Food & Dining", "Adventure & Outdoors",
                 "Shopping", "Art & Museums", "Nightlife", "Nature & Parks",
                 "Relaxation & Wellness"],
        default=["Culture & History", "Food & Dining"],
        help="Select what you enjoy most while traveling."
    )

    traveler_type = st.radio(
        "👥 Traveling As",
        options=["Solo", "Couple", "Family with Kids", "Group of Friends"],
        index=0
    )

    home_currency = st.text_input(
        "💱 Your Home Currency (optional)",
        placeholder="e.g. PKR, USD, GBP",
        help="We'll show the exchange rate for your destination."
    )

    st.divider()
    generate_btn = st.button("🚀 Generate My Itinerary", type="primary", use_container_width=True)


# ─────────────────────────────────────────────
# Main Content Area
# ─────────────────────────────────────────────
st.markdown('<p class="main-title">🗺️ AI Travel Planner</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by GROQ AI — get a personalized day-by-day itinerary instantly.</p>', unsafe_allow_html=True)

# Show welcome state
if not generate_btn:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Step 1** — Fill in your trip details in the sidebar.")
    with col2:
        st.info("**Step 2** — Select your travel style and budget.")
    with col3:
        st.info("**Step 3** — Hit 'Generate' and let the AI plan!")
    st.stop()

# ─────────────────────────────────────────────
# Input Validation
# ─────────────────────────────────────────────
errors = validate_inputs(destination, num_days, travel_style)
if errors:
    for error in errors:
        st.error(error)
    st.stop()

# ─────────────────────────────────────────────
# Main Generation Flow
# ─────────────────────────────────────────────
with st.spinner(f"🤖 Planning your {num_days}-day trip to {destination}..."):

    weather_data = None
    places_data = None
    
    weather_col, places_col, currency_col = st.columns(3)

    # Parallel enrichment calls
    with weather_col:
        try:
            weather_data = get_weather(destination)
            if weather_data:
                st.markdown(f"""
                    <div class="weather-card">
                        <b>🌤️ Weather in {destination}</b><br>
                        {weather_data['condition']}, {weather_data['temp_c']}°C<br>
                        <small>Humidity: {weather_data['humidity']}%</small>
                    </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.caption("Weather info currently unavailable.")

    with places_col:
        try:
            places_data = get_top_places(destination)
            if places_data:
                st.markdown(f"""
                    <div class="info-card">
                        <b>📍 Top Spots in {destination}</b><br>
                        {'<br>'.join([f"• {p}" for p in places_data[:4]])}
                    </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.caption("Top spots currently unavailable.")

    with currency_col:
        if home_currency:
            try:
                exchange_data = get_exchange_rate(home_currency.upper(), destination)
                if exchange_data:
                    st.markdown(f"""
                        <div class="info-card">
                            <b>💱 Exchange Rate</b><br>
                            1 {exchange_data['from']} = {exchange_data['rate']:.4f} {exchange_data['to']}<br>
                        </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.caption("Exchange rate unavailable.")

    st.divider()

    # Step 2: Generate the main itinerary via LLM (Gemini)
    try:
        raw_itinerary = generate_itinerary(
            destination=destination,
            num_days=num_days,
            budget=budget,
            travel_style=travel_style,
            traveler_type=traveler_type,
            weather_info=weather_data,
            places_info=places_data,
        )

        st.markdown(f'<p class="section-header">📋 Your {num_days}-Day {destination} Itinerary</p>',
                    unsafe_allow_html=True)

        # Display the result
        
        st.markdown(raw_itinerary)

        st.divider()

        st.download_button(
            label="📥 Download Itinerary",
            data=raw_itinerary,
            file_name=f"{destination.lower()}_itinerary.txt",
            mime="text/plain",
        )

    except Exception as e:
        st.error(f"❌ Generation Error: {e}")
        st.info("Check your GROQ_API_KEY in the .env file and ensure you have internet access.")