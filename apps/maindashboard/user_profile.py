import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

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
        Output('userprof_id_num', 'value'),
        Output('userprof_livedname', 'value'),
        Output('userprof_bday', 'value'),
        Output('userprof_phone_num', 'value'),
        Output('userprof_office', 'value'),
        Output('userprof_position', 'value'),
        Output('userprof_email', 'value'),
    ], 
    [Input('url', 'pathname')],
    [State('currentuserid', 'data')]
)

def update_profile_header(pathname, current_userid):
    user_info = db.get_user_info(current_userid)

    if user_info: 
        user_fname = user_info.get('user_fname', '')
        user_mname = user_info.get('user_mname', '')
        user_sname = user_info.get('user_sname', '')
        user_livedname = user_info.get('user_livedname', '')
        user_id_num = user_info.get('user_id_num', '')
        user_bday = user_info.get('user_bday', '')
        user_phone_num = user_info.get('user_phone_num', '')
        user_office_id = user_info.get('user_office', '')  # Retrieve office ID
        user_position = user_info.get('user_position', '')
        user_email = user_info.get('user_email', '')

        # Retrieve office name based on office ID
        user_office_name = db.get_office_info(user_office_id)

        # Concatenate full name
        fullname_parts = [part for part in [user_fname, user_sname] if part]  # Include only non-empty parts
        if user_livedname:
            fullname_parts.append('"' + user_livedname + '"')
        fullname = " ".join(fullname_parts)

        return (
            fullname, user_id_num, user_fname, user_mname, user_sname,
            user_id_num, user_livedname, user_bday, user_phone_num,
            user_office_name, user_position, user_email
        )
    else:
        return "", "", "", "", "", "", "", "", "", "", "", ""
  
@app.callback(
    Output('userprof_successmodal', 'is_open'),
    Output('userprof_feedback_message', 'children'),
    [Input('userprof_save_button', 'n_clicks')],
    [   
        State('currentuserid', 'data'),
        State('userprof_fname', 'value'),
        State('userprof_mname', 'value'),
        State('userprof_sname', 'value'),
        State('userprof_id_num', 'value'),
        State('userprof_livedname', 'value'),
        State('userprof_bday', 'value'),
        State('userprof_phone_num', 'value'), 
        State('userprof_position', 'value'),
        State('userprof_email', 'value')
    ]
)
def save_profile_changes(n_clicks, current_userid, fname, mname, sname, id_num, livedname, bday, phone_num, position, email):
    if n_clicks > 0:
        # Save the updated values to the database
        sql = """
        UPDATE maindashboard.users
        SET user_fname = %s, user_mname = %s, user_sname = %s, user_id_num = %s,
            user_livedname = %s, user_bday = %s, user_phone_num = %s,
            user_position = %s, user_email = %s
        WHERE user_id = %s
        """
        values = (fname, mname, sname, id_num, livedname, bday, phone_num, position, email, current_userid)
        db.modifydatabase(sql, values)
        return True, "Changes saved."
    return False, ""




form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                        "First Name ",
                        
                    ],
                    width=4),
                dbc.Col(dbc.Input(type="text", id='userprof_fname'), width=8),
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
                dbc.Col(dbc.Input(type="text", id='userprof_mname'), width=8),
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
                dbc.Col(dbc.Input(type="text", id='userprof_sname' ), width=8),
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
                dbc.Col(dbc.Input(type="text", id='userprof_id_num' ), width=8),
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
                dbc.Col(dbc.Input(type="text", id='userprof_livedname' ), width=8),
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
                    width=4),
                dbc.Col(
                    dbc.Input(
                        type="text", id='userprof_phone_num', placeholder="0000-00-00000"
                    ),
                    width=8,
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
                dbc.Col(dbc.Input(type="text" , id='userprof_office', disabled=True ), width=8),
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
                dbc.Col(dbc.Input(type="text" , id='userprof_position' ), width=8),
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
                dbc.Col(dbc.Input(type="text", id='userprof_email'), width=8),
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
                    profile_header,  
                    html.Hr(),
                    
                    html.Br(), 
                    form,  
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
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['Changes saved.'
                                    ],id='userprof_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='homepage', id='userprof_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='userprof_successmodal',
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
