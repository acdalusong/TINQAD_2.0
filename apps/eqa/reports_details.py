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
from uuid import uuid4
from datetime import date, datetime

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
                      "Report Type",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='rep_report_type',
                        placeholder="Select Report Type",
                        #options=[
                        #    {"label":"SAR","value":"SAR"},
                        #    {"label":"SSR","value":"SSR"},
                        #    {"label":"Post-EQA","value":"Post-EQA"},
                        #    {"label":"Assessment","value":"Assessment"},
                        #    {"label":"Benchmarking","value":"Benchmarking"},
                        #    ],
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
                        "SAR Version",
                    ],  
                    width=4),
                dbc.Col(
                    dcc.Input(
                        id='sar_version_id',
                        type='number',
                        placeholder="Enter Version Number",
                        min=1,
                        step=1,
                    ),
                    width=2,
                ),          
            ],
            id='sar_version',
            className="mb-2", 
        ), 

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree Program Title", 
                         html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='rep_degree_programs_id', 
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
                     "Date Submitted",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                       id='rep_currentdate',
                       date=str(pd.to_datetime("today").date()),
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        
############################################################################3
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Status",
                        html.Span("*", style={"color": "#F8B237"})
                    ],  
                    width=4),
                 
                dbc.Col(
                    dcc.Dropdown(
                        id='rep_checkstatus',
                        placeholder="Select Status",
                        options=[
                            {"label":"For Checking","value":"For Checking"},
                            {"label":"Checked","value":"Checked"},
                            {"label":"Desktop Review","value":"Desktop Review"},
                            ],
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
                        "Name of Checker",
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id='rep_checkedby', disabled=False),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Date of Checking",
                    ], 
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='rep_datechecked', disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Name of Desktop Reviewer",
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id='rep_desktopby', disabled=False),
                    width=6,
                ),
            ],
            id='sar_namedesk',
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Date of Desktop Review",
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='rep_datedesktop', disabled=False),
                    width=4,
                ),
            ],
            id='sar_datedesk',
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Notes",
                        html.Span("", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Textarea(id='rep_notes', placeholder="Add notes", disabled=False),
                    width=8,
                ),
            ],
            className="mb-2",
        ),          


        
        html.Hr(),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link Submission 1 ", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text",id="rep_link1", placeholder="Enter Link",
                              disabled=False),
                    width=5,
                ),
                dbc.Col(
                    dbc.Input(
                        id="rep_link1_timestamp", type="text", disabled=True, placeholder="Timestamp"
                        ),
                    width=3,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link Submission 2 ", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text",id="rep_link2", placeholder="Enter Link",
                              disabled=False),
                    width=5,
                ),
                dbc.Col(
                    dbc.Input(
                        id="rep_link2_timestamp", type="text", disabled=True, placeholder="Timestamp"
                        ),
                    width=3,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link Submission 3 ", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text",id="rep_link3", placeholder="Enter Link",
                              disabled=False),
                    width=5,
                ),
                dbc.Col(
                    dbc.Input(
                        id="rep_link3_timestamp", type="text", disabled=True, placeholder="Timestamp"
                        ),
                    width=3,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Endorsed for EQA? ",
                    ], 
                    width=4),
                dbc.Col(
                    dbc.RadioItems(
                        id="rep_endorsed",
                        options=[
                            {"label":"Yes","value":"True"},
                            {"label":"No","value":"False"},
                        ], 
                        value="False",
                        inline=True,
                    ),
                ),
            ],
            id='sar_endorsed',
            className="mb-1",
        ),





    ], 
)



