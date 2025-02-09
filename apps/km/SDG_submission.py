import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, no_update
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
UPLOAD_DIRECTORY = r".\assets\database\km"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

 

 
  
# Form layout with improvements
form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    ["Ranking Body", html.Span("*", style={"color": "#F8B237"})],
                    width=4,
                ),
                dbc.Col(
                    dbc.Select(
                        id='sdg_rankingbody',  
                        value=1,
                        disabled=False
                    ),
                    width=5,
                ), 
            ], 
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Evidence Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id="sdg_evidencename",  
                              placeholder="YearSDG_EvidenceName", disabled=False ),
                    width=6,
                ),
                
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label( "",width=4),
                dbc.Col(
                    html.P("e.g. 2024SDG_EvidenceForHealth", style={"color": "#F8B237"}),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Description about the evidence ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Textarea(id="sdg_description",placeholder="Enter Description", 
                                disabled=False ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Please indicate ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='selection_type',
                        options=[
                            {"label": "Office", "value": "office"},
                            {"label": "Department", "value": "department"},
                        ],
                        placeholder="Select Office or Department",
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
                        "Office ",
                         
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdg_office_id', 
                        disabled=True
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
                         
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdg_deg_unit_id',
                        disabled=True 
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
                        "Accomplished By ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id="sdg_accomplishedby", 
                              placeholder="Name Surname" ,
                              disabled=False), 
                              
                    width=4,
                ),
            ],
            className="mb-2",
        ),
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Date ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='sdg_datesubmitted',
                        date=str(pd.to_datetime("today").date()),  # Today's date by default 
                        clearable=True,
                        disabled=False
                        
                    ),
                    width=4,
                ),
            ],
            className="mb-2"
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Check Status ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdg_checkstatus',  
                        options=[
                            {"label": "Pending", "value": '1'},
                            {"label": "Approved", "value": '2'},
                            {"label": "For Revisions", "value": '3'},
                              
                        ],
                        value='1',
                        disabled=False
                        
                    ),
                    width=4,
                ),
 
            ],
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Notes for revision",
                    ],
                    width=4),
                dbc.Col(
                    dbc.Textarea(id="sdg_notes",placeholder="Enter notes for revision", 
                                disabled=True ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Submission Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='submission_type',
                        options=[
                            {"label": "File", "value": "file"},
                            {"label": "Link", "value": "link"},
                            {"label": "Both File and Link", "value": "both"},
                            
                        ],
                        placeholder="Select Submission Type",
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
                        "File Submissions ",
                        
                    ],
                    width=4,
                ),
                dbc.Col(
                    dcc.Upload(
                        id="sdg_file",
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
                        multiple=True,  # Enable multiple file uploads
                        disabled=False
                        
                    ),
                    width=6,
                ),
                
            ],
            className="mb-2",
        ),

        dbc.Row(
            [dbc.Label("",width=6),
             dbc.Col(id="sdg_file_output",style={"color": "#F8B237"}, width="auto")],  # Output area for uploaded file names
            className="mt-0",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link Submissions ", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text",id="sdg_link", placeholder="Enter Link",
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
                        "Add Applicable Criteria ", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Checklist(
                        id="sdg_applycriteria", 
                        value=[],  # Initial empty value, can be pre-filled if desired
                        inline=True, 
                        
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
         
    ],
    className="g-2",
)


# office dropdown
@app.callback(
    Output('sdg_office_id', 'options'),
    Input('url', 'pathname')
)
def populate_office_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT office_name as label, office_id as value
        FROM maindashboard.offices
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        office_types = df.to_dict('records')
        return office_types
    else:
        raise PreventUpdate

# depts dropdown
@app.callback(
    Output('sdg_deg_unit_id', 'options'),
    Input('url', 'pathname')
)
def populate_depts_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT deg_unit_name as label, deg_unit_id as value
        FROM  public.deg_unit
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        depts_types = df.to_dict('records')
        return depts_types
    else:
        raise PreventUpdate





 
