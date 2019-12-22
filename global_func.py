import sys
sys.path.insert(0,'../')
sys.path.insert(0,'../IML_Tokenizer/src/')
sys.path.insert(0,'../SJ_AI/src')
sys.path.insert(0,'./database/')
import atexit
import time
import numpy as np
from pymongo import *
from apscheduler.schedulers.background import BackgroundScheduler
from collections import Counter
from operator import itemgetter
from tzlocal import get_localzone
from datetime import timedelta, datetime
import json
import re
import csv
import jpype
#######################################################
from db_management import *
from db_info import *
from tknizer import get_tk
import LDA
import FastText
#######################################################
from variable import *


# BackgroundScheduler Initialize
def schedule_init():
	t_zone = get_localzone()
	scheduler = BackgroundScheduler()
	scheduler.start()

	#특정 시간마다 실행
	scheduler.add_job(measurement_run, 'cron', hour = 1, timezone = t_zone)

	#매 달마다 실행
	scheduler.add_job(create_word_cloud, trigger = "interval", days=30, timezone = t_zone)

	#매 시간마다 실행
	scheduler.add_job(real_time_insert, trigger = "interval", minutes = 5, timezone = t_zone)
	scheduler.add_job(update_posts_highest, trigger = "interval", hours = 1, timezone = t_zone)

	# weeks, days, hours, minutes, seconds
	# start_date='2010-10-10 09:30', end_date='2014-06-15 11:00'
	
	atexit.register(lambda: scheduler.shutdown())
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
#######################################################
#Background Func#######################################
#실시간 검색어 함수 preprocess
def preprocess(doc):
	emoji_pattern = re.compile("["
		u"\U0001F600-\U0001F64F"  # emoticons
		u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		u"\U0001F680-\U0001F6FF"  # transport & map symbols
		u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		"]+", flags=re.UNICODE)
	doc = re.sub(r'\s+'," ", doc)
	doc = doc.lower()
	doc = re.sub(r'[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', doc)
	doc = emoji_pattern.sub(r'', doc)
	doc = re.compile('[^ ㄱ-ㅣ가-힣|a-z]+').sub('', doc)
	return doc
#실시간 검색어 추출 함수
def real_time_keywords(search_input):
	temp = [i['search_split'] for i in search_input]
	check_list = []
	for i in range(len(temp)):
		temp_word = []
		for j in range(len(temp[i])):
			temp[i][j] = preprocess(temp[i][j])
			if len(temp[i][j]) > 1: temp_word.append(temp[i][j])
		check_list.append(temp_word)
	
	result = {}
	for words in check_list:
		# 단일 단어 추가
		for i in range(len(words)):
			if words[i] in result: result[words[i]] += 1
			else: result[words[i]] = 1
		
		# 연속 단어 추가(정방향)
		for i in range(2,len(words)):
			key = " ".join(words[0:i+1])
			if key in result: result[key] += 1
			else: result[key] = 1

	result = sorted(result.items(), key = itemgetter(0))
	temp = []
	for i in range(len(result)-1):
		if ((result[i+1][0].startswith(result[i][0]) or result[i+1][0].endswith(result[i][0])) and result[i+1][1] >= result[i][1]): 
			continue
		temp.append(result[i])
	result = sorted(temp, key = lambda x: len(x[0]))   
	result = sorted(result, key = itemgetter(1), reverse = True)
	return result

#실시간 검색어 캐싱 함수
def real_time_insert():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	search_log_list = find_search_log(db)
	search_log_list = list(search_log_list)

	real_tiem_result = real_time_keywords(search_log_list)

	insert_search_realtime(db, real_tiem_result)
	
	if db_client is not None:
		db_client.close()

