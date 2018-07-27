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


# �û�
class User(Base, UserMixin):
    __tablename__ = "user"  # �û���
    ROLE_USER = 10  # һ���û�
    ROLE_STAFF = 20  # ��ҵ�û�
    ROLE_ADMIN = 30  # ��������Ա
    id = db.Column(db.Integer, primary_key=True)  # ���
    name = db.Column(db.String(100), unique=True)  # ��Ա��
    email = db.Column(db.String(100))  # ����
    _password = db.Column('password',db.String(100))  # ����
    role = db.Column(db.SmallInteger, default=ROLE_USER)  # ��ɫ
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # ע��ʱ��
    user_company_info = db.relationship('Company', backref='user')  # ��ҵ��Ϣ�����ϵ
    user_user_info = db.relationship('Personal', backref='user')  # �����û���Ϣ�����ϵ

    def __repr__(self):
        return "<User %r>" % self.name

    #�û�����hash���ɺͼ���
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)


    def check_password(self, password):
        return check_password_hash(self._password, password)


        


# �����û�
class Personal(Base):
    __tablename__ = "personal"  # �����û���Ϣ��
    id = db.Column(db.Integer, primary_key=True)  # ���
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
            index=True,unique=True)# ������Ա
    name = db.Column(db.String(20))  # �û�����
    phone = db.Column(db.String(11))  # �û��绰
    jobyear = db.Column(db.Integer)  # ��������
    resume = db.Column(db.String(255))  # ����
    personal_jobwanted = db.relationship('JobWanted', backref='personal')

    def __repr__(self):
        return "<Personal %r>" % self.name


# ��ҵ�û�
class Company(Base):
    __tablename__ = "company"  # ��˾��Ϣ��
    id = db.Column(db.Integer, primary_key=True)  # ���
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # ������Ա
    name = db.Column(db.String(100), unique=True)  # ��˾����
    address = db.Column(db.String(100))  # ��˾��ַ
    phone = db.Column(db.String(11))  # ��˾�绰
    logo = db.Column(db.String(255))  # ��˾logo
    summary = db.Column(db.Text)  # ��˾���
    field = db.Column(db.String(64)) # ��˾��������
    financing = db.Column(db.String(64)) # �������
    company_job = db.relationship('Job', backref='company')  # ���������ϵ

    def __repr__(self):
        return "<Company %r>" % self.name


# ����
class Job(Base):
    __tablename__ = "job"  # ������
    id = db.Column(db.Integer, primary_key=True)  # ���
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # ������ҵ
    name = db.Column(db.String(100))  # ְλ����
    min_pay = db.Column(db.Integer)  # ���н��
    max_pay = db.Column(db.Integer)  # ���н��
    address = db.Column(db.String(100))  # �����ص�
    label = db.Column(db.String(255))  # ְλ��ǩ
    jobyear = db.Column(db.String(20))  # ��������Ҫ��
    education = db.Column(db.String(20))  # ����ѧ��Ҫ��
    description = db.Column(db.Text)
    job_JobWanted = db.relationship('JobWanted', backref='job')

    def __repr__(self):
        return "<Job %r>" % self.id


# ��ְ
class JobWanted(Base):
    __tablename__ = 'jobwanted'  # ��ְ��
    id = db.Column(db.Integer, primary_key=True)  # ���
    personal_id = db.Column(db.Integer, db.ForeignKey('personal.id'))  # ���������û�
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))  # ��������
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # Ͷ�ݼ���ʱ��

    def __repr__(self):
        return "<JobWanted %r>" % self.id
