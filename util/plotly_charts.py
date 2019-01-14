import sqlite3
from datetime import datetime

import plotly.offline
from plotly.graph_objs import *

javascript = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n'

DB_FILE = "data/health.db"

def user_data (username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))

    c.execute(command)
    user_id = c.fetchone()[0]
    print (user_id)
    current_weekday = datetime.now().weekday()
    print(current_weekday)
    command = "SELECT year, month, day, week_start_day FROM water_log WHERE user_id={}".format(repr(user_id))
    c.execute(command)
    data = c.fetchone()
    year = data[0]
    month = data[1]
    day = data[2]
    weekday = data[3]

    command = "SELECT intake_01, intake_02, intake_03, intake_04, intake_05, intake_06, intake_07 FROM water_log WHERE user_id={} AND year={} AND month={} AND day={}".format(repr(user_id), repr(year), repr(month), repr(day))
    c.execute(command)
    data = c.fetchall()

    water_data = []

    for row in data:
        water_data = row

    db.close()
    return (water_data) # "literally about to yeet myself into the sun but good, you? "


def sleep_chart(name, title) :
    hours_axis = []
    ticks = []
    i = 0
    while (i < 12 + 29):
        ticks.append(i)
        hours_axis.append((i + 12) % 24)
        i += 4

    print("hours axis")
    print (hours_axis)
    print("ticks")
    print(ticks)

    offset_x = [0, 2, 23, 3, 21, 1, 4]
    offset = []
    for n in offset_x:
        if n > 12:
            offset.append(n - 12)
        if n < 12:
            offset.append(n + 12)

    offsetting  = Bar(
        x=offset,
        y= ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        showlegend=False,
        orientation = 'h',
        hoverinfo='skip',
        opacity=0,
        width= .5,
        marker=dict(
            color='rgb(255,255,255)',
            line=dict(color='rgb(255,255,255)',)
        )
    )

    sleep = Bar(
        name="Hours Slept",
        x= [8, 4, 7, 3, 5, 10, 17],
        y= ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        showlegend=False,
        orientation = 'h',
        opacity=.6,
        width= .5,
        hoverinfo = 'x',
        marker=dict(
            color='rgb(23,53,98)',
            line=dict(color='rgb(248, 248, 249)')
        )
    )


    data = [offsetting, sleep]

    layout = Layout(
        title=title,
        autosize=True,
        barmode='stack',
        xaxis=dict(
            tickmode='array',
            dtick=2,
            tickvals=ticks,
            ticktext=hours_axis
        ),
        yaxis=dict(
        )
    )

    fig = dict(data=data, layout=layout)
    sleep_c = javascript + plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    name_chart = 'templates/' + name + '_chart.html'
    with open(name_chart, 'w') as f:
        f.write(sleep_c)

def macros_chart(data, name, title) :
    data = [
        Scatterpolar(
            r = [data[0], data[1], data[2], data[3]],
            theta = ['calories','carbs','protein', 'fat'],
            fill = 'toself',
            name = 'Total'
        )
        #Scatterpolar(
        #    r = [1.5, 152, 101, 38],
        #    theta = ['calories','carbs','protein', 'fat'],
        #    fill = 'toself',
        #    name = 'Group B'
        #)
    ]

    layout = Layout(
        polar = dict(
            radialaxis = dict(
                visible = True,
                range = [0, max(data)]
            )
        ),
        title=title,
        showlegend = False
    )

    fig = dict(data=data, layout=layout)
    macros_c = javascript + plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    name_chart = 'templates/' + name + '_chart.html'
    with open(name_chart, 'w') as f:
        f.write(macros_c)

def line_chart(data, name, title) :
    data = [Scatter(
        x= ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        y= [data[5], data[6], data[0], data[1], data[2], data[3], data[4]]
    )]

    layout = Layout(
        title=title,
        showlegend = False
    )

    fig = dict(data=data, layout=layout)
    line_c = javascript + plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    name_chart = 'templates/' + name + '_chart.html'
    with open(name_chart, 'w') as f:
        f.write(line_c)

def bar_chart(data, name, title) :
    data = [Bar(
        x= ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        y= [data[5], data[6], data[0], data[1], data[2], data[3], data[4]]
    )]

    layout = Layout(
        title=title,
        showlegend = False
    )

    fig = dict(data=data, layout=layout)
    bar_c = javascript + plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    name_chart = 'templates/' + name + '_chart.html'
    with open(name_chart, 'w') as f:
        f.write(bar_c)
