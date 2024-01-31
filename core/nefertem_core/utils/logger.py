"""
Logger module.
"""
import logging

# LOGGER
LOGGER = logging.getLogger("nefertem")
LOGGER.setLevel(logging.INFO)


# Create console handler set level to INFO and add filter
class LogFilter(logging.Filter):
    """
    Logs filter.
    """

    def filter(self, record):
        """
        Filter for nefertem logs.
        """
        return record.name == "nefertem"


ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.addFilter(LogFilter())

# Create formatter and add to console handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

# Add console handler to logger
LOGGER.addHandler(ch)
