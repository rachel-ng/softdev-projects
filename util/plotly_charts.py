import datetime

import plotly.offline
from plotly.graph_objs import *

def sleep_chart(data, name):
    '''Creates a horizontal bar chart (gantt style) for sleep'''

    # for the x axes
    hours_axis = [12, 16, 20, 0, 4, 8, 12, 16, 20, 0]
    ticks = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]

    # for when they go to sleep, ignores the minutes
    offset_x = [data[11], data[9], data[7], data[5], data[3], data[1], data[13]]
    offset = []
    for n in offset_x:
        t = str(n).split(":")
        if float(t[0]) == 0:
            pass
        else:
            if float(t[0]) > 12:
                offset.append(float(t[0]) - 12)
            if float(t[0]) < 12:
                offset.append(float(t[0]) + 12)

    # for the days, only adds to chart when there's data for it
    days_y =  ['Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday', 'Sunday']
    days = []
    d = 0

    # for how long they slept, once again ignores the minutes
    nap_time_x = [data[10], data[8], data[6], data[4], data[2], data[0], data[12]]
    nap_time = []
    for n in nap_time_x:
        t = str(n).split(":")
        if float(t[0]) == 0:
            pass
        else:
            nap_time.append(float(t[0]))
            days.append(days_y[d])
        d += 1

    bedtime = Bar(
        x=offset,
        y= days,
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
        x= nap_time, # slept
        y= days,
        hovertext = nap_time,
        showlegend=False,
        orientation = 'h',
        opacity=.6,
        width= .5,
        hoverinfo = 'text',
        marker=dict(
            color='rgb(23,53,98)',
            line=dict(color='rgb(248, 248, 249)')
        )
    )

    data = [bedtime, sleep]

    layout = Layout(
        height=400,
        autosize=True,
        barmode='stack',
        xaxis=dict(
            tickmode='array',
            dtick=1,
            tickvals=ticks,
            ticktext=hours_axis
        ),
        yaxis=dict(
        )
    )

    fig = dict(data=data, layout=layout)
    sleep_c = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    name_chart = 'templates/' + 'sleep' + '_chart.html'
    with open(name_chart, 'w') as f:
        f.write(sleep_c)

def macros_chart(data, name):
    '''Creates a radar chart for macronutrient data (carbs, protein, fat)'''

    user_data = [Scatterpolar(
        r = [275, 60, 51],
        theta = ['carbs','protein', 'fat'],
        hovertext = ['275g carbs','60g protein', '51g fat'],
        hoverinfo = 'text',
        fill = 'toself',
        name = 'What you were supposed to eat',
        marker=dict(
            color='rgb(244, 211, 94)',
            line=dict(color='rgb(255,255,255)')
        )
    ),
    Scatterpolar(
        r = data,
        theta = ['carbs','protein', 'fat'],
        hovertext = [str(data[0]) + 'g carbs', str(data[1]) + 'g protein', str(data[2]) + 'g fat'],
        hoverinfo = 'text',
        fill = 'toself',
        name = 'What you actually ate',
        opacity=.6,
        marker=dict(
            color='rgb(94,180,103)',
            line=dict(color='rgb(255,255,255)')
        )
    )]

    data.append(275)

    layout = Layout(
        legend=dict(
            orientation='h'
        ),
        polar=dict(
            radialaxis = dict(
                visible = True,
                range = [0, max(data)]
            )
        )
    )

    fig = Figure(data=user_data, layout=layout)
    macros_c = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    name_chart = 'templates/' + name + '_chart.html'
    with open(name_chart, 'w') as f:
        f.write(macros_c)

def calorie_chart(data, name):
    '''Creates a line chart specifically for calories'''

    # processes the data
    food_times = []
    daily_calories = []
    food_names = []

    current_cal = 0

    for i in data:
        if i[1] < 10:
            time = str(i[0]) + ":0" + str(i[1])
        else:
            time = str(i[0]) + ":" + str(i[1])

        food_times.append(time)

        # adds current calories to how many you've eaten so far to visually represent your calorie intaje
        daily_calories.append(current_cal + i[3])

        # formatting for the text displayed when hovering over those data points
        food_names.append(str(i[0]) + ":" + str(i[1]) + "  " + str(i[2]) + ": " + str(i[3]) + "calories consumed: " + str(current_cal + i[3]))
        current_cal += i[3]

    data = [Scatter(
        x = food_times,
        y = daily_calories,
        hovertext = food_names,
        hoverinfo = 'text',
        line = dict(color = 'rgb(95,184,104)')
    )]

    layout = Layout(
        showlegend = False,
        xaxis=dict(
            dtick=1
        )
    )

    fig = dict(data=data, layout=layout)
    line_c = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    name_chart = 'templates/' + name + '_chart.html'
    with open(name_chart, 'w') as f:
        f.write(line_c)

def line_chart(data, name, chart_color):
    '''Creates a line chart'''

    data = [Scatter(
        x = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        y = [data[6], data[0], data[1], data[2], data[3], data[4], data[5]],
        line = dict(color = chart_color)
    )]

    layout = Layout(
        showlegend = False
    )

    fig = dict(data=data, layout=layout)
    line_c = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    name_chart = 'templates/' + name + '_chart.html'
    with open(name_chart, 'w') as f:
        f.write(line_c)


def bar_chart(data, name, chart_color):
    '''Creates a bar chart'''

    data = [Bar(
        x= ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        y= [data[6], data[0], data[1], data[2], data[3], data[4], data[5]],
        opacity=.6,
        hoverinfo = 'y',
        marker=dict(
            color=chart_color,
            line=dict(color='rgb(248, 248, 249)')
        )
    )]

    layout = Layout(
        showlegend = False,
        yaxis=dict(
            tick0=0
        )
    )

    fig = dict(data=data, layout=layout)
    bar_c = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    name_chart = 'templates/' + name + '_chart.html'
    with open(name_chart, 'w') as f:
        f.write(bar_c)
