import os
import threading

from termmodrinth.singleton import Singleton
from termmodrinth.config import Config
from termmodrinth.logger import Logger
from termmodrinth.modrinth.api import ModrinthAPI
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
      path = Config().active_path(project_type)
      for f in os.listdir(path):
        if f.endswith(project_types[project_type]['extention']):
          if f not in self.files[project_type]:
            filename = "{}/{}".format(path, f)
            Logger().log("inf", "Removing {} in {}s".format(filename, project_type), "red")
            os.remove(filename)

  def printStats(self):
    for project_type in project_types.keys():
      Logger().log("inf", "{}s. Requested: {}; Processed: {}; Files: {}".format(project_type.capitalize(), len(Config().projects(project_type)), len(self.projects[project_type]), len(self.files[project_type])), "light_green")
    Logger().log("inf", "Total API queryes: {0[0]}; Spent time: {0[1]}; Average QPS: {0[2]}".format(ModrinthAPI().stats()), "light_green")
