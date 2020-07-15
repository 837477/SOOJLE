from flask import *
from flask_jwt_extended import *
from werkzeug import *
from bson.json_util import dumps
from bson.objectid import ObjectId
import jpype
import hashlib
##########################################
from db_management import *
from global_func import *
from tknizer import get_tk
import LDA
##########################################
from variable import *


#BluePrint
BP = Blueprint('admin', __name__)

#md5 해쉬
enc = hashlib.md5()

#회원 삭제 (보류)
@BP.route('/admin_remove_user/<string:user_id>')
@jwt_required
def admin_remove_user(user_id):
	admin = find_user(g.db, user_id=get_jwt_identity())

	#Admin 확인
	if admin is None or admin['user_id'] != SJ_ADMIN: abort(403)

	#삭제 대상 획원 유무 확인
	target_user = find_user(g.db, _id=1, user_id=user_id)

	if target_user is None:
		return jsonify(result = "Not found")

	#회원 삭제!
	result = remove_user(g.db, user_id)

	return jsonify(result = result)

#공지사항 전체 반환 (작동중)
@BP.route('/api/v1/admin/notice/all')
def SJ_api_v1_admin_notice__all():
	result = find_all_notice(g.db)
	result = dumps(result)

	return jsonify(
		result = "success",
		notice_list = result
	)

#공지사항 단일 반환 (작동중)
@BP.route('/api/v1/admin/notice/one/<string:notice_obi>')
def SJ_api_v1_admin_notice__one(notice_obi):
	#조회수 증가!
	update_notice_view(g.db, notice_obi)
	
	result = find_notice(g.db, notice_obi)

	#잘못된 요청을 보냈음!, Bad request 핸들러 반환
	if result is None: abort(400)

	result = dumps(result)
	
	return jsonify(
		result = "success",
		notice = result
	)

#공지사항 입력 (작동중)
@BP.route('/api/v1/admin/notice/insert', methods=['POST'])
@jwt_required
def SJ_api_v1_admin_notice__insert():
	NEW_TITLE = request.form['title']
	NEW_POST = request.form['post']

	ADMIN = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 ADMIN 토큰!, Admin only 핸들러 반환
	if ADMIN is None or ADMIN['user_id'] != SJ_ADMIN: abort(403)
	
	#길이 검증 실패!, Bad request 핸들러 반환
	if (len(NEW_TITLE) < SJ_REQUEST_LENGTH_LIMIT['notice_title_min'] and len(NEW_TITLE) > SJ_REQUEST_LENGTH_LIMIT['notice_title_max']) or (len(NEW_TITLE) < SJ_REQUEST_LENGTH_LIMIT['notice_post_min'] and len(NEW_TITLE) > SJ_REQUEST_LENGTH_LIMIT['notice_post_max']): abort(400)


	result = insert_notice(g.db, NEW_TITLE, NEW_POST)

	return jsonify(
		result = result
	)

#공지사항 수정 (작동중)
@BP.route('/api/v1/admin/notice/update/<string:notice_obi>', methods=['POST'])
@jwt_required
def SJ_api_v1_admin_notice__update(notice_obi):
	NEW_TITLE = request.form['title']
	NEW_POST = request.form['post']
	NEW_ACTIVATION = request.form['activation']
	
	ADMIN = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 ADMIN 토큰!, Admin only 핸들러 반환
	if ADMIN is None or ADMIN['user_id'] != SJ_ADMIN: abort(403)

	#길이 검증 실패!, Bad request 핸들러 반환
	if (len(NEW_TITLE) < SJ_REQUEST_LENGTH_LIMIT['notice_title_min'] and len(NEW_TITLE) > SJ_REQUEST_LENGTH_LIMIT['notice_title_max']) or (len(NEW_POST) < SJ_REQUEST_LENGTH_LIMIT['notice_post_min'] and len(NEW_POST) > SJ_REQUEST_LENGTH_LIMIT['notice_post_max']): abort(400)

	result = update_notice(g.db, notice_obi, NEW_TITLE, NEW_POST, int(NEW_ACTIVATION))

	return jsonify(
		result = result
	)

#공지사항 삭제 (작동중)
@BP.route('/api/v1/admin/notice/remove/<string:notice_obi>')
@jwt_required
def SJ_api_v1_admin_notice__remove(notice_obi):
	ADMIN = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 ADMIN 토큰!, Admin only 핸들러 반환
	if ADMIN is None or ADMIN['user_id'] != SJ_ADMIN: abort(403)

	NOTICE = find_notice(g.db, notice_obi)

	#해당 공지사항이 없는경우, Bad request 핸들러 반환
	if NOTICE is None: abort(400)

	result = remove_notice(g.db, notice_obi)

	return jsonify(
		result = result
	)

