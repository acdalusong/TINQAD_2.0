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
                       "Cluster ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='qaofficer_cluster_id',
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
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='qaofficer_college_id',
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
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(
                        id='qaofficer_deg_unit',
                        #placeholder="Select Department",
                        type="text"
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
                            {"label":"With record","value":"No record"},
                            {"label":"No record","value":"No record"},
                            {"label":"For renewal","value":"For renewal"},
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
                                    dbc.Button("Save", color="primary",  id="qaofficer_save_button", n_clicks=0),
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
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['QA Officer Profile added successfully.'
                                    ],id='qaofficer_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='/qaofficers_directory', id='qaofficer_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='qaofficer_successmodal',
                            backdrop=True,   
                            className="modal-success"    
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
        Output('qaofficer_alert', 'color'),
        Output('qaofficer_alert', 'children'),
        Output('qaofficer_alert', 'is_open'),
        Output('qaofficer_successmodal', 'is_open'),
        Output('qaofficer_feedback_message', 'children'),
        Output('qaofficer_btn_modal', 'href')
    ],
    [
        Input('qaofficer_save_button', 'n_clicks'),
        Input('qaofficer_btn_modal', 'n_clicks'),
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
        State('qaofficer_deg_unit', 'value'),
        State('qaofficer_role', 'value'),
        State('url', 'search')

    ]
)
 
