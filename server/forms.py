from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from server.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired("Enter Your Password")])
    
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Employee Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email("Wrong Format")])
    picture = FileField('Update Your Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Confirm')
    

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username Already EXIST')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The Mail Already EXIST')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    
class ContactForm(FlaskForm):
    employeeid = StringField("EmployeeID",  validators=[DataRequired("Please Enter Your ID.")])
    email = StringField("Email",  validators=[DataRequired("Wrong FORMAT."),Email("Wrong Format")])
    subject = StringField("Subject",  validators=[DataRequired("Please Enter A Subject.")])
    context = TextAreaField("Context",  validators=[DataRequired("Please Enter A Context.")])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Send")
    