#########################################################################3
# Layout for the Dash app
layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.Div([
                            dcc.Store(id='rep_toload', storage_type='memory', data=0),
                        ]),

                        html.H1("REPORT SUBMISSION DETAILS"),
                        html.Hr(),
                        html.Br(),

                        dbc.Alert(id="rep_alert", is_open=False),  # Alert for feedback
                        form,
                        html.Br(),

                        # Deletion section
                        dbc.Row(
                            [
                                dbc.Label("Wish to delete?", width=3),
                                dbc.Col(
                                    dbc.Checklist(
                                        id='rep_removerecord',
                                        options=[{'label': "Mark for Deletion", 'value': 1}],
                                        style={'fontWeight': 'bold'},
                                    ),
                                    width=5,
                                ),
                            ],
                            className="mb-3",
                            id='rep_removerecord_div'
                        ),

                        html.Br(),

                        # Save and cancel buttons
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("Save", color="primary", id="rep_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="rep_cancel_button", n_clicks=0, href="/assessment_reports"),
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='reports_details_confirmation_modal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="reports_details_confirmation_modal_cancel", color="warning"),
                                            dbc.Button("Confirm", id="reports_details_confirmation_modal_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='reports_details_confirmation_modal',
                            backdrop=True,   
                            className="modal-success"    
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id="reports_details_final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Click Proceed to continue.")),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        href="/assessment_reports",
                                        color="success", 
                                    ),
                                ),
                            ],
                            centered=True,
                            id='reports_details_final_modal',
                            backdrop='static',
                            keyboard=False,
                        ),  

                        html.Br(),
                        html.Br(),
                        html.Br(),

                        # Footer
                        dbc.Row(
                            [
                                dbc.Col(
                                    cm.generate_footer(),
                                    width={"size": 12, "offset": 0},
                                ),
                            ],
                        ),
                    ],
                    width=8,
                    style={"marginLeft": "15px"},
                ),
            ],
        ),
    ]
)

###########################################################################


#for the dates to be recorded in sql
#def safe_parse_date(val):
#    return date.fromisoformat(val) if val else None


#if sar reoprt type, hide sar version and desktop review
@app.callback(
    [
        Output('sar_version', 'style'),
        Output('sar_datedesk', 'style'),
        Output('sar_namedesk', 'style'),
        Output('sar_endorsed', 'style'),
    ],
    [
        Input('rep_report_type', 'value')
    ]
)
def toggle_visibility(rep_report_type):
    hide = {'display': 'none'}
    show = {}

    if rep_report_type == 'SAR':
        return [show, show, show, show]
    else:
        return [hide, hide, hide, hide]


