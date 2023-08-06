from google.oauth2 import service_account
from lib import fn;
from lib import DebugManager;
from lib import File;
from lib import Logger;
import io;
import os;
import csv;
import copy;
import pandas as pd;
import time;
import json;
from time import sleep;
import googleapiclient.discovery
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
# from apiclient import errors
from googleapiclient.errors import HttpError

SERVICE_ACCOUNT_FILE = fn.getRootPath() + '/' +fn.getNestedElement(fn.config,'GDRIVE_SERVICE_ACC_FILE', None);
SCOPES = fn.getNestedElement(fn.config,'GDRIVE_SCOPES', None);
GDRIVE_SHARING = eval(fn.getNestedElement(fn.config,'GDRIVE_SHARING', '[]'));
ROOT_PATH = '';
CHILD_PARENT = {};
CACHE_FILE_LIST = {};
CACHE_FILE_ID = {};
CACHE_ID_MAPPING = {};
CACHE_FILE_INFO = {};
DRIVE_SERVICE = None;
DEFAULT_DRIVE_KEY='GDRIVE_ANALYTICS_DB';
RETRIEVE_ATTEMPT = 0;

def connect():
	global SCOPES, SERVICE_ACCOUNT_FILE;
	credentials = None;
	if SCOPES is not None and type(SCOPES) == str:
		SCOPES = eval(SCOPES);
	if SERVICE_ACCOUNT_FILE is None or SCOPES is None:
		Logger.e('No credential file, connection failed.');
	else:
		# print('SERVICE_ACCOUNT_FILE', SERVICE_ACCOUNT_FILE)
		# print('SCOPES', SCOPES)
		Logger.v('connect google drive');

		credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
		# credentials = service_account.Credentials.from_service_account_file(filepath, scopes=SCOPES)
		# print('credentials', credentials);

	return credentials;

def init():
	global DRIVE_SERVICE;
	# Debug = DebugManager.DebugManager();
	# Debug.start();
	# Debug.trace('start');
	service = None;
	credentials = connect();
	# Debug.trace('connect');
	try:
		service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
		DRIVE_SERVICE = service;
		# print('service', service);
	except Exception as e:
		Logger.e('Failed init', e);
	# Debug.trace('start service');
	# Debug.end();
	# Debug.show('GDrive init');
	return service;

def initSheet():
	global DRIVE_SERVICE;
	# Debug = DebugManager.DebugManager();
	# Debug.start();
	# Debug.trace('start');
	service = None;
	credentials = connect();
	# Debug.trace('connect');
	try:
		service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
		DRIVE_SERVICE = service;
		# print('service', service);
	except Exception as e:
		Logger.e('Failed init', e);
	# Debug.trace('start service');
	# Debug.end();
	# Debug.show('GDrive init');
	return service;

# Call the Drive v3 API

def scrapeParents(child_list, parent_child_pair):
	global CHILD_PARENT;
	print(child_list)
	for child in child_list:
		# print('child', child);
		if child not in CHILD_PARENT:
			CHILD_PARENT[child] = [];
		parents = fn.getNestedElement(parent_child_pair, child, []);
		for parent in parents:
		# if parent == False:
		# 	continue;
		# else:
			CHILD_PARENT[child].append(parent);
			# print('parent', parent, parent_child_pair)
			new_child_list = fn.getNestedElement(parent_child_pair, parent, []);
			if len(new_child_list) > 0:
				scrapeParents(child_list=new_child_list, parent_child_pair=parent_child_pair);


def insertPermission(file_id, service=None, sharing_permission=GDRIVE_SHARING):
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	# print('GDRIVE_SHARING', GDRIVE_SHARING, type(GDRIVE_SHARING))
	for permission in sharing_permission:
		service.permissions().create(fileId=file_id, body=permission, sendNotificationEmail=False, supportsAllDrives=True).execute();
	return;

