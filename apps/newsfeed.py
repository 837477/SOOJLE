from flask import *
from bson.json_util import dumps
from db_management import *
from global_func import *
from datetime import datetime

BP = Blueprint('newsfeed', __name__)

@BP.route('/get_newsfeed')
@BP.route('/get_newsfeed/<int:pagenation>/<int:page>')
@BP.route('/get_newsfeed/<int:type>/<int:pagenation>/<int:page>')
@BP.route('/get_newsfeed/<string:tags>/<int:pagenation>/<int:page>')
@BP.route('/get_newsfeed/<int:type>/<string:tags>/<int:pagenation>/<int:page>')
@BP.route('/get_newsfeed/<int:type>/<string:tags>/<string:date>/<int:pagenation>/<int:page>')
def get_newsfeed(type=None, tags=None, date=None, pagenation=None, page=None):
	
	if tags is not None:
		tag_list = tags.split('_')
	else:
		tag_list = []

	if date is not None:
		date = datetime.strptime(date, '%Y-%m-%d')
	else:
		date = datetime.now()

	result = find_posts(g.db, None, tag_list, date, pagenation, page)

	return jsonify(
		posts = dumps(result),
		result = "success")

#############################################
#############################################
