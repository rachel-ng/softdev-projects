import plotly
import plotly.plotly as py
import plotly.graph_objs as go

trace0 = go.Bar(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = go.Bar(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = [trace0, trace1]

new_chart = plotly.offline.plot(data, output_type='div')

print(new_chart)
print("plotly")
