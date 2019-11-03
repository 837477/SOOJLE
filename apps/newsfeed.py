import requests

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
@BP.route('/get_popularity_newsfeed/<int:num>')
def get_popularity_newsfeed(num=500):
	result = find_popularity_newsfeed(g.db, num)

	return jsonify(
		result = "success",
		newsfeed = dumps(result))

#추천 뉴스피드
@BP.route('/get_recommendation_newsfeed')
@jwt_optional
#@logging_time
def get_recommendation_newsfeed():
	print("시작한다!")
	#데이트 정렬된 포스트 중 상위 X개만 가져온다.
	POST_LIST = find_all_posts(g.db, _id=1, topic=1, tag=1, view=1, fav_cnt=1, info=1, title=1, post=1, url=1, img=1, limit_=None)

	POST_LIST = list(POST_LIST)

	if get_jwt_identity():
		print("들어간다!")
		#유저를 _id, topic리스트, tag리스트 만 가져온다.
		USER = find_user(g.db, user_id=get_jwt_identity(), topic=1, tag=1)
		
		USER_TAG_SUM = sum(USER['tag'].values())

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
			TAS = inter_sum / USER_TAG_SUM
			
			#IS 작업
			IS = (((POST['fav_cnt']/Maxfav_cnt)*0.6) + ((POST['view']/Maxviews)*0.4))

			#RANDOM 작업
			RANDOM = numpy.random.random()

			#최종 값 저장
			result = TOS + TAS + IS + RANDOM

			#########################################
			#테스트 반환 디버깅용
			POST['_id'] = dumps(POST['_id'])
			POST['similarity'] = result
			POST['TOS'] = TOS
			POST['TAS'] = TAS
			#########################################

		#similarity를 기준으로 내림차순 정렬.
		POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	return jsonify(
		result = "success",
		newsfeed = POST_LIST[:1000])


#############################################
#############################################
@BP.route('/testtesttest')
@jwt_optional
def testtesttest():
	print("시작한다!")
	#데이트 정렬된 포스트 중 상위 X개만 가져온다.
	POST_LIST = find_all_posts(g.db, _id=1, topic=1, tag=1, view=1, fav_cnt=1, info=1, title=1, post=1, url=1, img=1, limit_=None)

	POST_LIST = list(POST_LIST)

	if get_jwt_identity():
		print("들어간다!")
		#유저를 _id, topic리스트, tag리스트 만 가져온다.
		USER = find_user(g.db, user_id=get_jwt_identity(), topic=1, tag=1)
		
		USER_TAG_SUM = sum(USER['tag'].values())

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
			TAS = inter_sum / USER_TAG_SUM
			
			#IS 작업
			IS = (((POST['fav_cnt']/Maxfav_cnt)*0.6) + ((POST['view']/Maxviews)*0.4))

			#RANDOM 작업
			RANDOM = numpy.random.random()

			#최종 값 저장
			result = TOS + TAS + IS + RANDOM

			POST['similarity'] = result

		#similarity를 기준으로 내림차순 정렬.
		POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

		###################################################
		###################################################

		token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjkwNjMxODcsIm5iZiI6MTU2OTA2MzE4NywianRpIjoiNDJjYTU3MTEtM2EzNC00OGNhLWJiYWQtZWI0MzU3MGQ2MDFiIiwiaWRlbnRpdHkiOiIxNjAxMTA5MiIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.sk6XgTJmJiNHRQQevm_BBYwmG1quyfXPW19KCDS9ZWw"
		header = {'Authorization':"Bearer " + token}
		#data = {'id':'admin', 'pw':'imlisgod'}

		# for i in range(500):
		# 	if i <= 200:
		# 		url = "http://localhost:5000/post_like/" + str(POST_LIST[i]['_id'])
		# 		html = requests.get(url, headers =header, data = data).content
		# 		html = json.loads(html)
		# 		print(html)

		# 	url2 = "http://localhost:5000/post_view/" + str(POST_LIST[i]['_id'])
		# 	html2 = requests.get(url2, headers =header, data = data).content
		# 	html2 = json.loads(html2)
		# 	print(html2)

		

		# for i in range(100):
		# 	data = {'search': POST_LIST[i]['post']}
		# 	url = "http://localhost:5000/search"
		# 	html = requests.post(url, headers =header, data = data).content
		# 	html = json.loads(html)
		# 	print(html)