from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from datetime import datetime, timedelta
import numpy
######################################################
import global_func
from variable import *




#SJ_DB_USER 관련#######################################
######################################################
#전체 유저 목록 반환 (미사용)
def find_all_user(db, _id=None, user_id=None, user_nickname=None, auto_login=None, topic=None, tag=None, fav_list=None, view_list=None, search_list=None, ft_vector=None, tag_sum=None, newsfeed_list=None, privacy=None, measurement_num=None):
	
	show_dict = {'_id': 0}
	if _id is not None: 
		show_dict['_id'] = 1
	if user_id is not None:
		show_dict['user_id'] = 1
	if user_nickname is not None:
		show_dict['user_nickname'] = 1
	if topic is not None:
		show_dict['topic'] = 1
	if tag is not None:
		show_dict['tag'] = 1
	if tag_sum is not None:
		show_dict['tag_sum'] = 1
	if ft_vector is not None:
		show_dict['ft_vector'] = 1
	if fav_list is not None:
		show_dict['fav_list'] = 1
	if view_list is not None:
		show_dict['view_list'] = 1
	if search_list is not None:
		show_dict['search_list'] = 1
	if newsfeed_list is not None:
		show_dict['newsfeed_list'] = 1
	if auto_login is not None:
		show_dict['auto_login'] = 1
	if privacy is not None:
		show_dict['privacy'] = 1
	if measurement_num is not None:
		show_dict['measurement_num'] = 1

	result = db[SJ_DB_USER].find({}, show_dict)

	return result

#특정 유저 반환 (사용)
def find_user(db, _id=None, user_id=None, user_pw=None, user_nickname=None, auto_login=None, topic=None, tag=None, fav_list=None, view_list=None, search_list=None, ft_vector=None, tag_sum=None, newsfeed_list=None, privacy=None, measurement_num=None):
	
	show_dict = {'_id': 0}
	if _id is not None:
		show_dict['_id'] = 1
	if user_id is not None:
		show_dict['user_id'] = 1
	if user_pw is not None:
		show_dict['user_pw'] = 1
	if user_nickname is not None:
		show_dict['user_nickname'] = 1
	if topic is not None:
		show_dict['topic'] = 1
	if tag is not None:
		show_dict['tag'] = 1
	if tag_sum is not None:
		show_dict['tag_sum'] = 1
	if ft_vector is not None:
		show_dict['ft_vector'] = 1
	if fav_list is not None:
		show_dict['fav_list'] = 1
	if view_list is not None:
		show_dict['view_list'] = 1
	if search_list is not None:
		show_dict['search_list'] = 1
	if newsfeed_list is not None:
		show_dict['newsfeed_list'] = 1
	if auto_login is not None:
		show_dict['auto_login'] = 1
	if privacy is not None:
		show_dict['privacy'] = 1
	if measurement_num is not None:
		show_dict['measurement_num'] = 1


	result = db[SJ_DB_USER].find_one(
		{
			'user_id': user_id
		}, 
		show_dict)

	return result

#유저 생성 (사용)
def insert_user(db, user_id, user_pw, user_nickname):
	topic_temp = numpy.ones(26)
	topic = (topic_temp / topic_temp.sum()).tolist()

	ft_vector = (numpy.zeros(30)).tolist()
	tag = {}
	tag_sum = 1
	fav_list = []
	view_list = []
	newsfeed_list = []
	search_list = []
	auto_login = 1
	renewal = datetime.now()
	privacy = 0
	measurement_num = 0

	result = db[SJ_DB_USER].insert(
		{
			'user_id': user_id,
			'user_pw': user_pw,
			'user_nickname': user_nickname,
			'ft_vector': ft_vector,
			'tag': tag,
			'tag_sum': tag_sum,
			'topic': topic,
			'fav_list': fav_list,
			'view_list': view_list,
			'newsfeed_list': newsfeed_list,
			'search_list': search_list,
			'auto_login': auto_login,
			'renewal': renewal,
			'privacy': privacy,
			'measurement_num': measurement_num
		})

	return "success"

