from termcolor import colored, cprint
import datetime

class Logger(object):
  def __init__(self):
    self.levels = {
      'inf': 'green',
      'wrn': 'yellow',
      'err': 'red'
    }

  def delimiter(self, delimiter, text):
    dlm = colored(delimiter * 64, "blue")
    print("{} {} {}".format(dlm, colored(text, "magenta"), dlm))

  def msg(self, text, color):
    print(colored(text, color))

  def log(self, level, project_type, slug, msg, msg_color = 'white'):
    print("[{}] [{}] {}: {}".format(colored(datetime.datetime.now().strftime("%H:%M:%S"), 'blue'),
                                    colored(level, self.levels[level]),
                                    colored('{}:{}'.format(project_type, slug), "magenta"),
                                    colored(msg, msg_color)))

logger = Logger()
