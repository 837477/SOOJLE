from flask import *
from bson.json_util import dumps
from bson.objectid import ObjectId
from db_management import *
from global_func import *
from datetime import datetime

BP = Blueprint('newsfeed', __name__)

#포스트 좋아요
@BP.route('/post_like/<string:obi>')
def post_like(obi):
	result = post_like_up(g.db, obi)

	return jsonify(result = result)

#포스트 좋아요 취소
@BP.route('/post_unlike/<string:obi>')
def post_unlike(obi):
	result = post_unlike(g.db, obi)

	return jsonify(result = result)

#포스트 조회수
@BP.route('/post_view/<string:obi>')
def post_view(obi):
	result = post_view(g.db, obi)

	return jsonify(result = result)

#유저가 접근 게시물 등록
@BP.route('/post_user_access/<string:obi>')
def post_user_access(obi):
	access_obj = {}
	
	topic = find_post_topic(g.db, obi)
	tag = find_post_tag(g.db, obi)

	access_obj['_id'] = ObjectId(obi)
	access_obj['topic'] = topic
	access_obj['tag'] = tag

	update_post_user_access(g.db, user_id, access_obj)



################################################
################################################

