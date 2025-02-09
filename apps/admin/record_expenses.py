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

import datetime

# Using the corrected path
UPLOAD_DIRECTORY = r".\assets\database\admin"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

custom_css = {
    "tabs": {"background-color": "#C2C2C2"},
    "tab": {"padding": "20px"},
    "active_tab": {"background-color": "yellow"}
}

layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
              
                dbc.Col(
                    [
                        html.H1("RECORD EXPENSES"),
                        html.Hr(),
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='recordexpenses_filter',
                                        placeholder='🔎 Search by Payee Name, Status, BUR no.',
                                        className='ml-auto'   
                                    ),
                                    width=8,
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add expense", color="primary", 
                                        href='/record_expenses/add_expense?mode=add', 
                                    ),
                                    width="auto",    
                                ),
                            ],
                            className="align-items-center",   
                            justify="between",  
                        ),
                        html.Br(),

                        dbc.Tabs(
                            [
                                dbc.Tab(label="|   Current   |", tab_id="current"),
                                dbc.Tab(label="|   View All Expenses   |", tab_id="view_all"),
                            ],
                            id="tabs",
                            active_tab="current",
                            style=custom_css["tabs"],
                            className="custom-tabs"
                        ),

                        html.Div(
                            id="tabs-content",
                            children=[
                                html.Div(
                                    id='recordexpenses_list', 
                                    style={
                                        'marginTop': '20px',
                                        'overflowX': 'auto',# This CSS property adds a horizontal scrollbar
                                        'overflowY': 'auto',   
                                        'maxHeight': '1000px',
                                    }
                                )
                            ],
                        ),
                    ], 
                    width=9, 
                    style={'marginLeft': '15px'}
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
    Output("tabs-content", "children"),
    [Input("tabs", "active_tab")],
)
def switch_tab(tab):
    if tab == "current":
        return [
            html.Div(
                id='recordexpenses_list', 
                style={
                    'marginTop': '20px',
                    'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                }
            )
        ]
    elif tab == "view_all":
        return [
            html.Div(
                id='recordexpenses_list', 
                style={
                    'marginTop': '20px',
                    'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                }
            )
        ]
    return html.Div("No Tab Selected")

@app.callback(
    Output('recordexpenses_list', 'children'),
    [
        Input('url', 'pathname'),   
        Input('recordexpenses_filter', 'value'),
        Input("tabs", "active_tab")
    ]
)
def recordexpenses_loadlist(pathname, searchterm, active_tab):
    if pathname == '/record_expenses':
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        
        if active_tab == "current":
            sql = """
                SELECT 
                    exp_id AS "ID",
                    exp_date AS "Date", 
                    exp_payee AS "Payee Name", 
                    me.main_expense_name AS "Main Expense Type",
                    se.sub_expense_name AS "Sub Expense Type",
                    exp_particulars AS "Particulars", 
                    exp_amount AS "Amount", 
                    es.expense_status_name AS "Status",
                    exp_bur_no AS "BUR No",
                    exp_submitted_by AS "Submitted by",
                    exp_receipt_name AS "File",
                    exp_receipt_path AS "File Path"
                FROM adminteam.expenses AS e
                LEFT JOIN adminteam.main_expenses AS me ON e.main_expense_id = me.main_expense_id
                LEFT JOIN adminteam.sub_expenses AS se ON e.sub_expense_id = se.sub_expense_id
                LEFT JOIN adminteam.expense_status AS es ON e.exp_status = es.expense_status_id
                WHERE 
                    EXTRACT(MONTH FROM exp_date) = %s 
                    AND EXTRACT(YEAR FROM exp_date) = %s
                    AND exp_del_ind IS FALSE
            """
            values = [current_month, current_year]

            if searchterm:
                sql += """ AND (exp_payee ILIKE %s OR es.expense_status_name ILIKE %s OR exp_bur_no ILIKE %s) """
                like_pattern = f"%{searchterm}%"
                values.extend([like_pattern, like_pattern, like_pattern])

            cols = ['ID', 'Date', 'Payee Name', 'Main Expense Type', 
                    'Sub Expense Type', 'Particulars', 'Amount', 'Status', 
                    'BUR No', 'Submitted by','File', 'File Path']

        elif active_tab == "view_all":
            sql = """
                SELECT 
                    exp_id AS "ID",
                    exp_date AS "Date", 
                    exp_payee AS "Payee Name", 
                    me.main_expense_name AS "Main Expense Type",
                    se.sub_expense_name AS "Sub Expense Type",
                    exp_particulars AS "Particulars", 
                    exp_amount AS "Amount", 
                    es.expense_status_name AS "Status",
                    exp_bur_no AS "BUR No",
                    exp_submitted_by AS "Submitted by",
                    exp_receipt_name AS "File",
                    exp_receipt_path AS "File Path"
                FROM adminteam.expenses AS e
                LEFT JOIN adminteam.main_expenses AS me ON e.main_expense_id = me.main_expense_id
                LEFT JOIN adminteam.sub_expenses AS se ON e.sub_expense_id = se.sub_expense_id
                LEFT JOIN adminteam.expense_status AS es ON e.exp_status = es.expense_status_id
                WHERE
                    exp_del_ind IS FALSE
            """
            values = []
            cols = ['ID', 'Date', 'Payee Name', 'Main Expense Type',
                    'Sub Expense Type', 'Particulars', 'Amount', 'Status', 
                    'BUR No', 'Submitted by','File', 'File Path']

            if searchterm:
                sql += """ AND (exp_payee ILIKE %s OR es.expense_status_name ILIKE %s OR exp_bur_no ILIKE %s) """
                like_pattern = f"%{searchterm}%"
                values.extend([like_pattern, like_pattern, like_pattern])

        df = db.querydatafromdatabase(sql, values, cols)
 
    else:
        return [html.Div("Invalid tab selection")]

    if not df.empty:
        df["Action"] = df["ID"].apply(
            lambda x: html.Div(
                dbc.Button('Edit', href=f'/record_expenses/add_expense?mode=edit&id={x}', size='sm', color='warning'),
                style={'text-align': 'center'}
            )
        )
        df = df[['Date', 'Payee Name', 'Main Expense Type', 'Sub Expense Type',
                'Particulars', 'Amount', 'Status', 'BUR No', 'Submitted by', 
                'File', 'Action']]
                
        df['File'] = df.apply(lambda row: html.A(row['File'], href=os.path.join(UPLOAD_DIRECTORY, row['File']) if row['File'] else ''), axis=1)

        df['Amount'] = df['Amount'].apply(lambda x: '{:,.2f}'.format(x))
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return [table]
        
    else:
        return [html.Div("No records to display")]

    return [html.Div("Query could not be processed")]
