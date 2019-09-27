from flask import *
from db_management import *
from numpy import dot
from numpy.linalg import norm
import numpy

from db_info import *

BP = Blueprint('similarity', __name__)

def similarity_run():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client['soojle']

	USER_LIST = find_all_user(db)
	POST_LIST = find_all_posts(db)

	for USER in USER_LIST:
		result = []
		for POST in POST_LIST:
			sim_dict = {}

			sim = similarity(USER['_id'], POST['_id'])
			sim_dict.update(
				post_id = POST['_id'],
				similarity = sim
				)

			result.append(sim_dict)
		update_user_post_similarity(db, USER['_id'], result)
		print(USER['_id'], ' :', result)

	db_client.close()

def similarity(user_id, post_id, except_ = 0):
	TOS = ToS(user_id, post_id)
	TAS = TaS(user_id, post_id)
	IS = Is(post_id, 0.5, 0.5, 1)
	random = rand_view = numpy.random.rand(0, 1)

	return TOS * (1 + TAS) + IS + random + except_

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
	#현재 조회수가 가장 높은 게시글은 2050 이다.
	#현재 좋아요가 가장 높은 게실은 510 이다.

	#나중에 캐싱한 값을 DB에서 호출해서 사용해야함.
	MaxInterests = 510
	MaxViews = 2050

	Interests = find_post_fav_cnt(g.db, post_id)
	Views = find_post_view(g.db, post_id)

	return (((Interests/MaxInterests)*X1) + ((Views/MaxViews)*X2)) * X3
###################################################
###################################################