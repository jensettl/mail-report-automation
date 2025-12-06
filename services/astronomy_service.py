import logging
import requests

import config

logger = logging.getLogger(__name__)

def get_astronomy_data(query: str, date: str):
    """ Fetch astronomy data from the WeatherAPI. """
    
    try:
        url = config.ASTRONOMY_URL
        params = {
            "key": config.WEATHER_API_KEY,
            "q": config.QUERY,
            "dt": config.TODAY,
        }
        astronomy_data = requests.get(url, params).json()
        
        if not astronomy_data:
            logger.warning("No astronomy data returned from API")
            return None
        
        logger.debug(f"Astronomy data fetched successfully for {query} on {date}")
        return astronomy_data
    except Exception as e:
        logger.error(f"Failed to fetch astronomy data: {e}", exc_info=True)
        return None
    