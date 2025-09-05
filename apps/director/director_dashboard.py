import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import plotly.graph_objs as go 

 




def get_total_checked():
    sql = f"""
        SELECT COUNT(*)
        FROM maindashboard.users u
        WHERE u.user_office = 1
        AND u.user_id IN (
            SELECT es.summary_evaluatee_id
            FROM director.evaluation_summaries es
            WHERE es.summary_evaluation_period = (
                SELECT ep.period_id
                FROM director.evaluation_periods ep
                WHERE ep.active_status = TRUE
                AND ep.period_del_ind = FALSE
            )
            AND es.summary_done = TRUE
        );   
    """
    total_evaluations_marked_as_done = db.query_single_value(sql)
    return total_evaluations_marked_as_done

def get_total_ongoing():
    sql = f"""
        SELECT COUNT(*)
        FROM maindashboard.users u
        WHERE u.user_office = 1
        AND u.user_id IN (
            SELECT es.summary_evaluatee_id
            FROM director.evaluation_summaries es
            WHERE es.summary_evaluation_period = (
                SELECT ep.period_id
                FROM director.evaluation_periods ep
                WHERE ep.active_status = TRUE
                AND ep.period_del_ind = FALSE
            )
            AND es.summary_done = FALSE
        );      
    """
    total_evaluations_marked_as_not_done = db.query_single_value(sql)
    return total_evaluations_marked_as_not_done

def get_total_unchecked():
    sql = f"""
        SELECT COUNT(*)
        FROM maindashboard.users u
        WHERE u.user_office = 1
        AND u.user_id NOT IN (
            SELECT es.summary_evaluatee_id
            FROM director.evaluation_summaries es
            WHERE es.summary_evaluation_period = (
                SELECT ep.period_id
                FROM director.evaluation_periods ep
                WHERE ep.active_status = TRUE
                AND ep.period_del_ind = FALSE
            )
        );  
    """

    need_to_edit_and_save_evaluations = db.query_single_value(sql)
    
    return need_to_edit_and_save_evaluations




def generate_donut_chart():
    # Call the functions to get the counts
    checked_count = get_total_checked()
    ongoing_count = get_total_ongoing()
    unchecked_count = get_total_unchecked()
    
    # Create the data for the pie chart
    labels = ['Marked as Done', 'To be Marked as Done', 'Not Yet Checked']
    values = [checked_count, ongoing_count, unchecked_count]
    
    # Define colors for the pie chart
    colors = ['#39B54A','#F8B237','#D37157']
    
    # Create the pie chart trace
    trace = go.Pie(labels=labels, values=values, hole=0.4, marker=dict(colors=colors))
    
    # Define layout for the pie chart
    layout = go.Layout(showlegend=False)
    
    # Return the figure
    return {'data': [trace], 'layout': layout}

def get_undergraduate_count():
    sql = """
    SELECT COUNT(*)
    FROM eqateam.sar_report sr
    JOIN eqateam.program_details pd ON sr.sarep_degree_programs_id = pd.programdetails_id
    WHERE pd.pro_program_type_id = 'Undergraduate'
    AND sr.sarep_del_ind IS FALSE;
    """
    values = []
    cols = ['total']
    df = db.querydatafromdatabase(sql, values, cols)
    return df['total'].iloc[0]



