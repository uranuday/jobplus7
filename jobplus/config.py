class BaseConfig(object):
    SECRET_KEY = '!!@@'
    UPLOAD_FOLDER = './uploads/'
    ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx', 'pdf'])
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024




class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/jobplus.db'
    TEMPLATES_AUTO_RELOAD = True




class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'
    



class TestingConfig(BaseConfig):
    pass





configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
        }
