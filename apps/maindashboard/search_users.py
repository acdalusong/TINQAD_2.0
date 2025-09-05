import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

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
                        html.H1("SEARCH USERS"),
                        html.Hr(),
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='searchusers_filter',
                                        placeholder='🔎 Search by name, office, position',
                                        className='ml-auto'   
                                    ),
                                    width=8,
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New", color="primary", 
                                        href='/register_user?mode=add', 
                                    ),
                                    width="auto",    
                                ),
                            ],
                            className="align-items-center",   
                            justify="between",  
                        ),
                         
                        html.Div(
                            id='searchusers_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto',
                                'overflowY': 'auto',   
                                'maxHeight': '800px',   
                            }
                        )
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
    [
        Output('searchusers_list', 'children')
    ],
    [
        Input('url', 'pathname'),  
        Input('searchusers_filter', 'value'),
    ]
)

def searchusers_loaduserlist(pathname, searchterm):
    if pathname == '/search_users':
        # Updated SQL query to join with the offices table
        sql = """  
            SELECT 
                u.user_id AS "ID",
                u.user_id_num AS "ID number",
                u.user_sname AS "Surname", 
                u.user_fname AS "First Name", 
                u.user_livedname AS "Nickname",
                o.office_name AS "Dept",  
                u.user_position AS "Position", 
                u.user_email AS "Email",  
                u.user_phone_num AS "Phone",
                u.user_bday AS "Birthday" 
            FROM maindashboard.users u
            LEFT JOIN maindashboard.offices o ON u.user_office = o.office_id
            WHERE 
                NOT user_del_ind
        """

        cols = ['ID','ID number','Surname', 'First Name', 'Nickname','Dept', 'Position', 'Email', 'Phone', 'Birthday']

        if searchterm:
            sql += """ AND (u.user_sname ILIKE %s OR u.user_fname ILIKE  %s OR u.user_position ILIKE %s OR 
                o.office_name ILIKE %s) """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern, like_pattern, like_pattern]
        else:
            values = []

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0] > 0:
            buttons = []
            for user_id in df['ID']:
                buttons.append(
                    html.Div(
                        dbc.Button('Edit',
                                   href=f'register_user?mode=edit&id={user_id}',
                                   size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
            df['Action'] = buttons

            df = df[['ID number','Surname', 'First Name', 'Nickname','Dept', 'Position', 'Email', 'Phone', 'Birthday', 'Action']]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    else:
        raise PreventUpdate
