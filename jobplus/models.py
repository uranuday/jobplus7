from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)


class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    # 保存简历的文件名
    resume = db.Column(db.String(32))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='SET NULL'))
    company = db.relationship("Company", uselist=False)
    name = db.Column(db.String(32))
    phone = db.Column(db.Integer)
    working_years = db.Column(db.SmallInteger)
    is_disable = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    location = db.Column(db.String(128))
    logo_url = db.Column(db.String(128))
    website = db.Column(db.String(64),)
    slogan = db.Column(db.String(128))
    description = db.Column(db.String(2048), nullable=False)

    def __repr__(self):
        return '<Company: {}>'.format(self.name)

class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.String(32))
    location = db.Column(db.String(128))
    description = db.Column(db.String(2048))
    requirement = db.Column(db.String(2048))
    is_online = db.Column(db.Boolean, default=True)
    company = db.relationship('Company', uselist=False, backref=db.backref('jobs'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='SET NULL'))
    applicant = db.relationship('User', secondary="application", backref='applied_jobs')

    def __repr__(self):
        return '<Job: {}>'.format(self.name)

class Application(Base):
    APPLIED = 10    #申请
    REJECTED = 20   #拒绝
    INTERVIEW = 30  #面试

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'),primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    job = db.relationship('Job',uselist=False)
    user = db.relationship('User',uselist=False)
    status = db.Column(db.SmallInteger, default=APPLIED)


    def __repr__(self):
        return "<Application: {} - {}>".format(self.job.name, self.user.username)




