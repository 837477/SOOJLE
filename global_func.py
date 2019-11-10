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
	scheduler.add_job(measurement_run(100), 'cron', hour = 16, minute = 26, timezone = t_zone)

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
	
	mongo_num = num * -1
	USER_list = db['user'].find({"user_id": "test"}, {
		'fav_list': {'$slice': mongo_num}, 
		'view_list': {'$slice': mongo_num}, 
		'search_list': {'$slice': mongo_num}
		})

	# USER_list = db['user'].find({}, {
	# 	'fav_list': {'$slice': num}, 
	# 	'view_list': {'$slice': num}, 
	# 	'search_list': {'$slice': num}
	# 	})

	for USER in USER_list:
		fav_tag = []
		view_tag = []
		fav_token = []
		view_token = []

		#사용자가 관심 기능을 수행한 게시물 ##########################
		fav_topic = np.zeros(LDA.NUM_TOPICS)
		for fav in USER['fav_list']:
			fav_topic += fav['topic']
			fav_tag += fav['tag']
			fav_token += fav['token']

		#FAS 전용
		fav_doc = (fav_tag + fav_token) * 2

		fav_tag *= 4
		fav_topic *= 4
		fav_topic /= num

		#사용자가 접근을 수행한 게시물 ##############################
		view_topic = np.zeros(LDA.NUM_TOPICS)
		for view in USER['view_list']:
			view_topic += view['topic']
			view_tag += view['tag']
			view_token += view['token']

		#FAS 전용
		view_doc = fav_tag + fav_token

		view_tag *= 3
		view_topic *= 3
		view_topic /= num

		#사용자가 검색을 수행한 키워드 ##############################
		search_keyword_list = USER['search_list'][num*2:]
		search_topic = LDA.get_topics(search_keyword_list)
		search_topic *= 3

		#FAS 전용
		similarwords = []

		for search_keyword in search_keyword_list:
			for keyword in FastText.sim_words(search_keyword):
				if keyword[1] >= 0.7: 
					similarwords.append(keyword[0])
				else: break

		search_doc = search_keyword_list + similarwords

		############################################################################

		#LDA Topic
		topic_result = (fav_topic + view_topic + search_topic)/10
		
		#FASTTEXT
		user_vector = FastText.get_doc_vector(fav_doc + view_doc + search_doc)

		#TAG
		tag_dict = dict(Counter(fav_tag + view_tag))
		tag_dict = sorted(tag_dict.items(), key=lambda x: x[1], reverse = True)
		#빈도수 랭킹 상위 X위 까지 보관.
		tag_result = {}

		if len(tag_dict) >= 10:
			for i in range(10):
				tag_result[tag_dict[i][0]] = tag_dict[i][1]
		else:
			for i in range(len(tag_dict)):
				tag_result[tag_dict[i][0]] = tag_dict[i][1]
					
		USER_TAG_SUM = sum(tag_result.values())
		#1.5배 증가
		USER_TAG_SUM *= 3
		USER_TAG_SUM //= 2

		############################################################################

		db['user'].update({'_id': USER['_id']}, {'$set': {
			'topic': list(topic_result), 
			'tag': tag_result, 
			'tag_sum': USER_TAG_SUM,
			'ft_vector': user_vector.tolist()
			}})

#조회수 랭킹1위 수 갱신
def update_posts_highest_view(db):
	return "success"

#좋아요 랭킹1위 수 갱신
def update_posts_highest_fav_cnt(db):
	return "success"
