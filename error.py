from flask import Blueprint, render_template, jsonify
BP = Blueprint('error', __name__)
# 배드 리퀘스트 에러를 반환할 경우, 즉시 로컬 스토리지 삭제
@BP.app_errorhandler(400)
def bad_requests(error):
		return jsonify(result = "bad request"), 400

@BP.app_errorhandler(403)
def admin_only(error):
		return jsonify(result = "admin only"), 403

@BP.app_errorhandler(404)
def page_not_found(error):
		return jsonify(result = "404 page"), 404

@BP.app_errorhandler(405)
def bad_requests(error):
		return jsonify(result = "bad request"), 405

@BP.app_errorhandler(406)
def bad_requests(error):
		return jsonify(result = "bad request"), 406

@BP.app_errorhandler(422)
def bad_requests(error):
		return jsonify(result = "bad request"), 422

@BP.app_errorhandler(500)
def server_error(error):
		return jsonify(result = "fail"), 500