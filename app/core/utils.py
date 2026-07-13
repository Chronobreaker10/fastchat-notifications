from datetime import datetime, timedelta, timezone


def get_msc_dt(dt: datetime) -> datetime:
    moscow_tz = timezone(timedelta(hours=3))
    return dt.astimezone(moscow_tz)