#유저 관심도 초기화 (사용)
def update_user_measurement_reset(db, user_id):
	topic_temp = numpy.ones(26)
	topic = (topic_temp / topic_temp.sum()).tolist()

	ft_vector = (numpy.zeros(30)).tolist()
	tag = {}
	tag_sum = 1
	fav_list = []
	view_list = []
	newsfeed_list = []
	search_list = []
	renewal = datetime.now()

	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$set':
			{
				'ft_vector': ft_vector,
				'tag': tag,
				'tag_sum': tag_sum,
				'topic': topic,
				'fav_list': fav_list,
				'view_list': view_list,
				'newsfeed_list': newsfeed_list,
				'search_list': search_list,
				'renewal': renewal
			}
		}
	)

	return "success"

#유저 삭제 (사용)
def remove_user(db, user_id):
	db[SJ_DB_USER].remove(
		{
			'user_id': user_id
		}
	)

	return "success"

#유저 닉네임 변경 (사용)
def update_nickname(db, user_id, new_nick):
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		}, 
		{
			'$set': {'user_nickname': new_nick}
		}
	)
	return "success"

#유저 갱신시간별 반환 (관심도 측정용) (사용)
def find_user_renewal(db, renewal_time):
	result = db[SJ_DB_USER].find(
		{	
			'renewal':
			{
				'$gt': renewal_time
			}
		}, 
		{
			'fav_list': 1,
			'view_list': 1,
			'search_list': 1,
			'newsfeed_list': 1,
			'measurement_num': 1
		}
	)
	return result

#유저 오토로그인 변경 (사용)
def update_user_auto_login(db, user_id, value):
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		}, 
		{
			'$set': {'auto_login': value}
		}
	)
	return "success"

#개인정보처리방침 동의현황 변경 (미사용)
def update_user_privacy(db, user_id, value):
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$set': {'privacy': value}
		}
	)
	return "success"

#유저 갱신 시간 갱신 (사용)
def update_user_renewal(db, user_id):
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$set':
			{
				'renewal': datetime.now()
			}
		}
	)
	return "success"

#유저 fav_list 중복 체크 (사용)
def check_user_fav_list(db, _id, post_obi):
	result = db[SJ_DB_USER].find_one(
		{
			'_id': _id
		}, 
		{
			'fav_list': 
			{
				'$elemMatch': 
				{
					'_id': post_obi
				}
			}
		}
	)

	return result
#유저 fav_list에 요소 추가 (사용)
def update_user_fav_list_push(db, _id, fav_obj):
	db[SJ_DB_USER].update(
		{
			'_id': _id
		},
		{
			'$push': 
			{
				'fav_list': 
				{
					'$each': [fav_obj],
					'$position': 0
				}
			}
		}
	)
	return "success"
#유저 fav_list에 요소 삭제 (사용)
def update_user_fav_list_pull(db, _id, post_obi):
	db[SJ_DB_USER].update(
		{
			'_id': _id
		},
		{
			'$pull': 
			{
				'fav_list': 
				{
					'_id': post_obi
				}
			}
		}
	)
	return "success"
#유저 fav_list 갱신 (pushback) (사용)
def refresh_user_fav_list(db, user_id, refresh_obj_list):
	#fav_list 삭제
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$unset': {'fav_list': 1}
		}
	)

	#새로운 fav_list 등록
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$push': 
			{
				'fav_list':
				{
					'$each': refresh_obj_list,
					'$position': 0
				}
			}
		}
	)

	return "success"

#유저 view_list에 요소 추가 (사용)
def update_user_view_list_push(db, _id, view_obj):
	db[SJ_DB_USER].update(
		{
			'_id': _id
		},
		{
			'$push': 
			{
				'view_list':
				{
					'$each': [view_obj],
					'$position': 0
				}
			}
		}
	)
	return "success"
