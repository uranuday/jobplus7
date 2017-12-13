from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin




db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)





class User(Base, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    pass





class Job(Base):
    id = db.Column(db.Integer, primary_key = True)
    pass




class Company(Base):
    id = db.Column(db.Integer, primary_key = True)
    pass
