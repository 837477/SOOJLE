import sys
sys.path.insert(0,'../')
sys.path.insert(0,'../IML_Tokenizer/src/')
sys.path.insert(0,'../SJ_AI/src')
sys.path.insert(0,'./database/')
from pymongo import *
from flask import g
from datetime import datetime, timedelta
from db_info import *
from variable import *
import numpy as np
from tknizer import get_tk
import LDA
import FastText
from db_management import *

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

	if 'posts' not in db_collections:
		db['posts']
		create_dummy_post(db)

	if 'SJ_USER' not in db_collections:
		db['SJ_USER']

	if 'SJ_CATEGORY' not in db_collections:
		create_category_of_topic(db)
		create_category_of_topic_info_num(db)
		create_category_of_topic_tag_vector(db)

	if 'SJ_VARIABLE' not in db_collections:
		create_variable(db)

	if 'SJ_REALTIME' not in db_collections:
		create_realtime(db)

	if 'SJ_SEARCH_LOG' not in db_collections:
		db['SJ_SEARCH_LOG']

	if 'SJ_DB_LOG' not in db_collections:
		db['SJ_LOG']

	if 'SJ_VISITOR' not in db_collections:
		db['SJ_VISITOR']

	if 'SJ_USER_BACKUP' not in db_collections:
		db['SJ_USER_BACKUP']

	if 'SJ_NOTICE' not in db_collections:
		db['SJ_NOTICE']

	if 'SJ_FEEDBACK' not in db_collections:
		db['SJ_FEEDBACK']

	if 'SJ_ANALYSIS' not in db_collections:
		db['SJ_ANALYSIS']

	if db_client is not None:
		db_client.close()

