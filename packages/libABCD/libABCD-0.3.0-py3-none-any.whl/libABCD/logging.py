###
# Logging
###

import logging
from logging.handlers import TimedRotatingFileHandler

import os
import sys
import traceback
import time
import libABCD

# note: ch and fh are global variables for this module

def _init_log_settings(logger):
  global ch,fh
  logger.setLevel(logging.DEBUG)
  # log directory
  #logdir = os.path.join(os.getenv("HOME"), "Developer/log")
  logdir = ("log")
  if not os.path.isdir(logdir):
    os.makedirs(logdir)
  # create file handler which logs even debug messages
  fh = TimedRotatingFileHandler(os.path.join(logdir, libABCD.name+'.log'),when='midnight',utc=True,delay=True)
  fh.setLevel(logging.INFO)
  # create console handler with a higher log level
  ch = logging.StreamHandler(sys.stdout)
  ch.setLevel(logging.DEBUG)
  # create formatter and add it to the handlers
  formatter = logging.Formatter('%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s')
  fh.setFormatter(formatter)
  ch.setFormatter(formatter)
  # add the handlers to the logger
  logger.addHandler(fh)  # handler[0] is file dump
  logger.addHandler(ch)  # handler[1] is stdout

def die():
    exc_type, exc_value, exc_tb = sys.exc_info()
    libABCD.logger.critical("Shutting down: {}".format(traceback.format_exception(exc_type, exc_value, exc_tb)))
    os._exit(1)

def quiet(data,conn):
    try:
        if libABCD.network_info["name"] == data["to"]:
            ch.setLevel(logging.INFO)
    except Exception as e:
        print(e)
        pass

def verbose(data,conn):
    try:
        if libABCD.network_info["name"] == data["to"]:
            ch.setLevel(logging.DEBUG)
    except Exception as e:
        pass

def setfilelog(level=logging.INFO):
    fh.setLevel(level)

def setstdout(level=logging.DEBUG):
    ch.setLevel(level)
