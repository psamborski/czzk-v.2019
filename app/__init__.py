from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# SECRET KEY
app.secret_key = '#'

# DATABASE
app.config.update(
    # source // SQLite: 'sqlite:///database/kurs.db'
    # create database <database_name> character set UTF8 collate utf8_bin
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://#',
    # set because of warning
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    # logs in terminal
    SQLALCHEMY_ECHO=False
)
db = SQLAlchemy(app)

# MAIL
app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='#',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='#',
    MAIL_PASSWORD='#',
    MAIL_DEFAULT_SENDER='#'
)
mail = Mail(app)

# AUTHENTICATION
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = 'CMS.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'Musisz się zalogować, by mieć dostęp do tej strony.'
login_manager.init_app(app)

# FILE UPLOAD
UPLOAD_FOLDER = app.root_path + '#'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from app import views
