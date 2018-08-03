from flask import Blueprint, render_template, request, current_app, request
from jobplus.models import Company, User, Job, JobWanted, db
from jobplus.decorators import company_required
from flask_login import current_user
from jobplus.forms import PersonalForm, JobForm


company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
def index():
    # 获取参数中传递过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = Company.query.paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('company/index.html', pagination=pagination)

@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/company_detail.html', company=company)

# 公司后台
@company.route('/admin/resume_pending', methods=['POST','GET'])
@company_required
def resume_pending():
    if request.method == 'GET':
        #设置初始时的页面,为待处理
        nowstate = request.args.get('state',default=1,type=int)
    if request.method == 'POST':
        #如果post不是发送的变为其他状态的请求,则获取表格操作发送的请求
        try:
            nextstate = int(request.form.get('state', '-1'))
            # jobwanted_id 会被post一个不在其操作权限的值吗?
            jobwanted_id = int(request.values.get('jobwanted_id','-1'))
            if nextstate > 0 and jobwanted_id > 0:
                jobwanted = JobWanted.query.get(jobwanted_id)
                if jobwanted and jobwanted.state != nextstate:
                    #jobwanted.state = nextstate
                    #db.session.add(jobwanted)
                    #db.session.commit()
                    return ('success')
        except TypeError:
           abort(404)
    page = request.args.get('page', default=1, type=int)
    # 查找company
    company = Company.query.filter_by(user_id=current_user.id).first()
    # 根据company id查找JobWanted表
    jobwanted = JobWanted.query.filter_by(company_id=company.id)
    # 查询state为待处理的jobwanted
    item = jobwanted.filter_by(state=nowstate)
    pending_num = len(jobwanted.filter_by(state=1).all())
    interview_num = len(jobwanted.filter_by(state=2).all())
    improper_num = len(jobwanted.filter_by(state=3).all())
    pagination = item.paginate(
            page=page,
            per_page=current_app.config['ADMIN_PER_PAGE'],
            error_out=False
              )
    return render_template(
            'company/resume_pending.html', pagination=pagination,
            pending_num=pending_num,improper_num=improper_num,
            interview_num=interview_num, nowstate=nowstate)


# 企业职位管理
@company.route('/admin/job', methods=['POST','GET'])
@company_required
def job():
    if request.method == 'GET':
        nowstate = request.args.get('state', default=1, type=int)
    if request.method == 'POST':
        try:
            nextstate = int(request.form.get('state'))
            job_id = int(request.form.get('job_id'))
            print(nextstate, job_id)
            job = Job.query.get_or_404(job_id)
            #db.session.add(job)
            #db.session.commit()
            return 'success'
        except TypeError:
            return 'fail'
    page = request.args.get('page', default=1, type=int)
    # 查找company
    company = Company.query.filter_by(user_id=current_user.id).first()
    job = company.company_job.query
    item = job.filter_by(state=nowstate)
    #职位上下架数量
    on_num = len(job.filter_by(state=1).all())
    off_num = len(job.filter_by(state=2).all())
    pagination = item.paginate(
            page=page,
            per_page=current_app.config['ADMIN_PER_PAGE'],
            error_out=False)
    return render_template(
            'company/admin_job.html', pagination=pagination,
            on_num=on_num,off_num=off_num,
            nowstate=nowstate)

# 企业职位编辑
@company.route('/admin/job_eidt', methods=['POST','GET'])
@company_required
def job_edit():
    job_id = request.args.get('job_id')
    try:
        job_id = int(job_id)
    except TypeError:
        pass
    if job_id:
        job = Job.query.get_or_404(job_id)
        form = JobForm(obj=job)
        if form.validate_on_submit():
            form.populate_obj(job)
            form.create_job(job)
            flash('修改成功','success')
            return redirect(url_for('company.job'))
    else:
        job = Job()
        form = JobForm()
    if form.validate_on_submit():
        # 增加缺少的数据
        job_id = Company.query.filter_by(user_id=current_user.id).id
        job.id = job.job_id
        job.state = 1
        form.populate_obj(job)
        form.create_job(job)
        flash('创建成功','success')
    return render_template('company/admin_job_edit.html',form=form)



# 企业配置信息
@company.route('/profile', methods=['POST','GET'])
@company_required
def profile():
    company = Company.query.filter_by(user_id=current_user.id)
    if not company:
        company = Company()
        company.user_id = current_user.id
        form = CompanyForm()
    else:
        form  = CompanyForm(obj=company)
    if form.validate_on_submit:
        if not company.name:
            if Company.query.filter_by(name=form.name.data):
                flash('公司名已被注册', 'success')
                return render_tempalte('company/profile.html', form=form)
        else:
            if company.name != form.name.data:
                if Company.query.filter_by(name=form.name.data):
                    flash('公司名已被注册', 'success')
                    return render_tempalte('company/profile.html', form=form)

        form.populate_obj(company)
        form.create_company(company)
        flash('编辑成功', 'success')
    return render_tempalte('company/profile.html', form=form)




# 测试
@company.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'POST':
        form = PersonalForm()
        return (form)
    else:
        form = PersonalForm()
    return render_template('company/test.html',form=form)

