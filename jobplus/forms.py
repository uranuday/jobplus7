from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField, FileField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from flask import flash
from jobplus.models import db, User



class LoginForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Email()])
    password = PasswordField("密码", validators=[Required(), Length(6, 24)])
    remember_me = BooleanField("记住我")
    submit = SubmitField("提交")


    def validate_email(self, field):
        if field.data and not User.query.filter_by(email = field.data).first():
            raise ValidationError('用户未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError("密码错误")



class UserProfileForm(FlaskForm):
    name = StringField("姓名", validators=[Required()])
    email = StringField("邮箱", validators=[Required(), Email()])
    phone = IntegerField("手机号", validators=[Required(), NumberRange(min=10000000000, max=19999999999, message="无效手机号")])
    working_years = IntegerField("工作年限", validators=[Required(), NumberRange(min=1, max=99)])
    resume = FileField("简历")
    submit = SubmitField("保存")


    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash("更新成功", 'success')
        return user



class CompanyProfileForm(FlaskForm):
    name = StringField("名称", validators=[Required(), Length(128)])
    location = StringField("地址", validators=[Required(), Length(128)])
    logo_url = StringField("Logo URL", validators=[Length(128)])
    website = StringField("Web Site", validators=[Length(64)])
    slogan = StringField("Slogan", validators=[Length(128)])
    description = TextAreaField("描述", validators=[Required(), Length(2048)])
    submit = SubmitField("保存")

    
    def update_company(self, company):
        self.populate_obj(company)
        db.session.add(company)
        db.session.commit()
        flash("更新成功", 'success')
        return company



