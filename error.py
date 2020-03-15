from flask import Blueprint, render_template, jsonify
BP = Blueprint('error', __name__)

#잘못된 요청일 때! (프론트 1차 과정을 무시하고 비정상적인 경로로 요청했을 경우!)
@BP.app_errorhandler(400)
def bad_requests(error):
	return jsonify(result = "Bad request"), 400

#잘못된 토큰일 때! (유저 토큰이 잘못되었을 경우!)
@BP.app_errorhandler(401)
def bad_requests(error):
	return jsonify(result = "Bad token"), 401

#잘못된 토큰일 때! (어드민 토큰이 잘못되었을 경우!)
@BP.app_errorhandler(403)
def admin_only(error):
	return jsonify(result = "Admin only"), 403

#없는 주소 접속시!
@BP.app_errorhandler(404)
def page_not_found(error):
	return render_template('etc/404.html')

#서버에서 처리할 수 없는 경우가 발생시!
@BP.app_errorhandler(500)
def server_error(error):
	return jsonify(result = "Fail"), 500


########################################################################
