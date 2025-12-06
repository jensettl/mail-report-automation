from . import data_cleaner, email_builder

"""
utils package for mail-report-automation.

Expose submodules so you can do:
    from mail_report_automation.utils.data_cleaner import <name>

Adjust __all__ to control the public API.
"""

__all__ = ["data_cleaner", "email_builder"]
__version__ = "0.1.0"