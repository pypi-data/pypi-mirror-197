import logging as log
import sys

DEBUG = log.DEBUG
INFO = log.INFO
ERROR = log.ERROR

'''
level = python_supporter.logging.DEBUG
#level = python_supporter.logging.INFO
#level = python_supporter.logging.ERROR
python_supporter.logging.basic_config(level)
'''
def basic_config(level=DEBUG, log_file="log.txt"):
    for name in log.root.manager.loggerDict:
        logger = log.getLogger(name)
        #logger.disabled = True
        logger.setLevel(log.ERROR)

    log.basicConfig(
        handlers=[
            log.FileHandler(log_file, encoding="utf-8"),
            log.StreamHandler(sys.stdout)
        ],
        format = '%(asctime)s: %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        level = level
    )

def debug(message):
    log.debug(message)

def info(message):
    log.info(message)

def error(message):
    log.error(message)
