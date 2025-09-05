import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, dash_table
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd
import hashlib

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db


 
# Your profile header component with circular image
profile_header = html.Div(
    [
        html.Div(
            [
                 
                html.H3(id="user_fullname", style={'marginBottom': 0}),
                html.P(id="user_idnumber", style={'marginBottom': 0})  
            ],
            style={'display': 'inline-block', 'verticalAlign': 'center'}
        ),
    ],
    style={'textAlign': 'left', 'marginTop': '20px'}
)


@app.callback(
    [
        Output('user_fullname', 'children'),
        Output('user_idnumber', 'children'),
        Output('userprof_fname', 'value'),
        Output('userprof_mname', 'value'),  
        Output('userprof_sname', 'value'),
        Output('userprof_suffixname', 'value'),
        Output('userprof_id_num', 'value'),
        Output('userprof_livedname', 'value'),
        Output('userprof_preferredpronouns', 'value'),
        Output('userprof_bday', 'value'),
        Output('userprof_placeofbirth', 'value'),
        Output('userprof_bloodtype', 'value'),
        Output('userprof_phone_num', 'value'),
        Output('userprof_office', 'value'),
        Output('userprof_position', 'value'),
        Output('userprof_email', 'value'),
    ], 
    [
        Input('url', 'pathname'), 
    ],
    [State('currentuserid', 'data')]
)

def update_profile_header(pathname, current_userid):
    user_info = db.get_user_info(current_userid)

    if user_info: 
        user_fname = user_info.get('user_fname', '')
        user_mname = user_info.get('user_mname', '')
        user_sname = user_info.get('user_sname', '')
        user_suffixname = user_info.get('user_suffixname', '')
        user_livedname = user_info.get('user_livedname', '')
        user_preferredpronouns = user_info.get('user_preferredpronouns', '')
        user_id_num = user_info.get('user_id_num', '')
        user_bday = user_info.get('user_bday', '')
        user_placeofbirth = user_info.get('user_placeofbirth', '')
        user_bloodtype = user_info.get('user_bloodtype', '')
        user_phone_num = user_info.get('user_phone_num', '')
        user_office_id = user_info.get('user_office', '')  # Retrieve office ID
        user_position = user_info.get('user_position', '')
        user_email = user_info.get('user_email', '')
        

        # Retrieve office name based on office ID
        user_office_name = db.get_office_info(user_office_id)

        # Concatenate full name
        fullname_parts = [part for part in [user_fname, user_mname, user_sname, user_suffixname] if part]
        if user_livedname:
            fullname_parts.append('"' + user_livedname + '"')
        fullname = " ".join(fullname_parts)

        return (
            fullname, user_id_num, user_fname, user_mname, user_sname, user_suffixname,
            user_id_num, user_livedname, user_preferredpronouns, user_bday, user_placeofbirth, user_bloodtype, user_phone_num,
            user_office_name, user_position, user_email
        )
    else:
        return "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
  
