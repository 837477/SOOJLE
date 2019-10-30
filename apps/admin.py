from flask import *
from flask_jwt_extended import *
from werkzeug import *
##########################################
from bson.json_util import dumps
from bson.objectid import ObjectId
##########################################
from db_management import *
from global_func import *
import jpype
from tknizer import get_tk
##########################################
BP = Blueprint('admin', __name__)
##########################################
#전체 유저 반환
@BP.route('/get_userlist')
@jwt_required
def get_userlist():
	USER = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	if USER is None: abort(400)

	if USER['user_major'] != 'admin':
		return jsonify(result = "you are not admin")

	USER_ALL = find_all_user(g.db, _id=1, user_id=1, user_name=1, user_major=1)

	return jsonify(
		result = "success",
		users = USER_ALL)

#특정 유저 관심도 초기화
@BP.route('/reset_interest/<string:obi>')
@jwt_required
def reset_interest(obi):
	USER = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	if USER is None: abort(400)

	if USER['user_major'] != 'admin':
		return jsonify(result = "you are not admin")

	result = update_unset_user_interest(g.db, obi)

	return jsonify(result = result)


#특정 포스트 삭제
@BP.route('/delete_post/<string:obi>')
@jwt_required
def delete_post(obi):
	USER = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	if USER is None: abort(400)

	if USER['user_major'] != 'admin':
		return jsonify(result = "you are not admin")

	