# sdg criteria checklist
@app.callback(
    Output('sdg_applycriteria', 'options'),
    Input('url', 'pathname')
)
def populate_applycriteria_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT sdgcriteria_code as label, sdgcriteria_id   as value
        FROM kmteam.SDGCriteria
        WHERE sdgcriteria_del_ind IS FALSE
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        applycriteria_types = df.to_dict('records')
        return applycriteria_types
    else:
        raise PreventUpdate

# Callback to handle enabling/disabling office and department dropdowns based on selection_type
@app.callback(
    [Output('sdg_office_id', 'disabled'),
     Output('sdg_deg_unit_id', 'disabled')],
    [Input('selection_type', 'value')]
)
def toggle_dropdowns(selection_type):
    if selection_type == 'office':
        return False, True  
    elif selection_type == 'department':
        return True, False 
    return True, True 


@app.callback(
    Output('sdg_notes', 'disabled'),
    [Input('sdg_checkstatus', 'value')]
)
def toggle_notes_input(check_status_id):
    if check_status_id == '3':
        return False
    return True











# Callback to handle enabling/disabling file and link submissions based on submission_type
@app.callback(
    [Output('sdg_file', 'disabled'),
     Output('sdg_link', 'disabled')],
    [Input('submission_type', 'value')]
)
def toggle_submissions(submission_type):
    if submission_type == 'file':
        return False, True  # Enable File, Disable Link
    elif submission_type == 'link':
        return True, False  # Disable File, Enable Link
    elif submission_type == 'both':
        return False, False  # Enable both
    return True, True  # Disable both by default

