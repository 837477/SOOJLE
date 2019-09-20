from pymongo import *
from flask import g

###################################
DB_HOST = 'localhost:27017'
DB_ID = 'root'
DB_PW = 'imlisgod'
###################################

def get_db():
    if 'db_client' not in g:
        db_client = MongoClient('mongodb://%s:%s@%s' %(DB_ID, DB_PW, DB_HOST))
        g.db_client = db_client

    if 'db' not in g:
        g.db = g.db_client["soojle"]
        

def close_db():
    db_client = g.pop('db_client', None)
    if db_client is not None:
        db_client.close()