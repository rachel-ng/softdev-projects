import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

javascript = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n'

def config() :
    with open('data/keys.json', 'r') as f:
        api_dict = json.load(f)

    plotly.tools.set_credentials_file(username= api_dict["PLOTLY_USERNAME"], api_key=api_dict["PLOTLY_API"])

    print("hooray!")

def sleep_chart() :
    hours_axis = []
    ticks = []
    i = 0
    while (i < 12 + 29):
        ticks.append(i)
        hours_axis.append((i + 12) % 24)
        i += 2

    print(ticks)
    print(hours_axis)


    offset_x = [0, 2, 23, 3, 21, 1, 4]
    offset = []
    for n in offset_x:
        if n > 12:
            offset.append(n - 12)
        if n < 12:
            offset.append(n + 12)

    offsetting  = go.Bar(
        x=offset,
        y=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday'],
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

    sleep = go.Bar(
        name="Hours Slept",
        x=[8, 4, 7, 3, 6, 10, 18],
        y=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday'],
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

    layout = go.Layout(
        title='Sleep Log',
        height=400,
        autosize=True,
        barmode='stack',
        xaxis=dict(
            ticks='outside',
            tickmode='linear',
            dtick=1,
            tickvals=ticks,
            ticktext=hours_axis
        ),
        yaxis=dict(
        )
    )

    fig = go.Figure(data=data, layout=layout)

    sleep_c = javascript + plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    with open('templates/sleep_chart.html', 'w') as f:
        f.write(sleep_c)

def macros_chart() :
    data = [
        go.Scatterpolar(
            r = [39, 28, 8, 7],
            theta = ['calories','carbs','protein', 'fat'],
            fill = 'toself',
            name = 'Group A'
        ),
        go.Scatterpolar(
            r = [1.5, 152, 101, 38],
            theta = ['calories','carbs','protein', 'fat'],
            fill = 'toself',
            name = 'Group B'
        )
    ]

    layout = go.Layout(
        polar = dict(
            radialaxis = dict(
                visible = True,
                range = [0, 175]
            )
        ),
        showlegend = False
    )
    fig = go.Figure(data=data, layout=layout)
    macros_c = javascript + plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    with open('templates/macros_chart.html', 'w') as f:
        f.write(macros_c)

def line_chart() :
    N = 7
    random_y = np.random.randn(N)

    trace = go.Scatter(
        x = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday'],
        y = random_y
    )

    data = [trace]

    line_c = javascript + plotly.offline.plot(data, include_plotlyjs=False, output_type='div')

    with open('templates/line_chart.html', 'w') as f:
        f.write(line_c)

def bar_chart() :
    data = [go.Bar(
        x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday'],
        y=[20, 14, 23, 64, 23, 56, 100]
    )]

    bar_c = javascript + plotly.offline.plot(data, include_plotlyjs=False, output_type='div')

    with open('templates/bar_chart.html', 'w') as f:
        f.write(bar_c)


sleep_chart()
macros_chart()
line_chart()
bar_chart()
