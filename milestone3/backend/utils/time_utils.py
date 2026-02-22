import time
from datetime import datetime, timezone


# --------------------------------------------
# Current Time Helpers
# --------------------------------------------

def now_timestamp() -> float:
    """
    Returns current UTC timestamp (float).
    """
    return time.time()


def now_datetime() -> datetime:
    """
    Returns current UTC datetime object.
    """
    return datetime.now(timezone.utc)


def now_iso() -> str:
    """
    Returns ISO-8601 formatted UTC time string.
    """
    return now_datetime().isoformat()


# --------------------------------------------
# Expiry / Timeout Utilities
# --------------------------------------------

def is_expired(
    past_timestamp: float,
    timeout_seconds: float
) -> bool:
    """
    Returns True if timeout exceeded.
    """
    return (now_timestamp() - past_timestamp) > timeout_seconds


def seconds_since(past_timestamp: float) -> float:
    """
    Returns seconds passed since timestamp.
    """
    return now_timestamp() - past_timestamp


def within_time_window(
    past_timestamp: float,
    window_seconds: float
) -> bool:
    """
    Returns True if timestamp is inside time window.
    """
    return seconds_since(past_timestamp) <= window_seconds


# --------------------------------------------
# Human Readable Formatting
# --------------------------------------------

def format_duration(seconds: float) -> str:
    """
    Converts seconds to human-readable duration.
    Example: 125 -> '2m 5s'
    """
    seconds = int(seconds)

    minutes = seconds // 60
    remaining = seconds % 60

    if minutes > 0:
        return f"{minutes}m {remaining}s"

    return f"{remaining}s"