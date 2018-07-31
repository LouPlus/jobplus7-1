from flask import Blueprint, render_template, request, current_app, request
from jobplus.models import Company, User, Job, JobWanted, db
from jobplus.decorators import company_required
from flask_login import current_user


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
    if request.method == 'POST':
        state = int(request.form.get('state', '-1'))
        # jobwanted_id 会被post一个不在其操作权限的值吗?
        jobwanted_id = int(request.values.get('jobwanted_id','-1'))
        if state > 0 and jobwanted_id > 0:
            jobwanted = JobWanted.query.get(jobwanted_id)
            print(jobwanted_id,state)
            return ('success')
            if jobwanted and jobwanted.state != state:
                #jobwanted.state = state
                #db.session.add(jobwanted)
                #db.session.commit()
                print('-------------------')
                return ('success')
    page = request.args.get('page', default=1, type=int)
    # 查找company
    company = Company.query.filter_by(user_id=current_user.id).first()
    # 根据company id查找JobWanted表
    jobwanted = JobWanted.query.filter_by(company_id=company.id).filter_by(state=1)
    if jobwanted:
        pagination = jobwanted.paginate(
                page=page,
                per_page=current_app.config['ADMIN_PER_PAGE'],
                error_out=False
                  )
    return render_template('company/resume_pending.html', pagination=pagination)


#@company.route('/admin/resume_interview', methods=['POST','GET'])
#@company_required
#def resume_interview():

# 测试
@company.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'POST':
        state = request.form.get('state', 'mzyb')
        some = request.values.get('jobwanted_id','mzyb')
        return (some+state)
    return render_template('company/test.html')

