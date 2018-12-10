#!/usr/bin/env python3

from dotenv import load_dotenv
from flask import Flask, render_template
import os
from werkzeug import check_password_hash, generate_password_hash


app = Flask(__name__)
# __file__ is the full pathname of this module
basedir = os.path.abspath(os.path.dirname(__file__))
# Load environment variables from this file
load_dotenv(os.path.join(basedir, '.env'))
users = {'test': ''}
test_passwd = os.environ.get('TEST_PASSWD')
users['test'] = test_passwd
journals = {'Test': {'user': 'test',
                     'title': 'Bootstrap',
                     'text': 'This is a test journal entry.'},
            'Two': {'user': 'test',
                    'title': 'Sequel',
                    'text': 'How about one more test entry.  This allows a '
                            'little better validation.'}
           }


@app.route('/')
def main():
    return render_template('index.html', journals=journals)


@app.route('/register')
def register():
    return render_template('register.html', title='User Sign Up')


@app.route('/login')
def login():
    return render_template('login.html', title='User Login')


@app.route('/logout')
def logout():
    return '<h1>User Logout</h1>'


@app.route('/entry')
def entry():
    return render_template('entry.html', title='Create an Entry')

