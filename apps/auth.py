from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from db_management import *
from sj_auth import *

BP = Blueprint('auth', __name__)

#######################################################
#페이지 URL#############################################

#######################################################
#로그인 및 회원가입(토큰발행) (OK)
@BP.route('/sign_in_up', methods=['POST'])
def sign_in_up():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']

	user = find_user(g.db, USER_ID)

	if user is None:
		result = refresh_sejong_portal(USER_ID, USER_PW)

	if result == "success":
		user = find_user(g.db, USER_ID)
	else:
		return jsonify(result = "not sejong")
	
	if check_password_hash(user['user_pw'], USER_PW):
		return jsonify(
			result = "success",
			access_token = create_access_token(
				identity = USER_ID,
				expires_delta=False)
			)
	
	result = refresh_sejong_portal(USER_ID, USER_PW)

	if result == "success":
		user = find_user(g.db, USER_ID)
	else:
		return jsonify(result = "not sejong")

	if check_password_hash(user['user_pw'], USER_PW):
		return jsonify(
			result = "success",
			access_token = create_access_token(
				identity = USER_ID,
				expires_delta=False)
			)
	else:
		return jsonify(result = "pw incorrect")
		
#회원정보 반환
@BP.route('/get_userinfo')
@jwt_required
def get_user_info():
	user = find_user(g.db, get_jwt_identity())

	if user is None: abort(400)

	return jsonify(
		result = "success",
		user_id = user['user_id'],
		user_name = user['user_name'],
		user_major = user['user_major']
		)

###############################################
###############################################
def refresh_sejong_portal(USER_ID, USER_PW):
	sejong_api_result = dosejong_api(USER_ID, USER_PW)
	if not sejong_api_result['result']:
		sejong_api_result = sjlms_api(USER_ID, USER_PW)
		if not sejong_api_result['result']:
			sejong_api_result = uis_api(USER_ID, USER_PW)
		
	if not sejong_api_result['result']:
		return "not sejong"
	else:
		insert_user(g.db,
			USER_ID,
			generate_password_hash(USER_PW),
			sejong_api_result['name'],
			sejong_api_result['major']
			)

	return "success"
