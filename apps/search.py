from flask import *
from flask_jwt_extended import *
from werkzeug import *
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
import operator
import math
import jpype
##########################################
from db_management import *
from global_func import *
import tknizer
##########################################
from variable import *


#BluePrint
BP = Blueprint('search', __name__)


#JAVA 스레드 이동.
jpype.attachThreadToJVM()

#유사도 스코어 측정
def match_score(token1, token2):
	MC = len(set(token1) & set(token2))
	MR = MC / len(token1)
	return MC * (1 + MR + math.floor(MR))

#priority_검색
@BP.route('/priority_search/<int:num>', methods = ['POST'])
@jwt_optional
def priority_search(num):
	#검색어 입력!
	search_str = request.form['search']

	#검색어로 시작되는 포스트들을 1차 regex 검색!
	title_regex = find_title_regex(g.db, search_str, 0)
	title_regex = list(title_regex)

	#공백 제거 및 토크나이져 작업
	del_space_list = search_str.split(' ')
	tokenizer_list = tknizer.get_tk(search_str)

	#FastText를 이용한 유사단어 추출
	ft_similarity_list = []
	for word in tokenizer_list:
		for sim_word in FastText.sim_words(word):
			if sim_word[1] >= SJ_FASTTEXT_SIM_PERCENT: 
				ft_similarity_list.append(sim_word[0])
			else: break	

	#로그인 판단 여부 확인.
	if get_jwt_identity():
		#USER 정보를 호출.
		USER = find_user(g.db, user_id=get_jwt_identity())

		#잘못된 USER 정보(잘못된 Token)일 때
		if USER is None: abort(401)

		#logging! (메인 로깅)
		insert_log(g.db, USER['user_id'], request.path)

		#DB search 로깅!
		search_logging(g.db, USER['user_id'], search_str, del_space_list, tokenizer_list, ft_similarity_list)

		#해당 유저의 갱신시간 갱신
		update_user_renewal(g.db, USER['user_id'])

	else:
		#logging! (메인 로깅)
		insert_log(g.db, request.remote_addr, request.path)

		#DB search 로깅!
		search_logging(g.db, "unknown", search_str, del_space_list, tokenizer_list, ft_similarity_list)		

	#토크나이져 처리된 리스트를 대상으로 검색하고, aggregate로 ids처리하여 posts 추출
	aggregate_posts = find_aggregate(g.db, tokenizer_list, 0, SJ_PS_LIMIT)
	aggregate_posts = list(aggregate_posts)

	#regex와 aggregate로 뽑힌 포스트를 합친다.
	aggregate_posts += title_regex

	##################################################
	#트랜드 스코어 용 date 함수
	now_time = datetime.now()
	year = now_time.year

	#Course Manual (수강편람 기간)
	CM_term_1 = (datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14))
	CM_term_2 = (datetime(year, 8, 1) < now_date) and (now_date < datetime(year, 8, 14))

	#Seasonal Semester (계절학기 기간)
	SS_term_1 = (datetime(year, 11, 25) < now_date) and (now_date < datetime(year, 12, 5))
	SS_term_2 = (datetime(year, 5, 25) < now_date) and (now_date < datetime(year, 6, 5))
	##################################################

	#수강편람/계절학기 기간!
	if (CM_term_1 or CM_term_2) or (SS_term_1 or SS_term_2):
		#검색 키워드와 문서간의 유사도 측정! (트렌드 적용 for)
		for post in aggregate_posts:
			#FAS 작업
			split_vector = FastText.get_doc_vector(del_space_list).tolist()
			FAS = FastText.vec_sim(split_vector, post['ft_vector'])

			T1 = match_score(del_space_list, post['title_token'])
			
			if tokenizer_list:
				T2 = match_score(tokenizer_list, set(post['token']+post['tag']))
			else: T2 =0

			if ft_similarity_list:
				T3 = match_score(ft_similarity_list, set(post['token']+post['tag']))
			else: T3 = 0

			#트랜드 스코어 적용!
			TREND = trendscore(post)

			post['similarity'] = round((T1 + T2 + T3 + FAS + TREND), 1)
			post['_id'] = str(post['_id'])

			#필요없는 반환 값 삭제
			del post['title_token']
			del post['token']
			del post['tag']
			del post['popularity']

	else:
		#검색 키워드와 문서간의 유사도 측정! (트렌드 비적용)
		for post in aggregate_posts:
			#FAS 작업
			split_vector = FastText.get_doc_vector(del_space_list).tolist()
			FAS = FastText.vec_sim(split_vector, post['ft_vector'])

			T1 = match_score(del_space_list, post['title_token'])
			
			if tokenizer_list:
				T2 = match_score(tokenizer_list, set(post['token']+post['tag']))
			else: T2 =0

			if ft_similarity_list:
				T3 = match_score(ft_similarity_list, set(post['token']+post['tag']))
			else: T3 = 0

			post['similarity'] = round((T1 + T2 + T3 + FAS), 1)
			post['_id'] = str(post['_id'])

			#필요없는 반환 값 삭제
			del post['title_token']
			del post['token']
			del post['tag']
			del post['popularity']

	#구해진 similarity - date로 내림차순 정렬
	aggregate_posts = sorted(aggregate_posts, key=operator.itemgetter('date'), reverse=True)
	aggregate_posts = sorted(aggregate_posts, key=operator.itemgetter('similarity'), reverse=True)

	#데이터로 들어온 상위 num개만 반환
	return jsonify(
		result = "success",
		search_result = aggregate_posts[:num])

