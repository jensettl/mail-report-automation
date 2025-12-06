from . import headlines_service, stocks_service, weather_service, astronomy_service

"""
utils package for mail-report-automation.

Expose submodules so you can do:
    from mail_report_automation.utils.data_cleaner import <name>

Adjust __all__ to control the public API.
"""

__all__ = ["headlines_service", "stocks_service", "weather_service", "astronomy_service"]
__version__ = "0.1.0"