#유저 view_list 갱신 (pushback) (사용)
def refresh_user_view_list(db, user_id, refresh_obj_list):
	#view_list 삭제
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$unset': {'view_list': 1}
		}
	)

	#새로운 view_list 등록
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$push': 
			{
				'view_list':
				{
					'$each': refresh_obj_list,
					'$position': 0
				}
			}
		}
	)

	return "success"

#유저 search_list에 요소 추가 (사용)
def update_user_search_list_push(db, user_id, search_obj):
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$push': 
			{
				'search_list': 
				{
					'$each': [search_obj],
					'$position': 0
				}
			}
		}
	)
	return "success"
#유저 search_list 갱신 (pushback) (사용)
def refresh_user_search_list(db, user_id, refresh_obj_list):
	#search_list 삭제
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$unset': {'search_list': 1}
		}
	)

	#새로운 view_list 등록
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$push': 
			{
				'search_list':
				{
					'$each': refresh_obj_list,
					'$position': 0
				}
			}
		}
	)

	return "success"

#유저 newsfeed_list에 요소 추가 (사용)
def update_user_newsfeed_list_push(db, _id, newsfeed_obj):
	db[SJ_DB_USER].update(
		{
			'_id': _id
		},
		{
			'$push': 
			{
				'newsfeed_list':
				{
					'$each': [newsfeed_obj],
					'$position': 0
				}
			}
		}
	)
	return "success"
#유저 newsfeed_list 갱신 (pushback) (사용)
def refresh_user_newsfeed_list(db, user_id, refresh_obj_list):
	#newsfeed_list 삭제
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$unset': {'newsfeed_list': 1}
		}
	)

	#새로운 view_list 등록
	db[SJ_DB_USER].update(
		{
			'user_id': user_id
		},
		{
			'$push': 
			{
				'newsfeed_list':
				{
					'$each': refresh_obj_list,
					'$position': 0
				}
			}
		}
	)

	return "success"

#유저 관심도 갱신.
def update_user_measurement(db, _id, topic, tag, tag_sum, ft_vector, measurement_num):
	db[SJ_DB_USER].update({'_id': _id}, 
		{
			'$set': 
			{
				'topic': topic, 
				'tag': tag, 
				'tag_sum': tag_sum,
				'ft_vector': ft_vector,
				'measurement_num': measurement_num
			}
		})

	return "success"

#유저 최근 검색 X개 불러오기
def find_user_lately_search(db, user_id, num):
	result = db[SJ_DB_USER].find_one(
		{	
			'user_id': user_id
		},
		{
			'_id': 0,
			'user_id': 0,
			'user_pw': 0,
			'user_nickname': 0,
			'ft_vector': 0,
			'topic': 0,
			'search_list': {'$slice': num},
			'fav_list': 0,
			'view_list': 0,
			'newsfeed_list': 0,
			'tag': 0,
			'tag_sum': 0,
			'auto_login': 0,
			'renewal': 0,
			'privacy': 0,
			'measurement_num': 0
		}
	)
	return result['search_list']




#SJ_DB_POST 관련#######################################
######################################################
#포스트 전체 가져오기 (사용)
def find_all_posts(db, _id=None, title=None, date=None, end_date=None, post=None, tag=None, img=None, url=None, hashed=None, info=None, view=None, fav_cnt=None, title_token=None, token=None, topic=None, ft_vector=None, popularity=None, skip_=0, limit_=None):

	show_dict = {'_id': 0}

	if _id is not None:
		show_dict['_id'] = 1
	if title is not None:
		show_dict['title'] = 1
	if date is not None:
		show_dict['date'] = 1
	if end_date is not None:
		show_dict['end_date'] = 1
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
	if ft_vector is not None:
		show_dict['ft_vector'] = 1
	if popularity is not None:
		show_dict['popularity'] = 1

	if limit_ is None:
		#기본적으로 날짜순 정렬 (최신)
		result = db[SJ_DB_POST].find(
			{}, 
			show_dict
		).sort([('date', -1)]).skip(skip_)

	else:
		#기본적으로 날짜순 정렬 (최신)
		result = db[SJ_DB_POST].find(
			{}, 
			show_dict
		).sort([('date', -1)]).skip(skip_).limit(limit_)

	return result

