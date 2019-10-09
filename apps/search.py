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
@jwt_optional
def search_():
	search_str = request.form['search']

	result = "success"

	if get_jwt_identity():
		USER = find_user(g.db, _id=1, user_id=get_jwt_identity())

		#JAVA 스레드 이동.
		jpype.attachThreadToJVM()
		#토크나이저 실행!
		tokenizer_result = get_tk(search_str)

		result = update_user_search_list_push(g.db, USER['_id'], tokenizer_result)

	return jsonify(result = result)
