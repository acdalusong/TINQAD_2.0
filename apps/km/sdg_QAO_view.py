import json
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
from dash import ALL
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import dash
from dash.exceptions import PreventUpdate

import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# Ensure upload directory exists
UPLOAD_DIRECTORY = r".\assets\database\km\sdg"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Define your highlight colors
highlight_colors = {
    'primary': "#0a4323",    # Main headers
    'secondary': "#7a0911",  # Section titles
    'accent': "#f8b237"      # Accent for borders/emphasis
}

# 1. SDG colors map
sdg_colors = {
    1: "#e5233d", 2: "#dda73a", 3: "#4ca146", 4: "#c7212f",
    5: "#ef402d", 6: "#27bfe6", 7: "#fbc412", 8: "#a31c44",
    9: "#f26a2e", 10: "#e01483", 11: "#f89d2a", 12: "#bf8d2c",
    13: "#407f46", 14: "#1f97d4", 15: "#59ba47", 16: "#136a9f",
    17: "#14496b",
}

# 2. Generate SDG buttons with working hrefs
sdg_buttons = []
for i in range(1, 18):
    sdg_buttons.append(
        dbc.Col(
            dbc.Button(
                f"SDG {i}",
                href=f"/SDG_evidencelist/sdg{i}",    # <-- proper f‑string here
                external_link=True,                  # treat as actual link
                style={
                    "backgroundColor": sdg_colors[i],
                    "color": "white",
                    "width": "100%",
                    "height": "80px",             # smaller height
                    "fontSize": "1.25rem",        # larger text
                    # borderRadius removed
                    "marginBottom": "1rem",
                },
                className="d-flex justify-content-center align-items-center",
            ),
            width=2,  # controls how many per row (12/2 = 6 per row)
        )
    )

card8 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("CURRENT RECKONING PERIOD", className="card-title", style={"color": "white"}), width=8),
                    dbc.Col(
                        [
                            dbc.Select(
                                id='reckoning_current_period',
                                placeholder="No period selected",
                                disabled = True,
                                options=[],
                            ),
                        ],
                        width=3,
                        className="d-grid gap-2 d-md-flex justify-content-md-end",
                    )
                ],
                align="center",
                justify="between"
            ),
            style={"background-color": highlight_colors['secondary']}
        ),
    ],
    className="mb-2"
)

card9 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("SET RECKONING PERIOD FOR SDG SUBMISSIONS", className="card-title", style={"color": "white"}), width=8),
                    dbc.Col(
                        [
                            dbc.Button("Update Reckoning Period", color="success", id="update_reckoning_period_btn"),
                        ],
                        width=3,
                        className="d-grid gap-2 d-md-flex justify-content-md-end",
                    )
                ],
                align="center",
                justify="between"
            ),
            style={"background-color": highlight_colors['secondary']}
        ),
    ],
    className="mb-2"
)

card10 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("MANAGE RECKONING PERIODS", className="card-title", style={"color": "white"}), width=6),
                    dbc.Col(
                        [
                            dbc.Button("Add a Reckoning Period", color="success", id="add_reckoning_period_btn"),
                            dbc.Button("Remove a Reckoning Period", color="warning", id="remove_reckoning_period_btn"),
                        ],
                        className="d-flex gap-2 justify-content-end ms-auto",
                    )
                ],
                align="center",
            ),
            style={"background-color": highlight_colors['secondary']}
        ),
    ],
    className="mb-2"
)

