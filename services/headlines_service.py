# Stock News Service

import logging
import requests

import config

logger = logging.getLogger(__name__)

def get_headline_data():
    """ Fetch top headlines from News API """
    try:
        params = {
            "apiKey": config.HEADLINES_API_KEY,
            "country": config.HEADLINES_COUNTRY,
            "category": config.HEADLINES_CATEGORY
        }
        
        response = requests.get(config.HEADLINES_URL, params=params)
        data = response.json()
        
        if not data:
            logger.warning("No headline data returned from API")
            return None
        
        headlines = data["articles"][0:3]
        logger.debug(f"Fetched {len(headlines)} headlines")
        return headlines
    except Exception as e:
        logger.error(f"Failed to fetch headlines: {e}", exc_info=True)
        return None