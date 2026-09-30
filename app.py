import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SkyCast Weather",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DARK THEME
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b1220;
    color: #f1f5f9;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Normal text */
p, span, label, div {
    color: #e2e8f0;
}

/* Headings */
h1 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

h2 {
    color: #f8fafc !important;
    font-weight: 750 !important;
}

h3 {
    color: #e2e8f0 !important;
}

/* Caption */
.stCaption, small {
    color: #94a3b8 !important;
}

/* Input */
div[data-baseweb="input"] {
    background-color: #111c2e;
    border: 1px solid #26364d;
    border-radius: 12px;
}

div[data-baseweb="input"] input {
    color: #ffffff !important;
    background-color: transparent !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #64748b !important;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 46px;
    border-radius: 12px;
    border: 1px solid #14b8a6;
    background-color: #0f766e;
    color: white !important;
    font-size: 16px;
    font-weight: 700;
}

.stButton > button:hover {
    background-color: #14b8a6;
    border-color: #2dd4bf;
    color: white !important;
}

/* Metrics */
div[data-testid="stMetric"] {
    background-color: #111c2e;
    border: 1px solid #26364d;
    border-radius: 16px;
    padding: 18px;
}

div[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 800;
}

div[data-testid="stMetricDelta"] {
    color: #5eead4 !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid #26364d;
    border-radius: 12px;
}

/* Expander */
div[data-testid="stExpander"] {
    background-color: #111c2e;
    border: 1px solid #26364d;
    border-radius: 14px;
}

div[data-testid="stExpander"] summary {
    color: #ffffff !important;
}

