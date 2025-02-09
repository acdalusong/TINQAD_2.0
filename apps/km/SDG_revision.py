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



form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Select Evidence Name", width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdgr_evidencename',
                        options=[],
                        disabled=False, 
                    ),
                    width=4,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Ranking Body", width=4),
                dbc.Col(
                    html.P(id='sdgr_rankingbody'),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Description about the evidence", width=4),
                dbc.Col(
                    html.P(id='sdgr_description'),
                    width=8,
                ),
            ],
            className="mb-3",
        ), 
        dbc.Row(
            [
                dbc.Label("Office", width=4),
                dbc.Col(
                    html.P(id='sdgr_office_id'),
                    width=8,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label("Department", width=4),
                dbc.Col(
                    html.P(id='sdgr_deg_unit_id'),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Revision Notes", width=4),
                dbc.Col(
                    html.P(id='sdgr_checknotes'),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Accomplished by",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),

                dbc.Col(
                    dbc.Input(type="text", placeholder="Name Surname",id='sdgr_accomplishedby', disabled=False),  
                    width=5, 
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Date Submitted", width=4),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='sdgr_datesubmitted',
                        date=str(pd.to_datetime("today").date()),  
                        clearable=True,
                        disabled=False, 
                    ),
                    width=4,
                ),
            ],
            className="mb-3",
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
                        id='sdgr_checkstatus',  
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
                    dbc.Textarea(id="sdgr_notes",placeholder="Enter notes for revision", 
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
                        id='sdgrsubmission_type',
                        options=[
                            {"label": "File", "value": "file"},
                            {"label": "Link", "value": "link"},
                            {"label": "Both File and Link", "value": "both"},
                        ],
                        placeholder="Select Submission Type",
                        disabled=False, 
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
                        id="sdgr_file",
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
                    ),
                    width=6,
                ),
                
            ],
            className="mb-2",
        ),

        dbc.Row(
            [dbc.Label("",width=6),
             dbc.Col(id="sdgr_file_output",style={"color": "#F8B237"}, width=6)],  # Output area for uploaded file names
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link Submissions ", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text",id="sdgr_link", placeholder="Enter Link"),
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
                        id="sdgr_applycriteria", 
                        value=[],  # Initial empty value, can be pre-filled if desired
                        inline=True
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
    ],
    className="g-2",
)



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
                                dcc.Store(id='sdgr_toload', storage_type='memory', data=0),
                            ]
                        ),
                        html.H1("ADD REVISION"),
                        html.Hr(),
                        html.Br(),
                        dbc.Alert(id="sdgr_alert", is_open=False),  # Alert for feedback
                        form,
                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='sdgr_removerecord',
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
                            id='sdgr_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="sdgr_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="sdgr_cancel_button", n_clicks=0, href="/SDG_evidencelist"),  
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
                                    ['Revised evidence submitted successfully.'
                                    ],id='sdgr_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='SDG_evidencelist', id='sdgr_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='sdgr_successmodal',
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





