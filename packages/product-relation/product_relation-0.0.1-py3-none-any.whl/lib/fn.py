import sys;
import json;
import hashlib;
import os, re, csv;
import pandas as pd;
import numpy as np;
import time;
import math;
import warnings

from . import basic;
from . import Logger;
from . import DateTime;
from datetime import datetime

warnings.simplefilter(action='ignore', category=FutureWarning)
country_codes = {};
captions_table = {};
def chunks(l, n): #split list l into multiple pieces consists of maximum n elements 
	n = max(1, n);
	return [l[i:i + n] for i in range(0, len(l), n)];

def getRootPath():
	dir_path = os.path.dirname(os.path.realpath(__file__));
	# Logger.v('getRootPath:',dir_path);

	# root_path = dir_path.split('/python')[0];
	root_path = os.path.normpath(dir_path+'/../');
	return root_path;
def getFileList(directory):
	from os import walk
	f = []
	for (dirpath, dirnames, filenames) in walk(directory):
		f.extend(filenames)
		break
	return f;

def getCurrentPath(path):
	return os.path.dirname(os.path.realpath(path));

def getCrawlPath():
	dir_path = os.path.dirname(os.path.realpath(__file__));
	if '/python' in dir_path:
		dir_path = dir_path.split('/python')[0];
		dir_path = dir_path+config['CRAWLER_PATH'];
	return dir_path;
	
def openRealPath(path, arg='r', filepath=False, defaultPath='root'):
	if defaultPath == 'crawl':
		root_path = getCrawlPath();
	else:  
		root_path = getRootPath();
	if not root_path in path: # ensure absolute path
		absolute_path = "%s/%s"%(root_path,path);
	else:
		absolute_path = path;
	if filepath:
		return absolute_path;
	
	if os.path.exists(absolute_path):
		return open(absolute_path, arg);
	return None;
# def getEnv():
#   if (int(os.getenv('LIVE', 0)) <=0):
#     env = json.load(openRealPath('../.env'));
#     print(env);
#     for e in env.keys():
#       #print(e, env[e]);
#       os.putenv(e, str(env[e]));
#       os.environ[e] = str(env[e]);
#   return os.environ;
config = basic.getConfig();#json.load(openRealPath('../config.json'));

def thousandify(n):
	#return locale.format("%d", n, grouping=True);
	return "{:,}".format(n);

def getRealValue(text):
	units = {
		'k':3,
		'm':6,
		'b':9
	}
	try:
		value = text.lower().replace(',','');
		for u in units.keys():
			if u in value:
				value = float(value.replace(u, ''))*pow(10, units[u]);
				break;
		return int(value);
	except Exception as e:
		print('fn.getRealValue',text, e);
		return 0;


def millify(n): #convert number into human readable
	number_seperator = ['', 'K','M','B','T'];
	millify_counter = 0;
	remainder = n;
	for x in range(0, len(number_seperator)):
		if(int(remainder/1000)>0):
			millify_counter+=1;
			remainder = float(remainder/1000);
	return "%s%s"%(round(remainder,1), number_seperator[millify_counter]);
def serialize(data):
	key = None;
	# from datetime import datetime;
	if type(data) == dict:
		key = data.keys();
	elif type(data) == list:
		key = range(0, len(data));

	if key:
		for x in key:
			if type(data[x]) == datetime:
				data[x] = str(data[x]);
			elif type(data[x]) in [dict, list]:
				data[x] = serialize(data[x]);

	return data;
def dumps(data, encode=True, indent=4):
	data = serialize(data);
	if indent == 0:
		raw = json.dumps(data, indent=None, separators=(',',':'), cls=NpEncoder);
	else:
		raw = json.dumps(data, indent=indent, cls=NpEncoder);

	if encode:
		return raw.encode('utf-8');
	else:
		return raw;

