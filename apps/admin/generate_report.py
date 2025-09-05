import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd 

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db


def create_card(title, content=None):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(content if content else "")
        ],
        className="mb-3",  # Add space below each card
    )


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                [
                    html.H1("GENERATE REPORTS"),
                    html.Hr(),
 

                    dbc.Row(
                            [
                                html.H4("SUBMITTED REPORTS"),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New", color="primary", 
                                        href='/training_documents', 
                                        ), width="auto", 
                                    ),
                                 
                                 
                            ]
                        ),

                    html.Br(),
                    html.Br(),
                    
                    dbc.Row(
                            [
                                html.H4("TRAINING DOCUMENTS"),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New", color="primary", 
                                        href='/training_documents', 
                                        ), width="auto", 
                                    ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='trainingdocuments_filter',
                                        placeholder='🔎 Search by name, position, cluster, department',
                                        className='ml-auto'   
                                        ),width="7",
                                    ),
                                    
                                html.Br(),
                                    
                                html.Div(
                                    id='trainingdocuments_list', 
                                        style={
                                            'marginTop': '20px',
                                            'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                                        }
                                    ),
                                 
                            ]
                        ),
                    
                    
                ], width=9, style={'marginLeft': '15px'}
                ),
                 
            ]
        ),
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
    [
        Output('trainingdocuments_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('trainingdocuments_filter', 'value'),
    ]
    )
  
  
def trainingdocuments_loadlist(pathname, searchterm):
    if pathname == '/generate_report':
        sql = """
            SELECT 
                td.complete_name AS "Name", 
                fp.fac_posn_name AS "Position", 
                c.cluster_name AS "Cluster",
                co.college_name AS "Department",
                qt.qa_training_name AS "QA Training",
                td.departure_date AS "Dep Date",
                td.return_date AS "Rep Date",
                td.venue AS "Venue"
            FROM adminteam.training_documents AS td
            LEFT JOIN fac_posns AS fp ON td.fac_posn_id = fp.fac_posn_id
            LEFT JOIN clusters AS c ON td.cluster_id = c.cluster_id
            LEFT JOIN college AS co ON td.college_id = co.college_id
            LEFT JOIN qa_training AS qt ON td.qa_training_id = qt.qa_training_id
        """

        cols = ['Name', 'Position', 'Cluster', 'Department', 'QA Training', 'Dep Date', 'Rep Date', 'Venue']

        if searchterm:
            # Add a WHERE clause with ILIKE to filter the results
            sql += """ 
                WHERE td.complete_name ILIKE %s 
                OR td.venue ILIKE %s 
                OR fp.fac_posn_name ILIKE %s 
                OR c.cluster_name ILIKE %s
                OR co.college_name ILIKE %s
                OR qt.qa_training_name ILIKE %s
                OR td.departure_date ILIKE %s
                OR td.return_date ILIKE %s
            """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern] * 8
        else:
            values = []

        df = db.querydatafromdatabase(sql, values, cols) 

        # Generate the table from the DataFrame
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]  # Wrap the table within a list
        else:
            return [html.Div("No records to display")]  # Wrap the message within a list
    else:
        raise PreventUpdate