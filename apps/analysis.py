from flask import *
from flask_jwt_extended import *
from werkzeug import *
##########################################
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
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
