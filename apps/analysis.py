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


#실시간 검색어 순위 반환
@BP.route('/api/v1/analysis/realtime_keyword')
def SJ_api_v1_analysis__realtime_keyword():
	result = find_search_realtime(g.db)
	result = result[0]

	return jsonify(
			result = "success",
			search_realtime = result['real_time'][:SJ_REALTIME_RETURN_LIMIT]
		)

#통계 통합형 반환
@BP.route('/api/v1/analysis/all')
def SJ_api_v1_analysis__all():
	result = {}

	#총 검색 갯수
	result['search_count'] = find_variable(g.db, 'total_search_cnt')
	
	#소통 수 반환 (하루 평균 기준)
	result['communication_avg'] = find_variable(g.db, 'communication_avg')
	
	#총 DB posts 갯수
	result['posts_count'] = find_variable(g.db, 'total_posts_cnt')
	
	#오늘 방문자 수
	result['today_visitor'] = find_today_visitor_count(g.db)

	#총 방문자 수
	result['total_visitor'] = find_variable(g.db, 'total_visitor')

	#하루 평균 방문자 수
	result['day_avg_visitor'] = find_variable(g.db, 'day_avg_visitor')

	#하루 최고 방문자 수
	result['highest_day_visitor'] = find_variable(g.db, 'highest_visitor')

	#전체 게시글 조회수
	result['total_view'] = find_variable(g.db, 'total_view')

	#전체 게시글 좋아요 수
	result['total_fav'] = find_variable(g.db, 'total_fav')

	return jsonify(
		result = "success",
		analysis = result
	)

#매일 기록되는 통계 반환 API (몇일 전 버전)
@BP.route('/api/v1/analysis/lastdays/<int:days>')
def SJ_api_v1_analysis__lastdays(days):
	today_year = datetime.today().year
	today_month = datetime.today().month
	today_day = datetime.today().day
	
	date = datetime(today_year, today_month, today_day) - timedelta(days = days+1)
	
	result = SJ_DB_ANALYSIS_find_lastdays(g.db, date)
	result = list(result)

	return jsonify(
		result = "success",
		analysis = result
	)

#무슨 디바이스로 접속했는지 기록용 API
@BP.route('/api/v1/analysis/insert_device/<string:device>')
def SJ_api_v1_analysis__insert_device(device):
	if device == 'device_pc' or device == 'device_tablet' or device == 'device_mobile':
		result = update_variable_inc(g.db, device, 1)

	#잘못된 디바이스가 들어왔을 때!, Bad request 핸들러 반환
	else: abort(400)

	return jsonify(
		result = result
	)

#무슨 디바이스로 접속했는지 기록용 API
@BP.route('/api/v1/analysis/get_device')
def SJ_api_v1_analysis__get_device():
	PC = find_variable(g.db, 'device_pc')
	TABLET = find_variable(g.db, 'device_tablet')
	MOBILE = find_variable(g.db, 'device_mobile')

	return jsonify(
		result = "success",
		pc = PC,
		tablet = TABLET,
		mobile = MOBILE
	)

