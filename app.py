#!/usr/bin/env python3

from dotenv import load_dotenv
from flask import Flask
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
                     'text': 'This is a test journal entry.'}}


@app.route('/')
def main():
    return '<h1>Welcome to the Journal!</h1>'


@app.route('/register')
def register():
    return '<h1>User Sign Up</h1>'


@app.route('/login')
def login():
    return '<h1>User Login</h1>'


@app.route('/logout')
def logout():
    return '<h1>User Logout</h1>'


@app.route('/entry')
def entry():
    return '<h1>Create A Journal Entry</h1>'

