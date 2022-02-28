import sys
#837477 Path
sys.path.insert(0,'./')
sys.path.insert(0,'../SOOJLE')
sys.path.insert(0,'../SJ_AI/src')
sys.path.insert(0,'../IML_Tokenizer/src')
sys.path.insert(0,'../SOOJLE/database')
sys.path.insert(0,'../SOOJLE/apps')
###########################################
#Ubuntu Path
sys.path.insert(0,'/home/iml/')
sys.path.insert(0,'/home/iml/SOOJLE/')
sys.path.insert(0,'/home/iml/SOOJLE/database')
sys.path.insert(0,'/home/iml/SOOJLE_Crawler/src/')
sys.path.insert(0,'/home/iml/SJ_AI/src')
sys.path.insert(0,'/home/iml/IML_Tokenizer/src/')
###################################################
from pymongo import *
from datetime import timedelta, datetime
###################################################
from db_management import *
from db_info import *
from variable import *
from global_func import get_default_day


#하루 통계 작업 (하루마다!) (테스트 대상)
def SJ_day_analysis():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]




	#오늘 통계 객체화
	################################################################
	today_analysis = {}
	#오늘 방문자 수 가져오기
	today_analysis['today_visitor'] = find_today_visitor_count(db)
	#오늘 시간대별 방문자 수
	today_analysis['today_time_visitor'] = find_variable(db, 'today_time_visitor')
	#오늘 조회된 게시글
	today_analysis['today_view'] = find_variable(db, 'today_view')
	#오늘 좋아요된 게시글
	today_analysis['today_fav'] = find_variable(db, 'today_fav')

	today = datetime.now() - timedelta(days = 1)

	today_year = today.year
	today_month = today.month
	today_day = today.day

	#오늘 날짜 기입!
	today_analysis['date'] = datetime(today_year, today_month, today_day)
	
	#매일 기록되는 통계 테이블에 기록!
	insert_everyday_analysis(db, today_analysis)
	################################################################






	#매일마다 갱신 시켜야하는 정적 변수들!
	################################################################
	#서비스 기간 하루 증가!
	update_variable_inc(db, 'service_period', 1)

	#총 방문자수 증가! (오늘 방문자 수를 더해준다.)
	update_variable_inc(db, 'total_visitor', today_analysis['today_visitor'])

	#최고 방문자 수 갱신!
	highest_visitor = find_variable(db, 'highest_visitor')
	if highest_visitor < today_analysis['today_visitor']:
		update_variable(db, 'highest_visitor', today_analysis['today_visitor'])

	#하루 평균 방문자 수 갱신!
	total_visitor = find_variable(db, 'total_visitor')
	service_period = find_variable(db, 'service_period')
	day_avg = total_visitor // service_period
	update_variable(db, 'day_avg_visitor', day_avg)

	#총 조회한 게시글 수 갱신!
	update_variable_inc(db, 'total_view', today_analysis['today_view'])

	#총 좋아요한 게시글 수 갱신!
	update_variable_inc(db, 'total_fav', today_analysis['today_fav'])

	#총 검색 횟수 갱신!
	total_search_cnt = find_search_count(db)
	update_variable(db, 'total_search_cnt', total_search_cnt)

	#총 게시글 수 갱신!
	total_posts_cnt = find_posts_count(db)
	update_variable(db, 'total_posts_cnt', total_posts_cnt)

	#총 소통 횟수 갱신!
	API_log_cnt = find_log_count(db)
	communication_avg = API_log_cnt // service_period
	update_variable(db, 'communication_avg', communication_avg)
	################################################################





	#매일마다 초기화 해줘야하는 정적 변수들!
	################################################################
	#오늘 조회한 게시글 0으로 초기화
	update_variable(db, 'today_view', 0)

	#오늘 좋아요한 게시글 0으로 초기화
	update_variable(db, 'today_fav', 0)

	#today_visitor 콜렉션 비우기!
	remove_today_visitor(db)

	#today_time_visitor 빈 리스트로 초기화
	today_time_visitor_empty = []
	update_variable(db, 'today_time_visitor', today_time_visitor_empty)
	################################################################
	if db_client is not None:
		db_client.close()
	

if __name__ == '__main__':
	FILE = open('/home/iml/log/background.log', 'a')
	#FILE = open('background.log', 'a')
	
	try:
		SJ_day_analysis()
		log_data = str(datetime.now()) + " ::: 하루 통계 캐싱 성공 :)  \n"
    
	except Exception as ex:
		log_data = str(datetime.now()) + " ::: 하루 통계 캐싱 실패 :(  \n" + str(ex) + "\n"

	FILE.write(log_data)

	FILE.close()