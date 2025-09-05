import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, no_update
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd
from pandas import isna

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

from urllib.parse import urlparse, parse_qs



form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Surname ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_sname", type="text"),
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_fname",type="text"),
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_mname",type="text"),
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_upmail",type="text"),
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='unithead_cluster_id',
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='unithead_college_id',
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='unithead_deg_unit_id',
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
                        "Faculty Rank/Position",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='unithead_fac_posn_name',
                        placeholder="Select Position",
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(id="unithead_fac_posn_number", type="text", placeholder="Number"),
                    width=2,
                ),
            ],
            className="mb-2",
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
                    dbc.Input(id="add_unithead_fac_posn", type="text", placeholder="Faculty position not in list?"),
                    width=6,
                ),
                dbc.Col(
                    dbc.Button("+", color="primary",  id="add_facposn_save_button", n_clicks=0),
                        width="auto"
                    ),     
            ],
            className="mb-2",
        ),
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Official Designation",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_desig",type="text"),
                    width=5,
                ),
            ],
            className="mb-2",
        ), 
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Start of Appointment",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='unithead_appointment_start'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "End of Appointment",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='unithead_appointment_end'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Dietary Restrictions", width=4),
                dbc.Col(
                    dbc.Input(id="unithead_dr", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Health Concerns / Medical Conditions", width=4),
                dbc.Col(
                    dbc.Input(id="unithead_hc", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Mobility and Accessibility Needs", width=4),
                dbc.Col(
                    dbc.Input(id="unithead_mn", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Shirt Size", width=4),
                dbc.Col(
                    dbc.Input(id="unithead_ss", type="text"),
                    width=6,
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
                                dcc.Store(id='unithead_toload', storage_type='memory', data=0),
                            ]
                        ),

                        html.H1("ADD NEW ACADEMIC HEAD PROFILE"),
                        html.Hr(),
                        dbc.Alert(id='unithead_alert', is_open=False), # For feedback purpose 
                        form, 
                        
                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='unithead_removerecord',
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
                            id='unithead_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary", id="unithead_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="unithead_cancel_button", n_clicks=0, href="/acad_heads_directory"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='unithead_confirmation_modal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="unithead_confirmation_modal_cancel", color="warning"),
                                            dbc.Button("Confirm", id="unithead_confirmation_modal_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='unithead_confirmation_modal',
                            backdrop=True,   
                            className="modal-success"    
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id="unithead_final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Click Proceed to continue.")),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        href="/acad_heads_directory",
                                        color="success", 
                                    ),
                                ),
                            ],
                            centered=True,
                            id='unithead_final_modal',
                            backdrop='static',
                            keyboard=False,
                        ),  
                        
                        dbc.Modal(
                            [
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['Faculty Position added successfully.'
                                    ],id='add_facposn_feedback_message'
                                ), 
                                
                            ],
                            centered=True,
                            id='add_facposn_successmodal',
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





