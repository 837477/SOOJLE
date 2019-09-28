from flask import *
from bson.json_util import dumps
from db_management import *
from global_func import *
from datetime import datetime
import operator

BP = Blueprint('newsfeed', __name__)

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
@BP.route('/get_recommendation_newsfeed/<int:num>')
def get_recommendation_newsfeed(num):
	#해당 유저의 유사도를 가져온다.
	user_similarity = find_user_similarity(g.db, "16011092")

	#similarity를 기준으로 내림차순 정렬.
	sort_similarity = sorted(user_similarity, key=operator.itemgetter('similarity'), reverse=True)

	#pymongo로 보낼 post_obi들이 들어갈 리스트 생성
	target_post = []

	#이미 정렬이 되었은, similarity를 삭제.
	for post in sort_similarity:
		del post['similarity']

	#정렬된 post_obi를 db에서 찾기 (or연산임 해당 obi들이 있는건 그냥 다 가지고옴)
	result = find_recommendation_newsfeed(g.db, sort_similarity[:num])

	return jsonify(
		posts = result)

	




#############################################
#############################################
