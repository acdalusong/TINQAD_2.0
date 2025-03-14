import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db 

import base64
import os
from urllib.parse import urlparse, parse_qs

UPLOAD_DIRECTORY = r".\assets\database\admin\trainings"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Complete Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", 
                              id='complete_name', 
                              placeholder="Last Name, First Name, Middle Initial",
                              disabled=False
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
                        "Position ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='fac_posn_name',
                        options=[],
                        placeholder="Select position",
                        disabled=False
                        
                    ),
                    width=4,
                ), 
                dbc.Col(
                    dbc.Input(id="fac_posn_number", type="text", 
                              placeholder="Number",
                              disabled=False),
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
                    dbc.Input(id="add_training_fac_posn", type="text", placeholder="Faculty position not in list?"),
                    width=6,
                ),
                dbc.Col(
                    dbc.Button("➕", color="primary",  id="add_training_save_button", n_clicks=0),
                        width="auto"
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
                       id='cluster_id',
                       placeholder="Select Cluster",
                       disabled=False
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
                       id='college_id',
                       placeholder="Select College",
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
                        "Department ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='deg_unit_id',
                        placeholder="Select Department",
                        disabled=False
                    ),
                    width=8,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Label(
                    "TRAINING DETAILS",
                    width=8,
                    style={"font-size": "20px", "font-weight": "bold"}  # Style for larger and bold font
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "QA Training Attended ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='qa_training_id',
                        options=[],
                        placeholder="Select QA Training"
                    ),
                    width=6,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Other QA Training Attended:", 
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='qa_training_other', placeholder="Other: Training Name"),
                    width=6,
                ),
            ],
            className="mb-1",
        ),
        
        dbc.Row(
           [
               dbc.Label(
                   [
                       "Date of Departure ",
                        html.Span("*", style={"color": "#F8B237"})
                   ],
                   width=4
               ),
               dbc.Col(
                   dcc.DatePickerSingle(
                       id='departure_date',
                       date=str(pd.to_datetime("today").date()),
                       className='SingleDatePicker'
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
                       "Date of Return ",
                        html.Span("*", style={"color": "#F8B237"})
                   ],
                   width=4
               ),
               dbc.Col(
                   dcc.DatePickerSingle(
                       id='return_date',
                       date=str(pd.to_datetime("today").date()),
                       className='SingleDatePicker'
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
                        "Training Venue/Location ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='venue', placeholder="Venue Name, City, Country"),
                    width=8,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Label(
                    "LIQUIDATION REQUIREMENTS",
                    width=12,
                    className="mb-2",
                    style={"font-size": "20px", "font-weight": "bold"}  # Style for larger and bold font
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Certificate of Participation/Attendance ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='pacert',
                        children=html.Div(
                            [
                                'Drag and Drop or Select Files',
                            ], 
                        ),
                        style={
                            'width': '100%', 'height': '30px',  'lineHeight': '30px',
                            'borderWidth': '1px', 'borderStyle': 'dashed',
                            'borderRadius': '5px', 'textAlign': 'center', 
                        },
                        multiple=True
                    ),
                    width=6
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [dbc.Label("",width=6),
             dbc.Col(id="pacert_output",style={"color": "#F8B237"}, width="auto")],  # Output area for uploaded file names
            className="mt-0",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Official Receipt of Training Attended ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='orcert',
                        children=html.Div(
                            [
                                'Drag and Drop or Select Files',
                            ], 
                        ),
                        style={
                            'width': '100%', 'height': '30px',  'lineHeight': '30px',
                            'borderWidth': '1px', 'borderStyle': 'dashed',
                            'borderRadius': '5px', 'textAlign': 'center', 
                        },
                        multiple=True 
                    ),
                    width=6
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [dbc.Label("",width=6),
            dbc.Col(id="orcert_output",style={"color": "#F8B237"}, width="auto")],  # Output area for uploaded file names
            className="mt-0",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Official Travel Report ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='otrcert',
                        children=html.Div(
                            [
                                'Drag and Drop or Select Files',
                            ], 
                        ),
                        style={
                            'width': '100%', 'height': '30px',  'lineHeight': '30px',
                            'borderWidth': '1px', 'borderStyle': 'dashed',
                            'borderRadius': '5px', 'textAlign': 'center', 
                        },
                        multiple=True
                    ),
                    width=6
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [dbc.Label("",width=6),
            dbc.Col(id="otrcert_output",style={"color": "#F8B237"}, width="auto")],  # Output area for uploaded file names
            className="mt-0",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Other Receipts "
                    ],
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='others',
                        children=html.Div(
                            [
                                'Drag and Drop or Select Files',
                            ], 
                        ),
                        style={
                            'width': '100%', 'height': '30px',  'lineHeight': '30px',
                            'borderWidth': '1px', 'borderStyle': 'dashed',
                            'borderRadius': '5px', 'textAlign': 'center', 
                        },
                        multiple=True 
                    ),
                    width=6
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [dbc.Label("",width=6),
             dbc.Col(id="others_output",style={"color": "#F8B237"}, width="auto")],  # Output area for uploaded file names
            className="mt-0",
        ),

        dbc.Row(
            [
                dbc.Label(
                    "Receiving Copy (Optional) ",
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='recert',
                        children=html.Div(
                            [
                                'Drag and Drop or Select Files',
                            ], 
                        ),
                        style={
                            'width': '100%', 'height': '30px',  'lineHeight': '30px',
                            'borderWidth': '1px', 'borderStyle': 'dashed',
                            'borderRadius': '5px', 'textAlign': 'center', 
                        },
                        multiple=True
                    ),
                    width=6
                ),
            ],
            className="mb-1",
        ),

        dbc.Row(
            [dbc.Label("",width=6),
             dbc.Col(id="recert_output",style={"color": "#F8B237"}, width="auto")],  
            className="mt-0",
        ),

        

   ],
   className="g-2",
)