#카테고리 컬럼 생성!
def create_category_of_topic(db):
	db[SJ_DB_CATEGORY].insert(
		[
			#대학교
			{
				'category_name': '대학교',
				'info': 
				[
					'sj1_main_founded', 'sj1_main_notice', 'sj1_main_entrance', 'sj1_main_job',  'sj1_main_schoiarship', 'sj1_main_college', 'sj1_main_bidding', 'sj1_main_dataprocessFAQ', 'sj1_main_studentFAQ', 'sj1_main_schoiarshipFAQ', 'sj1_main_foreignerFAQ', 'sj1_main_foreignernotice', 'sj1_main_student', 'sj6_library_notice', 'sj6_library_book', 'sj6_library_FAQ', 'sj7_promotion_article', 'sj7_promotion_prism', 'sj7_promotion_report', 'sj7_promotion_research', 'sj7_promotion_speech', 'sj8_promotion_media', 'sj15_classic_notice', 'sj15_classic_news', 'sj15_classic_creative', 'sj15_classic_event', 'sj15_classic_shp', 'sj17_counselor_notice', 'sj17_counselor_free', 'sj18_skbs_notice', 'sj18_skbs_event', 'sj18_skbs_article', 'sj18_skbs_music', 'sj18_skbs_news', 'sj19_chong_news', 'sj19_chong_notice', 'sj19_chong_lost','sj24_sejong_allie', 'sj29_sejong_dormitory', 'sj33_mobilelibrary_notice', 'sj44_naverblog_sejong', 'sj44_naverblog_campustown'
				],
				'tag': 
				[
					'장학', '사이버강의', '수강', '졸업', '조교', 'faq', '소식', '학사', '국제', '교환학생', '수강편람', '입학', '학술정보원', '입찰', '방송국', '홍보원', '교내', '전화번호부', 'ck사업단', '총학생회', '행복기숙사', '전자도서관', '학사일정', '대양휴머니티칼리지', '에델바이스', '학부', 'kmooc', '블랙보드', 'uis', '학기', '창의', '학술'
				] + 
				[
					'세종대학교', '세종대', '세종인', '휴학', '학교', '연구', '전공', '사업단', '홍보원', '장학금', '기숙사', '도서관', '세사대', '캠퍼스타운', '학위', '캠퍼스'
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
				] + 
				[
					'동호회', '봉사', '아카데미', '학생회', '중앙동아리', '멘토', '멘티', '소모임', 'skbs'
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
				] + 
				[
					'시상식', '상금', '대상', '최우수상', '우수상', '금상', '은상', '동상', '장려상', '아이디어', '예선', '본선', '페스티벌', '강사', '이벤트', '강당', '다과회', '원정대'
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
				] + 
				[
					'포트폴리오', '이력', '이력서', '자소서', '자기소개서', '급여', '연봉', '아르바이트', '파트타임', '사무직', '현장직', '시급', '근무', '근무지', '자격증', '일일직', '노동', '근로', '업종'
				]
			},
			#커뮤니티
			{
				'category_name': '커뮤니티',
				'info': 
				[
					'sj20_sejong_dc', 'sj30_sejongstation_notice', 'sj30_sejongstation_news', 'sj30_sejongstation_free', 'sj30_sejongstation_secret', 'sj30_sejongstation_qna', 'sj30_sejongstation_tip', 'sj30_sejongstation_graduation', 'sj30_sejongstation_job', 'sj30_sejongstation_activity', 'sj30_sejongstation_club', 'sj30_sejongstation_study', 'sj30_sejongstation_food', 'sj30_sejongstation_trade', 'community'
				],
				'tag': 
				[
					'학식', '고민&상담', '종교', '여행', '커뮤니티', '분실물', '연애', '세종냥이', '홍보', '세종대역'
				] + 
				[
					'커뮤니티', '카페', '영화', '독서', '문화', '생활', '개강', '종강'
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
			},
			{
				'category_name': '미사용',
				'info':
				[
					'sj23_everytime_book', 'sj34_everytime_all'
				],
				'tag': []
			}
		])

#카테고리 컬럼 info_num 추가!
def create_category_of_topic_info_num(db):
	#post_info 전체 호출
	post_info_list = db['post_info'].find()
	post_info_list = list(post_info_list)

	#category_of_topic 전체 호출
	category_of_topic_list = db[SJ_DB_CATEGORY].find()
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
		db[SJ_DB_CATEGORY].update(
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

	#수동 info들은 아래의 셋으로 생성
	#manual info set
	manual_info_set = {}
	#-1 = community
	manual_info_set['커뮤니티'] = [-1]

	db[SJ_DB_CATEGORY].update(
		{
			'category_name': '커뮤니티'
		},
		{
			'$push':
			{
				'info_num':
				{
					'$each': manual_info_set['커뮤니티'],
					'$position': 0
				}
			}
		}
	)

#카테고리 컬럼의 tag_vector 추가!
def create_category_of_topic_tag_vector(db):
	#category_of_topic 전체 호출
	category_of_topic_list = db[SJ_DB_CATEGORY].find(
		{
			'category_name': {'$in': list(SJ_CATEGORY_OF_TOPIC_SET)}
		},
		{
			'_id': 0
		}
	)
	category_of_topic_list = list(category_of_topic_list)

	for category in category_of_topic_list:
		category_tag_vector = FastText.get_doc_vector(category['tag']).tolist()

		#category_of_topic 콜렉션에 tag_vectort 추가!
		db[SJ_DB_CATEGORY].update(
			{
				'category_name': category['category_name']
			},
			{
				'$set':
				{
					'tag_vector': category_tag_vector
				}
			}
		)

#정적 테이블 컬럼 생성!
def create_variable(db):
	db[SJ_DB_VARIABLE].insert(
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
			},
			{
				'key': 'main_info_1',
				'value': "세종대학교 정보통합솔루션!"
			},
			{
				'key': 'main_info_2',
				'value': "안녕하세요! SOOJLE입니다."
			},
			{
				'key': 'all_tags',
				'value': ['IT&컴퓨터', '영어', '일본어', '중국어', '취업&진로', '창업', '장학', '행사', '공모전&대외활동', '세미나', '사이버강의', '수강', '멘토링', '모집', '스포츠', '과외&강사', '자취&하숙', '학식', '알바&구인', '동아리&모임', '고민&상담', '독서퀴즈', '봉사', '졸업', '공개채용', '추천채용', '특별채용', '수시채용', '인턴', '계약직', '정규직', '회계', '조교', '디자인', '법무', 'FAQ', '소식', '종교', '공지', '신입생', '학사', '국제', '여행', '교환학생', '수강편람', '게임', '식당', '장터', '카페', '입학', '경력', '신입', '기획', '기술직', '의료직', '교직', '마케팅', '조리직', '서비스직', '해외', '공모전&대외활동', '회계', '학술정보원', '박물관', '입찰', '방송국', '커뮤니티', '음악', '홍보원', '도서', '교내', '전화번호부', '네이버카페', '다음카페', '컴퓨터공학과', '물리천문학과', '영화예술학과', '역사학과', '공과대학', '환경에너지공간융합학과', '소프트웨어학과', '음악과', '만화애니메이션학과', '수학통계학부', '국어문학과', '에너지자원공학과', '화학과', '전자정보공학대학', '기계항공우주공학부', '지능기전공학부', '중국통상학과', '경제통신학과', '데이터사이언스학과', '행정학과', '경영학부', '호텔관광대학', '전자정보통신공학과', '정보보호학과', '나노신소재공학부', '국방시스템공학과', '산업디자인학과', '체육학과', '무용학과', '디자인이노베이션', '법학부', '국제학부', '영어영문학과', '일어일문학과', 'CK사업단', '교육학과', '미디어커뮤니케이션학과', '호텔관광외식경영학부', '호텔외식관광프랜차이즈경영학과', '글로벌조리학과', '생명시스템학부', '식품생명공학과', '바이오융합공학과', '바이오산업자원공학과', '건축공학과', '건축학과', '건축공학부', '기계공학과', '항공우주공학과', '원자력공학과', '항공시스템공학과', '회화과', '패션디자인학과', '총학생회', '분실물', '위키백과', '연애', '세종냥이', '메이플스토리', '카트라이더', '오버워치', '로스트아크', '방탄소년단', '건강', '작곡', '세종알리', '사이트', '행복기숙사', '세종대역', '두드림', '홍보', '전자도서관']
			},
			{
				'key': 'sj_auth_blacklist',
				'value': []
			}
		]
	)

#좋아요/조회수 초기 셋팅용 더비 포스트 생성!
def create_dummy_post(db):
	check_ = check_dummy_post(db)

	if not check_:
		insert_dummy_post(db)

#실시간 검색어 초기 설정
def create_realtime(db):
	db[SJ_DB_REALTIME].insert(
		{
			'real_time' : 
			[
				['세종대', 0.9],
				['장학금', 0.9],
				['학식', 0.9],
				['공모전', 0.9],
				['공결', 0.9],
				['스터디', 0.9],
				['세종사회봉사', 0.9],
				['수강', 0.9],
				['기초코딩', 0.9],
				['학술정보원', 0.9],
				['교양', 0.9],
				['토익', 0.9],
				['동아리', 0.9],
				['야식행사', 0.9],
				['기숙사', 0.9],
				['대양AI센터', 0.9],
				['어린이대공원', 0.9],
				['카페', 0.9],
				['맛집', 0.9],
				['대동제', 0.9]
			],
			'date': datetime.now()
		}
	)