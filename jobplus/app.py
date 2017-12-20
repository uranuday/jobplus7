from flask import Flask
from jobplus.models import db, User
from jobplus.config import configs
from flask_login import LoginManager





def register_blueprint(app):
    from .handlers import front, admin, user, company

    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(company)




def register_extensions(app):
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'





def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    register_blueprint(app)
    register_extensions(app)

    return app


