from datetime import UTC, datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo('Asia/Kolkata')


def now_ist():
    return datetime.now(IST)


def now_utc():
    return datetime.now(UTC)


def to_isoz(dt: datetime) -> str:
    """
    Convert *aware* datetime → ISO8601 string that ends in “Z”
    (i.e. +00:00 replaced with Z).
    """
    return dt.astimezone(UTC).isoformat(timespec='microseconds').replace('+00:00', 'Z')