# CU dropdown
@app.callback(
    Output('unithead_fac_posn_name', 'options'),
    Input('url', 'pathname')
)
def populate_fac_posn_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/acadheads_profile':
        sql = """
        SELECT fac_posn_name as label, fac_posn_name  as value
        FROM public.fac_posns
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        unithead_fac_posn_types = df.to_dict('records')
        return unithead_fac_posn_types
    else:
        raise PreventUpdate




# College dropdown
@app.callback(
    Output('unithead_college_id', 'options'),
    Input('unithead_cluster_id', 'value')
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
        
        unithead_college_options = df.to_dict('records')
        return unithead_college_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 

# Dept dropdown
@app.callback(
    Output('unithead_deg_unit_id', 'options'), 
    Input('unithead_college_id', 'value')
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

    

# Cluster dropdown
@app.callback(
    [
        Output('unithead_cluster_id', 'options'),
        Output('unithead_toload', 'data'),
        Output('unithead_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)

def unithead_loaddropdown(pathname, search):
    if pathname == '/acadheads_profile':
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
        Output('unithead_alert', 'color'),
        Output('unithead_alert', 'children'),
        Output('unithead_alert', 'is_open'),
        Output('unithead_confirmation_modal', 'is_open'),
        Output('unithead_confirmation_modal_message', 'children'),
        Output('unithead_final_modal', 'is_open'),
        Output('unithead_final_modal_header', 'children'),
        Output('unithead_confirmation_modal_confirm', 'color'),

    ],
    [
        Input('unithead_save_button', 'n_clicks'),
        Input('unithead_confirmation_modal_cancel', 'n_clicks'),
        Input('unithead_confirmation_modal_confirm', 'n_clicks'),
        Input('unithead_removerecord', 'value')
    ],
    [
        State('unithead_fname', 'value'),
        State('unithead_mname', 'value'),
        State('unithead_sname', 'value'),
        State('unithead_upmail', 'value'),
        State('unithead_fac_posn_name', 'value'),
        State('unithead_fac_posn_number', 'value'),
        State('unithead_desig', 'value'),    
        State('unithead_appointment_start', 'value'),
        State('unithead_appointment_end', 'value'),  
        State('unithead_cluster_id', 'value'),      
        State('unithead_college_id', 'value'), 
        State('unithead_deg_unit_id', 'value'),
        State('unithead_dr', 'value'),
        State('unithead_hc', 'value'),
        State('unithead_mn', 'value'),
        State('unithead_ss', 'value'),
        State('url', 'search')        
    ]
)
 
def record_acadhead_profile(submitbtn, cancel, confirm, removerecord,
                            unithead_fname, unithead_mname, 
                            unithead_sname, unithead_upmail,
                            unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                            unithead_appointment_start, unithead_appointment_end, 
                            unithead_cluster_id, unithead_college_id, unithead_deg_unit_id, 
                            unithead_dr, unithead_hc, unithead_mn, unithead_ss,
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
        if eventid == 'unithead_save_button' and submitbtn:
            if not all([unithead_sname, unithead_fname, unithead_mname, unithead_upmail, unithead_cluster_id, unithead_college_id,
                        unithead_deg_unit_id, unithead_fac_posn_name]) and not removerecord:
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please fill in required fields.'
                alert_open = True
                return [alert_color, alert_text, alert_open, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_button_color]
            else:
                if create_mode == 'add':
                        confirmation_modal_open = True
                        confirmation_modal_message = "Are you sure you want to create this Academic Head profile?"
                        confirm_button_color = "success"
                elif create_mode == 'edit':
                    confirmation_modal_open = True
                    confirmation_modal_message = "Are you sure you want to update this Academic Head profile?"
                    confirm_button_color = "success"
                    if removerecord:
                        confirmation_modal_message = "Are you sure you want to delete this Academic Head profile?"
                        confirm_button_color = 'danger'
               
        elif eventid == 'unithead_confirmation_modal_confirm' and confirm:
            if create_mode == 'add':
                unithead_appointment_start = unithead_appointment_start or None
                unithead_appointment_end   = unithead_appointment_end   or None
     
                sql = """
                    INSERT INTO iqateam.acad_unitheads (
                        unithead_fname, unithead_mname, unithead_sname, unithead_upmail,
                        unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                        unithead_appointment_start, unithead_appointment_end, unithead_cluster_id, 
                        unithead_college_id, unithead_deg_unit_id, 
                        unithead_dr, unithead_hc, unithead_mn, unithead_ss,
                        unithead_del_ind
                    )
                    VALUES (%s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s, %s, 
                            %s)
                """

                values = (unithead_fname, unithead_mname, 
                        unithead_sname, unithead_upmail,
                        unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                        
                        unithead_appointment_start, unithead_appointment_end, 
                        unithead_cluster_id, unithead_college_id, unithead_deg_unit_id, 
                        unithead_dr, unithead_hc, unithead_mn, unithead_ss, False
                )

                db.modifydatabase(sql, values) 
                final_modal_open = True
                final_modal_header = "Academic head profile created successfully."
                
            elif create_mode == 'edit':
                # Update existing user record
                unitheadid = parse_qs(parsed.query).get('id', [None])[0]
                
                if unitheadid is None:
                    raise PreventUpdate
                
                unithead_appointment_start = unithead_appointment_start or None
                unithead_appointment_end   = unithead_appointment_end   or None

                sqlcode = """
                    UPDATE iqateam.acad_unitheads
                    SET
                        unithead_fname = %s,
                        unithead_mname = %s,
                        unithead_sname = %s,                    
                        unithead_upmail = %s,
                        unithead_cluster_id = %s, 
                        unithead_college_id = %s, 
                        unithead_deg_unit_id = %s,
                        unithead_fac_posn_name = %s,
                        unithead_fac_posn_number = %s, 
                        unithead_desig = %s, 
                        unithead_appointment_start = %s,
                        unithead_appointment_end = %s,
                        unithead_dr = %s,
                        unithead_hc = %s,
                        unithead_mn = %s,
                        unithead_ss = %s,
                        unithead_del_ind = %s
                    WHERE 
                    
                        unithead_id = %s
                """
                to_delete = bool(removerecord) 
                
                values = [
                         unithead_fname, unithead_mname, 
                         unithead_sname, 
                         unithead_upmail,  unithead_cluster_id, unithead_college_id, unithead_deg_unit_id, unithead_fac_posn_name, 
                          unithead_fac_posn_number, unithead_desig, 
                          unithead_appointment_start,
                          unithead_appointment_end, 
                          unithead_dr, unithead_hc, unithead_mn, unithead_ss, 
                          to_delete, unitheadid]
                db.modifydatabase(sqlcode, values)

                final_modal_open = True
                final_modal_header = "Academic Head Profile Updated."
        elif eventid == 'unithead_confirmation_modal_cancel' and cancel:
            confirmation_modal_open = False
            confirmation_modal_message = ''

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    
    return [alert_color, alert_text, alert_open, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_button_color]  
 

@app.callback(
    [
        Output('unithead_fname', 'value'),
        Output('unithead_mname', 'value'),
        Output('unithead_sname', 'value'),
        Output('unithead_upmail', 'value'),
        Output('unithead_cluster_id', 'value'),      
        Output('unithead_college_id', 'value'), 
        Output('unithead_deg_unit_id', 'value'),
        Output('unithead_fac_posn_name', 'value'),
        Output('unithead_fac_posn_number', 'value'),
        Output('unithead_desig', 'value'),    
        Output('unithead_appointment_start', 'value'),
        Output('unithead_appointment_end', 'value'),  
        Output('unithead_dr', 'value'),
        Output('unithead_hc', 'value'),
        Output('unithead_mn', 'value'),
        Output('unithead_ss', 'value'),
       
    ],
    [  
        Input('unithead_toload', 'modified_timestamp')
    ],
    [
        State('unithead_toload', 'data'),
        State('url', 'search')
    ]
)
def unithead_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        unitheadid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                unithead_fname, unithead_mname, unithead_sname, unithead_upmail,
                unithead_cluster_id, unithead_college_id, unithead_deg_unit_id,
                unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                unithead_appointment_start, unithead_appointment_end,
                unithead_dr, unithead_hc, unithead_mn, unithead_ss
                
            FROM iqateam.acad_unitheads
            WHERE unithead_id = %s
        """
        values = [unitheadid]

        cols = [
            'unithead_fname', 'unithead_mname', 'unithead_sname', 'unithead_upmail',
            'unithead_cluster_id', 'unithead_college_id', 'unithead_deg_unit_id',
            'unithead_fac_posn_name', 'unithead_fac_posn_number', 'unithead_desig', 
            'unithead_appointment_start', 'unithead_appointment_end',
            'unithead_dr', 'unithead_hc', 'unithead_mn', 'unithead_ss'
            
        ]

         
        df = db.querydatafromdatabase(sql, values, cols)

        
        unithead_fname = df['unithead_fname'][0]
        unithead_mname = df['unithead_mname'][0]
        unithead_sname = df['unithead_sname'][0]
        unithead_upmail = df['unithead_upmail'][0]
        unithead_cluster_id = int(df['unithead_cluster_id'][0])
        unithead_college_id = df['unithead_college_id'][0]
        unithead_deg_unit_id = df['unithead_deg_unit_id'][0]
        unithead_fac_posn_name = df['unithead_fac_posn_name'][0]
        unithead_fac_posn_number = df['unithead_fac_posn_number'][0]
        unithead_desig = df['unithead_desig'][0]
        unithead_appointment_start = df['unithead_appointment_start'][0]
        unithead_appointment_end = df['unithead_appointment_end'][0]
        unithead_dr = df['unithead_dr'][0]
        unithead_hc = df['unithead_hc'][0]
        unithead_mn = df['unithead_mn'][0]
        unithead_ss = df['unithead_ss'][0]
        
        
        raw_start = df['unithead_appointment_start'][0]
        raw_end   = df['unithead_appointment_end'][0]

        # Convert pandas NaT to empty string so the date input is blank
        if pd.isna(raw_start):
            start_val = ''
        else:
            start_val = raw_start.strftime('%Y-%m-%d')

        if pd.isna(raw_end):
            end_val = ''
        else:
            end_val = raw_end.strftime('%Y-%m-%d')

        
        return [unithead_fname, unithead_mname, unithead_sname, unithead_upmail, 
                unithead_cluster_id, unithead_college_id, unithead_deg_unit_id,
                unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig,
                unithead_appointment_start, unithead_appointment_end,
                unithead_dr, unithead_hc, unithead_mn, unithead_ss
                ]
    
    else:
        raise PreventUpdate
    

