from flask import Blueprint


company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
def index(company_id):
    return '企业信息配置页面'
