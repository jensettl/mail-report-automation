# Logic for fetching and handling weather data

import logging
import requests

import config

logger = logging.getLogger(__name__)

def get_weather_data(query: str) -> dict | None :
    """   Fetch weather data from the WeatherAPI. """
    
    try:
        url = config.WEATHER_URL
        params = {
            "key": config.WEATHER_API_KEY,
            "q": config.QUERY,
        }
        weather_data = requests.get(url, params).json()
        
        if not weather_data:
            logger.warning("No weather data returned from API")
            return None
        
        logger.debug(f"Weather data fetched successfully for {query}")
        return weather_data
    except Exception as e:
        logger.error(f"Failed to fetch weather data: {e}", exc_info=True)
        return None
      