#피드백 전송 (작동중)
@BP.route('/api/v1/admin/feedback/send', methods=['POST'])
@jwt_required
def SJ_api_v1_admin_feedback__send():
	USER = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 토큰으로 유저 조회 불가!, Bad token 핸들러 반환
	if USER is None: abort(401)

	FEEDBACK_TYPE = request.form['type']
	FEEDBACK_POST = request.form['post']
	FEEDBACK_DATE = datetime.now()
	FEEDBACK_AUTHOR = USER['user_id']
	FEEDBACK_ACTIVATION = 1

	#길이 검증 실패!, Bad request 핸들러 반환
	if len(FEEDBACK_POST) > SJ_REQUEST_LENGTH_LIMIT['feedback_max']: abort(400)

	result = insert_user_feedback(g.db, FEEDBACK_TYPE, FEEDBACK_POST, FEEDBACK_DATE, FEEDBACK_AUTHOR, FEEDBACK_ACTIVATION)

	return jsonify(
		result = result
	)

#피드백 전체 반환 (작동중)
@BP.route('/api/v1/admin/feedback/all')
@jwt_required
def SJ_api_v1_admin_feedback__all():
	ADMIN = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 ADMIN 토큰!, Admin only 핸들러 반환
	if ADMIN is None or ADMIN['user_id'] != SJ_ADMIN: abort(403)

	result = find_all_feedback(g.db)
	result = dumps(result)

	return jsonify(
		result = "success",
		feedback_list = result
	)

#피드백 단일 반환 (작동중)
@BP.route('/api/v1/admin/feedback/one/<string:feedback_obi>')
@jwt_required
def SJ_api_v1_admin_feedback__one(feedback_obi):
	ADMIN = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 ADMIN 토큰!, Admin only 핸들러 반환
	if ADMIN is None or ADMIN['user_id'] != SJ_ADMIN: abort(403)
	
	result = find_feedback(g.db, feedback_obi)

	#잘못된 요청을 보냈음!, Bad request 핸들러 반환
	if result is None: abort(400)

	result = dumps(result)
	
	return jsonify(
		result = "success",
		feedback = result
	)

#피드백 활성화 변경 (작동중)
@BP.route('/api/v1/admin/feedback/activation/<string:feedback_obi>/<int:activation>')
@jwt_required
def SJ_api_v1_admin_feedback__activation(feedback_obi, activation):
	ADMIN = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 ADMIN 토큰!, Admin only 핸들러 반환
	if ADMIN is None or ADMIN['user_id'] != SJ_ADMIN: abort(403)
	
	check_feedback = find_feedback(g.db, feedback_obi)

	#잘못된 요청을 보냈음!, Bad request 핸들러 반환
	if check_feedback is None: abort(400)

	#잘못된 요청을 보냈음!, Bad request 핸들러 반환
	if activation > 1 or activation < 0: abort(400)

	result = update_feedback_activation(g.db, feedback_obi, activation)
	
	return jsonify(
		result = result
	)

#메인 Info 메시지 수정 (작동중)
@BP.route('/api/v1/admin/message/update', methods=['POST'])
@jwt_required
def SJ_api_v1_admin_message__update():
	ADMIN = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 ADMIN 토큰!, Admin only 핸들러 반환
	if ADMIN is None or ADMIN['user_id'] != SJ_ADMIN: abort(403)

	NEW_INFO_1 = request.form['new_info_1']
	NEW_INFO_2 = request.form['new_info_2']

	#길이 검증 실패!, Bad request 핸들러 반환
	if len(NEW_INFO_1) > 50 or len(NEW_INFO_2) > 50: abort(400)

	result = update_variable(g.db, 'main_info_1', NEW_INFO_1)
	result = update_variable(g.db, 'main_info_2', NEW_INFO_2)

	return jsonify(
		result = result
	)

#메인 Info 메시지 반환 (작동중)
@BP.route('/api/v1/admin/message/all')
def SJ_api_v1_admin_message__all():
	main_info_1 = find_variable(g.db, 'main_info_1')
	main_info_2 = find_variable(g.db, 'main_info_2')
	
	result = []

	result.append(main_info_1)
	result.append(main_info_2)

	return jsonify(
		result = "success",
		main_info = result
	)

#모든 회원 관심도 초기화 (보류)
@BP.route('/all_reset_user_measurement')
@jwt_required
def all_reset_user_measurement():
	ADMIN = find_user(g.db, user_id=get_jwt_identity())

	#잘못된 ADMIN 토큰!, Admin only 핸들러 반환
	if ADMIN is None or ADMIN['user_id'] != SJ_ADMIN: abort(403)

	USER_LIST = find_all_user(g.db, user_id=1)
	USER_LIST = list(USER_LIST)

	for USER in USER_LIST:
		#회원 관심도 초기화!
		result = update_user_measurement_reset(g.db, USER['user_id'])

	return jsonify(
		result = "success"
	)


#############################################################################
#############################################################################