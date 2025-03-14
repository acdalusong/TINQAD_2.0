from dash import dash, html, dcc, Input, Output, State, no_update
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
                        
                        # Confirmation Modal: asks the user to confirm the removal
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Confirm Choice of Removal"), className="bg-primary"),
                                dbc.ModalBody(html.H5("Are you sure you want to remove this expense type?")),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="confirm-modal-cancel", color="warning"),
                                        dbc.Button("Confirm", id="confirm-modal-confirm", color="danger"),
                                    ]
                                ),
                            ],
                            id="confirm-modal",
                            centered=True,
                            is_open=False,
                            backdrop="static"
                        ),
                        # Final Modal: notifies the user that the removal is complete
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Removed Successfully"), className="bg-success"),
                                dbc.ModalBody(html.H5("Expense type has been successfully removed."))
                            ],
                            id="final-modal",
                            centered=True,
                            is_open=False,
                        ),
                    ],
                    width=9,
                    style={'marginLeft': '15px'},
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
        ),
    ]
)

# Generates the expense types table.
@app.callback(
    Output('expensetype_list', 'children'),
    [Input('url', 'pathname')]
)
def expensetype_list(pathname):
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
            WHERE 
                se.sub_expense_del_ind = FALSE;
        """
        cols = ["ID", "Main Expense", "Sub Expense"]

        # Execute the query and fetch the data
        df = db.querydatafromdatabase(sql, [], cols)

        if df.shape[0] > 0:
            # Add an Action column with a removal button for each row.
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button(
                        'Remove',
                        id={'type': 'remove-button', 'index': x},
                        size='sm',
                        color='danger'
                    ),
                    style={'text-align': 'center'}
                )
            )

            # Select only the columns to display
            df = df[["Main Expense", "Sub Expense", "Action"]]

            # Build the table rows
            table_rows = []
            for _, row in df.iterrows():
                table_rows.append(html.Tr([
                    html.Td(row["Main Expense"]),
                    html.Td(row["Sub Expense"]),
                    html.Td(row["Action"]),
                ]))

            # Return the complete table
            return [dbc.Table(
                # Table header
                [html.Thead(html.Tr([html.Th(col) for col in df.columns]))] +
                # Table body
                [html.Tbody(table_rows)]
            )]
        else:
            return [html.Div("No expense types listed")]
    else:
        raise PreventUpdate

# Callback to process confirmation modals
@app.callback(
    [
        Output('expensetype_list', 'children', allow_duplicate=True),
        Output("confirm-modal", "is_open"),
        Output("final-modal", "is_open")
    ],
    [
        Input({'type': 'remove-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
        Input("confirm-modal-confirm", "n_clicks"),
        Input("confirm-modal-cancel", "n_clicks"),
    ],
    [
        State({'type': 'remove-button', 'index': dash.dependencies.ALL}, 'id'),
        State("confirm-modal", "is_open"),
    ],
    prevent_initial_call=True
)
def process_removal(n_clicks_list, confirm_btn, cancel_btn, button_id_list, confirmationmodal):
    
    output_list = no_update
    confirm_modal = False
    final_modal = False
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    event_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if not n_clicks_list or not any(n_clicks_list):
        raise PreventUpdate

    # Use a substring check instead of an exact string match.
    if "remove-button" in event_id:
        confirm_modal = True
        final_modal = False

    elif event_id == "confirm-modal-confirm" and confirm_btn:
        if confirmationmodal:
            output_list = []
            for n_clicks, button_id in zip(n_clicks_list, button_id_list):
                if n_clicks:
                    expensetype_id = button_id['index']
                    update_expense_sql = """
                        UPDATE adminteam.sub_expenses
                        SET sub_expense_del_ind = TRUE
                        WHERE sub_expense_id = %s
                    """
                    db.modifydatabase(update_expense_sql, [expensetype_id])
                    output_list.append(expensetype_list('/expense_list')[0])
                    final_modal = True
                    confirm_modal = False

    elif event_id == "confirm-modal-cancel" and cancel_btn:
        if confirmationmodal:
            confirm_modal = False

    return [output_list, confirm_modal, final_modal]

