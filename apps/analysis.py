from flask import *
from flask_jwt_extended import *
from werkzeug import *
##########################################
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import operator
import math
from numpy import dot
from numpy.linalg import norm
import numpy
##########################################
from db_management import *
from global_func import *
import jpype
import tknizer
from pprint import pprint
##########################################
BP = Blueprint('analysis', __name__)
##########################################

#실시간 검색서 순위 반환
@BP.route('/get_search_realtime')
def get_search_realtime():
	search_realtime = find_search_realtime(g.db)

	result = []
	for i in range(10):
		result.append(search_realtime['real_time'][i][0])

	return jsonify(
		result = "success",
		search_realtime = result)

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

