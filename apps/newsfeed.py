from flask import *
from flask_jwt_extended import *
from werkzeug import *
from bson.json_util import dumps
from datetime import datetime
from numpy import dot
from numpy.linalg import norm
import numpy
import operator
import time
#####################################
from db_management import *
from global_func import *
#####################################
from variable import *


#BluePrint
BP = Blueprint('newsfeed', __name__)


#현재 버전 2 테스트중
#토픽별 뉴스피드.ver1
@BP.route('/get_newsfeed_of_topic/<string:newsfeed_name>')
@jwt_optional
def get_newsfeed_of_topic(newsfeed_name):
	#총 시간 측정#################################################
	TOTAL_TIME_START = time.time()
	###########################################################

	#제대로 된 뉴스피드 네임이 들어오지 않을 경우
	if newsfeed_name not in SJ_NEWSFEED_OF_TOPIC_SET: abort(400)

	#요청한 뉴스피드에 대한 정보를 가져온다.
	newsfeed_type = find_newsfeed_of_topic(g.db, newsfeed_name)

	#info를 정규표현식으로 부르기위해 or연산자로 join
	info = "|".join(newsfeed_type['info'])

	#end_date처리 작업을 위한 현재시간 변수 선언
	now_date = datetime.now()

	#find_posts_of_category 시간 측정 (불러와서 리스트화 시킨 시간)#####
	FIND_POSTS_OF_CATEGORY_TIME_START = time.time()
	###########################################################
	#해당 토픽 뉴스피드에 관련된 게시글들을 불러온다.
	POST_LIST = find_newsfeed(g.db, info, newsfeed_type['tag'], newsfeed_type['negative_tag'], SJ_NEWSFEED_TOPIC_LIMIT)
	POST_LIST = list(POST_LIST)

	#end_date 처리!
	for POST in POST_LIST:
		#포스트에 end_date가 존재하고, 현재 날짜가 더 커버리면 (이미 지난 글)
		if ('end_date' in POST) and (now_date > POST['end_date']):
			#해당 포스트 삭제.
			POST_LIST.remove(POST)
	#find_posts_of_category 측정 종료 (불러와서 리스트화 시킨 시간)#####
	FIND_POSTS_OF_CATEGORY_TIME_END = time.time() - FIND_POSTS_OF_CATEGORY_TIME_START
	###########################################################
	
	#로그인시!
	if get_jwt_identity():
		#USER를 불러온다.
		USER = find_user(g.db, _id=1, user_id=get_jwt_identity(), topic=1, tag=1, tag_sum=1, ft_vector=1)
		
		#유효한 토큰인지 확인.
		if USER is None: abort(401)

		#logging! (메인 로그)
		insert_log(g.db, get_jwt_identity(), request.path)

		#접근한 뉴스피드 기록을 위한 obj 생성!
		newsfeed_obj = {}
		newsfeed_obj['newsfeed_name'] = newsfeed_type['newsfeed_name']
		newsfeed_obj['tag'] = newsfeed_type['tag']
		newsfeed_obj['date'] = datetime.now()

		#접근한 뉴스피드 기록!
		update_user_newsfeed_list_push(g.db, USER['_id'], newsfeed_obj)

		#해당 유저의 갱신시간 갱신
		update_user_renewal(g.db, USER['user_id'])
		
		#캐싱된 가장 높은 좋아요 수를 가져온다.
		Maxfav_cnt = find_variable(g.db, 'highest_fav_cnt')
		#캐싱된 가장 높은 조회수를 가져온다.
		Maxviews = find_variable(g.db, 'highest_view_cnt')

		#공모전&행사 뉴스피드는 사용자 관심도도 측정하여 따로 반환
		if newsfeed_name == '공모전&행사':
			#공모전&행사 뉴스피드 관심도 반영 시간 측정 (불러와서 리스트화 시킨 시간)###
			GET_SIMILARITY_TIME_START = time.time()
			###########################################################
			for POST in POST_LIST:
				#우선 판별!
				#당일로부터 30일 넘어가면 유사도 점수를 낮춘다.
				if get_default_day(30) > POST['date']:
					POST['similarity'] = 0
					continue

				#simijlarity 구하기!
				result = get_similarity(USER, POST, Maxfav_cnt, Maxviews)

				#최종 similarity 적용!
				POST['similarity'] = result

			#공모전&행사 뉴스피드 관심도 반영 측정 종료 (불러와서 리스트화 시킨 시간)###
			GET_SIMILARITY_TIME_END = time.time() - GET_SIMILARITY_TIME_START
			###########################################################
				
			#similarity를 기준으로 내림차순 정렬.
			POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	#비로그인!
	else:
		#logging! (메인 로그)
		insert_log(g.db, request.remote_addr, request.path)

	#총 시간 측정 종료#############################################
	TOTAL_TIME_END = time.time() - TOTAL_TIME_START
	###########################################################

	SPEED_RESULT = {}
	SPEED_RESULT['FIND_POSTS_OF_CATEGROY_TIME'] = FIND_POSTS_OF_CATEGORY_TIME_END
	if get_jwt_identity():
		if category_name == '공모전&행사':
			SPEED_RESULT['GET_SIMILARITY_TIME'] = GET_SIMILARITY_TIME_END
	SPEED_RESULT['TOTAL_TIME'] = TOTAL_TIME_END
	SPEED_RESULT['PROCESSING_POSTS_NUM'] = len(POST_LIST)
	SPEED_RESULT['RETURN_NUM'] = SJ_RETURN_NUM

	return jsonify(
			result = "success",
			newsfeed = dumps(POST_LIST[:SJ_RETURN_NUM]),
			speed_result = SPEED_RESULT
		)