def getFileById(file_id, service=None, cache=False):
	global CACHE_FILE_INFO;
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	file = None;

	if cache == True and fn.getNestedElement(CACHE_FILE_INFO, file_id, None):
		file = fn.getNestedElement(CACHE_FILE_INFO, file_id, None);
	else:
		try:
			file = service.files().get(fileId=file_id, fields='id, name, mimeType, parents', supportsAllDrives=True).execute();
			# print('run google', cache, file_id);
			# print('file id', file['id'])
			# print ('Title: %s' % file['name'])
			# print ('MIME type: %s' % file['mimeType'])
		except Exception as error:
			Logger.e('An error occurred: %s' % error);

	CACHE_FILE_INFO[file_id] = file;
	return file;

def getFileInformationById(file_id, service=None, cache=False):
	parent_id = file_id;
	children_parent_pair = {};
	item_detail_list = {};
	is_root = False;

	if parent_id not in children_parent_pair:
		children_parent_pair[parent_id] = [];

	while is_root == False:
		file = getFileById(service=service, file_id=parent_id, cache=cache);
		if file is not None:
			item_parents = fn.getNestedElement(file, 'parents', []);
			item_id = fn.getNestedElement(file, 'id', '');
			item_name = fn.getNestedElement(file, 'name', '');
			item_mime_type = fn.getNestedElement(file, 'mimeType', '');
			if len(item_parents) > 0:
				# if item_parents[0] not in parent_child_pair:
				# 	parent_child_pair[item_parents[0]] = [];
				# parent_child_pair[item_parents[0]].append(item_id);
				# parent_child_pair[item_parents[0]] = sorted(parent_child_pair[item_parents[0]]);
				
				if item_id not in item_detail_list:
					item_detail_list[item_id] = {
						'id': item_id,
						'name': item_name,
						'mimeType': item_mime_type,
						'parents': item_parents
					};
				
				children_parent_pair[file_id].append(item_id);

				parent_id = item_parents[0];
			else:
				is_root = True;
		else:
			is_root = True;

	file_information = {};
	for child in children_parent_pair:
		child_name = fn.getNestedElement(item_detail_list, '{0}.name'.format(child), '');
		mime_type = fn.getNestedElement(item_detail_list, '{0}.mimeType'.format(child), '');
		parents = children_parent_pair[child];
		path_elements = [];
		is_folder = False;

		if mime_type == 'application/vnd.google-apps.folder':
			is_folder = True;

		if child not in file_information:
			file_information[child] = {
				'id':child,
				'name': 'child_name',
				'is_folder': is_folder,
				'path': '',
			};

		for idx in range(len(parents)-1, -1, -1):
			parent = parents[idx];
			parent_name = fn.getNestedElement(item_detail_list, '{0}.name'.format(parent), '');
			path_elements.append(parent_name);

		file_information[child]['path'] = '/'.join(path_elements);
	return file_information;

def getFilepathById(file_id, service=None, cache=False):
	global CACHE_ID_MAPPING;
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();

	if cache == True and fn.getNestedElement(CACHE_ID_MAPPING, file_id, None):
		filepath = fn.getNestedElement(CACHE_ID_MAPPING, file_id, None);
	else:
		file_information = getFileInformationById(file_id, service, cache=cache);
		filepath = fn.getNestedElement(file_information, '{0}.path'.format(file_id), None);
	CACHE_ID_MAPPING[file_id] = filepath;
	return filepath;

def getDriveId(drive_key=DEFAULT_DRIVE_KEY):
	return fn.getNestedElement(fn.config, drive_key);

