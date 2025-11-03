from datetime import datetime


class DatetimeProvider:
    """Provides current datetime for easy mocking in tests."""

    @staticmethod
    def now() -> datetime:
        """Get current datetime in UTC."""
        return datetime.utcnow()

