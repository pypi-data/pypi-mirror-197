from . import basic;
from . import Logger;
from .basic import config;

from pymongo import MongoClient;
import pymongo;
import sys;
import os;
import socket
from . import fn;

class Database():
  def __init__(self):
    self.client = None;
    self.username = fn.getNestedElement(config,'MONGO_DB_USERNAME','');
    self.password = fn.getNestedElement(config,'MONGO_DB_PASSWORD','');
    
    ### local
    # self.host = fn.getNestedElement(config,'MONGO_DB_HOST','');
    # self.port = int(fn.getNestedElement(config,'MONGO_DB_PORT',''));

    self.host = '18.138.58.183'
    self.port = 1104;
  
  def check(self):
    success = False;
    try:
      db = self.client[config['MONGO_DB_NAME']];
      # if(self.username and self.password):
        # db.authenticate(self.username, self.password);
      db_names = self.client.database_names();
      success = len(db_names)>0;
    except pymongo.errors.AutoReconnect as e:
      Logger.v(e);
      print(e);
    except pymongo.errors.ConnectionFailure as e:
      Logger.v(e);
      print(e);
    except Exception as e:
      Logger.v(e);
      print(e);
    return success;

  def connect(self, index=False, connected=False):
    try:
      if not self.client:
        # if self.username and self.password:
        #   db_url = ('mongodb://%s:%s@%s:%d' % (self.username, self.password, self.host, self.port));
        # else:
        #   Logger.v('connect without username and password');
        db_url = ('mongodb://%s:%d' % (self.host, self.port));
        #db_url = ('mongodb://%s:%s@%s:%d' % (self.username, self.password, self.host, self.port));
        #print(db_url);

        Logger.v('Connecting to MongoClient, Connected:%s ...'%connected);
        self.client = MongoClient(db_url, serverSelectionTimeoutMS=1000, connect=connected, minPoolSize=1);
        #Logger.v('MongoClient Created...');
        if not self.check():
        #db_names = self.client.database_names();
        #Logger.v('MongoClient Database names:', db_names);
        #if len(db_names) <= 0:
          raise Exception("Empty Database");

        Logger.v('DB Connection Success');
    except pymongo.errors.AutoReconnect as e:
      Logger.v(e);
      self.restart(e);
    except pymongo.errors.ConnectionFailure as e:
      Logger.v(e);
      self.restart(e); 
    except Exception as e:
      Logger.v(e);
      self.restart(e); 

  def disconnect(self):
    self.client.close();
    Logger.v('Closed MongoClient');
    self.client = None;
    return self.client;

  def get(self, index=False, connected=False):
    if not self.client:
      self.connect(index=index, connected=connected);
    db = self.client[config['MONGO_DB_NAME']];
    # if(self.username and self.password):
      # db.authenticate(self.username, self.password);
    if(index):
        self.createIndex(db);
    return db;

  def createIndex(self, db):
    #db, self.client = connect();
    try:
      Logger.v('db.create_index.');
      db['account_page'].create_index([('upid', pymongo.DESCENDING),('uid', pymongo.DESCENDING),('canceled', pymongo.DESCENDING)]);
      db['account_page'].create_index([('upid', pymongo.DESCENDING),('page_type', pymongo.DESCENDING),('is_admin', pymongo.DESCENDING)]);
      db['page_fans'].create_index([('end_timestamp', pymongo.DESCENDING)]);
      db['page_fans'].create_index([('end_timestamp', pymongo.DESCENDING), ('name', pymongo.DESCENDING), ('upid', pymongo.ASCENDING)]);
      db['page_post'].create_index([('pid', pymongo.DESCENDING)]);
      db['page_post'].create_index([('upid', pymongo.DESCENDING)]);
      db['page_post_summary'].create_index([('pid', pymongo.DESCENDING), ('inserted_at', pymongo.DESCENDING)]);
      db['page_post_summary'].create_index([('upid', pymongo.DESCENDING)]);
      db['page_post_comments'].create_index([('pid', pymongo.DESCENDING),('uid', pymongo.DESCENDING)]);
      db['page_post_reactions'].create_index([('pid', pymongo.DESCENDING),('uid', pymongo.DESCENDING)]);
      db['page_post_comments'].create_index([('uid', pymongo.DESCENDING)]);
      db['page_post_reactions'].create_index([('uid', pymongo.DESCENDING)]);
      db['page_post_comments'].create_index([('cid', pymongo.DESCENDING)]);
      db['page_post_comments'].create_index([('pid', pymongo.DESCENDING)]);
      db['page_post_comments'].create_index([('cid', pymongo.DESCENDING),('pid', pymongo.DESCENDING),('upid', pymongo.DESCENDING)]);
      db['page_post_reactions'].create_index([('pid', pymongo.DESCENDING)]);
      #for search
      db['page_post_comments'].create_index([('upid', pymongo.DESCENDING),('post_created_timestamp', pymongo.DESCENDING)]);
      db['page_post_reactions'].create_index([('upid', pymongo.DESCENDING),('post_created_timestamp', pymongo.DESCENDING)]);
      
      db['page_post_comments'].create_index([('uid', pymongo.DESCENDING),('upid', pymongo.DESCENDING),('post_created_timestamp', pymongo.DESCENDING)]);
      db['page_post_reactions'].create_index([('uid', pymongo.DESCENDING),('upid', pymongo.DESCENDING),('post_created_timestamp', pymongo.DESCENDING)]);

      db['social_media_user'].create_index([('uid', pymongo.DESCENDING)]);
      db['social_media_user'].create_index([('uid', pymongo.DESCENDING), ('data_type', pymongo.DESCENDING)]);
      db['page_advertisement_stat'].create_index([('upid', pymongo.DESCENDING)]);

      db['tag_post'].create_index([('key', pymongo.DESCENDING), ('pid', pymongo.DESCENDING)]);
      db['tag_post'].create_index([('key', pymongo.DESCENDING)]);
      db['tag_post'].create_index([('interactions', pymongo.DESCENDING)]);
      db['post_tag_summary'].create_index([('tag', pymongo.DESCENDING)]);
      db['page_summary'].create_index([('upid', pymongo.DESCENDING),('uid', pymongo.DESCENDING),('date', pymongo.DESCENDING)]);
      db['page_summary'].create_index([('upid', pymongo.DESCENDING),('uid', pymongo.DESCENDING),('key', pymongo.DESCENDING)]);
    except Exception as e:
      Logger.e('db.createIndex.fail:',e);
      return None;

  def _close(self):
    self.disconnect();

  def restart(self, err):
    #print("Mongo Service Error:",err);
    print("Mongo Service Restarted @ IP:%s"%basic.getCurrentIP()); 
    mongo_db_command = "sudo service mongod restart";
    os.system(mongo_db_command);
    