def getFolderId(directory, service=None, cache=False, drive_key=DEFAULT_DRIVE_KEY):
	global CACHE_FILE_ID;
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	folder_id = None;
	directory = cleanFilepath(directory);

	if directory is not None:
		if cache == True and fn.getNestedElement(CACHE_FILE_ID, directory, None):
			folder_id = fn.getNestedElement(CACHE_FILE_ID, directory, None);
		else:
			split_dir = directory.split('/');
			folder_name = directory.split('/')[-1];
			query = "trashed=false and (mimeType = 'application/vnd.google-apps.folder') and (name = '{0}')".format(folder_name);
			# print('query getFolderId', query);
			response = service.files().list(
						pageSize=50, fields="nextPageToken, files(id, name, mimeType, parents)", corpora="drive", driveId=getDriveId(drive_key), includeItemsFromAllDrives=True,
						supportsAllDrives=True, q=query).execute();

			items = response.get('files', []);
			# print('folder length', len(items));
			for item in items:
				item_id = item['id'];
				item_mime_type = item['mimeType'];
				filepath = getFilepathById(file_id=item_id, service=service, cache=cache);
				if filepath == directory and item_mime_type == 'application/vnd.google-apps.folder':
					folder_id = item_id;
					break;
	CACHE_FILE_ID[directory] = folder_id;
	return folder_id;

def clearCacheFile():
	global CACHE_FILE_LIST, CACHE_FILE_ID, CACHE_ID_MAPPING;
	CACHE_FILE_LIST = {};
	CACHE_FILE_ID = {};
	CACHE_ID_MAPPING = {};

def cleanFilepath(filepath):
	if filepath is not None:
		filepath = filepath.strip('/');
		filepath = '/'.join([c for c in filepath.split('/') if c is not None and c != '']);
	return filepath;

def getDirectoryFiles(directory=None, drive_id=getDriveId(drive_key=DEFAULT_DRIVE_KEY), service=None, cache=False, drive_key=DEFAULT_DRIVE_KEY, include_subdir=True):
	global CACHE_FILE_LIST;
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	data = [];
	page = 0;
	check_files = True;
	next_page_token = None;
	query = "trashed=false";
	if drive_id is None:
		drive_id = getDriveId(drive_key=drive_key);
	directory = cleanFilepath(directory);
	folder_id = getFolderId(directory, service, cache, drive_key);
	if folder_id is None and directory is not None:
		check_files = False;
	elif folder_id is not None:
		query += " and '{0}' in parents".format(folder_id);
	# print('cache', cache);

	while check_files == True:
		if cache == True and fn.getNestedElement(CACHE_FILE_LIST, directory, []):
			data += fn.getNestedElement(CACHE_FILE_LIST, directory, []);
			check_files = False;
		else:
			# print('checking drive', directory, fn.getNestedElement(CACHE_FILE_LIST, directory, []), cache)
			# print('query getDirectoryFiles', query);
			if next_page_token is None:
				response = service.files().list(
					pageSize=50, fields="nextPageToken, files(id, name, mimeType, parents)", corpora="drive", driveId=drive_id, includeItemsFromAllDrives=True,
					supportsAllDrives=True, q=query).execute();
			else:
				response = service.files().list(
					pageSize=50, fields="nextPageToken, files(id, name, mimeType, parents)", corpora="drive", driveId=drive_id, includeItemsFromAllDrives=True,
					supportsAllDrives=True, pageToken=next_page_token, q=query).execute();

			data += response.get('files', []);
			try:
				next_page_token = response['nextPageToken'];
			except KeyError:
				check_files = False;
		page +=1;

	CACHE_FILE_LIST[directory] = data;

	temp_data = [];
	if include_subdir == False:
		for row in data:
			mime_type = row['mimeType'];
			if mime_type != 'application/vnd.google-apps.folder':
				temp_data.append(row);
		data = temp_data;
		
	# Logger.v('Cache S3 Directory for folder:%s, page:%s, files:%s'%(directory , page, len(data)));
	return data;

