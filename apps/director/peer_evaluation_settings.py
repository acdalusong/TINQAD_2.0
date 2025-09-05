import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, dash_table
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

# Define your highlight colors
highlight_colors = {
    'primary': "#0a4323",    # Main headers
    'secondary': "#7a0911",  # Section titles
    'accent': "#f8b237"      # Accent for borders/emphasis
}

# Card 1: CONTRIBUTIONS
card1 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("CONTRIBUTIONS", className="card-title"), width=10),
                    dbc.Col(
                        dbc.Button("Edit", size="sm", color="warning", id="edit_1"),
                        width=2,
                        style={"text-align": "right"}
                    )
                ],
                align="center"
            ),
            style={"background-color": highlight_colors['primary'], "color": "white"}
        ),
        dbc.CardBody(
            [
                dbc.InputGroup(
                    dbc.RadioItems(
                        options=[],
                        value=None,
                        inline=False,
                        id="radio_1"
                    ),
                    className="mb-3"
                ),
            ]
        )
    ],
    className="mb-4"
)

@app.callback(
    [
        Output('radio_1', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('refresh_store', 'data')
    ],
)

def rubrics_1_dropdown(pathname, refresh_data):
    if pathname == '/peer_evaluation_settings':
        sql = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 1
            ORDER BY rating_value
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        rubric_options = df.to_dict('records')

    else:
        raise PreventUpdate
    return [rubric_options]

# Card 2: COOPERATION WITH OTHERS
card2 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("COOPERATION WITH OTHERS", className="card-title"), width=10),
                    dbc.Col(
                        dbc.Button("Edit", size="sm", color="warning", id="edit_2"),
                        width=2,
                        style={"text-align": "right"}
                    )
                ],
                align="center"
            ),
            style={"background-color": highlight_colors['primary'], "color": "white"}
        ),
        dbc.CardBody(
            [
                dbc.InputGroup(
                    dbc.RadioItems(
                        options=[],
                        value=None,
                        inline=False,
                        id="radio_2"
                    ),
                    className="mb-3"
                ),
            ]
        )
    ],
    className="mb-4"
)

@app.callback(
    [
        Output('radio_2', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('refresh_store', 'data')
    ],
)

def rubrics_2_dropdown(pathname, refresh_data):
    if pathname == '/peer_evaluation_settings':
        sql = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 2
            ORDER BY rating_value
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        rubric_options = df.to_dict('records')

    else:
        raise PreventUpdate
    return [rubric_options]

# Card 3: FOCUS AND COMMITMENTS
card3 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("FOCUS AND COMMITMENTS", className="card-title"), width=10),
                    dbc.Col(
                        dbc.Button("Edit", size="sm", color="warning", id="edit_3"),
                        width=2,
                        style={"text-align": "right"}
                    )
                ],
                align="center"
            ),
            style={"background-color": highlight_colors['primary'], "color": "white"}
        ),
        dbc.CardBody(
            [
                dbc.InputGroup(
                    dbc.RadioItems(
                        options=[],
                        value=None,
                        inline=False,
                        id="radio_3"
                    ),
                    className="mb-3"
                ),
            ]
        )
    ],
    className="mb-4"
)

@app.callback(
    [
        Output('radio_3', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('refresh_store', 'data')
    ],
)

def rubrics_3_dropdown(pathname, refresh_data):
    if pathname == '/peer_evaluation_settings':
        sql = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 3
            ORDER BY rating_value
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        rubric_options = df.to_dict('records')

    else:
        raise PreventUpdate
    return [rubric_options]

# Card 4: TEAM ROLE FULFILLMENT
card4 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("TEAM ROLE FULFILLMENT", className="card-title"), width=10),
                    dbc.Col(
                        dbc.Button("Edit", size="sm", color="warning", id="edit_4"),
                        width=2,
                        style={"text-align": "right"}
                    )
                ],
                align="center"
            ),
            style={"background-color": highlight_colors['primary'], "color": "white"}
        ),
        dbc.CardBody(
            [
                dbc.InputGroup(
                    dbc.RadioItems(
                        options=[],
                        value=None,
                        inline=False,
                        id="radio_4"
                    ),
                    className="mb-3"
                ),
            ]
        )
    ],
    className="mb-4"
)