def isAlphaNum(string, symbol=[], exclude=[]):
	has_alpha = 0;
	has_number = 0;
	has_symbol = 0;
	if string not in exclude:
		for s in string:
			if s.isalpha():
				has_alpha += 1;
			if s.isnumeric():
				has_number += 1;
			for sym in symbol:
				if sym in string:
					has_symbol += 1
		if symbol:
			if has_number > 0 and has_alpha > 0 and has_symbol > 0:
				return True;
			else:
				return False;
		else:
			if has_number > 0 and has_alpha > 0:
				return True;
			else:
				return False;
	else:
		return False;

def convertToInt(string):
	result = string;
	if type(string) == str:
		try:
			string = string.replace(',', '');

			if '.' in string and (float(string) - int(string.split('.')[0]) == 0):
				string = string.split('.')[0];

			result = int(string);
		except Exception as ex:
			result = string;

	return result;

def isInteger(string):
	# print('string', string)
	result = False;
	if type(string) == str:
		try:
			string = string.replace(',', '');

			if '.' in string and (float(string) - int(string.split('.')[0]) == 0):
				string = string.split('.')[0];

			int(string);
			result = True;
		except Exception as ex:
			result = False;
	elif type(string) == int:
		result = True;
	elif type(string) == float:
		if math.isnan(string) == False:
			if string - int(string) == 0:
				result = True;
	else:
		# Logger.d('type isInteger', type(string));
		result = False;
	return result;

def isFloat(string):
	result = False;
	to_check = True;

	if type(string) == str:
		if '.' not in string and string.startswith('0') == True and string not in [0, '0']:
			to_check = False;
	# print('to_check', to_check)

	try:
		if math.isnan(float(string)) == True:
			# print('is nan')
			result = True;
			return result;
	except:
		pass;

	if to_check == True:
	# if type(string) == str and string.startswith('0') == False:
	# if type(string) == str:
		# print(float(string))
		try:
			string = string.replace(',', '');
			float(string);
			result = True;
		except Exception as ex:
			# print('test')
			result = False;
	elif type(string) == float:
		result = True;
	else:
		# Logger.d('type isFloat', type(string));
		result = False;

	return result;

def isBetween(a, x, b):
	return min(a, b) < x < max(a, b)

def hasAlphabet(string):
	result = False;
	for s in string:
		if s.isalpha():
			result = True;
			break;
	return result;

def getNestedElementByKey(json, name=""):
	if(json and name):
		if name in json:
			return json[name]; #name is exactly same as json
		elements = name.split(".");
		tmp = None;
		for e in elements:
			# Logger.v('Checking elements', e, tmp, json, name);
			if(not tmp):
				if(e in json):
					tmp = json[e];
				else:
					return None;
			elif(isInteger(e) and int(e) in tmp):
				tmp = tmp[int(e)];
			elif(isInteger(e) and int(e) < 0):
				tmp = tmp[int(e)];
			elif(isInteger(e) and int(e) == 0):
				tmp = tmp[int(e)];
			elif(e in tmp):
				# Logger.v('checking tmp', e, tmp);
				tmp = tmp[e];  
			else:
				return None;
		return tmp;
	return None;

def getNestedElement(json, keys_name="", default=None):
	if(json and keys_name):
		result = {};
		names = keys_name.split(', ');
		for name in names:
			result[name] = getNestedElementByKey(json, name);

		if keys_name in result:
			if result[keys_name] == None:
				return default;
			else:
				return result[keys_name];
		else:
			if result == None:
				return default;
			return result;
	return None;
def makeSpace(level):
	for x in range(1, level):
			print('\t', end='');

def getArrayElementAtIndex(array, index, default=None):
	try:
		return array[index];
	except IndexError:
		return default;

def show(data, keyname='data', level=1):
	if(type(data) == dict):
		for k in sorted(data.keys()):
			if type(data[k]) in [list, dict]:
				makeSpace(level);
				print('%s:'%k);
			show(data[k], k, level+1);
	elif(type(data) == list):
		makeSpace(level);
		if len(data)>0:
			data_type = type(data[0]);
			if data_type in [str, int, float]:
			#  show(data[0], level=level);
			#  print("%s\t:\t%s"%(keyname,data));
				print("%s"%data);
			elif len(data) == 1:
				print('[\n');
				show(data[0], level=level);
				makeSpace(level);
				print(']\n');
				# print('%s\t:\t[%s]'%(keyname,data[0]));
			else:
				print('%s\t:\t<List with length of %s>'%(keyname,len(data)));
		else:
			print('%s\n'%data);
	else:
		makeSpace(level);
		print("%s\t:\t%s\n"%(keyname,data));

