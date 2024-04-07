from termmodrinth.config import config
from termmodrinth.logger import logger
from termmodrinth.cleaner import Cleaner
from concurrent.futures import ThreadPoolExecutor
import os

class Worker(object):
  def __init__(self):
    self.cleaner = Cleaner()
    self.tp_executor = ThreadPoolExecutor(max_workers=8)

    # print(self.tp_executor)

  def updateProject(self, project_type, slug):
    if self.cleaner.append(project_type, slug):
      logger.log('inf', project_type, slug, 'Starting update')
      project_types[project_type]['class'](slug).update()
    else:
      logger.log('inf', project_type, slug, "Already updated", "cyan")

  def update(self):
    for project_type in ['mod', 'resourcepack', 'shader']:
      for slug in config.projects(project_type):
        self.appendThread(project_type, slug)

  def appendThread(self, project_type, slug):
    self.tp_executor.submit(self.updateProject, project_type, slug)

  def run(self):
    self.update()
    self.tp_executor.shutdown(wait=True)
    self.cleaner.cleanup()
    self.cleaner.printStats()


worker = Worker()

from termmodrinth.modrinth import project_types
# print(worker)
# from termmodrinth.modrinth.mod import ModrinthMod
# from termmodrinth.modrinth.resourcepack import ModrinthResourcePack
# from termmodrinth.modrinth.shader import ModrinthShader
