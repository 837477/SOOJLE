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
import numpy as np
import jpype
from pymongo import *
from collections import Counter
from operator import itemgetter
from tzlocal import get_localzone
from datetime import timedelta, datetime
###################################################
import LDA
import FastText
from db_management import *
from db_info import *
from tknizer import get_tk
from variable import *
from global_func import get_default_day

#관심도 측정.ver2
def SJ_interest_measurement_run():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	renewal_time = find_variable(db, 'renewal')

	USER_list = find_user_renewal(db, renewal_time)
	USER_list = list(USER_list)

	ACTION_DAY_CHECK = get_default_day(SJ_USER_ACTION_DAY_CHECK)

	CATEGORY_list = find_all_category_of_topic(db)
	CATEGORY_list = list(CATEGORY_list)
	CATEGORY = {}
	#뉴스피드 관심도 태그 구하기에서 빠른 접근을 위해서 dict형식으로 변환
	for cate in CATEGORY_list:
		CATEGORY[cate['category_name']] = cate['tag']

	for USER in USER_list:
		#좋아요/조회수가 하나도 없는 회원은 측정 안함.
		if (len(USER['fav_list']) == 0) and (len(USER['view_list']) == 0):
			continue
		
		user_log_backup(db, USER)

		fav_tag = []
		view_tag = []
		newsfeed_tag = []
		fav_token = []
		view_token = []
		search_list = []

		#사용자가 관심 기능을 수행한 게시물 ##########################
		fav_topic = (np.zeros(LDA.NUM_TOPICS))
		if len(USER['fav_list']) <= SJ_USER_LOG_LIMIT['fav'] * SJ_USER_ACTION_NUM_CHECK_PERCENT: 
			for fav in USER['fav_list']:
				fav_topic += fav['topic']
				fav_tag += fav['tag']
				fav_token += fav['token']
		else:
			for fav in USER['fav_list']:
				if fav['date'] < ACTION_DAY_CHECK: continue
				fav_topic += fav['topic']
				fav_tag += fav['tag']
				fav_token += fav['token']

		#FAS 구하기
		fav_doc = (fav_tag + fav_token) * 2

		#사용자가 접근을 수행한 게시물 ##############################
		view_topic = (np.zeros(LDA.NUM_TOPICS))
		if len(USER['view_list']) <= SJ_USER_LOG_LIMIT['view'] * SJ_USER_ACTION_NUM_CHECK_PERCENT: 
			for view in USER['view_list']:
				view_topic += view['topic']
				view_tag += view['tag']
				view_token += view['token']
		else:
			for view in USER['view_list']:
				if view['date'] < ACTION_DAY_CHECK: continue
				view_topic += view['topic']
				view_tag += view['tag']
				view_token += view['token']

		#FAS 구하기
		view_doc = view_tag + view_token

		#사용자가 검색을 수행한 키워드 ##############################
		if len(USER['search_list']) <= SJ_USER_LOG_LIMIT['search'] * SJ_USER_ACTION_NUM_CHECK_PERCENT:
			for search in USER['search_list']:
				search_list += search['tokenizer_split']
		else:
			for search in USER['search_list']:
				if search['date'] < ACTION_DAY_CHECK: continue
				search_list += search['tokenizer_split']
		
		search_topic = LDA.get_topics(search_list)
		search_doc = search_list

		#사용자가 접근한 뉴스피드 ################################
		A_NUM = 0 #대학교
		B_NUM = 0 #동아리&모임
		C_NUM = 0 #공모전&행사
		D_NUM = 0 #진로&구인
		E_NUM = 0 #자유

		if len(USER['newsfeed_list']) <= SJ_USER_LOG_LIMIT['newsfeed'] * SJ_USER_ACTION_NUM_CHECK_PERCENT:
			for newsfeed in USER['newsfeed_list']:
				if newsfeed['newsfeed_name'] == '대학교': A_NUM += 1
				elif newsfeed['newsfeed_name'] == '동아리&모임': B_NUM += 1
				elif newsfeed['newsfeed_name'] == '공모전&행사': C_NUM += 1
				elif newsfeed['newsfeed_name'] == '진로&구인': D_NUM += 1
				else: E_NUM += 1
		else:
			for newsfeed in USER['newsfeed_list']:
				if newsfeed['date'] < ACTION_DAY_CHECK: continue

				if newsfeed['newsfeed_name'] == '대학교': A_NUM += 1
				elif newsfeed['newsfeed_name'] == '동아리&모임': B_NUM += 1
				elif newsfeed['newsfeed_name'] == '공모전&행사': C_NUM += 1
				elif newsfeed['newsfeed_name'] == '진로&구인': D_NUM += 1
				else: E_NUM += 1

				newsfeed_tag += newsfeed['tag']
		
		newsfeed_tag += (CATEGORY['대학교'] * A_NUM) + (CATEGORY['동아리&모임'] * B_NUM) + (CATEGORY['공모전&행사'] * C_NUM) + (CATEGORY['진로&구인'] * D_NUM) + (CATEGORY['커뮤니티'] * E_NUM)

		newsfeed_topic = LDA.get_topics(newsfeed_tag)


		#가중치 작업
		fav_tag *= SJ_FAV_TAG_WEIGHT
		view_tag *= SJ_VIEW_TAG_WEIGHT
		
		fav_topic *= SJ_FAV_TOPIC_WEIGHT
		view_topic *= SJ_VIEW_TOPIC_WEIGHT
		search_topic *= SJ_SEARCH_TOPIC_WEIGHT
		newsfeed_topic *= SJ_NEWSFEED_TOPIC_WEIGHT

		if len(USER['fav_list']) != 0:
			fav_topic /= len(USER['fav_list'])
		
		if len(USER['view_list']) != 0:
			view_topic /= len(USER['view_list'])

		#LDA Topic
		TOPIC_RESULT = (fav_topic + view_topic + search_topic + newsfeed_topic)/SJ_TOPIC_RESULT_DIV

		#FASTTEXT
		FastText_doc = fav_doc + view_doc + search_doc

		if FastText_doc:
			USER_VERCTOR = FastText.get_doc_vector(fav_doc + view_doc + search_doc).tolist()
		else:
			USER_VERCTOR = ft_vector = (np.zeros(FastText.VEC_SIZE)).tolist()
			
		#TAG
		tag_dict = dict(Counter(fav_tag + view_tag))
		tag_dict = sorted(tag_dict.items(), key=lambda x: x[1])

		#최종 태그들 오브젝트
		TAG_RESULT = {}

		if len(tag_dict) >= 50:
			if tag_dict[0][1] == 1:
				tag_dict[0][1] = 2

			TAG_RESULT[tag_dict[0][0]] = tag_dict[0][1]

			for i in range(1, 50):
				tag_dict[i] = list(tag_dict[i])
	
				if (tag_dict[i-1][1] * 1.5) < tag_dict[i][1]:
					tag_dict[i][1] = int(tag_dict[i-1][1] * 1.5)
				
				TAG_RESULT[tag_dict[i][0]] = tag_dict[i][1]
		
		elif len(tag_dict) > 0:
			if tag_dict[0][1] == 1:
				tag_dict[0][1] = 2

			TAG_RESULT[tag_dict[0][0]] = tag_dict[0][1]

			for i in range(1, len(tag_dict)):
				tag_dict[i] = list(tag_dict[i])

				if (tag_dict[i-1][1] * 1.5) < tag_dict[i][1]:
					tag_dict[i][1] = int(tag_dict[i-1][1] * 1.5)

				TAG_RESULT[tag_dict[i][0]] = tag_dict[i][1]

		USER_TAG_SUM = sum(TAG_RESULT.values())

		USER_TAG_SUM *= SJ_TAG_SUM_WEIGHT

		if USER_TAG_SUM == 0:
			USER_TAG_SUM = 1

		# 사용자 태그로 사용자 태그 벡터 구하기
		USER_TAGS = []
		for key,value in TAG_RESULT.items():
			USER_TAGS += [key] * value
		TAG_VECTOR = FastText.get_doc_vector(USER_TAGS).tolist()

		#해당 USER 관심도 갱신!
		update_user_measurement(db, USER['_id'], list(TOPIC_RESULT), TAG_RESULT, USER_TAG_SUM, TAG_VECTOR, USER_VERCTOR, len(USER['fav_list']) + len(USER['view_list']) + len(USER['search_list']))

	update_variable(db, 'renewal', datetime.now())

	if db_client is not None:
		db_client.close()

