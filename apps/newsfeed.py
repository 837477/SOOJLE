from flask import *
from flask_jwt_extended import *
from werkzeug import *
#####################################
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
BP = Blueprint('newsfeed', __name__)
#####################################

#토픽별 뉴스피드
@BP.route('/get_topic_newsfeed/<int:type_num>')
def get_topic_newsfeed(type_num=None):
	POST_LIST = find_all_posts(g.db, _id=1, view=1, fav_cnt=1, info=1, title=1, post=1, url=1, img=1, limit_=3000)
	POST_LIST = loads(POST_LIST)

	result = []

	#대학교
	if None:
		for POST in POST_LIST:
			if PSOT['info'] == 'XXX':
				result.append(POST)
	#진로&구인
	elif type_num == 1:
		for POST in POST_LIST:
			if PSOT['info'] == 'XXX':
				result.append(POST)
	#공머전&행사
	elif type_num == 1:
		for POST in POST_LIST:
			if PSOT['info'] == 'XXX':
				result.append(POST)
	#동아리&모임
	elif type_num == 1:
		for POST in POST_LIST:
			if PSOT['info'] == 'XXX':
				result.append(POST)
	#장터
	elif type_num == 1:
		for POST in POST_LIST:
			if PSOT['info'] == 'XXX':
				result.append(POST)
	#자유
	else:
		for POST in POST_LIST:
			if PSOT['info'] == 'XXX':
				result.append(POST)
	
	return jsonify(
		result = "success",
		newsfeed = dumps(result))

#인기 뉴스피드
@BP.route('/get_popularity_newsfeed/<int:num>/<int:page>')
def get_popularity_newsfeed(num, page):
	#num : 몇개 대상 page : 반환 개수!
	result = find_popularity_newsfeed(g.db, num)
	result = list(result)

	return jsonify(
		result = "success",
		newsfeed = result[:page])

#추천 뉴스피드
@BP.route('/get_recommendation_newsfeed')
@jwt_optional
def get_recommendation_newsfeed():
	POST_LIST = find_all_posts(g.db, _id=1, topic=1, ft_vector=1, fav_cnt=1, view=1, tag=1, title=1, url=1, img=1, limit_=20000)

	POST_LIST = list(POST_LIST)

	if get_jwt_identity():
		#유저를 _id, topic리스트, tag리스트 만 가져온다.
		USER = find_user(g.db, user_id=get_jwt_identity(), topic=1, tag=1, tag_sum=1, ft_vector=1)

		#캐싱된 가장 높은 좋아요 수를 가져온다.
		Maxfav_cnt = find_variable(g.db, 'highest_fav_cnt')
		#캐싱된 가장 높은 조회수를 가져온다.
		Maxviews = find_variable(g.db, 'highest_view')
		
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
			IS = (((POST['fav_cnt']/Maxfav_cnt)*3) + ((POST['view']/Maxviews)))
			IS /= 4

			#RANDOM 작업
			RANDOM = numpy.random.random()
			RANDOM *= 2

			#최종 값 저장
			result = TOS + TAS + FAS + RANDOM

			del POST['topic']
			del POST['tag']
			del POST['ft_vector']

			#########################################
			#테스트 반환 디버깅용
			POST['_id'] = dumps(POST['_id'])
			POST['similarity'] = result
			POST['TOS'] = TOS
			POST['TAS'] = TAS
			POST['FAS'] = FAS
			POST['RANDOM'] = RANDOM
			#########################################

		#similarity를 기준으로 내림차순 정렬.
		POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	return jsonify(
		result = "success",
		newsfeed = POST_LIST[:200])

#################################################
#################################################
#################################################
@BP.route('/refresh_measurement', methods=['POST'])
#@BP.route('/refresh_measurement')
def refresh_measurement():
	LDA_ = request.form['LDA']
	FAST_ = request.form['FAST']

	USER = find_user(g.db, _id=1, user_id="test")

	#JAVA 스레드 이동.
	jpype.attachThreadToJVM()
	#토크나이저 실행!!
	LDA_ = get_tk(LDA_)
	FAST_ = get_tk(FAST_)

	LDA_result = LDA.get_topics(LDA_)
	FAST_result = FastText.get_doc_vector(FAST_)

	update_user_search_list_push(g.db, USER['_id'], (LDA_ + FAST_))

	POST_LIST = find_all_posts(g.db, _id=1, topic=1, token=1, ft_vector=1, tag=1)
	POST_LIST = list(POST_LIST)

	for POST in POST_LIST:
		#TOS 작업
		TOS = dot(LDA_result, POST['topic'])/(norm(LDA_result)*norm(POST['topic']))

		#FAS 작업
		FAS = FastText.vec_sim(FAST_result, POST['ft_vector'])

		POST['similarity'] = TOS + FAS

	#similarity를 기준으로 내림차순 정렬.
	POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	cnt = 0
	for i in range(1000):
		if cnt != 500:
			fav_obj = {}
			fav_obj['_id'] = POST_LIST[i]['_id']
			fav_obj['topic'] = POST_LIST[i]['topic']
			fav_obj['token'] = POST_LIST[i]['token']
			fav_obj['tag'] = POST_LIST[i]['tag']
			fav_obj['date'] = datetime.now()

			#유저 fav_list에 추가.
			result = update_user_fav_list_push(g.db, USER['_id'], fav_obj)

		view_obj = {}
		view_obj['_id'] = POST_LIST[i]['_id']
		view_obj['topic'] = POST_LIST[i]['topic']
		view_obj['token'] = POST_LIST[i]['token']
		view_obj['tag'] = POST_LIST[i]['tag']
		view_obj['date'] = datetime.now()

		#유저 view_list에 추가.
		update_user_view_list_push(g.db, USER['_id'], view_obj)

		cnt += 1

	measurement_run(400)

	return jsonify(result = "success")




