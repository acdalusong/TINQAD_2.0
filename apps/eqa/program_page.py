import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime 
#import os

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db
from urllib.parse import urlparse, parse_qs



#Part 1 - basic info
progbasiccard = dbc.Card(
    [
        dbc.CardHeader(html.H5(html.B("Basic Information"))), 
        dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Div("Degree Program", className="fw-bold text-primary fs-4 mb-2"),
                html.Div(id="pp_deg_prog", className="fs-5") 
            ], width=6),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                html.Div("College", className="fw-bold"),
                html.Div(id="pp_college")  
            ], width=6),
            dbc.Col([
                html.Div("Cluster", className="fw-bold"),
                html.Div(id="pp_cluster") 
            ], width=6),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                html.Div("Program Type", className="fw-bold"),
                html.Div(id="pp_progtype") 
            ], width=6),
            dbc.Col([
                html.Div("Department", className="fw-bold"),
                html.Div(id="pp_dept") 
            ], width=6),
        ]),
    ]),
    ],
    className="mb-4"
)


#Part 2 - reports
progrepscard = dbc.Card(
    [
        dbc.CardHeader(
            html.H5(html.B("Reports Submitted"))
        ),
        dbc.CardBody([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(
                            type='text',
                            id='progrepscard_search',
                            placeholder='🔎 Search by report type, status, notes, etc',
                            className='ml-auto'
                        ),
                        width=8
                    ),
                ],
                className="align-items-center",
                style={
                    "margin-right": "2px",
                    "margin-bottom": "15px",
                }
            ),
            html.Div(id='progrepstable')
        ])
    ],
    className="mb-3"
)


#Part 3 - eqa assessments
progeqacard = dbc.Card(
    [
        dbc.CardHeader(
            html.H5(html.B("EQA Activities"))
        ),
        dbc.CardBody([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(
                            type='text',
                            id='progeqacard_search',
                            placeholder='🔎 Search by date, EQA Type, notes, etc',
                            className='ml-auto'
                        ),
                        width=8
                    ),
                ],
                className="align-items-center",
                style={
                    "margin-right": "2px",
                    "margin-bottom": "15px",
                }
            ),
            html.Div(id='progeqatable')
        ])
    ],
    className="mb-3"
)




layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("PROGRAM PROFILE"),
                        html.Hr(),
                        html.Br(),

                        progbasiccard,
                        progrepscard,
                        progeqacard,
                        html.Br(),
                        html.Br(),
                        
                    ], 
                    width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)


#for basic info
@app.callback(
    Output("pp_deg_prog", "children"),
    Output("pp_college", "children"),
    Output("pp_dept", "children"),
    Output("pp_cluster", "children"),
    Output("pp_progtype", "children"),
    Input("url", "search")  # or some other trigger like dropdown
)
def load_program_details(search):
    parsed = urlparse(search)
    program_id = parse_qs(parsed.query).get("id", [None])[0]

    if program_id is None:
        raise PreventUpdate

    sql = """  
            SELECT
                pd.pro_degree_title,
                c.college_name,
                du.deg_unit_name,
                cl.cluster_shortname,
                pt.programtype_name
            FROM
                eqateam.program_details pd
                INNER JOIN public.college c ON pd.pro_college_id = c.college_id
                INNER JOIN public.deg_unit du ON pd.pro_department_id = du.deg_unit_id
                INNER JOIN public.clusters cl ON pd.pro_cluster_id = cl.cluster_id
                INNER JOIN eqateam.program_type pt ON pd.pro_program_type_id = pt.programtype_id
            WHERE 
                pd.programdetails_id = %s
        """
    values = [program_id]
    cols = ["Degree Program", "College", "Department", "Cluster", "Program Type"]

    df = db.querydatafromdatabase(sql, values, cols)

    if df.shape[0] == 0:
        return ["N/A"] * 5

    row = df.iloc[0]
    return row["Degree Program"], row["College"], row["Department"], row["Cluster"], row["Program Type"]


