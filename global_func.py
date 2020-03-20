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
import schedule
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

	#매 달마다 실행 ###################################################
	#scheduler.add_job(create_word_cloud, trigger = "interval", days=SJ_CREATE_WORDCLOUD_TIME, timezone = t_zone)

	scheduler.add_job(update_posts_highest, trigger = "interval", days=SJ_UPDATE_HIGHEST_FAV_VIEW_TIME, timezone = t_zone)

	#매 시간마다 실행 ##################################################

	#실시간 검색어 캐싱
	scheduler.add_job(real_time_insert, trigger = "interval", minutes = SJ_REALTIME_TIME, timezone = t_zone)

	#사용자 관심도 측정
	scheduler.add_job(measurement_run, trigger = "interval", hours = SJ_MEASUREMENT_TIME, timezone = t_zone)

	#특정 시간에 실행 ##################################################

	#방문자 통계
	scheduler.add_job(visitor_analysis_work, trigger = 'cron', hour="23", minute="59", timezone = t_zone)

	#매 시간별 방문자 측정
	scheduler.add_job(time_visitor_analysis_work, trigger = 'cron', minute="59", timezone = t_zone)
	

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

#날짜 플러스 연산
def get_plus_day(day):
	date = datetime.now() + timedelta(days = day)
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

	#최근 하루 이전의 검색 기록들을 가져온다.
	search_log_list = find_search_log(db)
	search_log_list = list(search_log_list)

	#검색기록들을 통하여 실시간 검색어를 추출한다.
	real_time_keywords_temp = real_time_keywords(search_log_list)

	#욕 필터링을 거친다.
	realtime_result = []
	for keyword in real_time_keywords_temp:
		#욕 필터링 걸리면 넘어감!
		if keyword in SJ_BAD_LANGUAGE:
			continue
		
		#10자 이상 삭제
		elif len(keyword) > 10:
			continue

		#최종 실시간 검색어 결과 반환
		realtime_result.append(keyword)

	if len(realtime_result) < SJ_REALTIME_LIMIT:
		lately_realtime = find_search_realtime(db)
		lately_realtime = list(lately_realtime)
		lately_realtime = lately_realtime[0]['real_time']
		
		realtime_result.sort(key=lambda x:x[1], reverse=True)
		lately_realtime.sort(key=lambda x:x[1], reverse=True)

		#가장 작은 값 찾기
		min_value = realtime_result[len(realtime_result) - 1][1]
		min_value -= 0.1

		#중복 키 찾기
		duple_key_list = list(set(dict(realtime_result)) & set(dict(lately_realtime)))
		
		#실시간 검색어 최종 리스트에 저번 리스트 순위를 추가하는 작업
		for lately in lately_realtime:
			check = True

			for duple_key in duple_key_list:
				if lately[0] == duple_key:
					check = False
			
			if check:
				realtime_result.append([lately[0], min_value])

			if len(realtime_result) == SJ_REALTIME_LIMIT:
				break
			
	insert_search_realtime(db, realtime_result[:SJ_REALTIME_LIMIT])
	
	if db_client is not None:
		db_client.close()

