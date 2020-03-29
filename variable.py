#백그라운드 시간
#####################################################
#Measurement_run Time (hours)
SJ_MEASUREMENT_TIME = 2
#Create_Wordcloud_run TIME (days)
SJ_CREATE_WORDCLOUD_TIME = 30
#Realtime_run Time (minutes)
SJ_REALTIME_TIME = 5
#Update_highest_fav_view (day)
SJ_UPDATE_HIGHEST_FAV_VIEW_TIME = 1
#Update_today_time_visitor (hour)
SJ_TIME_VISITOR_ANALYSIS_WORK_TIME = 1

#DB콜렉션 명
#####################################################
#DB_POST Collection name (현재 포스트 디비 이름)
SJ_DB_POST = "posts"
SJ_DB_REALTIME = "SJ_REALTIME"
SJ_DB_USER = "SJ_USER"
SJ_DB_VARIABLE = "SJ_VARIABLE"
SJ_DB_LOG = "SJ_LOG"
SJ_DB_SEARCH_LOG = "SJ_SEARCH_LOG"
SJ_DB_ANALYSIS = "SJ_ANALYSIS"
SJ_DB_USER_BACKUP = "SJ_USER_BACKUP"
SJ_DB_NOTICE = "SJ_NOTICE"
SJ_DB_CATEGORY = "SJ_CATEGORY"
SJ_DB_VISITOR = "SJ_VISITOR"
SJ_DB_FEEDBACK = "SJ_FEEDBACK"

#상수 변수들
#####################################################
#FASTTEXT Similarity percent (FT 유사도 비율)
SJ_FASTTEXT_SIM_PERCENT = 0.7
#ALL post return number (모든 포스트 반환 최대 제한)
SJ_RETURN_NUM = 300
#Priority Search limit number (일반 서치 DB호출 최대 제한)
SJ_PS_LIMIT = 10000
#Category Search limit number (카테고리 서치 DB호출 최대 제한)
SJ_CS_LIMIT = 5000
#Newsfeed of Topic limit(토픽별 뉴스피드 DB호출 최대 제한)
SJ_NEWSFEED_TOPIC_LIMIT = 2000
#No Token User Recommendation limit (비로그인 추천뉴스피드 DB호출 최대 제한)
SJ_NO_TOKEN_RECOMMENDATION_LIMIT = 500
#Category Search Default Date (카테고리 디폴트 데이트 설정, 일 단위)
SJ_CS_DEFAULT_DATE = 365
#Log user limit number (사용자 로그 불러오기 최대 제한)
SJ_USER_LOG_LIMIT = {
	'view': 100,
	'search': 40,
	'fav': 20,
	'newsfeed': 30
}
#실시간 검색 리미트
SJ_REALTIME_LIMIT = 20
#Realtime Return Limit (실시간 검색어 반환 최대 제한)
SJ_REALTIME_RETURN_LIMIT = 10
#Domain search similarity percent
SJ_DOMAIN_SIM_PERCENT = 0.8
#User cold limit (유저 Cold 기준)
SJ_USER_COLD_LIMIT = 20
#Request length limit (사용자 전송 글자수 제한) (이상, 이하 제도)
SJ_REQUEST_LENGTH_LIMIT = {
	'search_max': 200,
	'user_id_min': 6,
	'user_id_max': 30,
	'user_pw_max': 8,
	'user_nickname_min': 1,
	'user_nickname_max': 16,
	'feedback_max': 1000,
	'notice_title_min': 1,
	'notice_title_max': 50,
	'notice_post_min': 1,
	'notice_post_max': 1000,
	'main_info_max': 50
}

#스트링 변수들
#####################################################
#Newsfeed_of_topic 종류
SJ_NEWSFEED_OF_TOPIC_SET = {'대학교', '동아리&모임', '공모전&행사', '진로&구인', '장터', '자유'}
#Category_of_topic 종류
SJ_CATEGORY_OF_TOPIC_SET = {'대학교', '동아리&모임', '공모전&행사', '진로&구인', '자유'}
#욕 필터 셋
SJ_BAD_LANGUAGE = {'페미', '냄져', '한남', '자댕이', '조팔', '씨발', '섹스', '개년', '개새끼', '씹', '셋스', '느개비', '좆', '노무현', "느개비", '느금마', '니애미', '빠구리', '시발년' ,'시발새끼', '느그앰', '느그미', '노무혐', '빠9리', '시발롬', '시발련', '창년', '보빨러', '사까시', '걸레년', '걸레련', '보빨', '4카시', '사카시', '봊', '보전깨', '니미', '오피누', '오피녀', '이기야', '놈딱', '북딱', '지잡', '십색기', '십색갸', '십색꺄', '일배', '일베', '일간베스트', 'ㅈ같', '보들', '자들', '섹종', '섺종', '땅끄', '땅크', '씹년', '훌짓', '섺끈', '세끈', '섹끈', '섻', '섹ㅅ', 'ㅂㅅ', 'ㅅ발', 'ㅈ밥', 'ㅂ신', '시팔', '색기', '니엄', '니앰', 'ㅆ발', 'ㅆㅂ', '무현', '부랄', '붕알', '족같', 'ㅈㄹ', 'ㅅㅂ', 'ㅈㄹ', '쎅스', '섻스', '갈보', '빙신', '병신', '걸레', '콘돔', '보빨', '걸레', '창년', '느금', '놈현', '응디', '딱좋', '틀딱', '엠창', '니미', '시팔', '씨팔', '빨통', '등신', '모텔', '잠지', '보지', '시발', '셋스', '후빨', '홍어', '창녀', '애비', '애미', '개년', '썅'}
#ADMIN Major (관리자 판단용)
SJ_ADMIN = "SOOJLE"

#Recommendation Weight
#####################################################
SJ_TOS_WEIGHT = 1
SJ_TAS_WEIGHT = 1
SJ_FAS_WEIGHT = 1
#SJ_IS_WEIGHT = 1
#SJ_IS_FAV_WEIGHT = 0.75
#SJ_IS_VIEW_WEIGHT = 0.25
SJ_RANDOM_WEIGHT = 1

SJ_RECOMMENDATION_POST_NUM = 500
SJ_RECOMMENDATION_POST_WEIGHT = 150
SJ_RECOMMENDATION_POST_MINUS_WEIGHT = -75

#추천뉴스피드의 디폴트 데이트
SJ_RECOMMENDATION_DEFAULT_DATE = 60

#각 카테고리를 지정된 갯수만큼 자르기
SJ_RECOMMENDATION_CATEGORY_POST_NUM = [70, 28, 28, 28, 18]

#Measurement Weight
#####################################################
SJ_FAV_TAG_WEIGHT = 4
SJ_VIEW_TAG_WEIGHT = 3

SJ_FAV_TOPIC_WEIGHT = 35
SJ_VIEW_TOPIC_WEIGHT = 30
SJ_SEARCH_TOPIC_WEIGHT = 25
SJ_NEWSFEED_TOPIC_WEIGHT = 10

SJ_TOPIC_RESULT_DIV = SJ_FAV_TOPIC_WEIGHT + SJ_VIEW_TOPIC_WEIGHT + SJ_SEARCH_TOPIC_WEIGHT + SJ_NEWSFEED_TOPIC_WEIGHT

SJ_TAG_SUM_WEIGHT = 1.5

SJ_USER_ACTION_NUM_CHECK_PERCENT = 0.15
SJ_USER_ACTION_DAY_CHECK = 30