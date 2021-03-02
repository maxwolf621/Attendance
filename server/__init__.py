import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#SECURITY_EMAIL_SENDER = os.environ.get("MAIL")
#app.config['MAIL_USE_SSL'] = False
#enviroment variable 
app.config['MAIL_USERNAME'] ='jervismayer@gmail.com'
app.config['MAIL_PASSWORD'] ='Ji3ul4fm42k6eji6'

mail = Mail(app)
from server import routes
