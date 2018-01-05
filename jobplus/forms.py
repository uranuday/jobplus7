from flask_wtf import FlaskForm
#from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField, FileField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from flask import flash
from jobplus.models import db, User, Company, Job
from flask_login import current_user
import re



class LoginForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Email()])
    password = PasswordField("密码", validators=[Required(), Length(6, 24)])
    remember_me = BooleanField("记住我")
    submit = SubmitField("提交")


    def validate_email(self, field):
        if field.data and not User.query.filter_by(email = field.data).first():
            flash("用户未注册", 'danger')
            raise ValidationError('用户未注册')
        if field.data and User.query.filter_by(email = field.data).first().is_disable:
            flash("用户被禁用", 'danger')
            raise ValidationError('用户被禁用')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            flash("密码错误", 'danger')
            raise ValidationError("密码错误")


#用户基表单
class UserBaseForm(FlaskForm):
    username = StringField("用户名", validators=[Required(), Length(3,32)])
    email = StringField("邮箱", validators=[Required(), Email()])
    password = PasswordField("密码", validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField("重复密码", validators=[Required(), EqualTo('password', "密码不匹配")])
    name = StringField("姓名", validators=[Required(), Length(1, 30)])
    phone = IntegerField("手机号", validators=[Required(), NumberRange(min=10000000000, max=19999999999, message="无效手机号")])
    submit = SubmitField("保存")


    def add_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash("添加成功", 'success')
        return user


    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash("更新成功", 'success')
        return user



#企业基表单
class CompanyBaseForm(FlaskForm):
    company_name = StringField("公司名称", validators=[Required(), Length(0, 128)])
    location = StringField("地址", validators=[Required(), Length(0, 128)])
    logo_url = StringField("Logo URL", validators=[Length(0, 128)])
    website = StringField("Web Site", validators=[Length(0, 64)])
    slogan = StringField("Slogan", validators=[Length(0, 128)])
    description = TextAreaField("描述", validators=[Required(), Length(0, 2048)])
    submit = SubmitField("保存")


    def add_company(self):
        company = Company()
        self.populate_obj(company)
        db.session.add(company)
        db.session.commit()
        flash("添加成功", 'success')
        return user


    def update_company(self, company):
        self.populate_obj(company)
        db.session.add(company)
        db.session.commit()
    
        flash("更新成功", 'success')
        return company






class UserProfileForm(UserBaseForm):
    password = None
    repeat_password = None




class CompanyProfileForm(CompanyBaseForm):
    pass




class AddUserForm(UserBaseForm):
    user = None
    phone = None

    submit = SubmitField("提交")



    def validate_username(self, field):
        if not re.match('^\w*$', field.data):
            raise ValidationError("用户名只能包含字母和数字")
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已存在")


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已存在")



class UploadResumeForm(FlaskForm):
    resume = FileField("更新简历", validators=[Required()])
    submit = SubmitField("提交")




class AddCompanyForm(UserBaseForm, CompanyBaseForm):
    name = None
    phone = None
    location = None
    logo_url = None
    website = None
    slogan = None
    description = None

    submit = SubmitField("提交")


    def validate_username(self, field):
        if not re.match('^\w*$', field.data):
            raise ValidationError("用户名只能包含字母和数字")
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已存在")


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已存在")


    def validate_company_name(self, field):
        if Company.query.filter_by(company_name=field.data).first():
            raise ValidationError("公司已存在")


    def add_company_user(self):
        company = Company()
        user = User()


        self.populate_obj(company)
        self.populate_obj(user)
        user.company = company
        user.role = user.ROLE_COMPANY

        db.session.add(user)
        db.session.add(company)
        db.session.commit()

        flash("更新成功", 'success')

        return [user, company]






class EditUserForm(UserBaseForm):
    pass



class EditCompanyForm(UserBaseForm, CompanyBaseForm):
    phone = None
    name = None
    submit = SubmitField("保存")


    def update_company_user(self, user):
        company = user.company


        self.populate_obj(company)
        self.populate_obj(user)

        db.session.add(user)
        db.session.add(company)
        db.session.commit()

        flash("更新成功", 'success')

        return [user, company]



class JobBaseForm(FlaskForm):
    job_title = StringField("职位名称", validators=[Required(), Length(1, 120)])
    salary = StringField("薪资范围", validators=[Required(), Length(1, 30)])
    location = StringField("地点", validators=[Required(), Length(1, 120)])
    exp_requirement = StringField("经验要求", validators=[Required(), Length(1, 30)])
    edu_requirement = StringField("学历要求", validators=[Required(), Length(1, 30)])
    description = TextAreaField("职位描述", validators=[Required(), Length(1, 2000)])
    requirements = TextAreaField("职位要求", validators=[Required(), Length(1, 2000)])
    submit = SubmitField("提交")


    def add_job(self):
        job = Job()
        self.populate_obj(job)
        job.company = current_user.company

        db.session.add(job)
        db.session.commit()

        flash("职位添加成功", 'success')

        return job

    def update_job(self, job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()

        flash("职位更新成功", 'success')

        return job




