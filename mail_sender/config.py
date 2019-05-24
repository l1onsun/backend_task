import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'strong-password'
    #SECURITY_PASSWORD_SALT = 'password-salt'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'l7onsun@gmail.com'
    MAIL_PASSWORD = '1110002229996g'