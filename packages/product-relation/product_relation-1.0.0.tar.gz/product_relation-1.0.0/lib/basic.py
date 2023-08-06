from datetime import datetime
from datetime import timezone
from datetime import timedelta
import time;
import os;
import json;
import ast;
import socket;
import importlib;

def decodeHeader(raw):
	if raw.strip().startswith('POST'):
		if 'Content-Type: application/json' in raw:
			raw_data = raw.split('\n\r\n')[-1];
			return json.loads(raw_data) , 'POST';
	else:
		return json.loads(raw), 'SOCKET';

def getRootPath():
	abspath = os.path.dirname(os.path.abspath(__file__));
	domains = ['procurement'];
	for domain in domains:
		d = abspath.split(domain);
		if(len(d)>1):
			path = d[0]+'/'+domain;
			return path;
def getConfig():
	# abspath = os.path.dirname(os.path.abspath(__file__));
	# config = json.load(open(getRootPath()+'/config.json'));
	# config = ast.literal_eval(json.dumps(config));
	if (int(os.getenv('LIVE', '0')) <=0):
		# print(getRootPath()+'/.env');
		env = json.load(open(getRootPath()+'/.env'));
		#print(env);
		for e in env.keys():
			#print(e, env[e]);
			os.putenv(e, str(env[e]));
			os.environ[e] = str(env[e]);
	return os.environ;

def dumps(data):
	return json.dumps(data);

def now():#get datetime now
	timezone = time.timezone /3600;
	return datetime.utcnow() - timedelta(hours=timezone);

def GBfy(number):
	return round(number/1024/1024/1024, 1);
def getCurrentIP():
	return socket.gethostbyname(socket.gethostname());

def chunks(l, n): #split list l into multiple pieces consists of maximum n elements 
	n = max(1, n);
	return [l[i:i + n] for i in range(0, len(l), n)];

def extractData(obj, cols):
	data = {};
	for key in cols.keys():
		if key in obj:
			data[cols[key]] = obj[key];
	return data;

def getNestedElement(data, name = ""):
	if(data and name):
		elements = name.split(".");
		tmp = None;
		for e in elements:
			if(not tmp):
				if(e in data):
					tmp = data[e];
				else:
					return None;
			elif(e in tmp):
				tmp = tmp[e];
			else:
				return None;
		return tmp;
	return None;

def reloadlib(class_name):
	importlib.reload(class_name);

config = getConfig();