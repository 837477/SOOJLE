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
from pymongo import *
from datetime import timedelta, datetime
###################################################
from db_management import *
from db_info import *
from variable import *
from global_func import get_default_day

#variable 가장 높은 좋아요/조회수 갱신
def update_posts_highest():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client["soojle"]

	#새로운 fav / view 카운트
	new_fav = find_highest_fav_cnt(db)
	new_view = find_highest_view_cnt(db)

	update_variable(db, 'highest_fav_cnt', new_fav)
	update_variable(db, 'highest_view_cnt', new_view)

	if db_client is not None:
		db_client.close()


if __name__ == '__main__':
	FILE = open('/home/iml/log/background.log', 'a')
	#FILE = open('background.log', 'a')
	
	try:
		update_posts_highest()
		log_data = str(datetime.now()) + " ::: Highest post 캐싱 성공 :)  \n"
    
	except Exception as ex:
		log_data = str(datetime.now()) + " ::: Highest post 캐싱 실패 :(  \n" + str(ex) + "\n"

	FILE.write(log_data)

	FILE.close()
    