# Callback to display the names of the uploaded files
@app.callback(
    Output("pacert_output", "children"),
    [Input("pacert", "filename")],  # Use filename to get uploaded file names
)
def display_partiattendence_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"📑 {file_names_str}"
 
    return f"📑 {filenames}"


@app.callback(
    Output("orcert_output", "children"),
    [Input("orcert", "filename")],  # Use filename to get uploaded file names
)
def display_receipt_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"📑{file_names_str}"
 
    return f"📑{filenames}"

 
@app.callback(
    Output("otrcert_output", "children"),
    [Input("otrcert", "filename")],  # Use filename to get uploaded file names
)
def display_travelreport_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"📑 {file_names_str}"
 
    return f"📑 {filenames}"

 
@app.callback(
    Output("others_output", "children"),
    [Input("others", "filename")],  # Use filename to get uploaded file names
)
def display_otherreport_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"📑 {file_names_str}"
 
    return f"📑{filenames}"

 
@app.callback(
    Output("recert_output", "children"),
    [Input("recert", "filename")],  # Use filename to get uploaded file names
)
def display_receivingcopy_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"📑 {file_names_str}"
 
    return f"📑 {filenames}"

 
#faculty positions dropdown
@app.callback(
    Output('fac_posn_name', 'options'),
    Input('url', 'pathname')
)

