import json
import os

from termmodrinth.singleton import Singleton

class Config(Singleton):
  def __init__(self):
    with open('termmodrinth.json', 'r') as f:
      self.conf_data = json.load(f)

  def threads(self): return self.conf_data["threads"]

  def filterListComment(self, data): return list(filter(lambda x: not x.startswith("#"), data))

  def projects(self, project_type): return self.filterListComment(self.conf_data[project_type+'s'])

  def modrinthLoader(self, project_type): return self.conf_data["modrinth"]["loader"][project_type+'s']
  def modrinthMCVersions(self): return self.conf_data["modrinth"]["minecraft_versions"]

  def modrinthLogin(self): return self.conf_data["modrinth"]["user"]["login"]
  def modrinthPassword(self): return self.conf_data["modrinth"]["user"]["password"]

  def storage_path(self, project_type): return self.storage(project_type, "storage")
  def active_path(self, project_type): return self.storage(project_type, "active")
  def storage(self, project_type, storage_type):
    path = "{}/{}s/{}".format(self.conf_data["storage"], project_type, storage_type)
    os.makedirs(path, exist_ok=True)
    return path

  def primariesOnly(self, project_type): return self.conf_data["modrinth"]["primaries_only"][project_type+'s']
  def tryNotDownloadSources(self, project_type): return self.conf_data["modrinth"]["try_not_download_sources"][project_type+'s']

  def requestDependencies(self): return self.filterListComment(self.conf_data["modrinth"]["request_dependencies"])
