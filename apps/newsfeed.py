from flask import *
from flask_jwt_extended import *
from werkzeug import *
from bson.json_util import dumps
from datetime import datetime
from numpy import dot
from numpy.linalg import norm
import numpy
import operator
#####################################
from db_management import *
from global_func import *
#####################################
from variable import *

#BluePrint
BP = Blueprint('newsfeed', __name__)


#토픽별 뉴스피드
@BP.route('/get_newsfeed_of_topic/<string:newsfeed_name>')
@jwt_optional
def get_newsfeed_of_topic(newsfeed_name):
	#요청한 뉴스피드에 대한 정보를 가져온다.
	newsfeed_type = find_newsfeed_of_topic(g.db, newsfeed_name)

	#logging!
	if get_jwt_identity():
		#USER를 불러온다.
		USER = find_user(g.db, _id=1, user_id=get_jwt_identity(), topic=1, tag=1, tag_sum=1, ft_vector=1)
		
		#유효한 토큰이 아닐 때 
		if USER is None: abort(400)

		#logging! (메인 로그)
		insert_log(g.db, get_jwt_identity(), request.path, student_num = True)

		#접근한 뉴스피드 기록을 위한 obj 생성!
		newsfeed_obj = {}
		newsfeed_obj['newsfeed_name'] = newsfeed_type['newsfeed_name']
		newsfeed_obj['tag'] = newsfeed_type['tag']
		newsfeed_obj['date'] = datetime.now()

		#접근한 뉴스피드 기록!
		update_user_newsfeed_list_push(g.db, USER['_id'], newsfeed_obj)

		#해당 유저의 갱신시간 갱신
		update_user_renewal(g.db, USER['user_id'])

		#info를 정규표현식으로 부르기위해 or연산자로 join
		info = "|".join(newsfeed_type['info'])

		#공모전&행사 뉴스피드는 사용자 관심도도 측정하여 따로 반환
		if newsfeed_name == '공모전&행사':
			POST_LIST = find_newsfeed(g.db, info, newsfeed_type['tag'], newsfeed_type['negative_tag'], SJ_RETURN_NUM)

			POST_LIST = list(POST_LIST)

			for POST in POST_LIST:
				#TOS 작업
				TOS = dot(USER['topic'], POST['topic'])/(norm(USER['topic'])*norm(POST['topic']))

				#TAS 작업
				USER_TAG = USER['tag'].keys()
				TAG = USER_TAG & set(POST['tag'])
				inter_sum = 0
				for i in TAG:
					inter_sum += USER['tag'][i]
				TAS = inter_sum / USER['tag_sum']
				
				#FAS 작업
				FAS = FastText.vec_sim(USER['ft_vector'], POST['ft_vector'])

				#RANDOM 작업
				RANDOM = numpy.random.random()

				#가중치 작업
				TOS *= SJ_TOS_WEIGHT
				TAS *= SJ_TAS_WEIGHT
				FAS *= SJ_FAS_WEIGHT
				RANDOM *= SJ_RANDOM_WEIGHT

				POST['similarity'] = TOS + TAS + FAS + RANDOM

			#similarity를 기준으로 내림차순 정렬.
			POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

			return jsonify(
				result = "success",
				newsfeed = dumps(POST_LIST))

	#비로그인!
	else:
		#logging! (메인 로그)
		insert_log(g.db, request.remote_addr, request.path, student_num=None)

	#info를 정규표현식으로 부르기위해 or연산자로 join
	info = "|".join(newsfeed_type['info'])

	result = find_newsfeed(g.db, info, newsfeed_type['tag'], newsfeed_type['negative_tag'], SJ_RETURN_NUM)

	return jsonify(
		result = "success",
		newsfeed = dumps(result))

#인기 뉴스피드
@BP.route('/get_popularity_newsfeed')
@jwt_optional
def get_popularity_newsfeed():
	#logging! (메인 로그)
	if get_jwt_identity():
		#유저 확인
		USER = find_user(g.db, user_id=get_jwt_identity())

		#유효한 토큰이 아닐 때 
		if USER is None: abort(400)

		#logging (메인 로그)
		insert_log(g.db, USER['user_id'], request.path, student_num = True)
		#방문자 로그 기록!
		insert_today_visitor(g.db, USER['user_id'], student_num=True)

	else:
		insert_log(g.db, request.remote_addr, request.path)

	result = find_popularity_newsfeed(g.db, SJ_RETURN_NUM)

	return jsonify(
		result = "success",
		newsfeed = dumps(result))

