from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from pprint import pprint
###########################################
from db_management import *
from sj_auth import *
###########################################
from variable import *


#BluePrint
BP = Blueprint('auth', __name__)


#로그인 및 회원가입(토큰발행) (OK)
@BP.route('/sign_in_up', methods=['POST'])
def sign_in_up():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']

	user = find_user(g.db, user_id=USER_ID, user_pw=1)

	#SOOJLE DB에 해당 user가 없다면?
	if user is None:
		user = {}
		try:
			sejong_api_result = dosejong_api(USER_ID, USER_PW)
		except:
			return jsonify(result = "api error")
		if not sejong_api_result['result']:
			try:
				sejong_api_result = sjlms_api(USER_ID, USER_PW)
			except:
				return jsonify(result = "api error")
			if not sejong_api_result['result']:
				try:
					sejong_api_result = uis_api(USER_ID, USER_PW)
				except:
					return jsonify(result = "api error")

		#3개의 세종 API 불통시에 반환.
		if not sejong_api_result['result']:
			return jsonify(result = "not sejong")

		#SOOJLE DB에 추가.
		insert_user(g.db,
			USER_ID,
			generate_password_hash(USER_PW),
			sejong_api_result['name'],
			sejong_api_result['major']
			)

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
	user = find_user(g.db, user_id=get_jwt_identity(), auto_login=1, user_name=1, user_major=1, fav_list=1)

	if user is None: abort(400)

	return jsonify(
		result = "success",
		user_id = user['user_id'],
		user_name = user['user_name'],
		user_major = user['user_major'],
		user_fav_list = user['fav_list'],
		auto_login = user['auto_login']
		)

#자동로그인 유무 변경
@BP.route('/update_auto_login/<int:auto_login>')
@jwt_required
def update_auto_login(auto_login):
	USER = find_user(g.db, user_id=get_jwt_identity())

	if USER is None: abort(400)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path, student_num = True)

	if auto_login > 1 and auto_login < 0: abort(400)

	result = update_user_auto_login(g.db, USER['user_id'], auto_login)

	return jsonify(
		result = result
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
	else:
		USER = find_user(g.db, user_id=get_jwt_identity(), newsfeed_list=1)

	return jsonify(
		result = "success",
		user = dumps(USER))

#회원탈퇴
@BP.route('/remove_mine')
@jwt_required
def remove_mine():
	#삭제 대상 획원 유무 확인
	USER = find_user(g.db, _id=1, user_id=get_jwt_identity())

	if USER is None:
		return jsonify(result = "Not found")

	#회원 삭제!
	result = remove_user(g.db, USER['user_id'])

	return jsonify(result = result)

#회원 관심도 초기화
@BP.route('/reset_user_measurement')
@jwt_required
def reset_user_measurement(user_id):
	USER = find_user(g.db, _id=1, user_id=get_jwt_identity())

	if USER is None: abort(400)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path, student_num = True)

	#회원 삭제!
	result = reset_user_measurement(g.db, USER['user_id'])

	return jsonify(result = result)