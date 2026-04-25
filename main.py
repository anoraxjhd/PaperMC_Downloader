# Imports
import src.ui as ui
import src.vars as vars
from os import path
from argparse import ArgumentParser

vars.savePath = path.dirname(path.abspath(__file__))

def parseArgs():
  parser = ArgumentParser()
  parser.add_argument("--lang", choices=vars.supportedLanguages, default=vars.lang)
  parser.add_argument("--no-gui", action="store_true")

  args = parser.parse_args()
  vars.lang = args.lang
  vars.no_gui = args.no_gui

parseArgs()
if vars.no_gui:
  ui.terminal()
else:
  ui.GUI()