def hash(elements):
	h = hashlib.new('ripemd160');
	for element in elements:
		h.update(str(element).encode('utf-8'));
	return h.hexdigest();

def ensureDirectory(path, is_absolute=False):
	# path = path.replace("\\", "/");
	path = path.rstrip('/');
	if not path:
		return False;
	root_path = getRootPath();
	# root_path = root_path.replace("\\", "/");
	if is_absolute == False:
		if root_path in path: # make sure path is a full path.
			absolute_path = path; 
		else:
			absolute_path = "%s/%s"%(root_path, path);
	else:
		absolute_path = path;
	if not os.path.exists(absolute_path):
		folders = path.split('/');
		if len(folders)>1:
			ensureDirectory("/".join(folders[:-1]), is_absolute=is_absolute);
		# print('**** {0} ****'.format(absolute_path));
		os.mkdir(absolute_path);
	if os.path.isdir(absolute_path):
		return True;
	return False;

def extractHashtag(sentences):
	return list(filter(None, set([re.sub(r"(\W+)$", "", j, flags = re.UNICODE) for j in set([i for i in sentences.lower().split() if i.startswith("#") and not '#' in i[1:]])])));

def extractTag(sentences):
	return list(filter(None, set([re.sub(r"(\W+)$", "", j, flags = re.UNICODE) for j in set([i for i in sentences.lower().split() if i.startswith("@") and not '@' in i[1:]])]))); 

def extractKeyword(sentences):
	return sentences.split();

db = None;

def getDatabase():
	global db;
	if (not db):
		from lib import db as dblib;
		db = dblib.Database();
	return db.connect(True, True);

def writeTestFile(filename, data, minified=True):
	ensureDirectory('{0}/tests/'.format(getRootPath()));
	filename = '{0}/tests/{1}.json'.format(getRootPath(), filename);
	return writeJSONFile(filename, data, minified);

def readJSONFile(filename):
	data = [];
	try:
		with open(filename, 'r') as f:
			data = json.loads(f.read());
	except Exception as e:
		Logger.e('readJSONFile', e);
	return data;

class NpEncoder(json.JSONEncoder):
		def default(self, obj):
				if isinstance(obj, np.integer):
						return int(obj)
				elif isinstance(obj, np.floating):
						return float(obj)
				elif isinstance(obj, np.ndarray):
						return obj.tolist()
				else:
						return super(NpEncoder, self).default(obj)
						
def writeJSONFile(filename, data, minified=True, is_absolute=False):
	ensureDirectory('/'.join(filename.split('/')[:-1]), is_absolute=is_absolute);
	f = open(filename, 'wb');
	f.write(dumps(data, indent=0 if minified else 4));
	f.close();
	return True;

def writeHTMLFile(filename, data):
	ensureDirectory('/'.join(filename.split('/')[:-1]));
	Html_file= open(filename, 'w');
	Html_file.write(data);
	Html_file.close();

def writeCsvFile(filename, data):
	with open('%s.csv'%(filename), 'w', newline='', encoding='utf-8-sig') as csvfile:
		writer = csv.writer(csvfile);
		for d in data:
			writer.writerow(d);

def readExcelFile(filename):
	df = pd.read_excel(filename, sheet_name=None);
	data = [];
	for key in df.keys():
		data += json.loads(df[key].to_json(orient="records", date_format='iso'));
	return data;
