import json
import urllib.request
import urllib.parse

from termmodrinth.singleton import Singleton
from termmodrinth.config import Config


class ModrinthAPI(Singleton):
  def __init__(self):
    self.apiURL = "https://api.modrinth.com/v2/"
    # self.apiURL = "https://staging-api.modrinth.com/v2/"

  def dump_json(self, data):
    print(json.dumps(data, indent=2))

  def quote(self, string):
    return "%22{}%22".format(string)

  def callAPI(self, query):
    url = self.apiURL + query
    # print(url)
    with urllib.request.urlopen(url) as response:
      jdata = json.load(response)
      return jdata

  def loadSlug(self, project_id):
    pdata = self.callAPI("project/{}".format(project_id))
    # self.dump_json(pdata)
    return (pdata["slug"], pdata["project_type"])

  def loadProjectVersion(self, slug, project_type):
    loader = ""
    if project_type == "mod":
      loader = "&loaders=[{}]".format(self.quote(Config().modrinthLoader()))
    for mc_version in Config().modrinthMCVersions():
      api_path = 'project/{}/version?game_versions=[{}]{}'.format(slug, self.quote(mc_version), loader)
      pdata = self.callAPI(api_path)
      if len(pdata):
        # if len(pdata[0]["dependencies"]):
        # self.dump_json(pdata[0]["changelog"])
        return pdata[0]
