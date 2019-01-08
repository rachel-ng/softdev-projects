import os

from flask import Flask, render_template, request, session, redirect, url_for, flash

from util import user

import os
app = Flask(__name__) #create instance of class flask

app.secret_key = os.urandom(32)


@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    '''This function renders the HTML template for the signup page.'''
    return render_template('signup.html')

@app.route('/login')
def login():
    '''This function renders the HTML template for the login page.'''
    return render_template('login.html')
    
if __name__ == "__main__":
    app.debug = True
    app.run()
