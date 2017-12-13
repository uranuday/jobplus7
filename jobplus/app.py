from flask import Flask
from jobplus.models import db, User, Job, Company






def register_blueprint(app):
    from .handlers import front

    app.register_blueprint(front)



