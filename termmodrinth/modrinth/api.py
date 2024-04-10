import json
import urllib.request
import urllib.parse
import time
import os
import datetime
# from packaging.version import Version

from termmodrinth.singleton import Singleton
from termmodrinth.config import Config
from termmodrinth.logger import Logger

from termmodrinth.utils import convert_isoformat_date

class ModrinthAPI(Singleton):
  def _new(self):
    # self.apiURL = "https://staging-api.modrinth.com/v2/"
    self.apiURL = "https://api.modrinth.com/v2/"
    self.cache = {}
    self.resetQPS()
    self.totlal_requests = 0
    self.init_time = time.time()

  def dump_json(self, data):
    print(json.dumps(data, indent=2))

  def quote(self, string):
    return "%22{}%22".format(string)

  def resetQPS(self):
    self.requests = 0
    self.time = time.time()

  def checkQPS(self):
    delta = time.time() - self.time
    if self.requests >= Config().qps() and delta < 1:
      sleepTime = delta * 2
      Logger().log("inf", "QPS sleep {}s".format(round(sleepTime, 2)), "blue")
      time.sleep(sleepTime)
      self.resetQPS()

  def callAPI(self, query):
    url = self.apiURL + query
    # print(url)
    try:
      self.checkQPS()
      with urllib.request.urlopen(url) as response:
        self.requests += 1
        self.totlal_requests += 1
        jdata = json.load(response)
        return jdata
    except Exception as e:
      Logger().log('err', "Failure call api ({}): {}".format(url, e), "red")
      os._exit(1)

  def loadProject(self, project_id):
    if project_id not in self.cache.keys():
      self.cache[project_id] = self.callAPI("project/{}".format(project_id))
    # self.dump_json(pdata)
    return self.cache[project_id]

  def loadSlug(self, project_id):
    pdata = self.loadProject(project_id)
    return (pdata["slug"], pdata["project_type"])

  def mineLastVersion(self, data):
    data_item = data[0]
    for data_index in data:
      # print("curr: {}".format(data_index["version_number"]))
      if convert_isoformat_date(data_index["date_published"]) > convert_isoformat_date(data_item["date_published"]):
        data_item = data_index
    return data_item

  def loadProjectVersion(self, slug, project_type):
    key = "{}:{}".format(slug, project_type)
    if key not in self.cache.keys():
      for mc_version in Config().modrinthMCVersions(project_type):
        api_path = 'project/{}/version?game_versions=[{}]&loaders=[{}]'.format(slug, self.quote(mc_version), self.quote(Config().modrinthLoader(project_type)))
        pdata = self.callAPI(api_path)
        # if len(pdata) > 1:
        # self.dump_json(pdata)
        if len(pdata):
          self.cache[key] = self.mineLastVersion(pdata)
          Logger().projectLog('inf', slug, project_type, "Selected version: {}".format(self.cache[key]["version_number"]), "yellow")
          # self.dump_json(self.cache[key])
          break
        else:
          Logger().projectLog('wrn', project_type, slug, "Unavialable for minecraft version {}".format(mc_version), "light_grey")
    if key not in self.cache.keys():
      Logger().projectLog('err', project_type, slug, "None version available", "red")
      os._exit(1)
    return self.cache[key]

  def stats(self):
    time_spent = time.time() - self.init_time
    return (self.totlal_requests, time.strftime("%H:%M:%S", time.gmtime(time_spent)), round(self.totlal_requests/time_spent, 2))
