import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, no_update
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

from datetime import datetime
import hashlib
import re

from urllib.parse import urlparse, parse_qs



def hash_password(password): 
    password_bytes = password.encode('utf-8')

    # Generate the hashed password
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    return hashed_password

  

 



form = dbc.Form(
        [
            html.H5(html.B('Personal Information')),
            html.P('Leave blank if office account', className="fst-italic"),
            
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "First Name ", 
                        ], 
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_fname',  value='',disabled=False),
                        width=6,
                    ), 
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Middle Name ", 
                        ], 
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_mname', disabled=False),
                        width=6,
                    ), 
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Surname ", 
                        ], 
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_sname', disabled=False),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Lived Name ",
                        ], 
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_livedname', disabled=False),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            
            
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Birthday "
                        ],
                        width=3),
                    dbc.Col(
                        dbc.Input(type="date", id='user_bday', disabled=False),
                        width=4,
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
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_phone_num',  
                                  placeholder="0000-000-0000", maxLength=13, disabled=False),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "ID Number ",
                        ],
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_id_num', 
                                  placeholder="0000-00000",  maxLength=13, disabled=False),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),

            html.Br(),


            html.H5(html.B('Basic Information')),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Office ",
                            html.Span("*", style={"color":"#F8B237"})
                        ],
                        width=3
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='user_office',
                            placeholder="Select Office", 
                            disabled=False,
                        ),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Position ",
                            html.Span("*", style={"color": "#F8B237"})
                        ], 
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_position', 
                                  placeholder= 'Internal Quality Assurance Team',
                                  disabled=False),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Email Address ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_email', 
                                  placeholder= 'email@up.edu.ph', disabled=False),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Password ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3),
                    dbc.Col(
                        dbc.Input(type="password", id='user_password', disabled=False),
                        width=5,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Confirm Password ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3),
                    dbc.Col(
                        dbc.Input(type="password", id = 'confirm_password', 
                                  placeholder = 'Confirm password' , disabled=False),
                        width=5,
                    ),
                ],
                className="mb-2",
            ),
            # Access Type
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Access Type ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],width=3),
                    dbc.Col(
                        dbc.Select(
                            id='user_access_type',
                            options=[ 
                                {'label': 'Basic Access', 'value': '1'},
                                {'label': 'Full Access', 'value': '2'}, 
                            ],  
                            disabled=False,
                        ),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
    ] 
)




 
layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.Div(  
                            [
                                dcc.Store(id='registeruser_toload', storage_type='memory', data=0),
                            ]
                        ),
                        
                        html.H1("REGISTER NEW USER"),
                        html.Hr(),
                        html.P("", style={"color": "#F8B237"}),
                        dbc.Alert(id='registeruser_alert', is_open=False),  
                        form,
                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='registeruser_removerecord',
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
                            id='registeruser_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="registeruser_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="registeruser_cancel_button", n_clicks=0, href="/search_users"),  
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
                                    ],id='registeruser_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='/search_users', id='registeruser_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='registeruser_successmodal',
                            backdrop=True,   
                            className="modal-success"    
                        ),
                    ],
                    width=8, style={'marginLeft': '15px'}
                    
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
        html.Div(id='dummy-div', style={'display': 'none'})
    ]
)


 

