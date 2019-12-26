from flask import *
from flask_jwt_extended import *
from werkzeug import *
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime
##########################################
from db_management import *
from global_func import *
##########################################
from variable import *


#BluePrint
BP = Blueprint('post', __name__)


#포스트 좋아요 (사용자가 관심기능 수행한 게시물 모듈 포함)
@BP.route('/post_like/<string:post_obi>')
@jwt_required
def post_like(post_obi):	
	
	#USER 정보 불러오기
	USER = find_user(g.db, _id=1, user_id=get_jwt_identity())
	
	#잘못된 USER 정보(잘못된 token)
	if USER is None: abort(400)

	#logging
	insert_log(g.db, get_jwt_identity(), request.url)

	#이미 좋아요 한 글인지 확인용으로 불러온다.
	check_fav = check_user_fav_list(g.db, USER['_id'], post_obi)
	#좋아요 중복 확인
	if 'fav_list' in check_fav:
		return jsonify(result = "already like")

	#해당 POST를 불러온다.
	POST = find_post(g.db, post_obi, _id=1, topic=1, token=1, tag=1, fav_cnt=1, view=1, date=1, title=1, url=1, img=1)

	#해당 POST가 없으면?!
	if POST is None:
		return jsonify(result = "post is deleted")

	#해당 POST 좋아요 처리.
	update_post_like(g.db, POST['_id'])

	#USER의 fav_list에 들어갈 Object
	fav_obj = {}
	fav_obj['_id'] = str(POST['_id'])
	fav_obj['topic'] = POST['topic']
	fav_obj['token'] = POST['token']
	fav_obj['tag'] = POST['tag']
	fav_obj['post_date'] = POST['date']
	fav_obj['title'] = POST['title']
	fav_obj['url'] = POST['url']
	fav_obj['img'] = POST['img']
	fav_obj['date'] = datetime.now()

	#USER의 fav_list에 추가.
	result = update_user_fav_list_push(g.db, USER['_id'], fav_obj)
	#해당 유저의 갱신시간 갱신
	update_user_renewal(g.db, USER['user_id'])

	return jsonify(result = result)

#포스트 좋아요 취소 (사용자가 관심기능 수행한 게시물 모듈 포함)
@BP.route('/post_unlike/<string:post_obi>')
@jwt_required
def post_unlike(post_obi):
	#USER 정보 불러오기
	USER = find_user(g.db, _id=1, user_id=get_jwt_identity())

	#잘못된 USER 정보(잘못된 token)
	if USER is None: abort(400)

	#logging!
	insert_log(g.db, get_jwt_identity(), request.url)

	#이미 좋아요 한 글인지 확인용으로 불러온다.
	check_fav = check_user_fav_list(g.db, USER['_id'], post_obi)
	#좋아요를 한 글인지 확인한다.
	if not 'fav_list' in check_fav:
		return jsonify(result = "none like")

	#해당 POST를 불러온다.
	POST = find_post(g.db, post_obi, _id=1)
	#해당 POST가 없으면?!
	if POST is None:
		return jsonify(result = "post is deleted")

	#해당 POST 좋아요 취소 처리.
	update_post_unlike(g.db, post_obi)

	#USER의 fav_list에서 삭제.
	result = update_user_fav_list_pull(g.db, USER['_id'], post_obi)
	#해당 유저의 갱신시간 갱신
	update_user_renewal(g.db, USER['user_id'])

	return jsonify(result = result)

#포스트 조회수
@BP.route('/post_view/<string:post_obi>')
@jwt_optional
def post_view(post_obi):
	POST = find_post(g.db, post_obi, _id=1, topic=1, token=1, tag=1, fav_cnt=1, view=1, date=1, title=1, url=1, img=1)

	result = update_post_view(g.db, post_obi)

	if get_jwt_identity():
		USER = find_user(g.db, _id=1, user_id=get_jwt_identity())

		#유저에 들어갈 좋아요 누른 post 인코딩
		view_obj = {}
		view_obj['_id'] = str(POST['_id'])
		view_obj['topic'] = POST['topic']
		view_obj['token'] = POST['token']
		view_obj['tag'] = POST['tag']
		view_obj['post_date'] = POST['date']
		view_obj['title'] = POST['title']
		view_obj['url'] = POST['url']
		view_obj['img'] = POST['img']
		view_obj['date'] = datetime.now()

		#유저 view_list에 추가.
		result = update_user_view_list_push(g.db, USER['_id'], view_obj)
		#해당 유저의 갱신시간 갱신
		update_user_renewal(g.db, USER['user_id'])

	return jsonify(result = result)


