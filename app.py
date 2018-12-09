#!/usr/bin/env python3

from flask import Flask


app = Flask(__name__)


@app.route('/')
def main():
    return '<h1>Welcome to the Journal!</h1>'

