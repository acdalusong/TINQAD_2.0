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
                        "Degree Program Title", 
                         html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sarep_degree_programs_id', 
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
                     "Date",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                       id='sarep_currentdate',
                       date=str(pd.to_datetime("today").date()),
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
                        "File Submissions ",
                        
                    ],
                    width=4,
                ),
                dbc.Col(
                    dcc.Upload(
                        id="sarep_file",
                        children=html.Div(
                            [
                                'Drag and Drop or Select Files',
                            ], 
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
             dbc.Col(id="sarep_file_output",style={"color": "#F8B237"}, width="4")],   
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
                    dbc.Input(type="text",id="sarep_link", placeholder="Enter Link",
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],  
                    width=4),
                 
                dbc.Col(
                    dcc.Dropdown(
                        id='sarep_checkstatus',
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
                        html.Span("*", style={"color": "#F8B237"})
                    ], 
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='sarep_datereviewed', disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Assessed by",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id='sarep_assessedby', disabled=True),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Review Status ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='sarep_review_status',
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Textarea(id='sarep_notes', placeholder="Add notes", disabled=True),
                    width=8,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "SAR Score ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="sarep_sarscore", type="number", disabled=True),
                    width=3,
                ),
            ],
            className="mb-2",
        ),
             
    ], 

)




#eqa types dropdown
@app.callback(
    Output('sarep_approv_eqa', 'options'),
    Input('url', 'pathname')
)
def populate_approvedeqa_dropdown(pathname): 
    if pathname == '/assessmentreports/sar_details':
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


 

#review status dropdown
@app.callback(
    Output('sarep_review_status', 'options'),
    Input('url', 'pathname')
)
def populate_reviewstatus_dropdown(pathname): 
    if pathname == '/assessmentreports/sar_details':
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
    Output("sarep_file_output", "children"),
    [Input("sarep_file", "filename")],  
)
def display_uploaded_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"📑{file_names_str}"
 
    return f"📑{filenames}"


@app.callback(
    [
        Output('sarep_datereviewed', 'disabled'),
        Output('sarep_assessedby', 'disabled'),
        Output('sarep_review_status', 'disabled'),
        Output('sarep_notes', 'disabled'),
        Output('sarep_sarscore', 'disabled')
    ],
    [   
        Input('sarep_checkstatus', 'value')
    ]
)
def toggle_dropdowns(sarep_checkstatus_type):
    if sarep_checkstatus_type == 'For Checking':
        return True, True, True, True, True
    elif sarep_checkstatus_type == 'Already Checked':
        return False, False, False, False, False
    return True, True, True, True, True


 

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
                                dcc.Store(id='sarep_toload', storage_type='memory', data=0),
                            ]
                        ),
                        
                        html.H1("ADD NEW SAR SUBMISSION"),
                        html.Hr(),
                        html.Br(),
                        dbc.Alert(id="sarep_alert", is_open=False),  # Alert for feedback
                        form,
                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='sarep_removerecord',
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
                            id='sarep_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="sarep_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="sarep_cancel_button", n_clicks=0, href="/SDG_evidencelist"),  
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
                                    ['New SAR submitted successfully.'
                                    ],id='sarep_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='assessment_reports', id='sarep_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='sarep_successmodal',
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
        Output('sarep_degree_programs_id', 'options'),
        Output('sarep_toload', 'data'),
        Output('sarep_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)

def populate_degprog_dropdown(pathname, search):
    if pathname == '/assessmentreports/sar_details':
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



@app.callback(
    [
        Output('sarep_alert', 'color'),
        Output('sarep_alert', 'children'),
        Output('sarep_alert', 'is_open'),
        Output('sarep_successmodal', 'is_open'),
        Output('sarep_feedback_message', 'children'),
        Output('sarep_btn_modal', 'href')
    ],
    [
        Input('sarep_save_button', 'n_clicks'),
        Input('sarep_btn_modal', 'n_clicks'),
        Input('sarep_removerecord', 'value')
    ],
    [
        State('sarep_degree_programs_id', 'value'),
        State('sarep_currentdate', 'date'),
        State('sarep_file', 'contents'),
        State('sarep_file', 'filename'),  
        State('sarep_link', 'value'),
        State('sarep_checkstatus', 'value'),
        State('sarep_datereviewed', 'value'),
        State('sarep_assessedby', 'value'),
        State('sarep_review_status', 'value'),
        State('sarep_notes', 'value'),
        State('sarep_sarscore', 'value'),
        State('url', 'search')
    ]
)
def record_sar_details(submitbtn, closebtn, removerecord,
                        sarep_degree_programs_id, sarep_currentdate,
                        sarep_file_contents, sarep_file_names, sarep_link,  
                        sarep_checkstatus, sarep_datereviewed, 
                        sarep_assessedby, sarep_review_status, sarep_notes, sarep_sarscore,
                        search):
    
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'sarep_save_button' or not submitbtn:
        raise PreventUpdate

    # Initialize default response values
    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''
    feedbackmessage = None
    okay_href = None

    # Parse URL for mode
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    # Helper function to process file contents
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
        # Validate required fields
        if not all([sarep_degree_programs_id, sarep_checkstatus]):
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            return [alert_color, alert_text, True, modal_open, feedbackmessage, okay_href]

        if sarep_file_contents is None or sarep_file_names is None:
            sarep_file_contents = ["1"]
            sarep_file_names = ["1"]
 
        sarep_file_data, error = process_files(sarep_file_contents, sarep_file_names)
        if error:
            alert_open = True
            alert_color = 'danger'
            alert_text = error
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        # SQL insertion
        sql = """
            INSERT INTO eqateam.sar_report (
                sarep_degree_programs_id, sarep_currentdate, 
                sarep_file_path, sarep_file_name, sarep_file_type, sarep_file_size,
                sarep_link, sarep_checkstatus, sarep_datereviewed, sarep_assessedby,
                sarep_review_status, sarep_notes, sarep_sarscore
            )
            VALUES (%s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s)
        """
        values = (
            sarep_degree_programs_id, sarep_currentdate,
            sarep_file_data[0]["path"] if sarep_file_data else None,
            sarep_file_data[0]["name"] if sarep_file_data else None,
            sarep_file_data[0]["type"] if sarep_file_data else None,
            sarep_file_data[0]["size"] if sarep_file_data else None,
            sarep_link, sarep_checkstatus, sarep_datereviewed, sarep_assessedby,
            sarep_review_status, sarep_notes, sarep_sarscore
        ) 

        db.modifydatabase(sql, values)
        modal_open = True
        feedbackmessage = html.H5("New SAR report submitted successfully.")
        okay_href = "/assessment_reports"

    elif create_mode == 'edit': 
        sarepid = parse_qs(parsed.query).get('id', [None])[0]
        
        if sarepid is None:
            raise PreventUpdate
        
        # SQL update
        sqlcode = """
            UPDATE eqateam.sar_report
            SET
                sarep_checkstatus = %s,
                sarep_datereviewed = %s,
                sarep_review_status = %s,
                sarep_assessedby = %s,
                sarep_notes = %s,
                sarep_sarscore = %s,
                sarep_del_ind  = %s
            WHERE 
                sarep_id = %s
        """
        to_delete = bool(removerecord) 

        values = [sarep_checkstatus, sarep_datereviewed, sarep_review_status,
                sarep_assessedby, sarep_notes, sarep_sarscore, to_delete, sarepid]
        db.modifydatabase(sqlcode, values)

        feedbackmessage = html.H5("Status has been updated.")
        okay_href = "/assessment_reports"
        modal_open = True

    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]



    