'''
#토픽별 뉴스피드.ver2 (테스트 대상)
@BP.route('/get_newsfeed_of_topic/<string:category_name>')
@jwt_optional
def get_newsfeed_of_topic(category_name):
	#총 시간 측정#################################################
	TOTAL_TIME_START = time.time()
	###########################################################

	#제대로 된 카테고리 네임이 들어오지 않을 경우
	if category_name not in SJ_CATEGORY_OF_TOPIC_SET: abort(400)

	#요청한 카테고리에 대한 정보를 가져온다.
	category = find_category_of_topic(g.db, category_name)

	#end_date처리 작업을 위한 현재시간 변수 선언
	now_date = datetime.now()

	#find_posts_of_category 시간 측정 (불러와서 리스트화 시킨 시간)#####
	FIND_POSTS_OF_CATEGORY_TIME_START = time.time()
	###########################################################
	#해당 카테고리에 관련된 게시글들을 불러온다.
	POST_LIST = find_posts_of_category(g.db, category['info_num'], category['tag'], now_date, SJ_NEWSFEED_TOPIC_LIMIT)
	POST_LIST = list(POST_LIST)
	#find_posts_of_category 측정 종료 (불러와서 리스트화 시킨 시간)#####
	FIND_POSTS_OF_CATEGORY_TIME_END = time.time() - FIND_POSTS_OF_CATEGORY_TIME_START
	###########################################################

	#로그인시!
	if get_jwt_identity():
		#USER를 불러온다.
		USER = find_user(g.db, _id=1, user_id=get_jwt_identity(), topic=1, tag=1, tag_sum=1, ft_vector=1)
		
		#유효한 토큰인지 확인.
		if USER is None: abort(401)

		#logging! (메인 로그)
		insert_log(g.db, get_jwt_identity(), request.path)

		#접근한 뉴스피드 기록을 위한 obj 생성!
		newsfeed_obj = {}
		newsfeed_obj['newsfeed_name'] = category_name
		newsfeed_obj['tag'] = category['tag']
		newsfeed_obj['date'] = datetime.now()

		#접근한 뉴스피드 기록!
		update_user_newsfeed_list_push(g.db, USER['_id'], newsfeed_obj)

		#해당 유저의 갱신시간 갱신
		update_user_renewal(g.db, USER['user_id'])
		
		#캐싱된 가장 높은 좋아요 수를 가져온다.
		Maxfav_cnt = find_variable(g.db, 'highest_fav_cnt')
		#캐싱된 가장 높은 조회수를 가져온다.
		Maxviews = find_variable(g.db, 'highest_view_cnt')
		
		#공모전&행사 뉴스피드는 사용자 관심도도 측정하여 따로 반환
		if category_name == '공모전&행사':
			#공모전&행사 뉴스피드 관심도 반영 시간 측정 (불러와서 리스트화 시킨 시간)###
			GET_SIMILARITY_TIME_START = time.time()
			###########################################################
			for POST in POST_LIST:
				#우선 판별!
				#당일로부터 30일 넘어가면 유사도 점수를 낮춘다.
				if get_default_day(30) > POST['date']:
					POST['similarity'] = 0
					continue

				#simijlarity 구하기!
				result = get_similarity(USER, POST, Maxfav_cnt, Maxviews)

				#최종 similarity 적용!
				POST['similarity'] = result
			
			#공모전&행사 뉴스피드 관심도 반영 측정 종료 (불러와서 리스트화 시킨 시간)###
			GET_SIMILARITY_TIME_END = time.time() - GET_SIMILARITY_TIME_START
			###########################################################

			#similarity를 기준으로 내림차순 정렬.
			POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	#비로그인!
	else:
		#logging! (메인 로그)
		insert_log(g.db, request.remote_addr, request.path)

	#총 시간 측정 종료#############################################
	TOTAL_TIME_END = time.time() - TOTAL_TIME_START
	###########################################################

	SPEED_RESULT = {}
	SPEED_RESULT['FIND_POSTS_OF_CATEGROY_TIME'] = FIND_POSTS_OF_CATEGORY_TIME_END
	if get_jwt_identity():
		if category_name == '공모전&행사':
			SPEED_RESULT['GET_SIMILARITY_TIME'] = GET_SIMILARITY_TIME_END
	SPEED_RESULT['TOTAL_TIME'] = TOTAL_TIME_END
	SPEED_RESULT['PROCESSING_POSTS_NUM'] = len(POST_LIST)
	SPEED_RESULT['RETURN_NUM'] = SJ_RETURN_NUM

	return jsonify(
			result = "success",
			newsfeed = dumps(POST_LIST[:SJ_RETURN_NUM]),
			speed_result = SPEED_RESULT
		)
'''

