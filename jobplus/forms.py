from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField
from wtforms.validators import Length, Email,EqualTo, Required, URL, NumberRange
from jobplus.models import db, User


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