def retrieveFileId(filepath, service=None, cache=False, drive_key=DEFAULT_DRIVE_KEY):
	global CACHE_FILE_ID, RETRIEVE_ATTEMPT;
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	filepath = cleanFilepath(filepath);
	# print('cache retrieveFileId', cache)
	result = None;
	if cache == True and fn.getNestedElement(CACHE_FILE_ID, filepath, None):
		result = fn.getNestedElement(CACHE_FILE_ID, filepath, None);
	else:
		has_file, file_info = hasFile(filepath, service, cache=cache, drive_key=drive_key);
		# print('has_file', has_file, file_info, drive_key)
		if has_file == True:
			result = file_info['id'];
	# print('RETRIEVE_ATTEMPT', RETRIEVE_ATTEMPT);
	if RETRIEVE_ATTEMPT == 0:
		if result is None:
			RETRIEVE_ATTEMPT += 1;
			print('retry retrieving', filepath);
			service = init();
			result = retrieveFileId(filepath, service=service, cache=False, drive_key=drive_key);
	else:
		RETRIEVE_ATTEMPT = 0;
		CACHE_FILE_ID[filepath] = result;
		return result;
	CACHE_FILE_ID[filepath] = result;
	# print('RETRIEVE_ATTEMPT after', RETRIEVE_ATTEMPT);
	return result;

def hasFile(filepath, service=None, cache=False, drive_key=DEFAULT_DRIVE_KEY):
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	filepath = cleanFilepath(filepath);
	items = getDirectoryFiles(directory='/'.join(filepath.split('/')[:-1]), drive_id=None, service=service, cache=cache, drive_key=drive_key);
	file_id = None;
	has_file = False;
	file_info = {};
	for item in items:
		item_filepath = getFilepathById(file_id=item['id'], service=service, cache=cache);
		# print('item_filepath', item_filepath);
		# print('filepath', filepath);
		# print('filepath', filepath == item_filepath);
		if filepath == item_filepath:
			file_id = item['id'];
			has_file = True;
			file_info = item;
			# print('filepath', filepath);
			# print('file_id', file_id);
			break;
	return has_file, file_info;

def exportExcelWithId(file_id, destination, cache=False):
	excel_mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
	service = init();
	if file_id is not None:
		try:
			byte_data = service.files().export(fileId=file_id, mimeType=excel_mime).execute();
			with open(destination, 'wb') as f:
				f.write(byte_data);
				f.close();
			df = File.readExcelToDF(destination, sheet_name=None);
			print(df);
		except Exception as e:
			Logger.e('exportExcelWithId', e);

def exportCsvBySheetWithId(file_id, destination, sheetname, cache=False):
	service = initSheet();
	if file_id is not None:
		try:
			response = service.spreadsheets().values().get(spreadsheetId=file_id, range=sheetname).execute();
			with open(destination, 'w') as f:
				writer = csv.writer(f)
				writer.writerows(response.get('values'))
			f.close()
			
		except Exception as e:
			Logger.e('exportCsvBySheetWithId', e);


def downloadFileWithId(file_id, destination, cache=False):
	service = init();
	if file_id is not None:
		# print('file_id', file_id)
		filename = destination;
		# filename = 'output_data/drive_cache/{0}'.format(filepath);
		if os.path.exists(filename) and cache == True:
			return filename;
		else:
			# file_id = '0BwwA4oUTeiV1UVNwOHItT0xfa2M'
			# print('test')
			# request = service.files().get(fileId=file_id).execute();
			proceed_download = False;
			try:
				request = service.files().get_media(fileId=file_id).execute();
				proceed_download = True;
			except HttpError as t:
				Logger.e('HttpError', t.resp)

			except Exception as e:
				Logger.e('exception', e)

			if proceed_download == True:
				# print('downloading:', file_id, service.files().get(fileId=file_id))
				print('downloading:', filename)
				request = service.files().get_media(fileId=file_id)
				fh = io.FileIO(filename, 'wb')
				downloader = MediaIoBaseDownload(fh, request)
				done = False
				while done is False:
					status, done = downloader.next_chunk()
					# print ("Download %d%%." % int(status.progress() * 100))
				if done == True:
					return filename;
	else:
		Logger.e('File not exist', file_id);