#for the degree programs dropdown
@app.callback(
    [
        Output('rep_degree_programs_id', 'options'),
        Output('rep_toload', 'data'),
        Output('rep_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)
def populate_degprog_dropdown(pathname, search):
    if pathname == '/assessmentreports/reports_details':
        sql = """
            SELECT pro_degree_title as label, programdetails_id as value
            FROM eqateam.program_details
            
            WHERE pro_del_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        degprog_options = df.to_dict('records')
        
        
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [degprog_options, to_load, removediv_style]


#for report types dropdown
@app.callback(
    Output('rep_report_type', 'options'),
    Input('url', 'pathname')
)
def populate_reporttype_dropdown(pathname): 
    if pathname == '/assessmentreports/reports_details':
        sql ="""
        SELECT reporttype_name as label, reporttype_name as value
        FROM eqateam.report_type
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        reporttype_types = df.to_dict('records')
        return reporttype_types
    else:
        raise PreventUpdate






#for form submissions

@app.callback(
    [
        Output('rep_alert', 'color'),
        Output('rep_alert', 'children'),
        Output('rep_alert', 'is_open'),
        Output('reports_details_confirmation_modal', 'is_open'),
        Output('reports_details_confirmation_modal_message', 'children'),
        Output('reports_details_final_modal', 'is_open'),
        Output('reports_details_final_modal_header', 'children'),
        Output('reports_details_confirmation_modal_confirm', 'color')
    ],
    [
        Input('rep_save_button', 'n_clicks'),
        Input('reports_details_confirmation_modal_cancel', 'n_clicks'),
        Input('reports_details_confirmation_modal_confirm', 'n_clicks'),
        Input('rep_removerecord', 'value')
    ],
    [
        State('rep_report_type', 'value'),
        State('sar_version_id', 'value'),
        State('rep_degree_programs_id', 'value'),
        State('rep_currentdate', 'date'),
        State('rep_checkstatus', 'value'),
        State('rep_checkedby', 'value'),
        State('rep_datechecked', 'value'),
        State('rep_desktopby', 'value'),
        State('rep_datedesktop', 'value'),
        State('rep_notes', 'value'),
        State('rep_link1', 'value'),
        State('rep_link1_timestamp', 'value'),
        State('rep_link2', 'value'),
        State('rep_link2_timestamp', 'value'),
        State('rep_link3', 'value'),
        State('rep_link3_timestamp', 'value'),
        State('rep_endorsed', 'value'),
        State('url', 'search')
    ]
)
def record_rep_details(submitbtn, cancel, confirm, removerecord,
                        rep_report_type, sar_version_id, rep_degree_programs_id, rep_currentdate,
                        rep_checkstatus, rep_checkedby, rep_datechecked, rep_desktopby, rep_datedesktop, rep_notes,
                        rep_link1, rep_link1_timestamp, rep_link2, rep_link2_timestamp, rep_link3, rep_link3_timestamp,
                        rep_endorsed, search):
    
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    # Initialize default response values
    
    alert_color = ''
    alert_text = ''
    alert_open = False
    confirmation_modal_open = False
    confirmation_modal_message = ''
    final_modal_open = False
    final_modal_header = ''
    confirm_color = 'success'

    # Parse URL for mode
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    if eventid == 'rep_save_button' and submitbtn:
        # Validate required fields
        if not all([rep_report_type, rep_degree_programs_id, rep_checkstatus]):
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            return [alert_color, alert_text, True, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color]
        #rep_datedesktop = safe_parse_date(rep_datedesktop)
        #rep_datechecked = safe_parse_date(rep_datechecked)
        else:
            if create_mode == 'add':
                confirmation_modal_open = True
                confirmation_modal_message = "Are you sure you want to submit this report?"
                confirm_color = 'success'

            elif create_mode == 'edit':
                confirmation_modal_open = True
                confirmation_modal_message = "Are you sure you want to update this report?"
                if removerecord:
                    confirmation_modal_message = "Are you sure you want to mark this report for deletion?"
                    confirm_color = 'danger'

    elif eventid == 'reports_details_confirmation_modal_confirm' and confirm:  
        if create_mode == 'add':     
            # SQL insertion
            sql = """
                INSERT INTO eqateam.reports (
                    rep_report_type, sar_version_id, rep_degree_programs_id, rep_currentdate, 
                    rep_checkstatus, rep_checkedby, rep_datechecked, rep_desktopby, rep_datedesktop, rep_notes,
                    rep_link1, rep_link1_timestamp, rep_link2, rep_link2_timestamp, rep_link3, rep_link3_timestamp,
                    rep_endorsed
                )
                VALUES (%s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s)
            """
            values = (
                rep_report_type, sar_version_id, rep_degree_programs_id, rep_currentdate,
                rep_checkstatus, rep_checkedby, rep_datechecked, rep_desktopby, rep_datedesktop, rep_notes,
                rep_link1, rep_link1_timestamp, rep_link2, rep_link2_timestamp, rep_link3, rep_link3_timestamp,
                rep_endorsed
            ) 

            db.modifydatabase(sql, values)
            final_modal_open = True
            final_modal_header = "New report submitted successfully."

        elif create_mode == 'edit': 
            repid = parse_qs(parsed.query).get('id', [None])[0]
            
            if repid is None:
                raise PreventUpdate
            
            #rep_datedesktop = safe_parse_date(rep_datedesktop)
            #rep_datechecked = safe_parse_date(rep_datechecked)
            
            # SQL update
            sqlcode = """
                UPDATE eqateam.reports
                SET
                    sar_version_id = %s,
                    rep_checkstatus = %s,
                    rep_checkedby = %s,
                    rep_datechecked = %s,
                    rep_desktopby = %s,
                    rep_datedesktop = %s,
                    rep_notes = %s,
                    rep_link1 = %s,
                    rep_link1_timestamp = %s,
                    rep_link2 = %s,
                    rep_link2_timestamp = %s,
                    rep_link3 = %s,
                    rep_link3_timestamp = %s,
                    rep_endorsed = %s,
                    rep_del_ind = %s
                WHERE 
                    rep_id = %s
            """
            to_delete = bool(removerecord) 

            values = (
                sar_version_id,
                rep_checkstatus,
                rep_checkedby,
                rep_datechecked,
                rep_desktopby,
                rep_datedesktop,
                rep_notes,
                rep_link1,
                rep_link1_timestamp,
                rep_link2,
                rep_link2_timestamp,
                rep_link3,
                rep_link3_timestamp,
                rep_endorsed,

                to_delete,  # This is for rep_del_ind
                repid       # This is for WHERE rep_id = %s
            )
            db.modifydatabase(sqlcode, values)

            final_modal_open = True
            final_modal_header = "Report updated successfully."
        
    elif eventid == 'reports_details_confirmation_modal_cancel' and cancel:
        confirmation_modal_open = False
        confirmation_modal_message = ''

    else:
        raise PreventUpdate

    # print(alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href)
    # print("Raw input from form:")
    # print("rep_datechecked:", rep_datechecked)
    # print("rep_datedesktop:", rep_datedesktop)

    return [alert_color, alert_text, True, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_color]



    
############### for pre-fill dash form with existing data
@app.callback(
    [ 
        Output('rep_report_type', 'value'),
        Output('sar_version_id', 'value'),
        Output('rep_degree_programs_id', 'value'),
        Output('rep_currentdate', 'value'), 
        Output('rep_checkstatus', 'value'),
        Output('rep_checkedby', 'value'),
        Output('rep_datechecked', 'value'),
        Output('rep_desktopby', 'value'),
        Output('rep_datedesktop', 'value'),
        Output('rep_notes', 'value'),
        Output('rep_link1', 'value'),
        Output('rep_link1_timestamp', 'value'),
        Output('rep_link2', 'value'),
        Output('rep_link2_timestamp', 'value'),
        Output('rep_link3', 'value'),
        Output('rep_link3_timestamp', 'value'),
        Output('rep_endorsed', 'value'),
    ],
    [  
        Input('rep_toload', 'modified_timestamp')
    ],
    [
        State('rep_toload', 'data'),
        State('url', 'search')
    ]
)
def rep_load(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        repid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                rep_report_type, sar_version_id, rep_degree_programs_id, rep_currentdate, 
                rep_checkstatus, rep_checkedby, rep_datechecked, rep_desktopby, rep_datedesktop, rep_notes,
                rep_link1, rep_link1_timestamp, rep_link2, rep_link2_timestamp, rep_link3, rep_link3_timestamp,
                rep_endorsed
            FROM eqateam.reports
            WHERE rep_id = %s
        """
        values = [repid]

        cols = [
                'rep_report_type', 'sar_version_id', 'rep_degree_programs_id', 'rep_currentdate', 
                'rep_checkstatus', 'rep_checkedby', 'rep_datechecked', 'rep_desktopby', 'rep_datedesktop', 'rep_notes',
                'rep_link1', 'rep_link1_timestamp', 'rep_link2', 'rep_link2_timestamp', 'rep_link3', 'rep_link3_timestamp',
                'rep_endorsed',
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        rep_report_type = df['rep_report_type'][0]
        sar_version_id = df['sar_version_id'][0]
        rep_degree_programs_id = int(df['rep_degree_programs_id'][0])
        rep_currentdate = df['rep_currentdate'][0]
        rep_checkstatus = df['rep_checkstatus'][0]
        rep_checkstatus = df['rep_checkstatus'][0]
        rep_checkedby = df['rep_checkedby'][0]
        rep_datechecked = df['rep_datechecked'][0]
        rep_desktopby = df['rep_desktopby'][0]
        rep_datedesktop = df['rep_datedesktop'][0]
        rep_notes = df['rep_notes'][0]
        rep_link1 = df['rep_link1'][0]
        rep_link1_timestamp = df['rep_link1_timestamp'][0]
        rep_link2 = df['rep_link2'][0]
        rep_link2_timestamp = df['rep_link2_timestamp'][0]
        rep_link3 = df['rep_link3'][0]
        rep_link3_timestamp = df['rep_link3_timestamp'][0]
        rep_endorsed = df['rep_endorsed'][0]


        return [rep_report_type, sar_version_id, rep_degree_programs_id, rep_currentdate,
                rep_checkstatus, rep_checkedby, rep_datechecked, rep_desktopby, rep_datedesktop, rep_notes,
                rep_link1, rep_link1_timestamp,
                rep_link2, rep_link2_timestamp,
                rep_link3, rep_link3_timestamp,
                rep_endorsed]
    
    else:
        raise PreventUpdate


 ######### enables or disables form depending on url parameter
@app.callback(
    [ 
        Output('rep_report_type', 'disabled'), 
        Output('rep_degree_programs_id', 'disabled'), 
        Output('rep_currentdate', 'disabled'),  
    ],
    [Input('url', 'search')]
)
def rep_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 3
    return [False] * 3

