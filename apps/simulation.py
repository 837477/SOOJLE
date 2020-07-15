from flask import *
from flask_jwt_extended import *
from werkzeug import *
##########################################
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
import operator
import math
from numpy import dot
from numpy.linalg import norm
import numpy
##########################################
from db_management import *
from global_func import *
import jpype
import tknizer
##########################################
BP = Blueprint('simulation', __name__)
##########################################

#입력된 str을 split 해주는 API OK
@BP.route('/simulation_split/<string:input_str>')
def simulation_split(input_str):
	result = input_str.split(' ')

	return jsonify(
		result = "success",
		simulation = result)

#입력된 str을 tokenizer 해주는 API OK
@BP.route('/simulation_tokenizer/<string:input_str>')
def simulation_tokenizer(input_str):
	result = tknizer.get_tk(input_str)
	
	return jsonify(
		result = "success",
		simulation = result)

#입력된 str을 fasttext로 유사한 단어를 추출 해주는 API - OK
@BP.route('/get_similarity_words', methods = ['POST'])
def get_similarity_words():
	input_str = request.form['search']

	tokenizer_list = tknizer.get_tk(input_str)
	
	result = {}
	for word in tokenizer_list:
		similarity_list = []
		for sim_word in FastText.sim_words(word):
			temp = {}
			if sim_word[1] >= 0.5: 
				temp[sim_word[0]] = sim_word[1]
				similarity_list.append(temp)
			else: break	
		result[word] = similarity_list

	return jsonify(
		result = "success",
		simulation = result)

#해당 USER의 관심도 반환 API - OK
@BP.route('/simulation_get_user_measurement/<string:user_id>')
def simulation_get_user_measurement(user_id):
	USER = find_user(g.db, user_id=user_id, user_nickname=1, topic=1, tag=1, ft_vector=1)

	if USER is None: abort(400)

	return jsonify(
		result = "success",
		user = USER)

def match_score(token1, token2):
	MC = len(set(token1) & set(token2))
	MR = MC / len(token1)
	return MC * (1 + MR + math.floor(MR))