#select evidence name from list of revisions 
@app.callback(
    [
        Output('sdgr_evidencename', 'options'),
        Output('sdgr_toload', 'data'),
        Output('sdgr_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)

def evidence_name_loaddropdown(pathname, search):
    if pathname == '/SDGimpactrankings/SDG_revision':
        sql = """
            SELECT sdg_evidencename as label, sdg_evidencename as value
            FROM kmteam.SDGSubmission
            WHERE sdg_checkstatus = '3' AND sdg_del_ind = FALSE
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        evidence_name_options = df.to_dict('records')
        
        
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [evidence_name_options, to_load, removediv_style]





#ranking body appear
@app.callback(
    Output('sdgr_rankingbody', 'children'),
    [Input('sdgr_evidencename', 'value')]
)

def update_rankingbody_text(selected_evidencename_rb):
    if selected_evidencename_rb is None:
        return ""
    else:
        try: 
            rankingbody = db.get_rankingbody(selected_evidencename_rb)
            if rankingbody:
                return rankingbody
            else:
                return "No ranking body found for this evidence name"
        except Exception as e:
            return "An error occurred while fetching the rankingbody: {}".format(str(e))




#description appear
@app.callback(
    Output('sdgr_description', 'children'),
    [Input('sdgr_evidencename', 'value')]
)

def update_description_text(selected_evidencename_descript):
    if selected_evidencename_descript is None:
        return ""
    else:
        try: 
            description = db.get_sdgrdescription (selected_evidencename_descript)
            if description:
                return description
            else:
                return "No description found for this evidence name"
        except Exception as e:
            return "An error occurred while fetching the description: {}".format(str(e))




#office appear
@app.callback(
    Output('sdgr_office_id', 'children'),
    [Input('sdgr_evidencename', 'value')]
)

def update_office_text(selected_evidencename_office):
    if selected_evidencename_office is None:
        return ""
    else:
        try: 
            office = db.get_sdgroffice (selected_evidencename_office)
            if office:
                return office
            else:
                return ""
        except Exception as e:
            return "An error occurred while fetching the office: {}".format(str(e))


#department appear
@app.callback(
    Output('sdgr_deg_unit_id', 'children'),
    [Input('sdgr_evidencename', 'value')]
)

def update_department_text(selected_evidencename_department):
    if selected_evidencename_department is None:
        return ""
    else:
        try: 
            department = db.get_sdgrdepartment (selected_evidencename_department)
            if department:
                return department
            else:
                return ""
        except Exception as e:
            return "An error occurred while fetching the department: {}".format(str(e))



#notes appear
@app.callback(
    Output('sdgr_checknotes', 'children'),
    [Input('sdgr_evidencename', 'value')]
)

def update_notes_text(selected_evidencename_notes):
    if selected_evidencename_notes is None:
        return ""
    else:
        try: 
            notes = db.get_sdgrnotes (selected_evidencename_notes)
            if notes:
                return notes
            else:
                return ""
        except Exception as e:
            return "An error occurred while fetching the notes: {}".format(str(e))



 
# Callback to open notes
@app.callback(
    Output('sdgr_notes', 'disabled'),
    [Input('sdgr_checkstatus', 'value')]
)
def toggle_sdgrnotes_input(check_sdgrstatus_id):
    if check_sdgrstatus_id == '3':
        return False
    return True





# sdg criteria checklist
@app.callback(
    Output('sdgr_applycriteria', 'options'),
    Input('url', 'pathname')
)
def populate_applysdgrcriteria_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_revision':
        sql = """
        SELECT sdgcriteria_code as label, sdgcriteria_id   as value
        FROM kmteam.SDGCriteria
        WHERE sdgcriteria_del_ind  IS FALSE 
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        applysdgrcriteria_types = df.to_dict('records')
        return applysdgrcriteria_types
    else:
        raise PreventUpdate

 
@app.callback(
    [Output('sdgr_file', 'disabled'),
     Output('sdgr_link', 'disabled')],
    [Input('sdgrsubmission_type', 'value')]
)
def toggle_submissions(sdgrsubmission_type):
    if sdgrsubmission_type == 'file':
        return False, True  
    elif sdgrsubmission_type == 'link':
        return True, False   
    elif sdgrsubmission_type == 'both':
        return False, False   
    return True, True  
 
@app.callback(
    Output("sdgr_file_output", "children"),
    [Input("sdgr_file", "filename")],  
)
def display_uploaded_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"📑{file_names_str}"
 
    return f"📑 {filenames}"



@app.callback(
    [
        Output('sdgr_alert', 'color'),
        Output('sdgr_alert', 'children'),
        Output('sdgr_alert', 'is_open'),
        Output('sdgr_successmodal', 'is_open'),
        Output('sdgr_feedback_message', 'children'),
        Output('sdgr_btn_modal', 'href')
    ],
    [
        Input('sdgr_save_button', 'n_clicks'),
        Input('sdgr_btn_modal', 'n_clicks'),
        Input('sdgr_removerecord', 'value')
    ],
    [
        State('sdgr_evidencename', 'value'),
        State('sdgr_accomplishedby', 'value'),
        State('sdgr_datesubmitted', 'value'), 
        State('sdgr_checkstatus', 'value'), 
        State('sdgr_notes', 'value'),  
        State('sdgr_file', 'contents'),
        State('sdgr_file', 'filename'),  
        State('sdgr_link', 'value'), 
        State('sdgr_applycriteria', 'value'), 
        State('url', 'search')
    ]
)
def record_SDGrevision(submitbtn, closebtn, removerecord,
                       sdgr_evidencename, sdgr_accomplishedby, sdgr_datesubmitted, 
                       sdgr_checkstatus, sdgr_notes,
                       sdgr_file_contents, sdgr_file_names, sdgr_link, sdgr_applycriteria,
                       search):
    
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'sdgr_save_button' or not submitbtn:
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
        if not sdgr_evidencename:
            alert_color = 'danger'
            alert_text = 'Evidence name is required.'
            return [alert_color, alert_text, True, modal_open, feedbackmessage, okay_href]
        
        if sdgr_file_contents is None or sdgr_file_names is None:
            sdgr_file_contents = ["1"]
            sdgr_file_names = ["1"]
        
        # Process the files if there are any
        file_data = []
        if sdgr_file_contents and sdgr_file_names:
            for content, filename in zip(sdgr_file_contents, sdgr_file_names):
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

        # Copy relevant fields from SDGSubmission to SDGRevision
        sql_copy = """
            INSERT INTO kmteam.SDGRevision (
                sdgr_evidencename, sdgr_rankingbody, sdgr_description,
                sdgr_office_id, sdgr_deg_unit_id, sdgr_checknotes,
                sdgr_accomplishedby, sdgr_datesubmitted, sdgr_checkstatus, sdgr_notes,
                sdgr_file_path,  sdgr_file_name,  sdgr_file_type, sdgr_file_size,   
                sdgr_link, sdgr_applycriteria
            )
            SELECT 
                sdg_evidencename, sdg_rankingbody, sdg_description,
                sdg_office_id, sdg_deg_unit_id, sdg_notes,  
                %s, %s, %s, %s,    
                %s, %s, %s, %s,    
                %s, %s    
            FROM kmteam.SDGSubmission
            WHERE sdg_evidencename = %s;
        """

        values_copy = (
            sdgr_accomplishedby, sdgr_datesubmitted, sdgr_checkstatus,
            sdgr_notes,  # This is the check notes in SDGSubmission copied to notes in SDGRevision
            file_data[0]["path"] if file_data else None,
            file_data[0]["name"] if file_data else None,
            file_data[0]["type"] if file_data else None,
            file_data[0]["size"] if file_data else None,
            sdgr_link,
            json.dumps(sdgr_applycriteria) if sdgr_applycriteria else None,  # Convert to JSON
            sdgr_evidencename
        )
        
        try:
            db.modifydatabase(sql_copy, values_copy)
            modal_open = True
            feedbackmessage = html.H5("New evidence submitted successfully.")
            okay_href = "/SDG_evidencelist"
            
        except Exception as e:
            alert_color = 'danger'
            alert_text = f'Error copying record: {e}'
            return [alert_color, alert_text, True, modal_open, feedbackmessage, okay_href]

    elif create_mode == 'edit': 
        sdgrevisionid = parse_qs(parsed.query).get('id', [None])[0]
        
        if sdgrevisionid is None:
            raise PreventUpdate
        
        sqlcode = """
            UPDATE kmteam.SDGRevision
            SET
                sdgr_checkstatus = %s,
                sdgr_notes = %s,
                sdgr_applycriteria = %s, 
                sdgr_del_ind = %s
            WHERE 
                sdgrevision_id = %s
        """
        to_delete = bool(removerecord) 

        values = [
            sdgr_checkstatus, 
            sdgr_notes,  
            json.dumps(sdgr_applycriteria) if sdgr_applycriteria else None,
             
            to_delete, 
            sdgrevisionid
        ] 
        db.modifydatabase(sqlcode, values)

        feedbackmessage = html.H5("Status has been updated.")
        okay_href = "/SDG_evidencelist"
        modal_open = True

    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]


@app.callback(
    [
        Output('sdgr_evidencename', 'value'),
        Output('sdgr_rankingbody', 'value'),
        Output('sdgr_description', 'value'),
        Output('sdgr_office_id', 'value'),
        Output('sdgr_deg_unit_id', 'value'),
        Output('sdgr_checknotes', 'value'),
        Output('sdgr_accomplishedby', 'value'),
        Output('sdgr_datesubmitted', 'value'), 
        Output('sdgr_checkstatus', 'value'), 
        Output('sdgr_notes', 'value'), 
        Output('sdgr_file', 'filename'),  
        Output('sdgr_link', 'value'), 
        Output('sdgr_applycriteria', 'value'), 
    ],
    [
        Input('sdgr_toload', 'modified_timestamp')
    ],
    [
        State('sdgr_toload', 'data'),
        State('url', 'search')
    ]
)
def sdgrevision_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        sdgrevisionid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                sdgr_evidencename, sdgr_rankingbody, 
                sdgr_description, sdgr_office_id, sdgr_deg_unit_id, 
                sdgr_checknotes, 
                sdgr_accomplishedby, sdgr_datesubmitted, sdgr_checkstatus,
                sdgr_notes, sdgr_file_name, 
                sdgr_link, sdgr_applycriteria 
            FROM kmteam.SDGRevision
            WHERE sdgrevision_id = %s
        """
        values = [sdgrevisionid]

        cols = [
            'sdgr_evidencename', 'sdgr_rankingbody', 
            'sdgr_description', 'sdgr_office_id', 'sdgr_deg_unit_id', 
            'sdgr_checknotes', 
            'sdgr_accomplishedby', 'sdgr_datesubmitted', 'sdgr_checkstatus',
            'sdgr_notes', 'sdgr_file_name', 
            'sdgr_link', 'sdgr_applycriteria' 
            
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        sdgr_evidencename = df['sdgr_evidencename'][0]
        sdgr_rankingbody = df['sdgr_rankingbody'][0]
        
        sdgr_description = df['sdgr_description'][0]
        sdgr_office_id = df['sdgr_office_id'][0]

        sdgr_deg_unit_id = df['sdgr_deg_unit_id'][0]
        sdgr_checknotes = df['sdgr_checknotes'][0]
        sdgr_accomplishedby = df['sdgr_accomplishedby'][0]
        sdgr_datesubmitted = df['sdgr_datesubmitted'][0]
        sdgr_checkstatus = df['sdgr_checkstatus'][0]
        sdgr_notes = df['sdgr_notes'][0]
        sdgr_file_name = df['sdgr_file_name'][0]
        
        sdgr_link = df['sdgr_link'][0]
        sdgr_applycriteria = df['sdgr_applycriteria'][0]
         
        

        return [
            sdgr_evidencename,sdgr_rankingbody,
            sdgr_description, sdgr_office_id, sdgr_deg_unit_id,
            sdgr_checknotes, sdgr_accomplishedby,
            sdgr_datesubmitted, sdgr_checkstatus, sdgr_notes,
            sdgr_file_name, sdgr_link, sdgr_applycriteria
        ]

    else:
        raise PreventUpdate
    





@app.callback(
    [ 
        Output('sdgr_evidencename', 'disabled'),
        Output('sdgr_accomplishedby', 'disabled'),
        Output('sdgr_datesubmitted', 'disabled'), 
        Output('sdgrsubmission_type', 'disabled'),
  
    ],
    [Input('url', 'search')]
)
def sdg_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 4
    return [False] * 4