def populate_facultypositions_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/training_documents':
        sql = """
        SELECT fac_posn_name as label, fac_posn_name  as value
        FROM public.fac_posns
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        fac_posns_types = df.to_dict('records')
        return fac_posns_types
    else:
        raise PreventUpdate


#college dropdown
@app.callback(
    Output('college_id', 'options'),
    Input('cluster_id', 'value')
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
        
        college_options = df.to_dict('records')
        return college_options
    except Exception as e: 
        return [] 


# dgu dropdown
@app.callback(
    Output('deg_unit_id', 'options'), 
    Input('college_id', 'value')
)
def populate_dgu_dropdown(selected_college):
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
    

#qa training dropdown
@app.callback(
    Output('qa_training_id', 'options'),
    Input('url', 'pathname')
)
def populate_qatrainings_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/training_documents':
        sql = """
        SELECT trainingtype_name as label, trainingtype_id as value
        FROM qaofficers.training_type
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qa_training_options = df.to_dict('records')
        return qa_training_options
    else:
        raise PreventUpdate


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                [
                    html.Div(  
                            [
                                dcc.Store(id='trainingdocuments_toload', storage_type='memory', data=0),
                                dcc.Store(id='loaded_cluster_id', storage_type='memory'),
                                dcc.Store(id='loaded_college_id', storage_type='memory'),
                                dcc.Store(id='loaded_deg_unit_id', storage_type='memory'),
                            ]
                        ),

                    html.H1(id="training_documents_header"),
                    html.Hr(),
                    dbc.Alert(id='trainingdocuments_alert', is_open=False), # For feedback purpose
                    form, 
                    
                    html.Br(),   
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Label("Wish to delete?", width=4),
                                dbc.Col(
                                    dbc.Checklist(
                                        id='trainingdocuments_removerecord',
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
                        id='trainingdocuments_removerecord_div'
                    ),

                    html.Br(),
                    dbc.Row(
                        [ 
                            
                            dbc.Col(
                                dbc.Button("Save", color="primary",  id="trainingdocuments_save_button", n_clicks=0),
                                width="auto"
                            ),
                            dbc.Col(
                                dbc.Button("Cancel", color="warning", id="trainingdocuments_cancel_button", n_clicks=0, href="/training_record"),  
                                width="auto"
                            ),
                        ],
                        className="mb-2",
                        justify="end",
                    ),

                    
                    dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='trainingdocuments_confirmmodal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="trainingdocuments_cancel", color="warning"),
                                            dbc.Button("Confirm", id="trainingdocuments_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='trainingdocuments_confirmmodal',
                            backdrop="static",   
                        ),

                    # Final Modal for Training Documents
                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3(id="trainingdocuments_finalmodal_header"), close_button=False, className="bg-success"),
                            dbc.ModalBody(html.H5("Click Proceed to continue.")),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Proceed",
                                    href='/training_record',
                                    color="success", 
                                    id='trainingdocuments_finalmodal_btn'
                                ),
                            ),
                        ],
                        centered=True,
                        id='trainingdocuments_finalmodal',
                        backdrop='static',
                        keyboard=False,
                    ),  

                    dbc.Modal(
                            [
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(html.H5(
                                    ['Faculty Position added successfully.'
                                    ],id='add_training_feedback_message'
                                )), 
                                
                            ],
                            centered=True,
                            id='add_training_successmodal',
                            backdrop=True,   
                            className="modal-success"    
                    ),
                     
                ],
                width=8, style={'marginLeft': '15px'}
                
                )
            ]
        ),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ),
        
    ]
)


