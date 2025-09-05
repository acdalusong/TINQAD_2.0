import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, no_update
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

from urllib.parse import urlparse, parse_qs


 
form = dbc.Form(
    [
        html.H5("PERSONAL INFORMATION", className="form-header fw-bold"),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Surname ", 
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(id="qaofficer_sname", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "First Name ", 
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(id="qaofficer_fname",type="text"),
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
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(id="qaofficer_mname",type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "UP Mail ", 
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(id="qaofficer_upmail",type="text"),
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
                        id='qaofficer_cluster_id',
                        placeholder="Select Academic Cluster",
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
                       "Main Unit ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='qaofficer_college_id',
                        placeholder="Select Main Unit",
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
                       "Sub-unit ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='qaofficer_deg_unit_id',
                        placeholder="Select Sub-unit",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                       "Faculty Rank/Position ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='qaofficer_fac_posn_name',
                        placeholder="Select Position",
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(id="qaofficer_fac_posn_number", type="text", placeholder="Number"),
                    width=2,
                ),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Add new Faculty Position", 
                    ],
                    width=4
                ),
                 
                dbc.Col(
                    dbc.Input(id="add_qaofficer_fac_posn", type="text",placeholder="Faculty position not in list?"),
                    width=6,
                ),
                dbc.Col(
                    dbc.Button("?", color="primary",  id="add_qaofficer_save_button", n_clicks=0),
                        width="auto"
                    ),     
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Faculty Admin Position (if any)", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_facadmin_posn", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Admin Staff/REPS Position", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_staff_posn", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        html.Br(),
         
        html.H5("QA INFORMATION", className="form-header fw-bold"),
         
        dbc.Row(
            [
                dbc.Label(
                    [
                       "QA Position in the CU ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='qaofficer_cuposition_id',
                        placeholder="Select Position",
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
                        "With Basic Paper as QAO ", 
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id="qaofficer_basicpaper",
                        options=[
                            {"label":"Yes","value":"Yes"},
                            {"label":"No","value":"No"}
                        ],
                        placeholder="Please select yes/no"
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
                        "Remarks ", 
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id="qaofficer_remarks",
                        options=[
                            {"label":"With record","value":"With record"},
                            {"label":"No record","value":"No record"},
                            {"label":"Dual Role","value":"Dual Role"},
                            {"label":"Renewed","value":"Renewed"},
                            {"label":"Replaced","value":"Replaced"},
                        ],
                        placeholder="Select a remark"
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
                        "ALC ", 
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(id="qaofficer_alc", type="text"),
                    width=3,
                ),
            ],
            className="mb-2",
        ),
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Start of Term ", 
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="date", id='qaofficer_appointment_start'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "End of Term ", 
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="date", id='qaofficer_appointment_end'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Role in the CU-Level QA Committee", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_role", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Dietary Restrictions", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_dr", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Health Concerns / Medical Conditions", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_hc", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Mobility and Accessibility Needs", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_mn", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Shirt Size", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_ss", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

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
                                dcc.Store(id='qaofficer_toload', storage_type='memory', data=0),
                            ]
                        ),

                        html.H1("ADD NEW QA OFFICER PROFILE"),
                        html.Hr(),
                        dbc.Alert(id='qaofficer_alert', is_open=False), # For feedback purpose
                        form,

                        html.Br(),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='qaofficer_removerecord',
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
                            id='qaofficer_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary", id="qaofficer_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="qaofficer_cancel_button", n_clicks=0, href="/qaofficers_directory"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='qaofficer_confirmation_modal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="qaofficer_confirmation_modal_cancel", color="warning"),
                                            dbc.Button("Confirm", id="qaofficer_confirmation_modal_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='qaofficer_confirmation_modal',
                            backdrop=True,   
                            className="modal-success"    
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id="qaofficer_final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Click Proceed to continue.")),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        href="/qaofficers_directory",
                                        color="success", 
                                    ),
                                ),
                            ],
                            centered=True,
                            id='qaofficer_final_modal',
                            backdrop='static',
                            keyboard=False,
                        ),  
                       
                        dbc.Modal(
                            [
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['Faculty Position added successfully.'
                                    ],id='add_qaofficer_feedback_message'
                                ), 
                                
                            ],
                            centered=True,
                            id='add_qaofficer_successmodal',
                            backdrop=True,   
                            className="modal-success"    
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
 




