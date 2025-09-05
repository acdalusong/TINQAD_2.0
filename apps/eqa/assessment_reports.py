import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd
import os

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db


# Using the corrected path
UPLOAD_DIRECTORY = r".\assets\database\eqa"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Define the search bars
rep_search_bar = dbc.Col(
    dbc.Input(
        type='text',
        id='assessmentreports_filter',
        placeholder='🔎 Search by Report Type, Degree Program, Status',
        className='ml-auto'
    ),
    width="12",
    id='rep_search_bar'
)


# Define the layout
layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("PROGRAM-LEVEL REPORTS TRACKER"),
                        html.Hr(),
                        rep_search_bar,
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "➕ Add New Report", color="primary",
                                        href='/assessmentreports/reports_details?mode=add',
                                    ),
                                    width="auto",
                                ),
                                dbc.Col(
                                    html.P(html.B("Filter by Report Type", className="mr-1")),
                                    width="auto"  # Adjust the width to fit the content
                                ),
                                dbc.Col(
                                    dcc.Checklist(
                                        id='report_type',
                                        options=[],
                                        inline=True,
                                        labelStyle={'marginRight': '10px'}  # Adjust the margin as needed
                                    ),
                                    width="auto"  # Adjust the width to fit the content
                                ),
                                dbc.Col(
                                    dbc.Button("Deselect report type filters", id="deselect_button", color="danger", size="sm"),
                                    width="auto",  # Adjust the width to fit the content
                                    style={"margin-left": "auto"}  # Align the button to the right
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            id="content-tab",
                            children=[
                                html.Div(
                                    id='assessmentreports_list',
                                    style={
                                        'marginTop': '20px',
                                        'overflowX': 'auto'  # Adds a horizontal scrollbar
                                    }
                                )
                            ],
                        ),
                    ], width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        )
    ]
)

# S - CHECK THE SQL PLS




#eqa types dropdown
@app.callback(
    Output('report_type', 'options'),
    Input('url', 'pathname')
)
def populate_reporttype_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessment_reports':
        sql ="""
        SELECT reporttype_name as label, reporttype_name as value
        FROM eqateam.report_type
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        reporttype_types = df.to_dict('records')
        return reporttype_types
    else:
        raise PreventUpdate

#eqa deselect
@app.callback(
    Output('report_type', 'value'),
    [Input('deselect_button', 'n_clicks')]
)
def deselect_all_options(n_clicks):
    if n_clicks:
        # Return an empty list to deselect all options
        return []
    else:
        # Return current value if no click event has occurred
        return dash.no_update
























# Callback to load data into the table
@app.callback(
        Output('assessmentreports_list', 'children'),
    [   
        Input('url', 'pathname'),
        Input('report_type', 'value'),
        Input('assessmentreports_filter', 'value'),
    ]
)
def assessmentreports_loadlist(pathname, report_types, searchterm):
    if pathname != '/assessment_reports':
        raise PreventUpdate

    sql = None
    values = []
    cols = []

    sql = """
            SELECT  
                rep_id AS "ID", 
                rep_report_type AS "Report Type",
                dp.pro_degree_title  AS "Degree Program", 
                rep_currentdate AS "Date", 
                rep_checkstatus AS "Check Status",
                rep_link1 AS "File Name",
                rep_checkedby AS "Checked by",
                rep_notes AS "Notes"
            FROM 
                eqateam.reports AS reports
            LEFT JOIN 
                eqateam.program_details AS dp ON reports.rep_degree_programs_id = dp.programdetails_id 
            WHERE
                dp.pro_del_ind IS FALSE
                AND reports.rep_del_ind IS FALSE

        """
    cols = ['ID', 'Report Type' , 'Degree Program', 'Date', 'Check Status', 'File Name', 'Checked by',
                 'Notes']

    df = db.querydatafromdatabase(sql, values, cols)
        
        # Apply search filter if search term is provided
    
    if report_types:
            sql += " AND rep_report_type IN %s"
            values.append(tuple(report_types))

    if searchterm:
        like_pattern = f"%{searchterm}%"
        sql += """ AND (dp.pro_degree_title ILIKE %s OR 
                            rep_report_type ILIKE %s OR
                            rep_checkstatus ILIKE %s OR
                            rep_file1_name ILIKE %s OR
                            CAST(rep_checkstatus AS TEXT) ILIKE %s OR   
                            CAST(rep_notes AS TEXT) ILIKE %s) """       
        values = [like_pattern] * 6
        

    # Execute the query and load data
    if sql:
        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
        #if active_tab == "sar":
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('Edit', href=f'/assessmentreports/reports_details?mode=edit&id={x}', size='sm', color='warning'),
                    style={'text-align': 'center'}
                )
            )
            df = df[['Report Type' , 'Degree Program', 'Date', 'Check Status', 'File Name', 'Checked by',
                     'Notes', 'Action']]


            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        
        else:
            return [html.Div("No records to display")]

    return [html.Div("Query could not be processed")]
