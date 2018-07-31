from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)


# 用户
class User(Base, UserMixin):
    __tablename__ = "user"  # 用户表
    ROLE_USER = 10  # 一般用户
    ROLE_STAFF = 20  # 企业用户
    ROLE_ADMIN = 30  # 超级管理员
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 会员名
    email = db.Column(db.String(100))  # 邮箱
    _password = db.Column('password',db.String(100))  # 密码
    role = db.Column(db.SmallInteger, default=ROLE_USER)  # 角色
    user_company_info = db.relationship('Company',backref='user', uselist=False)  # 企业信息外键关系
    user_user_info = db.relationship('Personal', backref='user',uselist=False)  # 个人用户信息外键关系

    def __repr__(self):
        return "<User %r>" % self.name

    #用户密码hash生成和检验
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)


    def check_password(self, password):
        return check_password_hash(self._password, password)


# 个人用户
class Personal(Base):
    __tablename__ = "personal"  # 个人用户信息表
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
            index=True,unique=True)# 所属会员
    name = db.Column(db.String(20))  # 用户姓名
    phone = db.Column(db.String(11))  # 用户电话
    jobyear = db.Column(db.Integer)  # 工作年限
    resume = db.Column(db.String(255))  # 简历
    personal_jobwanted = db.relationship('JobWanted', backref='personal')

    def __repr__(self):
        return "<Personal %r>" % self.name


# 企业用户
class Company(Base):
    __tablename__ = "company"  # 公司信息表
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    name = db.Column(db.String(100), unique=True)  # 公司名称
    address = db.Column(db.String(100))  # 公司地址
    url = db.Column(db.String(64)) # 公司官网
    phone = db.Column(db.String(11))  # 公司电话
    logo = db.Column(db.String(255))  # 公司logo
    summary = db.Column(db.Text)  # 公司简介
    field = db.Column(db.String(64)) # 公司所属领域
    financing = db.Column(db.String(64)) # 融资情况
    company_job = db.relationship('Job', backref='company', uselist=False)  # 工作外键关系

    def __repr__(self):
        return "<Company %r>" % self.name


# 工作
class Job(Base):
    __tablename__ = "job"  # 工作表
    id = db.Column(db.Integer, primary_key=True)  # 编号
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # 所属企业
    name = db.Column(db.String(100))  # 职位名称
    min_pay = db.Column(db.Integer)  # 最低薪酬
    max_pay = db.Column(db.Integer)  # 最高薪酬
    address = db.Column(db.String(100))  # 工作地点
    label = db.Column(db.String(255))  # 职位标签
    jobyear = db.Column(db.String(20))  # 工作年限要求
    education = db.Column(db.String(20))  # 工作学历要求
    description = db.Column(db.Text)
    job_JobWanted = db.relationship('JobWanted', backref='job')

    def __repr__(self):
        return "<Job %r>" % self.id


# 求职
class JobWanted(Base):
    __tablename__ = 'jobwanted'  # 求职表

    RESUME_PENDING = 1 # 处理中
    RESUME_INTERVIEW = 2 # 面试
    RESUME_IMPROPER = 3 # 不合适
    id = db.Column(db.Integer, primary_key=True)  # 编号
    personal_id = db.Column(db.Integer, db.ForeignKey('personal.id'))  # 所属个人用户
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))  # 所属工作
    # 在公司后台分页时,遇到InstrumentedList object has not query,所以增加这个字段
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # 所属公司
    state = db.Column(db.SmallInteger,default=RESUME_PENDING) # 处理状态


    def __repr__(self):
        return "<JobWanted %r>" % self.id
