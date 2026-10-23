import requests
from Weather_Agent.config import GEOCODE_URL, FORECAST_URL, WEATHER_REQUEST_TIMEOUT

WEATHER_CODES: dict[int, str] = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "rain showers",
    95: "thunderstorm",
    96: "thunderstorm with hail",
}

def lookup_weather(location:str)->str:
    
    geo = requests.get(
        GEOCODE_URL,
        params={"name":location,"count":1},
        timeout=WEATHER_REQUEST_TIMEOUT,
    )
    geo.raise_for_status()
    
    matches = geo.json().get("results")
    if not matches:
        return f"We couldn't find a place called {location}"
    
    place = matches[0]
    lat, lon = place["latitude"], place["longitude"]
    
    label = ", ".join(
        part for part in (place["name"],place["country"]) if part
    )
    
    forecast = requests.get(
        FORECAST_URL,
        params={"latitude":lat,"longitude":lon,"current":"temperature_2m,weather_code,wind_speed_10m"},
        timeout=WEATHER_REQUEST_TIMEOUT
    )
    forecast.raise_for_status()
    
    current = forecast.json().get("current")
    
    temperature = current.get("temperature_2m")
    weather_code = current.get("weather_code")
    wind_speed = current.get("wind_speed_10m")
    sky = WEATHER_CODES.get(weather_code,f"weather_code: {weather_code}")
    
    wind_note = f"{wind_speed} km/h" if wind_speed else ""
    return f"The current temperature in {label} is {temperature}°C, the sky is {sky} and the wind speed is {wind_note}."

    # print(geo.json().get("results")[0])
    # print(label)
    # print(forecast.json())
    
print(lookup_weather("London"))