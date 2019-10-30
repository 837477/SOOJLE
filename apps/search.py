from flask import *
from flask_jwt_extended import *
from werkzeug import *
##########################################
from bson.json_util import dumps
from bson.objectid import ObjectId
##########################################
from db_management import *
from global_func import *
import jpype
from tknizer import get_tk
##########################################
BP = Blueprint('search', __name__)
##########################################

@BP.route('/search')
@logging_time
@jwt_optional
def search_():
	#search_str = request.form['search']

	#jwt 토큰이 들어오면, 유저 검색 기록에 기록!
	if get_jwt_identity():
		USER = find_user(g.db, _id=1, user_id=get_jwt_identity())

		#JAVA 스레드 이동.
		jpype.attachThreadToJVM()
		#토크나이저 실행!!
		tokenizer_result = get_tk(search_str)

		result = update_user_search_list_push(g.db, USER['_id'], tokenizer_result)

	#search_str을 페스트텍스트 함수에 넣어서 토큰 추출.
	#search_token = func()

	result = find_token(g.db, ['세종대학교', '연구'])

	return jsonify(result = result)
