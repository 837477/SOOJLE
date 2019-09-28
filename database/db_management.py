from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from global_func import *
from datetime import datetime, timedelta

#######################################################
#사용자 관련#############################################
#전체 유저 목록 반환 (원하는 필드를 1하면 그 필드들만 반환됨)
def find_all_user(db, _id=None, user_id=None, user_name=None, user_major=None, topic=None, tag=None, fav_list=None):
	
	show_dict = {'_id': 0}
	if _id is not None:
		show_dict['_id'] = 1
	if user_id is not None:
		show_dict['user_id'] = 1
	if user_name is not None:
		show_dict['user_name'] = 1
	if user_major is not None:
		show_dict['user_major'] = 1
	if topic is not None:
		show_dict['topic'] = 1
	if tag is not None:
		show_dict['tag'] = 1
	if fav_list is not None:
		show_dict['fav_list'] = 1

	result = db['user'].find({}, show_dict)

	return dumps(result)

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

#특정 유저 similarity 불러오기
def find_user_similarity(db, user_id):
	result = db['user'].find_one({'user_id': user_id}, {'similarity': 1})
	return result['similarity']

#유저와 문서의 유사도 갱신
def update_user_post_similarity(db, user_id, similarity):
	db['user'].update({'_id': ObjectId(user_id)}, {'$set': {'similarity': similarity}})
	return "success"

#유저가 접근한 게시물 갱신
def update_post_user_access(db, user_id, access_obj):
	item = []
	item.append(access_obj)

	db['user'].update({'user_id': user_id}, {'item': item})

	return "success"
#######################################################
#뉴스피드 관련############################################
#각각의 뉴스피드 반환 (공지, 알바구인 등등)
def find_newsfeed(db, type, tags, date, pagenation, page):
	result = db['test_posts1'].find({'$or': [{'tag': {'$in': tags}}, {'date': {'$lte': date}}]}).skip((page-1)*pagenation).limit(page*pagenation)
	return result

#인기 뉴스피드
def find_popularity_newsfeed(db, num):
	result = db['test_posts1'].find({}).sort([('date', -1)]).limit(num).sort([('interests', -1)])
	return result

#추천 뉴스피드
def find_recommendation_newsfeed(db, sort_similarity):
	result = db['test_posts1'].find({'$or': sort_similarity})
	return dumps(result)

#######################################################
#포스트 관련#############################################
#포스트 전체 가져오기 (가져오고 싶은 필드만 1로 지정하여 보내주면 됨)
def find_all_posts(db, _id=None, title=None, date=None, post=None, tag=None, img=None, url=None, hashed=None, info=None, view=None, fav_cnt=None, title_token=None, token=None, topic=None, interests=None, skip_=0, limit_=None):

	show_dict = {'_id': 0}

	if _id is not None:
		show_dict['_id'] = 1
	if title is not None:
		show_dict['title'] = 1
	if date is not None:
		show_dict['date'] = 1
	if post is not None:
		show_dict['post'] = 1
	if tag is not None:
		show_dict['tag'] = 1
	if img is not None:
		show_dict['img'] = 1
	if url is not None:
		show_dict['url'] = 1
	if hashed is not None:
		show_dict['hashed'] = 1
	if info is not None:
		show_dict['info'] = 1
	if view is not None:
		show_dict['view'] = 1
	if fav_cnt is not None:
		show_dict['fav_cnt'] = 1
	if title_token is not None:
		show_dict['title_token'] = 1
	if token is not None:
		show_dict['token'] = 1
	if topic is not None:
		show_dict['topic'] = 1
	if interests is not None:
		show_dict['interests'] = 1

	if limit_ is None:
		#기본적으로 날짜순 정렬 (최신)
		result = db['test_posts1'].find({}, show_dict).sort([('date', -1)]).skip(skip_)
	else:
		#기본적으로 날짜순 정렬 (최신)
		result = db['test_posts1'].find({}, show_dict).sort([('date', -1)]).skip(skip_).limit(limit_)

	return dumps(result)

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

###############################################
#variable###################################### 
#정적 테이블 변수 불러오기
def find_variable(db, key):
	result = db['variable'].find_one({'key': key}, {'value':1})
	return result['value']

#정적 테이블 변수 수정하기
def update_variable(db, key, value):
	db['variable'].update({'key': key}, {'$set': {'value': value }})
	return "success"

#조회수 랭킹1위 수 갱신
def update_posts_highest_view(db):
	highest_view = db['test_posts1'].find({}, {'view': 1}).sort([('view', -1)]).limit(1)
	highest_view = list(highest_view)[0]['view']

	highest_view_id = db['variable'].find_one({'key': 'highest_view'}, {'_id': 1})

	if highest_view_id is None:
		db['variable'].insert({'key': 'highest_view', 'value': 0})
		highest_view_id = db['variable'].find_one({'key': 'highest_view'}, {'_id': 1})

	db['variable'].update({'_id': ObjectId(highest_view_id['_id'])}, {'$set': {'value': highest_view}})

	return "success"

#좋아요 랭킹1위 수 갱신
def update_posts_highest_fav_cnt(db):
	highest_fav_cnt = db['test_posts1'].find({}, {'fav_cnt':1}).sort([('fav_cnt', -1)]).limit(1)
	highest_fav_cnt = list(highest_fav_cnt)[0]['fav_cnt']

	highest_fav_cnt_id = db['variable'].find_one({'key': 'highest_fav_cnt'}, {'_id': 1})

	if highest_fav_cnt_id is None:
		db['variable'].insert({'key': 'highest_fav_cnt', 'value': 0})
		highest_fav_cnt_id = db['variable'].find_one({'key': 'highest_fav_cnt'}, {'_id': 1})

	db['variable'].update({'_id': ObjectId(highest_fav_cnt_id['_id'])}, {'$set': {'value': highest_fav_cnt}})
	
	return "success"	