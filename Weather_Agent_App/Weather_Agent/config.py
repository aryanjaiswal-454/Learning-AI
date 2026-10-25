from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
import os

GEOCODE_URL = os.getenv("GEOCODE_URL","https://geocoding-api.open-meteo.com/v1/search")
FORECAST_URL = os.getenv("FORECAST_URL","https://api.open-meteo.com/v1/forecast")

WEATHER_REQUEST_TIMEOUT = int(os.getenv("WEATHER_REQUEST_TIMEOUT","10"))

PROJECT_ROOT = Path(__file__).resolve().parent
PROMPTS_DIR = PROJECT_ROOT / "prompt_templates"

MAX_TURNS = int(os.getenv("MAX_TURNS","10"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS","4096"))