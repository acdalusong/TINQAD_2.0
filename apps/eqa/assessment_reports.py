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
sar_search_bar = dbc.Col(
    dbc.Input(
        type='text',
        id='assessmentreports_filter_sar',
        placeholder='🔎 Search by Degree Program, Status, SAR Score',
        className='ml-auto'
    ),
    width="12",
    id='sar_search_bar'
)

others_search_bar = dbc.Col(
    dbc.Input(
        type='text',
        id='assessmentreports_filter_others',
        placeholder='🔎 Search by Degree Program, Assessment Title, EQA Type, Status, Report Type',
        className='ml-auto'
    ),
    width="12",
    id='others_search_bar'
)

# Define the layout
layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("ASSESSMENT REPORTS"),
                        html.Hr(),
                        sar_search_bar,
                        others_search_bar,
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "➕ Add New SAR", color="primary",
                                        href='/assessmentreports/sar_details?mode=add',
                                    ),
                                    width="auto",
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "➕ Add New Assessment", color="warning",
                                        href='/assessmentreports/assessment_details?mode=add',
                                    ),
                                    width="auto",
                                )
                            ]
                        ),
                        html.Br(),
                        dbc.Tabs(
                            [
                                dbc.Tab(label="|   Self Assessment Reports   |", tab_id="sar"),
                                dbc.Tab(label="|   Other Assessments   |", tab_id="others"),
                            ],
                            id="tabs",
                            active_tab="sar",
                            className="custom-tabs"
                        ),
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

# Callback to update the visibility of search bars
@app.callback(
    [Output('sar_search_bar', 'style'),
     Output('others_search_bar', 'style')],
    [Input('tabs', 'active_tab')]
)
def update_search_bar_visibility(active_tab):
    sar_style = {'display': 'none'} if active_tab != 'sar' else {}
    others_style = {'display': 'none'} if active_tab != 'others' else {}
    return sar_style, others_style

# Callback to disable input fields based on active tab
@app.callback(
    [Output('assessmentreports_filter_sar', 'disabled'),
     Output('assessmentreports_filter_others', 'disabled')],
    [Input('tabs', 'active_tab')]
)
def disable_input(active_tab):
    sar_disabled = active_tab != 'sar'
    others_disabled = active_tab != 'others'
    return sar_disabled, others_disabled

















