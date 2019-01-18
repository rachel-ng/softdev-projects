import os

from flask import Flask, render_template, request, session, redirect, url_for, flash

from util import user, exercise, water, food, sleep, plotly_charts, chart_data

app = Flask(__name__) #create instance of class flask

app.secret_key = os.urandom(32)


@app.route("/", methods = ["GET", "POST"])
def index():
    '''This function renders the home page, which includes all the user's information if logged in. It also allows the user to input a daily goal.'''
    if 'username' in session:
        username = session['username']
        exercise_hours = exercise.get_user_exercise(session['username'])
        exercise_last_category = exercise.get_user_category(session['username'])
        if exercise_last_category != None:
            exercise_last_category = "You last worked on "+exercise_last_category+" today."
        else:
            exercise_last_category = "You haven't worked out today."
        calories = food.get_total_calories(session['username'])
        carbs = food.get_total_carbs(session['username'])
        protein = food.get_total_protein(session['username'])
        fat = food.get_total_fat(session['username'])
        all_water = water.get_user_water(session['username'])

        # handle updating the user's daily goal on the page
        goal = user.get_user_goal(username)
        if goal == None:
            goal = ""
        if request.method == 'GET':
            return render_template("index.html", session=session, all_water=all_water,exercise_hours=exercise_hours, exercise_last_category=exercise_last_category, calories=calories, carbs=carbs, protein=protein, fat=fat, goal=goal)
        else:
            goal = request.form['goal']
            if (user.update_user_goal(username, goal) == True):
                flash("Daily goal successfully updated!")
                goal = user.get_user_goal(username)
            else:
                flash("Something went wrong! Uh oh")
        return render_template("index.html", session=session, all_water=all_water,exercise_hours=exercise_hours, exercise_last_category=exercise_last_category, calories=calories, carbs=carbs, protein=protein, fat=fat, goal=goal)

    return render_template("index.html", session=session)

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
    '''This function calls the add_info function to update the user's basic information in the database based on the form submitted by the user.'''
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
def sleep_disp():
    '''This function renders the sleep page with the user's information displayed. It receives the form submitted by the user and passes it to the sleep functions to update sleep log and calculate sleep.'''
    try:
        username = session['username']
        last_sleep = sleep.get_user_sleep(username)

        plotly_charts.sleep_chart(chart_data.get_user_sleep(username), "sleep")

        if request.method == 'GET':
            return render_template('sleep.html', past = last_sleep)
        else:
            starthr = int(request.form['hour1'])
            startmin = int(request.form['minutes1'])
            startx = int(request.form['group1'])
            # print("Start time: "+start_time)

            endhr = int(request.form['hour2'])
            endmin = int(request.form['minutes2'])
            endx = int(request.form['group2'])
            if endx == 0 and startx == 1:
                endx = 1
                startx = 0
            start_time = sleep.convert(starthr, startmin, startx)

            end_time = sleep.convert(endhr, endmin, endx)
            # print("End Time: "+end_time)
            total_time = sleep.get_diff(start_time, end_time)

            if (sleep.update_user_log(username, total_time, start_time) == True):
                flash("Sleep log successfully updated!")
                last_sleep = sleep.get_user_sleep(username)

                plotly_charts.sleep_chart(chart_data.get_user_sleep(username), "sleep")
            else:
                flash("Something went wrong! Uh oh")

            return render_template('sleep.html', past = last_sleep)

    # if there are errors, redirect to the home page
    except:
        flash("You must be logged in to access this page.")
        #print(session)
        return redirect('/')

@app.route('/water', methods=["GET", "POST"])
def water_disp():
    '''This function renders the water intake page with the user's information displayed. It receives the form submitted by the user and passes it to the water functions to convert the measure and update water log.'''
    try:
        username = session['username']
        all_water = water.get_user_water(username)

        plotly_charts.bar_chart(chart_data.get_user_water(username), "water", "rgb(88,180,197)")

        if request.method == 'GET':
            return render_template('water.html', total = all_water, percentage = water.calc_percentage(username))
        else:
            type = int(request.form['measure'])
            #print(type)
            input = request.form['inputW']
            amount = water.convert_measure(type, int(input))
            if (water.update_user_log(username, amount) == True):
                flash("Water log successfully updated!")
                all_water = water.get_user_water(username)

                plotly_charts.bar_chart(chart_data.get_user_water(username), "water", "rgb(88,180,197)")
            else:
                flash("Input amount of water")

            return render_template('water.html', total = all_water, percentage = water.calc_percentage(username))

    # if there are errors, redirect to the home page
    except:
        flash("You must be logged in to access this page.")
        #print(session)
        return redirect('/')