@app.callback(
    [
        Output('training_documents_header', 'children'),
        Output('cluster_id', 'options'),
        Output('trainingdocuments_toload', 'data'),
        Output('trainingdocuments_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)


def trainingdocuments_loaddropdown(pathname, search):
    if pathname == '/training_documents':
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
        header = "Add Training Document Details" if create_mode == 'add' else "Edit Training Document Details"
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [header, cluster_options, to_load, removediv_style]


@app.callback(
    [
        # Check if all fields are filled
        Output('trainingdocuments_alert', 'is_open'),
        Output('trainingdocuments_alert', 'color'),
        Output('trainingdocuments_alert', 'children'),
        Output('complete_name', 'className'),
        Output('fac_posn_name', 'className'),
        Output('cluster_id', 'className'),
        Output('college_id', 'className'),
        Output('deg_unit_id', 'className'),
        Output('qa_training_id', 'className'),
        Output('departure_date', 'className'),
        Output('return_date', 'className'),
        Output('venue', 'className'),
        # Open confirmation modal
        Output('trainingdocuments_confirmmodal', 'is_open'), 
        Output('trainingdocuments_confirmmodal_message', 'children'),
        # Button Colors Change When in Edit Mode
        Output("trainingdocuments_confirm", "color"),
        # Open success modal
        Output('trainingdocuments_finalmodal', 'is_open'),
        Output('trainingdocuments_finalmodal_header', 'children')
    ],
    [
        Input('trainingdocuments_save_button', 'n_clicks'),
        Input('trainingdocuments_confirm', 'n_clicks'),
        Input('trainingdocuments_cancel', 'n_clicks'),
    ],
    [
        State('trainingdocuments_removerecord', 'value'),
        State('trainingdocuments_confirmmodal', 'is_open'),
        State('complete_name', 'value'),
        State('fac_posn_name', 'value'),
        State('fac_posn_number', 'value'),
        State('cluster_id', 'value'),
        State('college_id', 'value'),
        State('deg_unit_id', 'value'),
        State('qa_training_id', 'value'),
        State('qa_training_other', 'value'),
        State('departure_date', 'date'),
        State('return_date', 'date'),
        State('venue', 'value'),
        
        State('pacert', 'contents'),
        State('pacert', 'filename'),

        State('orcert', 'contents'),
        State('orcert', 'filename'),

        State('otrcert', 'contents'),
        State('otrcert', 'filename'),

        State('others', 'contents'),
        State('others', 'filename'),
        
        State('recert', 'contents'),
        State('recert', 'filename'),
         
        State('url', 'search'),
    ]
)
def record_training_documents(save_clicks, confirm_clicks, cancel_clicks, removerecord, confirmationmodal,
                              complete_name, fac_posn_name, fac_posn_number,
                              cluster_id, college_id, deg_unit_id, qa_training_id,
                              qa_training_other, departure_date, return_date, venue,
                              pacert_contents, pacert_filename,  
                              orcert_contents, orcert_filename, 
                              otrcert_contents, otrcert_filename,  
                              others_contents, others_filename,
                              recert_contents, recert_filename, 
                              search):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    # Set default outputs
    alert_open = False
    alert_color = ''
    alert_text = ''
    complete_name_class = ''
    fac_posn_name_class = ''
    cluster_id_class = ''
    college_id_class = ''
    deg_unit_id_class = ''
    qa_training_id_class = ''
    departure_date_class = ''
    return_date_class = ''
    venue_class = ''
    confirm_modal_open = False
    confirm_message = ''
    btn_color = 'success'
    final_modal_open = False
    final_header = ''

    # Helper to process file uploads (same as your current helper)
    def process_files(contents, filenames):
        file_data = []
        for content, filename in zip(contents, filenames):
            if content == "1" and filename == "1":
                continue
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
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    # If the Save button is clicked, first validate inputs and then open the confirmation modal.
    if eventid == 'trainingdocuments_save_button' and save_clicks:
        # Ensure required fields are filled
        def get_input_class(value):
            return 'red-border' if not value else 'form-control'
        required_fields = [complete_name, fac_posn_name, cluster_id, college_id,
                           deg_unit_id, qa_training_id, departure_date, return_date, venue]
        if not all(required_fields) and not removerecord:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            complete_name_class = get_input_class(complete_name)
            fac_posn_name_class = get_input_class(fac_posn_name)
            cluster_id_class = get_input_class(cluster_id)
            college_id_class = get_input_class(college_id)
            deg_unit_id_class = get_input_class(deg_unit_id)
            qa_training_id_class = get_input_class(qa_training_id)
            departure_date_class = 'SingleDatePicker red-border' if not departure_date else 'SingleDatePicker'
            return_date_class = 'SingleDatePicker red-border' if not return_date else 'SingleDatePicker'
            venue_class = get_input_class(venue)
            
            return [alert_open, alert_color, alert_text, complete_name_class, fac_posn_name_class, cluster_id_class, college_id_class, 
                    deg_unit_id_class, qa_training_id_class, departure_date_class, return_date_class, venue_class,
                    False, '', btn_color,  False, '']
        else: # all inputs are valid
            if create_mode == 'add':
                confirm_message  = "Are you sure you want to add this training document?"
            elif create_mode == 'edit':
                if removerecord:
                    confirm_message = "Are you sure you want to delete this training document record?"
                    btn_color = 'danger'
                else:
                    confirm_message = "Are you sure you want to update this training document record?"
            confirm_modal_open = True
            return [False, '', '', complete_name_class, fac_posn_name_class, cluster_id_class, college_id_class, 
                    deg_unit_id_class, qa_training_id_class, departure_date_class, return_date_class, venue_class,
                    confirm_modal_open, confirm_message, btn_color,
                    False, '']

    elif eventid == 'trainingdocuments_confirm' and confirm_clicks:
        if confirmationmodal:
                if create_mode == 'add':
                    # Process each file upload; if a file group is missing, set default values.
                    if pacert_contents is None or pacert_filename is None:
                        pacert_contents, pacert_filename = ["1"], ["1"]
                    pacert_data, error = process_files(pacert_contents, pacert_filename)
                    if error:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = error
                        return [alert_open, alert_color, alert_text, complete_name_class, fac_posn_name_class, 
                                cluster_id_class, college_id_class, deg_unit_id_class, qa_training_id_class, departure_date_class, 
                                return_date_class, venue_class,confirm_modal_open, confirm_message, btn_color, final_modal_open, final_header]

                    if orcert_contents is None or orcert_filename is None:
                        orcert_contents, orcert_filename = ["1"], ["1"]
                    orcert_data, error = process_files(orcert_contents, orcert_filename)
                    if error:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = error
                        return [alert_open, alert_color, alert_text, complete_name_class, fac_posn_name_class, 
                                cluster_id_class, college_id_class, deg_unit_id_class, qa_training_id_class, departure_date_class, 
                                return_date_class, venue_class,confirm_modal_open, confirm_message, btn_color, final_modal_open, final_header]

                    if otrcert_contents is None or otrcert_filename is None:
                        otrcert_contents, otrcert_filename = ["1"], ["1"]
                    otrcert_data, error = process_files(otrcert_contents, otrcert_filename)
                    if error:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = error
                        return [alert_open, alert_color, alert_text, complete_name_class, fac_posn_name_class, 
                                cluster_id_class, college_id_class, deg_unit_id_class, qa_training_id_class, departure_date_class, 
                                return_date_class, venue_class,confirm_modal_open, confirm_message, btn_color, final_modal_open, final_header]

                    if others_contents is None or others_filename is None:
                        others_contents, others_filename = ["1"], ["1"]
                    others_data, error = process_files(others_contents, others_filename)
                    if error:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = error
                        return [alert_open, alert_color, alert_text, complete_name_class, fac_posn_name_class, 
                                cluster_id_class, college_id_class, deg_unit_id_class, qa_training_id_class, departure_date_class, 
                                return_date_class, venue_class,confirm_modal_open, confirm_message, btn_color, final_modal_open, final_header]

                    if recert_contents is None or recert_filename is None:
                        recert_contents, recert_filename = ["1"], ["1"]
                    recert_data, error = process_files(recert_contents, recert_filename)
                    if error:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = error
                        return [alert_open, alert_color, alert_text, complete_name_class, fac_posn_name_class, 
                                cluster_id_class, college_id_class, deg_unit_id_class, qa_training_id_class, departure_date_class, 
                                return_date_class, venue_class,confirm_modal_open, confirm_message, btn_color, final_modal_open, final_header]

                    sql = """
                        INSERT INTO adminteam.training_documents (
                            complete_name, fac_posn_name, fac_posn_number, cluster_id, college_id, deg_unit_id,
                            qa_training_id, qa_training_other, departure_date, return_date, venue, 
                            pacert_path, pacert_name, pacert_type, pacert_size, 
                            orcert_path, orcert_name, orcert_type, orcert_size,
                            otrcert_path, otrcert_name, otrcert_type, otrcert_size,
                            others_path, others_name, others_type, others_size,
                            recert_path, recert_name, recert_type, recert_size,
                            train_docs_del_ind
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s,  
                            %s, %s, %s, %s, 
                            %s, %s, %s, %s, 
                            %s, %s, %s, %s,
                            %s, %s, %s, %s, 
                            %s, %s, %s, %s,
                            %s  
                        )
                    """
                    values = (
                    complete_name, fac_posn_name, fac_posn_number, cluster_id, college_id, deg_unit_id,
                    qa_training_id, qa_training_other, departure_date, return_date, venue,
                    pacert_data[0]["path"] if pacert_data else None, pacert_data[0]["name"] if pacert_data else None,
                    pacert_data[0]["type"] if pacert_data else None, pacert_data[0]["size"] if pacert_data else None,
                    orcert_data[0]["path"] if orcert_data else None, orcert_data[0]["name"] if orcert_data else None,
                    orcert_data[0]["type"] if orcert_data else None, orcert_data[0]["size"] if orcert_data else None,
                    otrcert_data[0]["path"] if otrcert_data else None, otrcert_data[0]["name"] if otrcert_data else None,
                    otrcert_data[0]["type"] if otrcert_data else None, otrcert_data[0]["size"] if otrcert_data else None,
                    others_data[0]["path"] if others_data else None, others_data[0]["name"] if others_data else None,
                    others_data[0]["type"] if others_data else None, others_data[0]["size"] if others_data else None,
                    recert_data[0]["path"] if recert_data else None, recert_data[0]["name"] if recert_data else None,
                    recert_data[0]["type"] if recert_data else None, recert_data[0]["size"] if recert_data else None,
                    False  # train_docs_del_ind
                    )
                    db.modifydatabase(sql, values)
                    final_header = html.H5("Training document registered successfully.")

                elif create_mode == 'edit':
                    trainingdocumentsid = parse_qs(parsed.query).get('id', [None])[0]
                    if trainingdocumentsid is None:
                        raise PreventUpdate
                    sqlcode = """
                        UPDATE adminteam.training_documents
                        SET
                            qa_training_id = %s, 
                            qa_training_other = %s, 
                            departure_date = %s,
                            return_date = %s,
                            venue = %s,
                            train_docs_timestamp = CURRENT_TIMESTAMP,
                            train_docs_del_ind = %s 
                        WHERE 
                            training_documents_id = %s
                    """
                    to_delete = bool(removerecord)
                    values = [
                        qa_training_id,
                        qa_training_other, departure_date, return_date, venue,
                        to_delete, trainingdocumentsid
                    ]
                    db.modifydatabase(sqlcode, values)
                    final_header = html.H5("Document has been updated.")
                final_modal_open = True
                # After processing, close the confirmation modal.
                return [False, '', '', complete_name_class, fac_posn_name_class, cluster_id_class, college_id_class, 
                    deg_unit_id_class, qa_training_id_class, departure_date_class, return_date_class, venue_class,
                    False, '', btn_color, final_modal_open, final_header]
    # If the Cancel button in the confirmation modal is clicked, simply close the modal.
    elif eventid == 'trainingdocuments_cancel' and cancel_clicks:
        if confirmationmodal:
            return [False, '', '', complete_name_class, fac_posn_name_class, cluster_id_class, college_id_class, 
                    deg_unit_id_class, qa_training_id_class, departure_date_class, return_date_class, venue_class,
                    False, '', btn_color,  False, '']
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('complete_name', 'value'),
        Output('fac_posn_name', 'value'),
        Output('fac_posn_number', 'value'),
        Output('loaded_cluster_id', 'data'),
        Output('loaded_college_id', 'data'),
        Output('loaded_deg_unit_id', 'data'),
        Output('qa_training_id', 'value'),
        Output('qa_training_other', 'value'),
        Output('departure_date', 'date'),
        Output('return_date', 'date'),
        Output('venue', 'value'),
        Output('pacert', 'filename'),
        Output('orcert', 'filename'),
        Output('otrcert', 'filename'),
        Output('others', 'filename'),
        Output('recert', 'filename'),
    ],
    [  
        Input('trainingdocuments_toload', 'modified_timestamp')
    ],
    [
        State('trainingdocuments_toload', 'data'),
        State('url', 'search')
    ]
)
def trainingdocuments_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        trainingdocumentsid = parse_qs(parsed.query)['id'][0]
        if not trainingdocumentsid:
            raise PreventUpdate
 
        sql = """
            SELECT 
                complete_name, fac_posn_name, fac_posn_number, cluster_id, college_id, deg_unit_id,
                qa_training_id, qa_training_other, departure_date, return_date, venue, 
                pacert_name as pacert, orcert_name as orcert, otrcert_name as otrcert, 
                others_name as others, recert_name as recert
            FROM adminteam.training_documents
            WHERE training_documents_id = %s
        """
        values = [trainingdocumentsid]

        cols = [
            'complete_name', 'fac_posn_name', 'fac_posn_number', 'cluster_id', 'college_id', 'deg_unit_id',
            'qa_training_id', "qa_training_other" , 'departure_date', 'return_date', 'venue', 
            'pacert', 'orcert', 'otrcert', 'others', 'recert' 
        ]
         
        df = db.querydatafromdatabase(sql, values, cols)
        
        complete_name = df['complete_name'][0]
        fac_posn_name = df['fac_posn_name'][0]
        fac_posn_number = df['fac_posn_number'][0]
        cluster_id = int(df['cluster_id'][0])
        college_id = int(df['college_id'][0])
        deg_unit_id = int(df['deg_unit_id'][0])
        qa_training_id = int(df['qa_training_id'][0])
        qa_training_other = df['qa_training_other'][0]
        departure_date = df['departure_date'][0]
        return_date = df['return_date'][0]
        venue = df['venue'][0]
        pacert = df['pacert'][0]  
        orcert = df['orcert'][0]
        otrcert = df['otrcert'][0]
        others = df['others'][0]
        recert = df['recert'][0] 
        
        return [complete_name, fac_posn_name, fac_posn_number, cluster_id, college_id, deg_unit_id, 
                            qa_training_id, qa_training_other , departure_date, return_date, venue, 
                            pacert, orcert, otrcert, others, recert]
    
    else:
        raise PreventUpdate


@app.callback(
    Output('cluster_id', 'value'),
    [Input('cluster_id', 'options'),  # Trigger when options are loaded
     Input('loaded_cluster_id', 'data')]  # Loaded cluster_id from store
)
def set_cluster_value(cluster_options, loaded_cluster_id):
    if cluster_options and loaded_cluster_id is not None:
        # Check if loaded_cluster_id exists in the current options
        cluster_values = [option['value'] for option in cluster_options]
        if loaded_cluster_id in cluster_values:
            return loaded_cluster_id
    return dash.no_update  # Prevent update if conditions aren't met

@app.callback(
    Output('college_id', 'value'),
    [Input('college_id', 'options'),
     Input('loaded_college_id', 'data')],
)
def set_college_value(college_options, loaded_college_id):
    if college_options and loaded_college_id is not None:
        college_values = [option['value'] for option in college_options]
        if loaded_college_id in college_values:
            return loaded_college_id
    return dash.no_update

@app.callback(
    Output('deg_unit_id', 'value'),
    [Input('deg_unit_id', 'options'),
     Input('loaded_deg_unit_id', 'data')],
)
def set_deg_unit_value(deg_unit_options, loaded_deg_unit_id):
    if deg_unit_options and loaded_deg_unit_id is not None:
        deg_unit_values = [option['value'] for option in deg_unit_options]
        if loaded_deg_unit_id in deg_unit_values:
            return loaded_deg_unit_id
    return dash.no_update

@app.callback(
    [  
        Output('complete_name', 'disabled'),
        Output('fac_posn_name', 'disabled'),
        Output('fac_posn_number', 'disabled'),
        Output('cluster_id', 'disabled'),
        Output('college_id', 'disabled'),
        Output('deg_unit_id', 'disabled'), 
        Output('add_training_fac_posn', 'disabled'), 
        Output('pacert', 'disabled'),
        Output('orcert', 'disabled'),
        Output('otrcert', 'disabled'), 
        Output('others', 'disabled'), 
        Output('recert', 'disabled'), 
    ],
    [Input('url', 'search')]
)
def training_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 12
    return [False] * 12


@app.callback(
    [Output('add_training_successmodal', 'is_open')],
    [Input('add_training_save_button', 'n_clicks')],
    [State('add_training_fac_posn', 'value'), 
     State('url', 'search')]
)
 
def register_training_unithead(submitbtn, add_training_fac_posn, search):
    if submitbtn:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]

        if create_mode == 'add' and add_training_fac_posn:
            sql = """
                INSERT INTO public.fac_posns (fac_posn_name)
                VALUES (%s)
            """
            values = (add_training_fac_posn,)
            db.modifydatabase(sql, values)
            return [True]  
    raise PreventUpdate
