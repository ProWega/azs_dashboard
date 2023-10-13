import dash
from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(__name__)
progress = dbc.Progress(value=75, striped=True, animated=True)
layout = html.Div([
    html.H1('This is our parser_ page'),
    html.Div('This is our parser page content.'),
    dbc.Progress(
        value=80, label='80%', id="animated-progress", animated=True, striped=True
    )
])