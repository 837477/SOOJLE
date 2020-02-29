#Measurement_run Time (minutes)
SJ_MEASUREMENT_TIME = 30
#Create_Wordcloud_run TIME (days)
SJ_CREATE_WORDCLOUD_TIME = 30
#Realtime_run Time (minutes)
SJ_REALTIME_TIME = 5
#Update_highest_fav_view (day)
SJ_UPDATE_HIGHEST_FAV_VIEW_TIME = 1
#Update_today_time_visitor (hour)
SJ_TIME_VISITOR_ANALYSIS_WORK_TIME = 1

#DB_POST Collection name (현재 포스트 디비 이름)
SJ_DB_POST = "posts"
#FASTTEXT Similarity percent (FT 유사도 비율)
SJ_FASTTEXT_SIM_PERCENT = 0.7
#ALL post return number (모든 포스트 반환 최대 제한)
SJ_RETURN_NUM = 300
#Priority Search limit number (일반 서치 DB호출 최대 제한)
SJ_PS_LIMIT = 10000
#Category Search limit number (카테고리 서치 DB호출 최대 제한) ->10000개로 줄이자.
SJ_CS_LIMIT = 20000
#Newsfeed of Topic limit(토픽별 뉴스피드 DB호출 최대 제한)
SJ_NEWSFEED_TOPIC_LIMIT = 5000
#Recommendation limit (추천뉴스피드 DB호출 최대 제한)
SJ_RECOMMENDATION_LIMIT = 30000
#No Token User Recommendation limit (비로그인 추천뉴스피드 DB호출 최대 제한)
SJ_NO_TOKEN_RECOMMENDATION_LIMIT = 2000
#Log user limit number (사용자 로그 불러오기 최대 제한)
SJ_USER_LOG_LIMIT = 300
#ADMIN Major (관리자 판단용)
SJ_ADMIN = "SOOJLE"
#Realtime Return Limit (실시간 검색어 반환 최대 제한)
SJ_REALTIME_RETURN_LIMIT = 10
#Domain search similarity percent
SJ_DOMAIN_SIM_PERCENT = 0.8
#User cold limit (유저 Cold 기준)
SJ_USER_COLD_LIMIT = 20

#Newsfeed_of_topic 종류
SJ_NEWSFEED_OF_TOPIC_SET = {'대학교', '동아리&모임', '공모전&행사', '진로&구인', '장터', '자유'}

#Recommendation Weight
SJ_TOS_WEIGHT = 1
SJ_TAS_WEIGHT = 1
SJ_FAS_WEIGHT = 1.5
SJ_IS_WEIGHT = 1
SJ_IS_FAV_WEIGHT = 0.75
SJ_IS_VIEW_WEIGHT = 0.25
SJ_RANDOM_WEIGHT = 1.5

#Measurement Weight
SJ_FAV_TAG_WEIGHT = 4
SJ_VIEW_TAG_WEIGHT = 3

SJ_SEARCH_MEASURE_NUM = 100

SJ_FAV_TOPIC_WEIGHT = 45
SJ_VIEW_TOPIC_WEIGHT = 30
SJ_SEARCH_TOPIC_WEIGHT = 10
SJ_NEWSFEED_TOPIC_WEIGHT = 5

SJ_TOPIC_RESULT_DIV = SJ_FAV_TOPIC_WEIGHT + SJ_VIEW_TOPIC_WEIGHT + SJ_SEARCH_TOPIC_WEIGHT + SJ_NEWSFEED_TOPIC_WEIGHT

SJ_TAG_SUM_WEIGHT = 1.5

