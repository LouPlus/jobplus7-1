from flask import Blueprint, render_template, current_app

from flask_login import login_required
from jobplus.models import db, Company, Job


front = Blueprint('front', __name__, url_prefix='/')

@front.route('/')
def index():
    jobs = Job.query.paginate(
            page=1,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=True
            )
    companies = Company.query.paginate(
            page=1,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=True
            )
    return render_template('index.html', jobs=jobs, companies=companies, Company=Company)

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
    
