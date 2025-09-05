import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db
 
import json  
from urllib.parse import urlparse, parse_qs


form = dbc.Form(
    [
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree Program Title",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                
                dbc.Col(
                    dbc.Input(id="pro_degree_title", type="text", placeholder= "Bachelor of Science in Industrial Engineering"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree Program Shortname ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                
                dbc.Col(
                    dbc.Input(id="pro_degree_shortname", type="text", placeholder= "BS Industrial Engineering"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree Program Initials ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                
                dbc.Col(
                    dbc.Input(id="pro_degree_initials", type="text", placeholder= "BS IE"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Academic Cluster ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='pro_cluster_id', 
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
                        "College ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='pro_college_id', 
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
                        "Institute/ Department ",
                        html.Span("", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='pro_department_id', 
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
                        "Degree Program Type ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='pro_program_type_id', 
                    ),
                    width=4,
                ),
                 
            ],
            className="mb-2",
        ), 
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Academic Calendar Type ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='pro_calendar_type_id', 
                        options=[
                            {"label": "Semester", "value": "1"},
                            {"label": "Trimester", "value": "2"},
                            
                        ],
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),  

        html.Br(),
        html.Br(),
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
                                dcc.Store(id='pro_toload', storage_type='memory', data=0),
                            ]
                        ),

                        html.H1("ADD NEW PROGRAM"),
                        html.Hr(),
                        dbc.Alert(id='pro_alert', is_open=False), # For feedback purpose
                        form, 
                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='pro_removerecord',
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
                            id='pro_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="pro_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="pro_cancel_button", n_clicks=0, href="/program_list"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),

                        

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='pro_confirmation_modal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="pro_confirmation_modal_cancel", color="warning"),
                                            dbc.Button("Confirm", id="pro_confirmation_modal_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='pro_confirmation_modal',
                            backdrop=True,   
                            className="modal-success"    
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id="pro_final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Click Proceed to continue.")),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        href="/program_list",
                                        color="success", 
                                    ),
                                ),
                            ],
                            centered=True,
                            id='pro_final_modal',
                            backdrop='static',
                            keyboard=False,
                        ),  
                        
                    ], width=8, style={'marginLeft': '15px'}
                ),   
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
        )
    ]
)