#추천 뉴스피드 (테스트 대상)
@BP.route('/get_recommendation_newsfeed')
@jwt_optional
def get_recommendation_newsfeed():
	#총 시간 측정#################################################
	TOTAL_TIME_START = time.time()
	###########################################################

	#현재 날짜 가져오기.
	now_date = datetime.now()
	
	#반환 할 포스트 초기화
	POST_LIST = []
	#반활 할 스피드 측정 초기화
	SPEED_RESULT = {}

	#회원일 때!
	if get_jwt_identity():
		#유저 정보 불러오기.
		USER = find_user(g.db, user_id=get_jwt_identity(), topic=1, tag=1, ft_vector=1, tag_sum=1, measurement_num=1)

		#유효한 토큰인지 확인.
		if USER is None: abort(401)

		#logging (메인 로그)
		insert_log(g.db, USER['user_id'], request.path)
		#방문자 로그 기록!
		insert_today_visitor(g.db, USER['user_id'])

		#회원 관심도가 cold 상태일 때!
		if USER['measurement_num'] <= SJ_USER_COLD_LIMIT:
			#비로그인 전용 추천뉴스피드 호출!
			POST_LIST, SPEED_RESULT = get_recommendation_newsfeed_non_member(g.db, now_date)	

		#관심도가 cold가 아닐 때!
		else:
			#로그인 전용 추천뉴스피드 호출!
			POST_LIST, SPEED_RESULT = get_recommendation_newsfeed_member(g.db, USER, now_date)

	#비회원일 때!
	else:
		#logging (메인 로그)
		insert_log(g.db, request.remote_addr, request.path)
		#방문자 로그 기록!
		insert_today_visitor(g.db, request.remote_addr)		
		
		#비로그인 전용 추천뉴스피드 호출!
		POST_LIST, SPEED_RESULT = get_recommendation_newsfeed_non_member(g.db, now_date)

	#similarity를 기준으로 내림차순 정렬.
	POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	#총 시간 측정 종료#############################################
	TOTAL_TIME_END = time.time() - TOTAL_TIME_START
	###########################################################
	
	SPEED_RESULT['TOTAL_TIME'] = TOTAL_TIME_END
	SPEED_RESULT['RETURN_NUM'] = SJ_RETURN_NUM

	return jsonify(
			result = "success",
			newsfeed = dumps(POST_LIST[:SJ_RETURN_NUM]),
			speed_result = SPEED_RESULT
		)

#인기 뉴스피드
@BP.route('/get_popularity_newsfeed')
@jwt_optional
def get_popularity_newsfeed():
	#logging! (메인 로그)
	if get_jwt_identity():
		#유저 확인
		USER = find_user(g.db, user_id=get_jwt_identity())

		#유효한 토큰이 아닐 때 
		if USER is None: abort(401)

		#logging (메인 로그)
		insert_log(g.db, USER['user_id'], request.path)
		#방문자 로그 기록!
		insert_today_visitor(g.db, USER['user_id'])

	else:
		insert_log(g.db, request.remote_addr, request.path)

	result = find_popularity_newsfeed(g.db, SJ_RETURN_NUM)

	return jsonify(
		result = "success",
		newsfeed = dumps(result))


