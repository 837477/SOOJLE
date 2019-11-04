import sys
sys.path.insert(0,'../')
sys.path.insert(0,'../IML_Tokenizer/src/')
sys.path.insert(0,'../SJ_AI/src')
sys.path.insert(0,'database/')

import atexit
import time
from pymongo import *
import numpy as np
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from collections import Counter
from operator import itemgetter
from tzlocal import get_localzone
from datetime import timedelta, datetime
#######################################################
from db_management import *
from db_info import *
#######################################################
import jpype
from tknizer import get_tk
import LDA
import FastText
#######################################################

# BackgroundScheduler Initialize
def schedule_init():
	t_zone = get_localzone()
	scheduler = BackgroundScheduler()

	#특정 시간마다 실행
	#scheduler.add_job(measurement_run(100), 'cron', hour = 22, minute = 5, timezone = t_zone)

	#매 시간마다 실행
	# weeks, days, hours, minutes, seconds
	#scheduler.add_job(func = testtest, trigger = "interval", seconds = 10, timezone = t_zone)
	
	# start_date='2010-10-10 09:30', end_date='2014-06-15 11:00'
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())

#######################################################
#전역 함수###############################################
def get_nowtime():
	now = datetime.now()
	encode_time = now.strftime('%Y-%m-%d %H:%M:%S')

	return encode_time

def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn

#######################################################
#Background Func#######################################
#사용자 관심도 측정
def measurement_run(num):
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]
	
	USER_list = db['user'].find({}, {
		'fav_list': {'$slice': num}, 
		'view_list': {'$slice': num}, 
		'search_list': {'$slice': num}
		})

	for USER in USER_list:
		fav_view_tag = []

		#fav topic numpy array
		fav_topic = np.zeros(LDA.NUM_TOPICS)

		#view topic numpy array
		view_topic = np.zeros(LDA.NUM_TOPICS)

		for fav in USER['fav_list']:
			fav_topic += fav['topic']
			fav_view_tag += fav['tag'] * 4

		for view in USER['view_list']:
			view_topic += view['topic']
			fav_view_tag += view['tag'] * 3

		search_topic = LDA.get_topics(USER['search_list'])

		fav_topic /= num
		view_topic /= num

		#사용자가 관심 기능을 수행한 게시물
		fav_topic *= 4

		#사용자가 접근을 수행한 게시물
		view_topic *= 3

		#사용자가 검색을 수행한 키워드
		search_topic *= 3

		topic_result = (fav_topic + view_topic + search_topic)/10

		tag_dict = dict(Counter(fav_view_tag))
		tag_dict = sorted(tag_dict.items(), key=lambda x: x[1], reverse = True)

		tag_result = {}
		for i in range(15):
			tag_result[tag_dict[i][0]] = tag_dict[i][1]

		USER_TAG_SUM = sum(tag_result.values())

		db['user'].update({'_id': USER['_id']}, {'$set': {'topic': list(topic_result), 'tag': tag_result, 'tag_sum': USER_TAG_SUM}})

#조회수 랭킹1위 수 갱신
def update_posts_highest_view(db):
	return "success"

#좋아요 랭킹1위 수 갱신
def update_posts_highest_fav_cnt(db):
	return "success"