layout = html.Div(
    [
        dcc.Store(id='reckoning_refresh_store', data=0),  # hidden store for data refresh
        dcc.Store(id='reckoning_refresh_store_2', data=0),  # hidden store for data refresh
        dcc.Store(id='remove_candidate', data=None),
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        # Header
                        dbc.Row(
                            dbc.Col(html.H1("SDG EVIDENCES SUBMISSION"),
                                    style={"marginBottom": "-10px"}),
                        ),
                        html.Hr(),
                        # The Card with the Settings
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [card8, card9, card10],
                                    title="Form Settings",
                                ),
                            ],
                            start_collapsed=False,
                            always_open=True
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H5("Click a particular SDG to view its evidence submissions."),
                                    style={"backgroundColor": "#f8f9fa"},
                                ),
                                dbc.CardBody(
                                    dbc.Row(sdg_buttons, justify="start", align="stretch")
                                ),
                            ],
                            className="mb-4",
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please specify the dates for the new reckoning period"), close_button=False, className="bg-primary"),
                                dbc.ModalBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Label("Select Beginning Period"),
                                                        dcc.DatePickerSingle(
                                                            id='beginning_period',
                                                            placeholder="mm/dd/yyyy",
                                                            className='SingleDatePicker mb-2',
                                                            style={"width": "100%"},
                                                        ),
                                                    ],
                                                    md=6
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Label("Select Ending Period"),
                                                        dcc.DatePickerSingle(
                                                            id='ending_period',
                                                            placeholder="mm/dd/yyyy",
                                                            className='SingleDatePicker mb-2',
                                                            style={"width": "100%"},
                                                        )
                                                    ],
                                                    md=6
                                                ),
                                            ]
                                        ),
                                        html.Br(),
                                        html.H5("Please note that the selected dates will be added to the list of reckoning periods"),
                                        dbc.Alert(
                                            id="add_reckoning_period_modal_alert",
                                            color="danger",
                                            is_open=False,
                                        ),
                                    ],
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Close", id="add_reckoning_period_modal_close", color="warning"),
                                        dbc.Button("Confirm", id="add_reckoning_period_modal_confirm", color="success")
                                    ],
                                    style={"display": "flex", "justifyContent": "space-between"}
                                ),
                            ],
                            id="add_reckoning_period_modal",
                            backdrop='static',
                            centered=True,
                            className="modal-success",
                        ),
                        # Final Modal for Reckoning Period Settings
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id="reckoning_period_final_modal_header"), close_button=True, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(
                                    [
                                        html.H5(id="reckoning_period_final_modal_body"),
                                        html.Br(),
                                    ],
                                ),
                            ],
                            centered=True,
                            id="reckoning_period_final_modal",
                            backdrop="True",
                            className="modal-success",
                        ),
                    ],
                    width=9,
                    style={"marginLeft": "15px"},
                ),
                dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3("Please select the preferred reckoning period"), close_button=False, className="bg-primary"),
                            dbc.ModalBody(
                                [
                                    dcc.Dropdown(
                                        id="reckoning_period",
                                        options=[],
                                        placeholder="Select a reckoning period",
                                        multi=False,
                                        clearable=True,
                                        style={"width": "100%"}
                                    ),
                                    html.Br(),
                                    html.H5("Please note that the selected period will be used for all SDG Evidence Submissions"),
                                ],
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button("Close", id="reckoning_period_modal_close", color="warning"),
                                    dbc.Button("Confirm", id="reckoning_period_modal_confirm", color="success")
                                ],
                                style={"display": "flex", "justifyContent": "space-between"}
                            ),
                        ],
                        id="reckoning_period_modal",
                        backdrop='static',
                        centered=True,
                        className="modal-success",
                    ),   
                dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please select which reckoning period to delete"), close_button=False, className="bg-primary"),
                                dbc.ModalBody(
                                    [
                                        html.Div(
                                            id='reckoningperiod_list', 
                                            style={
                                                'marginTop': '20px',
                                                'overflowX': 'auto', 
                                                'overflowY': 'auto',   
                                                'maxHeight': '800px',
                                            }
                                        ),
                                        html.Br(),
                                        html.H5("Please note that the selected period will be removed from the list"),
                                    ],
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="remove_reckoning_period_modal_cancel", color="warning"),
                                    ]
                                ),
                            ],
                            id="remove_reckoning_period_modal",
                            is_open=False,  
                            backdrop=True,
                            centered=True,
                            className="modal-success",
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Confirm Choice of Removal"), className="bg-primary"),
                                dbc.ModalBody(html.H5("Are you sure you want to remove this reckoning period?")),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="remove_confirm_modal_2_cancel", color="warning"),
                                        dbc.Button("Confirm", id="remove_confirm_modal_2_confirm", color="danger"),
                                    ]
                                ),
                            ],
                            id="remove_confirm_modal_2",
                            centered=True,
                            is_open=False,
                            backdrop=True
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Removed Successfully"), className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Reckoning Period has been successfully removed."))
                            ],
                            id="remove_final_modal_2",
                            centered=True,
                            is_open=False,
                            backdrop=True,
                        ),
            ]
        ),
        dbc.Row(
            dbc.Col(cm.generate_footer(), width=12)
        ),
    ]
)