#함수들
###########################################################################
###########################################################################
#similarity 측정 함수
def get_similarity(USER, POST, Maxfav_cnt, Maxviews):
	#TOS 작업
	TOS = dot(USER['topic'], POST['topic']) / (norm(USER['topic']) * norm(POST['topic']))

	#TAS 작업
	USER_TAG = USER['tag'].keys()
	TAG = USER_TAG & set(POST['tag'])
	inter_sum = 0
	for i in TAG:
		inter_sum += USER['tag'][i]
	TAS = inter_sum / USER['tag_sum']
					
	#FAS 작업
	FAS = FastText.vec_sim(USER['ft_vector'], POST['ft_vector'])

	#IS 작업
	IS = (((POST['fav_cnt']/Maxfav_cnt)*SJ_IS_FAV_WEIGHT) + ((POST['view']/Maxviews)*SJ_IS_VIEW_WEIGHT))
					
	#RANDOM 작업
	RANDOM = numpy.random.random()

	#가중치 작업
	TOS *= SJ_TOS_WEIGHT
	TAS *= SJ_TAS_WEIGHT
	FAS *= SJ_FAS_WEIGHT
	IS *= SJ_IS_WEIGHT
	RANDOM *= SJ_RANDOM_WEIGHT

	#최종 값 저장
	result = TOS + TAS + FAS + RANDOM

	return result

#트랜드 스코어 판별 함수
def trendscore_discriminate(now_date):
	year = now_date.year

	'''
	#Course Manual (수강편람 기간)
	CM_term_1 = (datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14))
	CM_term_2 = (datetime(year, 8, 1) < now_date) and (now_date < datetime(year, 8, 14))

	#Seasonal Semester (계절학기 기간)
	SS_term_1 = (datetime(year, 11, 25) < now_date) and (now_date < datetime(year, 12, 5))
	SS_term_2 = (datetime(year, 5, 25) < now_date) and (now_date < datetime(year, 6, 5))
	
	#트랜드 스코어 판별 반환
	if CM_term_1 or CM_term_2 or SS_term_1 or SS_term_2:
		return True

	else:
		return False
	'''

	return  ((datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14))) or ((datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14))) or ((datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14)))

#트렌드 스코어 계산 함수
def trendscore(POST, now_date):

	#수강편람 trendscore
	if POST['info'] == 'main_student' and ('수강편람' in POST['tag']):
		return 10 

	#계절학기 trendscore
	elif POST['info'] == 'main_student' and ('계절학기' in POST['title_token']):
		return 4

	#아니면?!
	else: 
		return 0

