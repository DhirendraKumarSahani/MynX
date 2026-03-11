from langchain_core.tools import tool
import requests
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

@tool
def get_weather(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    try:
        api_key = settings.OPENWEATHERMAP_API_KEY

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=10)

        data = response.json()

        if response.status_code != 200:
            return f"Weather API error : {data}"
        
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]

        return f"The weather in {city} is {weather} with temperature {temperature}°C"
    
    except Exception as e:
        logger.error(f"Weather tool failed : {str(e)}")

        return "Weather service unavailable"