from flask import *
from flask_jwt_extended import *
from werkzeug import *
##########################################
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime
##########################################
from db_management import *
from global_func import *
##########################################
BP = Blueprint('post', __name__)
##########################################

#포스트 좋아요 (사용자가 관심기능 수행한 게시물 모듈 포함)
@BP.route('/post_like/<string:obi>')
@jwt_required
def post_like(obi):
	USER = find_user(g.db, _id=1, user_id=get_jwt_identity())
	if USER is None: abort(400)

	#중복 좋아요 체크.
	if 'fav_list' in check_user_fav_list(g.db, USER['_id'], obi):
		return jsonify(result = "already like")

	#해당 포스트 불러온다.
	POST = find_post(g.db, _id=obi, topic=1, token=1, tag=1, fav_cnt=1, view=1)

	#DB 해당 포스트 좋아요 (안에서 popularity 또한 갱신)
	update_post_like(g.db, POST)

	############################################

	#유저에 들어갈 좋아요 누른 post 인코딩
	fav_obj = {}
	fav_obj['_id'] = POST['_id'];
	fav_obj['topic'] = POST['topic']
	fav_obj['token'] = POST['token']
	fav_obj['tag'] = POST['tag']
	fav_obj['date'] = datetime.now()

	#유저 fav_list에 추가.
	result = update_user_fav_list_push(g.db, USER['_id'], fav_obj)

	return jsonify(result = result)

#포스트 좋아요 취소 (사용자가 관심기능 수행한 게시물 모듈 포함)
@BP.route('/post_unlike/<string:obi>')
@jwt_required
def post_unlike(obi):
	USER = find_user(g.db, _id=1, user_id=get_jwt_identity())
	if USER is None: abort(400)
	#해당 포스트 불러온다.
	POST = find_post(g.db, _id=obi, fav_cnt=1, view=1)
	#DB 해당 포스트 좋아요 취소(안에서 popularity 또한 갱신)
	update_post_unlike(g.db, POST)

	############################################

	#유저 fav_list에서 삭제.
	result = update_user_fav_list_pull(g.db, USER['_id'], POST['_id'])

	return jsonify(result = result)

#포스트 조회수
@BP.route('/post_view/<string:obi>')
@jwt_optional
def post_view(obi):
	POST = find_post(g.db, _id=obi, topic=1, token=1, tag=1, fav_cnt=1, view=1)

	result = update_post_view(g.db, POST)

	############################################

	if get_jwt_identity():
		USER = find_user(g.db, _id=1, user_id=get_jwt_identity())

		#유저에 들어갈 좋아요 누른 post 인코딩
		view_obj = {}
		view_obj['_id'] = POST['_id'];
		view_obj['topic'] = POST['topic']
		view_obj['token'] = POST['token']
		view_obj['tag'] = POST['tag']
		view_obj['date'] = datetime.now()

		#유저 view_list에 추가.
		result = update_user_view_list_push(g.db, USER['_id'], view_obj)

	return jsonify(result = result)

################################################
################################################