#사용자 관심도 측정 (테스트 대상)
def measurement_run():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	renewal_time = find_variable(db, 'renewal')

	#리뉴얼 시간보다 이상인 사람만 측정! (관심도 측정이 될 지표의 변동이 생겼다는 뜻!)
	USER_list = find_user_renewal(db, renewal_time)
	USER_list = list(USER_list)

	#액션 수행 날짜 제한에 필요한 기준 날짜 추출
	ACTION_DAY_CHECK = get_default_day(SJ_USER_ACTION_DAY_CHECK)

	for USER in USER_list:
		#사용자 로그 액션 먼저 개수 백업처리.
		user_log_backup(db, USER)

		fav_tag = []
		view_tag = []
		newsfeed_tag = []
		fav_token = []
		view_token = []
		search_list = []

		#사용자가 관심 기능을 수행한 게시물 ##########################
		fav_topic = (np.zeros(LDA.NUM_TOPICS))
		if len(USER['fav_list']) <= SJ_USER_LOG_LIMIT['fav'] * SJ_USER_ACTION_NUM_CHECK_PERCENT: 
			for fav in USER['fav_list']:
				fav_topic += fav['topic']
				fav_tag += fav['tag']
				fav_token += fav['token']
		else:
			for fav in USER['fav_list']:
				if fav['date'] < ACTION_DAY_CHECK: continue
				fav_topic += fav['topic']
				fav_tag += fav['tag']
				fav_token += fav['token']

		#FAS 구하기
		fav_doc = (fav_tag + fav_token) * 2

		#사용자가 접근을 수행한 게시물 ##############################
		view_topic = (np.zeros(LDA.NUM_TOPICS))
		if len(USER['view_list']) <= SJ_USER_LOG_LIMIT['view'] * SJ_USER_ACTION_NUM_CHECK_PERCENT: 
			for view in USER['view_list']:
				view_topic += view['topic']
				view_tag += view['tag']
				view_token += view['token']
		else:
			for view in USER['view_list']:
				if view['date'] < ACTION_DAY_CHECK: continue
				view_topic += view['topic']
				view_tag += view['tag']
				view_token += view['token']

		#FAS 구하기
		view_doc = view_tag + view_token

		#사용자가 검색을 수행한 키워드 ##############################
		if len(USER['search_list']) <= SJ_USER_LOG_LIMIT['search'] * SJ_USER_ACTION_NUM_CHECK_PERCENT:
			for search in USER['search_list']:
				search_list += search['tokenizer_split']
		else:
			for search in USER['search_list']:
				if search['date'] < ACTION_DAY_CHECK: continue
				search_list += search['tokenizer_split']
		
		search_topic = LDA.get_topics(search_list)
		search_doc = search_list

		#사용자가 접근한 뉴스피드 ################################
		if len(USER['newsfeed_list']) <= SJ_USER_LOG_LIMIT['newsfeed'] * SJ_USER_ACTION_NUM_CHECK_PERCENT:
			for newsfeed in USER['newsfeed_list']:
				newsfeed_tag += newsfeed['tag']
		else:
			for newsfeed in USER['newsfeed_list']:
				if newsfeed['date'] < ACTION_DAY_CHECK: continue
				newsfeed_tag += newsfeed['tag']

		newsfeed_topic = LDA.get_topics(newsfeed_tag)


		#가중치 작업
		fav_tag *= SJ_FAV_TAG_WEIGHT
		view_tag *= SJ_VIEW_TAG_WEIGHT
		
		fav_topic *= SJ_FAV_TOPIC_WEIGHT
		view_topic *= SJ_VIEW_TOPIC_WEIGHT
		search_topic *= SJ_SEARCH_TOPIC_WEIGHT
		newsfeed_topic *= SJ_NEWSFEED_TOPIC_WEIGHT

		if len(USER['fav_list']) != 0:
			fav_topic /= len(USER['fav_list'])
		
		if len(USER['view_list']) != 0:
			view_topic /= len(USER['view_list'])

		#LDA Topic
		TOPIC_RESULT = (fav_topic + view_topic + search_topic + newsfeed_topic)/SJ_TOPIC_RESULT_DIV

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
		USER_TAG_SUM *= SJ_TAG_SUM_WEIGHT

		#만약 TAG_SUM 이 0이면 1로 설정.
		if USER_TAG_SUM == 0:
			USER_TAG_SUM = 1

		#해당 USER 관심도 갱신! (관심도 측정 횟수 +1)
		update_user_measurement(db, USER['_id'], list(TOPIC_RESULT), TAG_RESULT, USER_TAG_SUM, USER_VERCTOR, len(USER['fav_list']) + len(USER['view_list']) + len(USER['search_list']) + len(USER['newsfeed_list']))

	update_variable(db, 'renewal', datetime.now())

	if db_client is not None:
		db_client.close()

#사용자 로그 액션 백업
def user_log_backup(db, USER):
	#fav
	if len(USER['fav_list']) > SJ_USER_LOG_LIMIT['fav']:
		#SJ_USER_LOG_LIMIT개로 다시 갱신!
		update_user_action_log_refresh(db, USER['_id'], 'fav', USER['fav_list'][:SJ_USER_LOG_LIMIT['fav']])
		#SJ_BACKUP 으로 이전!
		insert_user_backup(db, USER['user_id'], 'fav', USER['fav_list'][SJ_USER_LOG_LIMIT['fav']:])

	#view
	if len(USER['view_list']) > SJ_USER_LOG_LIMIT['view']:
		#SJ_USER_LOG_LIMIT개로 다시 갱신!
		update_user_action_log_refresh(db, USER['_id'], 'view', USER['view_list'][:SJ_USER_LOG_LIMIT['view']])
		#SJ_BACKUP 으로 이전!
		insert_user_backup(db, USER['user_id'], 'view', USER['view_list'][SJ_USER_LOG_LIMIT['view']:])

	#search
	if len(USER['search_list']) > SJ_USER_LOG_LIMIT['search']:
		#SJ_USER_LOG_LIMIT개로 다시 갱신!
		update_user_action_log_refresh(db, USER['_id'], 'search', USER['search_list'][:SJ_USER_LOG_LIMIT['search']])
		#SJ_BACKUP 으로 이전!
		insert_user_backup(db, USER['user_id'], 'search', USER['search_list'][SJ_USER_LOG_LIMIT['search']:])

	#newsfeed
	if len(USER['newsfeed_list']) > SJ_USER_LOG_LIMIT['newsfeed']:
		#SJ_USER_LOG_LIMIT개로 다시 갱신!
		update_user_action_log_refresh(db, USER['_id'], 'newsfeed', USER['newsfeed_list'][:SJ_USER_LOG_LIMIT['newsfeed']])
		#SJ_BACKUP 으로 이전!
		insert_user_backup(db, USER['user_id'], 'newsfeed', USER['newsfeed_list'][SJ_USER_LOG_LIMIT['newsfeed']:])