def writeExcelFile(filename, data, extension='xlsx', transpose=False, sheet_names=[], columns=[], index=True):
	ensureDirectory('/'.join(filename.split('/')[:-1]));
	while True:
		filepath = filename;
		if not filepath.endswith(extension):
			filepath = '{0}.{1}'.format(filename, extension);
		try:
			writer = pd.ExcelWriter(filepath, engine='xlsxwriter', options={ 'strings_to_urls': False } );
			if sheet_names:
				for sheet_name in sheet_names:
					if sheet_name in data:
						df = pd.DataFrame(data[sheet_name]);
						if transpose:
							df = df.transpose();
						Logger.v('Writing Sheets: {0}'.format(sheet_name));
						if columns:
							df.to_excel(writer, index=index, sheet_name=sheet_name, columns=columns);
						else:
							df.to_excel(writer, index=index, sheet_name=sheet_name);
			else:
				df = pd.DataFrame(data);
				if transpose:
					df = df.transpose();
				if columns:
					df.to_excel(writer, index=index, columns=columns);
				else:
					df.to_excel(writer, index=index);
			writer.save();
			Logger.v('Write Successful. Finish write file to {0}'.format(filepath));
			break;
		except Exception as ex:
			Logger.v('Unable to write file. Please close file ({0}) to allow rewrite.'.format(filename));
			Logger.e(ex);
			time.sleep(5);
		except (KeyboardInterrupt, SystemExit):
			return False;
	return True;

def isWordMatch(keyword, full_caption, options):
	condition = getNestedElement(options, 'condition', 'case');
	if condition == 'case':
		if keyword in full_caption:
			return True;
	elif condition == 'word':
		full_caption = full_caption.replace('\n', ' ');
		if keyword in full_caption.split(' '):
			return True;
	return False;
