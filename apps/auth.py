from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
###########################################
from db_management import *
from sj_auth import *
###########################################
BP = Blueprint('auth', __name__)
###########################################

#######################################################
#페이지 URL#############################################

#######################################################
#로그인 및 회원가입(토큰발행) (OK)
@BP.route('/sign_in_up', methods=['POST'])
def sign_in_up():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']

	user = find_user(g.db, user_id=USER_ID)

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
	user = find_user(g.db, user_id=get_jwt_identity(), user_name=1, user_major = 1)

	if user is None:
		return jsonify("not found")

	return jsonify(
		result = "success",
		user_id = user['user_id'],
		user_name = user['user_name'],
		user_major = user['user_major']
		)

#회원정보 특정 필드 반환
@BP.route('/get_specific_userinfo/<int:type_num>')
@jwt_required
def get_specific_userinfo(type_num=None):
	USER = find_user(g.db, user_id=USER_ID)

	if USER is None:
		return jsonify(result = "user is not define")

	#1 = 좋아요 리스트
	#2 = 접근한 리스트
	#3 = 검색기록 리스트
	#4 = 접근한 뉴스피드 리스트
	#None = 전체
	if type_num == 1:
		USER = find_user(g.db, user_id=get_jwt_identity(), fav_list=1)
	elif type_num == 2:
		USER = find_user(g.db, user_id=get_jwt_identity(), view_list=1)
	elif type_num == 3:
		USER = find_user(g.db, user_id=get_jwt_identity(), search_list=1)
	elif type_num == 4:
		USER = find_user(g.db, user_id=get_jwt_identity(), newsfeed_list=1)
	else:
		USER = find_user(g.db, user_id=get_jwt_identity(), fav_list=1, view_list=1, search_list=1, newsfeed_list=1)

	return jsonify(
		result = 'success',
		USER = dumps(USER))
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
