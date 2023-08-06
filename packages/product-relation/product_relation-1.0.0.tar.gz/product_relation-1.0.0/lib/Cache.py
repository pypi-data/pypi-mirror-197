from . import SharedMemoryManager;
from . import fn;
from . import Logger;

global_version = fn.getNestedElement(fn.config, 'CACHE_VERSION', '1.0');
cache_enabled = int(fn.getNestedElement(fn.config, 'CACHE_ENABLED', '0')) == 1;
collection_prefix = 'cache_{0}';
def updateQuery(original_query):
	global global_version;
	query = original_query.copy();
	query.update({
		'version': global_version
	});
	return query;

def getCollectionName(collection_name):
	global collection_prefix;
	return collection_prefix.format(collection_name);

def get(collection_name, original_query):
	global cache_enabled;
	if cache_enabled:
		dbManager = SharedMemoryManager.getInstance();
		db = dbManager.query();

		query = updateQuery(original_query);
		cache_collection_name = getCollectionName(collection_name); 
		row = db[cache_collection_name].find_one(query);
		return fn.getNestedElement(row, 'result');
	return None;

def set(collection_name, original_query, data):
	dbManager = SharedMemoryManager.getInstance();
	cache_collection_name = getCollectionName(collection_name); 
	query = updateQuery(original_query);
	dbManager.addBulkUpdate(cache_collection_name, query, {
			'result': data
	}, upsert=True, batch=False);
	return data;

