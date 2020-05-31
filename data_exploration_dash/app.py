import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from components.fish_loading_data_import import model_dict

import plotly.express as px

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length")


app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)