from flask import *
from bson.json_util import dumps
from datetime import datetime
from numpy import dot
from numpy.linalg import norm
import operator
#####################################
from db_management import *
from global_func import *
#####################################
BP = Blueprint('newsfeed', __name__)
#####################################

#####################################
@BP.route('/get_newsfeed/<int:type>/<string:tags>/<string:date>/<int:pagenation>/<int:page>')
def get_newsfeed(type=None, tags=None, date=None, pagenation=None, page=None):
	
	if tags is not None:
		tag_list = tags.split('_')
	else:
		tag_list = []

	if date is not None:
		date = datetime.strptime(date, '%Y-%m-%d')
	else:
		date = datetime.now()

	result = find_newsfeed(g.db, None, tag_list, date, pagenation, page)

	return jsonify(
		posts = dumps(result),
		result = "success")

#인기 뉴스피드
@BP.route('/get_popularity_newsfeed/<int:num>')
def get_popularity_newsfeed(num=200):
	result = find_popularity_newsfeed(g.db, num)

	return jsonify(
		posts = dumps(result),
		result = "success")

#추천 뉴스피드
@BP.route('/get_recommendation_newsfeed')
@logging_time
def get_recommendation_newsfeed():
	#유저를 _id, topic리스트, tag리스트 만 가져온다.
	USER = find_user_topic_tag(g.db, 'XXXXXX')
	#데이트 정렬된 포스트 중 상위 200개만 _id, topic리스트, tag리스트, 조회수, 좋아요 만 가져온다.
	POST_LIST = find_all_posts(g.db, _id=1, topic=1, tag=1, view=1, fav_cnt=1, limit_=500)

	POST_LIST = loads(POST_LIST)

	#캐싱된 가장 높은 좋아요 수를 가져온다.
	MaxInterests = find_variable(g.db, 'highest_fav_cnt')
	#캐싱된 가장 높은 조회수를 가져온다.
	MaxViews = find_variable(g.db, 'highest_view')


	for POST in POST_LIST:
		#TOS 작업
		TOS = dot(USER['topic'], POST['topic'])/(norm(USER['topic'])*norm(POST['topic']))

		#TAS 작업
		post_tag_len = len(POST['tag'])
		intersection_len = len(set(USER['tag']) & set(POST['tag']))
		TAS = intersection_len / post_tag_len
	
		#IS 작업
		IS = (((POST['fav_cnt']/MaxInterests)*0.5) + ((POST['view']/MaxViews)*0.5)) * 1

		#RANDOM = rand_view = numpy.random.random()
		RANDOM = 0

		#TOS와 TAS와 IS의 결과를 result에 저장
		#except는 어떤 포스트의 노출도를 높히기위해 존재하기 때문에 모든 포스트에 적용시킬 필요는 없다. 추가 API를 생성할 예정.
		result = TOS + TAS + IS + RANDOM

		#해당 포스트에 similarity 결과를 삽입.
		POST['similarity'] = result

	#similarity를 기준으로 내림차순 정렬.
	result = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	return jsonify(result = dumps(POST_LIST))


#############################################
#############################################
