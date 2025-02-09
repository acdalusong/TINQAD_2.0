import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db 


 
layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("View Complete Training List"),
                        html.Hr(),
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
                html.Br()
            ]
        ),
        html.Br(),
        html.Br(), 
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)
 