/* Divider */
hr {
    border-color: #26364d !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #080f1c;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Selectbox */
div[data-baseweb="select"] {
    background-color: #111c2e;
}

/* Alert boxes */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Charts */
div[data-testid="stVegaLiteChart"],
div[data-testid="stArrowVegaLiteChart"] {
    background-color: #111c2e;
    border-radius: 15px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCTIONS
# =========================================================

def weather_icon(weather):

    weather = weather.lower()

    if "thunder" in weather:
        return "⛈️"

    if "snow" in weather:
        return "❄️"

    if "rain" in weather:
        return "🌧️"

    if "drizzle" in weather:
        return "🌦️"

    if "fog" in weather:
        return "🌫️"

    if "overcast" in weather:
        return "☁️"

    if "cloud" in weather:
        return "⛅"

    if "clear" in weather:
        return "☀️"

    return "🌤️"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🌤️ SkyCast")

    st.caption("Weather Forecasting Dashboard")

    st.divider()

    st.subheader("⚙️ Dashboard")

    st.write("🌍 Real-time Weather")
    st.write("📅 7-Day Forecast")
    st.write("📊 Weather Analytics")

    st.divider()

    st.subheader("🛠️ Technology")

    st.write("🐍 Python")
    st.write("⚡ FastAPI Backend")
    st.write("🎨 Streamlit")
    st.write("🌐 Open-Meteo API")

    st.divider()

    st.caption("SkyCast Weather Forecast")
    st.caption("Powered by Python + Open-Meteo")


# =========================================================
# HEADER
# =========================================================

st.title("🌤️ SkyCast Weather Forecast")

st.write(
    "Real-time weather information with a detailed 7-day forecast."
)

# =========================================================
# SEARCH
# =========================================================

st.subheader("🔍 Search Location")

col1, col2 = st.columns([5, 1])

with col1:

    city = st.text_input(
        "City",
        placeholder="Enter city name e.g. Delhi, Mumbai, Patna...",
        label_visibility="collapsed"
    )

with col2:

    search = st.button(
        "🔎 Search",
        use_container_width=True
    )


# =========================================================
# WEATHER API
# =========================================================

if search:

    if not city.strip():

        st.warning("⚠️ Please enter a city name.")

    else:

        try:

            with st.spinner("🌐 Fetching latest weather data..."):

                # Streamlit Cloud compatible:
                # Fetch location directly from Open-Meteo Geocoding API
                geo_response = requests.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={
                        "name": city.strip(),
                        "count": 1,
                        "language": "en",
                        "format": "json"
                    },
                    timeout=20
                )

                if geo_response.status_code != 200:
                    st.error("❌ Unable to connect to the weather service.")
                    st.stop()

                geo_data = geo_response.json()

                if "results" not in geo_data or not geo_data["results"]:
                    st.error(f"❌ City '{city.strip()}' not found.")
                    st.stop()

                place = geo_data["results"][0]
                latitude = place["latitude"]
                longitude = place["longitude"]

                response = requests.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
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
                    },
                    timeout=20
                )

                # Convert Open-Meteo response to the same structure
                # already used by this frontend.
                if response.status_code == 200:
                    api_data = response.json()

                    weather_descriptions = {
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

                    def weather_description(code):
                        return weather_descriptions.get(code, "Unknown Weather")

                    current = api_data["current"]
                    daily = api_data["daily"]

                    data = {
                        "location": {
                            "city": place["name"],
                            "country": place.get("country", ""),
                            "latitude": latitude,
                            "longitude": longitude
                        },
                        "current_weather": {
                            "temperature": current["temperature_2m"],
                            "humidity": current["relative_humidity_2m"],
                            "feels_like": current["apparent_temperature"],
                            "precipitation": current["precipitation"],
                            "weather": weather_description(current["weather_code"]),
                            "wind_speed": current["wind_speed_10m"],
                            "pressure": current["surface_pressure"]
                        },
                        "forecast": [
                            {
                                "date": daily["time"][i],
                                "weather": weather_description(daily["weather_code"][i]),
                                "weather_code": daily["weather_code"][i],
                                "max_temperature": daily["temperature_2m_max"][i],
                                "min_temperature": daily["temperature_2m_min"][i],
                                "max_feels_like": daily["apparent_temperature_max"][i],
                                "min_feels_like": daily["apparent_temperature_min"][i],
                                "precipitation": daily["precipitation_sum"][i],
                                "rain": daily["rain_sum"][i],
                                "max_wind_speed": daily["wind_speed_10m_max"][i]
                            }
                            for i in range(len(daily["time"]))
                        ]
                    }


                else:
                    st.error("❌ Unable to fetch weather data.")
                    st.stop()

            # -------------------------------------------------
            # ERROR
            # -------------------------------------------------

            if response.status_code != 200:

                st.error("❌ Unable to fetch weather data.")

            else:

                # Weather data was already converted above into
                # the same structure used by the dashboard.
                location = data["location"]
                current = data["current_weather"]
                forecast = data["forecast"]

                # =================================================
                # LOCATION
                # =================================================

                st.divider()

                st.subheader(
                    f"📍 {location['city']}, {location['country']}"
                )

                st.caption(
                    datetime.now().strftime(
                        "%A, %d %B %Y"
                    )
                )

                # =================================================
                # CURRENT WEATHER
                # =================================================

                st.divider()

                st.subheader("🌡️ Current Weather")

                current_col1, current_col2 = st.columns(
                    [2, 3]
                )

                # -------------------------------------------------
                # MAIN TEMPERATURE
                # -------------------------------------------------

                with current_col1:

                    st.metric(
                        "Current Temperature",
                        f"{current['temperature']} °C"
                    )

                    st.markdown(
                        f"## {weather_icon(current['weather'])} "
                        f"{current['weather']}"
                    )

                    st.write(
                        f"Feels like **{current['feels_like']} °C**"
                    )

                # -------------------------------------------------
                # WEATHER DETAILS
                # -------------------------------------------------

                with current_col2:

                    m1, m2 = st.columns(2)

                    with m1:

                        st.metric(
                            "💧 Humidity",
                            f"{current['humidity']} %"
                        )

                        st.metric(
                            "🌧️ Precipitation",
                            f"{current['precipitation']} mm"
                        )

                    with m2:

                        st.metric(
                            "💨 Wind Speed",
                            f"{current['wind_speed']} km/h"
                        )

                        st.metric(
                            "🔵 Pressure",
                            f"{current['pressure']} hPa"
                        )

                # =================================================
                # 7 DAY FORECAST
                # =================================================

                st.divider()

                st.subheader("📅 7-Day Forecast")

                forecast_columns = st.columns(7)

                for i, day in enumerate(forecast):

                    date = datetime.strptime(
                        day["date"],
                        "%Y-%m-%d"
                    )

                    if i == 0:
                        day_name = "Today"
                    else:
                        day_name = date.strftime("%a")

                    with forecast_columns[i]:

                        st.markdown(
                            f"### {day_name}"
                        )

                        st.caption(
                            date.strftime("%d %b")
                        )

                        st.markdown(
                            f"# {weather_icon(day['weather'])}"
                        )

                        st.write(
                            f"**{round(day['max_temperature'])}°C**"
                        )

                        st.caption(
                            f"Low: {round(day['min_temperature'])}°C"
                        )

                        st.caption(
                            day["weather"]
                        )

                # =================================================
                # DETAILED TABLE
                # =================================================

                st.divider()

                st.subheader("📊 Detailed Forecast")

                forecast_df = pd.DataFrame(
                    forecast
                )

                display_df = forecast_df[
                    [
                        "date",
                        "weather",
                        "max_temperature",
                        "min_temperature",
                        "precipitation",
                        "rain",
                        "max_wind_speed"
                    ]
                ].copy()

                display_df.columns = [
                    "Date",
                    "Weather",
                    "Max Temp °C",
                    "Min Temp °C",
                    "Precipitation mm",
                    "Rain mm",
                    "Max Wind km/h"
                ]

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )

                # =================================================
                # ANALYTICS
                # =================================================

                st.divider()

                st.subheader("📈 Weather Analytics")

                chart_col1, chart_col2 = st.columns(2)

                # -------------------------------------------------
                # TEMPERATURE CHART
                # -------------------------------------------------

                with chart_col1:

                    st.write(
                        "🌡️ Temperature Trend"
                    )

                    temperature_chart = forecast_df[
                        [
                            "date",
                            "max_temperature",
                            "min_temperature"
                        ]
                    ].copy()

                    temperature_chart = (
                        temperature_chart
                        .set_index("date")
                    )

                    temperature_chart.columns = [
                        "Maximum Temperature",
                        "Minimum Temperature"
                    ]

                    st.line_chart(
                        temperature_chart
                    )

                # -------------------------------------------------
                # RAIN CHART
                # -------------------------------------------------

                with chart_col2:

                    st.write(
                        "🌧️ Rainfall Forecast"
                    )

                    rain_chart = forecast_df[
                        [
                            "date",
                            "rain"
                        ]
                    ].copy()

                    rain_chart = (
                        rain_chart
                        .set_index("date")
                    )

                    rain_chart.columns = [
                        "Rainfall (mm)"
                    ]

                    st.bar_chart(
                        rain_chart
                    )

                # =================================================
                # SUMMARY
                # =================================================

                st.divider()

                st.subheader("📋 7-Day Weather Summary")

                total_rain = forecast_df[
                    "rain"
                ].sum()

                highest_temp = forecast_df[
                    "max_temperature"
                ].max()

                lowest_temp = forecast_df[
                    "min_temperature"
                ].min()

                highest_wind = forecast_df[
                    "max_wind_speed"
                ].max()

                s1, s2, s3, s4 = st.columns(4)

                with s1:

                    st.metric(
                        "🌡️ Highest Temperature",
                        f"{round(highest_temp)} °C"
                    )

                with s2:

                    st.metric(
                        "❄️ Lowest Temperature",
                        f"{round(lowest_temp)} °C"
                    )

                with s3:

                    st.metric(
                        "🌧️ Total Rain",
                        f"{round(total_rain, 1)} mm"
                    )

                with s4:

                    st.metric(
                        "💨 Max Wind",
                        f"{round(highest_wind, 1)} km/h"
                    )

                # =================================================
                # RAW DATA
                # =================================================

                with st.expander(
                    "🔎 View Raw Weather Data"
                ):

                    st.json(data)

                # =================================================
                # FOOTER
                # =================================================

                st.divider()

                st.caption(
                    "🌤️ SkyCast Weather Forecast  |  "
                    "Python + Streamlit + Open-Meteo"
                )

        # =========================================================
        # CONNECTION ERROR
        # =========================================================

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Unable to connect to Open-Meteo."
            )

            st.info(
                "Please check your internet connection and try again."
            )

        # =========================================================
        # TIMEOUT
        # =========================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏳ Weather API is taking too long. "
                "Please try again."
            )

        # =========================================================
        # OTHER ERROR
        # =========================================================

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )
