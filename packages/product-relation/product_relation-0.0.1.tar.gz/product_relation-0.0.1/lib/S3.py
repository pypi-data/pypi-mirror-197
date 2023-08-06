import boto3;
import botocore;
from botocore.errorfactory import ClientError
import requests;
import tempfile;
import json; 
import os;
import pandas as pd;
import io;

from urllib.request import Request, urlopen;
from lib import fn;
from lib import Logger;
from lib import File;

cache = {};
def clearCache():
	global cache;
	cache = {};
def getRegionName():
	return fn.getNestedElement(fn.config, 'aws_region');
def getBucketName():
	return fn.getNestedElement(fn.config, 'aws_bucket');
def getDataBucketName():
	return fn.getNestedElement(fn.config, 'aws_data_bucket');
def getEIOSBucketName():
	return fn.getNestedElement(fn.config, 'aws_eios_bucket', 'eios');
def getAbbottMyBucketName():
	return fn.getNestedElement(fn.config, 'aws_abbott_my_bucket', 'abbott-my');

def connect(client=False):
	if not client:
		s3 = boto3.resource('s3',
			aws_access_key_id=fn.getNestedElement(fn.config, 'aws_access_key'),
			aws_secret_access_key=fn.getNestedElement(fn.config, 'aws_access_secret')
		);
	else:
		s3 = boto3.client('s3',
			aws_access_key_id=fn.getNestedElement(fn.config, 'aws_access_key'),
			aws_secret_access_key=fn.getNestedElement(fn.config, 'aws_access_secret')
		);
	return s3;

def init(bucket_name):
	s3 = connect();
	bucket = s3.Bucket(bucket_name);

	# for bucket in s3.buckets.all():
	#  	print(bucket.name);
	return bucket;

def listAll(bucket_name = getBucketName()):
	bucket = init(bucket_name);
	# for b in bucket.objects.all():
	# 	print(b);
	return bucket.objects.all();

def generateDirectory(page_type, upid):
	return '%s/%s'%(page_type, upid);

def generateProfileDirectory(page_type, platform):
	return '%s/%s'%(page_type, platform);	

def generateUrl(key, bucket_name = getBucketName()):
	region = getRegionName();
	return 'https://%s.amazonaws.com/%s/%s'%(region, bucket_name, key.replace(" ", "%20"));

def listDirectoryFiles(directory, bucket_name = getDataBucketName()):
	files = listDirectory(directory, bucket_name);
	return [fn.getNestedElement(x, 'Key') for x in files];

def listDirectory(directory, bucket_name = getDataBucketName(), use_cache=False):
	global cache;
	if use_cache:
		if not directory in cache.keys():
			data = getDirectoryFiles(directory, bucket_name);
			cache[directory] = data;
	else:
		data = getDirectoryFiles(directory, bucket_name);
		cache[directory] = data;
	return cache[directory];

def getDirectoryFiles(directory, bucket_name = getDataBucketName()):
	s3 = connect(client=True);
	s3args = {
		'Bucket':bucket_name,
		'Prefix':directory
	};
	data = [];
	page = 0;
	while True:
		response = s3.list_objects_v2(**s3args);
		data += response.get('Contents', []);
		page +=1;
		try:
			s3args['ContinuationToken'] = response['NextContinuationToken'];
		except KeyError:
			break;

	Logger.v('Cache S3 Directory for folder:%s, page:%s, files:%s'%(directory , page, len(data)));
	return data;

def hasFile(keyname, bucket_name=getBucketName()):
	try:
		directory = '/'.join(keyname.split('/')[:-1]);
		filename =keyname.split('/')[-1];
		# print(directory);
		files = listDirectory(directory, bucket_name);
		# print(bucket.get_key(filename, headers=None, version_id=None, response_headers=None, validate=True));
		# s3.head_object(Bucket=getBucketName(), Key=filename)
		for obj in files:
			# print(obj);
			if obj['Key'] == keyname:
				return True;
			# 	return obj['Size']
	except ClientError:
		pass;
	return False;

def readLatestFile(directory, extension='.json',bucket_name=getDataBucketName()):
	s3 = connect();
	data = {};
	directories = listDirectory(directory, bucket_name);
	fn.show(directories);
	filtered_file = list(filter(lambda x: x['Key'].endswith(extension), directories));
	sorted_file = sorted(filtered_file, key=lambda x: x['LastModified'], reverse=True);
	if sorted_file:
		latest_file = sorted_file[0]['Key'];
		data = read([latest_file], bucket_name)[latest_file];
	return data;


cache_directory = "/".join([fn.getCrawlPath(), 'cache']);
# Logger.v('Cache Directory:',cache_directory);
def cleanFilename(filename):
	return filename.replace(':', '');
def loadCache(key):
	global cache_directory;
	try:
		filename = cleanFilename(key);
		Logger.v('check filename', filename);
		return fn.readJSONFile('{0}/{1}'.format(cache_directory, filename));
	except Exception as ex:
		Logger.e('loadCache Fail,', key);
		return None;
def saveCache(key, data):
	global cache_directory;
	filename = cleanFilename(key);
	try:
		fn.writeJSONFile('{0}/{1}'.format(cache_directory, filename), data);
	except Exception as ex:
		Logger.e('S3.saveCache Failed: ',filename, ex);
		
def read(files=[], bucket_name=getDataBucketName(), filename_only=False, cache=True, encoding=True, chunk=False, chunk_size=10000, callback='', chunk_options=[], result_data={}):
	s3 = connect();
	data = {};
	for file in files:

		if filename_only:
			key_name = file.split('/')[-1].split('.')[0];
		else:
			key_name = file;

		cache_data = loadCache(key_name);
		if cache_data and cache:
			data[key_name] = cache_data;
		else:
			raw = s3.Object(bucket_name, file).get();
			extension = file.split('.')[-1];
			# Logger.v('Raw info', json.loads(raw['Body'].read().decode("utf-8")));
			data[key_name] = readFile(raw['Body'].read(), extension, encoding=encoding, chunk=chunk, chunk_size=chunk_size, callback=callback,chunk_options=chunk_options, result_data=result_data);
			saveCache(key_name, data[key_name]);
	return data;

def readFile(raw, extension, encoding=True, chunk=False, chunk_size=10000, callback='',chunk_options=[], result_data={}):
	if extension == 'xlsx':
		if encoding == True:
			df = pd.read_excel(io.BytesIO(raw), encoding='utf-8', sheet_name=None);
		else:
			df = pd.read_excel(io.BytesIO(raw), sheet_name=None, index_col=0);	
		data = [];
		for key in df.keys():
			data += json.loads(df[key].to_json(orient="records", date_format='iso'));
	elif extension == 'csv':
		if chunk:
			data = result_data;
			for chunk in pd.read_csv(io.BytesIO(raw), encoding='utf-8', chunksize=chunk_size):
				data = callback(chunk, chunk_options, data=data);
		else:
			df = pd.read_csv(io.BytesIO(raw), encoding='utf-8');
			data = df;
	else:
		data = json.loads(raw.decode("utf-8"));
	return data;

def save(source, destination, bucket_name=getBucketName()):
	bucket = init(bucket_name);
	# bucket.upload_file(source_file, target_file_path);
	result = bucket.upload_file(source, destination);
	return result;

def saveByData(data, filename, bucket_name= getDataBucketName(), returnTmpPath=False):
	with tempfile.NamedTemporaryFile(delete=False) as tmp:
		tmp.write(fn.dumps(data,indent=0)); #remove indent to minimize file
		tmp.close();
		if returnTmpPath:
			return {'tmp_path':tmp.name, 'filename':filename, 'bucket_name':bucket_name};
		save(tmp.name, filename, bucket_name);
		os.unlink(tmp.name);

	return generateUrl(filename, bucket_name);

def download(url, filename, overwrite=False):
	try:
		has_file = hasFile(filename, getBucketName());
		if not has_file or overwrite:
			if has_file:
				Logger.v('[S3 Download]%s Found, but overwriting image file.'%(filename));
			with tempfile.NamedTemporaryFile(delete=False) as tmp:
				Logger.v('downloading %s:'%filename, url);
				request = Request(url, headers={'User-Agent': 'Mozilla/5.0'});
				response = urlopen(request);
				content_type = response.getheader('Content-Type');
				if response.status == 200 and 'image' in content_type:
					web_byte = response.read();
					data = web_byte;
					tmp.write(data);
					tmp.close();
					save(tmp.name, filename);
					os.unlink(tmp.name);
				else:
					return None;
		return generateUrl(filename);
	except Exception as ex:
		Logger.e('Failed to cache image for %s'%filename);
		return None;

def uploadIfNotFound(keyname, bucket_name=getBucketName(), local_root=None):
	if local_root:
		keyname = keyname.replace(local_root, '');
		source = local_root + keyname;
		destination = keyname;
	else:
		source = keyname;
		destination = keyname;

	has_file = hasFile(keyname, bucket_name);
	print('has_file', has_file)
	if has_file == False:
		save(source, destination, bucket_name);
		print('save', destination)

def downloadDirectoryFroms3(remote_directory_name, bucket_name=getBucketName()):
	s3_resource = boto3.resource('s3')
	bucket = s3_resource.Bucket(bucket_name) 
	for obj in bucket.objects.filter(Prefix = remote_directory_name):
		if not os.path.exists(os.path.dirname(obj.key)):
			os.makedirs(os.path.dirname(obj.key))
		bucket.download_file(obj.key, obj.key) # save to same path