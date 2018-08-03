from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from werkzeug import secure_filename
from flask_login import login_required, current_user
from jobplus.forms import PersonalForm
from jobplus.models import Personal, User, JobWanted, Job, Company

from jobplus.decorators import person_required



user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/')
@person_required
def index():
    page = request.args.get('page',default=1,type=int)
    # 用current_user.id作为查询起点,有别的方法马?
    person = User.query.get(current_user.id).user_user_info
    jobwanted = JobWanted.query.filter_by(personal_id=person.id)
    pagination = jobwanted.paginate(
            page=page,
            per_page=current_app.config['ADMIN_PER_PAGE'],
            error_out=False
            )
    return render_template('user/index.html',pagination=pagination)



@user.route('/profile', methods=['POST','GET'])
@person_required
def profile():
    person = Personal.query.filter_by(user_id=current_user.id).first()
    user = User.query.filter_by(id=current_user.id).first()
    #备份一个person对象，不影响原对象的属性
    if person:
        #填充表格,保留person的id信息
        form = PersonalForm(obj=person)
        form.email.data = user.email
    else:
        person = Personal()
        form = PersonalForm()
    if form.validate_on_submit():
        #文件格式用户id＋''s'+源文件名
        filename = str(current_user.id)+"\'s"+secure_filename(form.resume.data.filename)
        #路径为固定，需要手动建立
        #没有验证文件路径是否存在，os无法直接递归建立目录
        filedir = '/home/shiyanlou/static/resumes/'+filename
        person.user_id = current_user.id
        form.resume.data.save(filedir)
        form.resume.data = filename
        form.populate_obj(person)
        form.create_person(person)
        #是否需要判断密码是否为空
        if form.password.data:
            user.password = form.password.data
            form.create_user(user)
        #先暂时跳转到首页
        flash('提交成功','success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html',form=form)
