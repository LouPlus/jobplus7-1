from flask import Blueprint, render_template, current_app, flash, redirect, url_for

from flask_login import login_required, login_user, logout_user
from jobplus.models import db, Company, Job, User
from jobplus.forms import RegisterForm, LoginForm



front = Blueprint('front', __name__)

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

@front.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user, form.remember_me.data)
        flash('登录成功','success')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route('/register_user', methods=['POST','GET'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.role = 10
        form.create_user(user)

        flash('注册成功','success')
        return redirect(url_for('company.index'))
    return render_template('register_user.html', form=form)

@front.route('/register_company',methods=['POST','GET'])
def register_company():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.role = 20
        form.create_user(user)
        flash('注册成功','success')
        return redirect(url_for('user.index'))
    return render_template('register_company.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('.index'))
    