@app.callback(
    [
        Output('radio_4', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('refresh_store', 'data')
    ],
)

def rubrics_4_dropdown(pathname, refresh_data):
    if pathname == '/peer_evaluation_settings':
        sql = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 4
            ORDER BY rating_value
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        rubric_options = df.to_dict('records')

    else:
        raise PreventUpdate
    return [rubric_options]

# Card 5: ABILITY TO COMMUNICATE
card5 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("ABILITY TO COMMUNICATE", className="card-title"), width=10),
                    dbc.Col(
                        dbc.Button("Edit", size="sm", color="warning", id="edit_5"),
                        width=2,
                        style={"text-align": "right"}
                    )
                ],
                align="center"
            ),
            style={"background-color": highlight_colors['primary'], "color": "white"}
        ),
        dbc.CardBody(
            [
                dbc.InputGroup(
                    dbc.RadioItems(
                        options=[],
                        value=None,
                        inline=False,
                        id="radio_5"
                    ),
                    className="mb-3"
                ),
            ]
        )
    ],
    className="mb-4"
)

@app.callback(
    [
        Output('radio_5', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('refresh_store', 'data')
    ],
)

def rubrics_5_dropdown(pathname, refresh_data):
    if pathname == '/peer_evaluation_settings':
        sql = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 5
            ORDER BY rating_value
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        rubric_options = df.to_dict('records')

    else:
        raise PreventUpdate
    return [rubric_options]

# Card 6: COMPLETION OF ASSIGNED TASK
card6 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("COMPLETION OF ASSIGNED TASK", className="card-title"), width=10),
                    dbc.Col(
                        dbc.Button("Edit", size="sm", color="warning", id="edit_6"),
                        width=2,
                        style={"text-align": "right"}
                    )
                ],
                align="center"
            ),
            style={"background-color": highlight_colors['primary'], "color": "white"}
        ),
        dbc.CardBody(
            [
                dbc.InputGroup(
                    dbc.RadioItems(
                        options=[],
                        value=None,
                        inline=False,
                        id="radio_6"
                    ),
                    className="mb-3"
                ),
            ]
        )
    ],
    className="mb-4"
)

@app.callback(
    [
        Output('radio_6', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('refresh_store', 'data')
    ],
)

def rubrics_6_dropdown(pathname, refresh_data):
    if pathname == '/peer_evaluation_settings':
        sql = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 6
            ORDER BY rating_value
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        rubric_options = df.to_dict('records')

    else:
        raise PreventUpdate
    return [rubric_options]


# Card 7: COMPLETION OF ASSIGNED TASK
card7 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("OPEN PEER EVALUATION SUBMISSIONS", className="card-title"), width=8),
                    dbc.Col(
                        [
                            dbc.Switch(
                                id="allow_switch",
                                label="Allow Submissions",
                                value = True,
                                persistence = True,
                                persistence_type = 'local',
                            ),
                        ],
                        width=4,
                        className="d-grid gap-2 d-md-flex justify-content-md-end",
                    )
                ],
                align="center"
            ),
            style={"background-color": highlight_colors['secondary'], "color": "white"}
        ),
    ],
    className="mb-2"
)

