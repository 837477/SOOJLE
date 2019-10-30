from flask import *
from flask_jwt_extended import *
from werkzeug import *
from bson.json_util import dumps
from bson.objectid import ObjectId
from operator import itemgetter
from collections import Counter
import numpy as np
import pandas as pd
##########################################
from db_management import *
from global_func import *
import jpype
from tknizer import get_tk
##########################################
import LDA
##########################################
BP = Blueprint('interest', __name__)
#####################################

#사용자 관심도 측정
@BP.route('/testtest/<int:num>')
def measurement_run(num):
	#사용자의 fav_list, view_list, search_list를 가져온다.
	USER = find_user(g.db, user_id="16011092", fav_list=1, view_list=1, search_list=1)

	#시간순 정렬(최신순)
	fav_list = sorted(USER['fav_list'], key=itemgetter('date'), reverse=True)
	view_list = sorted(USER['view_list'], key=itemgetter('date'), reverse=True)

	#fav topic numpy array
	fav_topic = np.zeros(10)
	#fav tag array
	fav_tag = []

	#view topic numpy array
	view_topic = np.zeros(10)
	#view tag arry
	view_tag = []

	for fav in fav_list[:num]:
		fav_topic += fav['topic']
		fav_tag += fav['tag']

	for view in view_list[:num]:
		view_topic = view['topic']
		view_tag = view['tag']

	#############사용자가 관심 기능을 수행한 게시물#############

	###LDA Format###
	#모든 문서를 대상으로 성분 합 연산 후 전체 문서 개수로 나눈다.
	fav_topic /= num
	#기여도 0.4를 곱해준다.
	fav_topic *= 4
	fav_topic /= 10

	###Tag Format###
	fav_tag = pd.DataFrame(fav_tag, columns = ['tags'])
	fav_tag = fav_tag.groupby('tags').size() * 4


	##################사용자가 접근한 게시물##################

	###LDA Format###
	#모든 문서를 대상으로 성분 합 연산 후 전체 문서 개수로 나눈다.
	view_topic /= num
	#기여도 0.4를 곱해준다.
	view_topic *= 3
	view_topic /= 10

	###Tag Format###
	view_tag = pd.DataFrame(view_tag, columns = ['tags'])
	view_tag = view_tag.groupby('tags').size() * 3

	###############사용자가 검색을 수행한 키워드###############


