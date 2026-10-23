from dotenv import load_dotenv
load_dotenv()
import os

GEOCODE_URL = os.getenv("GEOCODE_URL","https://geocoding-api.open-meteo.com/v1/search")
FORECAST_URL = os.getenv("FORECAST_URL","https://api.open-meteo.com/v1/forecast")

