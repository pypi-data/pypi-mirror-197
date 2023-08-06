import coloredlogs
import logging

DEBUG = False
SHOW_OUT = False  # show the output of scorch (display files content) to stdout

coloredlogs.install(level=logging.DEBUG)
