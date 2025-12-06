# Data cleaning and transformation functions

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def clean_weather_data(weather_data) -> dict | None:
    """   Clean and structure weather data from the API response. """
    
    if not weather_data or "location" not in weather_data:
        logger.warning("Invalid weather data structure")
        return None
    
    try:
        cleaned = {
            "location": weather_data["location"]["name"],
            "country": weather_data["location"]["country"],
            "temperature": weather_data["current"]["temp_c"],
            "humidity": weather_data["current"]["humidity"],
            "wind_speed": weather_data["current"]["wind_kph"],
            "condition": weather_data["current"]["condition"]["text"],
            "last_updated": parse_timestamp(weather_data["current"]["last_updated"])
        }
        logger.debug("Weather data cleaned successfully")
        return cleaned
    except KeyError as e:
        logger.error(f"Missing key in weather data: {e}", exc_info=True)
        return None

def clean_astronomy_data(astronomy_data) -> dict | None:
    """    Clean and structure astronomy data from the API response. """
    
    if not astronomy_data or "location" not in astronomy_data:
        logger.warning("Invalid astronomy data structure")
        return None
    
    try:
        cleaned = {
            "sunrise": astronomy_data["astronomy"]["astro"]["sunrise"],
            "sunset": astronomy_data["astronomy"]["astro"]["sunset"],
            "moonrise": astronomy_data["astronomy"]["astro"]["moonrise"],
            "moonset": astronomy_data["astronomy"]["astro"]["moonset"]
        }
        logger.debug("Astronomy data cleaned successfully")
        return cleaned
    except KeyError as e:
        logger.error(f"Missing key in astronomy data: {e}", exc_info=True)
        return None
    

def clean_stock_data(stock_data) -> dict | None:
    """    Clean and structure stock data from the API response. """
    
    if not stock_data:
        logger.warning("No stock data provided")
        return None
    
    logger.debug("Stock data cleaned successfully")
    return stock_data   # for future data cleaning
    

def clean_headlines_data(headlines_data) -> list | None:
    """    Clean and structure headlines data from the API response."""
    
    if not headlines_data:
        logger.warning("No headlines data provided")
        return None
    
    try:
        cleaned = []
        for article in headlines_data:
            cleaned.append({
                "title": article.get("title", "No title"),
                "description": article.get("description", "No description"),
                "url": article.get("url", "#"),
                "published_at": article.get("publishedAt", "No date")
            })
        logger.debug(f"Cleaned {len(cleaned)} headlines")
        return cleaned
    except Exception as e:
        logger.error(f"Error cleaning headlines data: {e}", exc_info=True)
        return None
    cleaned_data = []
    for article in headlines_data:
        cleaned_article = {
            "source": article["source"].get("name", "No source available"),
            "author": article["author"],
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "published_at": parse_timestamp(article["publishedAt"])
        }
        cleaned_data.append(cleaned_article)
    
    return cleaned_data
    

def parse_timestamp(timestamp_str) -> str:
    """    
    Convert a timestamp string into a readable datetime format.
    
    :return: str, formatted timestamp like 'Feb 9, 2025 at 10:30 AM'
    """
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except ValueError:
        return timestamp_str  # Return the original string if parsing fails
