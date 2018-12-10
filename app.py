#!/usr/bin/env python3

from dotenv import load_dotenv
from flask import flash, Flask, redirect, render_template, url_for
from flask_wtf import FlaskForm
import os
from secrets import token_urlsafe
from werkzeug import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError


app = Flask(__name__)
# __file__ is the full pathname of this module
basedir = os.path.abspath(os.path.dirname(__file__))
# Load environment variables from this file
load_dotenv(os.path.join(basedir, '.env'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or token_urlsafe()
users = {'test': ''}
test_passwd = os.environ.get('TEST_PASSWD')
users['test'] = test_passwd
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
        if username.data in users:
            raise ValidationError('Please use a different username.')


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    entry = TextAreaField('Journal Entry', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_title(self, title):
        if title.data in journals:
            raise ValidationError('Please use a different title.')


@app.route('/')
def main():
    return render_template('index.html', journals=journals)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        users[form.username.data] = generate_password_hash(form.password.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='User Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.username.data
        if user not in users or not check_password_hash(users[user], form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        return redirect(url_for('main'))
    return render_template('login.html', title='User Login', form=form)


@app.route('/logout')
def logout():
    return '<h1>User Logout</h1>'


@app.route('/entry', methods=['GET', 'POST'])
def entry():
    form = EntryForm()
    if form.validate_on_submit():
        journals[form.title.data] = {'text': form.entry.data}
        flash('Your entry is now live!')
        return redirect(url_for('main'))
    return render_template('entry.html', title='Create an Entry', form=form)

