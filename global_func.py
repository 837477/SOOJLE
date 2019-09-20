import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone
from datetime import timedelta, datetime
import time
#######################################################
from db_management import *
#######################################################

'''
# BackgroundScheduler Initialize
def schedule_init():
	t_zone = get_localzone()
	scheduler = BackgroundScheduler()
	#scheduler.add_job(func = test_bg, trigger = "interval", seconds = 1, timezone = t_zone)

	scheduler.add_job(Soojle_crawler, 'cron', hour = 0, minute = 5, timezone = t_zone)
	
	# weeks, days, hours, minutes, seconds
	# start_date='2010-10-10 09:30', end_date='2014-06-15 11:00'
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())
'''

#######################################################
#백그라운드 프로세스#######################################

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
