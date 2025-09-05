import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, dash_table
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import base64
import os
from urllib.parse import urlparse, parse_qs
import flask

# Define the highlight colors for styling
highlight_colors = {
    'primary': "#0a4323",    # Main headers
    'secondary': "#7a0911",  # Section titles
    'accent': "#f8b237"      # Accent for borders/emphasis
}

# Define the layout for the Peer Evaluation Form
peer_evaluation_form = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1("QAO Peer Evaluation Form", 
                    style={'color': highlight_colors['primary'], 'textAlign': 'center', 'marginTop': '20px'}),
            width=12
        )
    ),
    dbc.Row(
        dbc.Col(
            html.P(
                "Peer Evaluation gives feedback on each other's work, another group's work, or, if working in a group, "
                "other group-members' contribution to a project. It is part of an employee's development process. This peer "
                "review instrument will evaluate 6 attributes related to performance, skills or competencies, and attitude. "
                "Your review of your co-employees will be kept anonymous and will be used by the QAO Director to give feedback on "
                "their current performance and offer solutions for improvement.",
                style={'textAlign': 'center', 'marginBottom': '30px', 'padding': '0 20px'}
            ),
            width=12
        )
    ),
    html.Hr(),
    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                id="team_member_dropdown",
                options=[],  # Populate with team member options as needed
                placeholder="Select Team Member",
                style={'width': '100%'}
            ),
            width=12,
            style={'marginBottom': '20px'}
        )
    ),
    dbc.Row(
        dbc.Col(
            html.H2("PEER EVALUATION RUBRICS", 
                    style={'color': highlight_colors['secondary'], 'textAlign': 'center', 'marginBottom': '40px'}),
            width=12
        )
    ),
    
    # Section 1: Contributions
    dbc.Card(
        [
            dbc.CardHeader(
                [
                    dbc.Col(
                        html.H5("CONTRIBUTIONS", 
                                className="card-title",
                                style={'color': highlight_colors['secondary']}), 
                    )
                ],
                style={"background-color": highlight_colors['accent']}
            ),
            dbc.CardBody(
                [
                    html.Div(
                        dbc.RadioItems(
                            options=[],
                            id="contributions_radio",
                            inline=False,
                            labelStyle={'margin-bottom': '2px'}
                        ),
                        id="contributions_radio_container"  # new container ID
                    ),
                    html.Br(),
                    html.Div([
                        dbc.Label("Anecdotes/Remarks/Opportunities for Improvement:"),
                        dbc.Textarea(id="contributions_remarks", placeholder="Enter your remarks here...")
                    ], className="mb-3")
                ]
            ),
        ],
        className="mb-4",
    ),
    
    # Section 2: Cooperation With Others
    dbc.Card(
        [
            dbc.CardHeader(
                [
                    dbc.Col(
                        html.H5("COOPERATION WITH OTHERS", 
                                className="card-title",
                                style={'color': highlight_colors['secondary']}), 
                    )
                ],
                style={"background-color": highlight_colors['accent']}
            ),
            dbc.CardBody(
                [
                    html.Div(
                            dbc.RadioItems(
                                options=[],
                                id="cooperation_radio",
                                inline=False,
                                labelStyle={'margin-bottom': '2px'}
                            ),
                            id="cooperation_radio_container"  # new container ID
                    ),
                    html.Br(),
                    html.Div([
                        dbc.Label("Anecdotes/Remarks/Opportunities for Improvement:"),
                        dbc.Textarea(id="cooperation_remarks", placeholder="Enter your remarks here...")
                    ], className="mb-3")
                ]
            ),
        ],
        className="mb-4"
    ),
    
    # Section 3: Focus and Commitments
    dbc.Card(
        [
            dbc.CardHeader(
                [
                    dbc.Col(
                        html.H5("FOCUS AND COMMITMENTS", 
                                className="card-title",
                                style={'color': highlight_colors['secondary']}), 
                    )
                ],
                style={"background-color": highlight_colors['accent']}
            ),
            dbc.CardBody(
                [
                    html.Div(
                        dbc.RadioItems(
                            options=[],
                            id="focus_radio",
                            inline=False,
                            labelStyle={'margin-bottom': '2px'}
                        ),
                        id="focus_radio_container"  # new container ID
                    ),
                    html.Br(),
                    html.Div([
                        dbc.Label("Anecdotes/Remarks/Opportunities for Improvement:"),
                        dbc.Textarea(id="focus_remarks", placeholder="Enter your remarks here...")
                    ], className="mb-3")
                ]
            ),
        ],
        className="mb-4"
    ),
    
    # Section 4: Team Role Fulfillment
    dbc.Card(
        [
            dbc.CardHeader(
                [
                    dbc.Col(
                        html.H5("TEAM ROLE FULFILLMENT", 
                                className="card-title",
                                style={'color': highlight_colors['secondary']}), 
                    )
                ],
                style={"background-color": highlight_colors['accent']}
            ),
            dbc.CardBody(
                [
                    html.Div(
                        dbc.RadioItems(
                            options=[],
                            id="teamrole_radio",
                            inline=False,
                            labelStyle={'margin-bottom': '2px'}
                        ),
                        id="teamrole_radio_container"  # new container ID
                    ),
                    html.Br(),
                    html.Div([
                        dbc.Label("Anecdotes/Remarks/Opportunities for Improvement:"),
                        dbc.Textarea(id="teamrole_remarks", placeholder="Enter your remarks here...")
                    ], className="mb-3")
                ]
            ),
        ],
        className="mb-4"
    ),
    
    # Section 5: Ability to Communicate
    dbc.Card(
        [
            dbc.CardHeader(
                [
                    dbc.Col(
                        html.H5("ABILITY TO COMMUNICATE", 
                                className="card-title",
                                style={'color': highlight_colors['secondary']}), 
                    )
                ],
                style={"background-color": highlight_colors['accent']}
            ),
            dbc.CardBody(
                [
                    html.Div(
                        dbc.RadioItems(
                            options=[],
                            id="communicate_radio",
                            inline=False,
                            labelStyle={'margin-bottom': '2px'}
                        ),
                        id="communicate_radio_container"  # new container ID
                    ),
                    html.Br(),
                    html.Div([
                        dbc.Label("Anecdotes/Remarks/Opportunities for Improvement:"),
                        dbc.Textarea(id="communicate_remarks", placeholder="Enter your remarks here...")
                    ], className="mb-3")
                ]
            ),
        ],
        className="mb-4"
    ),

    # Section 6: Completion of Assigned Task
    dbc.Card(
        [
            dbc.CardHeader(
                [
                    dbc.Col(
                        html.H5("COMPLETION OF ASSIGNED TASK", 
                                className="card-title",
                                style={'color': highlight_colors['secondary']}), 
                    )
                ],
                style={"background-color": highlight_colors['accent']}
            ),
            dbc.CardBody(
                [
                    html.Div(
                        dbc.RadioItems(
                            options=[],
                            id="completion_radio",
                            inline=False,
                            labelStyle={'margin-bottom': '2px'}
                        ),
                        id="completion_radio_container"  # new container ID
                    ),
                    html.Br(),
                    html.Div([
                        dbc.Label("Anecdotes/Remarks/Opportunities for Improvement:"),
                        dbc.Textarea(id="completion_remarks", placeholder="Enter your remarks here...")
                    ], className="mb-3")
                ]
            ),
        ],
        className="mb-4"
    ),
    
], fluid=True)