#포스트 단일 가져오기 (사용)
def find_post(db, post_obi, _id=None, title=None, date=None, end_date=None, post=None, tag=None, img=None, url=None, hashed=None, info=None, view=None, fav_cnt=None, title_token=None, token=None, topic=None, ft_vector=None, popularity=None):

	show_dict = {'_id': 0}

	if _id is not None:
		show_dict['_id'] = 1
	if title is not None:
		show_dict['title'] = 1
	if date is not None:
		show_dict['date'] = 1
	if end_date is not None:
		show_dict['end_date'] = 1
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
	if ft_vector is not None:
		show_dict['ft_vector'] = 1
	if popularity is not None:
		show_dict['popularity'] = 1

	result = db[SJ_DB_POST].find_one(
		{
			'_id': ObjectId(post_obi)
		}, 
		show_dict
	)

	return result

#포스트 생성
def insert_post(db, title, post, tag, img, url, info, hashed, url_hashed, token, view, fav_cnt, title_token, login, learn, popularity, topic, ft_vector):
	db[SJ_DB_POST].insert(
		{
			'title': title,
			'post': post,
			'tag': tag,
			'img': img,
			'url': url,
			'info': info,
			'hashed': hashed,
			'url_hashed': url_hashed,
			'token': token,
			'view': view,
			'fav_cnt': fav_cnt,
			'title_token': title_token,
			'login': login,
			'learn': learn,
			'popularity': popularity,
			'topic': topic,
			'ft_vector': ft_vector,
			'date': datetime.now()
		}
	)

	return "success"

#포스트 수정
def update_post(db, post_obi, title, post, tag, img, url, info, hashed, url_hashed, token, title_token, topic, ft_vector):
	db[SJ_DB_POST].update(
		{
			'_id': ObjectId(post_obi)
		},
		{
			'$set':
			{
				'title': title,
				'post': post,
				'tag': tag,
				'img': img,
				'url': url,
				'info': info,
				'hashed': hashed,
				'url_hashed': url_hashed,
				'token': token,
				'title_token': title_token,
				'topic': topic,
				'ft_vector': ft_vector
			}
		}
	)

	return "success"

#포스트 삭제
def remove_post(db, post_obi):
	db[SJ_DB_POST].remove(
		{
			'_id': ObjectId(post_obi)
		}
	)
	return "success"

#포스트 좋아요 (사용)
def update_post_like(db, post_obi):
	db[SJ_DB_POST].update(
		{
			'_id': ObjectId(post_obi)
		}, 
		{
			'$inc': {'fav_cnt': 1, 'popularity': 3}
		}
	)
	return "success"

#포스트 좋아요 취소 (사용)
def update_post_unlike(db, post_obi):
	db[SJ_DB_POST].update(
		{
			'_id': ObjectId(post_obi)
		}, 
		{
			'$inc': 
			{
				'fav_cnt': -1, 
				'popularity': -3
			}
		}
	)
	return "success"

#포스트 조회수 올리기 (사용)
def update_post_view(db, post_obi):
	db[SJ_DB_POST].update(
		{
			'_id': ObjectId(post_obi)
		}, 
		{
			'$inc': 
			{
				'view': 1, 
				'popularity': 1
			}
		}
	)
	return "success"

#카테고리별 포스트들 반환 (사용)
def find_posts_of_category(db, info_num_list, now_date, num):
	result = db[SJ_DB_POST].find(
		{
			'$and':
			[
				{'info_num': {'$in': info_num_list}},
				{'end_date': {'$gt': now_date}}
			]
		},
		{
			'_id': 1,
			'title': 1,
			'date': 1,
			'img': 1,
			'fav_cnt': 1,
			'view': 1,
			'url': 1,
			'title_token': 1,
			'info': 1,
			'tag': 1,
			'topic': 1,
			'ft_vector': 1,
			'end_date': 1
		}
	).sort([('date', -1)]).limit(num).hint("info_num_1_end_date_-1_date_-1")
	return result

