from global_func import *

#######################################################
#사용자 관련#############################################

def insert_user(db, user_id, user_pw, user_name, user_major):
	result = db['user'].insert({
		'user_id': user_id,
		'user_pw': user_pw,
		'user_name': user_name,
		'user_major': user_major
		})
	return "success"

def select_user(db, user_id):
	result = db['user'].find_one(
		{'user_id': user_id},
		{
			'_id': 0,
			'user_id': 1,
			'user_name': 1,
			'user_major': 1
		}
	)
	return result

