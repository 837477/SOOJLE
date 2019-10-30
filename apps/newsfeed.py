from flask import *
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
@BP.route('/get_popularity_newsfeed/<int:num>')
def get_popularity_newsfeed(num=500):
	result = find_popularity_newsfeed(g.db, num)

	return jsonify(
		result = "success",
		newsfeed = dumps(result))

#추천 뉴스피드
@BP.route('/get_recommendation_newsfeed')
@jwt_optional
@logging_time
def get_recommendation_newsfeed():
	print("시작한다!")
	#데이트 정렬된 포스트 중 상위 500개만 가져온다.
	POST_LIST = find_all_posts(g.db, _id=None, topic=1, tag=1, view=1, fav_cnt=1, info=1, title=1, post=1, url=1, img=1, limit_=None)

	POST_LIST = list(POST_LIST)

	if get_jwt_identity():
		print("들어간다!")
		#유저를 _id, topic리스트, tag리스트 만 가져온다.
		USER = find_user(g.db, user_id=get_jwt_identity(), topic=1, tag=1)
		
		#캐싱된 가장 높은 좋아요 수를 가져온다.
		MaxInterests = find_variable(g.db, 'highest_fav_cnt')
		#캐싱된 가장 높은 조회수를 가져온다.
		MaxViews = find_variable(g.db, 'highest_view')

		for POST in POST_LIST:
			#TOS 작업
			TOS = dot(USER['topic'], POST['topic'])/(norm(USER['topic'])*norm(POST['topic']))

			#TAS 작업
			# post_tag_len = len(POST['tag'])
			# intersection_len = len(set(USER['tag']) & set(POST['tag']))
			# TAS = intersection_len / post_tag_len
			TAS = 0
		
			#IS 작업
			#IS = (((POST['fav_cnt']/MaxInterests)*0.5) + ((POST['view']/MaxViews)*0.5)) * 1
			IS = 0

			#RANDOM = rand_view = numpy.random.random()
			RANDOM = 0

			#TOS와 TAS와 IS의 결과를 result에 저장
			#except는 어떤 포스트의 노출도를 높히기위해 존재하기 때문에 모든 포스트에 적용시킬 필요는 없다. 추가 API를 생성할 예정.
			result = TOS + TAS + IS + RANDOM

			#해당 포스트에 similarity 결과를 삽입.
			POST['similarity'] = result
			POST['TOS'] = TOS
			POST['TAS'] = TAS

		#similarity를 기준으로 내림차순 정렬.
		POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)


	return jsonify(
		result = "success",
		newsfeed = POST_LIST[:1000])


#############################################
#############################################
