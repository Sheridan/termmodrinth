import datetime

def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def convert_isoformat_date(strdate):
    return datetime.datetime.strptime(strdate, "%Y-%m-%dT%H:%M:%S.%fZ")
