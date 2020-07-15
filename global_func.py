import sys
sys.path.insert(0,'../')
sys.path.insert(0,'../IML_Tokenizer/src/')
sys.path.insert(0,'../SJ_AI/src')
sys.path.insert(0,'./database/')
import atexit
import time
import numpy as np
from pymongo import *
from collections import Counter
from operator import itemgetter
from tzlocal import get_localzone
from datetime import timedelta, datetime
import json
import re
import csv
import jpype
import schedule
#######################################################
from db_management import *
from db_info import *
from tknizer import get_tk
import LDA
import FastText
#######################################################
from variable import *

#######################################################
#전역 함수###############################################

#함수 시간 측정
def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn

#날짜 마이너스 연산
def get_default_day(day):
	date = datetime.now() - timedelta(days = day)
	return date

#날짜 플러스 연산
def get_plus_day(day):
	date = datetime.now() + timedelta(days = day)
	return date

#######################################################
#Background Func#######################################
'''
#워드클라우드 생성
def create_word_cloud():
	print(datetime.now(), "[백그라운드] 워드클라우드 생성중 ...")
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	db_realtime = find_search_all_realtime(db)
	db_realtime = list(db_realtime)
	
	db_posts = find_all_posts(db, title_token=1, token=1, tag=1)
	db_posts = list(db_posts)

	result = []

	for realtime in db_realtime:
		for word in realtime['real_time']:
			result.append(word[0])

	for post in db_posts:
		result += post['title_token']
		result += post['token']
		result += post['tag']

	result = dict(Counter(result))
	result = sorted(result.items(), key=lambda x: x[1], reverse = True)

	file = open("./static/files/example.csv", 'w')
	file.write("text,frequency\n")

	necessary_str = ['SOOJLE', 'IML', '세종대']

	for necessary in necessary_str:
		data = "0%s,%d\n" %(necessary, 500)
		file.write(data)
	
	frequency = 100
	num = 500
	cnt = 0

	for object_ in result[:num]:
		if cnt % (num/20) == 0:
			frequency -= 5

		data = "_%s,%d\n" %(object_[0], frequency)
		file.write(data)
		
		cnt += 1

	file.close()

	if db_client is not None:
		db_client.close()
	
	print(datetime.now(), "[백그라운드] 워드클라우드 생성 끝 ...")
'''

