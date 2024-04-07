import urllib.request
import os

from termmodrinth.config import Config
from termmodrinth.logger import Logger
from termmodrinth.modrinth.api import ModrinthAPI

class ModrinthProject(object):
  def __init__(self, slug, project_type):
    self.slug = slug
    self.project_type = project_type
    self.storage_path = Config().storage_path(project_type)
    self.active_path = Config().active_path(project_type)
    self.data = ModrinthAPI().loadProjectVersion(self.slug, project_type)
    fn, ext = os.path.splitext(self.data["files"][0]["filename"])
    self.storage_filename = "{}/{}".format(self.storage_path, self.data["files"][0]["filename"])
    self.active_filename = "{}/{}".format(self.active_path, "{}{}".format(slug, ext))
    self.changelog_filename = "{}.changelog".format(self.storage_filename)
    # print(self.changelog_path)

  def download(self):
    if not os.path.isfile(self.storage_filename):
      Logger().log('inf', self.project_type, self.slug, "Downloading {}".format(self.data["files"][0]["url"]), 'green')
      if self.data["changelog"]:
        Logger().log('inf', self.project_type, self.slug, "Changelog:\n{}".format(self.data["changelog"]), "yellow")
        with open(self.changelog_filename, 'w') as f:
          f.write(self.data["changelog"])
      urllib.request.urlretrieve(self.data["files"][0]["url"], self.storage_filename)
    else:
      Logger().log('inf', self.project_type, self.slug, "Alredy downloaded", 'cyan')

  def link(self):
    if not os.path.isfile(self.active_filename):
      Logger().log('inf', self.project_type, self.slug, "Linking {}".format(self.active_filename), 'green')
      os.link(self.storage_filename, self.active_filename)
    else:
      Logger().log('inf', self.project_type, self.slug, "Alredy linked", 'cyan')

  def updateDependencies(self):
    from termmodrinth.worker import Worker
    for dependency in self.data["dependencies"]:
      if dependency["dependency_type"] == "required":
        slug, project_type = ModrinthAPI().loadSlug(dependency["project_id"])
        Logger().log('inf', self.project_type, self.slug, "Dependency: {}:{}".format(project_type, slug), "blue")
        Worker().updateProject(project_type, slug)

  def update(self):
    self.download()
    self.link()
    self.updateDependencies()
