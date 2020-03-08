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

	if 'user' not in db_collections:
		db['user']

	if 'posts' not in db_collections:
		db['posts']
		create_dummy_post(db)

	if 'category_of_topic' not in db_collections:
		create_category_of_topic(db)
		create_category_of_topic_info_num(db)

	if SJ_VARIABLE not in db_collections:
		create_variable(db)

	if 'search_realtime' not in db_collections:
		db['search_realtime']

	if 'search_log' not in db_collections:
		db['search_log']

	if 'log' not in db_collections:
		db['log']

	if 'today_visitor' not in db_collections:
		db['today_visitor']

	if 'pushback' not in db_collections:
		db['pushback']

	if 'notice' not in db_collections:
		db['notice']

	if 'feedback' not in db_collections:
		db['feedback']

	if 'everyday_analysis' not in db_collections:
		db['everyday_analysis']

	if db_client is not None:
		db_client.close()

#카테고리별 뉴스피드 컬럼 생성!
def create_category_of_topic(db):
	db['category_of_topic'].insert(
		[
			#대학교
			{
				'category_name': '대학교',
				'info': 
				[
					'sj1_main_founded', 'sj1_main_notice', 'sj1_main_entrance', 'sj1_main_job',  'sj1_main_schoiarship', 'sj1_main_college', 'sj1_main_bidding' 'sj1_main_dataprocessFAQ', 'sj1_main_studentFAQ', 'sj1_main_schoiarshipFAQ', 'sj1_main_foreignerFAQ', 'sj1_main_foreignernotice', 'sj6_library_notice', 'sj6_library_book', 'sj6_library_FAQ', 'sj7_promotion_article', 'sj7_promotion_prism', 'sj7_promotion_report', 'sj7_promotion_research', 'sj7_promotion_speech', 'sj8_promotion_media', 'sj15_classic_notice', 'sj15_classic_news', 'sj15_classic_creative', 'sj15_classic_event', 'sj15_classic_shp', 'sj17_counselor_notice', 'sj17_counselor_free', 'sj18_skbs_notice', 'sj18_skbs_event', 'sj18_skbs_article', 'sj18_skbs_music', 'sj18_skbs_news', 'sj19_chong_news', 'sj19_chong_notice', 'sj19_chong_lost','sj24_sejong_allie', 'sj29_sejong_dormitory', 'sj33_mobilelibrary_notice', 'sj44_naverblog_sejong', 'sj44_naverblog_campustown'
				],
				'tag': 
				[
					'장학', '사이버강의', '수강', '졸업', '조교', 'FAQ', '소식', '학사', '국제', '교환학생', '수강편람', '입학', '학술정보원', '입찰', '방송국', '홍보원', '교내', '전화번호부', 'CK사업단', '총학생회', '행복기숙사', '전자도서관', '학사일정', '대양휴머니티칼리지', '에델바이스', '학부', 'kmooc', '블랙보드', 'uis', '학기', '창의', '학술'
				]
			},
			#동아리&모임
			{
				'category_name': '동아리&모임',
				'info': 
				[
					'sj27_campuspick_language', 'sj27_campuspick_job', 'sj27_campuspick_certificate', 'sj27_campuspick_study', 'sj28_campuspick_club'

				],
				'tag': 
				[
					'멘토링', '동아리&모임', '방송국', '총학생회', '동아리', '모임', '스터디', '서포터즈', '봉사단'
				]
			},
			#공모전&행사
			{
				'category_name': '공모전&행사',
				'info': 
				[
					'sj25_thinkgood_info', 'sj26_campuspick_activity', 'sj26_campuspick_contest', 'sj31_dodream_event', 'sj32_dodream_promotion', 'sj35_detizen_contest', 'sj35_detizen_activity'
				],
				'tag': 
				[
					'행사', '공모전&대외활동', '세미나', '봉사', '두드림', '봉사단', '공모전', '대외활동', '대내활동', '특강', '강연', '대회', '경연', '대양홀', '콩쿨', '콩쿠르', '개최', '축제', '기념', '콘서트', '콘테스트', '연주회', '대동제', '힘미제', '박람회', '캠프', '컨퍼런스', '콘퍼런스', '간담회', '파티', '경진'
				]
			},
			#진로&구인
			{
				'category_name': '진로&구인',
				'info': 
				[
					'sj2_udream_notice', 'sj3_udream_jobinfo', 'sj4_udream_workinfo', 'sj5_udream_workyoung', 'sj36_jobkoreatip_tip', 'sj37_jobkorea_job', 'sj37_jobkorea_public', 'sj38_sejongbab_tip', 'sj39_rndjob_job', 'sj40_jobsolution_job', 'sj41_jobsolutionAnother_semina', 'sj42_jobsolutionAnother_review', 'sj42_jobsolutionAnother_interview', 'sj43_indeed_job'
				],
				'tag': 
				[
					'취업&진로', '창업', '모집', '과외&강사', '알바&구인', '공개채용', '추천채용', '특별채용', '수시채용', '인턴', '계약직', '정규직', '경력', '기술직', '의료직', '교직', '마케팅', '조리직', '서비스직', '알바', '구인', '과외', '강사', '취업', '진로', '채용', '직업', '일자리', '인턴쉽', '인턴십', '산업체'
				]
			},
			#자유
			{
				'category_name': '자유',
				'info': 
				[
					'sj20_sejong_dc', 'sj30_sejongstation_notice', 'sj30_sejongstation_news', 'sj30_sejongstation_free', 'sj30_sejongstation_secret', 'sj30_sejongstation_qna', 'sj30_sejongstation_tip', 'sj30_sejongstation_graduation', 'sj30_sejongstation_job', 'sj30_sejongstation_activity', 'sj30_sejongstation_club', 'sj30_sejongstation_study', 'sj30_sejongstation_food', 'sj30_sejongstation_trade'
				],
				'tag': 
				[
					'학식', '고민&상담', '종교', '여행', '커뮤니티', '분실물', '연애', '세종냥이', '홍보', '세종대역'
				]
			},
			#예외(검색용)
			{
				'category_name': '예외',
				'info':
				[
					'sj9_chinatrade_notice', 'sj9_chinatrade_job', 'sj9_history_notice', 'sj9_history_data', 'sj9_ecotrade_notice', 'sj9_ecotrade_event', 'sj9_administ_notice', 'sj9_management_notice', 'sj9_management_job', 'sj9_hotel_notice', 'sj9_software_notice', 'sj9_elecommunication_notice', 'sj9_elecommunication_data', 'sj9_infoprotection_notice', 'sj9_infoprotection_job', 'sj9_energy_notice', 'sj9_nano_notice', 'sj9_nano_job', 'sj9_nano_FAQ', 'sj9_defensesys_notice', 'sj9_indusdesign_notice', 'sj9_indusdesign_data', 'sj9_designinnovation_studentnotice', 'sj9_designinnovation_notice', 'sj9_designinnovation_data', 'sj9_animation_notice', 'sj9_pysical_notice', 'sj9_pysical_job', 'sj9_dance_notice', 'sj9_dance_event', 'sj9_law_notice', 'sj10_pysics_notice', 'sj11_japanese_notice', 'sj12_archi_notice', 'sj12_archi_news', 'sj13_computer_notice', 'sj13_computer_event', 'sj13_computer_job', 'sj14_imc_notice', 'sj14_imc_news', 'sj14_imc_student', 'sj16_navercafe_foreigner', 'sj16_navercafe_music', 'sj16_navercafe_animation', 'sj16_navercafe_math', 'sj16_navercafe_korean', 'sj16_navercafe_environmentenergy', 'sj16_navercafe_chemistry', 'sj16_navercafe_sjnanuri', 'sj16_navercafe_eleinfoengineer', 'sj16_navercafe_imc', 'sj16_navercafe_club', 'sj21_sejong_wiki', 'sj9_computer_notice'
				],
				'tag': []
			}
		])