def record_qaofficer_profile(submitbtn, closebtn, removerecord,
                            qaofficer_fname, qaofficer_mname, 
                            qaofficer_sname, qaofficer_upmail,
                            qaofficer_fac_posn_name, qaofficer_fac_posn_number,
                            qaofficer_facadmin_posn, qaofficer_staff_posn,
                            qaofficer_cuposition_id, qaofficer_basicpaper, 
                            qaofficer_remarks, qaofficer_alc,
                            qaofficer_appointment_start, qaofficer_appointment_end, 
                            qaofficer_cluster_id, qaofficer_college_id, 
                            qaofficer_deg_unit, qaofficer_role, search):
    ctx = dash.callback_context 

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'qaofficer_save_button' and submitbtn:
        
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            parsed = urlparse(search)
            create_mode = parse_qs(parsed.query).get('mode', [None])[0]
            
            if create_mode == 'add':

                # Input validation
                if not qaofficer_sname:
                    alert_color_sname = 'danger'
                    alert_text_sname = 'Check your inputs. Please add a Surname.'
                    return [alert_color_sname, alert_text_sname, alert_open, modal_open]
                
                if not qaofficer_fname:
                    alert_color_fname = 'danger'
                    alert_text_fname = 'Check your inputs. Please add a First Name.'
                    return [alert_color_fname, alert_text_fname, alert_open, modal_open]

                if not qaofficer_mname:
                    alert_color_mname = 'danger'
                    alert_text_mname = 'Check your inputs. Please add a Middle Name.'
                    return [alert_color_mname, alert_text_mname, alert_open, modal_open]

                

                if not qaofficer_upmail:
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add a UP Mail.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not qaofficer_cluster_id :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please select a Cluster.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not qaofficer_college_id :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please select a College.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not qaofficer_deg_unit :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please select a Department.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                

                if not qaofficer_fac_posn_name :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please select a Faculty Position.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                

                if not qaofficer_cuposition_id :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add a CU Position.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not qaofficer_basicpaper :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please check if there is basic paper.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not qaofficer_remarks :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add a remark.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                if not qaofficer_alc :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add an ALC.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                
                if not qaofficer_appointment_start  :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add a start date.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
                
                
                if not qaofficer_appointment_end  :
                    alert_color_upmail = 'danger'
                    alert_text_upmail = 'Check your inputs. Please add a end date.'
                    return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]

                sql = """
                    INSERT INTO  qaofficers.qa_officer (
                        qaofficer_fname, qaofficer_mname, qaofficer_sname, qaofficer_upmail,
                        qaofficer_fac_posn_name, qaofficer_fac_posn_number, qaofficer_facadmin_posn, qaofficer_staff_posn,
                        qaofficer_cuposition_id, qaofficer_basicpaper, qaofficer_remarks, qaofficer_alc,
                        qaofficer_appointment_start, qaofficer_appointment_end, qaofficer_cluster_id, 
                        qaofficer_college_id, qaofficer_deg_unit, qaofficer_role, qaofficer_del_ind
                    )
                    VALUES (%s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s)
                
                """

                values = (qaofficer_fname, qaofficer_mname, 
                        qaofficer_sname, qaofficer_upmail,
                        qaofficer_fac_posn_name, qaofficer_fac_posn_number,
                        qaofficer_facadmin_posn, qaofficer_staff_posn,
                        qaofficer_cuposition_id, qaofficer_basicpaper, 
                        qaofficer_remarks, qaofficer_alc,
                        qaofficer_appointment_start, qaofficer_appointment_end, 
                        qaofficer_cluster_id, qaofficer_college_id, qaofficer_deg_unit,
                        qaofficer_role, False
                )

                db.modifydatabase(sql, values) 
                modal_open = True
                feedbackmessage = html.H5("QA Officer registered successfully.")
                okay_href = "/qaofficers_directory"
                
            elif create_mode == 'edit':
                # Update existing user record
                qaofficerid = parse_qs(parsed.query).get('id', [None])[0]
                
                if qaofficerid is None:
                    raise PreventUpdate
                
                sqlcode = """
                    UPDATE qaofficers.qa_officer
                    SET
                        qaofficer_upmail = %s,
                        qaofficer_fac_posn_name = %s,
                        qaofficer_fac_posn_number = %s,
                        qaofficer_facadmin_posn = %s, 
                        qaofficer_staff_posn = %s,
                        qaofficer_remarks = %s,
                        qaofficer_appointment_end = %s,
                        qaofficer_del_ind = %s
                    WHERE
                        qaofficer_id = %s
                """

                to_delete = bool(removerecord) 
                
                values = [qaofficer_upmail, qaofficer_fac_posn_name, 
                          qaofficer_fac_posn_number, qaofficer_facadmin_posn, 
                          qaofficer_staff_posn, qaofficer_remarks, 
                          qaofficer_appointment_end, to_delete, qaofficerid]
                db.modifydatabase(sqlcode, values)
                
                feedbackmessage = html.H5("Account has been updated.")
                okay_href = "/qaofficers_directory"
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
        Output('qaofficer_deg_unit', 'value'),
        Output('qaofficer_role', 'value'),
       
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
                qaofficer_college_id, qaofficer_deg_unit, qaofficer_role
                
            FROM  qaofficers.qa_officer
            WHERE qaofficer_id = %s
        """
        values = [qaofficerid]

        cols = [
            'qaofficer_fname', 'qaofficer_mname', 'qaofficer_sname', 'qaofficer_upmail',
            'qaofficer_fac_posn_name', 'qaofficer_fac_posn_number', 'qaofficer_facadmin_posn', 'qaofficer_staff_posn',
            'qaofficer_cuposition_id', 'qaofficer_basicpaper', 'qaofficer_remarks', 'qaofficer_alc',
            'qaofficer_appointment_start', 'qaofficer_appointment_end', 'qaofficer_cluster_id', 
            'qaofficer_college_id', 'qaofficer_deg_unit', 'qaofficer_role'
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
        qaofficer_deg_unit = df['qaofficer_deg_unit'][0]
        qaofficer_role = df['qaofficer_role'][0]


        return [qaofficer_fname, qaofficer_mname, qaofficer_sname, qaofficer_upmail,
                qaofficer_fac_posn_name, qaofficer_fac_posn_number, qaofficer_facadmin_posn, qaofficer_staff_posn,
                qaofficer_cuposition_id, qaofficer_basicpaper, qaofficer_remarks, qaofficer_alc,
                qaofficer_appointment_start, qaofficer_appointment_end, qaofficer_cluster_id, 
                qaofficer_college_id, qaofficer_deg_unit, qaofficer_role
        ]
    
    else:
        raise PreventUpdate
  
    

@app.callback(
    [
        Output('qaofficer_fname', 'disabled'),
        Output('qaofficer_mname', 'disabled'),
        Output('qaofficer_sname', 'disabled'),

        Output('qaofficer_cuposition_id', 'disabled'),
        Output('qaofficer_basicpaper', 'disabled'),
        Output('qaofficer_alc', 'disabled'),      
        Output('qaofficer_appointment_start', 'disabled'),

        Output('qaofficer_cluster_id', 'disabled'),      
        Output('qaofficer_college_id', 'disabled'), 
        Output('qaofficer_deg_unit', 'disabled'),
        Output('add_qaofficer_fac_posn', 'disabled'),
        Output('qaofficer_role', 'disabled'),
    ],
    [Input('url', 'search')]

)      
def qaofficer_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 12  # Disable all inputs in edit mode
    return [False] * 12  # Enable all inputs otherwise


                

@app.callback(
    [Output('add_qaofficer_successmodal', 'is_open')],
    [Input('add_qaofficer_save_button', 'n_clicks')],
    [State('add_qaofficer_fac_posn', 'value'), 
     State('url', 'search')]
)
 
def register_qaofficer_unithead(submitbtn, add_qaofficer_fac_posn, search):
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