#카테고리별 포스트들 반환 (디폴트 데이트도 적용된 쿼리) (사용)
def find_posts_of_category_default_date(db, info_num_list, now_date, default_date, num):
	result = db[SJ_DB_POST].find(
		{
			'$and':
			[
				{'info_num': {'$in': info_num_list}},
				{'end_date': {'$gt': now_date}},
				{'date': {'$gt': global_func.get_default_day(default_date)}}
			]
		},
		{
			'_id': 1,
			'title': 1,
			'date': 1,
			'img': 1,
			'fav_cnt': 1,
			'view': 1,
			'url': 1,
			'title_token': 1,
			'info': 1,
			'tag': 1,
			'topic': 1,
			'ft_vector': 1,
			'end_date': 1
		}
	).sort([('date', -1)]).limit(num).hint("info_num_1_end_date_-1_date_-1")
	return result

#추천 뉴스피드 포스트들 불러오기 (사용)
def find_posts_of_recommendation(db, now_date, num):
	result = db[SJ_DB_POST].find(
		{
			'end_date': {'$gt': now_date}
		},
		{
			'_id': 1,
			'title': 1,
			'date': 1,
			'img': 1,
			'fav_cnt': 1,
			'view': 1,
			'url': 1,
			'title_token': 1,
			'info': 1,
			'tag': 1,
			'topic': 1,
			'ft_vector': 1,
			'end_date': 1
		}
	).sort([('date', -1)]).limit(num)
	return result

#인기 뉴스피드 반환 (사용)
def find_popularity_newsfeed(db, default_date, num):
	result = db[SJ_DB_POST].find(
		{
			'$and':
			[
				{'popularity': {'$gt': 0}},
				{'date': {'$gt': global_func.get_default_day(default_date)}}
			]
		},
		{
			'_id': 1,
			'title': 1,
			'date': 1,
			'end_date': 1,
			'img': 1,
			'fav_cnt': 1,
			'url': 1,
			'popularity': 1
		}
		).sort([('popularity', -1)]).limit(num)
	return result

#카테고리 검색
def find_search_of_category(db, search_list, info_num_list, num):
	result = db[SJ_DB_POST].find(
		{
			'$and':
			[
				{'token': {'$in': search_list}},
				{'info_num': {'$in': info_num_list}}
			]
		},
		{
			'_id':1, 
			'title':1,
			'date':1,
			'end_date':1,
			'img': 1,
			'url': 1,
			'fav_cnt': 1,
			'info': 1,
			###############
			'title_token':1,
			'token':1,
			'tag':1,
			'popularity':1,
			'ft_vector': 1
		}
		).sort([('date', -1)]).limit(num)
	return result

#총 DB포스트 갯수 반환
def find_posts_count(db):
	result = db[SJ_DB_POST].find().count()

	return result

#제일 높은 좋아요 수 반환
def find_highest_fav_cnt(db):
	result = db[SJ_DB_POST].find(
		{},
		{
			'_id': 0,
			'fav_cnt': 1
		}
	).sort([('fav_cnt', -1)]).limit(1)
	return result['fav_cnt']

#제일 높은 조회수 반환
def find_highest_view_cnt(db):
	result = db[SJ_DB_POST].find_one(
		{},
		{
			'_id': 0,
			'view': 1
		}
	).sort([('view', -1)]).limit(1)
	return result['view']

#더미 포스트 체크(있는지 확인용)
def check_dummy_post(db):
	result = db[SJ_DB_POST].find_one({'title': "(o^_^)o 안녕하세요. SOOJLE 입니다."})

	return result