#category_검색
@BP.route('/category_search/<int:type_check>/<int:num>', methods = ['POST'])
@jwt_optional
def category_search(type_check, num):
	search_str = request.form['search']

	#공백 제거
	del_space_str = search_str.split(' ')

	#토크나이져 작업
	tokenizer_list = tknizer.get_tk(search_str)

	#FastText를 이용한 유사단어 추출
	ft_similarity_list = []
	for word in tokenizer_list:
		for sim_word in FastText.sim_words(word):
			if sim_word[1] >= SJ_FASTTEXT_SIM_PERCENT: 
				ft_similarity_list.append(sim_word[0])
			else: break	

	aggregate_posts = find_aggregate(g.db, tokenizer_list, type_check, SJ_CS_LIMIT)
	aggregate_posts = list(aggregate_posts)

	##################################################
	#트랜드 스코어 용 date 함수
	now_time = datetime.now()
	year = now_time.year

	#Course Manual (수강편람 기간)
	CM_term_1 = (datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14))
	CM_term_2 = (datetime(year, 8, 1) < now_date) and (now_date < datetime(year, 8, 14))

	#Seasonal Semester (계절학기 기간)
	SS_term_1 = (datetime(year, 11, 25) < now_date) and (now_date < datetime(year, 12, 5))
	SS_term_2 = (datetime(year, 5, 25) < now_date) and (now_date < datetime(year, 6, 5))
	##################################################

	#수강편람/계절학기 기간!
	if (CM_term_1 or CM_term_2) or (SS_term_1 or SS_term_2):
		for post in aggregate_posts:
			#FAS 작업
			split_vector = FastText.get_doc_vector(del_space_str).tolist()
			FAS = FastText.vec_sim(split_vector, post['ft_vector'])

			T1 = match_score(del_space_str, post['title_token'])

			if tokenizer_list:
				T2 = match_score(tokenizer_list, set(post['token']+post['tag']))
			else:
				T2 =0

			if ft_similarity_list:
				T3 = match_score(ft_similarity_list, set(post['token']+post['tag']))
			else:
				T3 = 0

			#트랜드 스코어 적용!
			TREND = trendscore(post)

			post['similarity'] = round((T1 + T2 + T3 + FAS + TREND), 1)
			post['_id'] = str(post['_id'])

			#필요없는 반환 값 삭제
			del post['title_token']
			del post['token']
			del post['tag']
			del post['popularity']

	else:
		for post in aggregate_posts:
			#FAS 작업
			split_vector = FastText.get_doc_vector(del_space_str).tolist()
			FAS = FastText.vec_sim(split_vector, post['ft_vector'])

			T1 = match_score(del_space_str, post['title_token'])

			if tokenizer_list:
				T2 = match_score(tokenizer_list, set(post['token']+post['tag']))
			else:
				T2 =0

			if ft_similarity_list:
				T3 = match_score(ft_similarity_list, set(post['token']+post['tag']))
			else:
				T3 = 0

			post['similarity'] = round((T1 + T2 + T3 + FAS), 1)
			post['_id'] = str(post['_id'])

			#필요없는 반환 값 삭제
			del post['title_token']
			del post['token']
			del post['tag']
			del post['popularity']

	#구해진 similarity - date로 내림차순 정렬
	aggregate_posts = sorted(aggregate_posts, key=operator.itemgetter('date'), reverse=True)
	aggregate_posts = sorted(aggregate_posts, key=operator.itemgetter('similarity'), reverse=True)

	#데이터로 들어온 상위 num개만 반환
	return jsonify(
		result = "success",
		search_result = aggregate_posts[:num])

