from flask import Blueprint, render_template, request, current_app
from jobplus.models import Company

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
