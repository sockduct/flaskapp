#!/usr/bin/env python3

from flask import Flask


app = Flask(__name__)
users = {'test': ''}
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

