import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, no_update
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db


def map_academic_calendar_type(academic_calendar_type):
    if academic_calendar_type == 1:
        return "Semester"
    elif academic_calendar_type == 2:
        return "Trimester"
    else:
        return "Unknown"


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("PROGRAM LIST"),
                        html.Hr(),
                        
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='programlist_filter',
                                        placeholder=' Search by Degree Program, College, Department, Cluster',
                                        className='ml-auto'   
                                    ),
                                    width="6",
                                ),
                                dbc.Col(    
                                        dcc.Dropdown(
                                            id='cluster_dropdown',
                                            options=[
                                                {'label': 'ALC', 'value': '1'},
                                                {'label': 'MEC', 'value': '2'},
                                                {'label': 'SLC', 'value': '3'},
                                                {'label': 'STC', 'value': '4'}
                                            ],
                                            placeholder="Filter by cluster",
                                        ),
                                        width="2",
                                ),
                                dbc.Col(    
                                        dcc.Dropdown(
                                            id='progtype_dropdown',
                                            options=[
                                                {'label': 'Certificate', 'value': '1'},
                                                {'label': 'Diploma', 'value': '2'},
                                                {'label': 'Associate', 'value': '3'},
                                                {'label': 'Undergraduate', 'value': '4'},
                                                {'label': 'Masters', 'value': '5'},
                                                {'label': 'Doctorate', 'value': '6'}
                                            ],
                                            placeholder="Filter by Program Type",
                                        ),
                                        width="2",
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "+ Add Program", color="primary", 
                                        href='/program_details?mode=add', 
                                    ),
                                    width="auto",    
                                ),
                                #dbc.Col(   
                                #    dbc.Button(
                                #        "+ Add Program Info", color="warning", 
                                #        href='/program_info', 
                                #    ),
                                #    width="auto",    
                                #),
                            ],
                            className="align-items-center",   
                            justify="between",  
                        ),

 
                        html.Div(
                            id='programlist_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto', 
                                'overflowY': 'auto',   
                                'maxHeight': '800px',
                            }
                        ),

                        html.Br(),
                        html.Br(),

                    ], width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        )
    ]
)


@app.callback(
    [
        Output('programlist_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('programlist_filter', 'value'),
        Input('cluster_dropdown', 'value'), 
        Input('progtype_dropdown', 'value')
    ]
)
def programlist_loadlist(pathname, searchterm, sel_cluster, sel_progtype):
    if pathname == '/program_list':
        sql = """  
            SELECT
                pd.programdetails_id AS "ID",
                pd.pro_degree_title AS "Degree Program",
                c.college_name AS "College",
                du.deg_unit_name AS "Department",
                cl.cluster_shortname AS "Cluster",
                pt.programtype_name AS "Program Type",
                pro_calendar_type_id AS "Academic Calendar Type"
            FROM
                eqateam.program_details pd
                INNER JOIN public.college c ON pd.pro_college_id = c.college_id
                INNER JOIN public.deg_unit du ON pd.pro_department_id = du.deg_unit_id
                INNER JOIN public.clusters cl ON pd.pro_cluster_id = cl.cluster_id
                INNER JOIN eqateam.program_type pt ON pd.pro_program_type_id = pt.programtype_id
            WHERE 
                pd.pro_del_ind = false
        """
        cols = ['ID', "Degree Program", "College", "Department", "Cluster",  "Program Type", 
                "Academic Calendar Type"]
        
        values = []

        if sel_cluster:  # Add condition to filter by selected cluster
            sql += " AND cl.cluster_id = %s"
            values.append(sel_cluster)

        if sel_progtype:  # selected_years will be a list of selected progtype
            sql += " AND pt.programtype_id IN %s"
            values.append(tuple(sel_progtype))

        if searchterm:
            like_pattern = f"%{searchterm}%"
            additional_conditions = """
                AND (
                    pd.pro_degree_title ILIKE %s
                    OR c.college_name ILIKE %s
                    OR du.deg_unit_name ILIKE %s
                    OR cl.cluster_shortname ILIKE %s
                )
            """
            values.extend([like_pattern, like_pattern, like_pattern, like_pattern])
            sql += additional_conditions

        final_sql = sql + " ORDER BY pd.pro_degree_title"
         
        df = db.querydatafromdatabase(final_sql, values, cols)
        
        if df.shape[0] > 0:
            view_buttons = []
            edit_buttons = []
            for programdetails_id in df['ID']:
                view_buttons.append(
                    html.Div(
                        dbc.Button('View Program Page',
                                   href=f'program_page?id={programdetails_id}',
                                   size='sm', color='primary'),
                        style={'text-align': 'center'}
                    )
                )
                edit_buttons.append(
                    html.Div(
                        dbc.Button('Edit Program',
                                   href=f'program_details?mode=edit&id={programdetails_id}',
                                   size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
            df['View Page'] = view_buttons
            df['Edit'] = edit_buttons

            # Apply mapping function to "Academic Calendar Type" column
            df["Academic Calendar Type"] = df["Academic Calendar Type"].map(map_academic_calendar_type)

            df = df[["View Page", "Degree Program", "College", "Department", "Cluster",  "Program Type", 
                      "Academic Calendar Type", "Edit"]]

        # Generate the table from the filtered DataFrame
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    else:
        raise PreventUpdate

