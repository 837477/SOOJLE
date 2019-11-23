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

#입력된 str을 split 해주는 API
@BP.route('/simulation_split/<string:input_str>')
def simulation_split(input_str):
	result = input_str.split(' ')

	return jsonify(
		result = "success",
		simulation = result)

#입력된 str을 tokenizer 해주는 API
@BP.route('/simulation_tokenizer/<string:input_str>')
def simulation_tokenizer(input_str):
	result = tknizer.get_tk(input_str)
	
	return jsonify(
		result = "success",
		simulation = result)

#입력된 str을 fasttext로 유사한 단어를 추출 해주는 API
@BP.route('/simulation_fastext', methods = ['POST'])
def simulation_fastext():
	input_str = request.form['input_str']

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

