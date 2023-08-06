from lib import Logger;
from lib import fn;
from lib import DateTime;
from io import StringIO;
from sylk_parser import SylkParser;
import xlrd;
import pandas as pd;
import numpy as np;
import os;
import csv;
import sys;
import time;
import shutil;
import re;
import datetime;
import zipfile;
import dask.dataframe as dd;

def readParquetToDF(file, columns=None):
	try:
		df = dd.read_parquet(file, columns=columns);
	except Exception as e:
		Logger.e('DaskFile.readParquetToDF', e);
		print('file:', file);
		df = pd.DataFrame();

	return df;

def writeToParquet(filename, data, use_dictionary=False, engine='pyarrow', compression='snappy'):
    while True:
        try:
            data.to_parquet(filename, use_dictionary=use_dictionary, engine=engine, compression=compression)
            break;
        except Exception as ex:
            Logger.v('Unable to write file. Please close file ({0}) to allow rewrite.'.format(filename));
            Logger.e(ex);
            time.sleep(5);
        except (KeyboardInterrupt, SystemExit):
            return False;