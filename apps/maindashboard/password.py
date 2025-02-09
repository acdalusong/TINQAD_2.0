import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db 

import hashlib



password_header = html.Div(
    [
        html.Div(
            [
                html.H3(id="password_name_header", style={'marginBottom': 0}),
                html.P(id="password_idnumber", style={'marginBottom': 0})  
            ],
            style={'display': 'inline-block', 'verticalAlign': 'center'}
        ),
    ],
    style={'textAlign': 'left', 'marginTop': '20px'}
)
 

@app.callback(
    [
        Output('password_name_header', 'children'),
        Output('password_idnumber', 'children'),
    ], 
    [Input('url', 'pathname')],
    [State('currentuserid', 'data')]
)
def update_password_header(pathname, current_userid):
    user_info = db.get_user_info(current_userid)

    if user_info: 
        user_fname = user_info.get('user_fname', '')
        user_sname = user_info.get('user_sname', '')
        user_livedname = user_info.get('user_livedname', '')
        user_id_num = user_info.get('user_id_num', '')

        # Concatenate full name
        fullname_parts = [part for part in [user_fname, user_sname] if part]   
        if user_livedname:
            fullname_parts.append('"' + user_livedname + '"')
        fullname = " ".join(fullname_parts)

        return fullname, user_id_num
    else:
        return "",""
  
@app.callback(
    [
        Output('password_alert', 'color'),
        Output('password_alert', 'children'),
        Output('password_alert', 'is_open'),
        Output('password_successmodal', 'is_open'),
        Output('password_feedback_message', 'children'),
    ],
    [Input('password_save_button', 'n_clicks')],
    [   
        State('currentuserid', 'data'),
        State('prev_password', 'value'),
        State('new_password', 'value'),
        State('confirm_password', 'value'), 
    ]
)
def save_profile_changes(save, current_userid, prev_password, new_password, confirm_password):
    if save:
        # Check if new password and confirm password match
        if new_password != confirm_password:
            return 'danger', "New password and confirm password do not match.", True, False, ''

        # Check if previous password matches the one in the database
        if db.verify_password(current_userid, prev_password):
            # Update the password in the database
            db.update_password(current_userid, new_password)
            return 'success', '', False, True, 'Password updated successfully.'
        else:
            return 'danger', "Previous password is incorrect.", True, False, ''
    else:
        raise PreventUpdate
    



    








form = dbc.Form( 
    [  
                dbc.Row(
                    [
                        dbc.Label("Previous Password", width=4),
                        dbc.Col(dbc.Input(type="password", id="prev_password"), width=8),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Label("New Password", width=4),
                        dbc.Col(dbc.Input(type="password", id="new_password"), width=8),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Label("Confirm Password", width=4),
                        dbc.Col(dbc.Input(type="password", id="confirm_password"), width=8),
                    ],
                    className="mb-2",
                ), 
        ],
    className="g-2",
)
     



layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        password_header,
                        html.Hr(),
                        dbc.Alert(id='password_alert', is_open=False),  
                        html.Br(), 
                        form,  
                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="password_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="password_cancel_button", n_clicks=0, href="/homepage"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),

                        

                        dbc.Modal(
                            [
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['User registered successfully.'
                                    ],id='password_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='/homepage', id='password_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='password_successmodal',
                            backdrop=True,   
                            className="modal-success"    
                        ),
                    ], 
                    width=6, 
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
    ]
)

 