# Cluster dropdown
@app.callback(
    [
        Output('pro_cluster_id', 'options'),
        Output('pro_toload', 'data'),
        Output('pro_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)

def populate_cluster_dropdown(pathname, search):
    if pathname == '/program_details':
        sql = """
            SELECT cluster_name as label, cluster_id  as value
            FROM public.clusters 
            WHERE cluster_del_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        cluster_options = df.to_dict('records')
        
        
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [cluster_options, to_load, removediv_style]






# College dropdown
@app.callback(
    Output('pro_college_id', 'options'),
    Input('pro_cluster_id', 'value')
)
def populate_college_dropdown(selected_cluster):
    if selected_cluster is None:
        return []   
    
    try:  
        sql = """
        SELECT college_name as label,  college_id  as value
        FROM public.college
        WHERE cluster_id = %s
        """
        values = [selected_cluster]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        pro_college_options = df.to_dict('records')
        return pro_college_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 











# Degree Unit dropdown
@app.callback(
    Output('pro_department_id', 'options'),
    Input('pro_college_id', 'value')
)
def populate_dgu_dropdown(selected_college):
    if selected_college is None:
        return []   
    
    try:
        # Query to fetch degree units based on the selected college
        sql = """
        SELECT deg_unit_name as label,  deg_unit_id  as value
        FROM public.deg_unit
        WHERE college_id = %s
        """
        values = [selected_college]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        pro_dgu_options = df.to_dict('records')
        return pro_dgu_options
    except Exception as e:
        # Log the error or handle it appropriately
        return []
    

#Program type dropdown
@app.callback(
    Output('pro_program_type_id', 'options'),
    Input('url', 'pathname')
)
def populate_programtype_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/program_details':
        sql = """
        SELECT programtype_name  as label, programtype_id as value
        FROM eqateam.program_type
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        pro_programtype_types = df.to_dict('records')
        return pro_programtype_types
    else:
        raise PreventUpdate



 


@app.callback(
    [
        Output('pro_alert', 'color'),
        Output('pro_alert', 'children'),
        Output('pro_alert', 'is_open'),
        Output('pro_confirmation_modal', 'is_open'),
        Output('pro_confirmation_modal_message', 'children'),
        Output('pro_final_modal', 'is_open'),
        Output('pro_final_modal_header', 'children'),
        Output('pro_confirmation_modal_confirm', 'color'),

    ],
    [
        Input('pro_save_button', 'n_clicks'),
        Input('pro_confirmation_modal_cancel', 'n_clicks'),
        Input('pro_confirmation_modal_confirm', 'n_clicks'),
        Input('pro_removerecord', 'value')
    ],
    [
        State('pro_degree_title', 'value'),
        State('pro_degree_shortname', 'value'),
        State('pro_degree_initials', 'value'),
        State('pro_cluster_id', 'value'),
        State('pro_college_id', 'value'),
        State('pro_department_id', 'value'),
        State('pro_program_type_id', 'value'),
        State('pro_calendar_type_id', 'value'),
        State('url', 'search')        
    ]
)

def record_program_details(submitbtn, cancel, confirm, removerecord,
                            pro_degree_title, pro_degree_shortname, pro_degree_initials,
                            pro_cluster_id, pro_college_id, pro_department_id,
                            pro_program_type_id, pro_calendar_type_id,
                            search):
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate  # No input has triggered the callback
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    alert_color = 'danger'
    alert_text = ''
    alert_open = False
    confirmation_modal_open = False
    confirmation_modal_message = ''
    final_modal_open = False
    final_modal_header = ''
    confirm_color = 'success'

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    if eventid == 'pro_save_button' and submitbtn:
        if not all([pro_degree_title, pro_degree_shortname, pro_degree_initials]):
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            return [alert_color, alert_text, True, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color]
        else:
            if create_mode == 'add':
                confirmation_modal_open = True
                confirmation_modal_message = "Are you sure you want to add this new program?"
                confirm_color = 'success'
            elif create_mode == 'edit':
                confirmation_modal_open = True
                confirmation_modal_message = "Are you sure you want to update this program?"
                if removerecord:
                    confirmation_modal_message = "Are you sure you want to mark this program for deletion?"
                    confirm_color = 'danger'
    
    elif eventid == 'pro_confirmation_modal_confirm' and confirm:
        if create_mode == 'add':
            # Check existing records in the database
            check_existing_title_sql = """
                SELECT 1 
                FROM eqateam.program_details 
                WHERE pro_degree_title = %s AND pro_del_ind = False
            """
            existing_title = db.querydatafromdatabase(check_existing_title_sql, (pro_degree_title,), ["exists"])

            if not existing_title.empty:
                alert_text = 'Degree Program Title already exists. Please use a different title.'
                return ['danger', alert_text, True, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color]

            check_existing_shortname_sql = """
                SELECT 1 
                FROM eqateam.program_details 
                WHERE pro_degree_shortname = %s AND pro_del_ind = False
            """
            existing_shortname = db.querydatafromdatabase(check_existing_shortname_sql, (pro_degree_shortname,), ["exists"])

            if not existing_shortname.empty:
                alert_text = 'Degree Program Shortname already exists. Please use a different shortname.'
                return ['danger', alert_text, True, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color]

            check_existing_initials_sql = """
                SELECT 1 
                FROM eqateam.program_details 
                WHERE pro_degree_initials = %s AND pro_del_ind = False
            """
            existing_initials = db.querydatafromdatabase(check_existing_initials_sql, (pro_degree_initials,), ["exists"])

            if not existing_initials.empty:
                alert_text = 'Degree Program Initials already exists. Please use different initials.'
                return ['danger', alert_text, True, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color]

            sql = """
                INSERT INTO eqateam.program_details (
                    pro_degree_title, pro_degree_shortname, pro_degree_initials, 
                    pro_cluster_id, pro_college_id, pro_department_id,
                    pro_program_type_id, pro_calendar_type_id, 
                    pro_del_ind
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                pro_degree_title, pro_degree_shortname, pro_degree_initials,
                pro_cluster_id, pro_college_id, pro_department_id,
                pro_program_type_id, pro_calendar_type_id, 
                False
            )

            db.modifydatabase(sql, values) 
            final_modal_open = True
            final_modal_header = "New program added successfully."
                
        elif create_mode == 'edit':
            # Update existing user record
            programdetailsid = parse_qs(parsed.query).get('id', [None])[0]
                
            if not all([pro_degree_title, pro_degree_shortname, pro_degree_initials]):
                return [alert_color, "Missing required fields.",  True, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color]

            if programdetailsid is None:
                raise PreventUpdate
                
            sqlcode = """
                UPDATE eqateam.program_details
                SET
                    pro_degree_title = %s,
                    pro_degree_shortname = %s,
                    pro_degree_initials = %s,
                    pro_cluster_id = %s,
                    pro_college_id = %s,
                    pro_department_id = %s,
                    pro_program_type_id = %s,
                    pro_calendar_type_id = %s,
                    pro_del_ind = %s
                WHERE 
                    programdetails_id = %s
            """  
            to_delete = bool(removerecord) 
                
            values = [
                pro_degree_title,
                pro_degree_shortname,
                pro_degree_initials,
                pro_cluster_id,
                pro_college_id,
                pro_department_id,
                pro_program_type_id,
                pro_calendar_type_id,
                to_delete,
                programdetailsid
            ]
            db.modifydatabase(sqlcode, values)
            final_modal_open = True
            final_modal_header = "Program updated successfully."
    
        else:
            raise PreventUpdate
    elif eventid == 'pro_confirmation_modal_cancel' and cancel:
        # Close the confirmation modal without any action
        confirmation_modal_open = False
        confirmation_modal_message = ""
    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color] 

  


# Helper function for setting alerts
def set_alert(message, color):
    return [color, message, True, False]







@app.callback(
    [Output('newaccred_successmodal', 'is_open')],
    [Input('add_button', 'n_clicks')],
    [State('new_accreditation_body_id', 'value')]
)
def new_accreditation_details(addbtn, new_accreditation_body_id):
    if not addbtn or not new_accreditation_body_id:
        raise PreventUpdate  # Don't update if there's no click or no input
    
    modal_open = False

    try:
        sql = """
            INSERT INTO public.accreditation_body (
                body_name
            )
            VALUES (%s)
        """
        values = (new_accreditation_body_id,)
        db.modifydatabase(sql, values)  # Function to execute the SQL and commit changes
        modal_open = True  # Open a success modal

    except Exception as e:
        # Handle error appropriately
        modal_open = False
 
    return [modal_open]


 
@app.callback(
    [
        Output('pro_degree_title', 'value'),
        Output('pro_degree_shortname', 'value'),
        Output('pro_degree_initials', 'value'),
        Output('pro_cluster_id', 'value'),
        Output('pro_college_id', 'value'),
        Output('pro_department_id', 'value'),
        Output('pro_program_type_id', 'value'),
        Output('pro_calendar_type_id', 'value'),
       
    ],
    [  
        Input('pro_toload', 'modified_timestamp')
    ],
    [
        State('pro_toload', 'data'),
        State('url', 'search')
    ]
)


def pro_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        programdetailsid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                pro_degree_title, pro_degree_shortname, pro_degree_initials,
                pro_cluster_id, pro_college_id, pro_department_id,
                pro_program_type_id, pro_calendar_type_id
                
            FROM eqateam.program_details
            WHERE programdetails_id = %s
        """
        values = [programdetailsid]

        cols = [
            'pro_degree_title', 'pro_degree_shortname', 'pro_degree_initials',
            'pro_cluster_id', 'pro_college_id', 'pro_department_id',
            'pro_program_type_id', 'pro_calendar_type_id',
        ]

        df = db.querydatafromdatabase(sql, values, cols)


        pro_degree_title = df['pro_degree_title'][0]
        pro_degree_shortname = df['pro_degree_shortname'][0]
        pro_degree_initials = df['pro_degree_initials'][0]
        pro_cluster_id = int(df['pro_cluster_id'][0])
        pro_college_id = int(df['pro_college_id'][0])
        pro_department_id = int(df['pro_department_id'][0])
        pro_program_type_id = int(df['pro_program_type_id'][0])
        pro_calendar_type_id = int(df['pro_calendar_type_id'][0])
        
        

        
        return [pro_degree_title, pro_degree_shortname, pro_degree_initials,
                pro_cluster_id, pro_college_id, pro_department_id,
                pro_program_type_id, pro_calendar_type_id
                ]
    
    else:
        raise PreventUpdate
   