def capitalize(string, seperator=' '):
	parts = string.split(seperator);
	result = [];
	for p in parts:
		result.append(p.capitalize());
	return seperator.join(result);
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
		"""
		Call in a loop to create terminal progress bar
		@params:
				iteration   - Required  : current iteration (Int)
				total       - Required  : total iterations (Int)
				prefix      - Optional  : prefix string (Str)
				suffix      - Optional  : suffix string (Str)
				decimals    - Optional  : positive number of decimals in percent complete (Int)
				length      - Optional  : character length of bar (Int)
				fill        - Optional  : bar fill character (Str)
				printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
		"""
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filledLength = int(length * iteration // total)
		bar = fill * filledLength + '-' * (length - filledLength)
		print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
		# Print New Line on Complete
		if iteration == total: 
				print('\n');

def convertToSnakecase(string):
	return string.lower().replace(' ', '_');

def groupArrayByKey(data, unique_key_to_group='id', column_key_to_combine='value'):
	grouped_data = {};
	for d in data:
		unique_key = d[unique_key_to_group];
		if not unique_key in grouped_data:
			grouped_data[unique_key] = d;
		else:
			grouped_data[unique_key][column_key_to_combine] += d[column_key_to_combine];
	return list(grouped_data.values());

def removeDuplicate(datas, key='pid'):
	duplicate = [];
	new_result = [];
	for r in datas:
		if not r[key] in duplicate:
			duplicate.append(r[key]);
			new_result.append(r);
	return new_result;

def extractUsername(url):
	if url:
		url_parts = url.split('/');
		url_parts.reverse();
		for part in url_parts:
			if len(part) > 0:
				return part;
		return url_parts;
def getCurrentDirectory(file_path):
	return os.path.dirname(os.path.abspath(file_path));

def sortBySequence(data, sequence, remove_key=True):
	temp_result = {};
	if sequence:
		for seq in sequence:
			row = getNestedElement(data, seq, None);
			if row:
				temp_result.update({
					seq: row, 
				});
	else:
		temp_result = data;      
	if remove_key:
		result = list(temp_result.values());
	else:
		result = temp_result;
	return result; 

def convertToDate(columns, data, date_format='%Y-%m-%d', with_time=False, output_type='str'):
	data_columns = data.columns;
	# date_format = '%Y-%m-%d';
	if with_time:
		date_format = '%Y-%m-%d %H:%M:%S';
	for col in columns:
		if col in data_columns:
			date_list = data[col].unique().tolist();
			date_mapping = {};
			for date in date_list:
				if DateTime.isTimestamp(date):
					dt_date = DateTime.convertDateTimeFromTimestamp(date);
				elif type(date) == str:
					dt_date = DateTime.convertDateTimeFromString(date);
				else:
					dt_date = None;
				if dt_date:
					date_value = DateTime.toString(date=dt_date, date_format=date_format);
					date_mapping[date] = date_value;
				else:
					date_mapping[date] = None;

			data[col] = data[col].map(date_mapping);
			if output_type == 'datetime':
				data[col] = pd.to_datetime(data[col]);
			elif output_type == 'datetime_int':
				data[col] = pd.to_datetime(data[col]);
				data.loc[data[col].notnull(), col] = data[data[col].notnull()][col].astype(int);
	return data;

def convertPctToDecimal(pct):
	if type(pct) == str:
		if pct.endswith('%'):
			pct = float(pct.rstrip('%'));
			pct = pct/100;
	return pct;

def scientificToNumeric(scientific_notation):
	result = scientific_notation;
	if type(scientific_notation) == str:
	# if isFloat(scientific_notation) == False:
		# print('result', result)
		# print('scientific_notation', scientific_notation)
		if 'e' in scientific_notation:
			real_number = float(scientific_notation.split('e')[0]);
			power = float(scientific_notation.split('e')[1]);
			result = real_number * (10 ** power); 
			# print('real_number', real_number)
			# print('power', power)
			# print('result', result)
	return result;

def convertToNumeric(columns, data):
	data_columns = data.columns;
	for col in columns:
		# print('col', col)
		if col in data_columns:
			is_str = [True for c in data[col].unique().tolist() if type(c) == str];
			if len(is_str) > 0 and all(is_str) == True:
				is_str = True;
			else:
				is_str = False;

			mapping = {};
			for value in data[col].unique().tolist():
				if DateTime.isDate(value) == True:
					# print('value', type(value), value, col, DateTime.isDate(value));
					if DateTime.convertDateTimeFromString(value) is not None:
						cleaned_value = 0;
					else:
						cleaned_value = value;
				else:
					cleaned_value = value;

				mapping[value] = cleaned_value;

			data[col] = data[col].map(mapping);

			if data[col].dtype == object and is_str == True:
				
				# print('qwe', data[~(data[col].isna())])
				# print('zxc', data[( ~(data[col].isna()) & data[col].str.contains('e-'))])
				# print('asd', data[data[col].str.contains('e-')])

				# data.loc[(data[col].str.contains('e-') & ~(data[col].isna())), col] = 0;
				data.loc[(~(data[col].isna()) & data[col].str.contains('e-')), col] = 0;
				data.loc[(~(data[col].isna()) & data[col].str.contains('#DIV/0!')), col] = 0;
				
				# data.loc[(~(data[col].isna()) & data[col].str.contains('e-')), col] = data[col].apply(lambda x: scientificToNumeric(x));
				data.loc[:, col] = data[col].apply(lambda x: convertPctToDecimal(x));
				# data[col] = data[col].apply(lambda x: convertPctToDecimal(x));
				try:
					data.loc[:, col] = data[col].str.replace(',', '');
					data.loc[:, col] = data[col].str.replace('"', '');
					data.loc[:, col] = data[col].str.split(' ').str[0];

					# data[col] = data[col].str.replace(',', '');
					# data[col] = data[col].str.replace('"', '');
					data.loc[(data[col] == '-'), col] = 0;
				except Exception as e:
					# Logger.e('convertToNumeric', e);
					pass;

				data.loc[:, col] = data[col].replace(r'^\s*$', np.nan, regex=True);
				# print (data[pd.to_numeric(data[col], errors='coerce').isnull()])
				data.loc[:, col] = pd.to_numeric(data[col]);
				data.loc[(data[col].isna()), col] = 0;
				# data[col] = data[col].replace(r'^\s*$', np.nan, regex=True)
				# data[col] = pd.to_numeric(data[col]);
				# data[col] = data[col].fillna(0);
			elif col in data_columns and data[col].dtype.name == 'category':
				# data[col] = data[col].replace(r'^\s*$', np.nan, regex=True)
				# data[col] = pd.to_numeric(data[col]);
				# data[col] = data[col].fillna(0);

				data.loc[:, col] = data[col].replace(r'^\s*$', np.nan, regex=True);
				try:
					data.loc[:, col] = data[col].str.replace(',', '');
					data.loc[:, col] = data[col].str.replace('"', '');
					data.loc[(data[col] == '-'), col] = 0;
				except Exception as e:
					# Logger.e('convertToNumeric', e);
					pass;

				data.loc[:, col] = pd.to_numeric(data[col]);
				data.loc[(data[col].isna()), col] = 0;

	return data;

def renameDFColumn(column_keymap, data, mode=None, add_missing_column=False):
	for col in data.columns:
		col = str(col);
		new_col = ' '.join([c for c in col.strip().split(' ') if c]);
		if mode:
			if mode == 'upper':
				new_col = new_col.upper();
			elif mode == 'lower':
				new_col = new_col.lower();
			elif mode == 'snakecase':
				new_col = convertToSnakecase(new_col);
			elif mode == 'upper_snakecase':
				new_col = new_col.replace(' ', '_').upper();

		if col not in column_keymap and col != new_col:
			column_keymap.update({
				col: new_col,	
			});

	data = data.rename(columns=column_keymap, inplace=False);
	if add_missing_column:
		for col in list(column_keymap.keys()):
			new_col = str(column_keymap[col]);
			new_col = ' '.join([c for c in new_col.strip().split(' ') if c]);
			if new_col not in data.columns:
				data[new_col] = None;

	return data;

def excelColumnString(n):
	string = '';
	while n > 0:
		n, remainder = divmod(n - 1, 26);
		string = chr(65 + remainder) + string;
	return string;

def generatePivotTable(data, group_by, aggfunc, columns=None, percentage_key=None, dropna=True, margins=False, margins_name='All', ignore_agg_error=False):
	if ignore_agg_error == True:
		new_agg = {};
		for column in list(aggfunc.keys()):
			if column in data.columns:
				new_agg[column] = aggfunc[column];
		aggfunc = new_agg;
	table = pd.pivot_table(data, values=list(aggfunc.keys()), index=group_by, aggfunc=aggfunc, columns=columns, dropna=dropna, margins=margins, margins_name=margins_name);
	pivot_table = table.reset_index(level=group_by);
	if percentage_key:
		for pk in percentage_key:
			column_name = '{0}_percentage'.format(pk);
			if pivot_table[pk].sum() > 0:
				pivot_table[column_name] = pivot_table[pk] / pivot_table[pk].sum() * 100;
			else:
				pivot_table[column_name] = 0;
	return pivot_table;

def retrieveColumnInfo(columns, column_names, offset=0):
	result = {
		'idx': None,
		'name': None,
	}
	stop = False;
	for column_name in column_names:
		# print(column_name)
		for idx, column in enumerate(columns):
			# print('column', idx, column_name.strip().lower(), str(column).strip().lower(), column_name.strip().lower() == str(column).strip().lower())
			# if column_name == 'Avg 2 max (last 6 mths)':
				# print('column', column_name.strip().lower(), str(column).strip().lower(), column_name.strip().lower() == str(column).strip().lower())
			# 	print('idx', idx, (len(columns) - 1))
			if column_name.strip().lower() == str(column).strip().lower():
				if offset and idx != 0 and idx != (len(columns) - 1):
					result['idx'] = idx + offset;
					result['name'] = columns[idx + offset];
				else:
					result['idx'] = idx;
					result['name'] = column;
				# print(column_name, result);
				stop = True;
				break;
		if stop:
			break;
	return result;

def OOSByRow(c2_bal_outlet, total_outlet):
	if math.isnan(c2_bal_outlet):
		c2_bal_outlet = 0;
	if math.isnan(total_outlet):
		total_outlet = 0;

	if c2_bal_outlet > total_outlet:
		result = 0;
	elif total_outlet == 0:
		result = 0;
	else:
		result = 1 - (c2_bal_outlet/total_outlet);
	return result;

def turnoverByRow(sales_qty, balance):
	if math.isnan(sales_qty):
		sales_qty = 0;
	if math.isnan(balance):
		balance = 0;

	if sales_qty == 0 and balance == 0:
		result = 0;
	elif balance == 0:
		result = 0;
	elif sales_qty > balance:
		result = 1;
	else:
		result = sales_qty / balance;
	return result;

def excelRank(data, ascending=True):
	# round_data = data.round(4);

	# mapping_dict = {};
	# print(sorted(data['OVERALL|AVG_SCORE'].unique().tolist()));
	# exit()
	if ascending == True:
		reverse = False;
	else:
		reverse = True;



	# score_list = sorted(data.unique().tolist(), reverse=reverse);
	# for idx, d in enumerate(score_list):
	# 	mapping_dict[d] = idx;

	mapping_dict2 = {};
	# list2 = sorted(list(mapping_dict.values()), reverse=reverse);
	list2 = sorted(data.tolist(), reverse=reverse);
	for idx, d in enumerate(list2):
		if d not in mapping_dict2:
			mapping_dict2[d] = idx + 1;

	# data['OVERALL|AVG_SCORE1'] = data['OVERALL|AVG_SCORE'].map(mapping_dict);
	result = data.map(mapping_dict2);
	return result;

def reduceMemUsage(df, blacklist_cols=None):
	"""
	Iterate through all the columns of the dataframe and downcast the
	data type to reduce memory usage.

	The logic is numeric type will be downcast to the smallest possible
	numeric type. e.g. if an int column's value ranges from 1 - 8, then it
	fits into an int8 type, and will be downcast to int8.
	And object type will be converted to categorical type.

	Parameters
	----------
	df : pd.DataFrame
		Dataframe prior the memory reduction.

	blacklist_cols : collection[str], e.g. list[str], set[str]
		A collection of column names that won't go through the memory
		reduction process.

	Returns
	-------
	df : pd.DataFrame
		Dataframe post memory reduction.

	References
	----------
	https://www.kaggle.com/gemartin/load-data-reduce-memory-usage
	"""
	start_mem = compute_df_total_mem(df)
	# print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
	column_types = {};

	blacklist_cols = blacklist_cols if blacklist_cols else set()
	for col in df.columns:
		if col in blacklist_cols:
			continue
		
		col_type = df[col].dtype
		column_types[col] = col_type;
		if col_type != object and not all([True for c in df[col].dropna().unique().tolist() if pd.isna(c) == False]):
			c_min = df[col].min()
			c_max = df[col].max()
			if str(col_type)[:3] == 'int':
				if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
					df[col] = df[col].astype(np.int8)
					column_types[col] = 'np.int8';
				elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
					df[col] = df[col].astype(np.int16)
					column_types[col] = 'np.int16';
				elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
					df[col] = df[col].astype(np.int32)
					column_types[col] = 'np.int32';
				else:
					df[col] = df[col].astype(np.int64)  
					column_types[col] = 'np.int64';
			else:
				if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
					df[col] = df[col].astype(np.float16)
					column_types[col] = 'np.float16';
				elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
					df[col] = df[col].astype(np.float32)
					column_types[col] = 'np.float32';
				else:
					df[col] = df[col].astype(np.float64)
					column_types[col] = 'np.float64';
		elif len(df[col].unique().tolist()) < (len(df) / 4):
			df[col] = df[col].astype('category')
			column_types[col] = 'category';
		else:
			pass

	end_mem = compute_df_total_mem(df)
	# print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
	# print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
	# print('column_types', column_types);
	return df
	
def compute_df_total_mem(df):
	"""Returns a dataframe's total memory usage in MB."""
	return df.memory_usage(deep=True).sum() / 1024 ** 2