#사용자 로그 액션 백업
def user_log_backup(db, USER):
	#fav
	if len(USER['fav_list']) > SJ_USER_LOG_LIMIT['fav']:
		#SJ_USER_LOG_LIMIT개로 다시 갱신!
		update_user_action_log_refresh(db, USER['_id'], 'fav', USER['fav_list'][:SJ_USER_LOG_LIMIT['fav']])
		#SJ_BACKUP 으로 이전!
		insert_user_backup(db, USER['user_id'], 'fav', USER['fav_list'][SJ_USER_LOG_LIMIT['fav']:])

	#view
	if len(USER['view_list']) > SJ_USER_LOG_LIMIT['view']:
		#SJ_USER_LOG_LIMIT개로 다시 갱신!
		update_user_action_log_refresh(db, USER['_id'], 'view', USER['view_list'][:SJ_USER_LOG_LIMIT['view']])
		#SJ_BACKUP 으로 이전!
		insert_user_backup(db, USER['user_id'], 'view', USER['view_list'][SJ_USER_LOG_LIMIT['view']:])

	#search
	if len(USER['search_list']) > SJ_USER_LOG_LIMIT['search']:
		#SJ_USER_LOG_LIMIT개로 다시 갱신!
		update_user_action_log_refresh(db, USER['_id'], 'search', USER['search_list'][:SJ_USER_LOG_LIMIT['search']])
		#SJ_BACKUP 으로 이전!
		insert_user_backup(db, USER['user_id'], 'search', USER['search_list'][SJ_USER_LOG_LIMIT['search']:])

	#newsfeed
	if len(USER['newsfeed_list']) > SJ_USER_LOG_LIMIT['newsfeed']:
		#SJ_USER_LOG_LIMIT개로 다시 갱신!
		update_user_action_log_refresh(db, USER['_id'], 'newsfeed', USER['newsfeed_list'][:SJ_USER_LOG_LIMIT['newsfeed']])
		#SJ_BACKUP 으로 이전!
		insert_user_backup(db, USER['user_id'], 'newsfeed', USER['newsfeed_list'][SJ_USER_LOG_LIMIT['newsfeed']:])


if __name__ == '__main__':
	FILE = open('/home/iml/log/background.log', 'a')
	#FILE = open('background.log', 'a')
	
	try:
		SJ_interest_measurement_run()
		log_data = str(datetime.now()) + " ::: 관심도 측정 성공 :)  \n"
    
	except Exception as ex:
		log_data = str(datetime.now()) + " ::: 관심도 측정 실패 :(  \n" + str(ex) + "\n"

	FILE.write(log_data)

	FILE.close()
