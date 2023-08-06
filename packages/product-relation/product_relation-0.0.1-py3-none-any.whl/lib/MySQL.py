import mysql.connector;

from lib import fn;
from lib import DateTime;
from lib import File;
from lib import Logger;
from lib import GDrive;

MYSQL_HOST = fn.getNestedElement(fn.config,'MYSQL_HOST', None);
MYSQL_DB_NAME = fn.getNestedElement(fn.config,'MYSQL_DB_NAME', None);
MYSQL_USER_NAME = fn.getNestedElement(fn.config,'MYSQL_USER_NAME', None);
MYSQL_PASSWORD = fn.getNestedElement(fn.config,'MYSQL_PASSWORD', None);

def connect(database=None):
	if database is None:
		database = MYSQL_DB_NAME;
	try:
		connection = mysql.connector.connect(host=MYSQL_HOST,
											 database=database,
											 user=MYSQL_USER_NAME,
											 password=MYSQL_PASSWORD,
											 auth_plugin='mysql_native_password');

	except mysql.connector.Error as e:
		Logger.e("Error reading data from MySQL table", e);
		connection = None;
	return connection;

def close(connection, cursor):
	if connection.is_connected():
		connection.close()
		cursor.close()
		# Logger.v("MySQL connection is closed");

def retrieve(query, database=None, connection=None):
	result = [];
	if connection is None:
		connection = connect(database=database);

	if connection is not None:
		cursor = connection.cursor()
		cursor.execute(query)
		# get all records
		records = cursor.fetchall()
		columns = cursor.column_names;

		# print("Total number of rows in table: ", cursor.rowcount)

		# print("\nPrinting each row")
		for row in records:
			# print('row', dict(zip(columns, row)));
			result.append(dict(zip(columns, row)));

		close(connection, cursor);
	return result;

def insert(query_list, database=None, connection=None):
	result = [];
	if connection is None:
		connection = connect(database=database);

	if connection is not None:
		cursor = connection.cursor()
		for query in query_list:
			cursor.execute(query);

		connection.commit();
		# print("Total number of rows in table: ", cursor.rowcount)

		close(connection, cursor);

def update(query_list, database=None, connection=None):
	result = [];
	if connection is None:
		connection = connect(database=database);

	if connection is not None:
		cursor = connection.cursor()
		for query in query_list:
			cursor.execute(query);

		connection.commit();
		# print("Total number of rows in table: ", cursor.rowcount)

		close(connection, cursor);