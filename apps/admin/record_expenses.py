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
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H1("RECORD EXPENSES"),
                                    style={"marginRight": "auto"}  
                                ),
                                dbc.Col( 
                                    dbc.Button(
                                        "➕ Add expense", color="primary", 
                                        href='/record_expenses/add_expense?mode=add', 
                                    ),
                                    width="auto",
                                    style={"marginLeft": "auto"},   
                                ),
                            ],
                            style={"marginBottom": "-10px"}
                        ),
                        html.Hr(),
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    html.Label(
                                        "Payee Name:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='payee_name_filter',
                                        placeholder='Search by Payee Name',
                                        className='ml-auto'   
                                    ),
                                    width=4,
                                ),
                            ],
                            className="align-items-center mb-2",    
                        ),
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    html.Label(
                                        "Main Expense Type:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dcc.Dropdown(
                                    id="main_expense_filter",
                                    options=[],
                                    placeholder=" Select Main Expense"
                                    ),
                                    width=4,
                                ),
                                dbc.Col(  
                                    html.Label(
                                        "Sub Expense Type:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                            "width": "100%"}
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dcc.Dropdown(
                                    id="sub_expense_filter",
                                    options=[],
                                    placeholder=" Select Sub Expense"
                                    ),
                                    width=4,
                                ),
                            ],
                            className="align-items-center mb-2",   
                        ),
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    html.Label(
                                        "Select Status:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                            "width": "100%"}
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dcc.Dropdown(
                                    id="status_filter",
                                    options=[
                                        {"label": "Approved", "value": "Approved"},
                                        {"label": "Pending", "value": "Pending"},
                                        {"label": "Denied", "value": "Denied"},
                                    ],
                                    placeholder=" Select Status"
                                    ),
                                    width=4,
                                ),
                                dbc.Col(  
                                    html.Label(
                                        "BUR No:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='burno_filter',
                                        placeholder='Search by Bur No',
                                        className='ml-auto'   
                                    ),
                                    width=4,
                                ),
                            ],
                            className="align-items-center mb-2",   
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

#main expense dropdown
@app.callback(
    [
        Output('main_expense_filter', 'options'),
    ],
    [
        Input('url', 'pathname')
    ],
)

def populate_mainexpenses_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/record_expenses':
        sql = """
            SELECT main_expense_name as label,  main_expense_id  as value
            FROM adminteam.main_expenses

            WHERE main_expense_del_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        main_expense_types = df.to_dict('records')    
    else:
        raise PreventUpdate
    return [main_expense_types]

#sub expense dropdown
@app.callback(
    Output('sub_expense_filter', 'options'),
    Input('main_expense_filter', 'value')
)
def update_subexpenses_options(selected_main_expense):
    if selected_main_expense is None:
        return []  # Return empty options if no main expense is selected
    
    try:
        # Query to fetch sub-expenses based on the selected main expense
        sql = """
        SELECT sub_expense_name as label, sub_expense_id as value
        FROM adminteam.sub_expenses
        WHERE main_expense_id = %s
        """
        values = [selected_main_expense]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        sub_expense_options = df.to_dict('records')
        return sub_expense_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 

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
        Input('payee_name_filter', 'value'),
        Input('status_filter', 'value'),
        Input('main_expense_filter', 'value'),
        Input('sub_expense_filter', 'value'),
        Input('burno_filter', 'value'),
        Input("tabs", "active_tab")
    ]
)
def recordexpenses_loadlist(pathname, searchterm, status, main_expense, sub_expense, bur_no, active_tab):
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
                sql += """ AND (exp_payee ILIKE %s) """
                name_like_pattern = f"%{searchterm}%"
                values.append([name_like_pattern])

            if status:
                sql += """ AND es.expense_status_name = %s """
                values.append(status)
            
            if main_expense:
                sql += """ AND me.main_expense_id = %s"""
                values.append(main_expense)
            
            if main_expense and sub_expense:
                sql += """ AND se.sub_expense_id = %s"""
                values.append(sub_expense)
            
            if bur_no:
                sql += """ AND exp_bur_no ILIKE %s"""
                burno_like_pattern = f"%{bur_no}%"
                values.append(burno_like_pattern)

            # Add ORDER BY clause at the end
            sql += " ORDER BY exp_timestamp DESC"

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
                sql += """ AND (exp_payee ILIKE %s) """
                name_like_pattern = f"%{searchterm}%"
                values.extend([name_like_pattern])

            if status:
                sql += """ AND es.expense_status_name = %s """
                values.append(status)
            
            if main_expense:
                sql += """ AND me.main_expense_id = %s"""
                values.append(main_expense)
            
            if main_expense and sub_expense:
                sql += """ AND se.sub_expense_id = %s"""
                values.append(sub_expense)
            
            if bur_no:
                sql += """ AND exp_bur_no ILIKE %s"""
                burno_like_pattern = f"%{bur_no}%"
                values.extend(burno_like_pattern)

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
