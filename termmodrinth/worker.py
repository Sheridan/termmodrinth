from termmodrinth.config import config
from termmodrinth.logger import logger
from termmodrinth.cleaner import Cleaner
from concurrent.futures import ThreadPoolExecutor
import os

class Worker(object):
  def __init__(self):
    self.cleaner = Cleaner()
    self.tp_executor = ThreadPoolExecutor(max_workers=8)

  def updateMod(self, slug, cleaner):
    if cleaner.append('mod', slug):
      # logger.log('inf', 'mod', slug, 'Starting update')
      ModrinthMod(slug).update()
    else:
      logger.log('inf','mod', slug, "Already updated", "cyan")

  def updateResourcePack(self, slug, cleaner):
    if cleaner.append('resourcepack', slug):
      # logger.log('inf', 'resourcepack', slug, 'Starting update')
      ModrinthResourcePack(slug).update()
    else:
      logger.log('inf', 'resourcepack', slug, "Already updated", "cyan")

  def updateShader(self, slug, cleaner):
    if cleaner.append('shader', slug):
      # logger.log('inf', 'shader', slug, 'Starting update')
      ModrinthShader(slug).update()
    else:
      logger.log('inf', 'shader', slug, "Already updated", "cyan")

  def updateProject(self, slug, project_type):
    if project_type == "mod":
      self.tp_executor.submit(self.updateMod, slug)
    if project_type == "resourcepack":
      self.tp_executor.submit(self.updateResourcePack, slug)
    if project_type == "shader":
      self.tp_executor.submit(self.updateShader, slug)

  def updateMods(self):
    for slug in config.mods():
      self.tp_executor.submit(self.updateMod, slug, self.cleaner)

  def updateResourcePacks(self):
    for slug in config.resourcepacks():
      self.tp_executor.submit(self.updateResourcePack, slug, self.cleaner)

  def updateShaders(self):
    for slug in config.shaders():
      self.tp_executor.submit(self.updateShader, slug, self.cleaner)



  def run(self):
    # with ThreadPoolExecutor() as executor:
    #   executor.submit(self.updateMods)
    #   executor.submit(self.updateResourcePacks)
    #   executor.submit(self.updateShaders)
    self.updateMods()
    self.updateResourcePacks()
    self.updateShaders()
    self.tp_executor.shutdown(wait=True)
    self.cleaner.cleanup()
    self.cleaner.printStats()


worker = Worker()

from termmodrinth.modrinth.mod import ModrinthMod
from termmodrinth.modrinth.resourcepack import ModrinthResourcePack
from termmodrinth.modrinth.shader import ModrinthShader
