from . import *;
##
# { 'src':'type',
#   'target':'page_type',
#   'required':1
# }
def extract(obj, cols):
	total_required = len(cols);
	data = {};
	for key in cols:
		if type(key) == str:
			if key in obj:
				data[key] = obj[key];
		if type(key) == dict:
			src = fn.getNestedElement(key, 'src');
			target = fn.getNestedElement(key, 'target');
			required = fn.getNestedElement(key, 'required');
			default = fn.getNestedElement(key, 'default');
			classes = fn.getNestedElement(key, 'class');
			seperator  = fn.getNestedElement(key, 'seperator', ', ');
			if not required == None and required <0:
				total_required -=1;
			if target == None:
				target = src;
			if src in obj:
				data[target] = obj[src];
			elif 'default' in key:
				data[target] = default;
			#Logger.d("extract:", key, data[target],type(data[target]));
			if not classes == None and target in data and data[target]:
				if not type(data[target]) == classes: 
					if classes == list:

						if seperator in data[target]:
							data[target] = data[target].split(seperator);
						else:
							data[target] = [data[target]];
					#	Logger.d('change class', data);
					elif classes == str:
						data[target] = str(data[target]);
					elif classes == int:
						data[target] = int(data[target]);
	return data , len(data.keys()) >= total_required;

def refineElement(row, key_mapping):
	for m in key_mapping:
		src = m['src'];
		dest = m['dest'];
		remove = fn.getNestedElement(m, 'remove');
		data = fn.getNestedElement(row, src);
		if data:
			row[dest] = data;
			if remove:
				del row[src];
	return row;

def generate(valid, data, message=''):
	result = {};
	if not valid:
		result['success'] = False;
		if message == None:
			message = '';
		message += 'Not Enough Input Params.';

	if message:
		result['message'] = message;
		result['success'] = False;
		
	elif not data == None and not data == {}:
		result['success'] = True;
		if not type(data) == bool:
			result['data'] = data;
	else:
		result['success'] = False;

	return result;