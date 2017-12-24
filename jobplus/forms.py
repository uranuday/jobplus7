from flask_wtf import FlaskForm
#from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField, FileField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from flask import flash
from jobplus.models import db, User, Company



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
    submit = SubmitField("保存")



    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash("更新成功", 'success')
        return user



class CompanyProfileForm(FlaskForm):
    name = StringField("名称", validators=[Required(), Length(0, 128)])
    location = StringField("地址", validators=[Required(), Length(0, 128)])
    logo_url = StringField("Logo URL", validators=[Length(0, 128)])
    website = StringField("Web Site", validators=[Length(0, 64)])
    slogan = StringField("Slogan", validators=[Length(0, 128)])
    description = TextAreaField("描述", validators=[Required(), Length(0, 2048)])
    submit = SubmitField("保存")



    def update_company(self, company):
        self.populate_obj(company)
        db.session.add(company)
        db.session.commit()
        flash("更新成功", 'success')
        return company






class AddUserForm(FlaskForm):
    username = StringField("用户名", validators=[Required(), Length(3,32)])
    email = StringField("邮箱", validators=[Required(), Email()])
    password = PasswordField("密码", validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField("重复密码", validators=[Required(), EqualTo('password', "密码不匹配")])
    name = StringField("姓名", validators=[Required(), Length(1, 30)])
    phone = IntegerField("手机号", validators=[Required(), NumberRange(min=10000000000, max=19999999999, message="无效手机号")])
    submit = SubmitField("添加")



    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已存在")


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已存在")



    def add_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash("添加成功", 'success')
        return user




class UploadResumeForm(FlaskForm):
    resume = FileField("简历", validators=[Required()])
    submit = SubmitField("提交")




class AddCompanyForm(FlaskForm):
    username = StringField("用户名", validators=[Required(), Length(3,32)])
    email = StringField("邮箱", validators=[Required(), Email()])
    password = PasswordField("密码", validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField("重复密码", validators=[Required(), EqualTo('password', "密码不匹配")])
    company_name = StringField("公司名称", validators=[Required(), Length(1, 120)])
    website = StringField("企业网站", validators=[Required(), Length(1, 64)])
    logo_url = StringField("LOGO链接", validators=[Required(), Length(1, 120)])
    slogan = StringField("Slogan", validators=[Required(), Length(1, 120)])
    description = TextAreaField("企业介绍", validators=[Required(), Length(10, 2000)])
    submit = SubmitField("添加")



    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已存在")


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已存在")


    def validate_company_name(self, field):
        if Company.query.filter_by(name=field.data).first():
            raise ValidationError("公司已存在")


    def add_company(self):
        company = Company()
        user = User()

        company.name = self.company_name.data
        company.website = self.website.data
        company.logo_url = self.logo_url.data
        company.slogan = self.slogan.data
        company.description = self.description.data

        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        user.company = company
        user.role = 20


        db.session.add(user)
        db.session.add(company)
        db.session.commit()

        flash("更新成功", 'success')

        return [user, company]







