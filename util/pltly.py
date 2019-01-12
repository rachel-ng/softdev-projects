import plotly
import plotly.plotly as py
import plotly.graph_objs as go

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
        autosize=True,
        barmode='stack',
        xaxis=dict(
            ticks='outside',
            tickmode='linear',
            dtick=2,
            tickvals=ticks,
            ticktext=hours_axis
        ),
        yaxis=dict(
        )
    )

    fig = go.Figure(data=data, layout=layout)

    sleep_c = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    with open('templates/sleep_chart.html', 'w') as f:
        f.write(sleep_c)
