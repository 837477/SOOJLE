from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from datetime import datetime, timedelta
#####################################
from global_func import *
#####################################

#######################################################
#사용자 관련#############################################
#전체 유저 목록 반환
def find_all_user(db, _id=None, user_id=None, user_name=None, user_major=None, topic=None, tag=None, fav_list=None, view_list=None, search_list=None, tag_sum=None, newsfeed_list=None):
	
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
	if tag_sum is not None:
		show_dict['tag_sum'] = 1
	if fav_list is not None:
		show_dict['fav_list'] = 1
	if view_list is not None:
		show_dict['view_list'] = 1
	if search_list is not None:
		show_dict['search_list'] = 1
	if newsfeed_list is not None:
		show_dict['newsfeed_list'] = 1

	result = db['user'].find({}, show_dict)

	return result

#특정 유저, 특정 필드 목록 반환
def find_user(db, _id=None, user_id=None, user_pw=None, user_name=None, user_major=None, topic=None, tag=None, fav_list=None, view_list=None, search_list=None, tag_sum=None, newsfeed_list=None):
	
	show_dict = {'_id': 0}
	if _id is not None:
		show_dict['_id'] = 1
	if user_id is not None:
		show_dict['user_id'] = 1
	if user_pw is not None:
		show_dict['user_pw'] = 1
	if user_name is not None:
		show_dict['user_name'] = 1
	if user_major is not None:
		show_dict['user_major'] = 1
	if topic is not None:
		show_dict['topic'] = 1
	if tag is not None:
		show_dict['tag'] = 1
	if tag_sum is not None:
		show_dict['tag_sum'] = 1
	if fav_list is not None:
		show_dict['fav_list'] = 1
	if view_list is not None:
		show_dict['view_list'] = 1
	if search_list is not None:
		show_dict['search_list'] = 1
	if newsfeed_list is not None:
		show_dict['newsfeed_list'] = 1

	result = db['user'].find_one({'user_id': user_id}, show_dict)

	return result

#유저 생성
def insert_user(db, user_id, user_pw, user_name, user_major):
	result = db['user'].insert({'user_id': user_id, 'user_pw': user_pw, 'user_name': user_name, 'user_major': user_major})
	return "success"

#유저 관심도 초기화
def update_unset_user_interest(db, _id):
	db['user'].update({'_id': ObjectId(_id)}, {'$unset': {'fav_list':1, 'view_list':1, 'search_list':1 }})
	return "success"

#유저 fav_list에 요소 추가
def update_user_fav_list_push(db, _id, fav_obj):
	db['user'].update(
		{'_id': ObjectId(_id)},
		{'$push': {'fav_list': fav_obj}}
	)

	return "success"

#유저 fav_list에 요소 삭제 (좋아요 취소한 경우)
def update_user_fav_list_pull(db, _id, fav_obj_id):
	db['user'].update(
		{'_id': _id},
		{'$pull': {'fav_list': {'_id': fav_obj_id}}}
	)
	return "success"

#유저 fav_list 중복 체크용
def check_user_fav_list(db, _id, fav_obj_id):
	result = db['user'].find_one(
		{'_id': _id}, 
		{'fav_list': {'$elemMatch': {'_id': ObjectId(fav_obj_id)}}}
	)
	return result

#유저 view_list에 요소 추가
def update_user_view_list_push(db, _id, view_obj):
	db['user'].update(
		{'_id': ObjectId(_id)},
		{'$push': {'view_list': view_obj}}
	)
	return "success"

#유저 search_list에 요소 추가
def update_user_search_list_push(db, _id, search_keyword):
	db['user'].update(
		{'_id': ObjectId(_id)},
		{'$push': {'search_list': {'$each': search_keyword}}}
	)
	return "success"

#######################################################
#검색 관련###############################################
def find_token(db, token_list):
	result = db['test_posts5'].find({'$or': [ {'title_token': {'$in': token_list}}, {'token': {'$in': token_list}}, {'tag': {'$in': token_list}} ]}, {'_id':0, 'title':1}).limit(200)
	return result

#######################################################
#뉴스피드 관련############################################
#토픽별 뉴스피드 반환
def find_newsfeed(db, type, tags, date, pagenation, page):
	result = db['test_posts5'].find({'$or': [{'tag': {'$in': tags}}, {'date': {'$lte': date}}]}).skip((page-1)*pagenation).limit(page*pagenation)
	return result

#인기 뉴스피드
def find_popularity_newsfeed(db, num):
	result = db['test_posts5'].find({}, {'_id':0, 'post':0}).sort([('date', -1)]).limit(num).sort([('popularity', -1)])
	return result

#######################################################
#포스트 관련#############################################
#포스트 전체 가져오기
def find_all_posts(db, _id=None, title=None, date=None, post=None, tag=None, img=None, url=None, hashed=None, info=None, view=None, fav_cnt=None, title_token=None, token=None, topic=None, popularity=None, interests=None, skip_=0, limit_=None):

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
	if popularity is not None:
		show_dict['popularity'] = 1
	if interests is not None:
		show_dict['interests'] = 1

	if limit_ is None:
		#기본적으로 날짜순 정렬 (최신)
		result = db['test_posts5'].find({}, show_dict).sort([('date', -1)]).skip(skip_)

	else:
		#기본적으로 날짜순 정렬 (최신)
		result = db['test_posts5'].find({}, show_dict).sort([('date', -1)]).skip(skip_).limit(limit_)

	return result

#특정 포스트 가져오기 (가져오고 싶은 필드만 1로 지정하여 보내주면 됨)
def find_post(db, post_obi, _id=None, title=None, date=None, post=None, tag=None, img=None, url=None, hashed=None, info=None, view=None, fav_cnt=None, title_token=None, token=None, topic=None, popularity=None, interests=None):

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
	if popularity is not None:
		show_dict['popularity'] = 1
	if interests is not None:
		show_dict['interests'] = 1

	result = db['test_posts5'].find_one({'_id': ObjectId(post_obi)}, show_dict)

	return result

#포스트 좋아요
def update_post_like(db, post_obi):
	db['test_posts5'].update({'_id': ObjectId(post_obi)}, {'$inc': {'fav_cnt': 1, 'popularity': 3}})

	return "success"

#포스트 좋아요 취소
def update_post_unlike(db, post):
	db['test_posts5'].update_many({'_id': ObjectId(post['_id'])}, {'$inc': {'fav_cnt': -1, 'popularity': -3}})

	return "success"

#포스트 조회수 올리기
def update_post_view(db, post):
	db['test_posts5'].update_one(
		{'_id': ObjectId(post['_id'])}, {'$inc': {'view': 1, 'popularity': 1}})

	return "success"
###############################################
#admin######################################### 



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