#좋아요/조회수 초기 셋팅용 더비 포스트 생성
def insert_dummy_post(db):
	topic_temp = numpy.ones(26)
	topic = (topic_temp / topic_temp.sum()).tolist()
	db[SJ_DB_POST].insert(
		{
			'title' : "(o^_^)o 안녕하세요. SOOJLE 입니다.",
			'date': get_default_day(10000),
			'post': "안녕하세요. SOOJLE 입니다.",
			'tag': [],
			'img': 1,
			'url': "",
			'hashed': "",
			'info': "SOOJLE",
			'view': 1,
			'fav_cnt': 1,
			'title_token': [],
			'token': [],
			'login': 0,
			'learn': 1,
			'popularity': 0,
			'fav_vector': (numpy.zeros(30)).tolist(),
			'topic': topic
		}
	)
	return "success"




#SJ_DB_CATEGORY 관련###################################
######################################################
#카테고리별 타입 전체 반환
def find_all_category_of_topic(db):
	result = db[SJ_DB_CATEGORY].find(
		{},
		{
			'_id': 0
		}
	)
	return result

#카테고리별 타입 여러개 반환 (사용)
def find_category_of_topic_list(db, category_list):
	result = db[SJ_DB_CATEGORY].find(
			{
				'category_name': {'$in': category_list}
			}, 
			{
				'_id': 0,
				'tag': 1,
				'info_num': 1
			}
		)
	return result

#카테고리별 타입 반환 (사용)
def find_category_of_topic(db, category_name):
	result = db[SJ_DB_CATEGORY].find_one(
		{
			'category_name': category_name
		}, 
		{
			'_id': 0,
			'tag': 1,
			'info_num': 1
		}
	)
	return result




#SJ_DB_SEARCH_LOG 관련#################################
######################################################
#search_log에 search_obj 추가 (사용)
def insert_search_log(db, user_id, split_list):
	db[SJ_DB_SEARCH_LOG].insert(
		{
			'user_id': user_id,
			'search_split': split_list,
			'date': datetime.now()
		}
	)
	return "success"

#search_log 가져온다. (사용)
def find_search_log(db):
	result = db[SJ_DB_SEARCH_LOG].find(
		{
			'date':
			{
				'$gt': global_func.get_default_day(1)
			}
		},
		{
			'_id': 0,
			'search_split': 1
		}
	).sort([('date', -1)])

	return result

#총 검색 횟수 반환.
def find_search_count(db):
	result = db[SJ_DB_SEARCH_LOG].find().count()

	return result




#SJ_DB_LOG 관련########################################
######################################################
#log에 기록! (사용)
def insert_log(db, user_id, url):
	db[SJ_DB_LOG].insert(
		{
			'user_id': user_id,
			'url': url,
			'date': datetime.now()
		}
	)
	return "success"

#log에서 시간별로 가져온다. (사용)
def find_date_log(db, date, limit_):
	result = db[SJ_DB_LOG].find(
		{
			'date':
			{
				'$gte': date
			}
		},
		{
			'_id': 0,
			'user_id': 1
		}
	).sort([('date', -1)]).limit(limit_)

	return result

#log에서 회원별로 가져온다.
def find_user_log(db, user_id, limit_):
	result = db[SJ_DB_LOG].find(
		{
			'user_id': user_id
		},
		{
			'_id': 0
		}
	).sort([('date', -1)]).limit(limit_)

	return result

#log에서 시간별 + 회원별로 가져온다.
def find_user_date_log(db, user_id, date, limit_):
	result = db[SJ_DB_LOG].find(
		{
			'$and':
			[
				{'date': {'$gte': date}},
				{'user_id': user_id}
			]
		},
		{
			'_id': 0
		}
	).sort([('date', -1)]).limit(limit_)

	return result

#총 API로그 갯수 반환
def find_log_count(db):
	result = db[SJ_DB_LOG].find().count()

	return result




