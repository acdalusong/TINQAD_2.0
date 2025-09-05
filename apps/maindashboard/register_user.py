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
                    dbc.Label("First Name ", width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_fname', value='', disabled=False),
                        width=6,
                    ), 
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label("Middle Name ", width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_mname', disabled=False),
                        width=6,
                    ), 
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label("Surname ", width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_sname', disabled=False),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label("Suffix Name ", width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_suffixname', disabled=False),
                        width=6,
                    ), 
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label("Lived Name ", width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_livedname', disabled=False),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            
            dbc.Row(
                [
                    dbc.Label("Birthday ", width=3),
                    dbc.Col(
                        dbc.Input(type="date", id='user_bday', disabled=False),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label("Sex at Birth", width=3),
                    dbc.Col(
                        dbc.Select(
                            id='user_sexatbirth',
                            disabled = False,
                            options=[
                                {"label": "Male", "value": "Male"},
                                {"label": "Female", "value": "Female"},
                                {"label": "Other", "value": "Other"}
                            ],
                        ),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label("Place of Birth", width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_placeofbirth', disabled=False),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label("Blood Type", width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_bloodtype', disabled=False),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label("Preferred Pronouns", width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_preferredpronouns', disabled=False),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label("Phone Number ", width=3),
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
                    dbc.Label("ID Number ", width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='user_id_num', 
                                  placeholder="0000-00000", maxLength=13, disabled=False),
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
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='user_office_id',
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
                            "QAO Team",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3
                    ),
                    dbc.Col(
                        dbc.Select(
                            id='user_qao_team_id',
                            placeholder="Select QAO Team",
                            options=[],
                            disabled=False,
                        ),
                        width=6,
                    ),
                ],
                id='user_qao_team_id_div',
                className="mb-2",
                style={'display': 'none'}  # Hidden by default
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Position ",
                            html.Span("*", style={"color": "#F8B237"})
                        ], 
                        width=3
                    ),
                    dbc.Col(
                        dbc.Input(type="text", id='user_position', 
                                  placeholder='Student Intern, etc.',
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
                        width=3
                    ),
                    dbc.Col(
                        dbc.Input(type="text", id='user_email', 
                                  placeholder='email@up.edu.ph', disabled=False),
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
                        width=3
                    ),
                    dbc.Col(
                        dbc.Input(type="password", id='user_password', disabled=False),
                        width=6,
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
                        width=3
                    ),
                    dbc.Col(
                        dbc.Input(type="password", id='confirm_password', 
                                  placeholder='Confirm password', disabled=False),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Checklist(
                    options=[
                        {"label": "Show Password", "value": 1}
                    ],
                    value=[],
                    id="register_show_password",
                    inline=True,
                    ),
            # Access Type
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Access Type ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3
                    ),
                    dbc.Col(
                        dbc.Select(
                            id='user_access_type',
                            options=[],  
                            disabled=False,
                        ),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
    ] 
)

@app.callback(
    [
        Output('user_password', 'type'),
        Output('confirm_password', 'type'),
    ],
    [Input('register_show_password', 'value')]
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
                        html.Div(
                            [
                                dcc.Store(id='registeruser_toload', storage_type='memory', data=0),
                                dcc.Store(id='qao_team_required_info', storage_type='memory', data=0),
                            ]
                        ),
                        html.H1("REGISTER NEW USER"),
                        html.Hr(),
                        html.P("", style={"color": "#F8B237"}),
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
                                                {'label': "Mark for Deletion", 'value': 1}
                                            ], 
                                            style={'fontWeight': 'bold'},
                                        ),
                                        width=5,
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='registeruser_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Alert(id='registeruser_alert', is_open=False),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary", id="registeruser_save_button", n_clicks=0),
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
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='registeruser_initialmodal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="registeruser_initialmodal_cancel", color="warning"),
                                            dbc.Button("Confirm", id="registeruser_initialmodal_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='registeruser_initialmodal',
                            backdrop=True,
                            className="modal-success"
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id='registeruser_successmodal_header'), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Click Proceed to continue.")),
                                dbc.ModalFooter(
                                    dbc.Button("Proceed", href='/search_users'),
                                )
                            ],
                            centered=True,
                            id='registeruser_successmodal',
                            backdrop='static',
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
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ),
        html.Div(id='dummy-div', style={'display': 'none'})
    ]
)


