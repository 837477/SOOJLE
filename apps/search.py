from flask import *
from flask_jwt_extended import *
from werkzeug import *
##########################################
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
import operator
##########################################
from db_management import *
from global_func import *
import jpype
import tknizer
##########################################
BP = Blueprint('search', __name__)
##########################################
#JAVA 스레드 이동.
jpype.attachThreadToJVM()

@BP.route('/search_title', methods = ['POST'])
def search_title():
	start = time.time()

	search_str = request.form['search']

	#공백 제거
	del_space = search_str.split(' ')

	#공백이 제거된 검색어를 title_token을 DB에서 찾는다.
	search_post_list = find_title_token(g.db, del_space)
	search_post_list = list(search_post_list)

	for post in search_post_list:
		#DB에서 불러온 포스트의 title_token과 공백제거된 검색어랑 교집합을 시킨다.
		intersection = set(post['title_token']) & set(del_space)
		#교집합 시킨 갯수를 해당 포스트의 inter_cnt에 넣어준다.
		#기여도는 10000배
		post['inter_cnt'] = len(intersection) * 10000

	search_post_list = sorted(search_post_list, key=operator.itemgetter('inter_cnt'), reverse=True)

	print("time :", time.time() - start)
	print(len(search_post_list))

	return jsonify(
		result = "success",
		search_result = search_post_list[:100])

@BP.route('/search_token', methods = ['POST'])
def search_token():
	start = time.time()

	search_str = request.form['search']

	#토크나이저 처리
	tokenizer_str = tknizer.get_tk(search_str)

	#뽑힌 토크나이저가 없으면, 반환 결과 없다고 반환한다.
	if not tokenizer_str:
		return jsonify(result = "NONE")

	#토크나이저 처리된 검색어를 token을 DB에서 찾는다.
	search_post_list = find_token(g.db, tokenizer_str)
	search_post_list = list(search_post_list)

	for post in search_post_list:
		#DB에서 불러온 포스트의 token과 토크나이저 처리된 검색어랑 교집합을 시킨다.
		intersection = set(post['token']) & set(tokenizer_str)
		#교집합 시킨 갯수를 해당 포스트의 inter_cnt에 넣어준다.
		#기여도는 5000배
		post['inter_cnt'] = len(intersection) * 5000

	search_post_list = sorted(search_post_list, key=operator.itemgetter('inter_cnt'), reverse=True)

	print("time :", time.time() - start)
	print(len(search_post_list))

	return jsonify(
		result = "success",
		search_result = search_post_list[:100])

@BP.route('/search_ft_token', methods = ['POST'])
def search_ft_token():
	start = time.time()

	search_str = request.form['search']

	#토크나이저 처리
	tokenizer_str = tknizer.get_tk(search_str)

	#뽑힌 토크나이저가 없으면, 반환 결과 없다고 반환한다.
	if not tokenizer_str:
		return jsonify(result = "NONE")

	similarity_list = []
	for word in tokenizer_str:
		for sim_word in FastText.sim_words(word):
			if sim_word[1] >= 0.7: 
				similarity_list.append(sim_word[0])
			else: break	

	#FastText similarity 처리된 검색어를 token을 DB에서 찾는다.
	search_post_list = find_token(g.db, similarity_list)
	search_post_list = list(search_post_list)

	for post in search_post_list:
		#DB에서 불러온 포스트의 token과 토크나이저 처리된 검색어랑 교집합을 시킨다.
		intersection = set(post['token']) & set(similarity_list)
		#교집합 시킨 갯수를 해당 포스트의 inter_cnt에 넣어준다.
		#기여도는 5000배
		post['inter_cnt'] = len(intersection) * 2000

	search_post_list = sorted(search_post_list, key=operator.itemgetter('inter_cnt'), reverse=True)

	print("time :", time.time() - start)
	print(len(search_post_list))

	return jsonify(
		result = "success",
		search_result = search_post_list[:100])