@app.route('/nutrients', methods=["GET", "POST"])
def nutrients():
    '''This function renders the nutrition page with the user's information displayed. It receives the form submitted by the user and passes it to the food functions to update the food log with the meal and the amount eaten.'''
    try:
        username = session['username']

        plotly_charts.macros_chart([food.get_total_carbs(username), food.get_total_protein(username), food.get_total_fat(username)], "macros")
        plotly_charts.calorie_chart(chart_data.get_user_food(username), "calories")

        if request.method == 'GET':
            today_food = food.get_user_food(username)
            total_calories = food.get_total_calories(username)
            total_carbs = food.get_total_carbs(username)
            total_protein = food.get_total_protein(username)
            total_fat = food.get_total_fat(username)
            # print(today_food)
            return render_template('nutrients.html', today_food=today_food, calories=total_calories, carbs=total_carbs, fat=total_fat, protein=total_protein)
        else:
            user_meal = request.form['meal']
            user_amount = request.form['amount']
            if user_meal == '' or user_amount == '':
                today_food = food.get_user_food(username)
                total_calories = food.get_total_calories(username)
                total_carbs = food.get_total_carbs(username)
                total_protein = food.get_total_protein(username)
                total_fat = food.get_total_fat(username)
                print(today_food)
                flash("Your meal or amount cannot be empty.")
                return render_template('nutrients.html', today_food=today_food, calories=total_calories, carbs=total_carbs, fat=total_fat, protein=total_protein)

            if food.add_food(user_meal, user_amount, username) == True:
                today_food = food.get_user_food(username)
                total_calories = food.get_total_calories(username)
                total_carbs = food.get_total_carbs(username)
                total_protein = food.get_total_protein(username)
                total_fat = food.get_total_fat(username)
                print(today_food)

                plotly_charts.macros_chart([food.get_total_carbs(username), food.get_total_protein(username), food.get_total_fat(username)], "macros")
                plotly_charts.calorie_chart(chart_data.get_user_food(username), "calories")

                flash("Food added to log!")
                return render_template('nutrients.html', today_food=today_food, calories=total_calories, carbs=total_carbs, fat=total_fat, protein=total_protein)
            else:
                # catch errors with API key or empty query
                flash("We could not find the food you entered or the USDA Nutrients API key is missing.")
                today_food = food.get_user_food(username)
                total_calories = food.get_total_calories(username)
                return render_template('nutrients.html', today_food=today_food, calories=total_calories, carbs=total_carbs, fat=total_fat, protein=total_protein)
    # if there are errors, redirect to the home page
    except:
        flash("You must be logged in to access this page.")
        return redirect('/')

@app.route('/exercise', methods=["GET", "POST"])
def exercise_options():
    '''This function renders the exercise page with the user's information displayed. It receives the form submitted by the user and passes it to the exercise functions to update the exercise log with the hours spent working out and the category.'''
    try:
        username = session['username']
        all_categories = exercise.get_all_categories()
        hours = exercise.get_user_exercise(username)
        category = exercise.get_user_category(username)

        plotly_charts.bar_chart(chart_data.get_user_exercise(username), "exercise", "rgb(224,75,101)")

        if category != None:
            category = "You last worked on "+category+" today."
        else:
            category = "You haven't worked out today."
        if request.method == 'GET':
            return render_template('exercise.html', all_categories=all_categories, can_view_results=False, hours=hours, category=category)
        else:
            if request.form['submit'] == "Search":
                user_request = request.form['user_request']
                results = exercise.list_category_exercises(exercise.get_category_id(user_request))
                return render_template('exercise.html', all_categories=all_categories, results=results, can_view_results=True, hours=hours, category=category,requested=user_request)
            else:
                user_hours = request.form['hours']
                user_category = request.form['user_category']
                if exercise.update_user_log(user_hours, user_category, username) == True:
                    category = "You last worked on "+exercise.get_user_category(username)+" today."
                    plotly_charts.bar_chart(chart_data.get_user_exercise(username), "exercise", "rgb(224,75,101)")

                    flash("Exercise log successfully updated!")
                    hours = exercise.get_user_exercise(username)
                else:
                    flash("Hours and category cannot be empty.")
                return render_template('exercise.html', all_categories=all_categories, can_view_results=False, hours=hours, category=category)
    # if there are errors, redirect to the home page
    except:
        flash("You must be logged in to access this page.")
        return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.run()
