from flask import *
from flask_jwt_extended import *
from werkzeug import *
##########################################
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
import operator
import math
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

def match_score(token1, token2):
	MC = len(set(token1) & set(token2))
	MR = MC / len(token1)
	return MC * (1 + MR + math.floor(MR))

@BP.route('/priority_search/<int:num>', methods = ['POST'])
def priority_search(num):
	search_str = request.form['search']

	#검색어로 시작되는 포스트들을 1차 regex 검색!
	title_regex = find_title_regex(g.db, search_str)
	title_regex = list(title_regex)

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

	#토크나이져 처리된 리스트를 대상으로 검색하고, aggregate로 ids처리하여 posts 추출
	aggregate_posts = find_aggregate(g.db, tokenizer_list, 0)
	aggregate_posts = list(aggregate_posts)

	#regex와 aggregate로 뽑힌 포스트를 합친다.
	aggregate_posts += title_regex

	for post in aggregate_posts:
		post['_id'] = dumps(post['_id'])
		T1 = match_score(del_space_str, post['title_token'])
		T2 = match_score(tokenizer_list, set(post['token']+post['tag']))
		T3 = match_score(ft_similarity_list, set(post['token']+post['tag']))

		post['similarity'] = T1 + T2 + T3

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

@BP.route('/category_search/<int:community_check>/<int:num>', methods = ['POST'])
def category_search(community_check, num):
	search_str = request.form['search']

	#검색어로 시작되는 포스트들을 1차 regex 검색!
	title_regex = find_title_regex(g.db, search_str)
	title_regex = list(title_regex)

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

	#비 커뮤니티만!
	if community_check == 1:
		aggregate_posts = find_aggregate(g.db, tokenizer_list, 1)
	#커뮤니티만!
	else:
		aggregate_posts = find_aggregate(g.db, tokenizer_list, 2)

	aggregate_posts = list(aggregate_posts)

	#regex와 aggregate로 뽑힌 포스트를 합친다.
	aggregate_posts += title_regex

	for post in aggregate_posts:
		post['_id'] = dumps(post['_id'])
		T1 = match_score(del_space_str, post['title_token'])
		T2 = match_score(tokenizer_list, set(post['token']+post['tag']))
		T3 = match_score(ft_similarity_list, set(post['token']+post['tag']))

		post['similarity'] = T1 + T2 + T3

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