#사용자 관심도 측정
def measurement_run():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	#모든 유저의 관심도 측정 지표를 다 가져온다.
	USER_list = find_all_user(db, _id=1, fav_list=1, view_list=1, search_list=1, newsfeed_list=1)

	for USER in USER_list:
		fav_tag = []
		view_tag = []
		newsfeed_tag = []
		fav_token = []
		view_token = []
		search_list = []

		#사용자가 관심 기능을 수행한 게시물 ##########################
		fav_topic = (np.zeros(LDA.NUM_TOPICS))
		for fav in USER['fav_list']:
			fav_topic += fav['topic']
			fav_tag += fav['tag']
			fav_token += fav['token']

		#FAS 전용
		fav_doc = (fav_tag + fav_token) * 2

		fav_tag *= 4
		fav_topic *= 8
		if len(USER['fav_list']) != 0:
			fav_topic /= len(USER['fav_list'])

		#사용자가 접근을 수행한 게시물 ##############################
		view_topic = (np.zeros(LDA.NUM_TOPICS))
		for view in USER['view_list']:
			view_topic += view['topic']
			view_tag += view['tag']
			view_token += view['token']

		#FAS 전용
		view_doc = view_tag + view_token

		view_tag *= 3
		view_topic *= 6
		if len(USER['view_list']) != 0:
			view_topic /= len(USER['view_list'])

		#사용자가 검색을 수행한 키워드 ##############################
		for search_obj in USER['search_list']:
			search_list += search_obj['tokenizer_split']
		
		search_topic = LDA.get_topics(search_list)
		search_topic *= 5

		#FAS 전용
		similarwords = []

		for search_keyword in search_list:
			for keyword in FastText.sim_words(search_keyword):
				if keyword[1] >= SJ_FASTTEXT_SIM_PERCENT: 
					similarwords.append(keyword[0])
				else: break

		search_doc = search_list + similarwords

		#사용자가 접근한 뉴스피드 ################################
		for newsfeed in USER['newsfeed_list']:
			newsfeed_tag += newsfeed['tag']

		newsfeed_topic = LDA.get_topics(newsfeed_tag)
		#newsfeed_topic *= 1

		####################################################

		#LDA Topic
		TOPIC_RESULT = (fav_topic + view_topic + search_topic + newsfeed_topic)/20

		#FASTTEXT
		FastText_doc = fav_doc + view_doc + search_doc

		if FastText_doc:
			USER_VERCTOR = FastText.get_doc_vector(fav_doc + view_doc + search_doc).tolist()
		else:
			USER_VERCTOR = ft_vector = (np.zeros(FastText.VEC_SIZE)).tolist()
			
		#TAG
		tag_dict = dict(Counter(fav_tag + view_tag))
		tag_dict = sorted(tag_dict.items(), key=lambda x: x[1], reverse = True)
		
		#빈도수 랭킹 상위 X위 까지 보관.
		TAG_RESULT = {}

		if len(tag_dict) >= 10:
			for i in range(10):
				TAG_RESULT[tag_dict[i][0]] = tag_dict[i][1]
		else:
			for i in range(len(tag_dict)):
				TAG_RESULT[tag_dict[i][0]] = tag_dict[i][1]
					
		USER_TAG_SUM = sum(TAG_RESULT.values())

		#1.5배 증가
		USER_TAG_SUM *= 3
		USER_TAG_SUM //= 2

		#만약 TAG_SUM 이 0이면 1로 설정.
		if USER_TAG_SUM == 0:
			USER_TAG_SUM = 1

		#해당 USER 관심도 갱신!
		update_user_measurement(db, USER['_id'], list(TOPIC_RESULT), TAG_RESULT, USER_TAG_SUM, USER_VERCTOR)

	if db_client is not None:
		db_client.close()

