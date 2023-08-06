import os
import time

def clear():
  print(colors.red + '\nClearing Screen' + colors.end)
  os.system('clear')

class colors:
  red = '\u001b[31m'
  end = '\033[0m'
  warn = '\033[93m'
