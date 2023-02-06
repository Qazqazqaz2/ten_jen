import psycopg2
import psycopg2.extensions
from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import  SQLAlchemy
conn = psycopg2.connect(
    host="localhost",
    database="ten_jen",
    user="postgres",
    password="762341Aa",
    port=5432)

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

UPLOAD_FOLDER = r'/home/Armianin/Work/jen_ten'
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY'] ='6LeBCfIZAAAAAO39_L4Gd7f6uCM0PfP_N3XjHxkW'
app.config['RECAPTCHA_PRIVATE_KEY'] ='6LeBCfIZAAAAAJTjq0Xz_ndAW9LByCo1nJJKy'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'black'}
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db_cursor = conn.cursor()