@app.callback(
    [
        Output('submission_modal', 'is_open'),
        Output('submission_modal_message', 'children'),
        Output('allow_switch', 'value'),
    ],
    [
        Input('allow_switch', 'value'),
        Input('submission_modal_cancel', 'n_clicks'),
        Input('submission_modal_confirm', 'n_clicks')
    ],
    [State('allow_switch', 'value')],
    prevent_initial_call=True
)
def allow_form_submissions(toggle, cancel_btn, confirm_btn, current_switch):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    # When the switch is toggled, open the modal but do not override its value.
    if eventid == 'allow_switch':
        if toggle:
            modal = True
            message = "Do you really want to open form submissions?"
            final_toggle = dash.no_update
        else:
            modal = True
            message = "Do you really want to close form submissions?"
            final_toggle = dash.no_update
            
    # If the cancel button is clicked, revert the switch to its previous value.
    elif eventid == 'submission_modal_cancel' and cancel_btn:
        modal = False
        message = ""
        final_toggle = not current_switch

    # If the confirm button is clicked, commit the requested change.
    elif eventid == 'submission_modal_confirm' and confirm_btn:
        modal = False
        message = ""
        final_toggle = dash.no_update

    else:
        raise PreventUpdate
    return [modal, message, final_toggle]
    

@app.callback(
    [
        Output('main_decision', 'data'),
    ],
    [
        Input('allow_switch', 'value'),
    ],
)

def allow_form_submissions_b(toggle):
    if toggle == True:
        sqlcode = """
            UPDATE director.main_decision
            SET decision_bool = True
        """
        values = []
        db.modifydatabase(sqlcode, values)

        main_decision = 1
    elif toggle == False:
        sqlcode = """
            UPDATE director.main_decision
            SET decision_bool = False
        """
        values = []
        db.modifydatabase(sqlcode, values)

        main_decision = 0
    
    return [main_decision]