@app.callback(
    [    
        Output('user_profile_alert', 'is_open'),
        Output('user_profile_alert', 'color'),
        Output('user_profile_alert', 'children'),
        Output('userprof_initialmodal', 'is_open'),
        Output('user_profile_success', 'is_open'),
        Output('user_profile_success', 'children'),
        Output('userprof_offcanvas','is_open'),
        Output('userprof_offcanvas', 'className'),
        Output('userprof_email', 'className'),
    ],
    [
        Input('userprof_save_button', 'n_clicks'),
        Input('userprof_initialmodal_cancel', 'n_clicks'),
        Input('userprof_initialmodal_confirm', 'n_clicks')
    ],
    [   
        State('currentuserid', 'data'),
        State('userprof_fname', 'value'),
        State('userprof_mname', 'value'),
        State('userprof_sname', 'value'),
        State('userprof_suffixname', 'value'),
        State('userprof_id_num', 'value'),
        State('userprof_livedname', 'value'),
        State('userprof_preferredpronouns', 'value'),
        State('userprof_bday', 'value'),
        State('userprof_placeofbirth', 'value'),
        State('userprof_bloodtype', 'value'),
        State('userprof_phone_num', 'value'), 
        State('userprof_position', 'value'),
        State('userprof_email', 'value'),
        State('userprof_password', 'value'),
        State('userprof_confirmpassword', 'value'),
        State('userprof_offcanvas', 'is_open')
    ]
)
def save_profile_changes(save_btn, cancel_btn, confirm_btn, current_userid, fname, mname, sname, suffixname, id_num, livedname, pronouns, bday, placeofbirth, bloodtype, phone_num, position, email, password,
                         confirm_pw, confirm_condition):
    
    
    def hash_password(password): 
        if not password:
            return None
        password_bytes = password.encode('utf-8')
        # Generate the hashed password
        hashed_password = hashlib.sha256(password_bytes).hexdigest()
        return hashed_password

    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise PreventUpdate
    
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    alert_open = False
    alert_color = ''
    alert_message = ''
    initial_modal = False
    success_open = False
    success_message = ''
    offcanvas_open = False
    user_email_class = ''
    offcanvas_class = "offcanvas"

    if eventid == 'userprof_save_button' and save_btn:
        required_fields = []
        if not all(required_fields):
            alert_open = True
            alert_color = 'danger'
            alert_message = 'Please fill in all fields.'
        elif (password or confirm_pw) and password != confirm_pw:
            alert_open = True
            alert_color = 'danger'
            alert_message = 'Password and Confirm Password do not match.'
        else:
            initial_modal = True
        

    elif eventid == 'userprof_initialmodal_cancel' and cancel_btn:
        initial_modal = False

    elif eventid == 'userprof_initialmodal_confirm' and confirm_btn:

        # Check if email already exists in the database
        checker_b = """
        SELECT user_email
        FROM maindashboard.users
        WHERE user_email = %s AND user_id != %s AND user_del_ind = False
        """
        checker_values_b = [email, current_userid]
        checker_cols_b = ['user_email']
        df_checker_b = db.querydatafromdatabase(checker_b, checker_values_b, checker_cols_b)
        if not df_checker_b.empty:
            alert_open = True
            alert_color = 'danger'
            alert_message = 'Email already exists. Please use a different email.'
            user_email_class= 'red-border'
            initial_modal = False
            offcanvas_open = False
            return [alert_open, alert_color, alert_message, initial_modal, success_open, success_message, offcanvas_open, '' ,user_email_class] 
        # Treat None as ''
        pw = password or ""
        cpw = confirm_pw or ""

        if pw and pw == cpw:
            # we have a non‐empty password match => hash & update it
            hashed = hash_password(pw)
            sql = """
            UPDATE maindashboard.users
            SET user_fname = %s, user_mname = %s, user_sname = %s, user_suffixname = %s, user_id_num = %s,
                user_livedname = %s, user_preferredpronouns = %s, user_bday = %s, user_placeofbirth = %s, user_bloodtype = %s,
                user_phone_num = %s, user_position = %s, user_email = %s, user_password = %s
            WHERE user_id = %s
            """
            values = (
                fname, mname, sname, suffixname, id_num,
                livedname, pronouns, bday, placeofbirth,
                bloodtype, phone_num, position, email,
                hashed, current_userid
            )
            db.modifydatabase(sql, values)
            # new_refresh_value = current_refresh + 1
        else:
            # either no password provided, or mismatch — update everything *except* password
            sql_b = """
            UPDATE maindashboard.users
            SET user_fname = %s, user_mname = %s, user_sname = %s, user_suffixname = %s, user_id_num = %s,
                user_livedname = %s, user_preferredpronouns = %s, user_bday = %s, user_placeofbirth = %s, user_bloodtype = %s,
                user_phone_num = %s, user_position = %s, user_email = %s
            WHERE user_id = %s
            """
            values_b = (
                fname, mname, sname, suffixname, id_num,
                livedname, pronouns, bday, placeofbirth,
                bloodtype, phone_num, position, email,
                current_userid
            )
            db.modifydatabase(sql_b, values_b)
            # new_refresh_value = current_refresh + 1

        initial_modal = False
        success_open = True
        success_message = 'Your profile changes have been saved.'
        offcanvas_open = True

    elif confirm_condition:
        # show & shake
        offcanvas_open = True
        offcanvas_class = "offcanvas shake"
    else: 
        raise PreventUpdate
    return [alert_open, alert_color, alert_message, initial_modal, success_open, success_message, offcanvas_open, offcanvas_class, user_email_class]