@app.callback(
    [
        Output('user_office', 'options'),
        Output('registeruser_toload', 'data'),
        Output('registeruser_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)

def registeruser_loaddropdown(pathname, search):
    if pathname == '/register_user':
        sql = """
            SELECT office_name as label, office_id as value
            FROM maindashboard.offices
            
            WHERE office_del_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        office_options = df.to_dict('records')
        
        
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [office_options, to_load, removediv_style]







@app.callback(
    [
        Output('registeruser_alert', 'color'),
        Output('registeruser_alert', 'children'),
        Output('registeruser_alert', 'is_open'),
        Output('registeruser_successmodal', 'is_open'),
        Output('registeruser_feedback_message', 'children'),
        Output('registeruser_btn_modal', 'href')
    ],
    [
        Input('registeruser_save_button', 'n_clicks'),
        Input('registeruser_btn_modal', 'n_clicks'),
        Input('registeruser_removerecord', 'value')
    ],
    [
        State('user_fname', 'value'),
        State('user_mname', 'value'),
        State('user_sname', 'value'),
        State('user_livedname', 'value'),
        State('user_bday', 'value'),
        State('user_phone_num', 'value'),
        State('user_id_num', 'value'),
        State('user_office', 'value'),
        State('user_position', 'value'),
        State('user_email', 'value'),
        State('user_password', 'value'),
        State('confirm_password', 'value'),
        State('user_access_type', 'value'),
        State('url', 'search')
    ]
)
def register_user(submitbtn, closebtn, removerecord,
                  fname, mname, sname, livedname, bday, phone_num, id_num,
                  office, position, email, password, confirm_password,
                  user_access_type, search):
    
    ctx = dash.callback_context 

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'registeruser_save_button' and submitbtn:
        
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            parsed = urlparse(search)
            create_mode = parse_qs(parsed.query).get('mode', [None])[0]
            
            if create_mode == 'add':
                # Validation logic only for "add" mode
                if not password:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Check your inputs. Please add a password.'
                    return [alert_color, alert_text, alert_open, modal_open, None, None]  

                if not confirm_password:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Check your inputs. Please confirm your password.'
                    return [alert_color, alert_text, alert_open, modal_open, None, None]  

                if password != confirm_password:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Passwords do not match. Please try again.'
                    return [alert_color, alert_text, alert_open, modal_open, None, None]  
                
                # Insert new user record
                sql = """
                    INSERT INTO maindashboard.users (
                        user_fname, user_mname, user_sname, user_livedname, 
                        user_bday, user_phone_num, user_id_num, 
                        user_office, user_position, user_email, user_password, 
                        user_access_type, user_acc_status, user_del_ind
                    )
                    VALUES (
                        %s, %s, %s, 
                        %s, %s, %s, %s, 
                        %s, %s, %s, %s, 
                        %s, %s, %s
                    )
                """
                
                hashed_password = hash_password(password)
                
                values = (
                    fname, mname, sname, livedname, 
                    bday, phone_num, id_num, 
                    office, position, email, hashed_password, 
                    user_access_type, 1, False
                )

                db.modifydatabase(sql, values) 
                modal_open = True
                feedbackmessage = html.H5("User registered successfully.")
                okay_href = "/search_users"
                
            elif create_mode == 'edit':
                # Update existing user record
                userid = parse_qs(parsed.query).get('id', [None])[0]
                
                if userid is None:
                    raise PreventUpdate
                
                sqlcode = """
                    UPDATE maindashboard.users
                    SET
                        user_livedname = %s,
                        user_bday = %s,
                        user_phone_num = %s, 
                        user_id_num = %s, 
                        user_position = %s,
                        user_email = %s, 
                        user_del_ind = %s
                    WHERE 
                        user_id = %s
                """
                to_delete = bool(removerecord) 
                
                values = [livedname, bday, phone_num, id_num, position, email, to_delete, userid]
                db.modifydatabase(sqlcode, values)
                
                feedbackmessage = html.H5("Account has been updated.")
                okay_href = "/search_users"
                modal_open = True

            else:
                raise PreventUpdate

            return [alert_color, alert_text, alert_open, modal_open,
                    feedbackmessage, okay_href]  

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]  





@app.callback(
    [
        Output('user_fname', 'value'),
        Output('user_mname', 'value'),
        Output('user_sname', 'value'),
        Output('user_livedname', 'value'),
        Output('user_bday', 'value'),
        Output('user_phone_num', 'value'),
        Output('user_id_num', 'value'),
        Output('user_office', 'value'),
        Output('user_position', 'value'),
        Output('user_email', 'value'), 
        Output('user_access_type', 'value'),
    ],
    [  
        Input('registeruser_toload', 'modified_timestamp')
    ],
    [
        State('registeruser_toload', 'data'),
        State('url', 'search')
    ]
)
def registeruser_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        userid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                user_fname, user_mname,  user_sname, 
                user_livedname, user_bday, user_phone_num,  
                user_id_num,  user_office, 
                user_position, user_email, user_access_type
            FROM maindashboard.users
            WHERE user_id = %s
        """
        values = [userid]

        cols = [
            'fname', 'mname', 'sname', 'lname', 
            'bday', 'phone', 'id_num', 'officeid', 'position', 
            'email',  'access_type'
        ]

         
        df = db.querydatafromdatabase(sql, values, cols)

        
        fname = df['fname'][0]
        mname = df['mname'][0]
        sname = df['sname'][0]
        lname = df['lname'][0]
        bday = df['bday'][0]
        phone = df['phone'][0]
        id_num = df['id_num'][0]
        officeid = int(df['officeid'][0])
        position = df['position'][0]
        email = df['email'][0]  
        access_type = df['access_type'][0] 

        
        return [fname, mname, sname, lname, bday, phone, id_num, officeid, position, email, access_type]
    
    else:
        raise PreventUpdate
    



@app.callback(
    [
        Output('user_fname', 'disabled'),
        Output('user_mname', 'disabled'),
        Output('user_sname', 'disabled'),    
        Output('user_office', 'disabled'), 
        Output('user_password', 'disabled'),
        Output('confirm_password', 'disabled'),
        Output('user_access_type', 'disabled'),
    ],
    [Input('url', 'search')]
)
def set_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 7  # Disable all inputs in edit mode
    return [False] * 7  # Enable all inputs otherwise
