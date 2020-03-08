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

#회원가입
@BP.route('/sign_up', methods = ['POST'])
def sign_up():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']
	USER_PW_CHECK = request.form['pw_check']
	USER_NICKNAME = request.form['nickname']

	#해당 ID의 유저가 있는지 확인!
	user = find_user(g.db, user_id=USER_ID)

	#해당 ID의 유저가 있으면, 이미 있는 아이디로 반환.
	if user:
		return jsonify(
			result = "already id"
		)

	if (len(USER_ID) < 6 and len(USER_ID) > 30) or (len(USER_NICKNAME) < 1 and len(USER_NICKNAME) > 16) or len(USER_PW) < 8:
		return jsonify(
			result = "wrong user info"
		)

	if USER_PW != USER_PW_CHECK:
		return jsonify(
			result = "check pw"
		)

	#SOOJLE DB에 추가.
	insert_user(g.db,
		USER_ID,
		generate_password_hash(USER_PW),
		USER_NICKNAME
	)

	#유저 재조회!
	user = find_user(g.db, user_id=USER_ID, user_pw=1)
	
	#DB에서 성공적으로 조회되면, 회원가입 성공!
	if user:
		return jsonify(
			result = "success",
			access_token = create_access_token(
				identity = USER_ID,
				expires_delta=False)
		)
	#실패시, 실패 반환.
	else:
		return jsonify(
			result = "sign_up fail"
		)

#로그인
@BP.route('/sign_in', methods = ['POST'])
def sign_in():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']

	user = find_user(g.db, user_id=USER_ID, user_pw=1)

	#해당 유저가 존재하지 않으면?!
	if user is None:
		return jsonify(
			result = "No member"
		)
	
	#비밀번호 해시화 확인.
	if check_password_hash(user['user_pw'], USER_PW):
		return jsonify(
			result = "success",
			access_token = create_access_token(
				identity = USER_ID,
				expires_delta=False)
			)
	else:
		return jsonify(result = "incorrect pw")

#닉네임 변경
@BP.route('/change_nickname', methods = ['POST'])
@jwt_required
def change_nickname():
	NEW_NICKNAME = request.form['new_nickname']

	user = find_user(g.db, user_id=get_jwt_identity())

	#해당 유저가 존재하지 않으면?!
	if user is None:
		return jsonify(
			result = "No member"
		)

	#닉네임 길이 체크
	if len(NEW_NICKNAME) < 1 and len(NEW_NICKNAME) > 16:
		return jsonify(
			result = "rewrite_nickname"
		)
		
	result = update_nickname(g.db, user['user_id'], NEW_NICKNAME)

	return jsonify(
		result = result
	)

#회원정보 반환
@BP.route('/get_userinfo')
@jwt_required
def get_user_info():
	user = find_user(g.db, user_id=get_jwt_identity(), auto_login=1, user_nickname=1, fav_list=1, privacy=1)

	if user is None: abort(401)

	return jsonify(
		result = "success",
		user_id = user['user_id'],
		user_nickname = user['user_nickname'],
		user_fav_list = user['fav_list'],
		auto_login = user['auto_login'],
		privacy = user['privacy']
		)

#자동로그인 유무 변경
@BP.route('/update_auto_login/<int:auto_login>')
@jwt_required
def update_auto_login(auto_login):
	USER = find_user(g.db, user_id=get_jwt_identity())

	if USER is None: abort(400)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path)

	if auto_login > 1 and auto_login < 0: abort(400)

	result = update_user_auto_login(g.db, USER['user_id'], auto_login)

	return jsonify(
		result = result
	)

#개인정보처리방침 동의현황 변경
@BP.route('/update_privacy/<int:privacy>')
@jwt_required
def update_privacy(privacy):
	USER = find_user(g.db, user_id=get_jwt_identity())

	if USER is None: abort(400)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path)

	if auto_login > 1 and auto_login < 0: abort(400)

	result = update_user_privacy(g.db, USER['user_id'], privacy)

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
def reset_user_measurement():
	USER = find_user(g.db, user_id=get_jwt_identity())

	if USER is None: abort(401)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path)

	#회원 삭제!
	result = update_user_measurement_reset(g.db, USER['user_id'])

	return jsonify(
		result = result
	)

#회원 최근 검색어 반환
@BP.route('/get_user_lately_search/<int:num>')
@jwt_required
def get_user_lately_search(num):
	USER = find_user(g.db, user_id=get_jwt_identity())

	if USER is None: abort(401)

	#메인로그 기록!
	insert_log(g.db, USER['user_id'], request.path)

	result = find_user_lately_search(g.db, USER['user_id'], num)

	return jsonify(
		result = "success",
		lately_search_list = result
	)