#domain_검색
@BP.route('/domain_search', methods = ['POST'])
@jwt_optional
def domain_search():
	search_str = request.form['search']

	#검색어 스플릿
	search_split = search_str.split(' ')
	search_split_set = set(search_split)
	

	#검색어 토크나이저 작업
	search_tokenizer = tknizer.get_tk(search_str)
	search_tokenizer_set = set(search_tokenizer)

	#도메인 전부 불러오기
	all_domain = find_all_domain(g.db)
	all_domain = list(all_domain)
	
	result = []

	for domain in all_domain:
		title_intersection_len = len(search_split_set & set(domain['title_token']))
		if (title_intersection_len / len(search_split_set)) > SJ_DOMAIN_SIM_PERCENT:
			result.append(domain)
			continue
		
		#토크나이저가 뽑혔을 때만!
		if search_tokenizer:
			token_intersection_len = len(search_tokenizer_set & set(domain['token']))
			if (token_intersection_len / len(search_tokenizer_set)) > SJ_DOMAIN_SIM_PERCENT:
				result.append(domain)


	return jsonify(
		result = "success",
		search_result = result)

#Full_search
@BP.route('/full_search/<int:num>', methods = ['POST'])
@jwt_optional
def full_search(num):
	search_str = request.form['search']

	#검색어로 시작되는 포스트들을 1차 regex 검색!
	title_regex = find_full_title_regex(g.db, search_str, num)
	title_regex = list(title_regex)

	#공백 제거
	del_space_list = search_str.split(' ')

	#토크나이져 작업
	tokenizer_list = tknizer.get_tk(search_str)

	#FastText를 이용한 유사단어 추출
	ft_similarity_list = []
	for word in tokenizer_list:
		for sim_word in FastText.sim_words(word):
			if sim_word[1] >= SJ_FASTTEXT_SIM_PERCENT: 
				ft_similarity_list.append(sim_word[0])
			else: break	

	if get_jwt_identity():
		#logging!
		insert_log(g.db, get_jwt_identity(), request.path, student_num = True)

		#USER 정보를 불러온다.
		USER = find_user(g.db, user_id=get_jwt_identity())

		#잘못된 USER 정보(잘못된 Token)일 때
		if USER is None: abort(400)

		#DB search 로깅!
		search_logging(g.db, USER['user_id'], search_str, del_space_list, tokenizer_list, ft_similarity_list)

	else:
		#logging!
		insert_log(g.db, request.remote_addr, request.path)
		#DB search 로깅!
		search_logging(g.db, "unknown", search_str, del_space_list, tokenizer_list, ft_similarity_list)		

	#토크나이져 처리된 리스트를 대상으로 검색하고, aggregate로 ids처리하여 posts 추출
	aggregate_posts = find_full_aggregate(g.db, tokenizer_list, num)
	aggregate_posts = list(aggregate_posts)

	#regex와 aggregate로 뽑힌 포스트를 합친다.
	aggregate_posts += title_regex

	#트랜드 스코어 용 now datetime
	now_time = datetime.now()

	#검색 키워드와 문서간의 유사도 측정!
	for post in aggregate_posts:
		T1 = match_score(del_space_list, post['title_token'])
		
		if tokenizer_list:
			T2 = match_score(tokenizer_list, set(post['token']+post['tag']))
		else: T2 =0

		if ft_similarity_list:
			T3 = match_score(ft_similarity_list, set(post['token']+post['tag']))
		else: T3 = 0

		#트랜드 스코어 적용!
		TREND = trendscore(post, now_time)

		post['similarity'] = round((T1 + T2 + T3 + FAS + TREND), 1)
		post['_id'] = str(post['_id'])

		#필요없는 반환 값 삭제
		del post['title_token']
		del post['token']
		del post['tag']
		del post['popularity']

	#구해진 similarity - date로 내림차순 정렬
	aggregate_posts = sorted(aggregate_posts, key=operator.itemgetter('date'), reverse=True)
	aggregate_posts = sorted(aggregate_posts, key=operator.itemgetter('similarity'), reverse=True)

	#데이터로 들어온 상위 num개만 반환
	return jsonify(
		result = "success",
		search_result = aggregate_posts[:num])

#search_logging 기록!
def search_logging(db, user_id, original_str, split_list, tokenizer_list, similarity_list):
	
	if user_id:
		USER_search_obj = {}
		USER_search_obj['original'] = original_str
		USER_search_obj['search_split'] = split_list
		USER_search_obj['tokenizer_split'] = tokenizer_list
		USER_search_obj['similarity_split'] = similarity_list
		USER_search_obj['date'] = datetime.now()

		#유저 searching 기록!
		update_user_search_list_push(db, user_id, USER_search_obj)

	#공용 searching 기록!
	insert_search_log(db, user_id, split_list)

#트렌드 스코어 계산
def trendscore(POST):
	#수강편람 except
	if POST['info'] == 'main_student' and ('수강편람' in POST['tag']):
		return 10 

	#계절학기 except
	elif POST['info'] == 'main_student' and ('계절학기' in POST['title_token']):
		return 4

	else: 
		return 0