# @app.callback(
#     [
#         Output('unithead_fname', 'disabled'),
#         Output('unithead_mname', 'disabled'),
#         Output('unithead_sname', 'disabled'),
#         # Output('unithead_cluster_id', 'disabled'),      
#         # Output('unithead_college_id', 'disabled'), 
#         # Output('unithead_deg_unit_id', 'disabled'),  
#         # Output('add_unithead_fac_posn', 'disabled'),  
#         # Output('unithead_appointment_start', 'disabled'),
#     ],
#     [Input('url', 'search')]
# )
# def unithead_inputs_disabled(search):
#     if search:
#         parsed = urlparse(search)
#         create_mode = parse_qs(parsed.query).get('mode', [None])[0]
#         if create_mode == 'edit':
#             return [True] * 3  # Disable all inputs in edit mode
#     return [False] * 3  # Enable all inputs otherwise



@app.callback(
    [Output('add_facposn_successmodal', 'is_open')],
    [Input('add_facposn_save_button', 'n_clicks')],
    [State('add_unithead_fac_posn', 'value'), 
     State('url', 'search')]
)
 
def register_facposn_unithead(submitbtn, add_unithead_fac_posn, search):
    if submitbtn:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]

        if create_mode == 'add' and add_unithead_fac_posn:
            sql = """
                INSERT INTO public.fac_posns (fac_posn_name)
                VALUES (%s)
            """
            values = (add_unithead_fac_posn,)
            db.modifydatabase(sql, values)
            return [True]  
    raise PreventUpdate