# Callback to display the names of the uploaded files
@app.callback(
    Output("sdg_file_output", "children"),
    [Input("sdg_file", "filename")],  # Use filename to get uploaded file names
)
def display_uploaded_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list):
        # If multiple files are uploaded, join their names
        file_names_str = ", ".join(filenames)
        return f"📑{file_names_str}"

    # For single file upload, return the file name directly
    return f"📑{filenames}"


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
                                dcc.Store(id='sdgsubmission_toload', storage_type='memory', data=0),
                            ]
                        ),
                        
                        html.H1("ADD NEW SDG SUBMISSION"),
                        html.Hr(),
                        html.Br(),
                        dbc.Alert(id="sdgsubmission_alert", is_open=False),  # Alert for feedback
                        form,
                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='sdgsubmission_removerecord',
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
                            id='sdgsubmission_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="sdgsubmission_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="sdgsubmission_cancel_button", n_clicks=0, href="/SDG_evidencelist"),  
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
                                    ['New evidence submitted successfully.'
                                    ],id='sdgsubmission_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='SDG_evidencelist', id='sdgsubmission_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='sdgsubmission_successmodal',
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
        Output('sdg_rankingbody', 'options'),
        Output('sdgsubmission_toload', 'data'),
        Output('sdgsubmission_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)

def ranking_body_loaddropdown(pathname, search):
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
            SELECT ranking_body_name  as label, ranking_body_id  as value
            FROM kmteam.ranking_body
            
            WHERE ranking_body_expense_del_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        ranking_body_options = df.to_dict('records')
        
        
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [ranking_body_options, to_load, removediv_style]





@app.callback(
    [
        Output('sdgsubmission_alert', 'color'),
        Output('sdgsubmission_alert', 'children'),
        Output('sdgsubmission_alert', 'is_open'),
        Output('sdgsubmission_successmodal', 'is_open'),
        Output('sdgsubmission_feedback_message', 'children'),
        Output('sdgsubmission_btn_modal', 'href')
    ],
    [
        Input('sdgsubmission_save_button', 'n_clicks'),
        Input('sdgsubmission_btn_modal', 'n_clicks'),
        Input('sdgsubmission_removerecord', 'value')
    ],
    [
        State('sdg_rankingbody', 'value'),
        State('sdg_evidencename', 'value'),
        State('sdg_description', 'value'),
        State('sdg_office_id', 'value'),
        State('sdg_deg_unit_id', 'value'),
        State('sdg_accomplishedby', 'value'),
        State('sdg_datesubmitted', 'date'), 
        State('sdg_checkstatus', 'value'), 
        State('sdg_notes', 'value'), 
        State('sdg_file', 'contents'),
        State('sdg_file', 'filename'),  
        State('sdg_link', 'value'), 
        State('sdg_applycriteria', 'value'), 
        State('url', 'search')
    ]
)
def record_SDGsubmission(submitbtn, closebtn, removerecord,
                         sdg_rankingbody, sdg_evidencename, sdg_description,
                         sdg_office_id, sdg_deg_unit_id, sdg_accomplishedby, sdg_datesubmitted, 
                         sdg_checkstatus,sdg_notes,
                         sdg_file_contents, sdg_file_names, sdg_link, sdg_applycriteria,
                         search):
    
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'sdgsubmission_save_button' or not submitbtn:
        raise PreventUpdate

    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''
    feedbackmessage = None
    okay_href = None

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    if create_mode == 'add':
        # Ensure required fields are filled
        if not all([sdg_rankingbody, sdg_evidencename, sdg_accomplishedby]):
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            return [alert_color, alert_text, True, modal_open, feedbackmessage, okay_href]

        try:
            check_existing_name_sql = """
                SELECT 1 
                FROM kmteam.SDGSubmission 
                WHERE sdg_evidencename = %s
            """
            existing_name = db.querydatafromdatabase(check_existing_name_sql, (sdg_evidencename,), ["exists"])

            if not existing_name.empty:
                alert_color = 'danger'
                alert_text = 'The Evidence Name already exists. Please choose a unique name.'
                return [alert_color, alert_text, True, modal_open, feedbackmessage, okay_href]

        except Exception as e:
            alert_color = 'danger'
            alert_text = f'Error checking for existing evidence name: {e}'
            return [alert_color, alert_text, True, modal_open, feedbackmessage, okay_href]

        if sdg_file_contents is None or sdg_file_names is None:
            sdg_file_contents = ["1"]
            sdg_file_names = ["1"]

        # Process the files if there are any
        file_data = []
        if sdg_file_contents and sdg_file_names:
            for content, filename in zip(sdg_file_contents, sdg_file_names):
                if content == "1" and filename == "1":
                    continue  # Skip default "1" value
                try:
                    # Decode and save the file
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
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = f'Error processing file: {e}'
                    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        sql = """
            INSERT INTO kmteam.SDGSubmission (
                sdg_rankingbody, sdg_evidencename,
                sdg_description, sdg_office_id, sdg_deg_unit_id,
                sdg_accomplishedby, sdg_datesubmitted, sdg_checkstatus, sdg_notes,
                sdg_link, sdg_applycriteria,
                sdg_file_path, sdg_file_name, sdg_file_type, sdg_file_size
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        values = (
            sdg_rankingbody, sdg_evidencename, sdg_description, sdg_office_id,
            sdg_deg_unit_id, sdg_accomplishedby, sdg_datesubmitted, sdg_checkstatus,sdg_notes,
            sdg_link,
            json.dumps(sdg_applycriteria) if sdg_applycriteria else None,
            file_data[0]["path"] if file_data else None,
            file_data[0]["name"] if file_data else None,
            file_data[0]["type"] if file_data else None,
            file_data[0]["size"] if file_data else None,
        )

        db.modifydatabase(sql, values)
        modal_open = True
        feedbackmessage = html.H5("New evidence submitted successfully.")
        okay_href = "/SDG_evidencelist"

    elif create_mode == 'edit': 
        sdgsubmissionid = parse_qs(parsed.query).get('id', [None])[0]
        
        if sdgsubmissionid is None:
            raise PreventUpdate
        
        sqlcode = """
            UPDATE kmteam.SDGSubmission
            SET
                sdg_checkstatus = %s,
                sdg_notes = %s, 
                sdg_applycriteria = %s, 
                sdg_del_ind = %s

            WHERE 
                sdgsubmission_id = %s
        """
        to_delete = bool(removerecord) 

        values = [
            sdg_checkstatus, 
            sdg_notes, 
            json.dumps(sdg_applycriteria) if sdg_applycriteria else None,
                    
            to_delete, 
            sdgsubmissionid]
        db.modifydatabase(sqlcode, values)

        feedbackmessage = html.H5("Status has been updated.")
        okay_href = "/SDG_evidencelist"
        modal_open = True

    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]





 

    

@app.callback(
    [ 
        Output('sdg_rankingbody', 'value'),
        Output('sdg_evidencename', 'value'),
        Output('sdg_description', 'value'),
        Output('sdg_office_id', 'value'),
        Output('sdg_deg_unit_id', 'value'),
        Output('sdg_accomplishedby', 'value'),
        Output('sdg_datesubmitted', 'value'), 
        Output('sdg_checkstatus', 'value'), 
        Output('sdg_notes', 'value'), 
        Output('sdg_file', 'filename'),  
        Output('sdg_link', 'value'), 
        Output('sdg_applycriteria', 'value'), 
    ],
    [  
        Input('sdgsubmission_toload', 'modified_timestamp')
    ],
    [
        State('sdgsubmission_toload', 'data'),
        State('url', 'search')
    ]
)
def sdgsubmission_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        sdgsubmissionid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                sdg_rankingbody, sdg_evidencename,
                sdg_description, sdg_office_id, sdg_deg_unit_id,
                sdg_accomplishedby, sdg_datesubmitted, sdg_checkstatus,
                sdg_notes, sdg_file_name, 
                sdg_link, sdg_applycriteria 
            FROM kmteam.SDGSubmission
            WHERE sdgsubmission_id = %s
        """
        values = [sdgsubmissionid]

        cols = [
                'sdg_rankingbody', 'sdg_evidencename',
                'sdg_description', 'sdg_office_id', 'sdg_deg_unit_id',
                'sdg_accomplishedby', 'sdg_datesubmitted', 'sdg_checkstatus', 
                'sdg_notes', 'sdg_file_name' , 
                'sdg_link', 'sdg_applycriteria',
                
        ]

         
        df = db.querydatafromdatabase(sql, values, cols)

        
        sdg_rankingbody = int(df['sdg_rankingbody'][0])
        sdg_evidencename = df['sdg_evidencename'][0]
        sdg_description = df['sdg_description'][0]
        sdg_office_id = df['sdg_office_id'][0]

        sdg_deg_unit_id = df['sdg_deg_unit_id'][0]
        sdg_accomplishedby = df['sdg_accomplishedby'][0]
        sdg_datesubmitted = df['sdg_datesubmitted'][0]
        sdg_checkstatus = df['sdg_checkstatus'][0]
        sdg_notes = df['sdg_notes'][0]
        sdg_file_name = df['sdg_file_name'][0] 

        sdg_link = df['sdg_link'][0]
        sdg_applycriteria = df['sdg_applycriteria'][0]  
        
 

        
        return [sdg_rankingbody, sdg_evidencename, sdg_description, 
                sdg_office_id, sdg_deg_unit_id, sdg_accomplishedby, 
                sdg_datesubmitted, sdg_checkstatus,sdg_notes, sdg_file_name, 
                sdg_link, sdg_applycriteria, 
                ]
    
    else:
        raise PreventUpdate




@app.callback(
    [ 
        Output('sdg_rankingbody', 'disabled'),
        Output('sdg_evidencename', 'disabled'),
        Output('sdg_description', 'disabled'), 
        Output('sdg_accomplishedby', 'disabled'),
        Output('sdg_datesubmitted', 'disabled'),
        Output('selection_type', 'disabled'),
        Output('submission_type', 'disabled'),
  
    ],
    [Input('url', 'search')]
)
def sdg_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 7
    return [False] * 7
