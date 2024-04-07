from termmodrinth.modrinth.api import api
from termmodrinth.config import config
from termmodrinth.logger import logger
from termmodrinth.worker import worker
import urllib.request
import os

class ModrinthProject(object):
  def __init__(self, slug, project_type):
    self.slug = slug
    self.project_type = project_type
    self.storage_path = config.storage_path(project_type)
    self.active_path = config.active_path(project_type)
    self.data = api.loadProjectVersion(self.slug, project_type)
    fn, ext = os.path.splitext(self.data["files"][0]["filename"])
    self.storage_filename = "{}/{}".format(self.storage_path, self.data["files"][0]["filename"])
    self.active_filename = "{}/{}".format(self.active_path, "{}{}".format(slug, ext))
    self.changelog_filename = "{}.changelog".format(self.storage_filename)
    # print(self.changelog_path)

  def download(self):
    if not os.path.isfile(self.storage_filename):
      logger.log('inf', self.project_type, self.slug, "Downloading {}".format(self.data["files"][0]["url"]), 'green')
      if self.data["changelog"]:
        logger.log('inf', self.project_type, self.slug, "Changelog:\n{}".format(self.data["changelog"]), "yellow")
        with open(self.changelog_filename, 'w') as f:
          f.write(self.data["changelog"])
      urllib.request.urlretrieve(self.data["files"][0]["url"], self.storage_filename)
    else:
      logger.log('inf', self.project_type, self.slug, "Alredy downloaded", 'cyan')

  def link(self):
    if not os.path.isfile(self.active_filename):
      logger.log('inf', self.project_type, self.slug, "Linking {}".format(self.active_filename), 'green')
      os.link(self.storage_filename, self.active_filename)
    else:
      logger.log('inf', self.project_type, self.slug, "Alredy linked", 'cyan')

  def updateDependencies(self):
    for dependency in self.data["dependencies"]:
      if dependency["dependency_type"] == "required":
        slug, project_type = api.loadSlug(dependency["project_id"])
        worker.updateProject(slug, project_type)
        # logger.msg("{}:{}".format(project_type, slug), "red")

  def update(self):
    self.download()
    self.link()
    self.updateDependencies()
