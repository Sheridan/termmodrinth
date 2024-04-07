import json
import os

from termmodrinth.singleton import Singleton

class Config(Singleton):
  def __init__(self):
    with open('termmodrinth.json', 'r') as f:
      self.conf_data = json.load(f)

  def projects(self, project_type): return list(filter(lambda x: not x.startswith("#"), self.conf_data[project_type+'s']))

  def modrinthLoader(self): return self.conf_data["modrinth"]["loader"]
  def modrinthMCVersions(self): return self.conf_data["modrinth"]["minecraft_versions"]

  def modrinthLogin(self): return self.conf_data["modrinth"]["user"]["login"]
  def modrinthPassword(self): return self.conf_data["modrinth"]["user"]["password"]

  def storage_path(self, project_type): return self.storage(project_type, "storage")
  def active_path(self, project_type): return self.storage(project_type, "active")
  def storage(self, project_type, storage_type):
    path = "{}/{}s/{}".format(self.conf_data["storage"], project_type, storage_type)
    os.makedirs(path, exist_ok=True)
    return path
