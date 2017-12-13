from flask_sqlalchemy import AQLAlchemy
from datetime import datetime
from flask_login import UserMixin




db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.dateTime, default=datetime.utcnow, onupdate=datetime.utcnow)





class User(Base, UserMixin):
    pass





class Job(Base):
    pass




class Company(Base):
    pass
