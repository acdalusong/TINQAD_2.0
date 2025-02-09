from dash import dash, html, Input, Output, State
import dash_bootstrap_components as dbc
 
import dash 
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go

from app import app
from apps import commonmodules as cm
from apps import dbconnect as db
from datetime import datetime


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("Expense Types List"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                        dbc.Button("Add Expense Type", color="primary"),
                                        href="/expense_list/add_expensetype",
                                        style={"text-align": "right"}
                                    ),
                                    width={"size": 8}  
                                ),
                            ],
                        ),

                        html.Div(
                            id='expensetype_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto', 
                                'overflowY': 'auto',   
                                'maxHeight': '800px',
                            }
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
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)


@app.callback(
    Output('expensetype_list', 'children'),
    [Input('url', 'pathname')]
)
def expensetype_list (pathname):
    if pathname == '/expense_list':
        sql = """
            SELECT 
                se.sub_expense_id AS "ID",
                me.main_expense_shortname AS "Main Expense",
                se.sub_expense_name AS "Sub Expense"
            FROM 
                adminteam.sub_expenses se
            JOIN
                adminteam.main_expenses me ON se.main_expense_id = me.main_expense_id 
           
        """
         #WHERE 
               # se.sub_expense_del_ind = FALSE;
        cols = ["ID", "Main Expense", "Sub Expense"]

        # Execute the query and fetch the data
        df = db.querydatafromdatabase(sql, [], cols)

        if df.shape[0] > 0:
            # Add an Action column with a button for each row
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('Remove', id={'type': 'remove-button', 'index': x}, 
                               size='sm', color='danger'), style={'text-align': 'center'})
            )

            # Select only the columns you want to display
            df = df[["Main Expense", "Sub Expense", "Action"]]

            # Create a list of rows for the table
            table_rows = []
            for _, row in df.iterrows():
                table_rows.append(html.Tr([
                    html.Td(row["Main Expense"]),
                    html.Td(row["Sub Expense"]),
                    html.Td(row["Action"]),
                ]))

            # Return the table
            return [dbc.Table(
                # Header
                [html.Thead(html.Tr([html.Th(col) for col in df.columns]))] + 
                # Body
                [html.Tbody(table_rows)]
            )]
        else:
            return [html.Div("No expense types listed")]

    else:
        raise PreventUpdate
    



@app.callback(
    Output('expensetype_list', 'children', allow_duplicate=True),
    [Input({'type': 'remove-button', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State({'type': 'remove-button', 'index': dash.dependencies.ALL}, 'id')],
    prevent_initial_call=True
)
def remove_expensetype (n_clicks_list, button_id_list):
    if not n_clicks_list or not any(n_clicks_list):
        raise PreventUpdate

    outputs = []
    for n_clicks, button_id in zip(n_clicks_list, button_id_list):
        if n_clicks:
            expensetype_id = button_id['index']
            update_expense_sql = """
                UPDATE adminteam.sub_expenses
                SET sub_expense_del_ind = TRUE
                WHERE sub_expense_id = %s
            """
            db.modifydatabase(update_expense_sql, [expensetype_id])
            # Append the updated table to outputs list
            outputs.append(expensetype_list('/expense_list')[0])

    return outputs

 
