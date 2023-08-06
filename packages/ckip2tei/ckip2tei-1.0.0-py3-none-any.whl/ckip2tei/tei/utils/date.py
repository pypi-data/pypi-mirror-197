from datetime import datetime


def get_year(timestamp: str | int) -> str:
    """The get_year function converts `timestamp` to a year string.

    Args:
        timestamp (str | int): the timestamp to be converted
    Returns:
        a str
    """
    timestamp = int(timestamp) if isinstance(timestamp, str) else timestamp
    date_time = datetime.fromtimestamp(timestamp)
    return str(date_time.year)
