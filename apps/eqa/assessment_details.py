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
                        "Assessment Title ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="arep_title", type="text", disabled=False),
                    width=8,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                     "Date",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='arep_currentdate',
                        date=str(pd.to_datetime("today").date()),  # Ensure this line is correct
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
                    dbc.Input(type="date", id='arep_sched_assessdate', disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Col(dbc.Label(
                    [
                        "Duration of Scheduled Assessment", 
                    ],  
                ), width=4),
                dbc.Col(
                    dbc.Input(type="text", id='arep_sched_assessduration', 
                              placeholder="e.g. June 20-23, 2024",
                              disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                      "Report type ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_report_type',
                        placeholder="Select Report Type",
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
                        "Report Notes", 
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Textarea(id='arep_report_type_notes', placeholder="Add notes", disabled=False),
                    width=8,
                ),
            ],
            className="mb-2",
        ), 
        dbc.Row(
            [
                dbc.Label(
                    [
                        "File Submissions ",
                        
                    ],
                    width=4,
                ),
                dbc.Col(
                    dcc.Upload(
                        id="arep_file",
                        children=html.Div(
                            [
                                '       Drag and Drop or Select Files',
                            ],
                            style={"display": "flex", "alignItems": "center"},
                        ),
                        style={
                            'width': '100%',
                            'height': '30px',
                            'lineHeight': '30px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center', 
                        },
                        multiple=True,    
                    ),
                    width=6,
                ),
                
            ],
            className="mb-2",
        ),
 
        dbc.Row(
            [dbc.Label("",width=4),
             dbc.Col(id="arep_file_output",style={"color": "#F8B237"}, width="4")],   
            className="mt-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link Submissions ", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text",id="arep_link", placeholder="Enter Link",
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
                        "Check Status ", 
                    ],  
                    width=4),
                 
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_checkstatus',
                        placeholder="Select Status",
                        options=[
                            {"label":"For Checking","value":"For Checking"},
                            {"label":"Already Checked","value":"Already Checked"},
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
                        "Date Reviewed", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='arep_datereviewed', disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Review Status ", 
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_review_status',
                        placeholder="Select Review Status",
                        disabled=True,
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
                        "Notes ", 
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Textarea(id='arep_notes', placeholder="Add notes", disabled=True),
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
    if pathname == '/assessmentreports/assessment_details':
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




# Callback to handle enabling/disabling file and link submissions based on sarsubmission_type
@app.callback(
    [
        Output('arep_sched_assessdate', 'disabled'),
        Output('arep_sched_assessduration', 'disabled')
    ],
    [Input('arep_qscheddate', 'value')]
)
def toggle_date(arep_qscheddate_set):
    if arep_qscheddate_set == 'Yes':
        return False, False 
    elif arep_qscheddate_set == 'No':
        return True, True 
    return True, True   



#report types dropdown
@app.callback(
    Output('arep_report_type', 'options'),
    Input('url', 'pathname')
)
def populate_reporttype_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/assessment_details':
        sql ="""
        SELECT report_type_name as label, report_type_id as value
        FROM eqateam.report_type
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        report_types = df.to_dict('records')
        return report_types
    else:
        raise PreventUpdate






#review status dropdown
@app.callback(
    Output('arep_review_status', 'options'),
    Input('url', 'pathname')
)
def populate_reviewstatus_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/assessment_details':
        sql ="""
        SELECT review_status_name as label, review_status_id as value
        FROM eqateam.review_status
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        reviewstatus_types = df.to_dict('records')
        return reviewstatus_types
    else:
        raise PreventUpdate

 
# Callback to display the names of the uploaded files
@app.callback(
    Output("arep_file_output", "children"),
    [Input("arep_file", "filename")],  
)
def display_uploaded_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"?? {file_names_str}"
 
    return f"?? {filenames}"


@app.callback(
    [
        Output('arep_datereviewed', 'disabled'),
        Output('arep_review_status', 'disabled'),
        Output('arep_notes', 'disabled'), 
    ],
    [   
        Input('arep_checkstatus', 'value')
    ]
)
def toggle_dropdowns(arep_checkstatus_type):
    if arep_checkstatus_type == 'For Checking':
        return True, True, True
    elif arep_checkstatus_type == 'Already Checked':
        return False, False, False
    return True, True, True
















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
                        
                        html.H1("ADD NEW ASSESSMENT REPORT"),
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
                                    dbc.Button("Cancel", color="warning", id="arep_cancel_button", n_clicks=0, href="/assessment_reports"),  
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
                                    ['New assessment submitted successfully.'
                                    ],id='arep_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='assessment_reports', id='arep_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='arep_successmodal',
                            backdrop=True,   
                            className="modal-success"    
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
    if pathname == '/assessmentreports/assessment_details':
        sql = """
            SELECT pd.pro_degree_title AS label, pd.pro_degree_title AS value
            FROM eqateam.sar_report sr
            JOIN eqateam.program_details pd ON sr.sarep_degree_programs_id = pd.programdetails_id
            WHERE sr.sarep_del_ind = False
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
        Output('arep_successmodal', 'is_open'),
        Output('arep_feedback_message', 'children'),
        Output('arep_btn_modal', 'href')
    ],
    [
        Input('arep_save_button', 'n_clicks'),
        Input('arep_btn_modal', 'n_clicks'),
        Input('arep_removerecord', 'value')
    ],
    [
        State('arep_degree_programs_id', 'value'), 
        State('arep_title', 'value'),
        State('arep_currentdate', 'value'),  
        State('arep_approv_eqa', 'value'),
        State('arep_assessedby', 'value'),
        State('arep_qscheddate', 'value'),
        State('arep_sched_assessdate', 'value'),
        State('arep_sched_assessduration', 'value'),
        State('arep_report_type', 'value'),
        State('arep_report_type_notes', 'value'),
        State('arep_file', 'contents'),
        State('arep_file', 'filename'),  
        State('arep_link', 'value'),
        State('arep_checkstatus', 'value'),
        State('arep_datereviewed', 'value'),
        State('arep_review_status', 'value'),
        State('arep_notes', 'value'), 
        State('url', 'search'), 
    ]
)
 
def record_assessment_details (submitbtn, closebtn, removerecord,
                                arep_degree_programs_id, arep_title, arep_currentdate, 
                                arep_approv_eqa, arep_assessedby, arep_qscheddate, arep_sched_assessdate, 
                                arep_sched_assessduration, arep_report_type, arep_report_type_notes, 
                                arep_file_contents, arep_file_names, arep_link,  
                                arep_checkstatus, arep_datereviewed, 
                                arep_review_status, arep_notes,
                                search):

    
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'arep_save_button' or not submitbtn:
        raise PreventUpdate
 
    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''
    feedbackmessage = None
    okay_href = None
 
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0] 

   
    def process_files(contents, filenames):
        file_data = []
        for content, filename in zip(contents, filenames):
            if content == "1" and filename == "1":
                continue  # Skip default "1" value
            try:
                content_type, content_string = content.split(',')
                decoded_content = base64.b64decode(content_string)

                file_path = os.path.join(UPLOAD_DIRECTORY, filename)
                with open(file_path, 'wb') as f:
                    f.write(decoded_content)

                file_info = {
                    "path": file_path,
                    "name": filename,
                    "type": content_type,
                    "size": len(decoded_content),
                }
                file_data.append(file_info)

            except Exception as e:
                return None, f'Error processing file: {e}'
        return file_data, None

    if create_mode == 'add':  
        if not all([arep_degree_programs_id, arep_title, arep_approv_eqa, arep_checkstatus]):
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            return [alert_color, alert_text, True, modal_open, feedbackmessage, okay_href]

        if arep_file_contents is None or arep_file_names is None:
            arep_file_contents = ["1"]
            arep_file_names = ["1"]

        arep_file_data, error = process_files(arep_file_contents, arep_file_names)
        if error:
            alert_open = True
            alert_color = 'danger'
            alert_text = error
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        if arep_currentdate is None:
            arep_currentdate = str(pd.to_datetime("today").date())

        sql = """
            INSERT INTO eqateam.assess_report (
                arep_degree_programs_id, arep_title, arep_currentdate,
                arep_approv_eqa, arep_assessedby, arep_qscheddate,
                arep_sched_assessdate, arep_sched_assessduration, arep_report_type, 
                arep_report_type_notes,
                arep_file_path, arep_file_name, arep_file_type, arep_file_size,
                arep_link, arep_checkstatus, arep_datereviewed, 
                arep_review_status, arep_notes
            )
            VALUES (%s, %s, %s, 
                    %s, %s, %s,  
                    %s, %s, %s, 
                    %s, 
                    %s, %s, %s, %s,
                    %s, %s, %s, 
                    %s, %s)
        """
        values = (
            arep_degree_programs_id, arep_title, arep_currentdate,
            arep_approv_eqa, arep_assessedby, arep_qscheddate,
            arep_sched_assessdate, arep_sched_assessduration,
            arep_report_type, arep_report_type_notes,
            arep_file_data[0]["path"] if arep_file_data else None,
            arep_file_data[0]["name"] if arep_file_data else None,
            arep_file_data[0]["type"] if arep_file_data else None,
            arep_file_data[0]["size"] if arep_file_data else None,
            arep_link, arep_checkstatus, arep_datereviewed, 
            arep_review_status, arep_notes
        )
 

        db.modifydatabase(sql, values)
        modal_open = True
        feedbackmessage = html.H5("New assessment report submitted successfully.")
        okay_href = "/assessment_reports"

    elif create_mode == 'edit': 
        arepid = parse_qs(parsed.query).get('id', [None])[0]
        
        if arepid is None:
            raise PreventUpdate
        
        # SQL update
        sqlcode = """
            UPDATE eqateam.assess_report
            SET
                arep_qscheddate  = %s,
                arep_sched_assessdate = %s,
                arep_sched_assessduration  = %s,

                arep_checkstatus = %s,
                arep_datereviewed = %s,
                arep_review_status = %s,
                arep_notes = %s,
                arep_del_ind  = %s
            WHERE 
                arep_id = %s
        """
        to_delete = bool(removerecord) 

        values = [arep_qscheddate, arep_sched_assessdate, arep_sched_assessduration,
                  arep_checkstatus, arep_datereviewed, arep_review_status,
                arep_notes, to_delete, arepid]
        db.modifydatabase(sqlcode, values)

        feedbackmessage = html.H5("Status has been updated.")
        okay_href = "/assessment_reports"
        modal_open = True

    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]






@app.callback(
    [ 
        Output('arep_degree_programs_id', 'value'), 
        Output('arep_title', 'value'),
        Output('arep_currentdate', 'value'),  
        Output('arep_approv_eqa', 'value'),
        Output('arep_assessedby', 'value'),
        Output('arep_qscheddate', 'value'),
        Output('arep_sched_assessdate', 'value'),
        Output('arep_sched_assessduration', 'value'),
        Output('arep_report_type', 'value'),
        Output('arep_report_type_notes', 'value'), 
        Output('arep_file', 'filename'),  
        Output('arep_link', 'value'),
        Output('arep_checkstatus', 'value'),
        Output('arep_datereviewed', 'value'),
        Output('arep_review_status', 'value'),
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
                arep_degree_programs_id, arep_title, arep_currentdate,
                arep_approv_eqa, arep_assessedby, arep_qscheddate,
                arep_sched_assessdate, arep_sched_assessduration, arep_report_type, 
                arep_report_type_notes,
                arep_file_name,
                arep_link, arep_checkstatus, arep_datereviewed, 
                arep_review_status, arep_notes
            
            FROM eqateam.assess_report
            WHERE arep_id = %s
        """
        values = [arepid]

        cols = [
                "arep_degree_programs_id", "arep_title", "arep_currentdate",
                "arep_approv_eqa", "arep_assessedby", "arep_qscheddate",
                "arep_sched_assessdate", "arep_sched_assessduration", "arep_report_type", 
                "arep_report_type_notes",
                "arep_file_name",
                "arep_link", "arep_checkstatus", "arep_datereviewed", 
                "arep_review_status", "arep_notes"
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        
        arep_degree_programs_id = df['arep_degree_programs_id'][0]
        arep_title = df['arep_title'][0]
        arep_currentdate = df['arep_currentdate'][0]
        arep_approv_eqa = df['arep_approv_eqa'][0]
        
        arep_assessedby = df['arep_assessedby'][0]
        arep_qscheddate = df['arep_qscheddate'][0]
        arep_sched_assessdate = df['arep_sched_assessdate'][0]
        arep_sched_assessduration = df['arep_sched_assessduration'][0]

        arep_report_type = df['arep_report_type'][0]
        arep_report_type_notes = df['arep_report_type_notes'][0] 

        arep_file_name = df['arep_file_name'][0]
        arep_link = df['arep_link'][0]
        arep_checkstatus = df['arep_checkstatus'][0]
        arep_datereviewed = df['arep_datereviewed'][0]
        arep_review_status = df['arep_review_status'][0]
        arep_notes = df['arep_notes'][0]  
        
        return [arep_degree_programs_id, arep_title, arep_currentdate, 
                arep_approv_eqa, arep_assessedby, arep_qscheddate, 
                arep_sched_assessdate, arep_sched_assessduration,
                arep_report_type, arep_report_type_notes,
                arep_file_name, arep_link, 
                arep_checkstatus, arep_datereviewed,
                arep_review_status, arep_notes,  
                ]
    
    else:
        raise PreventUpdate






 
@app.callback(
    [ 
        Output('arep_degree_programs_id', 'disabled'), 
        Output('arep_title', 'disabled'), 
        Output('arep_currentdate', 'disabled'), 
        Output('arep_approv_eqa', 'disabled'), 
        Output('arep_assessedby', 'disabled'), 
        Output('arep_qscheddate', 'disabled'), 
        Output('arep_report_type', 'disabled'), 
        Output('arep_report_type_notes', 'disabled'),  
        
        Output('arep_file', 'disabled'), 
        Output('arep_link', 'disabled'),  
        
    ],
    [Input('url', 'search')]
)
def arep_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 10
    return [False] * 10


  
