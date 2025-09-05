import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import plotly.graph_objs as go

# Page layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label("Select Staff Member:"),
            dcc.Dropdown(
                id="staff-dropdown",
                placeholder="Choose a QA staff…",
                clearable=False,
            ),
        ], width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="performance-trend"),
        ], width=12),
    ]),
], fluid=True)

@app.callback(
    Output("staff-dropdown", "options"),
    Input("url", "pathname"),
)
def load_staff_options(pathname):
    if pathname != "/qa/performance-trend":
        raise PreventUpdate

    sql = """
        SELECT
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS label,
            u.user_id AS value
        FROM maindashboard.users u
        WHERE u.user_del_ind = FALSE
          AND u.user_office = 1
          AND u.user_id NOT IN (
              SELECT user_id
              FROM maindashboard.users
              WHERE user_office = 1
                AND user_qao_team_id = 1
          )
    """
    cols = ["label", "value"]
    df = db.querydatafromdatabase(sql, [], cols)
    return df.to_dict("records")


@app.callback(
    Output("performance-trend", "figure"),
    Input("staff-dropdown", "value"),
)
def update_performance_trend(user_id):
    if not user_id:
        # Empty figure if nothing selected
        return go.Figure().update_layout(
            title="Select a staff member to view trend"
        )

    # Query each active period’s weighted average for the selected user
    sql = """
        SELECT
            to_char(lower(ep.period_details), 'Mon YYYY') AS period_label,
            ROUND(
                AVG(ed.rating_value)::numeric, 2
            ) AS overall_avg
        FROM director.peer_evaluations pe
        JOIN director.evaluation_details ed ON pe.evaluation_id = ed.evaluation_id
        JOIN director.evaluation_periods ep ON pe.evaluation_period_id = ep.period_id
        WHERE pe.evaluatee_id = %s
          AND pe.peer_eval_delete_ind = FALSE
          AND ep.period_del_ind = FALSE
        GROUP BY ep.period_details
        ORDER BY lower(ep.period_details)
    """
    cols = ["period_label", "overall_avg"]
    df = db.querydatafromdatabase(sql, [user_id], cols)

    # Build the line chart
    fig = go.Figure(
        data=go.Scatter(
            x=df["period_label"],
            y=df["overall_avg"],
            mode="lines+markers",
            name="Overall Avg"
        )
    )
    fig.update_layout(
        title="Performance Trend",
        xaxis_title="Evaluation Period",
        yaxis_title="Overall Weighted Average",
    )
    return fig