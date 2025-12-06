# Entry point of your application

import logging
from pathlib import Path

from services import weather_service, astronomy_service, stocks_service, headlines_service
from utils import data_cleaner, email_builder

import config

# Configure logging at module startup (runs once)
def _configure_logging():
    """Configure logging for the entire application."""
    today = config.TODAY
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f"log-{today}.log"),
            logging.StreamHandler()
        ]
    )

_configure_logging()
logger = logging.getLogger(__name__)

TODAY = config.TODAY
TICKER_LIST = config.TICKER_LIST


def main():
    # Fetch data 
   
    weather_data = weather_service.get_weather_data(config.QUERY)
    logger.info("Weather Data collected!")
    
    astronomy_data = astronomy_service.get_astronomy_data(config.QUERY, TODAY)
    logger.info("Astronomy Data collected!")
    
    stock_data = stocks_service.get_stock_info(TICKER_LIST)
    logger.info("Stock Data collected!")
    
    headlines_data = headlines_service.get_headline_data()
    logger.info("Headlines Data collected!")
    
    
    # Clean and structure data
    cleaned_weather = data_cleaner.clean_weather_data(weather_data)
    cleaned_astronomy = data_cleaner.clean_astronomy_data(astronomy_data)
    cleaned_stock = data_cleaner.clean_stock_data(stock_data)
    cleaned_headlines = data_cleaner.clean_headlines_data(headlines_data)
    logger.info("Cleaning Data was successfull.")
    
    # Build email body
    email_body = email_builder.build_email_body(cleaned_weather, cleaned_astronomy, cleaned_stock, cleaned_headlines)
    logger.info("Building Email was successfull.")
    
    # Send email
    email_builder.sendEmail(config.EMAIL_FROM, config.EMAIL_TO, "Daily Report", email_body)
    
if __name__ == "__main__":
    main()