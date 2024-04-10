import datetime
import hashlib

def sizeof_fmt(num, suffix="B"):
  for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
    if abs(num) < 1024.0:
      return f"{num:3.1f}{unit}{suffix}"
    num /= 1024.0
  return f"{num:.1f}Yi{suffix}"

def convert_isoformat_date(strdate):
  return datetime.datetime.strptime(strdate, "%Y-%m-%dT%H:%M:%S.%fZ")

def get_file_sha512(filename):
  h  = hashlib.sha512()
  b  = bytearray(128*1024)
  mv = memoryview(b)
  with open(filename, 'rb', buffering=0) as f:
    while n := f.readinto(mv):
      h.update(mv[:n])
  return h.hexdigest()