def director_summary_legend(get_total_checked, get_total_ongoing, get_total_unchecked):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Span(get_total_checked(), 
                            style={
                                "font-weight": "bold", "display": "flex", 
                                "align-items": "center",  "justify-content": "center",
                                'backgroundColor': '#39B54A', 'borderRadius': '10px',      
                                'padding': '5px'
                            }
                        ),
                        width=3 
                    ),
                    dbc.Col(
                        [
                            html.B(
                                "Marked as Done", 
                                style={'marginLeft': '10px', 'textAlign': 'left', 'marginRight': '15px'}
                            ),
                            html.P(
                                "Staff Peer Valuation Marked as Done", 
                                style={'marginLeft': '10px', 'textAlign': 'left', 'marginRight': '15px'}
                            ),
                        ],
                        width=9
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Span(get_total_ongoing(), 
                            style={
                                "font-weight": "bold", "display": "flex", 
                                "align-items": "center",  "justify-content": "center",
                                'backgroundColor': '#F8B237', 'borderRadius': '10px',      
                                'padding': '5px'
                            }
                        ),
                        width=3 
                    ),
                    dbc.Col(
                        [
                            html.B(
                                "To be Marked as Done", 
                                style={'marginLeft': '10px', 'textAlign': 'left', 'marginRight': '15px'}
                            ),
                            html.P(
                                "Staff Peer Valuation Marked as Not Done", 
                                style={'marginLeft': '10px',  'textAlign': 'left', 'marginRight': '15px'}
                            ),
                        ],
                        width=9
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Span(get_total_unchecked(), 
                            style={
                                "font-weight": "bold", "display": "flex", 
                                "align-items": "center",  "justify-content": "center",
                                'backgroundColor': '#D37157', 'borderRadius': '10px',      
                                'padding': '5px'
                            }
                        ),
                        width=3 
                    ),
                    dbc.Col(
                        [
                            html.B(
                                "Not Yet Checked", 
                                style={'marginLeft': '10px', 'textAlign': 'left', 'marginRight': '15px'}
                            ),
                            html.P(
                                "Staff Peer Valuation Summaries yet to Edit and Save", 
                                style={'marginLeft': '10px',  'textAlign': 'left', 'marginRight': '15px'}
                            ),
                        ],
                        width=9
                    )
                ]
            )
        ]
    )

 

def director_evaluation_summary(director_summary_legend):
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H3(html.Strong("Summary of Peer Evaluations")),
                    html.A(id="current_period_director")
                ]
            ),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id='donut-chart', 
                                    figure=generate_donut_chart(),
                                    config={'displayModeBar': False},   
                                    style={'height': '400px', 'margin-right': '0px', 'margin-top': '0px'}  
                                ),
                                width=7
                            ),
                            dbc.Col(
                                [
                                    director_summary_legend(get_total_checked, get_total_ongoing, get_total_unchecked),
                                ],
                                width=5 
                            ),
                        ], 
                    ),
                ],   
            )
        ], style={'margin': '0', 'height': '500px'}  # Set the height of the card to 500px
    )




layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("DIRECTOR DASHBOARD"),
                        html.Hr(),
                        html.Div(  
                            [
                                dcc.Store(id='directordashboard_toload', storage_type='memory', data=0),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.CardBody(
                                                    html.Div(id='director_evaluation_summary')
                                                )
                                            ]
                                        ),   
                                    ],
                                ),
                            ]
                        ), 
                    ]
                ),
            ]
        ),
        html.Br(), html.Br(), html.Br(),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)


 



@app.callback(
    [Output('director_evaluation_summary', 'children')
    ],
    [Input('directordashboard_toload', 'modified_timestamp')],
    [State('directordashboard_toload', 'data')]
)
def update_charts(timestamp, toload):
    if toload:
        director_evaluation_summary_chart = director_evaluation_summary(director_summary_legend)  # Pass director_summary_legend here
        return [director_evaluation_summary_chart]  # Return both components
    else:
        raise PreventUpdate
    

@app.callback(
    Output('directordashboard_toload', 'data'),
    Input('url', 'pathname')
)
def trigger_chart_loading(pathname):
    if pathname == '/director_dashboard':
        return 1   
    return 0  

@app.callback(
    Output('current_period_director', 'children'),
    Input('url', 'pathname')
)
def evaluation_period_retriever(pathname):
    if pathname == '/director_dashboard':
        sql = """
            SELECT
			'From ' ||
                to_char(lower(period_details), 'Mon DD, YYYY') ||
                ' to ' ||
                to_char(upper(period_details) - INTERVAL '1 day', 'Mon DD, YYYY') AS active_period
            FROM director.evaluation_periods
            WHERE active_status = TRUE
            AND 
            period_del_ind = FALSE
        """
        values = []
        cols = ['active_period']
        df = db.querydatafromdatabase(sql, values, cols)
        
        active_period = df['active_period'][0]
        return [active_period]
    
    else:
        raise PreventUpdate 