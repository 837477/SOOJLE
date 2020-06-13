from flask import *
##########################################
from db_management import *
from global_func import *
##########################################

#Blueprint
BP = Blueprint('main', __name__)

#페이지 URL#############################################
@BP.route('/')
@BP.route('/home')
def home():
	return render_template('home/main.html')

@BP.route('/introduce')
def introduce():
	return render_template('etc/introduce.html')

@BP.route('/programmer')
def programmer():
	return render_template('etc/programmers.html')

@BP.route('/board')
def board():
	return render_template('board/pageboard.html')

@BP.route('/testing_search')
def testing_search():
	return render_template('testing/testing_search.html')

@BP.route('/kiosk/ai')
def testing_search():
	return render_template('testing/testing_search.html')

@BP.route('/testing_recommend')
def testing_recommend():
	return render_template('kiosk/kiosk.html')

@BP.route('/not_suported_IE')
def not_suported_IE():
	return render_template('etc/ie.html')