from flask import *
from flask_jwt_extended import *
from werkzeug import *
##########################################
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
import operator
import math
from numpy import dot
from numpy.linalg import norm
import numpy
##########################################
from db_management import *
from global_func import *
import jpype
import tknizer
##########################################
BP = Blueprint('simulation', __name__)
##########################################

#입력된 str을 split 해주는 API
@BP.route('/simulation_split/<string:input_str>')
def simulation_split(input_str):
	result = input_str.split(' ')

	return jsonify(
		result = "success",
		simulation = result)

#입력된 str을 tokenizer 해주는 API
@BP.route('/simulation_tokenizer/<string:input_str>')
def simulation_tokenizer(input_str):
	result = tknizer.get_tk(input_str)
	
	return jsonify(
		result = "success",
		simulation = result)

#simulation_priority_검색 API
@BP.route('/simulation_priority_search/<int:num>', methods = ['POST'])
def simulation_priority_search(num):
	search_str = request.form['search']

	#공백 제거
	del_space_list = search_str.split(' ')

	#토크나이져 작업
	tokenizer_list = tknizer.get_tk(search_str)

	#FastText를 이용한 유사단어 추출
	ft_similarity_list = []
	for word in tokenizer_list:
		for sim_word in FastText.sim_words(word):
			if sim_word[1] >= 0.7: 
				ft_similarity_list.append(sim_word[0])
			else: break	


	#토크나이져 처리된 리스트를 대상으로 검색하고, aggregate로 ids처리하여 posts 추출
	aggregate_posts = find_aggregate(g.db, tokenizer_list, 0)
	aggregate_posts = list(aggregate_posts)

	for post in aggregate_posts:
		T1 = match_score(del_space_list, post['title_token'])
		
		if tokenizer_list:
			T2 = match_score(tokenizer_list, set(post['token']+post['tag']))
		else: T2 =0

		if ft_similarity_list:
			T3 = match_score(ft_similarity_list, set(post['token']+post['tag']))
		else: T3 = 0

		post['similarity'] = T1 + T2 + T3
		post['_id'] = str(post['_id'])

		#필요없는 반환 값 삭제
		del post['title_token']
		del post['token']
		del post['tag']
		del post['popularity']

	#구해진 similarity로 내림차순 정렬
	aggregate_posts = sorted(aggregate_posts, key=operator.itemgetter('similarity'), reverse=True)

	#데이터로 들어온 상위 num개만 반환
	return jsonify(
		result = "success",
		search_result = aggregate_posts[:num])

#simulation_category_검색 API
@BP.route('/simulation_category_search/<int:type_check>/<int:num>', methods = ['POST'])
def simulation_category_search(type_check, num):
	search_str = request.form['search']

	#공백 제거
	del_space_str = search_str.split(' ')

	#토크나이져 작업
	tokenizer_list = tknizer.get_tk(search_str)

	#FastText를 이용한 유사단어 추출
	ft_similarity_list = []
	for word in tokenizer_list:
		for sim_word in FastText.sim_words(word):
			if sim_word[1] >= 0.7: 
				ft_similarity_list.append(sim_word[0])
			else: break	

	aggregate_posts = find_aggregate(g.db, tokenizer_list, type_check)

	aggregate_posts = list(aggregate_posts)

	#regex와 aggregate로 뽑힌 포스트를 합친다.
	aggregate_posts += title_regex

	for post in aggregate_posts:
		T1 = match_score(del_space_str, post['title_token'])

		if tokenizer_list:
			T2 = match_score(tokenizer_list, set(post['token']+post['tag']))
		else:
			T2 =0

		if ft_similarity_list:
			T3 = match_score(ft_similarity_list, set(post['token']+post['tag']))
		else:
			T3 = 0

		post['similarity'] = T1 + T2 + T3
		post['_id'] = str(post['_id'])

		#필요없는 반환 값 삭제
		del post['title_token']
		del post['token']
		del post['tag']
		del post['popularity']

	#구해진 similarity로 내림차순 정렬
	aggregate_posts = sorted(aggregate_posts, key=operator.itemgetter('similarity'), reverse=True)

	#데이터로 들어온 상위 num개만 반환
	return jsonify(
		result = "success",
		search_result = aggregate_posts[:num])

#해당 USER의 관심도 반환 API
@BP.route('/simulation_get_user_measurement/<string:user_id>')
def simulation_get_user_measurement(user_id):
	USER = find_user(g.db, user_id=user_id, user_name=1, user_major=1, topic=1, tag=1, ft_vector=1)

	if USER is None: abort(400)

	return jsonify(
		result = "success",
		user = USER)

def match_score(token1, token2):
	MC = len(set(token1) & set(token2))
	MR = MC / len(token1)
	return MC * (1 + MR + math.floor(MR))

