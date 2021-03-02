from datetime import datetime
from server import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#for web
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    #User dpeneds on Employee
    emp_id = db.Column(db.String(20), db.ForeignKey('employee.emp_id'), nullable=False)
    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}', '{self.image_file}, '{self.password}')"
#for Notification
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #Post depneds on user_id 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

#for Face_Recognition
class Employee(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(20), nullable=False,primary_key=True)
    department = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(20), unique=False,nullable=False)
    user = db.relationship('User',backref='employee',lazy=True)
    record = db.relationship('Record',backref='personal',lazy=True)
    def __repr__(self):
        return f"Employee('{self.emp_id}', '{self.department}','{self.position}')"

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50), nullable=True, default =' ')
    date = db.Column(db.String(50), nullable=True, default =' ')
    late = db.Column(db.String(10), nullable=True, default =' ')
    
    emp_id = db.Column(db.String(20), db.ForeignKey('employee.emp_id'), nullable=False)  
    def __repr__(self):
        return f"Record('{self.emp_id}','{self.date}', '{self.time}')"