#variable 가장 높은 좋아요/조회수 갱신
def update_posts_highest():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	#새로운 fav / view 카운트
	new_fav = find_highest_fav_cnt(db)
	new_view = find_highest_view_cnt(db)

	update_variable(db, 'highest_fav_cnt', new_fav)
	update_variable(db, 'highest_view_cnt', new_view)

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

#하루 통계 작업 (하루마다!) (테스트 대상)
def visitor_analysis_work():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]




	#오늘 통계 객체화
	################################################################
	today_analysis = {}
	#오늘 방문자 수 가져오기
	today_analysis['today_visitor'] = find_today_visitor_count(db)
	#오늘 시간대별 방문자 수
	today_analysis['today_time_visitor'] = find_variable(db, 'today_time_visitor')
	#오늘 조회된 게시글
	today_analysis['today_view'] = find_variable(db, 'today_view')
	#오늘 좋아요된 게시글
	today_analysis['today_fav'] = find_variable(db, 'today_fav')

	today_year = datetime.today().year
	today_month = datetime.today().month
	today_day = datetime.today().day

	#오늘 날짜 기입!
	today_analysis['date'] = datetime(today_year, today_month, today_day)
	
	#매일 기록되는 통계 테이블에 기록!
	insert_everyday_analysis(db, today_analysis)
	################################################################






	#매일마다 갱신 시켜야하는 정적 변수들!
	################################################################
	#서비스 기간 하루 증가!
	update_variable_inc(db, 'service_period', 1)

	#총 방문자수 증가! (오늘 방문자 수를 더해준다.)
	update_variable_inc(db, 'total_visitor', today_analysis['today_visitor'])

	#최고 방문자 수 갱신!
	highest_visitor = find_variable(db, 'highest_visitor')
	if highest_visitor < today_analysis['today_visitor']:
		update_variable(db, 'highest_visitor', today_analysis['today_visitor'])

	#하루 평균 방문자 수 갱신!
	total_visitor = find_variable(db, 'total_visitor')
	service_period = find_variable(db, 'service_period')
	day_avg = total_visitor // service_period
	update_variable(db, 'day_avg_visitor', day_avg)

	#총 조회한 게시글 수 갱신!
	update_variable_inc(db, 'total_view', today_analysis['today_view'])

	#총 좋아요한 게시글 수 갱신!
	update_variable_inc(db, 'total_fav', today_analysis['today_fav'])

	#총 검색 횟수 갱신!
	total_search_cnt = find_search_count(db)
	update_variable(db, 'total_search_cnt', total_search_cnt)

	#총 게시글 수 갱신!
	total_posts_cnt = find_posts_count(db)
	update_variable(db, 'total_posts_cnt', total_posts_cnt)

	#총 소통 횟수 갱신!
	API_log_cnt = find_log_count(db)
	communication_avg = API_log_cnt // service_period
	update_variable(db, 'communication_avg', communication_avg)
	################################################################





	#매일마다 초기화 해줘야하는 정적 변수들!
	################################################################
	#오늘 조회한 게시글 0으로 초기화
	update_variable(db, 'today_view', 0)

	#오늘 좋아요한 게시글 0으로 초기화
	update_variable(db, 'today_fav', 0)

	#today_visitor 콜렉션 비우기!
	remove_today_visitor(db)

	#today_time_visitor 빈 리스트로 초기화
	today_time_visitor_empty = []
	update_variable(db, 'today_time_visitor', today_time_visitor_empty)
	################################################################
	if db_client is not None:
		db_client.close()

#매 시간별 방문자 수 기록! 
def time_visitor_analysis_work():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	#한시간 전 시간 가져오기
	time = datetime.now() - timedelta(minutes = 59)

	#(현재시간-1시간) ~ 현재시간 의 방문자 수 가져오기
	visitor_cnt = find_today_time_visitor(db, time)

	#시간별 방문자 오브젝트 생성!
	hour_visitor_obj = {}
	if datetime.now().hour == 0:
		hour_visitor_obj['time'] = 24
	else:	
		hour_visitor_obj['time'] = datetime.now().hour
	
	hour_visitor_obj['visitor'] = visitor_cnt

	#시간별 방문자 수 기록!
	push_today_time_visitor(db, hour_visitor_obj)

	if db_client is not None:
		db_client.close()