#추천 뉴스피드
@BP.route('/get_recommendation_newsfeed')
@jwt_optional
def get_recommendation_newsfeed():
	POST_LIST = find_all_posts(g.db, _id=1, topic=1, ft_vector=1, fav_cnt=1, view=1, tag=1, title=1, info=1, title_token=1, url=1, img=1, date=1, limit_=SJ_RECOMMENDATION_LIMIT)

	POST_LIST = list(POST_LIST)
	
	now_date = datetime.now()

	#회원일 때!
	if get_jwt_identity():
		#유저를 _id, topic리스트, tag리스트 만 가져온다.
		USER = find_user(g.db, user_id=get_jwt_identity(), topic=1, tag=1, tag_sum=1, ft_vector=1)

		#유효한 토큰이 아닐 때 
		if USER is None: abort(400)

		#logging (메인 로그)
		insert_log(g.db, USER['user_id'], request.path, student_num = True)
		#방문자 로그 기록!
		insert_today_visitor(g.db, USER['user_id'], student_num=True)

		#회원 관심도가 cold 상태일 때!
		if USER['tag_sum'] == 1:
			#비로그인일 때 추천뉴스피드 호출!
			POST_LIST = get_recommendation_newsfeed_2(g.db, now_date)	
		#관심도가 cold가 아닐 때!
		else:
			#캐싱된 가장 높은 좋아요 수를 가져온다.
			Maxfav_cnt = find_variable(g.db, 'highest_fav_cnt')
			#캐싱된 가장 높은 조회수를 가져온다.
			Maxviews = find_variable(g.db, 'highest_view_cnt')
			
			for POST in POST_LIST:
				#TOS 작업
				TOS = dot(USER['topic'], POST['topic'])/(norm(USER['topic'])*norm(POST['topic']))

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
				TREND = trendscore(POST, now_date)

				#최종 값 저장
				result = TOS + TAS + FAS + RANDOM + TREND

				POST['similarity'] = result

	#비회원일 때! (no token)
	else:
		#logging (메인 로그)
		insert_log(g.db, request.remote_addr, request.path, student_num=None)
		#방문자 로그 기록!
		insert_today_visitor(g.db, request.remote_addr, student_num=None)

		#비로그인일 때 추천뉴스피드 호출!
		POST_LIST = get_recommendation_newsfeed_2(g.db, now_date)		

	#similarity를 기준으로 내림차순 정렬.
	POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	return jsonify(
		result = "success",
		newsfeed = dumps(POST_LIST[:SJ_RETURN_NUM]))

#비회원 추천 뉴스피드
def get_recommendation_newsfeed_2(db, now_date):
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

	for POST in POST_LIST:
		RANDOM = numpy.random.random()
		RANDOM *= SJ_RANDOM_WEIGHT
		TREND = trendscore(POST, now_date)

		result = RANDOM + TREND

		POST['similarity'] = result
	
	return POST_LIST

#트렌드 스코어 계산
def trendscore(POST, now_date):
	year = now_date.year

	#Course Manual (수강편람 기간)
	CM_term_1 = (datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14))
	CM_term_2 = (datetime(year, 8, 1) < now_date) and (now_date < datetime(year, 8, 14))

	#Seasonal Semester (계절학기 기간)
	SS_term_1 = (datetime(year, 11, 25) < now_date) and (now_date < datetime(year, 12, 5))
	SS_term_2 = (datetime(year, 5, 25) < now_date) and (now_date < datetime(year, 6, 5))

	#수강편람 except
	if POST['info'] == 'main_student' and ('수강편람' in POST['tag']) and (CM_term_1 or CM_term_2):
		return 10 

	#계절학기 except
	elif POST['info'] == 'main_student' and ('계절학기' in POST['title_token']) and (SS_term_1 or SS_term_2):
		return 4

	else: 
		return 0

	