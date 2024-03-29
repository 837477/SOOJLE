from flask import *
from flask_jwt_extended import *
from werkzeug import *
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
import operator
import math
import jpype
import time
##########################################
from db_management import *
from global_func import *
import tknizer
##########################################
from variable import *


#BluePrint
BP = Blueprint('search', __name__)

#유사도 스코어 측정
def match_score(token1, token2):
	MC = len(set(token1) & set(token2))
	MR = MC / len(token1)
	return MC * (1 + MR + math.floor(MR))

#검색 로깅 (작동중)
@BP.route('/api/v1/search/logging', methods=['POST'])
@jwt_optional
def SJ_api_v1_search__logging():
	#JAVA 스레드 이동.
	jpype.attachThreadToJVM()

	#검색어 입력!
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

	#로그인 판단 여부 확인.
	if get_jwt_identity():
		#USER 정보를 호출.
		USER = find_user(g.db, user_id=get_jwt_identity())

		#잘못된 USER 정보(잘못된 Token)일 때
		if USER is None: abort(401)

		#유저 searching object 생성!
		USER_search_obj = {}
		USER_search_obj['original'] = search_str
		USER_search_obj['search_split'] = del_space_str
		USER_search_obj['tokenizer_split'] = tokenizer_list
		USER_search_obj['similarity_split'] = ft_similarity_list
		USER_search_obj['date'] = datetime.now()

		#유저 searching 기록!
		update_user_search_list_push(g.db, USER['user_id'], USER_search_obj)

		#공용 searching 기록!
		insert_search_log(g.db, USER['user_id'], del_space_str)

	else:
		#공용 searching 기록!
		insert_search_log(g.db, "unknown", del_space_str)

	return jsonify(
			result = "success"
		)

