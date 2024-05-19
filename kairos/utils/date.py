from datetime import datetime, timezone


def now(tz: timezone = timezone.utc) -> datetime:
    return datetime.now(tz=tz)