#SJ_DB_USER_BACKUP 관련################################
######################################################
#pushback 함수 (user document 16Mb 초과 방지)
def insert_pushback(db, user_id, type_, back_obj_list):
	#좋아요 타입
	if type_ == 'fav':
		for back_obj in back_obj_list:
			db[SJ_DB_USER_BACKUP].insert(
				{
					'user_id': user_id,
					'type': 'fav',
					'obj_id': back_obj['_id'],
					'topic': back_obj['topic'],
					'token': back_obj['token'],
					'tag': back_obj['tag'],
					'post_date': back_obj['post_date'],
					'title': back_obj['title'],
					'url': back_obj['url'],
					'img': back_obj['img'],
					'date': back_obj['date']
				}
			)
	
	#조회수 타입
	elif type_ == 'view':
		for back_obj in back_obj_list:
			db[SJ_DB_USER_BACKUP].insert(
				{
					'user_id': user_id,
					'type': 'view',
					'obj_id': back_obj['_id'],
					'topic': back_obj['topic'],
					'token': back_obj['token'],
					'tag': back_obj['tag'],
					'post_date': back_obj['post_date'],
					'title': back_obj['title'],
					'url': back_obj['url'],
					'img': back_obj['img'],
					'date': back_obj['date']
				}
			)
	
	#검색 타입
	elif type_ == 'search':
		for back_obj in back_obj_list:
			db[SJ_DB_USER_BACKUP].insert(
				{
					'user_id': user_id,
					'type': 'search',
					'original': back_obj['original'],
					'search_split': back_obj['search_split'],
					'tokenizer_split': back_obj['tokenizer_split'],
					'similarity_split': back_obj['similarity_split'],
					'date': back_obj['date']
				}
			)
	
	#뉴스피드 타입
	else:
		for back_obj in back_obj_list:
			db[SJ_DB_USER_BACKUP].insert(
				{
					'user_id': user_id,
					'type': 'newsfeed',
					'newsfeed_name': back_obj['newsfeed_name'],
					'tag': back_obj['tag'],
					'date': back_obj['date']
				}
			)
		
	return "success"




#SJ_DB_REALTIME 관련###################################
######################################################
#search_realtime 가져오기!
def find_search_all_realtime(db):
	result = db[SJ_DB_REALTIME].find(
		{},
		{
			'_id': 0
		}
	)
	return result

#search_realtime 단일 가져오기!
def find_search_realtime(db):
	result = db[SJ_DB_REALTIME].find(
		{},
		{
			'_id': 0,
			'real_time': 1,
			'date': 1
		}
	).sort([('date', -1)]).limit(1)
	return result

#search_realtime에 기록!
def insert_search_realtime(db, real_time_list):
	db[SJ_DB_REALTIME].insert(
		{
			'real_time' : real_time_list,
			'date': datetime.now()
		}
	)
	return "success"




#SJ_DB_VISITOR 관련####################################
######################################################
#today_vistior 입력! (중복체크까지 여기서 함)
def insert_today_visitor(db, user_id):
	check = db[SJ_DB_VISITOR].find_one(
		{
			'user_id': user_id
		}
	)

	#방문 안한 유저라면?
	if check is None:
		db[SJ_DB_VISITOR].insert(
			{
				'user_id': user_id,
				'date': datetime.now()
			}
		)

		#총 방문자 수 +1
		update_variable_inc(db, 'total_visitor', 1)

#today_visitor_count 반환!
def find_today_visitor_count(db):
	result = db[SJ_DB_VISITOR].find().count()

	return result

#today (현재시간 ~ 특정 시간) 방문자 수 가져오기!
def find_today_time_visitor(db, time):
	result = db[SJ_DB_VISITOR].find(
		{
			'date':
			{
				'$gt': time
			}
		}
	).count()
	
	return result

#today visitor 콜렉션 데이터 전체 삭제! (데이터 비우기)
def remove_today_visitor(db):
	db[SJ_DB_VISITOR].remove({})

	return "success"




#SJ_DB_ANALYSIS 관련###################################
######################################################
#매일 갱신되는 통계 테이블에 추가!
def insert_everyday_analysis(db, analysis_obj):
	db[SJ_DB_ANALYSIS].insert(
		analysis_obj
	)
	return "success"

#매일 통계에서 특정 날짜 이후 통계 반환
def find_everyday_analysis_days(db, date):
	result = db[SJ_DB_ANALYSIS].find(
		{
			'date': 
			{
				'$gte': date
			}
		},
		{
			'_id': 0
		}
	)

	return result

