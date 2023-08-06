import logging
import logging.handlers
import argparse
import sys
import time
from . import fn

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
	def __init__(self, logger, level):
		#"""Needs a logger and a logger level."""
		self.logger = logger;
		self.level = level;

	def write(self, message):
		# Only log if there is a message (not just a new line)
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip());
	def flush(self):
		pass;


def start(filename):

	LOG_FILE_NAME = fn.openRealPath("../log/"+filename).name;
	LOG_DAYS = 1;
	LOG_LEVEL = logging.DEBUG;
	logger = logging.getLogger(__name__)
	# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
	# Give the logger a unique name (good practice)
	logger = logging.getLogger(__name__)
	# Set the log level to LOG_LEVEL
	logger.setLevel(LOG_LEVEL)
	# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
	handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE_NAME, when="midnight", backupCount=LOG_DAYS)
	# Format each log message like this
	formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
	# Attach the formatter to the handler
	handler.setFormatter(formatter)
	# Attach the handler to the logger
	logger.addHandler(handler)


	# Replace stdout with logging to file at INFO level
	sys.stdout = MyLogger(logger, logging.INFO)
	# Replace stderr with logging to file at ERROR level
	sys.stderr = MyLogger(logger, logging.ERROR)

def v(*string):
	try:
		if True:
			print('[Verbose]',*string);
	except Exception as ex:
		print('[Verbose][error]', ex);
def d(*string):
	try:
		if True:
			print('[Debug]',*string);
	except Exception as ex:
		print('[Debug][error]', ex);
def e(*string):
	try:
		if True:
			print('[Error]',*string);
	except Exception as ex:
		print('[Error][error]', ex);