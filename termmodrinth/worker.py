from concurrent.futures import ThreadPoolExecutor, wait

from termmodrinth.singleton import Singleton
from termmodrinth.cleaner import Cleaner
from termmodrinth.config import Config
from termmodrinth.logger import Logger
from termmodrinth.modrinth import project_types

class Worker(Singleton):
  def _new(self):
    self.tp_executor = ThreadPoolExecutor(max_workers=Config().threads())

  def updateProject(self, project_type, slug):
    if Cleaner().appenSlug(project_type, slug):
      Logger().projectLog('inf', project_type, slug, 'Starting update')
      project_types[project_type]['class'](slug).update()
    else:
      Logger().projectLog('inf', project_type, slug, "Already updated", "light_blue")

  def update(self):
    for project_type in project_types.keys():
      for slug in Config().projects(project_type):
        self.appendThread(project_type, slug)

  def appendThread(self, project_type, slug):
    self.tp_executor.submit(self.updateProject, project_type, slug)

  def run(self):
    self.update()
    self.tp_executor.shutdown(wait=True, cancel_futures=False)
    Cleaner().cleanup()
    Cleaner().printStats()