@app.callback(
    [
        Output('reckoning_current_period', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('reckoning_refresh_store', 'data'),
        Input('reckoning_refresh_store_2', 'data')
    ],
)

def populate_reckoning_current_period(pathname, refresh_data, refresh_data_2):
    if pathname == '/SDG_evidencelist':
        sql = """
            SELECT
			'From ' ||
                to_char(lower(reckoning_period_details), 'Mon DD, YYYY') ||
                ' to ' ||
                to_char(upper(reckoning_period_details) - INTERVAL '1 day', 'Mon DD, YYYY')
                AS label,
                reckoning_period_id   AS value
            FROM kmteam.reckoning_periods
            WHERE active_status = TRUE
            AND reckoning_period_del_ind = FALSE
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        reckoning_current_periods = df.to_dict('records')
        return [reckoning_current_periods]
    
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('reckoning_current_period', 'value'),
    ],
    [
        Input('url', 'pathname'),
        Input('reckoning_refresh_store', 'data'),
        Input('reckoning_refresh_store_2', 'data')
    ],
)

def populate_reckoning_current_period(pathname, refresh_data, refresh_data_2):
    if pathname == '/SDG_evidencelist':
        sql = """
            SELECT
			    reckoning_period_id AS active_period
            FROM kmteam.reckoning_periods
            WHERE active_status = TRUE
            AND 
            reckoning_period_del_ind = FALSE
        """
        values = []
        cols = ['active_period']
        df = db.querydatafromdatabase(sql, values, cols)

        if df.empty:
            return [None]
        
        active_period = df['active_period'][0]
        return [active_period]
    
    else:
        raise PreventUpdate


@app.callback(
    Output('reckoningperiod_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('reckoning_refresh_store', 'data'),
        Input('reckoning_refresh_store_2', 'data')
    ],
    
)
def reckoningperiod_list(pathname, refresh_data, refresh_data_2):
    if pathname == '/SDG_evidencelist':
        sql = """
            SELECT
                reckoning_period_id AS "ID",
                'From ' ||
                to_char(lower(reckoning_period_details), 'MM-DD-YYYY') ||
                ' to ' ||
                to_char(upper(reckoning_period_details) - INTERVAL '1 day', 'MM-DD-YYYY') AS "Reckoning Period"
            FROM kmteam.reckoning_periods
            WHERE reckoning_period_del_ind = FALSE
            ORDER BY reckoning_period_id DESC;
        """
        cols = ["ID", "Reckoning Period"]

        # Execute the query and fetch the data
        df = db.querydatafromdatabase(sql, [], cols)

        if df.shape[0] > 0:
            # Add an Action column with a removal button for each row.
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button(
                        'Remove',
                        id={'type': 'remove_button_2', 'index': x},
                        size='sm',
                        color='danger'
                    ),
                    style={'text-align': 'center'}
                )
            )

            # Select only the columns to display
            df = df[["Reckoning Period", "Action"]]

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
                    html.Td(row["Reckoning Period"]),
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
            return [html.Div("No reckoning periods listed")]
    else:
        raise PreventUpdate

@app.callback(
    Output('reckoning_period', 'options'),
    Input('url', 'pathname'),
    Input('reckoning_refresh_store', 'data'),
    Input('reckoning_refresh_store_2', 'data'),
)
def populate_reckoning_period(pathname, refresh_data, refresh_data_2):
    if pathname == '/SDG_evidencelist':
        sql = """
            SELECT
			'From ' ||
                to_char(lower(reckoning_period_details), 'Mon DD, YYYY') ||
                ' to ' ||
                to_char(upper(reckoning_period_details) - INTERVAL '1 day', 'Mon DD, YYYY')
                AS label,
                reckoning_period_id   AS value
            FROM kmteam.reckoning_periods
            WHERE active_status = FALSE
            AND
            reckoning_period_del_ind = FALSE
            ORDER BY reckoning_period_id DESC;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        reckoning_periods = df.to_dict('records')
        return reckoning_periods
    
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('add_reckoning_period_modal', 'is_open'),
        Output('add_reckoning_period_modal_alert', 'is_open'),
        Output('add_reckoning_period_modal_alert', 'children'),
    ],
    [
        Input('add_reckoning_period_btn', 'n_clicks'),
        Input('add_reckoning_period_modal_close', 'n_clicks'),
        Input('add_reckoning_period_modal_confirm', 'n_clicks'),
    ],
    [
        State('beginning_period', 'date'),
        State('ending_period', 'date'),
    ],
)
def save_add_period_option(period_btn, close_btn, confirm_btn, beginning, ending):
    ctx = dash.callback_context
    if not ctx.triggered:
        # no event yet
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    is_open = False
    alert_open = False
    alert_msg = ""

    if eventid == 'add_reckoning_period_btn' and period_btn:
        # Open the modal on initial “Add” click
        is_open = True

    elif eventid == 'add_reckoning_period_modal_close' and close_btn:
        # Close modal on “Close”
        is_open = False

    elif eventid == 'add_reckoning_period_modal_confirm' and confirm_btn:
        # Attempt to confirm — validate inputs
        # 1) both dates must be provided
        if not beginning or not ending:
            alert_open = True
            alert_msg = "Please select both a start and end date."
            is_open = True

        else:
            # parse ISO strings into date objects
            fmt = "%Y-%m-%d"
            try:
                start_dt = datetime.strptime(beginning, fmt).date()
                end_dt   = datetime.strptime(ending, fmt).date()
            except ValueError:
                alert_open = True
                alert_msg = "Invalid date format."
                is_open = True
            else:
                # 2) end must be on or after start
                if end_dt < start_dt:
                    alert_open = True
                    alert_msg = "End date cannot be earlier than start date."
                    is_open = True
                else:
                    # VALID: proceed (e.g. write to DB or update store)
                    is_open = False
                    alert_open = False
                    alert_msg = ""
    else:
        # any other event — do nothing
        raise PreventUpdate

    return is_open, alert_open, alert_msg


