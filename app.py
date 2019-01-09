import os

from flask import Flask, render_template, request, session, redirect, url_for, flash

from util import user

import os
app = Flask(__name__) #create instance of class flask

app.secret_key = os.urandom(32)


@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html",session = session)

@app.route('/signup')
def signup():
    '''This function renders the HTML template for the signup page.'''
    return render_template('signup.html')

@app.route('/register_auth', methods = ['POST'])
def register_auth():
    '''This function checks the form on the signup page and calls register() to register the user into the database.'''
    username = request.form['username']
    password = request.form['password']
    confirmed_pass = request.form['confirmedPassword']
    if username == "":
        flash("Please make sure to enter a username!")
        return redirect(url_for('signup'))
    elif password == "":
        flash("Please make sure to enter a password!")
        return redirect(url_for('signup'))
    elif password != confirmed_pass: # checks to make sure two passwords entered are the same
        flash("Please make sure the passwords you enter are the same.")
        return redirect(url_for('signup'))
    else:
        if user.register(username, password):
            flash("You have successfully registered.")
        else:
            flash("Please enter another username. The one you entered is already in the database.")
            return redirect(url_for('signup'))
    return redirect('/login')


@app.route('/login')
def login():
    '''This function renders the HTML template for the login page.'''
    return render_template('login.html')

@app.route('/login_auth', methods = ['POST'])
def login_auth():
    '''This function calls authenticate() to check if the form's username and password match the database. If successful, this function redirects the user to the home page.'''
    username = request.form['username']
    password = request.form['password']

    if user.authenticate(username, password):
        session['username'] = username
        flash("You have successfully logged in.")
        return redirect('/')
    else:
        flash("Invalid username and password combination")
        return render_template('login.html')

@app.route('/logout')
def logout():
    '''This function removes the username from the session, logging the user out. Redirects user to home page.'''
    session.pop('username') # ends session
    flash("You have successfully logged out.")
    return redirect('/')

@app.route('/profile')
def profile():
    '''This function renders the HTML template for the profile page.'''
    try:
        user = session['username']
        return render_template('profile.html', user=user)
    except:
        flash("You must be logged in to access this page.")
        return redirect('/')

@app.route('/user_info', methods = ['POST'])
def user_info():
    username = session['username']
    height = request.form['height']
    weight = request.form['weight']
    if user.add_info(height, weight, username):
        flash("Changes successfully saved!")
    else:
        flash("Changes could not be saved.")
    return redirect(url_for('profile'))

if __name__ == "__main__":
    app.debug = True
    app.run()