form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                        "First Name ",
                        
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="text", id='userprof_fname'), width=6),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Middle Name",
                        
                    ], 
                    width=4),
                dbc.Col(dbc.Input(type="text", id='userprof_mname'), width=6),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Surname ",
                        
                    ], 
                    width=4),
                dbc.Col(dbc.Input(type="text", id='userprof_sname' ), width=6),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Suffix Name ",
                        
                    ], 
                    width=4),
                dbc.Col(dbc.Input(type="text", id='userprof_suffixname' ), width=6),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "ID Number ",
                        
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="text", id='userprof_id_num' ), width=6),
            ],
            className="mb-2",
        ), 
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Lived Name "
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="text", id='userprof_livedname' ), width=6),
            ],
            className="mb-2", 
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Preferred Pronouns "
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="text", id='userprof_preferredpronouns' ), width=6),
            ],
            className="mb-2", 
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Birthday "
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='userprof_bday'),
                    width=6,
                ),
            ],
            className="mb-2", 
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Place of Birth "
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id='userprof_placeofbirth'),
                    width=6,
                ),
            ],
            className="mb-2", 
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Blood Type "
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id='userprof_bloodtype'),
                    width=6,
                ),
            ],
            className="mb-2", 
        ),
        dbc.Row(
               [
                dbc.Label(
                    [
                        "Phone Number "
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(
                        type="text", id='userprof_phone_num', placeholder="0000-00-00000"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
       
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Office/Department ",
                        
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="text" , id='userprof_office', disabled=True ), width=6),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Position ",
                        
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="text" , id='userprof_position' ), width=6),
            ],
            className="mb-2",
        ),
        
         
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Email Address (primary) ",
                        
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="text", id='userprof_email'), width=6),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Password ",
                        
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="password" , id='userprof_password' ), width=6),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Confirm Password ",
                        
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="password" , id='userprof_confirmpassword' ), width=6),
            ],
            className="mb-2",
        ),
        dbc.Checklist(
            options=[
                {"label": "Show Password", "value": 1}
            ],
            value=[],
            id="profile_show_password",
            inline=True,
        ),
    ],
    className="g-2",
)


@app.callback(
    [
        Output('userprof_password', 'type'),
        Output('userprof_confirmpassword', 'type'),
    ],
    [Input('profile_show_password', 'value')]
)
def toggle_password_visibility(checked_values):
    if checked_values:
        return 'text', 'text'
    else:
        return 'password', 'password'

layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                [
                    profile_header,  
                    html.Hr(),
                    
                    html.Br(), 
                    form, 
                    dbc.Alert(id='user_profile_alert', is_open=False), # For feedback purpose 
                    dbc.Alert(id='user_profile_success', is_open=False, color='success', duration=4000),
                    # Offcanvas slide‑in from the right on successful save
                    dbc.Offcanvas(
                        [
                            html.H5("Your profile changes have been saved.", className="mb-3"),
                            html.P([
                                "You may now return to the homepage by clicking ",
                                html.A("Proceed", href="/homepage", className="fw-bold"),
                                ", or browse through different modules from the navigation bar."
                            ]),
                        ],
                        id="userprof_offcanvas",
                        title="Success!",
                        is_open=False,
                        placement="end",
                        backdrop=True,
                        style={
                            "width": "400px",               # default was 400px → make it wider
                            "maxWidth": "80%",              # but cap at 80% of viewport on small screens
                            "boxShadow": "0 0.5rem 1rem rgba(0,0,0,0.5)",  # deeper shadow
                        },
                        className="offcanvas",
                        scrollable=True,
                    ),
                    dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="userprof_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="userprof_cancel_button", n_clicks=0, href="homepage"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(
                                    html.H5('Are you sure you want to save your changes?'),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id= "userprof_initialmodal_cancel", color="warning"),
                                        dbc.Button("Confirm", id= "userprof_initialmodal_confirm", color="success")
                                    ]
                                ),
                            ],
                            centered=True,
                            id='userprof_initialmodal',
                            backdrop=True,   
                            className="modal-success"    
                        ), 
                    ], 
                    width=8, 
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