# Fac Posn dropdown
@app.callback(
    Output('qaofficer_fac_posn_name', 'options'),
    Input('url', 'pathname')
)
def populate_fac_posn_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/qaofficers_profile':
        sql = """
        SELECT fac_posn_name as label, fac_posn_name  as value
        FROM  public.fac_posns 
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qaofficer_fac_posns_types = df.to_dict('records')
        return qaofficer_fac_posns_types
    else:
        raise PreventUpdate




# College dropdown
@app.callback(
    Output('qaofficer_college_id', 'options'),
    Input('qaofficer_cluster_id', 'value')
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
        
        qaofficer_college_options = df.to_dict('records')
        return qaofficer_college_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 
    
# Degree Unit dropdown
@app.callback(
    Output('qaofficer_deg_unit_id', 'options'), 
    Input('qaofficer_college_id', 'value')
)
def populate_degree_unit_dropdown(selected_college):
    if selected_college is None:
        return []  # Return empty options if no college is selected
    
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
        
        dgu_options = df.to_dict('records')
        return dgu_options
    except Exception as e:
        # Log the error or handle it appropriately
        return []



# CU dropdown
@app.callback(
    Output('qaofficer_cuposition_id', 'options'),
    Input('url', 'pathname')
)
def populate_cuposition_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/qaofficers_profile':
        sql = """
        SELECT cuposition_name as label, cuposition_id  as value
        FROM qaofficers.cuposition
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qaofficer_cuposition_types = df.to_dict('records')
        return qaofficer_cuposition_types
    else:
        raise PreventUpdate



# Cluster dropdown
@app.callback(
    [
        Output('qaofficer_cluster_id', 'options'),
        Output('qaofficer_toload', 'data'),
        Output('qaofficer_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def qaofficer_loaddropdown(pathname, search):
    if pathname == '/qaofficers_profile':
        sql = """
            SELECT cluster_name as label, cluster_id  as value
            FROM public.clusters
            WHERE unit_type_id = 1 and cluster_del_ind = False
            
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

 
@app.callback(
    [
        Output('qaofficer_alert', 'color'),
        Output('qaofficer_alert', 'children'),
        Output('qaofficer_alert', 'is_open'),
        Output('qaofficer_confirmation_modal', 'is_open'),
        Output('qaofficer_confirmation_modal_message', 'children'),
        Output('qaofficer_final_modal', 'is_open'),
        Output('qaofficer_final_modal_header', 'children'),
        Output('qaofficer_confirmation_modal_confirm', 'color'),
    ],
    [
        Input('qaofficer_save_button', 'n_clicks'),
        Input('qaofficer_confirmation_modal_cancel', 'n_clicks'),
        Input('qaofficer_confirmation_modal_confirm', 'n_clicks'),
        Input('qaofficer_removerecord', 'value')
    ],
    [
        State('qaofficer_fname', 'value'),
        State('qaofficer_mname', 'value'),
        State('qaofficer_sname', 'value'),
        State('qaofficer_upmail', 'value'),

        State('qaofficer_fac_posn_name', 'value'),
        State('qaofficer_fac_posn_number', 'value'),
        State('qaofficer_facadmin_posn', 'value'),
        State('qaofficer_staff_posn', 'value'),


        State('qaofficer_cuposition_id', 'value'),
        State('qaofficer_basicpaper', 'value'),
        State('qaofficer_remarks', 'value'),   
        State('qaofficer_alc', 'value'),      
        State('qaofficer_appointment_start', 'value'),
        State('qaofficer_appointment_end', 'value'),  
        State('qaofficer_cluster_id', 'value'),      
        State('qaofficer_college_id', 'value'), 
        State('qaofficer_deg_unit_id', 'value'),
        State('qaofficer_role', 'value'),
        State('qaofficer_dr', 'value'),
        State('qaofficer_hc', 'value'),
        State('qaofficer_mn', 'value'),
        State('qaofficer_ss', 'value'),
        State('url', 'search')

    ]
)
 
def record_qaofficer_profile(submitbtn, cancel, confirm, removerecord,
                            qaofficer_fname, qaofficer_mname, 
                            qaofficer_sname, qaofficer_upmail,
                            qaofficer_fac_posn_name, qaofficer_fac_posn_number,
                            qaofficer_facadmin_posn, qaofficer_staff_posn,
                            qaofficer_cuposition_id, qaofficer_basicpaper, 
                            qaofficer_remarks, qaofficer_alc,
                            qaofficer_appointment_start, qaofficer_appointment_end, 
                            qaofficer_cluster_id, qaofficer_college_id, 
                            qaofficer_deg_unit_id, qaofficer_role,
                            qaofficer_dr, qaofficer_hc, qaofficer_mn, qaofficer_ss,
                            search):
    ctx = dash.callback_context 

    alert_color = ''
    alert_text = ''
    alert_open = False
    confirmation_modal_open = False
    confirmation_modal_message = ''
    final_modal_open = False
    final_modal_header = ''
    confirm_button_color = ''

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    if ctx.triggered:
        if eventid == 'qaofficer_save_button' and submitbtn:
            if not all([qaofficer_sname, qaofficer_fname, qaofficer_mname, qaofficer_upmail, qaofficer_cluster_id, qaofficer_college_id,
                        qaofficer_deg_unit_id, qaofficer_fac_posn_name,
                        qaofficer_fac_posn_number,
                        qaofficer_remarks]) and not removerecord:
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please fill in required fields.'
                alert_open = True
                return [alert_color, alert_text, alert_open, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_button_color]
            else:
                if create_mode == 'add':
                        confirmation_modal_open = True
                        confirmation_modal_message = "Are you sure you want to create this QA Officer profile?"
                        confirm_button_color = "success"
                elif create_mode == 'edit':
                    confirmation_modal_open = True
                    confirmation_modal_message = "Are you sure you want to update this QA Officer profile?"
                    confirm_button_color = "success"
                    if removerecord:
                        confirmation_modal_message = "Are you sure you want to delete this QA Officer profile?"
                        confirm_button_color = 'danger'

        elif eventid == 'qaofficer_confirmation_modal_confirm' and confirm:
            if create_mode == 'add':
                sql = """
                    INSERT INTO  qaofficers.qa_officer (
                        qaofficer_fname, qaofficer_mname, qaofficer_sname, qaofficer_upmail,
                        qaofficer_fac_posn_name, qaofficer_fac_posn_number, qaofficer_facadmin_posn, qaofficer_staff_posn,
                        qaofficer_cuposition_id, qaofficer_basicpaper, qaofficer_remarks, qaofficer_alc,
                        qaofficer_appointment_start, qaofficer_appointment_end, qaofficer_cluster_id, 
                        qaofficer_college_id, qaofficer_deg_unit_id, qaofficer_role, 
                        qaofficer_dr, qaofficer_hc, qaofficer_mn, qaofficer_ss,
                        qaofficer_del_ind
                    )
                    VALUES (%s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s, %s,
                            %s)
                
                """

                values = (qaofficer_fname, qaofficer_mname, 
                        qaofficer_sname, qaofficer_upmail,
                        qaofficer_fac_posn_name, qaofficer_fac_posn_number,
                        qaofficer_facadmin_posn, qaofficer_staff_posn,
                        qaofficer_cuposition_id, qaofficer_basicpaper, 
                        qaofficer_remarks, qaofficer_alc,
                        qaofficer_appointment_start, qaofficer_appointment_end, 
                        qaofficer_cluster_id, qaofficer_college_id, qaofficer_deg_unit_id,
                        qaofficer_role, qaofficer_dr, qaofficer_hc, qaofficer_mn, qaofficer_ss, 
                        False
                )

                db.modifydatabase(sql, values) 
                final_modal_open = True
                final_modal_header = "QA Officer profile created successfully."
            elif create_mode == 'edit':
                # Update existing user record
                qaofficerid = parse_qs(parsed.query).get('id', [None])[0]
                
                if qaofficerid is None:
                    raise PreventUpdate
                
                sqlcode = """
                    UPDATE qaofficers.qa_officer
                    SET
                        qaofficer_fname = %s,
                        qaofficer_mname = %s,
                        qaofficer_sname = %s,
                        qaofficer_upmail = %s,
                        qaofficer_cluster_id = %s, 
                        qaofficer_college_id = %s, 
                        qaofficer_deg_unit_id = %s,
                        qaofficer_fac_posn_name = %s,
                        qaofficer_fac_posn_number = %s,
                        qaofficer_facadmin_posn = %s, 
                        qaofficer_staff_posn = %s,
                        qaofficer_cuposition_id = %s,
                        qaofficer_remarks = %s,
                        qaofficer_appointment_start = %s,
                        qaofficer_appointment_end = %s,
                        qaofficer_dr = %s,
                        qaofficer_hc = %s,
                        qaofficer_mn = %s,
                        qaofficer_ss = %s,
                        qaofficer_del_ind = %s
                    WHERE
                        qaofficer_id = %s
                """

                to_delete = bool(removerecord) 
                values = [
                qaofficer_fname, qaofficer_mname, 
                qaofficer_sname,
                qaofficer_upmail, qaofficer_cluster_id, qaofficer_college_id, qaofficer_deg_unit_id,
                qaofficer_fac_posn_name, qaofficer_fac_posn_number, qaofficer_facadmin_posn, 
                qaofficer_staff_posn, qaofficer_cuposition_id,
                qaofficer_remarks, qaofficer_appointment_start,
                qaofficer_appointment_end, qaofficer_dr, qaofficer_hc, qaofficer_mn, qaofficer_ss,
                to_delete, qaofficerid
                ]

                db.modifydatabase(sqlcode, values)

                final_modal_open = True
                final_modal_header = "QA Officer Profile Updated."
        elif eventid == 'qaofficer_confirmation_modal_cancel' and cancel:
            confirmation_modal_open = False
            confirmation_modal_message = ''

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    
    return [alert_color, alert_text, alert_open, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_button_color]  

@app.callback(
    [
        Output('qaofficer_fname', 'value'),
        Output('qaofficer_mname', 'value'),
        Output('qaofficer_sname', 'value'),
        Output('qaofficer_upmail', 'value'),
        Output('qaofficer_fac_posn_name', 'value'),
        Output('qaofficer_fac_posn_number', 'value'),
        Output('qaofficer_facadmin_posn', 'value'),
        Output('qaofficer_staff_posn', 'value'),
        Output('qaofficer_cuposition_id', 'value'),
        Output('qaofficer_basicpaper', 'value'),
        Output('qaofficer_remarks', 'value'),   
        Output('qaofficer_alc', 'value'),      
        Output('qaofficer_appointment_start', 'value'),
        Output('qaofficer_appointment_end', 'value'),  
        Output('qaofficer_cluster_id', 'value'),      
        Output('qaofficer_college_id', 'value'), 
        Output('qaofficer_deg_unit_id', 'value'),
        Output('qaofficer_role', 'value'),
        Output('qaofficer_dr', 'value'),
        Output('qaofficer_hc', 'value'),
        Output('qaofficer_mn', 'value'),
        Output('qaofficer_ss', 'value'),
       
    ],
    [  
        Input('qaofficer_toload', 'modified_timestamp')
    ],
    [
        State('qaofficer_toload', 'data'),
        State('url', 'search')
    ]
)
def qaofficer_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        qaofficerid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                qaofficer_fname, qaofficer_mname, qaofficer_sname, qaofficer_upmail,
                qaofficer_fac_posn_name, qaofficer_fac_posn_number, qaofficer_facadmin_posn, qaofficer_staff_posn,
                qaofficer_cuposition_id, qaofficer_basicpaper, qaofficer_remarks, qaofficer_alc,
                qaofficer_appointment_start, qaofficer_appointment_end, qaofficer_cluster_id, 
                qaofficer_college_id, qaofficer_deg_unit_id, qaofficer_role,
                qaofficer_dr, qaofficer_hc, qaofficer_mn, qaofficer_ss
                
            FROM  qaofficers.qa_officer
            WHERE qaofficer_id = %s
        """
        values = [qaofficerid]

        cols = [
            'qaofficer_fname', 'qaofficer_mname', 'qaofficer_sname', 'qaofficer_upmail',
            'qaofficer_fac_posn_name', 'qaofficer_fac_posn_number', 'qaofficer_facadmin_posn', 'qaofficer_staff_posn',
            'qaofficer_cuposition_id', 'qaofficer_basicpaper', 'qaofficer_remarks', 'qaofficer_alc',
            'qaofficer_appointment_start', 'qaofficer_appointment_end', 'qaofficer_cluster_id', 
            'qaofficer_college_id', 'qaofficer_deg_unit_id', 'qaofficer_role', 
            'qaofficer_dr', 'qaofficer_hc', 'qaofficer_mn', 'qaofficer_ss'
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        qaofficer_fname = df['qaofficer_fname'][0]
        qaofficer_mname = df['qaofficer_mname'][0]
        qaofficer_sname = df['qaofficer_sname'][0]
        qaofficer_upmail = df['qaofficer_upmail'][0]
        qaofficer_fac_posn_name = df['qaofficer_fac_posn_name'][0]
        qaofficer_fac_posn_number = df['qaofficer_fac_posn_number'][0]
        qaofficer_facadmin_posn = df['qaofficer_facadmin_posn'][0]
        qaofficer_staff_posn = df['qaofficer_staff_posn'][0]
        qaofficer_cuposition_id = df['qaofficer_cuposition_id'][0]
        qaofficer_basicpaper = df['qaofficer_basicpaper'][0]
        qaofficer_remarks = df['qaofficer_remarks'][0]
        qaofficer_alc = df['qaofficer_alc'][0]
        qaofficer_appointment_start = df['qaofficer_appointment_start'][0]
        qaofficer_appointment_end = df['qaofficer_appointment_end'][0]
        qaofficer_cluster_id = int(df['qaofficer_cluster_id'][0])
        qaofficer_college_id = df['qaofficer_college_id'][0]
        qaofficer_deg_unit_id = df['qaofficer_deg_unit_id'][0]
        qaofficer_role = df['qaofficer_role'][0]
        qaofficer_dr = df['qaofficer_dr'][0]
        qaofficer_hc = df['qaofficer_hc'][0]
        qaofficer_mn = df['qaofficer_mn'][0]
        qaofficer_ss = df['qaofficer_ss'][0]


        return [qaofficer_fname, qaofficer_mname, qaofficer_sname, qaofficer_upmail,
                qaofficer_fac_posn_name, qaofficer_fac_posn_number, qaofficer_facadmin_posn, qaofficer_staff_posn,
                qaofficer_cuposition_id, qaofficer_basicpaper, qaofficer_remarks, qaofficer_alc,
                qaofficer_appointment_start, qaofficer_appointment_end, qaofficer_cluster_id, 
                qaofficer_college_id, qaofficer_deg_unit_id, qaofficer_role,  
                qaofficer_dr, qaofficer_hc, qaofficer_mn, qaofficer_ss
        ]
    
    else:
        raise PreventUpdate
  
    

# @app.callback(
#     [
#         Output('qaofficer_fname', 'disabled'),
#         Output('qaofficer_mname', 'disabled'),
#         Output('qaofficer_sname', 'disabled'),

#         # Output('qaofficer_cuposition_id', 'disabled'),
#         # Output('qaofficer_basicpaper', 'disabled'),
#         # Output('qaofficer_alc', 'disabled'),      
#         # Output('qaofficer_appointment_start', 'disabled'),

#         # Output('qaofficer_cluster_id', 'disabled'),      
#         # Output('qaofficer_college_id', 'disabled'), 
#         # Output('qaofficer_deg_unit_id', 'disabled'),
#         # Output('add_qaofficer_fac_posn', 'disabled'),
#         # Output('qaofficer_role', 'disabled'),
#     ],
#     [Input('url', 'search')]

# )      
# def qaofficer_inputs_disabled(search):
#     if search:
#         parsed = urlparse(search)
#         create_mode = parse_qs(parsed.query).get('mode', [None])[0]
#         if create_mode == 'edit':
#             return [True] * 3  # Disable all inputs in edit mode
#     return [False] * 3  # Enable all inputs otherwise


                

@app.callback(
    [Output('add_qaofficer_successmodal', 'is_open')],
    [Input('add_qaofficer_save_button', 'n_clicks')],
    [State('add_qaofficer_fac_posn', 'value'), 
     State('url', 'search')]
)
 
def register_qaofficer_qaofficer(submitbtn, add_qaofficer_fac_posn, search):
    if submitbtn:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]

        if create_mode == 'add' and add_qaofficer_fac_posn:
            sql = """
                INSERT INTO public.fac_posns (fac_posn_name)
                VALUES (%s)
            """
            values = (add_qaofficer_fac_posn,)
            db.modifydatabase(sql, values)
            return [True]  
    raise PreventUpdate