#매일 통계에서 특정 날짜 통계 반환
def find_everyday_analysis_specific_day(db, date):
	result = db[SJ_DB_ANALYSIS].find_one(
		{
			'date': date
		},
		{
			'_id': 0
		}
	)

	return result




#SJ_DB_NOTICE 관련#####################################
######################################################
#공지사항 추가
def insert_notice(db, title, post):
	db[SJ_DB_NOTICE].insert(
		{
			'title': title,
			'post': post,
			'view': 0,
			'date': datetime.now(),
			'activation': 1
		}		
	)

	return "success"

#공지사항 수정
def update_notice(db, notice_obi, title, post, activation):
	db[SJ_DB_NOTICE].update(
		{
			'_id': ObjectId(notice_obi)
		},
		{
			'$set':
			{
				'title': title,
				'post': post,
				'activation': activation,
				'date': datetime.now()
			}	
		}
		
	)

	return "success"

#공지사항 삭제
def remove_notice(db, notice_obi):
	db[SJ_DB_NOTICE].remove(
		{
			'_id': ObjectId(notice_obi)
		}
	)

	return "success"

#공지사항 전체 반환
def find_all_notice(db):
	result = db[SJ_DB_NOTICE].find().sort([('date', -1)])

	return result

#공지사항 단일 반환
def find_notice(db, notice_obi):
	result = db[SJ_DB_NOTICE].find_one(
		{
			'_id': ObjectId(notice_obi)
		}
	)

	return result

#공지사항 조회수 올리기
def update_notice_view(db, notice_obi):
	db[SJ_DB_NOTICE].update(
		{
			'_id': ObjectId(notice_obi)
		}, 
		{
			'$inc': 
			{
				'view': 1
			}
		}
	)

	return "success"




#SJ_DB_FEEDBACK 관련###################################
######################################################
#피드백 입력
def insert_user_feedback(db, feedback):
	db[SJ_DB_FEEDBACK].insert(
    	feedback
   	)
	return "success"




#SJ_DB_VARIABLE 관련###################################
######################################################
#정적 테이블 변수 불러오기
def find_variable(db, key):
	result = db[SJ_DB_VARIABLE].find_one(
		{
			'key': key
		}, 
		{
			'_id': 0,
			'value':1
		}
	)
	return result['value']

#정적 테이블 변수 수정하기(값 변경)
def update_variable(db, key, value):
	db[SJ_DB_VARIABLE].update(
		{
			'key': key
		}, 
		{
			'$set': {'value': value }
		}
	)
	return "success"	

#정적 테이블 변수 수정하기(값 증가, 감소) _ 정수 자료형만 가능!
def update_variable_inc(db, key, increase):
	db[SJ_DB_VARIABLE].update(
		{
			'key': key
		}, 
		{
			'$inc': {'value': increase}
		}
	)
	return "success"

#today 매 시간별 방문자 수 기록!
def push_today_time_visitor(db, hour_visitor_obj):
	db[SJ_DB_VARIABLE].update(
		{
			'key': 'today_time_visitor'
		},
		{
			'$push':
			{
				'value': hour_visitor_obj
			}
		}
	)

	return "success"





#그 이외 것들############################################
######################################################
#domain 다 불러오기 (사용)
def find_all_domain(db):
	result = db['domain'].find(
		{},
		{
			'_id': 0
		}
	)
	return result

#domain_title_regex 검색 (사용)
def find_domain_title_regex(db, search_str):
	result = db['domain'].find(
			{
				'$or':
				[
					{'title': {'$regex':search_str}},
					{'url': {'$regex':search_str}}
				]
			}, 
			{
				'_id': 0,
				'title': 1,
				'post': 1,
				'url': 1
			}
		)
	return result

#domain_post_regex 검색 (사용)
def find_domain_post_regex(db, regex_str):
	result = db['domain'].find(
			{
				'post': {'$regex':regex_str}
			}, 
			{
				'_id': 0,
				'title': 1,
				'post': 1,
				'url': 1
			}
		)
	return result