#category (작동중)
@BP.route('/api/v1/search/category/<string:category_name>/<int:num>', methods = ['POST'])
@jwt_optional
def SJ_api_v1_search__category(category_name, num):
	#JAVA 스레드 이동.
	jpype.attachThreadToJVM()

	#총 시간 측정#################################################
	TOTAL_TIME_START = time.time()
	###########################################################
	
	#검색어 입력!
	search_str = request.form['search']

	#길이 체크
	if len(search_str) > SJ_REQUEST_LENGTH_LIMIT['search_max']:
		return jsonify(result = "long string")

	#공백 제거
	del_space_str = search_str.split(' ')

	#토크나이저 시간 측정###########################################
	TOKENIZER_TIME_START = time.time()
	###########################################################
	#토크나이져 작업
	tokenizer_list = tknizer.get_tk(search_str)
	#토크나이저 측정 종료###########################################
	TOKENIZER_TIME_END = time.time() - TOKENIZER_TIME_START
	###########################################################

	#FT 유사 단어 추출 시간 측정#####################################
	FASTTEXT_TIME_START = time.time()
	###########################################################
	#FastText를 이용한 유사단어 추출
	ft_similarity_list = []
	for word in tokenizer_list:
		for sim_word in FastText.sim_words(word):
			if sim_word[1] >= SJ_FASTTEXT_SIM_PERCENT: 
				ft_similarity_list.append(sim_word[0])
			else: break	
	#FT 유사 단어 추출 시간 측정#####################################
	FASTTEXT_TIME_END = time.time() - FASTTEXT_TIME_START
	###########################################################


	#카테고리 불러오기!
	category_type = find_category_of_topic(g.db, category_name)

	#최종 검색 키워드 리스트
	final_search_keyword = list(set(ft_similarity_list + tokenizer_list + del_space_str))

	#find_search_of_category 시간 측정 (불러와서 리스트화 시킨 시간)####
	FIND_SEARCH_OF_CATEGORY_TIME_START = time.time()
	###########################################################
	#해당 카테고리에서 검색어와 관련된 포스트 불러오기!
	POST_LIST = find_search_of_category_default_date(g.db, final_search_keyword, category_type['info_num'], SJ_CS_DEFAULT_DATE, SJ_CS_LIMIT)
	POST_LIST = list(POST_LIST)

	#만약 1년 이내의 게시글이 1개도 안나왔을 경우, default_date를 0으로 설정
	if POST_LIST == 0:
		POST_LIST = find_search_of_category(g.db, final_search_keyword, category_type['info_num'], SJ_CS_LIMIT)
		POST_LIST = list(POST_LIST)

	#find_search_of_category 시간 측정 (불러와서 리스트화 시킨 시간)####
	FIND_SEARCH_OF_CATEGORY_TIME_END = time.time() - FIND_SEARCH_OF_CATEGORY_TIME_START
	###########################################################

	#현재 날짜 가져오기.
	now_date = datetime.now()

	#매치스코어 + 트랜드 반영/미반영 시간 측정##########################
	MATCH_TREND_TIME_START = time.time()
	###########################################################

	#트랜드 스코어 적용 판별########################################
	#트랜드 스코어 적용일 시
	if trendscore_discriminate(now_date):
		for POST in POST_LIST:
			#FAS 작업
			split_vector = FastText.get_doc_vector(del_space_str).tolist()
			FAS = FastText.vec_sim(split_vector, POST['ft_vector'])

			T1 = match_score(del_space_str, POST['title_token'])

			if tokenizer_list:
				T2 = match_score(tokenizer_list, set(POST['token']+POST['tag']))
			else:
				T2 =0

			if ft_similarity_list:
				T3 = match_score(ft_similarity_list, set(POST['token']+POST['tag']))
			else:
				T3 = 0

			#트랜드 스코어 적용!
			TREND = trendscore(POST)

			POST['similarity'] = round((T1 + T2 + T3 + FAS + TREND), 1)
			POST['_id'] = str(POST['_id'])

			#필요없는 반환 값 삭제
			del POST['title_token']
			del POST['token']
			del POST['tag']
			del POST['popularity']
	
	#트랜드 스코어 적용 안할 시
	else:
		for POST in POST_LIST:
			#FAS 작업
			split_vector = FastText.get_doc_vector(del_space_str).tolist()
			FAS = FastText.vec_sim(split_vector, POST['ft_vector'])

			T1 = match_score(del_space_str, POST['title_token'])

			if tokenizer_list:
				T2 = match_score(tokenizer_list, set(POST['token']+POST['tag']))
			else:
				T2 =0

			if ft_similarity_list:
				T3 = match_score(ft_similarity_list, set(POST['token']+POST['tag']))
			else:
				T3 = 0

			POST['similarity'] = round((T1 + T2 + T3 + FAS), 1)
			POST['_id'] = str(POST['_id'])

			#필요없는 반환 값 삭제
			del POST['title_token']
			del POST['token']
			del POST['tag']
			del POST['popularity']
	
	#매치스코어 + 트랜드 반영/미반영 시간 측정##########################
	MATCH_TREND_TIME_END = time.time() - MATCH_TREND_TIME_START
	###########################################################

	#구해진 similarity - date로 내림차순 정렬
	POST_LIST = sorted(POST_LIST, key=operator.itemgetter('date'), reverse=True)
	POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	#총 시간 측정 종료#############################################
	TOTAL_TIME_END = time.time() - TOTAL_TIME_START
	###########################################################

	SPEED_RESULT = {}
	SPEED_RESULT['TOKENIZER_TIME'] = TOKENIZER_TIME_END
	SPEED_RESULT['FASTTEXT_TIME'] = FASTTEXT_TIME_END
	SPEED_RESULT['FIND_SEARCH_OF_CATEGORY_TIME'] = FIND_SEARCH_OF_CATEGORY_TIME_END
	SPEED_RESULT['MATCH_TREND_TIME'] = MATCH_TREND_TIME_END
	SPEED_RESULT['TOTAL_TIME'] = TOTAL_TIME_END
	SPEED_RESULT['PROCESSING_POSTS_NUM'] = len(POST_LIST)
	SPEED_RESULT['RETURN_NUM'] = num

	#데이터로 들어온 상위 num개만 반환
	return jsonify(
			result = "success",
			search_result = POST_LIST[:num],
			speed_result = SPEED_RESULT
		)

