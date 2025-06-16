import logging
import os
import time
from datetime import datetime, timezone


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt="%Y-%m-%dT%H:%M:%S.%f%z"):
        # Use datetime to format time with timezone offset
        ct = datetime.fromtimestamp(record.created, tz=timezone.utc)
        if datefmt:
            return ct.strftime(datefmt)
        return ct.isoformat()

    def format(self, record):
        # Set the asctime attribute by calling formatTime
        record.asctime = self.formatTime(record, self.datefmt)

        # Get the absolute file path of the calling function
        abs_file_path = os.path.abspath(record.pathname)

        # Format the log message with all required information
        parent_msg = super().format(record)

        # Build the log message
        msg_to_print = (
            f"{record.asctime} | {record.levelname} | {abs_file_path} | "
            f"{record.funcName} | {record.lineno} | {parent_msg}"
        )
        return msg_to_print


# Set the time to UTC
logging.Formatter.converter = time.gmtime

# Use the custom formatter with a specified date format (RFC 3339-like with timezone offset)
formatter = CustomFormatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S.%f%z")

# Configure the logger with a stream handler
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)