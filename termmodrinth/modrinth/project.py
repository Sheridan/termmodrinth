import urllib.request
import datetime
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
    self._version_data = None
    self._project_data = None

  def version_data(self):
    if not self._version_data:
      self._version_data = ModrinthAPI().loadProjectVersion(self.slug, self.project_type)
    return self._version_data

  def project_data(self):
    if not self._project_data:
      self._project_data = ModrinthAPI().loadProject(self.version_data()["project_id"])
    return self._project_data

  def storage_filename(self, remote_filename): return "{}_{}_{}".format(self.slug, self.version_data()['version_number'], remote_filename)
  def storage_filepath(self, remote_filename): return "{}/{}".format(self.storage_path, self.storage_filename(remote_filename))

  def info_filename(self): return "{}_{}.info".format(self.slug, self.version_data()['version_number'])
  def info_filepath(self): return "{}/{}".format(self.storage_path, self.info_filename())

  def filelist_filename(self): return "{}_{}.files".format(self.slug, self.version_data()['version_number'])
  def filelist_filepath(self): return "{}/{}".format(self.storage_path, self.filelist_filename())

  def active_filename(self, is_primary, file_index, extention): return "{}.{}".format(self.slug, extention) if is_primary else "{}_{}.{}".format(self.slug, file_index - 1, extention)
  def active_filepath(self, is_primary, file_index, extention): return "{}/{}".format(self.active_path, self.active_filename(is_primary, file_index, extention))

  def fileMustBeDownloaded(self, is_primary, filename):
    if is_primary:
      return True
    if Config().primariesOnly(self.project_type):
      return False
    if Config().tryNotDownloadSources(self.project_type) and self.isSources(filename):
      return False
    return True

  def isSources(self, filename):
    return "source" in filename or "src" in filename

  def writeCalculatedInfoPart(self, file_handler, caption, text):
    Logger().projectLog('inf', self.project_type, self.slug, "{}: {}".format(caption, text), "yellow")
    file_handler.write("{}: {}\n".format(caption, text))

  def writeInfoPart(self, file_handler, data, key):
    if data[key]:
        caption = key.capitalize().replace("_", " ")
        ifnewline = "\n" if "\n" in data[key] else ""
        text = "{}{}".format(ifnewline, data[key])
        self.writeCalculatedInfoPart(file_handler, caption, text)

  def mineInfo(self):
    with open(self.info_filepath(), 'w') as file_handler:
      self.writeInfoPart(file_handler, self.project_data(), "title")
      self.writeInfoPart(file_handler, self.project_data(), "description")
      self.writeInfoPart(file_handler, self.project_data(), "monetization_status")
      self.writeInfoPart(file_handler, self.version_data(), "name")
      self.writeInfoPart(file_handler, self.version_data(), "version_number")
      self.writeInfoPart(file_handler, self.version_data(), "version_type")
      self.writeCalculatedInfoPart(file_handler, "Published date", datetime.datetime.fromisoformat(self.project_data()["published"]).strftime("%Y.%m.%d %H:%M:%S"))
      self.writeCalculatedInfoPart(file_handler, "Updated date", datetime.datetime.fromisoformat(self.project_data()["updated"]).strftime("%Y.%m.%d %H:%M:%S"))
      self.writeCalculatedInfoPart(file_handler, "Supported minecraft versions", ", ".join(self.version_data()["game_versions"]))
      self.writeCalculatedInfoPart(file_handler, "Supported loaders", ", ".join(self.version_data()["loaders"]))
      self.writeCalculatedInfoPart(file_handler, "Side", "; ".join(["Server: {}".format(self.project_data()["server_side"]), "Client: {}".format(self.project_data()["client_side"])]))
      self.writeInfoPart(file_handler, self.project_data(), "issues_url")
      self.writeInfoPart(file_handler, self.project_data(), "wiki_url")
      self.writeInfoPart(file_handler, self.version_data(), "changelog")

  def download(self):
    if len(self.version_data()["files"]):
      if not os.path.isfile(self.filelist_filepath()):
        self.mineInfo()
        filelist_handler = open(self.filelist_filepath(), 'w')
        for remote_file in self.version_data()["files"]:
          if self.fileMustBeDownloaded(remote_file["primary"], remote_file["filename"]):
            if not os.path.isfile(self.storage_filepath(remote_file["filename"])):
              Logger().projectLog('inf', self.project_type, self.slug, "Downloading {}".format(remote_file["url"]), 'green')
              filelist_handler.write("{}\n".format(self.storage_filename(remote_file["filename"])))
              urllib.request.urlretrieve(remote_file["url"], self.storage_filepath(remote_file["filename"]))
            else:
              Logger().projectLog('inf', self.project_type, self.slug, "{} alredy downloaded".format(remote_file["filename"]), 'cyan')
        filelist_handler.close()
      else:
        Logger().projectLog('inf', self.project_type, self.slug, "All files alredy downloaded", 'cyan')

  def link(self):
    from termmodrinth.cleaner import Cleaner
    for index, remote_file in enumerate(self.version_data()["files"]):
      if self.fileMustBeDownloaded(remote_file["primary"], remote_file["filename"]):
        storage_filepath = self.storage_filepath(remote_file["filename"])
        extention = os.path.splitext(storage_filepath)[1][1:]
        active_filepath = self.active_filepath(remote_file["primary"], index, extention)
        Cleaner().appenFile(self.project_type, self.active_filename(remote_file["primary"], index, extention))
        if not os.path.isfile(active_filepath):
          Logger().projectLog('inf', self.project_type, self.slug, "Linking {}".format(self.active_filename(remote_file["primary"], index, extention)), 'green')
          os.link(storage_filepath, active_filepath)
        else:
          Logger().projectLog('inf', self.project_type, self.slug, "{} alredy linked".format(self.active_filename(remote_file["primary"], index, extention)), 'cyan')

  def updateDependencies(self):
    from termmodrinth.worker import Worker
    for dependency in self.version_data()["dependencies"]:
      if dependency["project_id"]:
        slug, project_type = ModrinthAPI().loadSlug(dependency["project_id"])
        Logger().projectLog('inf', self.project_type, self.slug, "Dependency {}: {}:{}".format(dependency["dependency_type"], project_type, slug), "blue")
        if dependency["dependency_type"] in Config().requestDependencies():
          Logger().projectLog('inf', self.project_type, self.slug, "Request dependency: {}:{}".format(project_type, slug), "green")
          Worker().updateProject(project_type, slug)

  def update(self):
    self.download()
    self.link()
    self.updateDependencies()
