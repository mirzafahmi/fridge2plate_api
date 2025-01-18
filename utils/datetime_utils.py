from datetime import datetime, timedelta
from typing import Optional


class DateTimeUtils:
    @staticmethod
    def parse_iso_datetime(date_str: Optional[str]) -> Optional[datetime]:
        """
        Converts an ISO 8601 formatted string to a datetime object.
        Returns None if the input is None or invalid.
        """
        if date_str is None:
            return None
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            raise ValueError(f"Invalid datetime format: {date_str}")

    @staticmethod
    def is_valid_datetime(date_str: Optional[str]) -> bool:
        """
        Checks if the input string is a valid ISO 8601 datetime string.
        """
        try:
            if date_str is None:
                return False
            datetime.fromisoformat(date_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def assert_is_none_or_datetime(date_str: Optional[str]) -> None:
        """
        Asserts that the input is either None or a valid ISO 8601 datetime string.
        """
        if date_str is not None and not DateTimeUtils.is_valid_datetime(date_str):
            raise AssertionError(f"{date_str} is not None or a valid ISO datetime.")
