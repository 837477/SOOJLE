from bson.objectid import ObjectId
from global_func import *
from datetime import datetime, timedelta
import pymongo

#######################################################
#사용자 관련#############################################
#전체 유저 목록 반환 (id만)
def find_all_user(db):
	result = db['user'].find({}, {'_id': 1})
	return list(result)

#유저 생성
def insert_user(db, user_id, user_pw, user_name, user_major):
	result = db['user'].insert({'user_id': user_id, 'user_pw': user_pw, 'user_name': user_name, 'user_major': user_major})
	return "success"

#특정 유저 찾기
def find_user(db, user_id):
	result = db['user'].find_one({'user_id': user_id}, {'_id': 0, 'user_id': 1, 'user_pw': 1, 'user_name': 1, 'user_major': 1})
	return result

#특정 유저 토픽 불러오기
def find_user_topic(db, user_id):
	result = db['user'].find_one({'_id': ObjectId(user_id)}, {'_id':0, 'topic':1})
	return result['topic']

#특정 유저 태그 불러오기
def find_user_tag(db, user_id):
	result = db['user'].find_one({'_id': ObjectId(user_id)}, {'_id':0, 'tag':1})
	return result['tag']

#유저와 문서의 유사도 갱신
def update_user_post_similarity(db, user_id, similarity):
	db['user'].update({'_id': ObjectId(user_id)}, {'similarity': similarity})
	return "success"

#######################################################
#뉴스피드 관련############################################
def find_newsfeed(db, type, tags, date, pagenation, page):
	result = db['test_posts1'].find({'$or': [{'tag': {'$in': tags}}, {'date': {'$lte': date}}]}).skip((page-1)*pagenation).limit(page*pagenation)
	return result

def find_recommendation_newsfeed(db, num):
	now_date = datetime.now()
	date = now_date + timedelta(days=-90)
	result = db['test_posts1'].find({'date': {'$gte': date}}).sort([('interests', -1)]).limit(num)
	return result

#######################################################
#포스트 관련#############################################
#포스트 전체 가져오기(post_obi만 가져옴.)
def find_all_posts(db):
	result = db['test_posts1'].find({}, {'_id': 1})
	return list(result)

#포스트 좋아요
def update_post_like(db, post_obi):
	db['posts'].update({'_id': ObjectId(post_obi)}, {'$inc': {'fav_cnt': 1}})
	return "success"

#포스트 좋아요 취소
def update_post_unlike(db, post_obi):
	db['posts'].update({'_id': ObjectId(post_obi)}, {'$inc': {'fav_cnt': -1}})
	return "success"

#포스트 조회수 올리기
def update_post_view(db, post_obi):
	db['posts'].update({'_id': ObjectId(post_obi)}, {'$inc': {'view': 1}})
	return "success"

#단일 포스트 조회수 불러오기
def find_post_view(db, post_obi):
	result = db['test_posts1'].find_one({'_id': ObjectId(post_obi)}, {'_id':0, 'view':1})
	return result['view']

#단일 포스트 토픽 목록 불러오기
def find_post_topic(db, post_obi):
	result = db['test_posts1'].find_one({'_id': ObjectId(post_obi)}, {'_id':0, 'topic':1})
	return result['topic']

#단일 포스트 태그 목록 불러오기
def find_post_tag(db, post_obi):
	result = db['test_posts1'].find_one({'_id': ObjectId(post_obi)}, {'_id':0, 'tag':1})
	return result['tag']

#단일 포스트 좋아요 수 불러오기
def find_post_fav_cnt(db, post_obi):
	result = db['test_posts1'].find_one({'_id': ObjectId(post_obi)}, {'_id':0, 'fav_cnt':1})
	return result['fav_cnt']