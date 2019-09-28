#!/usr/bin/env python3
###########################################
import sys
from flask import *
from flask_jwt_extended import *
from flask_cors import CORS
###########################################
sys.path.insert(0,'./')
sys.path.insert(0,'../')
sys.path.insert(0,'../SJ_Auth')
sys.path.insert(0,'./database')
sys.path.insert(0,'./apps')
sys.path.insert(0,'/home/iml/')
sys.path.insert(0,'/home/iml/SOOJLE/')
sys.path.insert(0,'/home/iml/SOOJLE_Crawler/src/')
sys.path.insert(0,'/home/iml/SJ_Auth')
sys.path.insert(0,'/home/iml/SJ_AI/src')
sys.path.insert(0,'/home/iml/IML_Tokenizer/src/')
sys.path.insert(0,'../../IML_Tokenizer/src/')
###########################################
from init_database import *
from global_func import *
###########################################
#APPS
import main, auth, newsfeed, error, similarity

application = Flask(__name__, instance_relative_config=True)
cors = CORS(application)

#Debug or Release
application.config.update(
		DEBUG = True,
		JWT_SECRET_KEY = 'HELLO WE ARE SOOJLE',
	)
jwt = JWTManager(application)

def main_app(test_config = None):
	#백그라운드 작업
	schedule_init()
	#페이지들
	application.register_blueprint(main.BP)
	application.register_blueprint(auth.BP)
	application.register_blueprint(newsfeed.BP)
	application.register_blueprint(similarity.BP)

@application.before_request
def before_request():
	get_db()

@application.teardown_request
def teardown_request(exception):
	close_db()

main_app()

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)

    