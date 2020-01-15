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

#회원 삭제
@BP.route('/admin_remove_user/<string:user_id>')
@jwt_required
def admin_remove_user(user_id):
	admin = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	#Admin 확인
	if admin is None or admin['major'] != SJ_ADMIN:
		return jsonify(result = "Not admin")

	#삭제 대상 획원 유무 확인
	target_user = find_user(g.db, _id=1, user_id=user_id)

	if target_user is None:
		return jsonify(result = "Not found")

	#회원 삭제!
	result = remove_user(g.db, user_id)

	return jsonify(result = result)

#게시글 입력
@BP.route('/insert_post', methods=['POST'])
@jwt_required
def insert_post():
	admin = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	#Admin 확인
	if admin is None or admin['major'] != SJ_ADMIN:
		return jsonify(result = "Not admin")

	title = request.form['title']
	post = request.form['post']
	tag = request.form['tag']
	img = request.form['img']
	url = request.form['url']
	info = request.form['info']

	hashed = hashlib.md5((title + post).encode('utf-8')).hexdigest()
	url_hashed = hashlib.md5(url.encode('utf-8')).hexdigest()
	token = tknizer.get_tk(title + post).lower()
	view = 0
	fav_cnt = 0
	title_token = title.split(' ')
	login = 0
	learn = 0
	popularity = 0
	topic = LDA.get_topics((tag + token))
	ft_vector = FastText.get_doc_vector((tag + token)).tolist()

	result = insert_post(g.db, title, post, tag, img, url, info, hashed, url_hashed, token, view, fav_cnt, title_token, login, learn, popularity, topic, ft_vector)

	return jsonify(
		result = result
	)

#게시글 수정
@BP.route('/update_post/<string:post_obi>', methods=['POST'])
@jwt_required
def update_post(post_obi):
	admin = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	#Admin 확인
	if admin is None or admin['major'] != SJ_ADMIN:
		return jsonify(result = "Not admin")

	title = request.form['title']
	post = request.form['post']
	tag = request.form['tag']
	img = request.form['img']
	url = request.form['url']
	info = request.form['info']

	hashed = hashlib.md5((title + post).encode('utf-8')).hexdigest()
	url_hashed = hashlib.md5(url.encode('utf-8')).hexdigest()
	token = tknizer.get_tk(title + post).lower()
	title_token = title.split(' ')
	topic = LDA.get_topics((tag + token))
	ft_vector = FastText.get_doc_vector((tag + token)).tolist()

	result = update_post(g.db, post_obi, title, post, tag, img, url, info, hashed, url_hashed, token, title_token, topic, ft_vector)

	return jsonify(
		result = result
	)

#게시글 삭제
@BP.route('/remove_post/<string:post_obi>')
@jwt_required
def remove_post(post_obi):
	admin = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	#Admin 확인
	if admin is None or admin['major'] != SJ_ADMIN:
		return jsonify(result = "Not admin")

	target_post = find_post(g.db, post_obi=post_obi)

	if target_post is None:
		return jsonify(result = "Not found")

	#post 삭제!
	result = remove_post(g.db, post_obi)

	return jsonify(result = result)

#공지사항 입력
@BP.route('/insert_notice', methods=['POST'])
@jwt_required
def insert_notice():
	new_title = request.form['title']
	new_post = request.form['post']
	new_url = request.form['url']

	admin = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	#Admin 확인
	if admin is None or admin['major'] != SJ_ADMIN:
		return jsonify(result = "Not admin")

	result = insert_notice(g.db, title, post, rul)

	return jsonify(
		result = result
	)

#공지사항 수정
@BP.route('/update_notice/<string:notice_obi>', methods=['POST'])
@jwt_required
def update_notice(notice_obi):
	new_title = request.form['title']
	new_post = request.form['post']
	new_url = request.form['url']
	
	admin = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	#Admin 확인
	if admin is None or admin['major'] != SJ_ADMIN:
		return jsonify(result = "Not admin")

	result = update_notice(g.db, notice_obi, title, post, url)

	return jsonify(
		reuslt = result
	)

#공지사항 삭제
@BP.route('/remove_notice/<string:notice_obi>', methods=['POST'])
@jwt_required
def remove_notice(notice_obi):
	admin = find_user(g.db, user_id=get_jwt_identity(), user_major=1)

	#Admin 확인
	if admin is None or admin['major'] != SJ_ADMIN:
		return jsonify(result = "Not admin")

	notice = find_notice(g.db, notice_obi)

	if notice is None:
		return jsonify(result = "Not found")

	result = remove_notice(g.db, notice_obi)

	return jsonify(
		result = result
	)

@BP.route('/send_feedback', methods=['POST'])
@jwt_required
def send_feedback():
	user = find_user(g.db, user_id=get_jwt_identity())
	if user is None: abort(400)

	FEEDBACK_TYPE = request.form['type']
	FEEDBACK_POST = request.form['post']
	FEEDBACK_TIME = datetime.now()
	FEEDBACK_AUTHOR = user['user_id']

	feedback_data = {
    	'type': FEEDBACK_TYPE,
    	'time': FEEDBACK_TIME,
    	'post': FEEDBACK_POST,
    	'author': FEEDBACK_AUTHOR
	}

	result = insert_user_feedback(g.db, feedback_data)

	if result == "success":
		return jsonify(result = "success")
	else:
		return jsonify(result = "fail")
	

#admin 생성
@BP.route('/create_admin')
def create_admin():
	USER_ID = "test15"
	USER_PW = "test15"

	#SOOJLE DB에 추가.
	insert_user(g.db,
		USER_ID,
		generate_password_hash(USER_PW),
		"SOOJLE",
		"SJ_SUPER_ADMIN_837477_IML_NB"
	)

	return jsonify(
		result = "success",
		access_token = create_access_token(
			identity = USER_ID,
			expires_delta=False)
	)
	