allowed_layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                [
                    html.Div(  
                            [
                                dcc.Store(id='peer_eval_toload', storage_type='memory', data=0),
                            ]
                    ),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H1(id="peer_eval_header"),
                                        width=8
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            "Back",
                                            color="success",
                                            href="/peer_evaluation_landing"
                                        ),
                                        width=4,
                                        id="peer_eval_back_btn_div",
                                        style={"display": "flex", "justifyContent": "flex-end"}
                                    )
                                ],
                                align="center"
                            ),
                            html.Hr(),
                        ],
                        className="mb-0"
                    ),
                    peer_evaluation_form, 
                    html.Br(),
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Label("Wish to delete?", width=4),
                                dbc.Col(
                                    dbc.Checklist(
                                        id='peer_eval_remove_record',
                                        options=[
                                            {
                                                'label': "Mark for Deletion",
                                                'value': 1
                                            }
                                        ], 
                                        style={'fontWeight':'bold'},
                                    ),
                                    width=5,
                                ),
                            ],
                            className="mb-3",
                        ),
                        id='peer_eval_remove_record_div'
                    ),
                    html.Br(),
                    dbc.Alert(id='peer_eval_alert', is_open=False), # For feedback purpose
                    html.Div(
                            dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="peer_eval_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="peer_eval_cancel_button", n_clicks=0, href="/peer_evaluation_landing"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-3",
                            justify="end",
                            ),
                        id='peer_eval_buttons_div',
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                            dbc.ModalBody(html.H5(id='peer_eval_modal_message')),
                            dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="peer_eval_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id="peer_eval_modal_confirm", color="success"),
                                    ], 
                            )
                                
                        ],
                        centered=True,
                        id='peer_eval_modal',
                        backdrop=True,   
                        className="modal-success"    
                    ),

                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3(id="peer_eval_final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                            dbc.ModalBody(html.H5("Click Proceed to continue.")),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Proceed",
                                    href="/peer_evaluation_landing",
                                    color="success", 
                                ),
                            ),
                        ],
                        centered=True,
                        id='peer_eval_final_modal',
                        backdrop='static',
                        keyboard=False,
                    ),  
                ],
                width=8,
                style={"marginLeft": "15px"},
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ), 
    ], 
)

