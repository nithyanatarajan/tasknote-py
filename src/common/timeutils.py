from datetime import UTC, datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo('Asia/Kolkata')


def now_ist():
    return datetime.now(IST)


def now_utc():
    return datetime.now(UTC)