#category (작동중)
@BP.route('/api/v1/search/category_no_limit/<string:category_name>/<int:num>', methods = ['POST'])
@jwt_optional
def SJ_api_v1_search__category_no_limit(category_name, num):
	#JAVA 스레드 이동.
	jpype.attachThreadToJVM()

	#총 시간 측정#################################################
	TOTAL_TIME_START = time.time()
	###########################################################
	
	#검색어 입력!
	search_str = request.form['search']

	#길이 체크
	if len(search_str) > SJ_REQUEST_LENGTH_LIMIT['search_max']:
		return jsonify(result = "long string")

	#공백 제거
	del_space_str = search_str.split(' ')

	#토크나이저 시간 측정###########################################
	TOKENIZER_TIME_START = time.time()
	###########################################################
	#토크나이져 작업
	tokenizer_list = tknizer.get_tk(search_str)
	#토크나이저 측정 종료###########################################
	TOKENIZER_TIME_END = time.time() - TOKENIZER_TIME_START
	###########################################################

	#FT 유사 단어 추출 시간 측정#####################################
	FASTTEXT_TIME_START = time.time()
	###########################################################
	#FastText를 이용한 유사단어 추출
	ft_similarity_list = []
	for word in tokenizer_list:
		for sim_word in FastText.sim_words(word):
			if sim_word[1] >= SJ_FASTTEXT_SIM_PERCENT: 
				ft_similarity_list.append(sim_word[0])
			else: break	
	#FT 유사 단어 추출 시간 측정#####################################
	FASTTEXT_TIME_END = time.time() - FASTTEXT_TIME_START
	###########################################################


	#카테고리 불러오기!
	category_type = find_category_of_topic(g.db, category_name)

	#최종 검색 키워드 리스트
	final_search_keyword = list(set(ft_similarity_list + tokenizer_list + del_space_str))

	#find_search_of_category 시간 측정 (불러와서 리스트화 시킨 시간)####
	FIND_SEARCH_OF_CATEGORY_TIME_START = time.time()
	###########################################################
	#해당 카테고리에서 검색어와 관련된 포스트 불러오기!
	POST_LIST = find_search_of_category(g.db, final_search_keyword, category_type['info_num'], SJ_CS_LIMIT)
	POST_LIST = list(POST_LIST)

	#find_search_of_category 시간 측정 (불러와서 리스트화 시킨 시간)####
	FIND_SEARCH_OF_CATEGORY_TIME_END = time.time() - FIND_SEARCH_OF_CATEGORY_TIME_START
	###########################################################

	#현재 날짜 가져오기.
	now_date = datetime.now()

	#매치스코어 + 트랜드 반영/미반영 시간 측정##########################
	MATCH_TREND_TIME_START = time.time()
	###########################################################

	#트랜드 스코어 적용 판별########################################
	#트랜드 스코어 적용일 시
	if trendscore_discriminate(now_date):
		for POST in POST_LIST:
			#FAS 작업
			split_vector = FastText.get_doc_vector(del_space_str).tolist()
			FAS = FastText.vec_sim(split_vector, POST['ft_vector'])

			T1 = match_score(del_space_str, POST['title_token'])

			if tokenizer_list:
				T2 = match_score(tokenizer_list, set(POST['token']+POST['tag']))
			else:
				T2 =0

			if ft_similarity_list:
				T3 = match_score(ft_similarity_list, set(POST['token']+POST['tag']))
			else:
				T3 = 0

			#트랜드 스코어 적용!
			TREND = trendscore(POST)

			POST['similarity'] = round((T1 + T2 + T3 + FAS + TREND), 1)
			POST['_id'] = str(POST['_id'])

			#필요없는 반환 값 삭제
			del POST['title_token']
			del POST['token']
			del POST['tag']
			del POST['popularity']
	
	#트랜드 스코어 적용 안할 시
	else:
		for POST in POST_LIST:
			#FAS 작업
			split_vector = FastText.get_doc_vector(del_space_str).tolist()
			FAS = FastText.vec_sim(split_vector, POST['ft_vector'])

			T1 = match_score(del_space_str, POST['title_token'])

			if tokenizer_list:
				T2 = match_score(tokenizer_list, set(POST['token']+POST['tag']))
			else:
				T2 =0

			if ft_similarity_list:
				T3 = match_score(ft_similarity_list, set(POST['token']+POST['tag']))
			else:
				T3 = 0

			POST['similarity'] = round((T1 + T2 + T3 + FAS), 1)
			POST['_id'] = str(POST['_id'])

			#필요없는 반환 값 삭제
			del POST['title_token']
			del POST['token']
			del POST['tag']
			del POST['popularity']
	
	#매치스코어 + 트랜드 반영/미반영 시간 측정##########################
	MATCH_TREND_TIME_END = time.time() - MATCH_TREND_TIME_START
	###########################################################

	#구해진 similarity - date로 내림차순 정렬
	POST_LIST = sorted(POST_LIST, key=operator.itemgetter('date'), reverse=True)
	POST_LIST = sorted(POST_LIST, key=operator.itemgetter('similarity'), reverse=True)

	#총 시간 측정 종료#############################################
	TOTAL_TIME_END = time.time() - TOTAL_TIME_START
	###########################################################

	SPEED_RESULT = {}
	SPEED_RESULT['TOKENIZER_TIME'] = TOKENIZER_TIME_END
	SPEED_RESULT['FASTTEXT_TIME'] = FASTTEXT_TIME_END
	SPEED_RESULT['FIND_SEARCH_OF_CATEGORY_TIME'] = FIND_SEARCH_OF_CATEGORY_TIME_END
	SPEED_RESULT['MATCH_TREND_TIME'] = MATCH_TREND_TIME_END
	SPEED_RESULT['TOTAL_TIME'] = TOTAL_TIME_END
	SPEED_RESULT['PROCESSING_POSTS_NUM'] = len(POST_LIST)
	SPEED_RESULT['RETURN_NUM'] = num

	#데이터로 들어온 상위 num개만 반환
	return jsonify(
			result = "success",
			search_result = POST_LIST[:num],
			speed_result = SPEED_RESULT
		)

