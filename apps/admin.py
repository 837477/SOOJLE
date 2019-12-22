from flask import *
from flask_jwt_extended import *
from werkzeug import *
from bson.json_util import dumps
from bson.objectid import ObjectId
import jpype
##########################################
from db_management import *
from global_func import *
from tknizer import get_tk
##########################################
from variable import *


#BluePrint
BP = Blueprint('admin', __name__)


#회원 삭제
@BP.route('/remove_user/<string:user_id>')
@jwt_required
def remove_user(user_id):
	admin = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	#Admin 확인
	if admin is None or admin['major'] != SJ_ADMIN:
		return jsonify(result = "Not admin")

	#삭제 대상 획원 유무 확인
	target_user = find_user(g.db, _id=1, user_id=user_id)

	if target_user is None:
		return jsonify(result = "Not found")

	#회원 삭제!
	result = remove_user(g.db, user_id)

	return jsonify(result = result)

#게시글 삭제
@BP.route('/remove_post/<string:post_obi>')
@jwt_required
def remove_post(post_obi):
	admin = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	#Admin 확인
	if admin is None or admin['major'] != SJ_ADMIN:
		return jsonify(result = "Not admin")

	target_post = find_post(g.db, post_obi=post_obi)

	if target_post is None:
		return jsonify(result = "Not found")

	#post 삭제!
	result = remove_post(g.db, post_obi)

	return jsonify(result = result)


#게시글 수정 (보류)
@BP.route('/update_post', methods=['POST'])
@jwt_required
def update_post():
	new_title = request.form['title']
	new_post = request.form['post']
	

#게시글 입력 (보류)


#admin 생성
# @BP.route('/create_admin')
# def create_admin():
# 	USER_ID = ""
# 	USER_PW = ""

# 	#SOOJLE DB에 추가.
# 	insert_user(g.db,
# 		USER_ID,
# 		generate_password_hash(USER_PW),
# 		"SOOJLE",
# 		"SJ_SUPER_ADMIN_837477_IML_NB"
# 	)

# 	return jsonify(
# 		result = "success",
# 		access_token = create_access_token(
# 			identity = USER_ID,
# 			expires_delta=False)
# 	)
	