card8 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("CURRENT PEER EVALUATION PERIOD", className="card-title", style={"color": "white"}), width=8),
                    dbc.Col(
                        [
                            dbc.Select(
                                id='current_period',
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

@app.callback(
    [
        Output('current_period', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('refresh_store', 'data')
    ],
)

def populate_current_period(pathname, refresh_data):
    if pathname == '/peer_evaluation_settings':
        sql = """
            SELECT
			'From ' ||
                to_char(lower(period_details), 'Mon DD, YYYY') ||
                ' to ' ||
                to_char(upper(period_details) - INTERVAL '1 day', 'Mon DD, YYYY')
                AS label,
                period_id   AS value
            FROM director.evaluation_periods
            WHERE active_status = TRUE
            AND period_del_ind = FALSE
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        current_periods = df.to_dict('records')
        return [current_periods]
    
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('current_period', 'value'),
    ],
    [
        Input('url', 'pathname'),
        Input('refresh_store', 'data')
    ],
)

def populate_current_period(pathname, refresh_data):
    if pathname == '/peer_evaluation_settings':
        sql = """
            SELECT
			    period_id AS active_period
            FROM director.evaluation_periods
            WHERE active_status = TRUE
            AND 
            period_del_ind = FALSE
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



card9 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("SET PEER EVALUATION PERIOD", className="card-title", style={"color": "white"}), width=8),
                    dbc.Col(
                        [
                            dbc.Button("Update Evaluation Period", color="success", id="update_period_btn"),
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
                    dbc.Col(html.H5("MANAGE PEER EVALUATION PERIODS", className="card-title", style={"color": "white"}), width=6),
                    dbc.Col(
                        [
                            dbc.Button("Add an Evaluation Period", color="success", id="add_period_btn"),
                            dbc.Button("Remove an Evaluation Period", color="warning", href='/peer_evaluation_settings/remove_evaluation_periods'),
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





card11 = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(html.H5("PEER EVALUATION FORM PREVIEW", className="card-title"), width=8),
                    dbc.Col(
                        [
                            dbc.Button("View Form", color="success", id="preview_btn", href='/peer_evaluation_settings/peer_evaluation_forms?mode=view'),
                        ],
                        width=4,
                        className="d-grid gap-2 d-md-flex justify-content-md-end",
                    )
                ],
                align="center"
            ),
            style={"background-color": highlight_colors['secondary'], "color": "white"}
        ),
    ],
    className="mb-2"
)


# Define the overall layout in a container
layout = html.Div(
    [
        dcc.Store(id='main_decision', data=0, storage_type='local'),  # hidden store for main decision
        dcc.Store(id='refresh_store', data=0),  # hidden store for data refresh
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H2("QAO Peer Evaluation Settings", className="my-4", style={"color": highlight_colors['secondary']}),
                        html.Hr(),
                        # Accordion with "Form Content" and "Form Settings"
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    # Form Settings: cards 7-9
                                    [card7, card8, card9, card10, card11],
                                    title="Form Settings",
                                ),
                                dbc.AccordionItem(
                                    # Form Content: cards 1-6
                                    [card1, card2, card3, card4, card5, card6], 
                                    title="Form Content"
                                )
                            ],
                            start_collapsed=False,
                            always_open=True
                        ),
                        html.Br(),
                        html.Br(),
                        dbc.Alert(id='alert', is_open=False),  # For feedback purposes
                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3("Edit Rubric Option"), className="bg-primary", close_button=False),
                            dbc.ModalBody(
                                [
                                    dbc.Select(
                                        id="edit_rubric_option",
                                        placeholder= "Select a rubric option to edit",
                                        options=[],
                                    ),
                                    html.Br(),
                                    dbc.Textarea(
                                        id="edit_rubric_textarea",
                                        size="lg",
                                        className="mb-3",
                                        placeholder="Select a rubric and edit the text here",
                                    ),
                                ],
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button("Cancel", id="edit_button_modal_cancel", color="warning"),
                                    dbc.Button("Confirm", id="edit_button_modal_confirm", color="success")
                                ],
                                style={"display": "flex", "justifyContent": "space-between"}
                            ),
                        ],
                        id="edit_button_modal",
                        backdrop='static',
                        centered=True,
                        className="modal-success",
                        size="xl"
                    ),

                    # Final Modal for Peer Evaluation Settings
                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3(id="final_confirmation_modal_header"), close_button=True, className="bg-success", style={"color": "white"}),
                            dbc.ModalBody(
                                [
                                    html.H5(id="final_confirmation_modal_body"),
                                    html.Br(),
                                ],
                            ),
                        ],
                        centered=True,
                        id="final_confirmation_modal",
                        backdrop="True",
                        className="modal-success",
                    ),  

                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3("Please confirm your choice"), close_button=False, className="bg-primary"),
                            dbc.ModalBody(
                                [
                                    dbc.ModalBody(html.H5(id="submission_modal_message"))
                                ],
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button("No", id="submission_modal_cancel", color="warning"),
                                    dbc.Button("Yes", id="submission_modal_confirm", color="success")
                                ],
                                style={"display": "flex", "justifyContent": "space-between"}
                            ),
                        ],
                        id="submission_modal",
                        backdrop='static',
                        centered=True,
                        className="modal-success",
                    ), 
                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3("Please select the preferred evaluation period"), close_button=False, className="bg-primary"),
                            dbc.ModalBody(
                                [
                                    dcc.Dropdown(
                                        id="period",
                                        options=[],
                                        placeholder="Select a period",
                                        multi=False,
                                        clearable=True,
                                        style={"width": "100%"}
                                    ),
                                    html.Br(),
                                    html.H5("Please note that the selected period will be used for all peer evaluations"),
                                ],
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button("Close", id="period_modal_close", color="warning"),
                                    dbc.Button("Confirm", id="period_modal_confirm", color="success")
                                ],
                                style={"display": "flex", "justifyContent": "space-between"}
                            ),
                        ],
                        id="period_modal",
                        backdrop='static',
                        centered=True,
                        className="modal-success",
                    ),   
                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3("Please specify the dates fort the new evaluation period"), close_button=False, className="bg-primary"),
                            dbc.ModalBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.Label("Select Half-Year Period"),
                                                    dbc.Select(
                                                        id='period_half',
                                                        options=[
                                                            {'label': 'Period 1 (Jan 1 - Jun 30)', 'value': '1'},
                                                            {'label': 'Period 2 (Jul 1 - Dec 31)', 'value': '2'},
                                                        ],
                                                        placeholder="Choose 1 or 2",
                                                    ),
                                                ],
                                                md=6
                                            ),
                                            dbc.Col(
                                                [
                                                    html.Label("Enter Year"),
                                                    dbc.Input(
                                                        id='period_year',
                                                        type='number',
                                                        min=2000,  # adjust as needed
                                                        placeholder="e.g. 2025",
                                                    ),
                                                ],
                                                md=6
                                            ),
                                        ]
                                    ),
                                    html.Br(),
                                    html.H5("Please note that the selected period and year will be added to the list of evaluation periods"),
                                    dbc.Alert(
                                        id="add_period_modal_alert",
                                        color="danger",
                                        is_open=False,
                                    ),
                                ],
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button("Close", id="add_period_modal_close", color="warning"),
                                    dbc.Button("Confirm", id="add_period_modal_confirm", color="success")
                                ],
                                style={"display": "flex", "justifyContent": "space-between"}
                            ),
                        ],
                        id="add_period_modal",
                        backdrop='static',
                        centered=True,
                        className="modal-success",
                    ),   
                ],
                width=9, 
                style={'marginLeft': '15px'}
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ),
    ],
)

