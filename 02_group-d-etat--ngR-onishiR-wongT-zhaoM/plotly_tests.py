import os

from flask import Flask, render_template, request, session, redirect, url_for, flash

from util import user, exercise, water, food, sleep, plotly_charts, chart_data

app = Flask(__name__) #create instance of class flask

app.secret_key = os.urandom(32)


@app.route('/')
def plotly_tests():
    username = 'r'

    sleep_data = chart_data.get_user_sleep(username)
    plotly_charts.sleep_chart(sleep_data, "sleep")

    water_data = chart_data.get_user_water(username)
    plotly_charts.bar_chart(water_data, "water", "rgb(88,180,197)")

    user_macros = [food.get_total_carbs(username), food.get_total_protein(username), food.get_total_fat(username)]
    plotly_charts.macros_chart(user_macros, "macros")

    food_data = chart_data.get_user_food(username)
    plotly_charts.calorie_chart(food_data, "calories")

    exercise_data = chart_data.get_user_exercise(username)
    plotly_charts.bar_chart(exercise_data, "exercise", "rgb(224,75,101)")

    return render_template('all_charts.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