@app.callback(
    [ 
        Output('sarep_degree_programs_id', 'value'),
        Output('sarep_currentdate', 'value'), 
        Output('sarep_file', 'filename'), 
        Output('sarep_link', 'value'),
        Output('sarep_checkstatus', 'value'),
        Output('sarep_datereviewed', 'value'),
        Output('sarep_assessedby', 'value'),
        Output('sarep_review_status', 'value'),
        Output('sarep_notes', 'value'),
        Output('sarep_sarscore', 'value'), 
    ],
    [  
        Input('sarep_toload', 'modified_timestamp')
    ],
    [
        State('sarep_toload', 'data'),
        State('url', 'search')
    ]
)
def sarep_load(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        sarepid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                sarep_degree_programs_id, sarep_currentdate, 
                sarep_file_name, 
                sarep_link, sarep_checkstatus, sarep_datereviewed, sarep_assessedby,
                sarep_review_status, sarep_notes, sarep_sarscore
            FROM eqateam.sar_report
            WHERE sarep_id = %s
        """
        values = [sarepid]

        cols = [
                'sarep_degree_programs_id', 'sarep_currentdate', 
                'sarep_file_name', 
                'sarep_link', 'sarep_checkstatus', 'sarep_datereviewed', 'sarep_assessedby',
                'sarep_review_status', 'sarep_notes', 'sarep_sarscore'  
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        
        sarep_degree_programs_id = int(df['sarep_degree_programs_id'][0])
        sarep_currentdate = df['sarep_currentdate'][0]
        sarep_file_name = df['sarep_file_name'][0]
        sarep_link = df['sarep_link'][0]
        sarep_checkstatus = df['sarep_checkstatus'][0]
        sarep_datereviewed = df['sarep_datereviewed'][0]
        sarep_assessedby = df['sarep_assessedby'][0]
        sarep_review_status = df['sarep_review_status'][0]
        sarep_notes = df['sarep_notes'][0] 
        sarep_sarscore = df['sarep_sarscore'][0] 
        
        return [sarep_degree_programs_id, sarep_currentdate, 
                sarep_file_name, 
                sarep_link, sarep_checkstatus, sarep_datereviewed, sarep_assessedby,
                sarep_review_status, sarep_notes, sarep_sarscore
                ]
    
    else:
        raise PreventUpdate


 
@app.callback(
    [ 
        Output('sarep_degree_programs_id', 'disabled'), 
        Output('sarep_currentdate', 'disabled'),  
        Output('sarep_file', 'disabled'),  
        Output('sarep_link', 'disabled'),  
    ],
    [Input('url', 'search')]
)
def sarep_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 4
    return [False] * 4
