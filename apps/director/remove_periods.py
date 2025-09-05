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
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H1("List of Evaluation Periods"),
                                    width=8,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Back",
                                        color="success",
                                        href="/peer_evaluation_settings"
                                    ),
                                    width=4,
                                    style={"display": "flex", "justifyContent": "flex-end"}
                                ),
                            ],
                            align="center"
                        ),
                        html.Hr(),
                        html.Div(
                            id='evaluationperiod_list', 
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
                                dbc.ModalBody(html.H5("Are you sure you want to remove this evaluation period?")),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="remove_confirm_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id="remove_confirm_modal_confirm", color="danger"),
                                    ]
                                ),
                            ],
                            id="remove_confirm_modal",
                            centered=True,
                            is_open=False,
                            backdrop=True
                        ),
                        # Final Modal: notifies the user that the removal is complete
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Removed Successfully"), className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Evaluation Period has been successfully removed."))
                            ],
                            id="remove_final_modal",
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
    Output('evaluationperiod_list', 'children'),
    [Input('url', 'pathname')]
)
def evaluationperiod_list(pathname):
    if pathname == '/peer_evaluation_settings/remove_evaluation_periods':
        sql = """
            SELECT
                period_id AS "ID",
                'From ' ||
                to_char(lower(period_details), 'MM-DD-YYYY') ||
                ' to ' ||
                to_char(upper(period_details) - INTERVAL '1 day', 'MM-DD-YYYY') AS "Evaluation Period"
            FROM director.evaluation_periods
            WHERE period_del_ind = FALSE
            ORDER BY period_id DESC;
        """
        cols = ["ID", "Evaluation Period"]

        # Execute the query and fetch the data
        df = db.querydatafromdatabase(sql, [], cols)

        if df.shape[0] > 0:
            # Add an Action column with a removal button for each row.
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button(
                        'Remove',
                        id={'type': 'remove_button', 'index': x},
                        size='sm',
                        color='danger'
                    ),
                    style={'text-align': 'center'}
                )
            )

            # Select only the columns to display
            df = df[["Evaluation Period", "Action"]]

            # 1) Build a header row, centering the 'Action' Th
            table_header = html.Thead(
                html.Tr([
                    html.Th(col, className="text-center" if col == "Action" else "")
                    for col in df.columns
                ])
            )

            # 2) Build table body rows, centering the action cells
            table_rows = []
            for _, row in df.iterrows():
                table_rows.append(html.Tr([
                    html.Td(row["Evaluation Period"]),
                    html.Td(row["Action"], className="text-center")
                ]))
            table_body = html.Tbody(table_rows)

            # 3) Return the styled table
            return [
                dbc.Table(
                    [table_header, table_body],
                    bordered=True,
                    hover=True,
                    responsive=True,
                    className="table-sm"
                )
            ]
        else:
            return [html.Div("No evaluation periods listed")]
    else:
        raise PreventUpdate

# Callback to process confirmation modals
@app.callback(
    [
        Output('evaluationperiod_list', 'children', allow_duplicate=True),
        Output("remove_confirm_modal", "is_open"),
        Output("remove_final_modal", "is_open")
    ],
    [
        Input({'type': 'remove_button', 'index': dash.dependencies.ALL}, 'n_clicks'),
        Input("remove_confirm_modal_confirm", "n_clicks"),
        Input("remove_confirm_modal_cancel", "n_clicks"),
    ],
    [
        State({'type': 'remove_button', 'index': dash.dependencies.ALL}, 'id'),
        State("remove_confirm_modal", "is_open"),
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
    if "remove_button" in event_id:
        confirm_modal = True
        final_modal = False

    elif event_id == "remove_confirm_modal_confirm" and confirm_btn:
        if confirmationmodal:
            output_list = []
            for n_clicks, button_id in zip(n_clicks_list, button_id_list):
                if n_clicks:
                    period_id = button_id['index']
                    update_evaluation_period_sql = """
                        UPDATE director.evaluation_periods
                        SET period_del_ind = TRUE
                        WHERE period_id = %s
                    """
                    db.modifydatabase(update_evaluation_period_sql, [period_id])
                    output_list.append(evaluationperiod_list('/peer_evaluation_settings/remove_evaluation_periods')[0])
                    final_modal = True
                    confirm_modal = False

    elif event_id == "remove_confirm_modal_cancel" and cancel_btn:
        if confirmationmodal:
            confirm_modal = False

    return [output_list, confirm_modal, final_modal]

