import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime, timedelta

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
                        html.H1("IQA DASHBOARD"),
                        html.Hr(),
                        html.Br(),

                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.B("Academic Unit Heads Tracker")),
                                        dbc.CardBody(
                                            html.Div(
                                                id='acadheadsmoredetails_list',
                                                style={
                                                    'marginTop': '20px',
                                                    'overflowX': 'auto',
                                                    'overflowY': 'auto',
                                                    'maxHeight': '300px',
                                                }
                                            )
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
                                        dbc.CardHeader(html.B("QA Officers Tracker")),
                                        dbc.CardBody(
                                            html.Div(
                                                id='qaofficersmoredetails_list',
                                                style={
                                                    'marginTop': '20px',
                                                    'overflowX': 'auto',
                                                    'overflowY': 'auto',
                                                    'maxHeight': '300px',
                                                }
                                            )
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
    Output('acadheadsmoredetails_list', 'children'),
    [Input('url', 'pathname')]
)
def acadheadsmoredetails_loadlist(pathname):
    if pathname == '/dashboard/more_details':
        today = datetime.today() 

        sql = f"""
            SELECT 
                c.cluster_shortname AS "Cluster",
                cl.college_shortname AS "Academic Unit",
                du.deg_unit_shortname AS "Degree Granting Unit",
                a.unithead_full_name AS "Name",
                a.unithead_upmail AS "UP mail",
                a.unithead_appointment_end AS "End of Term"
            FROM iqateam.acad_unitheads a
            JOIN public.clusters c ON a.unithead_cluster_id = c.cluster_id
            JOIN public.college cl ON a.unithead_college_id = cl.college_id
            JOIN public.deg_unit du ON a.unithead_deg_unit_id = du.deg_unit_id
            WHERE  
                a.unithead_del_ind IS False
                AND a.unithead_appointment_end BETWEEN '{today}' AND '{today + timedelta(days=30)}'
        """
 
        cols = ['Cluster', 'Academic Unit', 'Degree Granting Unit', 'Name', 'UP mail', 'End of Term']
        
        # Query the database
        df = db.querydatafromdatabase(sql, [], cols)
        
        # Process the DataFrame if not empty
        if not df.empty:
            df.reset_index(drop=True, inplace=True)
            df.index += 1
            df.index.name = 'No.'
            count_div = html.Div(f"Total Academic Unit Heads: {len(df)}")
            
            df['Days Left'] = (pd.to_datetime(df['End of Term']) - pd.Timestamp.now()).dt.days
            df['Days Left'] = df['Days Left'].apply(lambda x: max(x, 0))
            df.reset_index(inplace=True)
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return html.Div([count_div, table])
        else:
            return html.Div("No records to display")
    else:
        raise PreventUpdate
    
 


@app.callback(
    Output('qaofficersmoredetails_list', 'children'),
    [Input('url', 'pathname')]
)
def qaofficersmoredetails_loadlist(pathname):
    if pathname == '/dashboard/more_details': 

        sql = """
            SELECT 
                c.cluster_shortname AS "Cluster",
                cl.college_shortname AS "Academic Unit",
                du.deg_unit_shortname AS "Degree Granting Unit",
                q.qaofficer_full_name AS "Name",
                q.qaofficer_upmail AS "UP mail",
                q.qaofficer_appointment_end AS "End of Term",
                q.qaofficer_remarks AS "Status"
            FROM qaofficers.qa_officer q
            JOIN public.clusters c ON q.qaofficer_cluster_id = c.cluster_id
            JOIN public.college cl ON q.qaofficer_college_id = cl.college_id
            JOIN public.deg_unit du ON q.qaofficer_deg_unit_id = du.deg_unit_id
            WHERE q.qaofficer_del_ind IS False; 
        """
 
        cols = ['Cluster', 'Academic Unit', 'Degree Granting Unit', 'Name', 'UP mail', 'End of Term','Status']
         
        df = db.querydatafromdatabase(sql, [], cols)
        
        # Process the DataFrame if not empty
        if not df.empty:
            df.reset_index(drop=True, inplace=True)
            df.index += 1
            df.index.name = 'No.'
            count_div = html.Div(f"Total QA Officers: {len(df)}")
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return html.Div([count_div, table])
        else:
            return html.Div("No records to display")
    else:
        raise PreventUpdate