@app.callback(
    [
        Output('reckoning_period_modal', 'is_open'),
    ],
    [
        Input('update_reckoning_period_btn', 'n_clicks'),
        Input('reckoning_period_modal_close', 'n_clicks'),
        Input('reckoning_period_modal_confirm', 'n_clicks'),
    ],
)
def save_period_option(reckoning_period_btn, close_btn, confirm_btn):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    period_modal_open = False

    if eventid == 'update_reckoning_period_btn' and reckoning_period_btn:
        period_modal_open = True

    elif eventid == 'reckoning_period_modal_confirm' and confirm_btn:
        period_modal_open = False

    elif eventid == 'reckoning_period_modal_close' and close_btn:
        period_modal_open = False
        
    else:
        raise PreventUpdate
    
    return [period_modal_open]


@app.callback(
    [
        Output('reckoning_period_final_modal', 'is_open'),
        Output('reckoning_period_final_modal_header', 'children'),
        Output('reckoning_period_final_modal_body', 'children'),
        Output('reckoning_refresh_store', 'data'),
    ],
    [
        Input('reckoning_period_modal_confirm', 'n_clicks'),
        Input('add_reckoning_period_modal_confirm', 'n_clicks'),
    ],
    [
        State('reckoning_period', 'value'),
        State('reckoning_period_modal', 'is_open'),
        State('add_reckoning_period_modal', 'is_open'),
        State('add_reckoning_period_modal_alert', 'is_open'),
        State('beginning_period', 'date'),
        State('ending_period', 'date'),
        State('reckoning_refresh_store', 'data')
    ],
)
def save_record_options(reckoning_period_button_confirm, add_button_confirm, chosen_reckoning_period, periodmodal, add_periodmodal,
                         add_reckoning_period_modal_alert, beginning, ending, current_refresh):

    ctx = dash.callback_context 
    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    confirmation_modal = False
    confirmation_modal_header = ""
    confirmation_modal_body = ""
    new_refresh_value = current_refresh

    if periodmodal:
        if eventid == 'reckoning_period_modal_confirm' and reckoning_period_button_confirm:
            try:
                chosen_reckoning_period_final = int(chosen_reckoning_period)
            except (TypeError, ValueError):
                raise PreventUpdate

            sqlcode = """
                UPDATE kmteam.reckoning_periods
                SET active_status = CASE
                    WHEN reckoning_period_id = %s THEN TRUE
                    ELSE FALSE
                END;
            """

            values = [chosen_reckoning_period_final]
            db.modifydatabase(sqlcode, values)
            
            confirmation_modal = True
            confirmation_modal_header = "Reckoning Period Updated"
            confirmation_modal_body = "The reckoning period has been successfully updated."
            new_refresh_value = current_refresh + 1
    
    elif add_periodmodal and eventid == 'add_reckoning_period_modal_confirm' and add_button_confirm:
        # 1) both dates must be provided
        if beginning is None or ending is None:
            raise PreventUpdate

        # 2) parse and check order
        try:
            start_dt = datetime.strptime(beginning, "%Y-%m-%d").date()
            end_dt   = datetime.strptime(ending,   "%Y-%m-%d").date()
        except ValueError:
            # bad date format → do nothing
            raise PreventUpdate

        if end_dt < start_dt:
            # end before start → do nothing
            raise PreventUpdate

        # 3) at this point both dates are valid and in the right order → proceed to insert
        sqlcode = """
            INSERT INTO kmteam.reckoning_periods (
                reckoning_period_details,
                active_status,
                reckoning_period_del_ind
            ) 
            VALUES (
                daterange(%s, %s, '[]'), 
                FALSE, 
                FALSE
            );
        """
        values = [beginning, ending]
        db.modifydatabase(sqlcode, values)
        # Show confirmation and bump refresh
        confirmation_modal = True
        confirmation_modal_header = "Reckoning Period Added"
        confirmation_modal_body = "The new reckoning period has been successfully added."
        new_refresh_value = current_refresh + 1

    return [confirmation_modal, confirmation_modal_header, confirmation_modal_body, new_refresh_value]

