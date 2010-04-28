import curses
import logging
import sys

from colorlogger import ColoredLogFormatter


__author__ = "Matt Dennewitz"
__version__ = (0, 1, 0, 'pre')
__all__ = ["document", "fields"]


def get_logger(name="stretchpants-indexer", loglevel=logging.INFO, color=True):
    color = False
    if curses and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except:
            pass
    channel = logging.StreamHandler()
    channel.setFormatter(ColoredLogFormatter(color=color))
    
    logger = logging.getLogger(name)
    logger.addHandler(channel)
    logger.setLevel(loglevel)
    
    return logger


def autodiscover(app_list):
    import imp
    import importlib

    for app in app_list:
        try:
            app_path = importlib.import_module(app).__path__
        except:
            continue

        try:
            imp.find_module('search', app_path)
        except:
            continue

        importlib.import_module("%s.search" % app)
