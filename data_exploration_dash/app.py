import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

from components.fish_data_loading_import import model_dict, subject_stimulus_df, component_functions

import plotly.express as px

import pandas as pd
import numpy as np

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length")


app = dash.Dash()

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='subject_picklist',
            options=[{
                "label": subject,
                "value": subject
            } for subject in subject_stimulus_df["subject"].unique()],
            value='subject_1'
        ),
        dcc.Dropdown(
            id='stimulus_picklist',
            value='0'
        )
    ]),
    html.Div([
        html.Div([
            html.Label([
                "Number of X-axis bins:",
                dcc.Slider(
                    id='num_x_bins',
                    min=1,
                    max=100,
                    step=1,
                    value=40,
                    marks={
                        1:'1',
                        10: '10',
                        20:'20',
                        30:'30',
                        40:'40',
                        50:'50',
                        60:'60',
                        70:'70',
                        80:'80',
                        90:'90',
                        100:'100'
                    }
                ),
            ]),
        ]),
        html.Div([
            html.Label([
                "Number of Y-axis bins:",
                dcc.Slider(
                    id='num_y_bins',
                    min=1,
                    max=100,
                    step=1,
                    value=20,
                    marks={
                        1:'1',
                        10: '10',
                        20:'20',
                        30:'30',
                        40:'40',
                        50:'50',
                        60:'60',
                        70:'70',
                        80:'80',
                        90:'90',
                        100:'100'
                    }
                ),
            ]),
        ]),
        html.Div([
            html.Label([
                "Number of Z-axis bins:",
                dcc.Slider(
                    id='num_z_bins',
                    min=1,
                    max=50,
                    step=1,
                    value=1,
                    marks={
                        1:'1',
                        10: '10',
                        20:'20',
                        30:'30',
                        40:'40',
                        50:'50'
                    }
                ),
            ]),
        ]),
    ]),
    html.Div([
        dcc.Graph(
            id="fish_figure"
        ),
        dcc.Graph(
            id='comp_functions'
        )
    ])
])

@app.callback(
    dash.dependencies.Output('comp_functions', 'figure'),
    [  
        dash.dependencies.Input('subject_picklist', 'value'),
        dash.dependencies.Input('stimulus_picklist', 'value')
    ]
)
def update_component_function_data(subject, stimulus):
    if subject and stimulus:
        data=component_functions[f"{subject}:{stimulus}"].T
        fig = go.Figure()
        color_discrete_map={
            '0':'red',
            '1':'orangered',
            '2':'orange',
            '3':'yellow',
            '4':'green',
            '5':'blue',
            '6':'indigo',
            '7':'violet',
            '8':'fuchsia',
            '9':'pink'
        }
        for row_num in range(len(data)):
            row_data = data[row_num]
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(row_data))), y=row_data,
                    mode='lines',
                    name=f"Component {row_num}",
                    line=dict(color=color_discrete_map[f"{row_num}"])
                )
            )
        return fig

@app.callback(
    dash.dependencies.Output('fish_figure', 'figure'),
    [  
        dash.dependencies.Input('subject_picklist', 'value'),
        dash.dependencies.Input('stimulus_picklist', 'value'),
        dash.dependencies.Input('num_x_bins', 'value'),
        dash.dependencies.Input('num_y_bins', 'value'),
        dash.dependencies.Input('num_z_bins', 'value')
    ])
def update_fish_figure_data(subject, stimulus, x_bins, y_bins, z_bins):
    if subject and stimulus:
        fish_df = model_dict[f"{subject}:{stimulus}"]
        fish_df["x_bin"] = pd.cut(fish_df["x"], x_bins)
        fish_df["y_bin"] = pd.cut(fish_df["y"], y_bins)
        fish_df["z_bin"] = pd.cut(fish_df["z"], z_bins)
        groups = fish_df.groupby(["x_bin","y_bin","z_bin"]).sum().dropna()[[0,1,2,3,4,5,6,7,8,9]]
        dominant_component = groups.abs().idxmax(axis=1).astype('str').rename("dominant_component")
        new_fish_data = fish_df.join(dominant_component, on=["x_bin","y_bin","z_bin"], how="left")
        fig = px.scatter_3d(
            new_fish_data, 
            x="x", y="y", z="z", 
            color="dominant_component",
            opacity=0.5,
            range_x=[0,2000],
            range_y=[0,2000],
            range_z=[0,2000],
            color_discrete_map={
                '0':'red',
                '1':'orangered',
                '2':'orange',
                '3':'yellow',
                '4':'green',
                '5':'blue',
                '6':'indigo',
                '7':'violet',
                '8':'fuchsia',
                '9':'pink'},
            height=800
        )
        fig.update_layout(legend= {'itemsizing': 'constant'}, legend_title_text='Dominant Component')
        fig.update_traces(marker=dict(size=1))
        return fig
    else:
        return None

@app.callback(
    dash.dependencies.Output("stimulus_picklist", "options"),
    [dash.dependencies.Input('subject_picklist', 'value')]
)
def update_stimulus_options(value):
    return [{
        "label": "All Stimuli" if stimulus == None else stimulus,
        "value": "None" if stimulus == None else stimulus
    } for stimulus in subject_stimulus_df[subject_stimulus_df["subject"]==value]["stimulus"].unique()]

app.run_server(debug=True)