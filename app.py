import os

from flask import Flask, render_template, request, session, redirect, url_for, flash

from util import user, exercise, water, food #sleep

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
        username = session['username']
        user_data = user.get_info(username)
        # print(user_data)
        return render_template('profile.html', user=username, user_data=user_data)
    except:
        flash("You must be logged in to access this page.")
        return redirect('/')

@app.route('/user_info', methods = ['POST'])
def user_info():
    username = session['username']
    age = request.form['age']
    height = request.form['height']
    weight = request.form['weight']
    allergies = request.form['allergies']
    dietary_restrictions = request.form['dietary_restrictions']

    if user.add_info(age, height, weight, allergies, dietary_restrictions, username):
        flash("Changes successfully saved!")
    else:
        flash("Changes could not be saved.")
    return redirect(url_for('profile'))

@app.route('/sleep', methods=["GET", "POST"])
def sleep():
    return render_template('sleep.html')

@app.route('/water', methods=["GET", "POST"])
def water_disp():
    print(session)
    try:
        username = session['username']
        water.get_user_water(username)
        all_water = water.get_user_water(username)
        if request.method == 'GET':
            return render_template('water.html', total = all_water, percentage = water.calc_percentage(username))
        else:
            type = int(request.form['measure'])
            #print(type)
            input = int(request.form['inputW'])
            #print(input)
            amount = water.convert_measure(type, input)
            print("converted amount:")
            print(amount)
            print(username)
            print(water.update_user_log(username, amount))
            if (water.update_user_log(username, amount) == True):
                flash("Water log successfully updated!")
            else:
                flash("Input field cannot be empty.")
            return render_template('water.html', total = all_water, percentage = water.calc_percentage(username))

    except:
        flash("You must be logged in to access this page.")
        #print(session)
        return redirect('/')

@app.route('/nutrients')
def nutrients():
    return render_template('nutrients.html')

@app.route('/exercise', methods=["GET", "POST"])
def exercise_options():
    try:
        username = session['username']
        all_categories = exercise.get_all_categories()
        hours = exercise.get_user_exercise(username)
        category = exercise.get_user_category(username)
        if category != None:
            category = "You worked on "+category+" today."
        else:
            category = "You haven't worked out today."
        if request.method == 'GET':
            return render_template('exercise.html', all_categories=all_categories, can_view_results=False, hours=hours, category=category)
        else:
            if request.form['submit'] == "Search":
                user_request = request.form['user_request']
                results = exercise.list_category_exercises(exercise.get_category_id(user_request))
                return render_template('exercise.html', all_categories=all_categories, results=results, can_view_results=True, hours=hours, category=category)
            else:
                user_hours = request.form['hours']
                user_category = request.form['user_category']
                if exercise.update_user_log(user_hours, user_category, username) == True:
                    category = "You worked on "+exercise.get_user_category(username)+" today."
                    flash("Exercise log successfully updated!")
                    hours = exercise.get_user_exercise(username)
                else:
                    flash("Hours and category cannot be empty.")
                return render_template('exercise.html', all_categories=all_categories, can_view_results=False, hours=hours, category=category)
    except:
        flash("You must be logged in to access this page.")
        return redirect('/')



if __name__ == "__main__":
    app.debug = True
    app.run()
