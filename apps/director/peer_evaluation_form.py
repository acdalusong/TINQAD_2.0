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
                    dbc.RadioItems(
                        options=[],
                        id="final_contributions_radio",
                        inline=False,
                        labelStyle={'margin-bottom': '2px'}
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
                    dbc.RadioItems(
                        options=[],
                        id="final_cooperation_radio",
                        inline=False,
                        labelStyle={'margin-bottom': '2px'}
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
                    dbc.RadioItems(
                        options=[],
                        id="final_focus_radio",
                        inline=False,
                        labelStyle={'margin-bottom': '2px'}
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
                    dbc.RadioItems(
                        options=[],
                        id="final_teamrole_radio",
                        inline=False,
                        labelStyle={'margin-bottom': '2px'}
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
                    dbc.RadioItems(
                        options=[],
                        id="final_communicate_radio",
                        inline=False,
                        labelStyle={'margin-bottom': '2px'}
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
                    dbc.RadioItems(
                        options=[],
                        id="final_completion_radio",
                        inline=False,
                        labelStyle={'margin-bottom': '2px'}
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

layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                [
                    dbc.Button("Back", href='/peer_evaluation_settings'),
                    html.Hr(),
                    html.Div(  
                            [
                                dcc.Store(id='final_eval_toload', storage_type='memory', data=0),
                            ]
                        ),
                    dbc.Alert(id='final_eval_alert', is_open=False), # For feedback purpose
                    peer_evaluation_form, 
                    html.Br(),

                    html.Br(),

                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                            dbc.ModalBody(html.H5(id='final_eval_modal_message')),
                            dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="final_eval_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id="final_eval_modal_confirm", color="success"),
                                    ], 
                            )
                                
                        ],
                        centered=True,
                        id='final_eval_modal',
                        backdrop=True,   
                        className="modal-success"    
                    ),

                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3(id="final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                            dbc.ModalBody(html.H5("Click Proceed to continue.")),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Proceed",
                                    href="/record_expenses",
                                    color="success", 
                                ),
                            ),
                        ],
                        centered=True,
                        id='final_modal',
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
    ]
)

@app.callback(
    [
        Output('final_contributions_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_1_dropdown(pathname):
    if pathname == '/peer_evaluation_settings/peer_evaluation_forms':
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

@app.callback(
    [
        Output('final_cooperation_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_2_dropdown(pathname):
    if pathname == '/peer_evaluation_settings/peer_evaluation_forms':
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

@app.callback(
    [
        Output('final_focus_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_3_dropdown(pathname):
    if pathname == '/peer_evaluation_settings/peer_evaluation_forms':
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

@app.callback(
    [
        Output('final_teamrole_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_4_dropdown(pathname):
    if pathname == '/peer_evaluation_settings/peer_evaluation_forms':
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

@app.callback(
    [
        Output('final_communicate_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_5_dropdown(pathname):
    if pathname == '/peer_evaluation_settings/peer_evaluation_forms':
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

@app.callback(
    [
        Output('final_completion_radio', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def rubrics_6_dropdown(pathname):
    if pathname == '/peer_evaluation_settings/peer_evaluation_forms':
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