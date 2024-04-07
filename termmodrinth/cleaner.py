from termmodrinth.config import config
from termmodrinth.logger import logger
import os

class Cleaner(object):
  def __init__(self):
    self.projects = {
      'mod': [],
      'resourcepack': [],
      'shader': []
    }
    self.extentions = {
      'mod': '.jar',
      'resourcepack': '.zip',
      'shader': '.zip'
    }

  def append(self, project_type, slug):
    if slug not in self.projects[project_type]:
      self.projects[project_type].append(slug)
      return True
    return False

  def cleanup(self):
    for project_type in ['mod', 'resourcepack', 'shader']:
      logger.delimiter("|", "Cleaning up {}s".format(project_type))
      path = config.active_path(project_type)
      for f in os.listdir(path):
        if f.endswith(self.extentions[project_type]):
          fn, ext = os.path.splitext(f)
          if fn not in self.projects[project_type]:
            filename = "{}/{}".format(path, f)
            logger.msg("Removing {}".format(filename), "red")
            os.remove(filename)

  def printStats(self):
    logger.delimiter("=", "Stats")
    logger.msg("Mods. Requested: {}; Downloaded: {}".format(len(config.mods()), len(self.projects['mod'])), "light_green")
    logger.msg("Resourcepacks. Requested: {}; Downloaded: {}".format(len(config.resourcepacks()), len(self.projects['resourcepack'])), "light_green")
    logger.msg("Shaders. Requested: {}; Downloaded: {}".format(len(config.shaders()), len(self.projects['shader'])), "light_green")