#유저 로그 푸시백
def user_log_pushback():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	# 'fav_list': {'$slice': mongo_num}, 
	# 	'view_list': {'$slice': mongo_num}, 
	# 	'search_list': {'$slice': mongo_num},
	# 	'newsfeed_list': {'$slice': mongo_num}

	#모든 유저의 관심도 측정 지표를 다 가져온다.
	USER_list = find_all_user(db, user_id=1, fav_list=1, view_list=1, search_list=1, newsfeed_list=1)
	USER_list = list(USER_list)

	for USER in USER_list:
		#fav
		if len(USER['fav_list']) > SJ_USER_LOG_LIMIT:
			refresh_obj = []
			back_obj_list = []
			cnt = 0
			for fav in USER['fav_list']:
				if cnt < SJ_USER_LOG_LIMIT:
					refresh_obj.append(fav)
				else:
					back_obj_list.append(fav)
				cnt += 1
			#400개로 맞춤 갱신!
			refresh_user_fav_list(db, USER['user_id'], refresh_obj)
			#pushback 으로 이전!
			insert_pushback(db, USER['user_id'], 'fav', back_obj_list)

		#view
		if len(USER['view_list']) > SJ_USER_LOG_LIMIT:
			refresh_obj = []
			back_obj_list = []
			cnt = 0
			for view in USER['view_list']:
				if cnt < SJ_USER_LOG_LIMIT:
					refresh_obj.append(view)
				else:
					back_obj_list.append(view)
				cnt += 1
			#400개로 맞춤 갱신!
			refresh_user_view_list(db, USER['user_id'], refresh_obj)
			#pushback 으로 이전!
			insert_pushback(db, USER['user_id'], 'view', back_obj_list)

		#search
		if len(USER['search_list']) > SJ_USER_LOG_LIMIT:
			refresh_obj = []
			back_obj_list = []
			cnt = 0
			for search in USER['search_list']:
				if cnt < SJ_USER_LOG_LIMIT:
					refresh_obj.append(search)
				else:
					back_obj_list.append(search)
				cnt += 1
			#400개로 맞춤 갱신!
			refresh_user_search_list(db, USER['user_id'], refresh_obj)
			#pushback 으로 이전!
			insert_pushback(db, USER['user_id'], 'search', back_obj_list)

		#newsfeed
		if len(USER['newsfeed_list']) > SJ_USER_LOG_LIMIT:
			refresh_obj = []
			back_obj_list = []
			cnt = 0
			for newsfeed in USER['newsfeed_list']:
				if cnt < SJ_USER_LOG_LIMIT:
					refresh_obj.append(newsfeed)
				else:
					back_obj_list.append(newsfeed)
				cnt += 1
			#400개로 맞춤 갱신!
			refresh_user_newsfeed_list(db, USER['user_id'], refresh_obj)
			#pushback 으로 이전!
			insert_pushback(db, USER['user_id'], 'newsfeed', back_obj_list)

#variable 가장 높은 좋아요/조회수 갱신
def update_posts_highest():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	#새로운 fav / view 카운트
	new_fav = find_highest_fav_cnt(db)
	new_view = find_highest_view_cnt(db)

	update_variable(db, 'highest_fav_cnt', new_fav)
	update_variable(db, 'highest_view_cnt', new_fav)

	if db_client is not None:
		db_client.close()

#워드클라우드 생성
def create_word_cloud():
	print("word_cloud")
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	db_realtime = find_search_all_realtime(db)
	db_realtime = list(db_realtime)
	
	db_posts = find_all_posts(db, title_token=1, token=1, tag=1)
	db_posts = list(db_posts)

	result = []

	#실시간 검색어 전부 가져와서 검색어만 추출
	for realtime in db_realtime:
		for word in realtime['real_time']:
			result.append(word[0])

	#DB의 전체 POST들의 title_token 과 token만 전체 추출
	for post in db_posts:
		result += post['title_token']
		result += post['token']
		result += post['tag']

	result = dict(Counter(result))
	result = sorted(result.items(), key=lambda x: x[1], reverse = True)

	file = open("./static/files/example.csv", 'w')
	file.write("text,frequency\n")

	necessary_str = ['SOOJLE', 'IML', '세종대']

	#최 상단 필수 워드클라우드 작성!
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

