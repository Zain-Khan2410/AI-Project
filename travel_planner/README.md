# ✈️ AI-Powered Travel Planner

> **Course:** Artificial Intelligence (AI) — End Semester Project  
> **Team:** Zamin, Atta & Zain  
> **Instructor:** Atif Luqman

---

## What This Does

An AI-powered web app that generates personalised day-by-day travel itineraries based on your destination, budget, travel style, and trip duration. Powered by OpenAI's GPT models, with optional real-time weather, top attractions, and currency data.

---

## Quick Start

### 1. Clone / Download the project
```bash
cd travel_planner
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API keys
```bash
cp .env.example .env
```
Open `.env` in any text editor and paste your API keys.

**Getting the OpenAI key (required):**
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy it into `.env` as `OPENAI_API_KEY=sk-...`

**Getting WeatherAPI key (optional but recommended):**
1. Go to https://www.weatherapi.com and sign up free
2. Copy the key from the dashboard into `.env`

**Getting Foursquare key (optional):**
1. Go to https://foursquare.com/developer and create an app
2. Copy the API key into `.env`

### 5. Run the app
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## Project Structure

```
travel_planner/
├── app.py                  ← Streamlit UI (main entry point)
├── planner/
│   ├── llm.py              ← LLM API calls & prompt engineering
│   ├── weather.py          ← WeatherAPI.com integration
│   ├── places.py           ← Foursquare Places API
│   └── currency.py         ← Exchange rate API
├── utils/
│   ├── formatters.py       ← Output formatting helpers
│   └── validators.py       ← Input validation
├── .env                    ← Your API keys (never share this)
├── .env.example            ← Template for .env
├── requirements.txt        ← Python dependencies
└── README.md
```

---

## How It Works

1. **User fills inputs** in the sidebar: city, days, budget, interests
2. **Validators check** inputs for errors
3. **API calls** fetch live weather, top places, and exchange rate (in parallel)
4. **Prompt Builder** assembles a detailed, structured prompt injecting all context
5. **OpenAI API** receives the prompt and generates a Markdown itinerary
6. **Streamlit renders** the result with a download button

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| UI Framework | Streamlit |
| LLM | OpenAI GPT-4o-mini |
| Weather | WeatherAPI.com |
| Places | Foursquare Places API v3 |
| Currency | ExchangeRate-API |
| Config | python-dotenv |

---

## Future Extensions (for higher marks)

- [ ] Save itineraries to a database (SQLite)
- [ ] User login & history (Streamlit Auth)
- [ ] Google Maps embed for each day's route
- [ ] PDF export of the itinerary
- [ ] Multi-city trip planning
- [ ] Flight & hotel price estimates via Amadeus API