#카테고리별 뉴스피드 컬럼 info_num 추가!
def create_category_of_topic_info_num(db):
	#post_info 전체 호출
	post_info_list = db['post_info'].find()
	post_info_list = list(post_info_list)

	#category_of_topic 전체 호출
	category_of_topic_list = db['category_of_topic'].find()
	category_of_topic_list = list(category_of_topic_list)

	#카테고리 를 반복문 돌림
	for category in category_of_topic_list:
		#카테고리 info_num 임시 배열을 생성
		category_temp_info_num_list = []

		#각 카테고리들의 info를 반복문 돌림!
		for category_info in category['info']:
			#post_info 리스트를 반복문 돌림!
			for post_info in post_info_list:
				#카테고리 명이랑 정의된 post_info와 같으면?!
				if category_info == post_info['info_id']:
					#info num 추출!
					category_temp_info_num_list.append(post_info['info_num'])
					#시간복잡도를 위해 찾은건 다시 for문 돌릴때 볼 필요 없으므로 삭제.
					#post_info_list.remove(post_info)
		
		#category_of_topic 콜렉션에 info_num 리스트 컬럼 추가!
		db['category_of_topic'].update(
			{
				'category_name': category['category_name']
			},
			{
				'$set':
				{
					'info_num': category_temp_info_num_list
				}
			}
		)

#정적 테이블 컬럼 생성!
def create_variable(db):
	db[SJ_VARIABLE].insert(
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
			},
			{
				'key': 'communication_avg',
				'value': 0
			},
			{
				'key': 'device_pc',
				'value': 0
			},
			{
				'key': 'device_tablet',
				'value': 0
			},
			{
				'key': 'device_mobile',
				'value': 0
			}
		]
	)

##좋아요/조회수 초기 셋팅용 더비 포스트 생성!
def create_dummy_post(db):
	check_ = check_dummy_post(db)

	if not 'title' in check_:
		insert_dummy_post(db)