#domain (작동중)
@BP.route('/api/v1/search/domain', methods = ['POST'])
@jwt_optional
def SJ_api_v1_search__domain():
	#JAVA 스레드 이동.
	jpype.attachThreadToJVM()

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

#입력된 str을 fasttext로 유사한 단어를 추출 해주는 API (연관검색어) (보류)
@BP.route('/api/v1/search/similarity_words', methods = ['POST'])
def simulation_fastext():
	#JAVA 스레드 이동.
	jpype.attachThreadToJVM()

	input_str = request.form['search']

	tokenizer_list = tknizer.get_tk(input_str)
	
	result = {}
	for word in tokenizer_list:
		similarity_list = []
		for sim_word in FastText.sim_words(word):
			temp = {}
			if sim_word[1] >= SJ_FASTTEXT_SIM_PERCENT: 
				temp[sim_word[0]] = sim_word[1]
				similarity_list.append(temp)
			else: break	
		result[word] = similarity_list

	return jsonify(
		result = "success",
		similarity_words = result)

###############################################################################################
###############################################################################################

#트랜드 스코어 판별 함수
def trendscore_discriminate(now_date):
	year = now_date.year

	'''
	#Course Manual (수강편람 기간)
	CM_term_1 = (datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14))
	CM_term_2 = (datetime(year, 8, 1) < now_date) and (now_date < datetime(year, 8, 14))

	#Seasonal Semester (계절학기 기간)
	SS_term_1 = (datetime(year, 11, 25) < now_date) and (now_date < datetime(year, 12, 5))
	SS_term_2 = (datetime(year, 5, 25) < now_date) and (now_date < datetime(year, 6, 5))
	
	#트랜드 스코어 판별 반환
	if CM_term_1 or CM_term_2 or SS_term_1 or SS_term_2:
		return True

	else:
		return False
	'''

	return  ((datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14))) or ((datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14))) or ((datetime(year, 2, 1) < now_date) and (now_date < datetime(year, 2, 14)))

#트렌드 스코어 계산 함수
def trendscore(POST, now_date):

	#수강편람 trendscore
	if POST['info'] == 'main_student' and ('수강편람' in POST['tag']):
		return 10 

	#계절학기 trendscore
	elif POST['info'] == 'main_student' and ('계절학기' in POST['title_token']):
		return 4

	#아니면?!
	else: 
		return 0
