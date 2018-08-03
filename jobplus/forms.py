from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField
from wtforms.validators import Length, Email,EqualTo, Required, URL, NumberRange, Optional, URL, AnyOf
from jobplus.models import db, User, Company, Personal


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.user = user
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误或用户不存在')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('确定')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')

    def create_user(self, user):
        db.session.add(user)
        db.session.commit()
        return user


class PersonalForm(FlaskForm):
    name = StringField('真实名', validators=[Required(), Length(1, 5)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码(不填不改变)')
    phone = StringField('手机号', validators=[Required(), Length(11,12)])
    jobyear = IntegerField('工作年限', validators=[Required(),NumberRange(0,100)])
    #file upload
    resume = FileField('简历',validators=[
        FileRequired(),
        FileAllowed(['doc','docx','pdf'],'doc only')]
        )
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱错误')

    def validate_password(self,field):
        if field.data:
            if 6 <= len(field.data) <= 12:
                raise validationError('密码必须6｀12位')

    def create_person(self, person):
        db.session.add(person)
        db.session.commit()


class JobForm(FlaskForm):

    name = StringField('职位名称', validators=[Required(), Length(1,10)])
    min_pay = IntegerField('最低薪酬', validators=[Required(),Length(0,8)])
    max_pay = IntegerField('最高薪酬', validators=[Required(),Length(0,8)])
    address = StringField('工作地点',validators=[Length(0,49)])
    label = StringField('标签',validators=[Length(0,4)])
    jobyear = IntegerField('工作年限', validators=[Required(),NumberRange(0,100)])
    education = StringField('学历要求', validators=[Required()])
    description = TextAreaField('职位描述',validators=[Required()])
    submit = SubmitField('提交')

    def validate_max_pay(self,filed):
        if field.data < self.min_pay:
            raise ValidationError('最高薪酬不小于最低薪酬')

    def create_job(self,job):
        db.session.add(job)
        db.session.commit()


#公司表单类
class CompanyForm(FlaskForm):
    # 公司名称创建时需要验证
    name = StringField('公司名称', validators=[Required(), Length(1,30)])
    address = StringField('地址', validators=[Required(), Length(1,49)])
    url = StringField('官网(可选)', validators=[Optional(), URL(), Length(1,64)])
    phone = StringField('电话', validators=[Required(),Length(8,11)])
    logo = FileField('logo(可选)',validators=[
        Optional(),
        FileRequired(),
        FileAllowed(['png'],'png only')]
        )
    summary = StringField('简介', validators=[Required(), Length(5,30)])
    field = StringField('领域', validators=[Required(), Length(2,10)])
    financing = StringField('融资情况(可选)', validators=[Optional(),AnyOf(('A轮','B轮','C轮','天使轮'))])
    submit =SubmitField('提交')

    def validate_phone(self,field):
        if not field.data.isdigit():
            raise ValidationError('只由数字组成')
    def create_company(self, company):
        db.session.add(company)
        db.session.commit()


# 管理员编辑用户表单
class UsereditForm(FlaskForm):
    name = StringField('真实名', validators=[Required(), Length(1, 5)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码(不填不改变)', validators=[Optional(), Length(6,12)])
    phone = StringField('手机号', validators=[Required(), Length(11,12)])
    submit = SubmitField('提交')

#管理员修改公司表单类
class CompanyeditForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码(不填不改变)', validators=[Optional(), Length(6,12)])
    # 公司名称创建时需要验证
    name = StringField('公司名称', validators=[Required(), Length(1,30)])
    url = StringField('官网(可选)', validators=[Optional(), URL(), Length(1,64)])
    summary = StringField('简介', validators=[Required(), Length(5,30)])
    submit = SubmitField('提交')


