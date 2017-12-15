from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash




db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)






class Company(Base):
    id = db.Column(db.Integer, primary_key = True)
    logo_url = db.Column(db.String(256))
    name = db.Column(db.String(64), unique=True, nullable=False)
    website = db.Column(db.String(64))
    slogan = db.Column(db.String(64))
    location = db.Column(db.String(256))
    description = db.Column(db.String(1024))



    def __repr__(self):
        return "<Company:{}>".format(self.name)






class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_APPLICANT = 10
    ROLE_RECRUITER = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    role = db.Column(db.SmallInteger, default = ROLE_APPLICANT)
    resume = db.Column(db.String(256))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))



    def __repr__(self):
        return "<User: {}>".format(self.name)






class Job(Base):

    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable=False)
    aslary = db.Column(db.String(64))
    experience = db.Column(db.String(64))
    location = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', uselist=False)
    description = db.Column(db.String(1024))
    requirement = db.Column(db.String(1024))
    is_online = db.Column(db.Boolean, default=True)
    applicant = db.relationship('User', secondary="application", backref='applied_jobs')



    def __repr__(self):
        return "<Job: {}>".format(self.name)



class Application(Base):

    APPLIED = 10
    REJECTED = 20
    INTERVIEW = 30

    __tablename__ = 'application'
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.SmallInteger, default=APPLIED)
    user = db.relationship('User')
    job = db.relationship('Job')



    def __repr__(self):
        return "<Application: {} - {}>".format(self.job.name, self.user.name)