@app.callback(
    [
        Output('team_member_dropdown', 'options'),
        Output('peer_eval_header', 'children'),
        Output('peer_eval_toload', 'data'),
        Output('peer_eval_remove_record_div', 'style'),
        Output('peer_eval_buttons_div', 'style'),
        Output('peer_eval_back_btn_div', 'style'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('currentuserid', 'data'),
        State('url', 'search'),
    ],
)

def team_members_dropdown(pathname, current_userid, search):
    if pathname == '/peer_evaluation_form_entry':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]

        base_sql = """
            SELECT 
                CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS label, 
                user_id AS value
            FROM maindashboard.users u
            WHERE u.user_del_ind = False 
            AND u.user_office = 1
            AND u.user_id NOT IN (
                SELECT u.user_id 
                FROM maindashboard.users u
                WHERE u.user_id = %s
            )
            AND u.user_id NOT IN(
                SELECT u.user_id 
                FROM maindashboard.users u
                WHERE u.user_office = 1
                AND
                u.user_qao_team_id = 1
            )
        """
        values = [current_userid]
        if create_mode == 'add':
            # In add mode, exclude all users that already have a peer review entry
            sql = base_sql + """
                AND u.user_id NOT IN (
                SELECT pe.evaluatee_id
                FROM director.peer_evaluations pe
                WHERE pe.evaluator_id = %s
                AND evaluation_period_id = (
                    SELECT period_id   AS value
                        FROM director.evaluation_periods
                        WHERE active_status = TRUE
                        AND period_del_ind = FALSE
                )
                AND pe.peer_eval_delete_ind = False
                )
            """
            values += [current_userid]
        
        elif create_mode == 'edit' or create_mode == 'view':
            # In edit mode, get the current staff_profile_id from query string
            evaluation_id = parse_qs(parsed.query).get('id', [None])[0]
            if not evaluation_id:
                raise PreventUpdate

            # Retrieve the current evaluatee_id for this record
            sql_current = """
                SELECT evaluatee_id 
                FROM director.peer_evaluations
                WHERE evaluation_id = %s
                AND evaluator_id = %s
            """
            current_record = db.querydatafromdatabase(sql_current, [evaluation_id, current_userid], ['evaluatee_id'])
            if len(current_record.index) == 0:
                raise PreventUpdate
            current_user_id = int(current_record['evaluatee_id'][0])

            # Exclude all users with profiles except for the one currently selected
            sql = base_sql + """
              AND (
                  u.user_id NOT IN (
                        SELECT evaluatee_id 
                        FROM director.peer_evaluations
                        WHERE peer_eval_delete_ind = False
                        AND evaluation_period_id = (
                            SELECT period_id   AS value
                                FROM director.evaluation_periods
                                WHERE active_status = TRUE
                                AND period_del_ind = FALSE
                        )
                  )
                  OR u.user_id = %s
              )
            """
            values += [current_user_id]
        else:
            raise PreventUpdate
        
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        team_members = df.to_dict('records')

        if create_mode == 'add':
            header = "Add Peer Evaluation Entry"
            peer_eval_toload = 0
            peer_eval_remove_record_div_style = {'display': 'none'}
            button_style = {'display': 'flex', 'justifyContent': 'flex-end'}
            peer_eval_back_btn_div_style = {'display': 'none'}
        elif create_mode == 'edit':
            header = "Edit Peer Evaluation Entry"
            peer_eval_toload = 1
            peer_eval_remove_record_div_style = None
            button_style = {'display': 'flex', 'justifyContent': 'flex-end'}
            peer_eval_back_btn_div_style = {'display': 'none'}
        elif create_mode == 'view':
            header = "View Peer Evaluation Entry"
            peer_eval_toload = 1
            peer_eval_remove_record_div_style = {'display': 'none'}
            button_style = {'display': 'none'}
            peer_eval_back_btn_div_style = {"display": "flex", "justifyContent": "flex-end"}
    else:
        raise PreventUpdate
    return [team_members, header, peer_eval_toload, peer_eval_remove_record_div_style, button_style, peer_eval_back_btn_div_style]


