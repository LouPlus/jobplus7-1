from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()


# 用户
class User(db.Model):
    __tablename__ = "user"  # 用户表
    ROLE_USER = 10  # 一般用户
    ROLE_STAFF = 20  # 企业用户
    ROLE_ADMIN = 30  # 超级管理员
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 会员名
    email = db.Column(db.String(100))  # 邮箱
    password = db.Column(db.String(100))  # 密码
    db.Column(db.SmallInteger, default=ROLE_USER)  # 角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 注册时间
    user_company_info = db.relationship('company', backref='user')  # 企业信息外键关系
    user_user_info = db.relationship('personal', backref='user')  # 个人用户信息外键关系

    def __repr__(self):
        return "<User %r>" % self.name


# 个人用户
class Personal(db.Model):
    __tablename__ = "personal"  # 个人用户信息表
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    name = db.Column(db.String(20))  # 用户姓名
    phone = db.Column(db.String(11))  # 用户电话
    jobyear = db.Column(db.Integer)  # 工作年限
    resume = db.Column(db.String(255))  # 简历
    personal_jobwanted = db.relationship('jobwanted', backref='personal')

    def __repr__(self):
        return "<Personal %r>" % self.name


# 企业用户
class Company(db.Model):
    __tablename__ = "company"  # 公司信息表
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    name = db.Column(db.String(100), unique=True)  # 公司名称
    address = db.Column(db.String(100))  # 公司地址
    phone = db.Column(db.String(11))  # 公司电话
    logo = db.Column(db.String(255))  # 公司logo
    summary = db.Column(db.Text)  # 公司简介
    company_job = db.relationship('job', backref='company')  # 工作外键关系

    def __repr__(self):
        return "<Company %r>" % self.name


# 工作
class Job(db.Model):
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
    job_describe = db.Column(db.Text)
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 创建工作时间
    job_JobWanted = db.relationship('jobwanted', backref='job')

    def __repr__(self):
        return "<Job %r>" % self.id


# 求职
class JobWanted(db.Model):
    __tablename__ = 'jobwanted'  # 求职表
    id = db.Column(db.Integer, primary_key=True)  # 编号
    personal_id = db.Column(db.Integer, db.ForeignKey('personal.id'))  # 所属个人用户
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))  # 所属工作
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 投递简历时间

    def __repr__(self):
        return "<JobWanted %r>" % self.id
