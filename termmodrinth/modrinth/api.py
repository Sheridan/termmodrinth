import json
import urllib.request
import urllib.parse

from termmodrinth.singleton import Singleton
from termmodrinth.config import Config
from termmodrinth.logger import Logger

class ModrinthAPI(Singleton):
  def __init__(self):
    self.apiURL = "https://api.modrinth.com/v2/"
    self.cache = {}
    # self.apiURL = "https://staging-api.modrinth.com/v2/"

  def dump_json(self, data):
    print(json.dumps(data, indent=2))

  def quote(self, string):
    return "%22{}%22".format(string)

  def callAPI(self, query):
    url = self.apiURL + query
    # print(url)
    try:
      with urllib.request.urlopen(url) as response:
        jdata = json.load(response)
        return jdata
    except Exception as e:
      Logger().log('err', "", "", "Failure call api: {}".format(e), "white")
    # raise Exception("Can not request api")

  def loadProject(self, project_id):
    if project_id not in self.cache.keys():
      self.cache[project_id] = self.callAPI("project/{}".format(project_id))
    # self.dump_json(pdata)
    return self.cache[project_id]

  def loadSlug(self, project_id):
    pdata = self.loadProject(project_id)
    return (pdata["slug"], pdata["project_type"])

  def loadProjectVersion(self, slug, project_type):
    key = "{}:{}".format(slug, project_type)
    if key not in self.cache.keys():
      for mc_version in Config().modrinthMCVersions():
        api_path = 'project/{}/version?game_versions=[{}]&loaders=[{}]'.format(slug, self.quote(mc_version), self.quote(Config().modrinthLoader(project_type)))
        pdata = self.callAPI(api_path)
        if len(pdata):
          # self.dump_json(pdata[0])
          self.cache[key] = pdata[0]
          break
    if key not in self.cache.keys():
      Logger().log('err', project_type, slug, "No project version available", "white")
      raise Exception("No project version available")
    return self.cache[key]