#____________________________________________________________________________
#for progreps table
@app.callback(
        Output('progrepstable', 'children'),
    [   
        Input('url', 'pathname'),
        Input('url', 'search'),
        Input('progrepscard_search', 'value'),
    ]
)
def progreps_loadlist(pathname, search, searchterm):
    if pathname != '/program_page':
        raise PreventUpdate

    parsed = urlparse(search)
    program_id = parse_qs(parsed.query).get("id", [None])[0]

    if program_id is None:
        raise PreventUpdate

    sql = """
            SELECT  
                rep_id AS "ID", 
                rep_report_type AS "Report Type",
                dp.pro_degree_title  AS "Degree Program", 
                rep_currentdate AS "Date", 
                rep_checkstatus AS "Check Status",
                rep_link1 AS "File Name",
                rep_checkedby AS "Checked by",
                rep_datechecked AS "Date Checked",
                rep_notes AS "Notes"
            FROM 
                eqateam.reports AS reports
            LEFT JOIN 
                eqateam.program_details AS dp ON reports.rep_degree_programs_id = dp.programdetails_id 
            WHERE
                dp.programdetails_id = %s
        """
    values = [program_id]
    cols = ['ID', 'Report Type' , 'Degree Program', 'Date', 'Check Status', 'File Name', 'Checked by',
                'Date Checked', 'Notes']

    df = db.querydatafromdatabase(sql, values, cols)
        
        # Apply search filter if search term is provided
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
                    'Date Checked', 'Notes', 'Action']]


            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        
        else:
            return [html.Div("No records to display")]

    return [html.Div("Query could not be processed")]



#___________________________________________________________________________________________
#for progeqa table

@app.callback(
        Output('progeqatable', 'children'),
    [   
        Input('url', 'pathname'),
        Input('url', 'search'),
        Input('progeqacard_search', 'value'),
    ]
)
def progeqa_loadlist(pathname, search, searchterm):
    if pathname != '/program_page':
        raise PreventUpdate

    parsed = urlparse(search)
    program_id = parse_qs(parsed.query).get("id", [None])[0]

    if program_id is None:
        raise PreventUpdate
    
    sql = """  
            SELECT 
                a.arep_id AS "ID",
                arep_year AS "Year",
                TO_CHAR(arep_sched_startdate, 'FMMonth FMDD, YYYY') AS "Start Date", 
                arep_degree_programs_id AS "Degree Program", 
                arep_assessedby AS "Assessing Body",
                eqa.approv_eqa_name AS "EQA Type",
                arep_notes AS "Notes"
            FROM 
                eqateam.assess_report AS a 
            JOIN 
                eqateam.approv_eqa AS eqa ON a.arep_approv_eqa = eqa.approv_eqa_id
            WHERE
                a.arep_degree_programs_id = %s
        """

    cols = ['ID', 'Year', 'Start Date', 'Degree Program' , 'Assessing Body','EQA Type', 'Notes']   
        
    values = [program_id]
        
    if searchterm:
            # Adding search condition for arep_title and arep_degree_programs_id
        sql += " AND (arep_notes ILIKE %s OR arep_degree_programs_id ILIKE %s OR arep_assessedby ILIKE %s)"
        values.extend(['%' + searchterm + '%', '%' + searchterm + '%', '%' + searchterm + '%'])


    df = db.querydatafromdatabase(sql, values, cols) 

        # Generate the table from the DataFrame
    if not df.empty:
        df["Action"] = df["ID"].apply(
            lambda x: html.Div(
                dbc.Button('Edit', href=f'/assessment_tracker/assessment_details?mode=edit&id={x}', size='sm', color='warning'),
                style={'text-align': 'center'}
            )
        )
        df = df[['Year', 'Start Date', 'Degree Program' , 'Assessing Body','EQA Type', 'Notes', 'Action']]
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return [table]
        
    else:
        return [html.Div("No records to display")]
        