'''
#현재 버전 2 테스트중
#회원 전용 추천 뉴스피드.ver1
def get_recommendation_newsfeed_member(db, USER, now_date):
	#추쳔 뉴스피드를 위한 포스트들을 불러오는 시간 측정 시작#################
	FIND_ALL_POSTS_TIME_START = time.time()
	###########################################################
	#게시글들을 불러온다.
	POST_LIST = find_all_posts(g.db, _id=1, topic=1, ft_vector=1, fav_cnt=1, view=1, tag=1, title=1, info=1, title_token=1, url=1, img=1, date=1, end_date=1, limit_=SJ_RECOMMENDATION_LIMIT)
	POST_LIST = list(POST_LIST)
	#추쳔 뉴스피드를 위한 포스트들을 불러오는 시간 측정 종료#################
	FIND_ALL_POSTS_TIME_END = time.time() - FIND_ALL_POSTS_TIME_START
	###########################################################

	#캐싱된 가장 높은 좋아요 수를 가져온다.
	Maxfav_cnt = find_variable(g.db, 'highest_fav_cnt')
	#캐싱된 가장 높은 조회수를 가져온다.
	Maxviews = find_variable(g.db, 'highest_view_cnt')



	#트랜드 스코어 반영하는 시간 측정 시작##############################
	TREND_TIME_START = time.time()
	###########################################################
	#트랜드 스코어 적용
	if trendscore_discriminate(now_date):
		for POST in POST_LIST:
			#end_date 처리!
			#포스트에 end_date가 존재하고, 현재 날짜가 더 커버리면 (이미 지난 글)
			if ('end_date' in POST) and (now_date > POST['end_date']):
				#해당 포스트 삭제. (첫 번째 방안)
				#POST_LIST.remove(POST)

				#해당 포스트 유사도를 0으로 측정 (두 번째 방안)
				POST['similarity'] = 0
				continue
					
			#트랜드 스코어 적용!
			TREND = trendscore(POST, now_date)
			
			#simijlarity 구하기!
			result = get_similarity(USER, POST, Maxfav_cnt, Maxviews)

			#최종 similarity 적용!
			POST['similarity'] = result + TREND
					
	#트랜드 스코어 미적용
	else:
		for POST in POST_LIST:
			#end_date 처리!
			#포스트에 end_date가 존재하고, 현재 날짜가 더 커버리면 (이미 지난 글)
			if ('end_date' in POST) and (now_date > POST['end_date']):
				#해당 포스트 삭제. (첫 번째 방안)
				#POST_LIST.remove(POST)

				#해당 포스트 유사도를 0으로 측정 (두 번째 방안)
				POST['similarity'] = 0
				continue
					
			#simijlarity 구하기!
			result = get_similarity(USER, POST, Maxfav_cnt, Maxviews)
					
			#최종 similarity 적용!
			POST['similarity'] = result
	#트랜드 스코어 반영하는 시간 측정 종료##############################
	TREND_TIME_END = time.time() - TREND_TIME_START
	###########################################################

	SPEED_RESULT = {}
	SPEED_RESULT['MEMBER_FIND_ALL_POSTS_TIME'] = FIND_ALL_POSTS_TIME_END
	SPEED_RESULT['MEMBER_TREND_TIME'] = TREND_TIME_END
	SPEED_RESULT['MEMBER_PROCESSING_POSTS_NUM'] = len(POST_LIST)

	return POST_LIST, SPEED_RESULT
'''

#회원 전용 추천 뉴스피드.ver2
def get_recommendation_newsfeed_member(db, USER, now_date):
	#추쳔 뉴스피드를 위한 포스트들을 불러오는 시간 측정 시작#################
	FIND_ALL_POSTS_TIME_START = time.time()
	###########################################################
	#게시글들을 불러온다.
	POST_LIST = find_posts_of_recommendation(g.db, now_date, num=SJ_RECOMMENDATION_LIMIT)
	POST_LIST = list(POST_LIST)
	#추쳔 뉴스피드를 위한 포스트들을 불러오는 시간 측정 종료#################
	FIND_ALL_POSTS_TIME_END = time.time() - FIND_ALL_POSTS_TIME_START
	###########################################################

	#캐싱된 가장 높은 좋아요 수를 가져온다.
	Maxfav_cnt = find_variable(g.db, 'highest_fav_cnt')
	#캐싱된 가장 높은 조회수를 가져온다.
	Maxviews = find_variable(g.db, 'highest_view_cnt')



	#트랜드 스코어 반영하는 시간 측정 시작##############################
	SIM_TREND_TIME_START = time.time()
	###########################################################
	#트랜드 스코어 적용
	if trendscore_discriminate(now_date):
		for POST in POST_LIST:				
			#트랜드 스코어 적용!
			TREND = trendscore(POST, now_date)
			
			#simijlarity 구하기!
			result = get_similarity(USER, POST, Maxfav_cnt, Maxviews)

			#최종 similarity 적용!
			POST['similarity'] = result + TREND
					
	#트랜드 스코어 미적용
	else:
		for POST in POST_LIST:
			#simijlarity 구하기!
			result = get_similarity(USER, POST, Maxfav_cnt, Maxviews)
					
			#최종 similarity 적용!
			POST['similarity'] = result
	#트랜드 스코어 반영하는 시간 측정 종료##############################
	SIM_TREND_TIME_END = time.time() - TREND_TIME_START
	###########################################################

	SPEED_RESULT = {}
	SPEED_RESULT['MEMBER_FIND_ALL_POSTS_TIME'] = FIND_ALL_POSTS_TIME_END
	SPEED_RESULT['MEMBER_SIM_TREND_TIME'] = TREND_TIME_END
	SPEED_RESULT['MEMBER_PROCESSING_POSTS_NUM'] = len(POST_LIST)

	return POST_LIST, SPEED_RESULT

