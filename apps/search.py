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

@BP.route('/search', methods=['POST'])
@logging_time
@jwt_optional
def search_():
	search_str = request.form['search']

	#JAVA 스레드 이동.
	jpype.attachThreadToJVM()
	#토크나이저 실행!!
	tokenizer_result = get_tk(search_str)

	if not tokenizer_result:
		return jsonify(result = "NONE")

	#jwt 토큰이 들어오면, 유저 검색 기록에 기록!
	if get_jwt_identity():
		USER = find_user(g.db, _id=1, user_id=get_jwt_identity())

		result = update_user_search_list_push(g.db, USER['_id'], tokenizer_result)

	FastText_token = FastText.sim_words(tokenizer_result)

	search_token = []
	for token in FastText_token:
		if token[1] > 0:
			search_token.append(token[0])

	print(search_token)
	result = find_token(g.db, search_token)

	return jsonify(
		result = "success",
		search = list(result))
