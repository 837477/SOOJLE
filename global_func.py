import atexit
import time
from pymongo import *
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone
from datetime import timedelta, datetime
#######################################################
from db_management import *
from db_info import *
#######################################################


# BackgroundScheduler Initialize
def schedule_init():
	t_zone = get_localzone()
	scheduler = BackgroundScheduler()

	#특정 시간마다 실행
	#scheduler.add_job(update_posts_highest, 'cron', hour = 16, minute = 45, timezone = t_zone)

	#매 시간마다 실행
	# weeks, days, hours, minutes, seconds
	scheduler.add_job(func = update_posts_highest, trigger = "interval", seconds = 10, timezone = t_zone)
	
	# start_date='2010-10-10 09:30', end_date='2014-06-15 11:00'
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())


#######################################################
#백그라운드 프로세스#######################################
def update_posts_highest():
	db_client = MongoClient('mongodb://%s:%s@%s' %(MONGODB_ID, MONGODB_PW, MONGODB_HOST))
	db = db_client['soojle']

	#모든 포스트 중에서 가장 높은 view수 갱신
	update_posts_highest_view(db)

	#모든 포스트 중에서 가장 높은 fav_cnt수 갱신
	update_posts_highest_fav_cnt(db)

	db_client.close()


#######################################################
#전역 함수###############################################
def get_nowtime():
	now = datetime.now()
	encode_time = now.strftime('%Y-%m-%d %H:%M:%S')

	return encode_time

def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn
