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
		sejong_api_result = dosejong_api(USER_ID, USER_PW)
		if not sejong_api_result['result']:
			sejong_api_result = sjlms_api(USER_ID, USER_PW)
		
		if not sejong_api_result['result']:
			return jsonify(result = "not_sejong")
		else:
			insert_user(g.db,
				USER_ID,
				generate_password_hash(USER_PW),
				sejong_api_result['name'],
				sejong_api_result['major']
				)

	user = find_user(g.db, USER_ID)
	
	if check_password_hash(user['user_pw'], USER_PW):
		return jsonify(
			result = "success",
			access_token = create_access_token(
				identity = USER_ID,
				expires_delta=False)
			)
	else:
		return jsonify(result = "incorrect_password")

#회원정보 반환
@BP.route('/get_user_info')
@jwt_required
def get_user_info():
	user = select_user(g.db, 'get_jwt_identity()')

	if user is None: abort(400)

	return jsonify(
		result = "success",
		user_id = user['user_id'],
		user_name = user['user_name'],
		user_major = user['user_major']
		)
