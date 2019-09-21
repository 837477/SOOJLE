from flask import *
from bson.json_util import dumps
from db_management import *
from global_func import *
from datetime import datetime

BP = Blueprint('newsfeed', __name__)

@BP.route('/get_newsfeed/<int:type>/<string:tags>/<string:date>/<int:pagenation>/<int:page>')
def get_newsfeed(type, tags, date, pagenation, page):
	
	tag_list = tags.split('_')
	if(date == 'now'):
		date = datetime.now()
	else:
		date = datetime.strptime(date, '%Y-%m-%d')

	result = find_posts(g.db, None, tag_list, date, pagenation)

	return jsonify(
		posts = dumps(result),
		result = "success")

#############################################
#############################################
