#!/usr/bin/env python3

from dotenv import load_dotenv
from flask import flash, Flask, redirect, render_template, url_for
from flask_login import (current_user, LoginManager, login_user, logout_user,
                         login_required)
from flask_wtf import FlaskForm
import os
from secrets import token_urlsafe
from user import User
from werkzeug import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError


# Instantiate Flask:
app = Flask(__name__)
#
# Load relevant environment variables:
# __file__ is the full pathname of this module
basedir = os.path.abspath(os.path.dirname(__file__))
# Load environment variables from this file
load_dotenv(os.path.join(basedir, '.env'))
#
# Setup Flask Environment:
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or token_urlsafe()
#
# Setup Flask Extensions:
login_manager = LoginManager(app)
login_manager.login_view = 'login'
#
# Setup test user
users = {}
username = 'test'
test_passwd = os.environ.get('TEST_PASSWD')
users[username] = User('test', '', passwd_hash=test_passwd)
#
# Setup test journal entries
journals = {'Test': {'user': 'test',
                     'text': 'This is a test journal entry.'},
            'Two': {'user': 'test',
                    'text': 'How about one more test entry.  This allows a '
                            'little better validation.'}
           }


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.exists(username.data):
            raise ValidationError('Please use a different username.')


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    entry = TextAreaField('Journal Entry', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_title(self, title):
        if title.data in journals:
            raise ValidationError('Please use a different title.')


# Used by Flask-Login
@login_manager.user_loader
def load_user(id):
    # This is awful - only doing to avoid using a database!
    for user in users:
        if users[user].id == int(id):
            return users[user]


@app.route('/')
def main():
    return render_template('index.html', journals=journals)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        users[form.username.data] = User(form.username.data, form.password.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='User Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = form.username.data
        if not User.exists(user) or not users[user].check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(users[user])
        flash(f'Welcome back {user}!')
        return redirect(url_for('main'))
    return render_template('login.html', title='User Login', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        flash(f'Goodbye {current_user.username}!')
    logout_user()
    return redirect(url_for('main'))


@app.route('/entry', methods=['GET', 'POST'])
@login_required
def entry():
    form = EntryForm()
    if form.validate_on_submit():
        journals[form.title.data] = {'text': form.entry.data,
                                     'user': current_user.username}
        flash('Your entry is now live!')
        return redirect(url_for('main'))
    return render_template('entry.html', title='Create an Entry', form=form)

