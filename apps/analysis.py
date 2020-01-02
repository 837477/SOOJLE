from flask import *
from flask_jwt_extended import *
from werkzeug import *
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from pprint import pprint
##########################################
from db_management import *
from global_func import *
import jpype
import tknizer
##########################################
from variable import *


#BluePrint
BP = Blueprint('analysis', __name__)


#실시간 검색서 순위 반환
@BP.route('/get_search_realtime')
def get_search_realtime():
	result = find_search_realtime(g.db)
	result = result[0]

	return jsonify(
		result = "success",
		search_realtime = result['real_time'][:SJ_REALTIME_RETURN_LIMIT])

#log) 시간대 반환 (date는 한개씩만 사용 가능, limit 설정!)
@BP.route('/get_log_date/<int:months>/<int:days>/<int:hours>/<int:limit>')
def get_log_date(months, days, hours, limit):
	#시간별로 로그 반환!
	if months != 0 and months <= 6:
		date = datetime.now() - relativedelta(months = months)
	elif days != 0 and days <= 7:
		date = datetime.now() - timedelta(days = days)
	elif hours != 0 and hours <= 24:
		date = datetime.now() - timedelta(hours = hours)
	else:
		return jsonify(result = "try again")

	result = find_date_log(g.db, date, limit)
	result = list(result)

	return jsonify(
		result = "success",
		log = result)

#log) 특정 user 반환
@BP.route('/get_log_user/<string:user_id>/<int:limit>')
def get_log_user(user_id, limit):
	result = find_user_log(g.db, user_id, limit)
	result = list(result)

	return jsonify(
		result = "success",
		log = result)
	
#log) 특정 user, 시간별 반환
@BP.route('/get_log_user_date/<string:user_id>/<int:months>/<int:days>/<int:hours>/<int:limit>')
def get_log_user_date(user_id, months, days, hours, limit):
	#시간별로 로그 반환!
	if months != 0 and months <= 6:
		date = datetime.now() - relativedelta(months = months)
	elif days != 0 and days <= 7:
		date = datetime.now() - timedelta(days = days)
	elif hours != 0 and hours <= 24:
		date = datetime.now() - timedelta(hours = hours)
	else:
		return jsonify(result = "try again")

	result = find_user_date_log(g.db, user_id, date, limit)
	result = list(result)

	return jsonify(
		result = "success",
		log = result)

#입력된 str을 fasttext로 유사한 단어를 추출 해주는 API
@BP.route('/get_similarity_words', methods = ['POST'])
def simulation_fastext():
	input_str = request.form['search']

	tokenizer_list = tknizer.get_tk(input_str)
	
	result = {}
	for word in tokenizer_list:
		similarity_list = []
		for sim_word in FastText.sim_words(word):
			temp = {}
			if sim_word[1] >= SJ_FASTTEXT_SIM_PERCENT: 
				temp[sim_word[0]] = sim_word[1]
				similarity_list.append(temp)
			else: break	
		result[word] = similarity_list

	return jsonify(
		result = "success",
		similarity_words = result)

#외부사이트 접속했다는 것을 알려주기위한 API
@BP.route('/access_external_site/<string:site_name>')
@jwt_optional
def access_external_site(site_name):
	#logging!
	if get_jwt_identity():
		result = insert_log(g.db, get_jwt_identity(), request.path, student_num = True, site_name)
	else:
		result = insert_log(g.db, request.remote_addr, request.path, site_name)

	return jsonify(result = result)

# #명예의 전당: 외부사이트
# @BP.route('/get_max_external_site')
# def get_max_external_site():


#명예의 전당: 학번 업데이트
@BP.route('/testtest')
def testtest():
	result = aggregate_groupby_log_student_num(g.db)
	result = list(result)


	print(result[0])
	