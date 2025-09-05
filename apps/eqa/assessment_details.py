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

import base64
import os
from urllib.parse import urlparse, parse_qs

# Using the corrected path
UPLOAD_DIRECTORY = r".\assets\database\eqa"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)






form = dbc.Form(
    [
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree Program Title ", 
                         html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_degree_programs_id', 
                        disabled=False
                    ),
                    width=8,
                ),
                 
            ],
            className="mb-2",
        ),
          
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Assessment Year ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="arep_year", type="text", disabled=False),
                    width=2,
                ),
            ],
            className="mb-2",
        ),  

        dbc.Row(
            [
                dbc.Label(
                    [
                     "Approved EQA Type ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_approv_eqa',
                        placeholder="Select EQA Type",
                        disabled=False
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
                        "To be Assessed by ",
                        html.Span("*", style={"color": "#F8B237"})
                    ], 
                    width=4),
                dbc.Col(
                    dbc.Input(id="arep_assessedby", type="text", placeholder="Select Accreditation Body", disabled=False),
                    width=8,
                ),
            ],
            className="mb-2",
        ), 

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Set assessment date? ",
                        html.Span("*", style={"color": "#F8B237"})
                    ], 
                    width=4),
                dbc.Col(
                    dbc.RadioItems(
                        id="arep_qscheddate",
                        options=[
                            {"label":"Yes","value":"Yes"},
                            {"label":"No","value":"No"},
                        ], 
                        inline=True,
                    ),
                ),
            ],
            className="mb-1",
        ),
                
        dbc.Row(
            [
                dbc.Col(dbc.Label(
                    [
                        "First day of Scheduled Assessment Date ", 
                    ],  
                ), width=4),
                dbc.Col(
                    dbc.Input(type="date", id='arep_sched_startdate', disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Col(dbc.Label(
                    [
                        "Last day of Scheduled Assessment Date ", 
                    ],  
                ), width=4),
                dbc.Col(
                    dbc.Input(type="date", id='arep_sched_enddate', disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),


        dbc.Row(
            [
                dbc.Label(
                    [
                        "Notes ", 
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Textarea(id='arep_notes', placeholder="Add notes", disabled=False),
                    width=8,
                ),
            ],
            className="mb-2",
        ),
    ]
)




 

#eqa types dropdown
@app.callback(
    Output('arep_approv_eqa', 'options'),
    Input('url', 'pathname')
)
def populate_approvedeqa_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessment_tracker/assessment_details':
        sql ="""
        SELECT approv_eqa_name as label, approv_eqa_id as value
        FROM eqateam.approv_eqa
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        approvedeqa_types = df.to_dict('records')
        return approvedeqa_types
    else:
        raise PreventUpdate




# disable/able date if yes or no
@app.callback(
    [
        Output('arep_sched_startdate', 'disabled'),
        Output('arep_sched_enddate', 'disabled')
    ],
    [Input('arep_qscheddate', 'value')]
)
def toggle_date(arep_qscheddate_set):
    if arep_qscheddate_set == 'Yes':
        return False, False 
    elif arep_qscheddate_set == 'No':
        return True, True 
    return True, True   



# Layout for the Dash app
layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.Div(  
                            [
                                dcc.Store(id='arep_toload', storage_type='memory', data=0),
                            ]
                        ),
                        
                        html.H1("EQA ACTIVITY DETAILS"),
                        html.Hr(),
                        html.Br(),
                        dbc.Alert(id="arep_alert", is_open=False),  # Alert for feedback
                        form,
                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='arep_removerecord',
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
                            id='arep_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="arep_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="arep_cancel_button", n_clicks=0, href="/assessment_tracker"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='arep_confirmation_modal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="arep_confirmation_modal_cancel", color="warning"),
                                            dbc.Button("Confirm", id="arep_confirmation_modal_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='arep_confirmation_modal',
                            backdrop=True,   
                            className="modal-success"    
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id="arep_final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Click Proceed to continue.")),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        href="/assessment_tracker",
                                        color="success", 
                                    ),
                                ),
                            ],
                            centered=True,
                            id='arep_final_modal',
                            backdrop='static',
                            keyboard=False,
                        ),
                        
                    ],
                    width=8,
                    style={"marginLeft": "15px"},
                ),
            ],
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(),
                    width={"size": 12, "offset": 0},
                ),
            ],
        ),
    ]
)







#i think for updates
@app.callback(
    [
        Output('arep_degree_programs_id', 'options'),
        Output('arep_toload', 'data'),
        Output('arep_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)
def populate_arepdegprog_dropdown(pathname, search):
    if pathname == '/assessment_tracker/assessment_details':
        sql = """
            SELECT pd.pro_degree_title AS label, pd.pro_degree_title AS value
            FROM eqateam.reports r
            JOIN eqateam.program_details pd ON r.rep_degree_programs_id = pd.programdetails_id
            WHERE r.rep_endorsed = True
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        arepdegprog_options = df.to_dict('records')
        
        
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [arepdegprog_options, to_load, removediv_style]


@app.callback(
    [
        Output('arep_alert', 'color'),
        Output('arep_alert', 'children'),
        Output('arep_alert', 'is_open'),
        Output('arep_confirmation_modal', 'is_open'),
        Output('arep_confirmation_modal_message', 'children'),
        Output('arep_final_modal', 'is_open'),
        Output('arep_final_modal_header', 'children'),
        Output('arep_confirmation_modal_confirm', 'color'),
        
    ],
    [
        Input('arep_save_button', 'n_clicks'),
        Input('arep_confirmation_modal_cancel', 'n_clicks'),
        Input('arep_confirmation_modal_confirm', 'n_clicks'),
        Input('arep_removerecord', 'value')
    ],
    [
        State('arep_degree_programs_id', 'value'), 
        State('arep_year', 'value'), 
        State('arep_approv_eqa', 'value'),
        State('arep_assessedby', 'value'),
        State('arep_qscheddate', 'value'),
        State('arep_sched_startdate', 'value'),
        State('arep_sched_enddate', 'value'),
        State('arep_notes', 'value'), 
        State('url', 'search'), 
    ]
)
 
def record_assessment_details (submitbtn, cancel, confirm, removerecord,
                                arep_degree_programs_id, arep_year, 
                                arep_approv_eqa, arep_assessedby, arep_qscheddate, 
                                arep_sched_startdate, arep_sched_enddate, arep_notes,
                                search):

    
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
 
    
    alert_color = ''
    alert_text = ''
    alert_open = False
    confirmation_modal_open = False
    confirmation_modal_message = ''
    final_modal_open = False
    final_modal_header = ''
    confirm_color = 'success'
 
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0] 

    if eventid == 'arep_save_button' and submitbtn:
        if not all([arep_degree_programs_id, arep_year, arep_approv_eqa]):
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            return [alert_color, alert_text, True, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color]
        else:
            if create_mode == 'add':
                confirmation_modal_open = True
                confirmation_modal_message = "Are you sure you want to submit this activity details?"
            elif create_mode == 'edit':
                confirmation_modal_open = True
                confirmation_modal_message = "Are you sure you want to update this activity details?"
                if removerecord:
                    confirmation_modal_message = "Are you sure you want to mark this activity details for deletion?"
                    confirm_color = 'danger'
    elif eventid == 'arep_confirmation_modal_confirm' and confirm:
        if create_mode == 'add':
            sql = """
                INSERT INTO eqateam.assess_report (
                    arep_degree_programs_id, arep_year, arep_approv_eqa, arep_assessedby,
                    arep_qscheddate, arep_sched_startdate, arep_sched_enddate,
                    arep_notes
                )
                VALUES (%s, %s, %s, %s, 
                        %s, %s, %s,  
                        %s)
            """
            values = (
                arep_degree_programs_id, arep_year, arep_approv_eqa, arep_assessedby,
                arep_qscheddate, arep_sched_startdate, arep_sched_enddate,
                arep_notes
            )
    

            db.modifydatabase(sql, values)
            final_modal_open = True
            final_modal_header = "New activity details submitted successfully."

        elif create_mode == 'edit': 
            arepid = parse_qs(parsed.query).get('id', [None])[0]
            
            if arepid is None:
                raise PreventUpdate
            
            # SQL update
            sqlcode = """
                UPDATE eqateam.assess_report
                SET
                    arep_qscheddate  = %s,
                    arep_sched_startdate = %s,
                    arep_sched_enddate  = %s,

                    arep_assessedby = %s,
                    arep_notes = %s,
                    arep_del_ind  = %s
                WHERE 
                    arep_id = %s
            """
            to_delete = bool(removerecord) 

            values = [arep_qscheddate, arep_sched_startdate, arep_sched_enddate,
                    arep_assessedby,
                    arep_notes, to_delete, arepid]
            db.modifydatabase(sqlcode, values)
            final_modal_open = True
            final_modal_header = "Activity Details updated successfully."
    elif eventid == 'arep_confirmation_modal_cancel' and cancel:
        confirmation_modal_open = False
        confirmation_modal_message = ''
        
    else:
        raise PreventUpdate

    return [alert_color, alert_text, True, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color]






@app.callback(
    [ 
        Output('arep_degree_programs_id', 'value'), 
        Output('arep_year', 'value'),
        Output('arep_approv_eqa', 'value'),
        Output('arep_assessedby', 'value'),
        Output('arep_qscheddate', 'value'),
        Output('arep_sched_startdate', 'value'),
        Output('arep_sched_enddate', 'value'),
        Output('arep_notes', 'value'), 
    ],
    [  
        Input('arep_toload', 'modified_timestamp')
    ],
    [
        State('arep_toload', 'data'),
        State('url', 'search')
    ]
)
def arep_load(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        arepid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT
                arep_degree_programs_id, arep_year, arep_approv_eqa, arep_assessedby,
                arep_qscheddate, arep_sched_startdate, arep_sched_enddate,
                arep_notes
            
            FROM eqateam.assess_report
            WHERE arep_id = %s
        """
        values = [arepid]

        cols = [
                "arep_degree_programs_id", "arep_year", "arep_approv_eqa", "arep_assessedby",
                "arep_qscheddate", "arep_sched_startdate", "arep_sched_enddate",
                "arep_notes"
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        
        arep_degree_programs_id = df['arep_degree_programs_id'][0]
        arep_year = df['arep_year'][0]
        arep_approv_eqa = df['arep_approv_eqa'][0]
        arep_assessedby = df['arep_assessedby'][0]

        arep_qscheddate = df['arep_qscheddate'][0]
        arep_sched_startdate = df['arep_sched_startdate'][0]
        arep_sched_enddate = df['arep_sched_enddate'][0]

        arep_notes = df['arep_notes'][0]  
        
        return [arep_degree_programs_id, arep_year, arep_approv_eqa, arep_assessedby, 
                arep_qscheddate, arep_sched_startdate, arep_sched_enddate,
                arep_notes,  
                ]
    
    else:
        raise PreventUpdate






 
@app.callback(
    [ 
        Output('arep_degree_programs_id', 'disabled'), 
        Output('arep_approv_eqa', 'disabled')        
    ],
    [Input('url', 'search')]
)
def arep_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 2
    return [False] * 2


  