'''
#현재 버전 2 테스트중
#비회원 전용 추천 뉴스피드.ver1
def get_recommendation_newsfeed_non_member(db, now_date):
	#요청한 뉴스피드에 대한 정보를 가져온다.
	newsfeed_type = find_all_newsfeed_of_topic(db)
	newsfeed_type = list(newsfeed_type)

	POST_LIST = []

	for newsfeed in newsfeed_type:
		if newsfeed['newsfeed_name'] != '장터':
			#info를 정규표현식으로 부르기위해 or연산자로 join
			info = "|".join(newsfeed['info'])

			result = find_newsfeed(g.db, info, newsfeed['tag'], newsfeed['negative_tag'], SJ_NO_TOKEN_RECOMMENDATION_LIMIT)

			POST_LIST += list(result)

	#트랜드 스코어 적용 판별##############################################
	#트랜드 스코어 적용일 시
	if trendscore_discriminate(now_date):
		for POST in POST_LIST:
			#end_date 처리!
			#포스트에 end_date가 존재하고, 현재 날짜가 더 커버리면 (이미 지난 글)
			if ('end_date' in POST) and (now_date > POST['end_date']):
				#해당 포스트 삭제. (첫 번째 방안)
				#POST_LIST.remove(POST)
				
				#해당 포스트 유사도를 0으로 측정 (두 번째 방안)
				POST['similarity'] = 0
				continue

			RANDOM = numpy.random.random()
			RANDOM *= SJ_RANDOM_WEIGHT
			TREND = trendscore(POST)

			result = RANDOM + TREND

			POST['similarity'] = result
	
	#트랜드 스코어 적용 안할 시
	else:
		for POST in POST_LIST:
			#end_date 처리!
			#포스트에 end_date가 존재하고, 현재 날짜가 더 커버리면 (이미 지난 글)
			if ('end_date' in POST) and (now_date > POST['end_date']):
				#해당 포스트 삭제. (첫 번째 방안)
				#POST_LIST.remove(POST)
				
				#해당 포스트 유사도를 0으로 측정 (두 번째 방안)
				POST['similarity'] = 0
				continue

			RANDOM = numpy.random.random()
			RANDOM *= SJ_RANDOM_WEIGHT

			POST['similarity'] = RANDOM
	#################################################################
		
	return POST_LIST
'''

#비회원 전용 추천 뉴스피드.ver2
def get_recommendation_newsfeed_non_member(db, now_date):
	#요청한 카테고리 대한 정보를 가져온다.
	category_list = find_category_of_topic_list(db, list(SJ_CATEGORY_OF_TOPIC_SET))
	category_list = list(category_list)
	
	#처리할 포스트 리스트 초기화
	POST_LIST = []
	
	#각각의 카테고리의 포스트들을 불러오는 시간 측정 시작###################
	FIND_POSTS_OF_CATEGORY_TIME_START = time.time()
	###########################################################
	for category in category_list:
		temp_result = find_posts_of_category(g.db, category['info_num'], category['tag'], now_date, SJ_NO_TOKEN_RECOMMENDATION_LIMIT)
		POST_LIST += list(temp_result)
	#각각의 카테고리의 포스트들을 불러오는 시간 측정 종료###################
	FIND_POSTS_OF_CATEGORY_TIME_END = time.time() - FIND_POSTS_OF_CATEGORY_TIME_START
	###########################################################



	#트랜드 스코어 반영하는 시간 측정 시작##############################
	TREND_TIME_START = time.time()
	###########################################################
	#트랜드 스코어 적용
	if trendscore_discriminate(now_date):
		for POST in POST_LIST:
			RANDOM = numpy.random.random()
			RANDOM *= SJ_RANDOM_WEIGHT
			TREND = trendscore(POST)

			POST['similarity'] = RANDOM + TREND
	
	#트랜드 스코어 미적용
	else:
		for POST in POST_LIST:
			RANDOM = numpy.random.random()
			RANDOM *= SJ_RANDOM_WEIGHT

			POST['similarity'] = RANDOM
	#트랜드 스코어 반영하는 시간 측정 종료##############################
	TREND_TIME_END = time.time() - TREND_TIME_START
	###########################################################

	SPEED_RESULT = {}
	SPEED_RESULT['NON_MEMBER_FIND_POSTS_OF_CATEGORY_TIME'] = FIND_POSTS_OF_CATEGORY_TIME_END
	SPEED_RESULT['NON_MEMBER_TREND_TIME'] = TREND_TIME_END
	SPEED_RESULT['NON_MEMBER_PROCESSING_POSTS_NUM'] = len(POST_LIST)

	return POST_LIST, SPEED_RESULT
