from flask import *
from pymongo import *
from db_management import *
from numpy import dot
from numpy.linalg import norm
import numpy

from global_func import *
from db_info import *

BP = Blueprint('similarity', __name__)

@BP.route('/test')
#각 사용자와 포스트의 유사도 체크후, DB개신
def similarity_run():
	#전체 유저를 _id, topic리스트, tag리스트 만 가져온다.
	USER_LIST = find_all_user(g.db, _id=1, topic=1, tag=1)
	#데이트 정렬된 포스트 중 상위 3000개만 _id, topic리스트, tag리스트, 조회수, 좋아요 만 가져온다.
	POST_LIST = find_all_posts(g.db, _id=1, topic=1, tag=1, view=1, fav_cnt=1, limit_=3000)

	USER_LIST = loads(USER_LIST)
	POST_LIST = loads(POST_LIST)

	#캐싱된 가장 높은 좋아요 수를 가져온다.
	MaxInterests = find_variable(g.db, 'highest_fav_cnt')
	#캐싱된 가장 높은 조회수를 가져온다.
	MaxViews = find_variable(g.db, 'highest_view')

	for USER in USER_LIST:
		#유저 테이블에 들어갈 유사도 결과 필드 리스트 생성
		sim_result = []
		for POST in POST_LIST:
			#해당 유저와, 각각의 포스트들의 유사도를 사전 형식으로 저장
			sim_dict = {}

			#TOS 작업
			TOS = dot(USER['topic'], POST['topic'])/(norm(USER['topic'])*norm(POST['topic']))

			#TAS 작업
			post_tag_len = len(POST['tag'])
			intersection_len = len(set(USER['tag']) & set(POST['tag']))
			TAS = intersection_len / post_tag_len

			#IS 작업
			IS = (((POST['fav_cnt']/MaxInterests)*0.5) + ((POST['view']/MaxViews)*0.5)) * 1

			RANDOM = rand_view = numpy.random.random()

			#TOS와 TAS와 IS의 결과를 result에 저장
			#except는 어떤 포스트의 노출도를 높히기위해 존재하기 때문에 모든 포스트에 적용시킬 필요는 없다. 추가 API를 생성할 예정.
			result = TOS * (1 + TAS) + IS + RANDOM

			#해당 포스트와, 계산된 sim의 결과를 사전으로 만듬.
			sim_dict['_id'] = POST['_id']
			sim_dict['similarity'] = result
			#유저의 sim 리스트목록에 추가.
			sim_result.append(sim_dict)

		update_user_post_similarity(g.db, USER['_id'], sim_result)

		
# #전에 쓰던 함수
# def similarity(user_id, post_id, except_ = 0):
# 	TOS = ToS(user_id, post_id)
# 	TAS = TaS(user_id, post_id)
# 	IS = Is(post_id, 0.5, 0.5, 1)

# 	return TOS * (1 + TAS) + IS

####################################################
####################################################
def ToS(user_id, post_id):
	user = find_user_topic(g.db, user_id)
	post = find_post_topic(g.db, post_id)

	return dot(user, post)/(norm(user)*norm(post))

def TaS(user_id, post_id):
	user = find_user_tag(g.db, user_id)
	post = find_post_tag(g.db, post_id)

	post_len = len(post)
	intersection = len(set(user) & set(post))

	return intersection / post_len

def Is(post_id, X1, X2, X3):
	MaxInterests = find_variable(g.db, 'highest_fav_cnt')
	MaxViews = find_variable(g.db, 'highest_view')

	Interests = find_post_fav_cnt(g.db, post_id)
	Views = find_post_view(g.db, post_id)

	return (((Interests/MaxInterests)*X1) + ((Views/MaxViews)*X2)) * X3
###################################################
###################################################