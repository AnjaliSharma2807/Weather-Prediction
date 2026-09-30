from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime

app = FastAPI(
    title="Weather Forecasting API",
    description="Free Weather Forecasting API using Open-Meteo",
    version="1.0.0"
)


# ---------------------------------------------------------
# CITY TO COORDINATES
# ---------------------------------------------------------

def get_coordinates(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Unable to connect to weather service."
        )

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found."
        )

    result = data["results"][0]

    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "name": result["name"],
        "country": result.get("country", "")
    }


# ---------------------------------------------------------
# WEATHER DESCRIPTION
# ---------------------------------------------------------

def weather_description(code):

    descriptions = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        80: "Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Hail",
        99: "Thunderstorm with Heavy Hail"
    }

    return descriptions.get(code, "Unknown Weather")


# ---------------------------------------------------------
# CURRENT WEATHER + FORECAST
# ---------------------------------------------------------

@app.get("/weather")
def get_weather(city: str):

    location = get_coordinates(city)

    latitude = location["latitude"]
    longitude = location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
            "surface_pressure"
        ],

        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "precipitation_sum",
            "rain_sum",
            "wind_speed_10m_max"
        ],

        "forecast_days": 7,

        "timezone": "auto"
    }

    response = requests.get(
        weather_url,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Unable to fetch weather data."
        )

    data = response.json()

    current = data["current"]
    daily = data["daily"]

    forecast = []

    for i in range(len(daily["time"])):

        forecast.append({
            "date": daily["time"][i],

            "weather": weather_description(
                daily["weather_code"][i]
            ),

            "weather_code": daily["weather_code"][i],

            "max_temperature": daily[
                "temperature_2m_max"
            ][i],

            "min_temperature": daily[
                "temperature_2m_min"
            ][i],

            "max_feels_like": daily[
                "apparent_temperature_max"
            ][i],

            "min_feels_like": daily[
                "apparent_temperature_min"
            ][i],

            "precipitation": daily[
                "precipitation_sum"
            ][i],

            "rain": daily[
                "rain_sum"
            ][i],

            "max_wind_speed": daily[
                "wind_speed_10m_max"
            ][i]
        })

    return {
        "location": {
            "city": location["name"],
            "country": location["country"],
            "latitude": latitude,
            "longitude": longitude
        },

        "current_weather": {

            "temperature": current[
                "temperature_2m"
            ],

            "humidity": current[
                "relative_humidity_2m"
            ],

            "feels_like": current[
                "apparent_temperature"
            ],

            "precipitation": current[
                "precipitation"
            ],

            "weather": weather_description(
                current["weather_code"]
            ),

            "wind_speed": current[
                "wind_speed_10m"
            ],

            "pressure": current[
                "surface_pressure"
            ]
        },

        "forecast": forecast,

        "generated_at": datetime.now().isoformat()
    }


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Weather Forecasting API is running!",
        "endpoint": "/weather?city=Delhi"
    }