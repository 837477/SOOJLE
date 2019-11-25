from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
import operator
###########################################
from db_management import *
from sj_auth import *
from pprint import pprint
###########################################
BP = Blueprint('auth', __name__)
###########################################

###########################################
#로그인 및 회원가입(토큰발행) (OK)
@BP.route('/sign_in_up', methods=['POST'])
def sign_in_up():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']

	user = find_user(g.db, user_id=USER_ID, user_pw=1)

	if user is None:
		result = refresh_sejong_portal(USER_ID, USER_PW)
	else:
		result = "success"

	#위 refresh_sejong_portal()을 통과 못했다면 3개의 로그인 api를 통과하지 못한 것. (통과했다면 result 값이 success임)
	if result == "not sejong":
		return jsonify(result = "not sejong")
	
	#세종대학교 내부 전산 오류
	elif result == "api error":
		return jsonify(result = "api error")
	
	user = find_user(g.db, user_id=USER_ID, user_pw=1)

	if check_password_hash(user['user_pw'], USER_PW):
		return jsonify(
			result = "success",
			access_token = create_access_token(
				identity = USER_ID,
				expires_delta=False)
			)
	else:
		return jsonify(result = "incorrect pw")
		
#회원정보 반환
@BP.route('/get_userinfo')
@jwt_required
def get_user_info():
	user = find_user(g.db, user_id=get_jwt_identity(), user_name=1, user_major=1, fav_list=1)

	if user is None:
		return jsonify("not found")

	return jsonify(
		result = "success",
		user_id = user['user_id'],
		user_name = user['user_name'],
		user_major = user['user_major'],
		user_fav_list = user['fav_list']
		)

#회원정보 특정 필드 반환
@BP.route('/get_specific_userinfo/<int:type_num>')
@jwt_required
def get_specific_userinfo(type_num=None):
	USER = find_user(g.db, user_id=get_jwt_identity())

	if USER is None: abort(400)

	if type_num == 0:
		USER = find_user(g.db, user_id=get_jwt_identity(), fav_list=1, view_list=1, search_list=1)
	elif type_num == 1:
		USER = find_user(g.db, user_id=get_jwt_identity(), fav_list=1)
	elif type_num == 2:
		USER = find_user(g.db, user_id=get_jwt_identity(), view_list=1)
	elif type_num == 3:
		USER = find_user(g.db, user_id=get_jwt_identity(), search_list=1)

	return jsonify(
		result = "success",
		user = dumps(USER))

###############################################
###############################################
def refresh_sejong_portal(USER_ID, USER_PW):
	try:
		sejong_api_result = dosejong_api(USER_ID, USER_PW)
	except:
		return "api error"
	if not sejong_api_result['result']:
		try:
			sejong_api_result = sjlms_api(USER_ID, USER_PW)
		except:
			return "api error"
		if not sejong_api_result['result']:
			try:
				sejong_api_result = uis_api(USER_ID, USER_PW)
			except:
				return "api error"

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
