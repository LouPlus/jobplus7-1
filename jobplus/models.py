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
    user_company_info = db.relationship('company_info', backref='user')  # 企业信息外键关系
    user_user_info = db.relationship('user_info', backref='user')  # 用户信息外键关系

    def __repr__(self):
        return "<User %r>" % self.name


# 个人用户
class User_ifo(db.Model):
    __tablename__ = "user_info"  # 用户信息表
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    name = db.Column(db.String(20))  # 用户姓名
    phone = db.Column(db.String(11))  # 用户电话
    jobyear = db.Column(db.Integer)  # 工作年限
    resume = db.Column(db.String(255))  # 简历

    def __repr__(self):
        return "<User %r>" % self.name


# 企业用户
class Company_info(db.Model):
    __tablename__ = "company_info"  # 公司信息表
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    name = db.Column(db.String(100), unique=True)  # 公司名称
    address = db.Column(db.String(100))  # 公司地址
    phone = db.Column(db.String(11))  # 公司电话
    logo = db.Column(db.String(255))  # 公司logo
    summary = db.Column(db.text)  # 公司简介

    def __repr__(self):
        return "<Company_info %r>" % self.name
