import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State 
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
                        "Cluster ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='unithead_cluster_id',
                        placeholder="Select Cluster",
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='unithead_college_id',
                        placeholder="Select College",
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
                        "Department ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(
                        id='unithead_deg_unit', type="text"
                        #placeholder="Select Department",
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
                                    dbc.Button("Save", color="primary",  id="unithead_save_button", n_clicks=0),
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
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['Unit Head added successfully.'
                                    ],id='unithead_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='/acad_heads_directory', id='unithead_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='unithead_successmodal',
                            backdrop=True,   
                            className="modal-success"    
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


@app.callback(
    [
        Output('unithead_alert', 'color'),
        Output('unithead_alert', 'children'),
        Output('unithead_alert', 'is_open'),
        Output('unithead_successmodal', 'is_open'),
        Output('unithead_feedback_message', 'children'),
        Output('unithead_btn_modal', 'href')
    ],
    [
        Input('unithead_save_button', 'n_clicks'),
        Input('unithead_btn_modal', 'n_clicks'),
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
        State('unithead_deg_unit', 'value'),
        State('url', 'search')        
    ]
)
 
def record_acadhead_profile(submitbtn, closebtn, removerecord,
                            unithead_fname, unithead_mname, 
                            unithead_sname, unithead_upmail,
                            unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                            unithead_appointment_start, unithead_appointment_end, 
                            unithead_cluster_id, unithead_college_id, unithead_deg_unit, search):
    ctx = dash.callback_context 

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'unithead_save_button' and submitbtn:
        
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            parsed = urlparse(search)
            create_mode = parse_qs(parsed.query).get('mode', [None])[0]
            
            if create_mode == 'add':
                
                # Input validation
                if not unithead_sname:
                    alert_color_sname = 'danger'
                    alert_text_sname = 'Check your inputs. Please add a Surname.'
                    return [alert_color_sname, alert_text_sname, alert_open, modal_open]
                
                if not unithead_fname:
                    alert_color_fname = 'danger'
                    alert_text_fname = 'Check your inputs. Please add a First Name.'
                    return [alert_color_fname, alert_text_fname, alert_open, modal_open]

                if not unithead_mname:
                    alert_color_mname = 'danger'
                    alert_text_mname = 'Check your inputs. Please add a Middle Name.'
                    return [alert_color_mname, alert_text_mname, alert_open, modal_open]
 
                if not unithead_upmail:
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add a UP Mail.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not unithead_cluster_id :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please select a Cluster.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not unithead_college_id :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please select a College.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not unithead_deg_unit :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please select a Department.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not unithead_fac_posn_name :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add a Faculty Position.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not unithead_desig  :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add an Official Designation.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not unithead_appointment_start  :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add a start date.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                
                if not unithead_appointment_end  :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add a end date.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
     
                sql = """
                    INSERT INTO iqateam.acad_unitheads (
                        unithead_fname, unithead_mname, unithead_sname, unithead_upmail,
                        unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                        unithead_appointment_start, unithead_appointment_end, unithead_cluster_id, 
                        unithead_college_id, unithead_deg_unit, unithead_del_ind
                    )
                    VALUES (%s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s, %s, %s)
                """

                values = (unithead_fname, unithead_mname, 
                        unithead_sname, unithead_upmail,
                        unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                        
                        unithead_appointment_start, unithead_appointment_end, 
                        unithead_cluster_id, unithead_college_id, unithead_deg_unit, False
                )

                db.modifydatabase(sql, values) 
                modal_open = True
                feedbackmessage = html.H5("Unit head registered successfully.")
                okay_href = "/acad_heads_directory"
                
            elif create_mode == 'edit':
                # Update existing user record
                unitheadid = parse_qs(parsed.query).get('id', [None])[0]
                
                if unitheadid is None:
                    raise PreventUpdate
                
                sqlcode = """
                    UPDATE iqateam.acad_unitheads
                    SET
                        unithead_upmail = %s,
                        unithead_fac_posn_name = %s,
                        unithead_fac_posn_number = %s, 
                        unithead_desig = %s, 
                        unithead_appointment_end = %s,
                        unithead_del_ind = %s
                    WHERE 
                        unithead_id = %s
                """
                to_delete = bool(removerecord) 
                
                values = [unithead_upmail, unithead_fac_posn_name, 
                          unithead_fac_posn_number, unithead_desig, 
                          unithead_appointment_end, to_delete, unitheadid]
                db.modifydatabase(sqlcode, values)
                
                feedbackmessage = html.H5("Account has been updated.")
                okay_href = "/acad_heads_directory"
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
        Output('unithead_fname', 'value'),
        Output('unithead_mname', 'value'),
        Output('unithead_sname', 'value'),
        Output('unithead_upmail', 'value'),
        Output('unithead_cluster_id', 'value'),      
        Output('unithead_college_id', 'value'), 
        Output('unithead_deg_unit', 'value'),
        Output('unithead_fac_posn_name', 'value'),
        Output('unithead_fac_posn_number', 'value'),
        Output('unithead_desig', 'value'),    
        Output('unithead_appointment_start', 'value'),
        Output('unithead_appointment_end', 'value'),  
       
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
                unithead_cluster_id, unithead_college_id, unithead_deg_unit,
                unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                unithead_appointment_start, unithead_appointment_end
                
            FROM iqateam.acad_unitheads
            WHERE unithead_id = %s
        """
        values = [unitheadid]

        cols = [
            'unithead_fname', 'unithead_mname', 'unithead_sname', 'unithead_upmail',
            'unithead_cluster_id', 'unithead_college_id', 'unithead_deg_unit',
            'unithead_fac_posn_name', 'unithead_fac_posn_number', 'unithead_desig', 
            'unithead_appointment_start', 'unithead_appointment_end'
            
        ]

         
        df = db.querydatafromdatabase(sql, values, cols)

        
        unithead_fname = df['unithead_fname'][0]
        unithead_mname = df['unithead_mname'][0]
        unithead_sname = df['unithead_sname'][0]
        unithead_upmail = df['unithead_upmail'][0]
        unithead_cluster_id = int(df['unithead_cluster_id'][0])
        unithead_college_id = df['unithead_college_id'][0]
        unithead_deg_unit = df['unithead_deg_unit'][0]
        unithead_fac_posn_name = df['unithead_fac_posn_name'][0]
        unithead_fac_posn_number = df['unithead_fac_posn_number'][0]
        unithead_desig = df['unithead_desig'][0]
        unithead_appointment_start = df['unithead_appointment_start'][0]
        unithead_appointment_end = df['unithead_appointment_end'][0]
        
        

        
        return [unithead_fname, unithead_mname, unithead_sname, unithead_upmail, 
                unithead_cluster_id, unithead_college_id, unithead_deg_unit,
                unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig,
                unithead_appointment_start, unithead_appointment_end
                ]
    
    else:
        raise PreventUpdate
    

@app.callback(
    [
        Output('unithead_fname', 'disabled'),
        Output('unithead_mname', 'disabled'),
        Output('unithead_sname', 'disabled'),
        Output('unithead_cluster_id', 'disabled'),      
        Output('unithead_college_id', 'disabled'), 
        Output('unithead_deg_unit', 'disabled'),  
        Output('add_unithead_fac_posn', 'disabled'),  
        Output('unithead_appointment_start', 'disabled'),
    ],
    [Input('url', 'search')]
)
def unithead_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 8  # Disable all inputs in edit mode
    return [False] * 8  # Enable all inputs otherwise















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
