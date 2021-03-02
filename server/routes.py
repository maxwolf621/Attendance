import os, smtplib
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from server import app, db, bcrypt, mail
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from server.forms import LoginForm, UpdateAccountForm, PostForm, ContactForm
from server.models import User,Post,Record,Employee
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/home")
@login_required
def home():
    #pages 
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    '''
        For employee that do the login
        It would 
        1. check validity of email such as ~@gamil.com etc...
        2. via digest to compare user input password and password in the DB
    '''
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Login Failed,Please Check Your Email' , 'danger')
            return render_template('login.html', title='Login', form=form)
        
        '''
            To compare hashpassword (backend and user-input)
        '''
        hashed_password=bcrypt.generate_password_hash(user.password)
        if bcrypt.check_password_hash(hashed_password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            #return '<p>White Test two Digests are The Same</p>'
        else:
            #return 'White Test two Digests are not The Same'
            flash('Login Failed,Please check your Password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    '''
    save picture of employee in the directory ../static/profile_pics
    '''
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    '''
    normalize the picture
    '''
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/attendance",methods=['GET'])
@login_required
def attendance():
    '''
    Check Attendnace of Employee by querying from DB
    '''
    headings=("Empolyee ID","Time","Date","Late")
    record = db.session.query(Record.emp_id,Record.time,Record.date,Record.late).filter_by(emp_id=current_user.emp_id).all()
    page = request.args.get('page', 1, type=int)
    records = Record.query.paginate(page=page, per_page=5)
    return render_template('attendance.html', title='Attendance',headings= headings ,records = record)

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    '''
    update account after user/employee modifying
    or
    user/employee checks personal Information
    '''
    form = UpdateAccountForm()
    if form.validate_on_submit():
        '''
            Edit the personal information 
        '''
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    '''
        user makes a new post
    '''
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@app.route("/apply",methods=['Get','Post'])
@login_required
def apply():
    ''' 
    Contact or Apply for something 
    to System Administor 
    '''
 
    form = ContactForm() 
    print(current_user.email)
    print("YOYO")
    if request.method == 'POST':
        if form.validate() == False:
            flash('Warning!! FORMAT ERROR' , 'danger')
            return render_template('apply.html', form=form)
        else:
            msg = Message(form.subject.data, 
                          sender=os.environ.get('EMAIL_USER'),
                          recipients=[current_user.email])
    
            msg.html = f'<h1 style="border:2px solid DodgerBlue;">A Requirment From EmployID : \
                        {form.employeeid.data} , Email : {form.email.data} \
                        </h1> <h1 style="color:MediumSeaGreen;">context : {form.context.data}</h1> <br>\
                        <bstyle="color:#FF4E4F" > </b>'
            
            mail.send(msg)
            if form.employeeid.data != current_user.emp_id :
                flash("Employee ID should be youself" ,'danger')
                return render_template('apply.html', form=form)

            flash("Your Requirement has been sent.  We will Reply you as Soon as Possible" ,'success')
            return redirect(url_for('home'))

    elif request.method == 'GET': 
        form.employeeid.data = current_user.emp_id
        form.email.data = current_user.email
        return render_template('apply.html', title='Apply', form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