# Callback to populate Office dropdown and determine mode (add/edit)
@app.callback(
    [
        Output('user_office_id', 'options'),
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
    Output('user_qao_team_id_div', 'style'),
    Output('qao_team_required_info', 'data'),
    Input('user_office_id', 'value')
)
def toggle_qao_dropdown(selected_office):
    if selected_office == 1:
        data_value = 1
        return [{'display': 'flex'}, data_value]
    else:
        data_value = 0
        return [{'display': 'none'}, data_value]




# Populate QAO Team options based on Office selection
@app.callback(
    Output('user_qao_team_id', 'options'),
    Input('user_office_id', 'value'),
)
def update_qao_team_options(selected_office):
    if selected_office is None:
        return []
    try:
        sql = """
        SELECT qao_team_names as label, qao_team_id as value
        FROM maindashboard.qao_teams
        WHERE office_id = %s
        """
        values = [selected_office]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        qao_team_options = df.to_dict('records')
        return qao_team_options
    except Exception as e:
        return []


# Populate Access Type dropdown
@app.callback(
    Output('user_access_type', 'options'),
    [Input('url', 'pathname')]
)
def populate_useraccess_dropdown(pathname):
    if pathname == '/register_user':
        sql = """
            SELECT access_type_name as label, access_type_id as value
            FROM maindashboard.access_type
            ORDER BY access_type_id ASC
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        access_types = df.to_dict('records')
    else:
        raise PreventUpdate
    return access_types



# Callback for saving user data (both add and edit modes)
@app.callback(
    [
        Output('registeruser_alert', 'is_open'),
        Output('registeruser_alert', 'color'),
        Output('registeruser_alert', 'children'),
        Output('registeruser_initialmodal', 'is_open'),
        Output('registeruser_initialmodal_message', 'children'),
        Output('registeruser_initialmodal_confirm', 'color'),
        Output('registeruser_successmodal', 'is_open'),
        Output('registeruser_successmodal_header', 'children'),
        Output('user_fname', 'className'),
        Output('user_mname', 'className'),
        Output('user_sname', 'className'),
        Output('user_bday', 'className'),
        Output('user_sexatbirth', 'className'),
        Output('user_placeofbirth', 'className'),
        Output('user_bloodtype', 'className'),
        Output('user_phone_num', 'className'),
        Output('user_id_num', 'className'),
        Output('user_qao_team_id', 'className'),
        Output('user_position', 'className'),
        Output('user_email', 'className'),
        Output('user_password', 'className'),
        Output('confirm_password', 'className'),
        Output('user_access_type', 'className'),
        Output('user_office_id', 'className')
    ],
    [
        Input('registeruser_save_button', 'n_clicks'),
        Input('registeruser_initialmodal_cancel', 'n_clicks'),
        Input('registeruser_initialmodal_confirm', 'n_clicks'),
        
    ],
    [
        State('registeruser_removerecord', 'value'),
        State('user_fname', 'value'),
        State('user_mname', 'value'),
        State('user_sname', 'value'),
        State('user_suffixname', 'value'),
        State('user_livedname', 'value'),
        State('user_bday', 'value'),
        State('user_sexatbirth', 'value'),
        State('user_placeofbirth', 'value'),
        State('user_bloodtype', 'value'),
        State('user_preferredpronouns', 'value'),
        State('user_phone_num', 'value'),
        State('user_id_num', 'value'),
        State('user_office_id', 'value'),
        State('user_qao_team_id', 'value'),
        State('user_position', 'value'),
        State('user_email', 'value'),
        State('user_password', 'value'),
        State('confirm_password', 'value'),
        State('user_access_type', 'value'),
        State('url', 'search'),
        State('qao_team_required_info', 'data'),
    ]
)
def register_user(submitbtn, cancelbtn, confirmbtn, removerecord,
                  fname, mname, sname, suffixname, livedname, bday, sexatbirth, placeofbirth, bloodtype, preferredpronouns, phone_num, id_num,
                  office, user_qao_team_id, position, email, password, confirm_password,
                  user_access_type, search, qao_team_required_info):
    
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate
    
    alert_open = False
    alert_color = ''
    alert_text = ''
    initial_modal_open = False
    initial_message = ''
    confirm_btn_color = 'success'
    final_modal_open = False
    final_header = ''
    user_fname_class = ''
    user_mname_class = ''
    user_sname_class = ''
    user_bday_class = ''
    user_sexatbirth_class = ''
    user_placeofbirth_class = ''
    user_bloodtype_class = ''
    user_phone_num_class = ''
    user_id_num_class = ''
    user_qao_team_id_class = ''
    user_position_class = ''
    user_email_class = ''
    user_password_class = ''
    user_confirm_password_class = ''
    user_access_type_class = ''
    user_office_class = ''

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]
    
    def get_input_class(value):
            return 'red-border' if not value else 'form-control'

    if eventid == 'registeruser_save_button' and submitbtn:
        if create_mode == 'add':
            if qao_team_required_info == 1:
                required_fields = [fname, mname, sname, bday, sexatbirth, placeofbirth, bloodtype, phone_num, id_num, user_qao_team_id, 
                                position, email, password, confirm_password, user_access_type]
                if not all(required_fields) and not removerecord:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Check your inputs. Please fill out the required fields.'
                    user_bday_class = 'SingleDatePicker red-border' if not bday else 'SingleDatePicker'
                    user_fname_class= get_input_class(fname)
                    user_mname_class= get_input_class(mname)
                    user_sname_class= get_input_class(sname)
                    user_sexatbirth_class= get_input_class(sexatbirth)
                    user_placeofbirth_class= get_input_class(placeofbirth)
                    user_bloodtype_class= get_input_class(bloodtype)
                    user_phone_num_class= get_input_class(phone_num)
                    user_id_num_class= get_input_class(id_num)
                    user_qao_team_id_class= get_input_class(user_qao_team_id)
                    user_position_class= get_input_class(position)
                    user_email_class= get_input_class(email)
                    user_password_class= get_input_class(password)
                    user_confirm_password_class= get_input_class(confirm_password)
                    user_access_type_class= get_input_class(user_access_type)

                elif password != confirm_password:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Password and Confirm Password do not match.'
                    user_fname_class= get_input_class(fname)
                    user_mname_class= get_input_class(mname)
                    user_sname_class= get_input_class(sname)
                    user_sexatbirth_class= get_input_class(sexatbirth)
                    user_placeofbirth_class= get_input_class(placeofbirth)
                    user_bloodtype_class= get_input_class(bloodtype)
                    user_phone_num_class= get_input_class(phone_num)
                    user_id_num_class= get_input_class(id_num)
                    user_qao_team_id_class= get_input_class(user_qao_team_id)
                    user_position_class= get_input_class(position)
                    user_email_class= get_input_class(email)
                    user_access_type_class= get_input_class(user_access_type)
                    user_password_class= 'red-border'
                    user_confirm_password_class= 'red-border'
                else:
                    initial_modal_open = True
                    initial_message = "Are you sure you want to add this user entry?"
            else:  
                required_fields = [office, position, email, password, confirm_password, user_access_type]
                if not all(required_fields) and not removerecord:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Check your inputs. Please fill out the required fields.' 
                    user_office_class = get_input_class(office)
                    user_position_class= get_input_class(position)
                    user_email_class= get_input_class(email)
                    user_password_class= get_input_class(password)
                    user_confirm_password_class= get_input_class(confirm_password)
                    user_access_type_class= get_input_class(user_access_type)
                elif password != confirm_password:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Password and Confirm Password do not match.'
                    user_position_class= get_input_class(position)
                    user_email_class= get_input_class(email)
                    user_access_type_class= get_input_class(user_access_type)
                    user_password_class= 'red-border'
                    user_confirm_password_class= 'red-border'
                else: 
                    initial_modal_open = True
                    initial_message = "Are you sure you want to add this user entry?"

        elif create_mode == 'edit':
            if removerecord:
                initial_modal_open = True
                initial_message = "Are you sure you want to delete this user entry?"
                confirm_btn_color = 'danger'
            else:
                initial_modal_open = True
                initial_message = "Are you sure you want to edit this user entry?"
                confirm_btn_color = 'success'
        else:
            print("Unexpected mode:", create_mode)
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Invalid mode specified in the URL.'
    elif eventid == 'registeruser_initialmodal_confirm' and confirmbtn:
        if create_mode == 'add':
            checker = """
                SELECT user_email
                FROM maindashboard.users
                WHERE user_email = %s AND
                user_del_ind = False
            """
            checker_values = [email]
            checker_cols = ['user_email']
            df_checker = db.querydatafromdatabase(checker, checker_values, checker_cols)
            if not df_checker.empty:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Email already exists. Please use a different email.'
                user_email_class= 'red-border'
                initial_modal_open = False
                final_modal_open = False
                return [alert_open, alert_color, alert_text, initial_modal_open, initial_message, confirm_btn_color, final_modal_open, final_header,
                    user_fname_class, user_mname_class, user_sname_class, user_bday_class, user_sexatbirth_class, user_placeofbirth_class,
                    user_bloodtype_class, user_phone_num_class, user_id_num_class, user_qao_team_id_class, user_position_class, user_email_class,
                    user_password_class, user_confirm_password_class, user_access_type_class, user_office_class]  

            # add user to database
            sql = """
                INSERT INTO maindashboard.users (
                    user_fname, user_mname, user_sname, user_livedname, 
                    user_bday, user_phone_num, user_id_num, 
                    user_office, user_qao_team_id, user_position, user_email, user_password, 
                    user_access_type, user_acc_status, user_del_ind, 
                    user_suffixname, user_sexatbirth, user_placeofbirth, user_bloodtype, user_preferredpronouns
                )
                VALUES (
                    %s, %s, %s, 
                    %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """
            hashed_password = hash_password(password)
            values = (
                fname, mname, sname, livedname, 
                bday, phone_num, id_num, 
                office, user_qao_team_id, position, email, hashed_password, 
                user_access_type, 1, False,
                suffixname, sexatbirth, placeofbirth, bloodtype, preferredpronouns
            )
            db.modifydatabase(sql, values)
            final_modal_open = True
            final_header = "User Successfully Added"
        elif create_mode == 'edit':
            userid = parse_qs(parsed.query).get('id', [None])[0]
            if userid is None:
                raise PreventUpdate
            
            # Check if email already exists in the database
            checker_b = """
            SELECT user_email
            FROM maindashboard.users
            WHERE user_email = %s AND user_id != %s AND user_del_ind = False
            """
            checker_values_b = [email, userid]
            checker_cols_b = ['user_email']
            df_checker_b = db.querydatafromdatabase(checker_b, checker_values_b, checker_cols_b)
            if not df_checker_b.empty:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Email already exists. Please use a different email.'
                user_email_class= 'red-border'
                initial_modal_open = False
                final_modal_open = False
                return [alert_open, alert_color, alert_text, initial_modal_open, initial_message, confirm_btn_color, final_modal_open, final_header,
                    user_fname_class, user_mname_class, user_sname_class, user_bday_class, user_sexatbirth_class, user_placeofbirth_class,
                    user_bloodtype_class, user_phone_num_class, user_id_num_class, user_qao_team_id_class, user_position_class, user_email_class,
                    user_password_class, user_confirm_password_class, user_access_type_class, user_office_class]  

            # Update existing user record (include new fields)
            
            sqlcode = """
                UPDATE maindashboard.users
                SET
                    user_suffixname = %s,
                    user_livedname = %s,
                    user_bday = %s,
                    user_sexatbirth = %s,
                    user_placeofbirth = %s,
                    user_bloodtype = %s,
                    user_preferredpronouns = %s,
                    user_phone_num = %s, 
                    user_id_num = %s, 
                    user_position = %s,
                    user_email = %s, 
                    user_del_ind = %s
                WHERE 
                    user_id = %s
            """
            to_delete = bool(removerecord) 
            values = [suffixname, livedname, bday, sexatbirth, placeofbirth, bloodtype, preferredpronouns, phone_num, id_num, position, email, to_delete, userid]
            db.modifydatabase(sqlcode, values)
            final_modal_open = True
            if removerecord:
                final_header = "User Entry Successfully Removed"
            else:
                final_header = "User Entry Successfully Updated"

    elif eventid == 'registeruser_initialmodal_cancel' and cancelbtn:
        initial_modal_open = False
        initial_message = ''

    else:
        raise PreventUpdate
    return [alert_open, alert_color, alert_text, initial_modal_open, initial_message, confirm_btn_color, final_modal_open, final_header,
            user_fname_class, user_mname_class, user_sname_class, user_bday_class, user_sexatbirth_class, user_placeofbirth_class,
            user_bloodtype_class, user_phone_num_class, user_id_num_class, user_qao_team_id_class, user_position_class, user_email_class,
            user_password_class, user_confirm_password_class, user_access_type_class, user_office_class]  

# Callback to load profile data in edit mode
@app.callback(
    [
        Output('user_fname', 'value'),
        Output('user_mname', 'value'),
        Output('user_sname', 'value'),
        Output('user_suffixname', 'value'),
        Output('user_livedname', 'value'),
        Output('user_bday', 'value'),
        Output('user_sexatbirth', 'value'),
        Output('user_placeofbirth', 'value'),
        Output('user_bloodtype', 'value'),
        Output('user_preferredpronouns', 'value'),
        Output('user_phone_num', 'value'),
        Output('user_id_num', 'value'),
        Output('user_office_id', 'value'),
        Output('user_qao_team_id', 'value'),
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
                u.user_fname, u.user_mname, u.user_sname, u.user_suffixname,
                u.user_livedname, u.user_bday, u.user_sexatbirth, u.user_placeofbirth, u.user_bloodtype, u.user_preferredpronouns, u.user_phone_num,  
                u.user_id_num, u.user_office, u.user_qao_team_id,
                u.user_position, u.user_email, u.user_access_type
            FROM maindashboard.users u
            LEFT JOIN maindashboard.qao_teams q ON u.user_qao_team_id = q.qao_team_id
            WHERE user_id = %s
        """
        values = [userid]
        cols = [
            'fname', 'mname', 'sname', 'suffixname', 'lname', 
            'bday', 'sexatbirth', 'placeofbirth', 'bloodtype', 'preferredpronouns', 'phone', 'id_num', 'officeid', 'user_qao_team_id', 'position',  
            'email', 'access_type'
        ]
        df = db.querydatafromdatabase(sql, values, cols)

        fname = df['fname'][0]
        mname = df['mname'][0]
        sname = df['sname'][0]
        suffixname = df['suffixname'][0]
        lname = df['lname'][0]
        bday = df['bday'][0]
        sexatbirth = df['sexatbirth'][0]
        placeofbirth = df['placeofbirth'][0]
        bloodtype = df['bloodtype'][0]
        preferredpronouns = df['preferredpronouns'][0]
        phone = df['phone'][0]
        id_num = df['id_num'][0]
        officeid = df['officeid'][0]
        user_qao_team_id = df['user_qao_team_id'][0]
        position = df['position'][0]
        email = df['email'][0]  
        access_type = df['access_type'][0]

        return [fname, mname, sname, suffixname, lname, bday, sexatbirth, placeofbirth, bloodtype, preferredpronouns,
                phone, id_num, officeid, user_qao_team_id, position, email, access_type]
    else:
        raise PreventUpdate


# Callback to disable inputs in edit mode 
@app.callback(
    [
        Output('user_fname', 'disabled'),
        Output('user_mname', 'disabled'),
        Output('user_sname', 'disabled'),
        Output('user_suffixname', 'disabled'),
        Output('user_sexatbirth', 'disabled'),
        Output('user_office_id', 'disabled'),
        Output('user_qao_team_id', 'disabled'),
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
            return [True] * 10  # Disable all inputs in edit mode
    return [False] * 10  # Enable all inputs otherwise