# 1) New callback: whenever ANY remove_button_2 is clicked, stash its index in remove_candidate
@app.callback(
    Output('remove_candidate', 'data'),
    Input({'type': 'remove_button_2', 'index': ALL}, 'n_clicks'),
    State({'type': 'remove_button_2', 'index': ALL}, 'id'),
    prevent_initial_call=True
)
def capture_remove_candidate(n_clicks_list, btn_id_list):
    for n, btn in zip(n_clicks_list, btn_id_list):
        if n:
            # store the exact period_id to delete
            return btn['index']
    # fallback
    return dash.no_update

# 2) Your existing remove_period_option now only handles modals + final SQL
@app.callback(
    [
        Output("remove_reckoning_period_modal", "is_open"),
        Output("remove_confirm_modal_2",     "is_open"),
    ],
    [
        Input('remove_reckoning_period_btn', 'n_clicks'),
        Input('remove_reckoning_period_modal_cancel', 'n_clicks'),
        Input({'type': 'remove_button_2', 'index': ALL},  'n_clicks'),
        Input("remove_confirm_modal_2_confirm", 'n_clicks'),
        Input("remove_confirm_modal_2_cancel",'n_clicks'),
    ],
    State('url','pathname'),
    prevent_initial_call=True
)
def remove_period_option(remove_btn,
                         cancel_select,
                         any_remove_clicks,
                         confirm_delete,
                         cancel_confirm,
                         pathname):
    if pathname != '/SDG_evidencelist':
        raise PreventUpdate

    ctx = dash.callback_context
    trg = ctx.triggered[0]['prop_id'].split('.')[0]

    # defaults
    open_select = False
    open_confirm = False

    if trg == 'remove_reckoning_period_btn' and remove_btn:
        open_select = True
    elif trg == 'remove_reckoning_period_modal_cancel' and cancel_select:
        open_select = False
    elif 'remove_button_2' in trg and any(any_remove_clicks):
        # user clicked exactly one of the row‑level “Remove” buttons
        open_confirm = True
    elif trg == 'remove_confirm_modal_2_confirm' and confirm_delete:
        # **we do not run SQL here!** we’ll handle it in the next callback
        open_confirm = False
    elif trg == 'remove_confirm_modal_2_cancel' and cancel_confirm:
        open_confirm = False

    return open_select, open_confirm

# 3) New callback: when they click **Confirm** on the “Are you sure?” modal,
#    pull the saved period_id from remove_candidate and do the UPDATE.
@app.callback(
    Output('reckoning_refresh_store_2', 'data'),
    Output("remove_final_modal_2",       "is_open"),
    Input('remove_confirm_modal_2_confirm', 'n_clicks'),
    State('remove_candidate', 'data'),
    State('reckoning_refresh_store_2', 'data'),
    prevent_initial_call=True
)
def actually_delete_period(confirm_clicks, period_to_delete, current_refresh):
    if not confirm_clicks or period_to_delete is None:
        raise PreventUpdate

    sql = """
        UPDATE kmteam.reckoning_periods
        SET reckoning_period_del_ind = TRUE
        WHERE reckoning_period_id = %s
    """
    db.modifydatabase(sql, [period_to_delete])

    # bump your refresh counter so all dependent callbacks re‑run
    return [True, current_refresh + 1]