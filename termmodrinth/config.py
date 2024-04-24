import json
import os

from termmodrinth.singleton import Singleton

class Config(Singleton):
  def _new(self):
    with open('termmodrinth.json', 'r') as f:
      self.conf_data = json.load(f)
    self._qps = int(self.conf_data["modrinth"]["max_queries_per_minute"] / 60)
    self._paths = {}

  def threads(self): return self.conf_data["threads"]
  def qps(self): return self._qps

  def filterListComment(self, data): return list(filter(lambda x: not x.startswith("#"), data))

  def projects(self, project_type): return self.filterListComment(self.conf_data[project_type+'s'])

  def modrinthLoader(self, project_type): return self.conf_data["modrinth"]["loader"][project_type+'s']
  def modrinthMCVersions(self, project_type): return self.filterListComment(self.conf_data["modrinth"]["minecraft_versions"][project_type+'s'])

  def modrinthLogin(self): return self.conf_data["modrinth"]["user"]["login"]
  def modrinthPassword(self): return self.conf_data["modrinth"]["user"]["password"]

  def cacheLiveSecunds(self): return self.conf_data["cache_lifetime_minutes"]*60
  def tmpPath(self): return self.conf_data["tmp_path"]

  def storage_path(self, project_type): return self.storage(project_type, "storage")
  def active_path(self, project_type): return self.storage(project_type, "active")
  def storage(self, project_type, storage_type):
    key = "{}:{}".format(project_type, storage_type)
    if key not in self._paths:
      self._paths[key] = "{}/{}s/{}".format(self.conf_data["storage"], project_type, storage_type)
      os.makedirs(self._paths[key], exist_ok=True)
    return self._paths[key]

  def primariesOnly(self, project_type): return self.conf_data["modrinth"]["primaries_only"][project_type+'s']
  def tryNotDownloadSources(self, project_type): return self.conf_data["modrinth"]["try_not_download_sources"][project_type+'s']

  def requestDependencies(self): return self.filterListComment(self.conf_data["modrinth"]["request_dependencies"])
