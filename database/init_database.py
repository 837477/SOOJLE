from pymongo import *
from flask import g
from datetime import datetime, timedelta
from db_info import *


def get_db():
    if 'db_client' not in g:
        db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
        g.db_client = db_client

    if 'db' not in g:
        g.db = g.db_client["soojle"]
        
def close_db():
    db_client = g.pop('db_client', None)
    if db_client is not None:
        db_client.close()

#몽고디비 첫 start collection 체킹 및 초기화
def init_db():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	#현재 db에 있는 collection 이름을 리스트로 불러온다.
	db_collections = db.list_collection_names()

	if not 'user' in db_collections:
		db['user']

	if not 'posts' in db_collections:
		db['posts']
		create_dummy_post(db)

	if not 'newsfeed_of_topic' in db_collections:
		create_newsfeed_of_topic(db)

	if not 'variable' in db_collections:
		create_variable(db)

	if not 'search_realtime' in db_collections:
		db['search_realtime']

	if not 'search_log' in db_collections:
		db['search_log']

	if not 'log' in db_collections:
		db['log']

	if db_client is not None:
		db_client.close()

#토빅별 뉴스피드 컬럼 생성!
def create_newsfeed_of_topic(db):
	db['newsfeed_of_topic'].insert(
		[
			#대학교
			{'newsfeed_name': '대학교',
			'info': ['^main', '^library_', '^promotion_', '^classic_', '^counselor', '^skbs_', '^chong_', '_dormitory$', '^dodream_', '^mobilelibrary_', '^naverblog_sejong$'],
			'tag': ['장학', '사이버강의', '수강', '졸업', '조교', 'FAQ', '소식', '학사', '국제', '교환학생', '수강편람', '입학', '학술정보원', '입찰', '방송국', '홍보원', '교내', '전화번호부', 'CK사업단', '총학생회', '행복기숙사', '전자도서관', '학사일정', '대양휴머니티칼리지', '에델바이스', '학부', 'kmooc', '블랙보드', 'uis', '학기', '창의', '학술'],
			'negative_tag': ['커뮤니티']},
			#동아리&모임
			{'newsfeed_name': '동아리&모임',
			'info': ['_language$', '^campuspick_job$', '_certificate$', '_study$', '_club$'],
			'tag': ['멘토링', '동아리&모임', '방송국', '총학생회', '동아리', '모임', '스터디', '서포터즈', '봉사단'],
			'negative_tag': []},
			#공모전&행사
			{'newsfeed_name': '공모전&행사',
			'info': ['_event$', '_shp$', '^thinkgood_', '_activity$', '_contest$', '_semina$', '_speech$'],
			'tag': ['행사', '공모전&대외활동', '세미나', '봉사', '두드림', '봉사단', '공모전', '대외활동', '대내활동', '특강', '강연', '대회', '경연', '대양홀', '콩쿨', '콩쿠르', '개최', '축제', '기념', '콘서트', '콘테스트', '연주회', '대동제', '힘미제', '박람회', '캠프', '컨퍼런스', '콘퍼런스', '간담회', '파티', '경진'],
			'negative_tag': ['커뮤니티']},
			#진로&구인
			{'newsfeed_name': '진로&구인',
			'info': ['_job$', '^udream_', '_college$', '^jobkorea', '^sejongbab_', '^rndjob_', '^jobsolution'],
			'tag': ['취업&진로', '창업', '모집', '과외&강사', '알바&구인', '공개채용', '추천채용', '특별채용', '수시채용', '인턴', '계약직', '정규직', '경력', '기술직', '의료직', '교직', '마케팅', '조리직', '서비스직', '알바', '구인', '과외', '강사', '취업', '진로', '채용', '직업', '일자리', '인턴쉽', '인턴십', '산업체'],
			'negative_tag': ['커뮤니티']},
			#장터
			{'newsfeed_name': '장터',
			'info': ['^everytime_book$', '_trade$'],
			'tag': ['자취&하숙', '자취', '하숙', '장터'],
			'negative_tag': []},
			#자유
			{'newsfeed_name': '자유',
			'info': ['^sejongstation_', '^everytime_', '_lost$'],
			'tag': ['학식', '고민&상담', '종교', '여행', '커뮤니티', '분실물', '연애', '세종냥이', '홍보', '세종대역'],
			'negative_tag': []}
		])

#정적 테이블 컬럼 생성!
def create_variable(db):
	db['variable'].insert(
		[
			{
				'key': 'highest_fav_cnt',
				'value': 1
			},
			{
				'key': 'highest_view_cnt',
				'value': 1
			},
			{
				'key': 'renewal',
				'value': datetime.now()
			},
			{
				'key': 'total_visitor',
				'value': 0
			},
			{
				'key': 'highest_visitor',
				'value': 0
			},
			{
				'key': 'today_time_visitor',
				'value': []
			},
			{
				'key': 'day_avg_visitor',
				'value': 0
			},
			{
				'key': 'service_period',
				'value': 1
			},
			{
				'key': 'total_view',
				'value': 0
			},
			{
				'key': 'total_fav',
				'value': 0
			},
			{
				'key': 'today_view',
				'value': 0
			},
			{
				'key': 'today_fav',
				'value': 0
			},
			{
				'key': 'total_posts_cnt',
				'value': 0
			},
			{
				'key': 'total_search_cnt',
				'value': 0
			}
		]
	)


##좋아요/조회수 초기 셋팅용 더비 포스트 생성!
def create_dummy_post(db):
	check_ = check_dummy_post(db)

	if not 'title' in check_:
		insert_dummy_post(db)