def downloadFile(filepath, destination, service=None, cache=False, drive_key=DEFAULT_DRIVE_KEY, absolute_path=True):
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();

	filepath = cleanFilepath(filepath);
	# print('cache downloadFile', cache)
	file_id = retrieveFileId(filepath, service, cache, drive_key);
	# print('filepath', filepath)
	# print('file_id', file_id)
	if file_id is not None:
		# print('file_id', file_id)
		filename = destination;
		# filename = 'output_data/drive_cache/{0}'.format(filepath);
		if os.path.exists(filename) and cache == True:
			return filename;
		else:
			# file_id = '0BwwA4oUTeiV1UVNwOHItT0xfa2M'
			request = service.files().get_media(fileId=file_id)
			print('downloading:', filepath)
			fn.ensureDirectory('/'.join(filename.split('/')[:-1]), is_absolute=absolute_path);
			fh = io.FileIO(filename, 'wb')
			downloader = MediaIoBaseDownload(fh, request)
			done = False
			while done is False:
				status, done = downloader.next_chunk()
				# print ("Download %d%%." % int(status.progress() * 100))
			if done == True:
				return filename;
	else:
		Logger.e('File not exist', filepath);

def readFile(filepath, destination, service=None, cache=False, dtype=str, drive_key=DEFAULT_DRIVE_KEY, absolute_path=True):
	# Debug = DebugManager.DebugManager()
	# Debug.start()
	# Debug.trace('start')
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	# print('cache readFile', cache)
	filepath = cleanFilepath(filepath);
	file = downloadFile(filepath, destination=destination, service=service, cache=cache, drive_key=drive_key, absolute_path=absolute_path);
	# Debug.trace('download')
	# print('readFile', file)
	if file is not None:
		df = File.readToDF(file, dtype=dtype);
	else:
		df= pd.DataFrame();
	# Debug.trace('read')
	# Debug.end()
	# Debug.show()
	# print(df)
	return df;

def ensureDirectory(directory, service=None, cache=False, drive_key=DEFAULT_DRIVE_KEY):
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	directory = cleanFilepath(directory);
	joined_folder = [];
	directory_elements = directory.split('/');
	saving_folder_id = None;
	# print('directory', directory)
	# print('directory_elements', directory_elements)
	for idx in range(0, len(directory_elements)):
		temp = [];
		for idx2, folder in enumerate(directory_elements):
			temp.append(folder);
			if idx2 == idx:
				break;
		joined_folder.append('/'.join(temp));
	# print('joined_folder', joined_folder)

	folder_mapping = {};
	for idx, folder in enumerate(joined_folder):
		if idx == 0:
			parent_id = getDriveId(drive_key);
		else:
			parent_id = folder_mapping[joined_folder[idx-1]];
		folder_id = getFolderId(folder, service, cache, drive_key);
		if folder_id is None:
			folder_id = createNewFolder(folder, parent_id, service, drive_key);
		folder_mapping[folder] = folder_id;

	save_folder_id = fn.getNestedElement(folder_mapping, directory, None)
	return save_folder_id;

def createNewFolder(directory, parent_id=None, service=None, drive_key=DEFAULT_DRIVE_KEY):
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	if parent_id is None:
		parent_id = getDriveId(drive_key);
	directory = cleanFilepath(directory);
	folder_name = directory.split('/')[-1];
	file_metadata = {
		'name': folder_name,
		'mimeType': 'application/vnd.google-apps.folder',
		'parents': [parent_id],
	}
	file = service.files().create(body=file_metadata, fields='id', supportsAllDrives=True).execute()
	# print 'Folder ID: %s' % file.get('id')
	return file['id'];

