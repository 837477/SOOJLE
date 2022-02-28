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
import re
from pymongo import *
from collections import Counter
from operator import itemgetter
from datetime import timedelta, datetime
###################################################
from db_management import *
from db_info import *
from variable import *

#실시간 검색어 함수 preprocess
def preprocess(doc):
	emoji_pattern = re.compile("["
		u"\U0001F600-\U0001F64F"  # emoticons
		u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		u"\U0001F680-\U0001F6FF"  # transport & map symbols
		u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		"]+", flags=re.UNICODE)
	doc = re.sub(r'\s+'," ", doc)
	doc = doc.lower()
	doc = re.sub(r'[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', doc)
	doc = emoji_pattern.sub(r'', doc)
	doc = re.compile('[^ ㄱ-ㅣ가-힣|a-z]+').sub('', doc)
	return doc

#실시간 검색어 추출 함수
def real_time_keywords(search_input):
	temp = [i['search_split'] for i in search_input]
	check_list = []
	for i in range(len(temp)):
		temp_word = []
		for j in range(len(temp[i])):
			temp[i][j] = preprocess(temp[i][j])
			if len(temp[i][j]) > 1: temp_word.append(temp[i][j])
		check_list.append(temp_word)
	
	result = {}
	for words in check_list:
		# 단일 단어 추가
		for i in range(len(words)):
			if words[i] in result: result[words[i]] += 1
			else: result[words[i]] = 1
		
		# 연속 단어 추가(정방향)
		for i in range(2,len(words)):
			key = " ".join(words[0:i+1])
			if key in result: result[key] += 1
			else: result[key] = 1

	result = sorted(result.items(), key = itemgetter(0))
	temp = []
	for i in range(len(result)-1):
		if ((result[i+1][0].startswith(result[i][0]) or result[i+1][0].endswith(result[i][0])) and result[i+1][1] >= result[i][1]): 
			continue
		temp.append(result[i])
	result = sorted(temp, key = lambda x: len(x[0]))   
	result = sorted(result, key = itemgetter(1), reverse = True)
	return result

#실시간 검색어 캐싱 함수
def SJ_realtime_insert():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	search_log_list = find_search_log(db)
	search_log_list = list(search_log_list)
	
	real_time_keywords_temp = real_time_keywords(search_log_list)

	#최근에 검색어가 0개 이면, 애초에 캐싱을 안하고 함수 종료.
	if len(real_time_keywords_temp) == 0:
		return False

	#욕 필터링
	realtime_result = []
	for keyword in real_time_keywords_temp:
		if keyword in SJ_BAD_LANGUAGE:
			continue
		
		elif len(keyword) > 10:
			continue

		realtime_result.append(keyword)

	if len(realtime_result) < SJ_REALTIME_LIMIT:
		lately_realtime = find_search_realtime(db)
		lately_realtime = list(lately_realtime)
		lately_realtime = lately_realtime[0]['real_time']
		
		realtime_result.sort(key=lambda x:x[1], reverse=True)
		lately_realtime.sort(key=lambda x:x[1], reverse=True)

		#가장 작은 값 찾기
		min_value = realtime_result[len(realtime_result) - 1][1]
		min_value -= 0.1

		#중복 키 찾기
		duple_key_list = list(set(dict(realtime_result)) & set(dict(lately_realtime)))
		
		#실시간 검색어 최종 리스트에 저번 리스트 순위를 추가하는 작업
		for lately in lately_realtime:
			check = True

			for duple_key in duple_key_list:
				if lately[0] == duple_key:
					check = False
			
			if check:
				realtime_result.append([lately[0], min_value])

			if len(realtime_result) == SJ_REALTIME_LIMIT:
				break
			
	insert_search_realtime(db, realtime_result[:SJ_REALTIME_LIMIT])
	
	if db_client is not None:
		db_client.close()

if __name__ == '__main__':
	FILE = open('/home/iml/log/background.log', 'a')
	#FILE = open('background.log', 'a')
	
	try:
		SJ_realtime_insert()
		log_data = str(datetime.now()) + " ::: 실시간 검색어 캐싱 성공 :)  \n"
    
	except Exception as ex:
		log_data = str(datetime.now()) + " ::: 실시간 검색어 캐싱 실패 :(  \n" + str(ex) + "\n"

	FILE.write(log_data)

	FILE.close()
