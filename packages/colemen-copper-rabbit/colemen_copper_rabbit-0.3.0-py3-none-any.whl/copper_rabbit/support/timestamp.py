
from datetime import datetime
from datetime import timezone

def format_timestamp(ts,force_timestamp=True):
    if ts is None:
        if force_timestamp is True:
            ts = round(datetime.now(tz=timezone.utc).timestamp())
    if isinstance(ts,(float)):
        ts = round(ts)
    return ts


def current_unix_timestamp():
    return round(datetime.now(tz=timezone.utc).timestamp())