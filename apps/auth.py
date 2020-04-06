from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from pprint import pprint
###########################################
from db_management import *
###########################################
from variable import *

#/api/v1/analysis/lastdays/<int:days>
#SJ_api_v1_analysis_lastdays(days):

#BluePrint
BP = Blueprint('auth', __name__)

#회원가입 (작동중)
@BP.route('/api/v1/auth/sign_up', methods = ['POST'])
def SJ_api_v1_auth__sign_up():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']
	USER_PW_CHECK = request.form['pw_check']
	USER_NICKNAME = request.form['nickname']

	USER = find_user(g.db, user_id=USER_ID)

	#해당 ID의 유저가 이미 있으면?!
	if USER:
		return jsonify(result = "Exist")

	#비밀번호 확인 검증 실패!, Bad request 핸들러 반환
	if USER_PW != USER_PW_CHECK: abort(400)

	#길이 검증 실패!, Bad request 핸들러 반환
	if (len(USER_ID) < SJ_REQUEST_LENGTH_LIMIT['user_id_min'] and len(USER_ID) > SJ_REQUEST_LENGTH_LIMIT['user_id_max']) or (len(USER_NICKNAME) < SJ_REQUEST_LENGTH_LIMIT['user_nickname_min'] and len(USER_NICKNAME) > SJ_REQUEST_LENGTH_LIMIT['user_nickname_max']) or len(USER_PW) < SJ_REQUEST_LENGTH_LIMIT['user_pw_max']: abort(400)

	#SOOJLE DB에 추가.
	insert_user(g.db,
		USER_ID,
		generate_password_hash(USER_PW),
		USER_NICKNAME
	)

	#유저 재조회!
	USER = find_user(g.db, user_id=USER_ID, user_pw=1)
	
	#DB에서 성공적으로 조회되면, 회원가입 성공!
	if USER:
		return jsonify(
			result = "success",
			access_token = create_access_token(
				identity = USER_ID,
				expires_delta=False)
		)
	#실패!, Fail 핸들러 반환
	else: abort(500)

#로그인 (작동중)
@BP.route('/api/v1/auth/sign_in', methods = ['POST'])
def SJ_api_v1_auth__sign_in():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']

	USER = find_user(g.db, user_id=USER_ID, user_pw=1)

	#해당 유저가 존재하지 않는다!
	if USER is None:
		return jsonify (result = "Not found")
	
	#비밀번호 해시화 확인.
	if check_password_hash(USER['user_pw'], USER_PW):
		return jsonify(
			result = "success",
			access_token = create_access_token(
				identity = USER_ID,
				expires_delta=False)
			)
	else:
		return jsonify(result = "Incorrect pw")

#닉네임 변경 (작동중)
@BP.route('/api/v1/auth/change_nickname', methods = ['POST'])
@jwt_required
def SJ_api_v1_auth__change_nickname():
	NEW_NICKNAME = request.form['new_nickname']

	USER = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 토큰으로 유저 조회 불가!, Bad token 핸들러 반환
	if USER is None: abort(401)

	#길이 검증 실패!, Bad request 핸들러 반환
	if len(NEW_NICKNAME) < SJ_REQUEST_LENGTH_LIMIT['user_nickname_min'] and len(NEW_NICKNAME) > SJ_REQUEST_LENGTH_LIMIT['user_nickname_max']: abort(400)

	result = update_nickname(g.db, USER['user_id'], NEW_NICKNAME)

	return jsonify(
		result = result
	)

#회원정보 반환 (작동중)
@BP.route('/api/v1/auth/get_userinfo')
@jwt_required
def SJ_api_v1_auth__get_userinfo():
	USER = find_user(g.db, user_id=get_jwt_identity(), auto_login=1, user_nickname=1, fav_list=1, privacy=1)

	#잘못된 토큰으로 유저 조회 불가!, Bad token 핸들러 반환
	if USER is None: abort(401)

	#반환 할 return_object 객체
	return_object = {}
	return_object['result'] = "success"
	return_object['user_id'] = USER['user_id']
	return_object['user_nickname'] = USER['user_nickname']
	return_object['user_fav_list'] = USER['fav_list']
	return_object['auto_login'] = USER['auto_login']
	return_object['auto_login'] = USER['auto_login']
	return_object['privacy'] = USER['privacy']

	#들어온 토큰이 ADMIN 토큰인지 확인!
	if USER['user_id'] == SJ_ADMIN:
		return_object['admin'] = 1
	else:
		return_object['admin'] = 0

	return jsonify(
		return_object
	)

#자동로그인 유무 변경 (작동중)
@BP.route('/api/v1/auth/change_autologin/<int:auto_login>')
@jwt_required
def SJ_api_v1_auth__change_autologin(auto_login):
	USER = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 토큰으로 유저 조회 불가!, Bad token 핸들러 반환
	if USER is None: abort(401)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path)

	#잘못된 요청을 보냈음!, Bad request 핸들러 반환
	if auto_login > 1 and auto_login < 0: abort(400)

	result = update_user_auto_login(g.db, USER['user_id'], auto_login)

	return jsonify(
		result = result
	)

#개인정보처리방침 동의현황 변경 (보류)
@BP.route('/update_privacy/<int:privacy>')
@jwt_required
def update_privacy(privacy):
	USER = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 토큰으로 유저 조회 불가!, Bad token 핸들러 반환
	if USER is None: abort(401)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path)

	#잘못된 요청을 보냈음!, Bad request 핸들러 반환
	if auto_login > 1 and auto_login < 0: abort(400)

	result = update_user_privacy(g.db, USER['user_id'], privacy)

	return jsonify(
		result = result
	)

#회원정보 특정 필드 반환 (작동중)
@BP.route('/api/v1/auth/get_specific_userinfo/<int:type_num>')
@jwt_required
def SJ_api_v1_auth__get_specific_userinfo(type_num=None):
	USER = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 토큰으로 유저 조회 불가!, Bad token 핸들러 반환
	if USER is None: abort(401)

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
		user = dumps(USER)
	)

#회원탈퇴 (작동중)
@BP.route('/api/v1/auth/delete_user')
@jwt_required
def SJ_api_v1_auth__delete_user():
	USER = find_user(g.db, _id=1, user_id=get_jwt_identity())

	#잘못된 토큰으로 유저 조회 불가!, Bad token 핸들러 반환
	if USER is None: abort(401)

	#회원 삭제!
	result = remove_user(g.db, USER['user_id'])

	return jsonify(result = result)
	
#회원 관심도 초기화 (작동중)
@BP.route('/api/v1/auth/reset_measurement')
@jwt_required
def SJ_api_v1_auth__reset_measurement():
	USER = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 토큰으로 유저 조회 불가!, Bad token 핸들러 반환
	if USER is None: abort(401)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path)

	#회원 관심도 초기화!
	result = update_user_measurement_reset(g.db, USER['user_id'])

	return jsonify(
		result = result
	)

#회원 최근 검색어 반환 (작동중)
@BP.route('/api/v1/auth/get_lately_search/<int:num>')
@jwt_required
def SJ_api_v1_auth__get_lately_search(num):
	USER = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 토큰으로 유저 조회 불가!, Bad token 핸들러 반환
	if USER is None: abort(401)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path)

	result = find_user_lately_search(g.db, USER['user_id'], num)

	return jsonify(
		result = "success",
		lately_search_list = result
	)