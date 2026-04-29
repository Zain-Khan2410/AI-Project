# AI-Project
# 🗺️ AI Travel Planner

---

## 📌 Project Overview

The **AI Travel Planner** is an intelligent web application that automatically generates personalized day-by-day travel itineraries based on user preferences. Users simply enter their destination, number of days, budget, and travel style — and the AI instantly creates a complete, structured travel plan.

The system uses a **Large Language Model (LLaMA 3.3 70B via Groq API)** to generate intelligent travel recommendations, combined with real-time data from multiple APIs for weather, top attractions, currency conversion, and destination photos.

---

## ✨ Features

- 🤖 **AI-Generated Itineraries** — Day-by-day travel plans powered by LLaMA 3.3 70B
- 🌤️ **Live Weather** — Real-time weather conditions at your destination
- 📍 **Top Attractions** — Popular tourist spots fetched via OpenStreetMap
- 💱 **Currency Conversion** — Live exchange rates for your home currency
- 📸 **Destination Photos** — Beautiful travel photos via Unsplash API
- 📥 **Download Itinerary** — Save your travel plan as a text file
- 👥 **Traveler Customization** — Solo, Couple, Family, or Group options
- 🎯 **Travel Style Selection** — Culture, Food, Adventure, Shopping, and more

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.13 |
| UI Framework | Streamlit |
| LLM | LLaMA 3.3 70B (via Groq API) |
| Weather | WeatherAPI.com |
| Places | OpenStreetMap (Overpass API) |
| Currency | ExchangeRate-API |
| Photos | Unsplash API |
| Config | python-dotenv |

---

## 🔑 API Keys — Where to Get Them

| API | Website | Cost | Used For |
|-----|---------|------|----------|
| Groq | console.groq.com | ✅ Free | LLM itinerary generation |
| WeatherAPI | weatherapi.com | ✅ Free | Live weather data |
| ExchangeRate | exchangerate-api.com | ✅ Free | Currency conversion |
| Unsplash | unsplash.com/developers | ✅ Free | Destination photos |
| OpenStreetMap | No key needed | ✅ Free | Tourist attractions |

---

## 🚀 How to Use

1. Enter your **destination city** in the sidebar (e.g. Tokyo, Paris, Dubai)
2. Select **number of days** using the slider (1–14)
3. Choose your **budget level** (Budget / Mid-range / Luxury)
4. Select your **travel style** (Culture, Food, Adventure, etc.)
5. Choose **traveler type** (Solo, Couple, Family, Group)
6. Optionally enter your **home currency** for exchange rates
7. Click **"🚀 Generate My Itinerary"**
8. View your complete day-by-day itinerary with photos, weather, and attractions
9. Download your itinerary using the **Download** button

---

## 🔄 System Workflow

```
User Input → Input Validation → API Data Fetch (Weather + Places + Currency + Photos)
     ↓
Prompt Builder (injects all context into LLM prompt)
     ↓
Groq API (LLaMA 3.3 70B generates the itinerary)
     ↓
Streamlit renders the complete travel plan
```

---

## 📦 Requirements

```
streamlit==1.35.0
requests==2.31.0
python-dotenv==1.0.1
groq
```

Submitted to: Atif Luqman | Artificial Intelligence Course

</div>
