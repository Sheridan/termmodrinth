import os
import threading

from termmodrinth.singleton import Singleton
from termmodrinth.config import Config
from termmodrinth.logger import Logger
from termmodrinth.modrinth import project_types

class Cleaner(Singleton):
  projects = {
      'mod': [],
      'resourcepack': [],
      'shader': []
    }

  files = {
      'mod': [],
      'resourcepack': [],
      'shader': []
    }

  def appenSlug(self, project_type, slug):
    with threading.Lock():
      if slug not in self.projects[project_type]:
        self.projects[project_type].append(slug)
        return True
      return False
    raise Exception("Wrong lock")

  def appenFile(self, project_type, filename):
    with threading.Lock():
      if filename not in self.files[project_type]:
        self.files[project_type].append(filename)
        return True
      return False
    raise Exception("Wrong lock")

  def cleanup(self):
    for project_type in project_types.keys():
      Logger().delimiter("|", "Cleaning up {}s".format(project_type))
      path = Config().active_path(project_type)
      for f in os.listdir(path):
        if f.endswith(project_types[project_type]['extention']):
          if f not in self.files[project_type]:
            filename = "{}/{}".format(path, f)
            Logger().msg("Removing {}".format(filename), "red")
            os.remove(filename)

  def printStats(self):
    Logger().delimiter("=", "Stats")
    for project_type in project_types.keys():
      Logger().msg("{}s. Requested: {}; Downloaded: {}".format(project_type.capitalize(), len(Config().projects(project_type)), len(self.projects[project_type])), "light_green")
