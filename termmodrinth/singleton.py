
class Singleton(object):
  _instance = None

  def __new__(cls):
    if not cls._instance:
      cls._instance = super().__new__(cls)
      cls._instance._new()
      # print(cls)
    return cls._instance

  def _new(self):
    pass