def uploadFile(filepath, local_file, service=None, cache=False, drive_key=DEFAULT_DRIVE_KEY, folder_id=None):
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	filepath = cleanFilepath(filepath);
	extension = filepath.split('.')[-1];
	filename = filepath.split('/')[-1];
	has_file, file_info = hasFile(filepath=filepath, service=service, cache=cache, drive_key=drive_key);
	# has_file = False;
	if extension == 'csv':
		meta_mime_type = 'text/csv';
		media_mime_type = 'text/csv';
	elif extension == 'xlsx':
		meta_mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
		media_mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
	elif extension == 'zip':
		meta_mime_type = 'application/zip';
		media_mime_type = 'application/zip';

	try:
		print('uploading:', local_file)
		file_metadata = {
			'name': filename,
			'mimeType': meta_mime_type,
			'parents': [],
		}
		media = MediaFileUpload(local_file,
								mimetype=meta_mime_type,
								resumable=True)

		if has_file == True:
			file_metadata['parents'] = file_info['parents'];
			file_id = file_info['id'];	
			file = service.files().update(fileId=file_id, media_body=media, fields='id, name, parents, mimeType', supportsAllDrives=True).execute()
			# print('update', file)

		else:
			if folder_id is None:
				folder_id = ensureDirectory(directory='/'.join(filepath.split('/')[:-1]), service=service, cache=cache, drive_key=drive_key);

			file_metadata['parents'] = [folder_id];
			file = service.files().create(body=file_metadata, media_body=media, fields='id, name, parents, mimeType', supportsAllDrives=True).execute()
			insertPermission(file['id'], service=service, sharing_permission=GDRIVE_SHARING);
	except Exception as e:
		Logger.e('GDrive.uploadFile', e);

def uploadFileSimple(filepath, local_file, file_metadata, service=None, cache=False, drive_key=DEFAULT_DRIVE_KEY, folder_id=None, ):
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();
	# filepath = cleanFilepath(filepath);
	# extension = filepath.split('.')[-1];
	# filename = filepath.split('/')[-1];
	# # has_file, file_info = hasFile(filepath=filepath, service=service, cache=cache, drive_key=drive_key);
	# # has_file = False;
	# if extension == 'csv':
	# 	meta_mime_type = 'text/csv';
	# 	media_mime_type = 'text/csv';
	# elif extension == 'xlsx':
	# 	meta_mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
	# 	media_mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
	# elif extension == 'zip':
	# 	meta_mime_type = 'application/zip';
	# 	media_mime_type = 'application/zip';

	try:
		print('uploading:', local_file)
		# print('file_metadata', file_metadata)
		# file_metadata = {
		# 	'name': filename,
		# 	'mimeType': meta_mime_type,
		# 	'parents': [],
		# }
		media = MediaFileUpload(local_file,
								mimetype=file_metadata['mimeType'],
								resumable=True)

		# if has_file == True:
		# 	file_metadata['parents'] = file_info['parents'];
		# 	file_id = file_info['id'];	
		# 	file = service.files().update(fileId=file_id, media_body=media, fields='id, name, parents, mimeType', supportsAllDrives=True).execute()
		# 	# print('update', file)

		# else:
		# 	if folder_id is None:
		# 		folder_id = ensureDirectory(directory='/'.join(filepath.split('/')[:-1]), service=service, cache=cache, drive_key=drive_key);
		# 	else:
		# print('media', media)
		file_metadata['parents'] = [folder_id];
		# print('file_metadata', file_metadata)
		file = service.files().create(body=file_metadata, media_body=media, fields='id, name, parents, mimeType', supportsAllDrives=True).execute()
		# print('create', file)
		insertPermission(file['id'], service=service, sharing_permission=GDRIVE_SHARING);
	except Exception as e:
		Logger.e('GDrive.uploadFile', e, filepath);

# ...

def deleteFiles(file_id_list, service=None):
	"""Permanently delete a file, skipping the trash.

	Args:
		service: Drive API service instance.
		file_id: ID of the file to delete.
	"""
	if DRIVE_SERVICE is not None:
		service = DRIVE_SERVICE;
	elif service is None:
		service = init();

	for file_id in file_id_list:
		try:
			service.files().delete(fileId=file_id, supportsAllDrives=True).execute();
			print('removing:', file_id);
		except Exception as error:
			print('An error occurred: %s' % error)