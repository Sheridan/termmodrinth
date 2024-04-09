from termmodrinth.singleton import Singleton
from termcolor import colored
import datetime

class Logger(Singleton):
  levels = {
      'inf': 'green',
      'wrn': 'yellow',
      'err': 'red'
    }

  def _timestamp(self):
    return colored(datetime.datetime.now().strftime("%H:%M:%S"), 'blue')

  def _level(self, level):
    return colored(level, self.levels[level])

  def log(self, level, msg, color):
    print("[{}] [{}] {}".format(self._timestamp(),
                                self._level(level),
                                colored(msg, color)))

  def projectLog(self, level, project_type, slug, msg, msg_color = 'white'):
    print("[{}] [{}] {}: {}".format(self._timestamp(),
                                    self._level(level),
                                    colored('{}:{}'.format(project_type, slug), "magenta"),
                                    colored(msg, msg_color)))