# Callback to load data into the table
@app.callback(
        Output('assessmentreports_list', 'children'),
    [   
        Input('url', 'pathname'),
        Input('assessmentreports_filter_sar', 'value'),
        Input('assessmentreports_filter_others', 'value'),
        Input('tabs', 'active_tab')
    ]
)
def assessmentreports_loadlist(pathname, sar_searchterm, others_searchterm, active_tab):
    if pathname != '/assessment_reports':
        raise PreventUpdate

    sql = None
    values = []
    cols = []

    if active_tab == "sar":
        sql = """
            SELECT  
                sarep_id AS "ID", 
                sarep_currentdate AS "Date", 
                dp.pro_degree_title  AS "Degree Program", 
                sarep_checkstatus AS "Check Status",
                sarep_link AS "SAR Link",
                sarep_file_name AS "SAR File",
                sarep_file_path AS "File Path",
                sarep_review_status AS "Review Status",
                sarep_datereviewed AS "Date Reviewed",
                sarep_assessedby AS "Assessed by",
                sarep_notes AS "Notes",
                sarep_sarscore AS "SAR Score"
            FROM 
                eqateam.sar_report AS ar
            LEFT JOIN 
                eqateam.program_details AS dp ON ar.sarep_degree_programs_id = dp.programdetails_id 
            LEFT JOIN 
                eqateam.review_status AS rs ON ar.sarep_review_status = rs.review_status_id 
            WHERE
                sarep_del_ind IS FALSE
        """
        cols = ['ID', 'Date', 'Degree Program', 'Check Status', 'SAR Link', 'SAR File', 'File Path', 'Review Status',
                'Date Reviewed', 'Assessed by', 'Notes', 'SAR Score']

        df = db.querydatafromdatabase(sql, values, cols)
        
        # Apply search filter if search term is provided
        if sar_searchterm:
            like_pattern = f"%{sar_searchterm}%"
            sql += """ AND (dp.pro_degree_title ILIKE %s OR 
                            sarep_checkstatus ILIKE %s OR
                            sarep_link ILIKE %s OR
                            sarep_file_name ILIKE %s OR
                            CAST(sarep_review_status AS TEXT) ILIKE %s OR   
                            CAST(sarep_sarscore AS TEXT) ILIKE %s) """       
            values = [like_pattern] * 6
        
        
    elif active_tab == "others":
        sql = """
            SELECT 
                arep_id AS "ID",
                arep_currentdate AS "Date",
                arep_degree_programs_id AS "Degree Program",
                arep_title AS "Assessment Title",
                appr.approv_eqa_name AS "EQA Type",
                arep_assessedby AS "Assessed by",
                rt.report_type_name AS "Report Type",
                arep_report_type_notes AS "Report Notes",
                arep_link AS "Link",
                arep_file_name AS "File",
                arep_file_path AS "File Path",
                arep_checkstatus AS "Check Status",
                arep_datereviewed AS "Date Reviewed",
                arep_review_status AS "Review Status",
                arep_notes AS "Notes"
            FROM 
                eqateam.assess_report AS assr
            LEFT JOIN 
                eqateam.report_type AS rt ON assr.arep_report_type = rt.report_type_id 
            LEFT JOIN 
                eqateam.review_status AS rs ON assr.arep_review_status = rs.review_status_id 
            LEFT JOIN
                eqateam.approv_eqa AS appr ON assr.arep_approv_eqa = appr.approv_eqa_id
            
            WHERE
                arep_del_ind IS FALSE
        """
        cols = ['ID','Date', 'Degree Program', 'Assessment Title', 'EQA Type', 'Assessed by',
                'Report Type', 'Report Notes', "Link",'File', 'File Path', 'Check Status', 'Date Reviewed', "Review Status", 'Notes']
        
        

        # Apply search filter if search term is provided
        if others_searchterm:
            like_pattern = f"%{others_searchterm}%"
            sql += """ AND (CAST(arep_degree_programs_id AS TEXT) ILIKE %s OR
                            arep_title ILIKE %s OR
                            CAST(arep_approv_eqa AS TEXT) ILIKE %s OR       
                            arep_checkstatus ILIKE %s OR
                            rt.report_type_name ILIKE %s OR
                            rs.review_status_name ILIKE %s) """
            values = [like_pattern] * 6

    else:
        return [html.Div("Invalid tab selection")]

    # Execute the query and load data
    if sql:
        df = db.querydatafromdatabase(sql, values, cols)
        
        if "Review Status" in df.columns:
            df["Review Status"] = df["Review Status"].replace({1: "Endorsed for EQA", 2: "For Revision"})

        if not df.empty:
            if active_tab == "sar":
                df["Action"] = df["ID"].apply(
                    lambda x: html.Div(
                        dbc.Button('Edit', href=f'/assessmentreports/sar_details?mode=edit&id={x}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
                df = df[['Date', 'Degree Program', 'Check Status', 'SAR Link', 'SAR File', 'Review Status',
                        'Date Reviewed', 'Assessed by', 'Notes', 'SAR Score', 'Action']]
                 
                df['SAR File'] = df.apply(lambda row: html.A(row['SAR File'], href=os.path.join(UPLOAD_DIRECTORY, row['SAR File']) if row['SAR File'] else ''), axis=1)
            
            elif active_tab == "others":
                df["Action"] = df["ID"].apply(
                    lambda x: html.Div(
                        dbc.Button('Edit', href=f'/assessmentreports/assessment_details?mode=edit&id={x}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
                df = df[['Date', 'Degree Program', 'Assessment Title', 'EQA Type', 'Assessed by',
                         'Report Type', 'Report Notes', "Link", 'File', 'Check Status', 'Date Reviewed', "Review Status", 'Notes', 'Action']]
                 
                df['File'] = df.apply(lambda row: html.A(row['File'], href=os.path.join(UPLOAD_DIRECTORY, row['File']) if row['File'] else ''), axis=1)
            

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        
        else:
            return [html.Div("No records to display")]

    return [html.Div("Query could not be processed")]
