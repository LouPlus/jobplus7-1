from flask import Blueprint, render_template

from flask_login import login_required


front = Blueprint('front', __name__, url_prefix='/')

@front.route('/')
def index():
    return render_template('index.html')

@front.route('/login')
def login():
    return '登录'

@front.route('/register')
def register():
    return '用户注册'

@front.route('/logout')
@login_required
def logout():
    return '退出'
    
