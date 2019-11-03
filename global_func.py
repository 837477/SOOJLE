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
	#scheduler.add_job(testtest, 'cron', hour = 19, minute = 18, timezone = t_zone)

	#매 시간마다 실행
	# weeks, days, hours, minutes, seconds
	#scheduler.add_job(func = testtest, trigger = "interval", seconds = 10, timezone = t_zone)
	
	# start_date='2010-10-10 09:30', end_date='2014-06-15 11:00'
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())

#######################################################
#백그라운드 프로세스#######################################

#포스트의 최고 좋아요, 조회수 갱신
#def update_posts_highest():
	#db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	#db = db_client['soojle']

	#모든 포스트 중에서 가장 높은 view수 갱신
	#update_posts_highest_view(db)

	#모든 포스트 중에서 가장 높은 fav_cnt수 갱신
	#update_posts_highest_fav_cnt(db)

	#db_client.close()

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
	#사용자의 fav_list, view_list, search_list를 가져온다.
	USER = find_user(db,  _id=1, user_id="XXXXX", fav_list=1, view_list=1, search_list=1)

	#시간순 정렬(최신순)
	fav_list = sorted(USER['fav_list'], key=itemgetter('date'), reverse=True)
	view_list = sorted(USER['view_list'], key=itemgetter('date'), reverse=True)

	fav_view_tag = []

	#fav topic numpy array
	fav_topic = np.zeros(LDA.NUM_TOPICS)

	#view topic numpy array
	view_topic = np.zeros(LDA.NUM_TOPICS)

	for fav in fav_list[:num]:
		fav_topic += fav['topic']
		fav_view_tag += fav['tag'] * 4

	for view in view_list[:num]:
		view_topic += view['topic']
		fav_view_tag += view['tag'] * 3

	search_topic = LDA.get_topics(USER['search_list'])

	fav_topic /= num
	view_topic /= num

	#############사용자가 관심 기능을 수행한 게시물#############
	###LDA Format###
	fav_topic *= 0.4

	##################사용자가 접근한 게시물##################
	###LDA Format###
	view_topic *= 0.3

	###############사용자가 검색을 수행한 키워드###############
	search_topic *= 0.3

	topic_result = fav_topic + view_topic + search_topic

	tag_result = {}
	tag_dict = dict(Counter(fav_view_tag))

	cnt = 0
	for key in tag_dict:
		if cnt == 20:
			break
		tag_result[key] = tag_dict[key]
		cnt += 1

	db['user'].update({'_id': USER['_id']}, {'$set': {'topic': list(topic_result), 'tag': tag_result}})
