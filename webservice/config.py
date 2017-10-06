class Config(object):
    DEBUG = False

    TESTING = False

    SECRET_KEY = 'SOPA_DE_CARACOL'

    SQLALCHEMY_TRACK_MODIFICATIONS = False,

# class Production(Config):
#     DATABASE_URI = 'mysql://root@localhost/flask_blog'

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask_blog'
