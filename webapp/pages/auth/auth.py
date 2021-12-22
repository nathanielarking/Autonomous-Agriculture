from flask import Blueprint, render_template, request, flash, redirect, url_for
from data.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from webapp import db
from flask_login import login_user, login_required, logout_user, current_user 
import logging

#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

#Create blueprint object to hold URLs
auth_blueprint = Blueprint('auth_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

@auth_blueprint.route('/auth/login', methods=['GET', 'POST'])
def login():
    #When a message is sent with the POST form, AKA the form submission
    if request.method =='POST':
        #Assign variables from request
        email = request.form.get('email')
        password = request.form.get('password')

        #Search database for user with matching email
        user = db.session.query(User).filter(User.email==email).first()
        #If that user is found, else flash error
        if user:
            #If password is correct, else flash error
            if check_password_hash(user.password, password):
                flash('Successfully logged in!', category='success')
                login_user(user, remember=True)
                logging.info(f'User logged in, email:{email}, username:{user.username}')
                return redirect(url_for('home_blueprint.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('auth/login.html', user=current_user, palette=palette)

@auth_blueprint.route('/auth/logout')
@login_required
def logout():
    logging.info(f'User logged out, email:{current_user.email}, username:{current_user.username}')
    logout_user()
    return redirect(url_for('auth_blueprint.login'))

@auth_blueprint.route('/auth/signup', methods=['GET', 'POST'])
def signup():
    #When a message is sent with the POST form, AKA the form submission
    if request.method == 'POST':
        #Assign variables from request
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #Respond based on input, else is called if account creation is successful
        user = db.session.query(User).filter(User.email==email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) <= 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) <= 2:
            flash('Username must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) <= 7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            #Create a new instance of the user class
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            #Add and commit to database
            db.session.add(new_user)
            db.session.commit()
            #Flash to user and redirect them to the home page
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            logging.info(f'New account created, email:{email}, username:{username}')
            return redirect(url_for('home_blueprint.home'))

    return render_template('auth/signup.html', user=current_user, palette=palette)