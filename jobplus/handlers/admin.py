from flask import Blueprint, render_template, request, current_app, request, flash
from jobplus.models import Company, User, Job, JobWanted, db, Personal
from jobplus.decorators import admin_required
from flask_login import current_user
from jobplus.forms import CompanyeditForm, UsereditForm


admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/users', methods=['POST','GET'])
@admin_required
def users():
    if request.method == 'POST':
        try:
            id = request.form.get('id',type=int)
            state = request.form.get('state',type=int)
            if not id or not state:
                raise ValueError
            user = User.query.get_or_404(id)
            user.state = state
            db.session.add(user)
            db.session.commit()
            return 'success'
        except ValueError:
            pass
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
            page=page,
            per_page = current_app.config['INDEX_PER_PAGE'],
            error_out = False
            )
    return render_template('/admin/admin_users.html', pagination=pagination)


# 编辑用户资料
@admin.route('/users/edituser', methods=['POST','GET'])
@admin_required
def users_edit():
    id = request.args.get('id',type=int)
    if not id:
        # 创建用户
        user = User()
        person = Personal()
        user.role = 10
        person.user_id = user.id
    else:
        user = User.query.get_or_404(id)
        person  = user.user_user_info
    form = UsereditForm(obj=person)
    form.email.data = user.email
    if form.validate_on_submit():
        form.populate_obj(person)
        user.password = form.password.data
        db.session.add(person)
        db.session.add(user)
        db.session.commit()
        flash('编辑用户信息成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('/admin/users_edit.html', form=form)


# 编辑企业用户资料
@admin.route('/users/editcompany', methods=['POST','GET'])
@admin_required
def company_edit():
    id = request.args.get('id',type=int)
    if not id:
        abort(404)
    user = User.query.get_or_404(id)
    company  = user.user_company_info
    form = CompanyeditForm(obj=company)
    form.email.data = user.email
    if form.validate_on_submit():
        if company.name != form.name.data:
            if Company.query.filter_by(name=form.name.data):
                flash ('公司名称已存在' ,'success')
                return render_template('/admin/users_edit.html', form=form)
        form.populate_obj(company)
        user.password = form.password.data
        db.session.add(company)
        db.session.add(user)
        db.session.commit()
        flash('编辑用户信息成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('/admin/company_edit.html', form=form)


# 增加企业用户
@admin.route('/users/addcompany', methods=['POST','GET'])
@admin_required
def company_add():
    company  = Company()
    user = User()
    user.role = 20
    company.user_id = user.id
    form = CompanyForm()
    if form.validate_on_submit():
        if Company.query.filter_by(name=form.name.data):
            flash ('公司名称已存在' ,'success')
            return render_template('/admin/company_add.html', form=form)
        form.populate_obj(company)
        user.password = form.password.data
        db.session.add(company)
        db.session.add(user)
        db.session.commit()
        flash('编辑用户信息成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('/admin/company_edit.html', form=form)


# 职位管理
@admin.route('/jobs', methods=['POST','GET'])
@admin_required
def jobs():
    if request.method == 'POST':
        try:
            id = request.form.get('id',type=int)
            state = request.form.get('state',type=int)
            if not id or not state:
                raise ValueError
            job = Job.query.get_or_404(id)
            job.state = state
            db.session.add(job)
            db.session.commit()
            return 'success'
        except ValueError:
            pass
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
            page=page,
            per_page = current_app.config['INDEX_PER_PAGE'],
            error_out = False
            )
    return render_template('/admin/admin_jobs.html', pagination=pagination)

