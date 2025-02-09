import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime, timedelta

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db





@app.callback(
    Output('acad_unitheadstotal_count', 'children'),
    [Input('url', 'pathname')]
)
def acad_unitheadscount(pathname):
    if pathname == '/iqa_dashboard':
        today = datetime.today()
        twomonthsfromnow = today + timedelta(days=60)
        sql = """
            SELECT COUNT(*) 
            FROM iqateam.acad_unitheads  
            WHERE 
                unithead_del_ind IS False 
                AND unithead_appointment_end BETWEEN %s AND %s;
        """
        params = (today, twomonthsfromnow)
        acad_unitheadstotal_count = db.query_single_value_db(sql, params)
        return acad_unitheadstotal_count

@app.callback(
    Output('qa_officerstotal_count', 'children'),
    [Input('url', 'pathname')]
)
def qa_officerscount(pathname):
    if pathname == '/iqa_dashboard':
        today = datetime.today()
        twomonthsfromnow = today + timedelta(days=60)
        sql = """
            SELECT COUNT(*) 
            FROM qaofficers.qa_officer 
            WHERE 
                qaofficer_del_ind = False
                AND qaofficer_appointment_end BETWEEN %s AND %s;
        """
        params = (today, twomonthsfromnow)
        qa_officerstotal_count = db.query_single_value_db(sql, params)
        return qa_officerstotal_count





layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("IQA DASHBOARD"),
                        html.Hr(),
                        html.Br(),

                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H3("Academic Unit Heads")),
                                        dbc.CardBody(
                                            [ 
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Strong("Total =", style={"margin-right": "3px", "margin-top": "10px"}),
                                                            width="auto"
                                                        ),
                                                        dbc.Col(
                                                            html.Span(id='acad_unitheadstotal_count', style={"font-weight": "bold"}),
                                                            width={"size": 2, "sm": 2, "l": 1},
                                                            style={
                                                                "backgroundColor": "#A9CD46",
                                                                "borderRadius": "10px",
                                                                "padding": "5px",
                                                                "textAlign": "center",
                                                                "marginLeft": "-10px" 
                                                            }
                                                        ),   
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.A(
                                                                dbc.Button("More details..", color="link"),
                                                                href="/dashboard/more_details",
                                                                style={"text-align": "right"}
                                                            ),
                                                            width={"size": 2, "offset": 10}  # Adjust width and offset for alignment
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    id='acadheadsdashboard_list',
                                                    style={
                                                        'marginTop': '20px',
                                                        'overflowX': 'auto',
                                                        'overflowY': 'auto',
                                                        'maxHeight': '300px',
                                                    }
                                                )
                                            ]
                                        )
                                    ],
                                    color="light"
                                ),
                                width=12
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H3("Quality Assurance Officers")),
                                        dbc.CardBody(
                                            [ 
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Strong("Total =", style={"margin-right": "3px", "margin-top": "10px"}),
                                                            width="auto"
                                                        ),
                                                        dbc.Col(
                                                            html.Span(id='qa_officerstotal_count', style={"font-weight": "bold"}),
                                                            width={"size": 2, "sm": 2, "l": 1},
                                                            style={
                                                                "backgroundColor": "#A9CD46",
                                                                "borderRadius": "10px",
                                                                "padding": "5px",
                                                                "textAlign": "center",
                                                                "marginLeft": "-10px" 
                                                            }
                                                        ),   
                                                        
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.A(
                                                                dbc.Button("More details..", color="link"),
                                                                href="/dashboard/more_details",
                                                                style={"text-align": "right"}
                                                            ),
                                                            width={"size": 2, "offset": 10}  # Adjust width and offset for alignment
                                                        ),
                                                    ],
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Div(
                                                            id='qaofficersdashboard_list',
                                                            style={
                                                                'marginTop': '20px',
                                                                'overflowX': 'auto',
                                                                'overflowY': 'auto',
                                                                'maxHeight': '300px',
                                                            }
                                                        )
                                                    ],
                                                ),
                                                
                                            ]
                                        )
                                    ],
                                    color="light"
                                ),
                                width=12
                            )
                        ),
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(), html.Br(), html.Br(),
        dbc.Row(
            dbc.Col(
                cm.generate_footer(),
                width={"size": 12, "offset": 0}
            )
        )
    ]
)








@app.callback(
    Output('acadheadsdashboard_list', 'children'),
    [Input('url', 'pathname')]
)
def acadheadsmoredetails_loadlist(pathname):
    if pathname == '/iqa_dashboard':
        today = datetime.today() 

        sql = f"""
            SELECT 
                c.college_name AS "College",
                COUNT(*) AS "Terms Expiring in 2 Months"
            FROM iqateam.acad_unitheads a
            JOIN public.college c ON a.unithead_college_id = c.college_id
            WHERE 
                a.unithead_appointment_end BETWEEN '{today}' AND '{today + timedelta(days=60)}'
                AND a.unithead_del_ind IS False
            GROUP BY a.unithead_college_id, c.college_name; 
        """
         
        cols = ['College', 'Terms Expiring in 2 Months']
        
        # Query the database
        df = db.querydatafromdatabase(sql, [], cols)
        
        # Process the DataFrame if not empty
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return (table)
        else:
            return ("No records to display")
    else:
        raise PreventUpdate
    
 


@app.callback(
    Output('qaofficersdashboard_list', 'children'),
    [Input('url', 'pathname')]
)

def qaofficersmoredetails_loadlist(pathname):
    if pathname == '/iqa_dashboard': 
        today = datetime.today()
        twomonthsfromnow = today + timedelta(days=60)
        
        # Define the SQL query with the date range
        sql = f"""
            SELECT c.college_name AS "College",
                COUNT(*) AS "QA Officers",
                SUM(CASE WHEN qaofficer_basicpaper = 'Yes' THEN 1 ELSE 0 END) AS "Approved Papers",
                SUM(CASE WHEN qaofficer_remarks = 'For renewal' THEN 1 ELSE 0 END) AS "Renewal",
                SUM(CASE WHEN qaofficer_remarks = 'No record' THEN 1 ELSE 0 END) AS "No Record",
                SUM(CASE WHEN qaofficer_appointment_end BETWEEN '{today}' AND '{twomonthsfromnow}' THEN 1 ELSE 0 END) AS "Expiring"
            FROM qaofficers.qa_officer q
            JOIN public.college c ON q.qaofficer_college_id = c.college_id
            WHERE q.qaofficer_del_ind = False
            GROUP BY q.qaofficer_college_id, c.college_name;
        """
 
        cols = ['College', 'QA Officers', 'Approved Papers',  'Renewal', 'No Record', 'Expiring']
         
        df = db.querydatafromdatabase(sql, [], cols)
        
        # Process the DataFrame if not empty
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return (table)
        else:
            return ("No records to display")
    else:
        raise PreventUpdate