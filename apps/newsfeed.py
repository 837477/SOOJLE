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
		USER = find_user(g.db, _id=1, user_id=get_jwt_identity())
		
		#logging!
		insert_log(g.db, get_jwt_identity(), request.url)

		#접근한 뉴스피드 기록을 위한 obj 생성!
		newsfeed_obj = {}
		newsfeed_obj['newsfeed_name'] = newsfeed_type['newsfeed_name']
		newsfeed_obj['tag'] = newsfeed_type['tag']
		newsfeed_obj['date'] = datetime.now()

		#접근한 뉴스피드 기록!
		update_user_newsfeed_list_push(g.db, USER['_id'], newsfeed_obj)

	else:
		insert_log(g.db, request.full_path, request.url)

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
	#logging!
	if get_jwt_identity():
		insert_log(g.db, get_jwt_identity(), request.url)
	else:
		insert_log(g.db, request.full_path, request.url)

	result = find_popularity_newsfeed(g.db, SJ_RETURN_NUM)

	return jsonify(
		result = "success",
		newsfeed = dumps(result))

#추천 뉴스피드
@BP.route('/get_recommendation_newsfeed')
@jwt_optional
def get_recommendation_newsfeed():
	POST_LIST = find_all_posts(g.db, _id=1, topic=1, ft_vector=1, fav_cnt=1, view=1, tag=1, title=1, url=1, img=1, date=1, limit_=SJ_RECOMMENDATION_LIMIT)

	POST_LIST = list(POST_LIST)

	if get_jwt_identity():
		#logging
		insert_log(g.db, get_jwt_identity(), request.url)

		#유저를 _id, topic리스트, tag리스트 만 가져온다.
		USER = find_user(g.db, user_id=get_jwt_identity(), topic=1, tag=1, tag_sum=1, ft_vector=1)

		#유효한 토큰이 아닐 때 
		if USER is None: abort(400)

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
			IS = (((POST['fav_cnt']/Maxfav_cnt)*3) + ((POST['view']/Maxviews)))
			IS /= 4

			#RANDOM 작업
			RANDOM = numpy.random.random()
			RANDOM *= 2

			#최종 값 저장
			result = TOS + TAS + FAS + RANDOM

			POST['similarity'] = result

		#similarity를 기준으로 내림차순 정렬.
		POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)
	
	#Token이 안들어왔을 때
	else:
		insert_log(g.db, request.full_path, request.url)

	return jsonify(
		result = "success",
		newsfeed = dumps(POST_LIST[:SJ_RETURN_NUM]))
