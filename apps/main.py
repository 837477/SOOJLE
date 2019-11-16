from flask import *
from db_management import *
from global_func import *

BP = Blueprint('main', __name__)

#######################################################
#페이지 URL#############################################
@BP.route('/')
@BP.route('/home')
def main_home():
	return render_template('main/index.html')