@app.callback(
    Output('period', 'options'),
    Input('url', 'pathname'),
    Input('refresh_store', 'data'),
)
def populate_evaluation_period(pathname, refresh_data):
    if pathname == '/peer_evaluation_settings':
        sql = """
            SELECT
			'From ' ||
                to_char(lower(period_details), 'Mon DD, YYYY') ||
                ' to ' ||
                to_char(upper(period_details) - INTERVAL '1 day', 'Mon DD, YYYY')
                AS label,
                period_id   AS value
            FROM director.evaluation_periods
            WHERE active_status = FALSE
            AND
            period_del_ind = FALSE
            ORDER BY period_id DESC;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        evaluation_periods = df.to_dict('records')
        return evaluation_periods
    
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('period_modal', 'is_open'),
    ],
    [
        Input('update_period_btn', 'n_clicks'),
        Input('period_modal_close', 'n_clicks'),
        Input('period_modal_confirm', 'n_clicks'),
    ],
)
def save_period_option(period_btn, close_btn, confirm_btn):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    period_modal_open = False

    if eventid == 'update_period_btn' and period_btn:
        period_modal_open = True

    elif eventid == 'period_modal_confirm' and confirm_btn:
        period_modal_open = False

    elif eventid == 'period_modal_close' and close_btn:
        period_modal_open = False
        
    else:
        raise PreventUpdate
    
    return [period_modal_open]
    
@app.callback(
    [
        Output('add_period_modal', 'is_open'),
        Output('add_period_modal_alert', 'is_open'),
        Output('add_period_modal_alert', 'children'),
    ],
    [
        Input('add_period_btn', 'n_clicks'),
        Input('add_period_modal_close', 'n_clicks'),
        Input('add_period_modal_confirm', 'n_clicks'),
    ],
    [
        State('period_half', 'value'),
        State('period_year', 'value'),
    ],
)
def save_add_period_option(period_btn, close_btn, confirm_btn, half, year):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    add_period_modal_open = False
    add_period_alert_open = False
    add_period_alert_message = ""

    if eventid == 'add_period_btn' and period_btn:
        add_period_modal_open = True

    elif eventid == 'add_period_modal_confirm' and confirm_btn:
        if half not in ('1','2') or not year:
            add_period_alert_open = True
            add_period_alert_message = "Please select a period (1 or 2) and enter a valid year."
            add_period_modal_open = True
        else:
            add_period_modal_open = False

    elif eventid == 'add_period_modal_close' and close_btn:
        add_period_modal_open = False
        
    else:
        raise PreventUpdate
    
    return [add_period_modal_open, add_period_alert_open, add_period_alert_message]
    

# displaying the choices for select button
@app.callback(
    [
        Output('edit_button_modal', 'is_open'),
        Output('edit_rubric_option', 'options'),
    ],
    [
        Input('edit_1', 'n_clicks'),
        Input('edit_2', 'n_clicks'),
        Input('edit_3', 'n_clicks'),
        Input('edit_4', 'n_clicks'),
        Input('edit_5', 'n_clicks'),
        Input('edit_6', 'n_clicks'),
        Input('edit_button_modal_cancel', 'n_clicks'),
        Input('edit_button_modal_confirm', 'n_clicks'),
    ],
)

def edit_record_options(edit_btn, edit_btn2, edit_btn3, edit_btn4, edit_btn5, edit_btn6,
                        cancel_btn, confirm_btn):
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    edit_modal = False
    modal_rubric_options = ''

    if eventid == 'edit_1' and edit_btn:
        edit_modal = True
        sql = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 1
            ORDER BY rating_value
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        modal_rubric_options = df.to_dict('records')
    
    elif eventid == 'edit_2' and edit_btn2:
        edit_modal = True
        sql_2 = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 2
            ORDER BY rating_value
        """
        values_2 = []
        cols_2 = ['label', 'value']
        df_2 = db.querydatafromdatabase(sql_2, values_2, cols_2)
        modal_rubric_options = df_2.to_dict('records')

    elif eventid == 'edit_3' and edit_btn3:
        edit_modal = True
        sql_3 = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 3
            ORDER BY rating_value
        """
        values_3 = []
        cols_3 = ['label', 'value']
        df_3 = db.querydatafromdatabase(sql_3, values_3, cols_3)
        modal_rubric_options = df_3.to_dict('records')

    elif eventid == 'edit_4' and edit_btn4:
        edit_modal = True
        sql_4 = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 4
            ORDER BY rating_value
        """
        values_4 = []
        cols_4 = ['label', 'value']
        df_4 = db.querydatafromdatabase(sql_4, values_4, cols_4)
        modal_rubric_options = df_4.to_dict('records')

    elif eventid == 'edit_5' and edit_btn5:
        edit_modal = True
        sql_5 = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 5
            ORDER BY rating_value
        """
        values_5 = []
        cols_5 = ['label', 'value']
        df_5 = db.querydatafromdatabase(sql_5, values_5, cols_5)
        modal_rubric_options = df_5.to_dict('records')

    elif eventid == 'edit_6' and edit_btn6:
        edit_modal = True
        sql_6 = """
            SELECT option_text as label, option_id as value
            FROM director.rubric_options 
            WHERE rubric_id = 6
            ORDER BY rating_value
        """
        values_6 = []
        cols_6 = ['label', 'value']
        df_6 = db.querydatafromdatabase(sql_6, values_6, cols_6)
        modal_rubric_options = df_6.to_dict('records')

    elif eventid == 'edit_button_modal_confirm' and confirm_btn:
        edit_modal = False

    elif eventid == 'edit_button_modal_cancel' and cancel_btn:
        edit_modal = False

    else:
        edit_modal = False
        modal_rubric_options= ''

    

    return [edit_modal, modal_rubric_options]


# displaying the choices for the text area
@app.callback(
    Output('edit_rubric_textarea', 'value'),
    Input('edit_rubric_option', 'value'),
)
def update_textarea_on_option_change(rubric_option_id):

    if rubric_option_id is None:
        # Return empty or a default value if nothing is selected
        return ""
    
    sql_b = """
        SELECT option_text
        FROM director.rubric_options
        WHERE option_id = %s
    """
    values_b = [rubric_option_id]
    dfcolumns_b = ['option_text']
    df_b = db.querydatafromdatabase(sql_b, values_b, dfcolumns_b)
            
    if not df_b.empty:
            return df_b.iloc[0]['option_text']
    else:
            return ""
    

@app.callback(
    [
        Output('final_confirmation_modal', 'is_open'),
        Output('final_confirmation_modal_header', 'children'),
        Output('final_confirmation_modal_body', 'children'),
        Output('refresh_store', 'data'),
    ],
    [
        Input('edit_button_modal_confirm', 'n_clicks'),
        Input('edit_rubric_textarea', 'value'),
        Input('edit_rubric_option', 'value'),
        Input('period_modal_confirm', 'n_clicks'),
        Input('add_period_modal_confirm', 'n_clicks'),
    ],
    [
        State('edit_button_modal', 'is_open'),
        State('period', 'value'),
        State('period_modal', 'is_open'),
        State('add_period_modal', 'is_open'),
        State('add_period_modal_alert', 'is_open'),
        State('period_half', 'value'),
        State('period_year', 'value'),
        State('refresh_store', 'data')
    ]
)
def save_record_options(edit_button_confirm, edit_rubric_textarea, rubric_option_id, period_button_confirm, add_button_confirm, editmodal, chosen_period, periodmodal, add_periodmodal,
                         add_periodmodal_alert, half, year, current_refresh):

    ctx = dash.callback_context 
    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    confirmation_modal = False
    confirmation_modal_header = ""
    confirmation_modal_body = ""
    new_refresh_value = current_refresh

    if editmodal:
        if eventid == 'edit_button_modal_confirm' and edit_button_confirm:
            try:
                # Ensure rubric_option_id is an integer
                rubric_option_id = int(rubric_option_id)
            except (TypeError, ValueError):
                raise PreventUpdate

            sqlcode = """
                UPDATE director.rubric_options
                SET option_text = %s
                WHERE option_id = %s
            """
            values = [edit_rubric_textarea, rubric_option_id]
            db.modifydatabase(sqlcode, values)

            # Update states: show confirmation modal, refresh store, and close the edit modal.
            confirmation_modal = True
            confirmation_modal_header = "Rubric Option Edited"
            confirmation_modal_body = "The rubric option has been successfully edited."
            new_refresh_value = current_refresh + 1

    elif periodmodal:
        if eventid == 'period_modal_confirm' and period_button_confirm:
            try:
                # Ensure rubric_option_id is an integer
                chosen_period_final = int(chosen_period)
            except (TypeError, ValueError):
                raise PreventUpdate

            sqlcode = """
                UPDATE director.evaluation_periods
                SET active_status = CASE
                    WHEN period_id = %s THEN TRUE
                    ELSE FALSE
                END;
            """

            values = [chosen_period_final]
            db.modifydatabase(sqlcode, values)
            
            confirmation_modal = True
            confirmation_modal_header = "Evaluation Period Updated"
            confirmation_modal_body = "The evaluation period has been successfully updated."
            new_refresh_value = current_refresh + 1
    
    elif add_periodmodal and eventid == 'add_period_modal_confirm' and add_button_confirm:
        # 1) Ensure both dates present
        if half not in ('1','2') or not year:
            raise PreventUpdate
        else:
            # Build start/end based on half-year
            if half == '1':
                start = f"{year}-01-01"
                end   = f"{year}-06-30"
            else:
                start = f"{year}-07-01"
                end   = f"{year}-12-31"

            # PostgreSQL daterange literal: '[YYYY-MM-DD,YYYY-MM-DD]'
            daterange = f'[{start},{end}]'

            # Insert into DB
            sqlcode = """
                INSERT INTO director.evaluation_periods (
                    period_details,
                    active_status,
                    period_del_ind
                ) VALUES (%s, FALSE, FALSE);
            """
            values = [daterange]
            db.modifydatabase(sqlcode, values)
            # Show confirmation and bump refresh
            confirmation_modal = True
            confirmation_modal_header = "Evaluation Period Added"
            confirmation_modal_body = "The new evaluation period has been successfully added."
            new_refresh_value = current_refresh + 1

    return [confirmation_modal, confirmation_modal_header, confirmation_modal_body, new_refresh_value]
