import threading


class Singleton:
  _instance = None
  _lock = threading.Lock()

  def __new__(cls):
    if not cls._instance:
      with cls._lock:
        if not cls._instance:
          cls._instance = super().__new__(cls)
    return cls._instance