not_allowed_layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("Peer Evaluation Form Submission is not yet available."),
                        html.Hr(),

                        html.P("Wait for the evaluation period to start."),
                        
                        
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ],
)

main_layout =  html.Div(
    [
        dbc.Row(
            [
                dcc.Store(id='layout_load_entry', storage_type='memory', data=0),
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("Peer Evaluation Form Submission is not yet available."),
                        html.Hr(),

                        html.P("Wait for the evaluation period to start."),
                        
                        
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ],
    id="main_layout_entry"
)
    
@app.callback(
    Output('layout_load_entry', 'data'),
    Input('url', 'pathname'),
)
def layout_options(pathname):
    if pathname == '/peer_evaluation_form_entry':
        sql = """
            SELECT COUNT(*)
            FROM director.main_decision
            WHERE decision_bool = 'True'
        """
        values = []
        cols = ['count']
        df  = db.querydatafromdatabase(sql, values, cols)

        main_decision_result = int(df['count'][0])

        if main_decision_result > 0:
            layout_value = 1
        else:
            layout_value = -1
        return layout_value
    
    raise PreventUpdate

@app.callback(
    Output('main_layout_entry', 'children'),
    Input('layout_load_entry', 'data')
)
def final_layout_options(value):
    if value > 0:
        return allowed_layout
    else:
        return not_allowed_layout

@app.callback(
    [
        Output('contributions_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_1_dropdown(pathname):
    if pathname == '/peer_evaluation_form_entry':
        sql = """
            SELECT option_text as label, rating_value as value
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

@app.callback(
    [
        Output('cooperation_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_2_dropdown(pathname):
    if pathname == '/peer_evaluation_form_entry':
        sql = """
            SELECT option_text as label, rating_value as value
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

@app.callback(
    [
        Output('focus_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_3_dropdown(pathname):
    if pathname == '/peer_evaluation_form_entry':
        sql = """
            SELECT option_text as label, rating_value as value
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

@app.callback(
    [
        Output('teamrole_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_4_dropdown(pathname):
    if pathname == '/peer_evaluation_form_entry':
        sql = """
            SELECT option_text as label, rating_value as value
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

@app.callback(
    [
        Output('communicate_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_5_dropdown(pathname):
    if pathname == '/peer_evaluation_form_entry':
        sql = """
            SELECT option_text as label, rating_value as value
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

@app.callback(
    [
        Output('completion_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_6_dropdown(pathname):
    if pathname == '/peer_evaluation_form_entry':
        sql = """
            SELECT option_text as label, rating_value as value
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

@app.callback(
    [
        Output('peer_eval_alert', 'is_open'),
        Output('peer_eval_alert', 'color'),
        Output('peer_eval_alert', 'children'),
        Output('peer_eval_modal', 'is_open'),
        Output('peer_eval_modal_message', 'children'),
        Output('peer_eval_modal_confirm', 'color'),
        Output('peer_eval_final_modal', 'is_open'),
        Output('peer_eval_final_modal_header', 'children'),
    ],
    [
        Input('peer_eval_save_button', 'n_clicks'),
        Input('peer_eval_modal_cancel', 'n_clicks'),
        Input('peer_eval_modal_confirm', 'n_clicks'),
    ], 
    [   
        State('peer_eval_remove_record', 'value'),
        State('url', 'search'),
        State('currentuserid', 'data'),
        State('team_member_dropdown', 'value'),
        State('contributions_radio', 'value'),
        State('cooperation_radio', 'value'),
        State('focus_radio', 'value'),
        State('teamrole_radio', 'value'),
        State('communicate_radio', 'value'),
        State('completion_radio', 'value'),
        State('contributions_remarks', 'value'),
        State('cooperation_remarks', 'value'),
        State('focus_remarks', 'value'),
        State('teamrole_remarks', 'value'),
        State('communicate_remarks', 'value'),
        State('completion_remarks', 'value'),
    ]
)
def save_expense(submitbtn, cancelbtn, confirmbtn, remove_record, search,
                 evaluator, evaluatee, 
                 contributions, cooperation, focus, teamrole, communicate, completion,
                 contributions_remarks, cooperation_remarks, focus_remarks, teamrole_remarks, communicate_remarks, completion_remarks):

    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]
    
    # Set default outputs
    alert_open = False
    alert_color = ""
    alert_text = ""
    initial_modal_open = ""
    initial_modal_message = ""
    btn_color = 'success'
    final_modal_open = False
    final_modal_header = ""

    if eventid == 'peer_eval_save_button' and submitbtn:
        required_fields = [evaluator, evaluatee, contributions, cooperation, focus, teamrole, communicate,completion]
        
        if not all(required_fields) and not remove_record:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
        else: # all inputs are valid
            if create_mode == 'add':
                initial_modal_open = True
                initial_modal_message  = "Are you sure you want to submit this peer evaluation entry?"
            elif create_mode == 'edit':
                if remove_record:
                    initial_modal_open = True
                    initial_modal_message = "Are you sure you want to delete this peer evaluation entry?"
                    btn_color = 'danger'
                else:
                    initial_modal_open = True
                    initial_modal_message = "Are you sure you want to update this peer evaluation entry?"

    elif eventid == 'peer_eval_modal_confirm' and confirmbtn:
        if create_mode == 'add':
            # For inserting into peer evaluations and returning the new evaluation_id
            sql_eval = """
                INSERT INTO director.peer_evaluations (evaluator_id, evaluatee_id, evaluation_period_id)
                VALUES (%s, %s, 
                    (SELECT period_id
                    FROM director.evaluation_periods
                    WHERE active_status = TRUE
                        AND period_del_ind  = FALSE
                    LIMIT 1)
                )
                RETURNING evaluation_id
            """
            values_eval = (evaluator, evaluatee)
            # Use execute_returning to capture the returned evaluation_id
            result_df = db.execute_returning(sql_eval, values_eval, dfcolumns=['evaluation_id'])
            # Cast the returned evaluation_id to a Python int
            evaluation_id = int(result_df['evaluation_id'][0])

            # 2. Prepare the rubric details inserts. Map each rubric to its corresponding input values.
            # Explicitly cast rating values to int in case they are numpy.int64
            rubric_inserts = [
                (evaluation_id, 1, int(contributions), contributions_remarks),
                (evaluation_id, 2, int(cooperation), cooperation_remarks),
                (evaluation_id, 3, int(focus), focus_remarks),
                (evaluation_id, 4, int(teamrole), teamrole_remarks),
                (evaluation_id, 5, int(communicate), communicate_remarks),
                (evaluation_id, 6, int(completion), completion_remarks)
            ]

            # SQL for inserting into evaluation_details
            sql_detail = """
                INSERT INTO director.evaluation_details (evaluation_id, rubric_id, rating_value, feedback)
                VALUES (%s, %s, %s, %s)
            """

            # Loop over each rubric insert and execute the insert query
            for insert_values in rubric_inserts:
                db.modifydatabase(sql_detail, insert_values)
            final_modal_open = True
            final_modal_header = "Peer Evaluation Entry Successfully Submitted"
        elif create_mode == 'edit':
            evaluation_id = parse_qs(parsed.query).get('id', [None])[0]
            if not evaluation_id:
                raise PreventUpdate
            evaluation_id = int(evaluation_id)  # Convert to a native Python int

            if remove_record:
                # If the record is marked for deletion, update the peer_eval_delete_ind flag
                sql_delete_eval = """
                    UPDATE director.peer_evaluations
                    SET peer_eval_delete_ind = True, evaluation_date = CURRENT_TIMESTAMP
                    WHERE evaluation_id = %s
                """
                db.modifydatabase(sql_delete_eval, (evaluation_id,))
                final_modal_open = True
                final_modal_header = "Peer Evaluation Entry Successfully Deleted"
            else:
                # Update the main peer evaluations record.
                sql_update_eval = """
                    UPDATE director.peer_evaluations
                    SET evaluator_id = %s, evaluatee_id = %s, evaluation_date = CURRENT_TIMESTAMP,
                        peer_eval_delete_ind = False
                    WHERE evaluation_id = %s
                """
                values_update_eval = (evaluator, evaluatee, evaluation_id)
                db.modifydatabase(sql_update_eval, values_update_eval)

                # Prepare the rubric details updates for each rubric entry.
                rubric_updates = [
                    (int(contributions), contributions_remarks, 1, evaluation_id),
                    (int(cooperation), cooperation_remarks, 2, evaluation_id),
                    (int(focus), focus_remarks, 3, evaluation_id),
                    (int(teamrole), teamrole_remarks, 4, evaluation_id),
                    (int(communicate), communicate_remarks, 5, evaluation_id),
                    (int(completion), completion_remarks, 6, evaluation_id)
                ]

                # SQL for updating evaluation_details
                sql_update_detail = """
                    UPDATE director.evaluation_details
                    SET rating_value = %s, feedback = %s
                    WHERE rubric_id = %s AND evaluation_id = %s
                """

                # Loop over each rubric update and execute the update query
                for update_values in rubric_updates:
                    db.modifydatabase(sql_update_detail, update_values)
                final_modal_open = True
                final_modal_header = "Peer Evaluation Entry Successfully Updated"
            
    elif eventid == 'peer_eval_modal_cancel' and cancelbtn:
        initial_modal_open = False
        initial_modal_message = ""

    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, final_modal_open, final_modal_header]

@app.callback(
    [ 
        Output('team_member_dropdown', 'disabled'),
        Output('contributions_remarks', 'disabled'),
        Output('cooperation_remarks', 'disabled'),
        Output('focus_remarks', 'disabled'),
        Output('teamrole_remarks', 'disabled'),
        Output('communicate_remarks', 'disabled'),
        Output('completion_remarks', 'disabled'),
        Output('team_member_dropdown', 'style'),
        Output('contributions_remarks', 'style'),
        Output('cooperation_remarks', 'style'),
        Output('focus_remarks', 'style'),
        Output('teamrole_remarks', 'style'),
        Output('communicate_remarks', 'style'),
        Output('completion_remarks', 'style'),
        # New outputs for radio item containers:
        Output('contributions_radio_container', 'style'),
        Output('cooperation_radio_container', 'style'),
        Output('focus_radio_container', 'style'),
        Output('teamrole_radio_container', 'style'),
        Output('communicate_radio_container', 'style'),
        Output('completion_radio_container', 'style'),
    ],
    [
        Input('url', 'search')
    ]
)
def peer_eval_disabled(search):

    editable_disabled_style = {
        "background-color": "white",
        "color": "black",
        "opacity": "1",
        "pointer-events": "none"
    }
    # Initialize the "disabled" properties (booleans)
    team_display = False
    contributions_remarks_display = cooperation_remarks_display = focus_remarks_display = teamrole_remarks_display = communicate_remarks_display = completion_remarks_display = False

    # Initialize style properties as empty dictionaries instead of empty strings
    team_display_style = {}
    contributions_remarks_style = cooperation_remarks_style = focus_remarks_style = teamrole_remarks_style = communicate_remarks_style = completion_remarks_style = {}

    # Initialize the style properties for radio item containers
    contributions_radio_container_style = cooperation_radio_container_style = focus_radio_container_style = teamrole_radio_container_style = communicate_radio_container_style = completion_radio_container_style = {}

    # Parse the URL search parameters
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'add':
            pass
        elif create_mode == 'edit':
            team_display = True
        elif create_mode == 'view':
            team_display = contributions_remarks_display = cooperation_remarks_display = focus_remarks_display = teamrole_remarks_display = communicate_remarks_display = completion_remarks_display = True
            team_display_style = editable_disabled_style
            contributions_remarks_style = cooperation_remarks_style = focus_remarks_style = teamrole_remarks_style = communicate_remarks_style = completion_remarks_style = editable_disabled_style
            contributions_radio_container_style = cooperation_radio_container_style = focus_radio_container_style = teamrole_radio_container_style = communicate_radio_container_style = completion_radio_container_style = editable_disabled_style
    
    return[team_display,
           contributions_remarks_display, cooperation_remarks_display, focus_remarks_display, teamrole_remarks_display, communicate_remarks_display, completion_remarks_display,
           team_display_style, contributions_remarks_style, cooperation_remarks_style, focus_remarks_style, teamrole_remarks_style, communicate_remarks_style, completion_remarks_style,
           contributions_radio_container_style, cooperation_radio_container_style, focus_radio_container_style, teamrole_radio_container_style, communicate_radio_container_style, completion_radio_container_style]

@app.callback(
    [   
        Output('team_member_dropdown', 'value'),
        Output('contributions_radio', 'value'),
        Output('cooperation_radio', 'value'),
        Output('focus_radio', 'value'),
        Output('teamrole_radio', 'value'),
        Output('communicate_radio', 'value'),
        Output('completion_radio', 'value'),
        Output('contributions_remarks', 'value'),
        Output('cooperation_remarks', 'value'),
        Output('focus_remarks', 'value'),
        Output('teamrole_remarks', 'value'),
        Output('communicate_remarks', 'value'),
        Output('completion_remarks', 'value'),
    ],
    [
        Input('peer_eval_toload', 'modified_timestamp'),
    ],
    [
        State('peer_eval_toload', 'data'),
        State('currentuserid', 'data'),
        State('url', 'search'),
    ]
)
def peereval_load(timestamp, toload, current_userid, search):
    if toload:
        parsed = urlparse(search)
        evaluation_id = parse_qs(parsed.query).get('id', [None])[0]
        if evaluation_id is None:
            raise PreventUpdate
        evaluation_id = int(evaluation_id)  # ensure native int

        # 1. Retrieve the evaluatee_id from the peer_evaluations table.
        sql_eval = """
            SELECT evaluatee_id
            FROM director.peer_evaluations
            WHERE evaluation_id = %s
              AND evaluator_id = %s
        """
        eval_df = db.querydatafromdatabase(sql_eval, [evaluation_id, current_userid], ['evaluatee_id'])
        if eval_df.empty:
            raise PreventUpdate
        evaluatee_id = int(eval_df['evaluatee_id'][0])

        # 2. Retrieve evaluation details for each rubric.
        sql_details = """
            SELECT rubric_id, rating_value, feedback
            FROM director.evaluation_details
            WHERE evaluation_id = %s
        """
        details_df = db.querydatafromdatabase(sql_details, [evaluation_id], ['rubric_id', 'rating_value', 'feedback'])
        
        # Create a dictionary mapping rubric_id to its rating and feedback.
        rubric_data = {}
        for _, row in details_df.iterrows():
            rubric_id = int(row['rubric_id'])
            rubric_data[rubric_id] = {
                'rating': int(row['rating_value']),
                'feedback': row['feedback'] if row['feedback'] is not None else ""
            }

        # Get values for each rubric. If a value isn't found, default to None or empty string.
        contributions_val   = rubric_data.get(1, {}).get('rating', None)
        contributions_text  = rubric_data.get(1, {}).get('feedback', "")
        cooperation_val     = rubric_data.get(2, {}).get('rating', None)
        cooperation_text    = rubric_data.get(2, {}).get('feedback', "")
        focus_val           = rubric_data.get(3, {}).get('rating', None)
        focus_text          = rubric_data.get(3, {}).get('feedback', "")
        teamrole_val        = rubric_data.get(4, {}).get('rating', None)
        teamrole_text       = rubric_data.get(4, {}).get('feedback', "")
        communicate_val     = rubric_data.get(5, {}).get('rating', None)
        communicate_text    = rubric_data.get(5, {}).get('feedback', "")
        completion_val      = rubric_data.get(6, {}).get('rating', None)
        completion_text     = rubric_data.get(6, {}).get('feedback', "")

        return [
            evaluatee_id,
            contributions_val,
            cooperation_val,
            focus_val,
            teamrole_val,
            communicate_val,
            completion_val,
            contributions_text,
            cooperation_text,
            focus_text,
            teamrole_text,
            communicate_text,
            completion_text
        ]
    else:
        raise PreventUpdate


