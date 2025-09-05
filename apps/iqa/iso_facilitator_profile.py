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
        # Surname
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Surname ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="isofaci_sname", type="text", required=False),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
        # First Name
        dbc.Row(
            [
                dbc.Label(
                    [
                        "First Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="isofaci_fname", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
        # Middle Name
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Middle Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="isofaci_mname", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
        # UP Mail
        dbc.Row(
            [
                dbc.Label(
                    [
                        "UP Mail ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="isofaci_upmail", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

       # Unit/Office Type (Checkbox for Administrative or Academic Unit)
        dbc.Row(
            [
                dbc.Label(
                    [
                        "What type of unit/office will you be representing? ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='isofaci_unit_type_id',
                        placeholder= "Select Unit Type"
                        
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        #OCES Group
         dbc.Row(
            [
                dbc.Label(
                    [
                       "Academic Cluster/OCES Group ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='isofaci_cluster_id',
                        placeholder="Select Academic Cluster/OCES Group",
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        #Main Unit
        dbc.Row(
            [
                dbc.Label(
                    [
                       "Main Unit ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='isofaci_college_id',
                        placeholder="Select Main Unit",
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        #Sub-unit
        dbc.Row(
            [
                dbc.Label(
                    [
                       "Sub-unit ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='isofaci_deg_unit_id',
                        placeholder="Select Sub-unit",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        #Faculty Position
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
                        id='isofaci_fac_posn_name',
                        placeholder="Select Position",
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(id="isofaci_fac_posn_number", type="text", placeholder="Number"),
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
                    dbc.Input(id="add_isofaci_fac_posn", type="text",placeholder="Faculty position not in list?"),
                    width=6,
                ),
                dbc.Col(
                    dbc.Button("?", color="primary",  id="add_isofaci_save_button", n_clicks=0),
                        width="auto"
                    ),     
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Faculty Admin Position (if any)", width=4),
                dbc.Col(
                    dbc.Input(id="isofaci_facadmin_posn", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Admin Staff/REPS Position", width=4),
                dbc.Col(
                    dbc.Input(id="isofaci_staff_posn", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Role in the CU-Level QA Committee (Type NA if not applicable)", width=4),
                dbc.Col(
                    dbc.Input(id="isofaci_rolecuqa", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

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
                        id='isofaci_cuposition_id',
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
                       "CQAO/DQAO Level ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='isofaci_cdqao_id',
                        placeholder= "Select CQAO/DQAO Level"
                        
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
                        "Remarks ", 
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id="isofaci_remarks",
                        options=[
                            {"label":"With record","value":"With record"},
                            {"label":"No record","value":"No record"},
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
        dbc.Label("Dietary Restrictions", width=4),
        dbc.Col(
            dbc.Input(id="isofaci_dr", type="text"),
            width=6,
        ),
    ],
    className="mb-2",
),
dbc.Row(
    [
        dbc.Label("Health Concerns / Medical Conditions", width=4),
        dbc.Col(
            dbc.Input(id="isofaci_hc", type="text"),
            width=6,
        ),
    ],
    className="mb-2",
),
dbc.Row(
    [
        dbc.Label("Mobility and Accessibility Needs", width=4),
        dbc.Col(
            dbc.Input(id="isofaci_mn", type="text"),
            width=6,
        ),
    ],
    className="mb-2",
),
dbc.Row(
    [
        dbc.Label("Shirt Size", width=4),
        dbc.Col(
            dbc.Input(id="isofaci_ss", type="text"),
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
                                dcc.Store(id='isofaci_toload', storage_type='memory', data=0),
                            ]
                        ),

                        html.H1("ADD NEW ISO FACILITATOR PROFILE"),
                        html.Hr(),
                        dbc.Alert(id='isofaci_alert', is_open=False),  # For feedback purposes 
                        form,  # This is your form defined earlier
                        
                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='isofaci_removerecord',
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
                            id='isofaci_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary", id="isofaci_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="isofaci_cancel_button", n_clicks=0, href="/iso_facilitator_directory"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),

                        # Success modal for ISO Facilitator profile added
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='iso_faci_confirmation_modal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="iso_faci_confirmation_modal_cancel", color="warning"),
                                            dbc.Button("Confirm", id="iso_faci_confirmation_modal_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='iso_faci_confirmation_modal',
                            backdrop=True,   
                            className="modal-success"    
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id="iso_faci_final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Click Proceed to continue.")),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        href="/iso_facilitator_directory",
                                        color="success", 
                                    ),
                                ),
                            ],
                            centered=True,
                            id='iso_faci_final_modal',
                            backdrop='static',
                            keyboard=False,
                        ),  

                        
                        # Modal for any other success message (e.g., position or office related)
                        dbc.Modal(
                            [
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['Faculty position added successfully.'],
                                    id='add_isofaci_feedback_message'
                                ), 
                            ],
                            centered=True,
                            id='add_isofaci_successmodal',
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

        dbc.Row(
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
    Output('isofaci_fac_posn_name', 'options'),
    Input('url', 'pathname')
)
def populate_fac_posn_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/iso_facilitator_profile':
        sql = """
        SELECT fac_posn_name as label, fac_posn_name  as value
        FROM  public.fac_posns 
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        isofaci_fac_posns_types = df.to_dict('records')
        return isofaci_fac_posns_types
    else:
        raise PreventUpdate

# College dropdown for ISO Facilitator
@app.callback(
    Output('isofaci_college_id', 'options'),
    Input('isofaci_cluster_id', 'value')  # This will now use the college_id value directly
)
def populate_college_dropdown(selected_cluster):
    if selected_cluster is None:
        return []
        
    try:
        # SQL query to fetch all colleges since no cluster filter is needed
        sql = """
        SELECT college_name as label, college_id as value
        FROM public.college
        WHERE cluster_id = %s
        """
        values = [selected_cluster]  # No need to pass any filter value now
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        # Convert the results into the appropriate format for the dropdown
        isofaci_college_options = df.to_dict('records')
        return isofaci_college_options
    except Exception as e:
        # Log the error or handle it appropriately
        # print(f"Error populating college dropdown: {e}")
        return []  # Return an empty list if there's an error


# Degree Unit dropdown
@app.callback(
    Output('isofaci_deg_unit_id', 'options'), 
    Input('isofaci_college_id', 'value')
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


# CU dropdown
@app.callback(
    Output('isofaci_cuposition_id', 'options'),
    Input('url', 'pathname')
)
def populate_cuposition_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/iso_facilitator_profile':
        sql = """
        SELECT cuposition_name as label, cuposition_id  as value
        FROM qaofficers.cuposition
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        isofaci_cuposition_types = df.to_dict('records')
        return isofaci_cuposition_types
    else:
        raise PreventUpdate


# Cluster dropdown
@app.callback(
    [
        Output('isofaci_cluster_id', 'options'),
        # Output('isofaci_toload', 'data'),
        # Output('isofaci_removerecord_div', 'style'),
    ],
    [
        Input('isofaci_unit_type_id', 'value')
    ])

def cluster_dropdown(selected_unit_type):
    if selected_unit_type is None:
        return [[]]
    
    try:
        sql = """
            SELECT cluster_name as label, cluster_id  as value
            FROM public.clusters
            WHERE unit_type_id = %s
        """
        values = [selected_unit_type]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        cluster_options = df.to_dict('records')
        return [cluster_options]
    
    except Exception as e:
        return [[]]
    
@app.callback(
    [
        Output('isofaci_toload', 'data'),
        Output('isofaci_removerecord_div', 'style'),
    ],
    Input('url', 'pathname'),
    State('url', 'search')
)
def load_iso_faci_data(pathname, search):
    if pathname != '/iso_facilitator_profile':
        raise PreventUpdate

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    if create_mode == 'edit':
        return [1, None]  # load data, show remove button
    else:
        return [0, {'display': 'none'}]  # don't load, hide button

    
#unit type 
@app.callback(
    Output('isofaci_unit_type_id', 'options'),
    Input('url', 'pathname'),
    State('url', 'search'),
)
def load_unit_type_options(pathname, search):
    if pathname == '/iso_facilitator_profile':
        sql = """
            SELECT unit_type_name as label, unit_type_id as value
            FROM public.unit_type
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        unit_type_options = df.to_dict('records')
        return unit_type_options
    else:
        raise PreventUpdate

#cqao dqao checkbox
@app.callback(
    Output('isofaci_cdqao_id', 'options'),
    Input('url', 'pathname'),
    State('url', 'search'),
)
def load_cqaodqao_options(pathname, search):
    if pathname == '/iso_facilitator_profile':
        sql = """
            SELECT cdqao_name as label, cdqao_id as value
            FROM public.cdqao
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        cdqao_options = df.to_dict('records')
        return cdqao_options
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('isofaci_alert', 'color'),
        Output('isofaci_alert', 'children'),
        Output('isofaci_alert', 'is_open'),
        # TO ADD NEW CONFIRMATION AND FINAL MODAL
        Output('iso_faci_confirmation_modal', 'is_open'),
        Output('iso_faci_confirmation_modal_message', 'children'),
        Output('iso_faci_final_modal', 'is_open'),
        Output('iso_faci_final_modal_header', 'children'),
        Output('iso_faci_confirmation_modal_confirm', 'color'),
    ],
    [
        Input('isofaci_save_button', 'n_clicks'),
        Input('iso_faci_confirmation_modal_cancel', 'n_clicks'),
        Input('iso_faci_confirmation_modal_confirm', 'n_clicks'),

        Input('isofaci_removerecord', 'value')
    ],
    [
        State('isofaci_fname', 'value'),
        State('isofaci_mname', 'value'),
        State('isofaci_sname', 'value'),
        State('isofaci_upmail', 'value'),
        State('isofaci_unit_type_id', 'value'),        
        State('isofaci_cluster_id', 'value'),        
        State('isofaci_college_id', 'value'),
        State('isofaci_deg_unit_id', 'value'),
        State('isofaci_fac_posn_name', 'value'),
        State('isofaci_fac_posn_number', 'value'),
        State('isofaci_facadmin_posn', 'value'),
        State('isofaci_staff_posn', 'value'),
        State('isofaci_rolecuqa', 'value'),
        State('isofaci_cuposition_id', 'value'),
        State('isofaci_cdqao_id', 'value'),
        State('isofaci_remarks', 'value'),
        State('isofaci_dr', 'value'),
        State('isofaci_hc', 'value'),
        State('isofaci_mn', 'value'),
        State('isofaci_ss', 'value'),
        State('url', 'search')
    ]
)
def record_isofacilitator_profile(submitbtn, cancel, confirm, removerecord,
                               isofaci_fname, isofaci_mname, 
                               isofaci_sname, isofaci_upmail,
                               isofaci_unit_type_id,
                               isofaci_cluster_id,
                               isofaci_college_id, isofaci_deg_unit_id, 
                               isofaci_fac_posn_name, isofaci_fac_posn_number,
                               isofaci_facadmin_posn, isofaci_staff_posn,
                               isofaci_rolecuqa,
                               isofaci_cuposition_id, isofaci_cdqao_id, 
                               isofaci_remarks,
                               isofaci_dr, isofaci_hc, isofaci_mn, isofaci_ss,

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
        if eventid == 'isofaci_save_button' and submitbtn:
            # Input validation
            if not all([isofaci_sname, isofaci_fname, isofaci_mname, isofaci_upmail, isofaci_unit_type_id, isofaci_cluster_id, isofaci_college_id,
                        isofaci_deg_unit_id, isofaci_fac_posn_name, isofaci_cdqao_id, isofaci_remarks]) and not removerecord:
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please fill in required fields.'
                alert_open = True
                return [alert_color, alert_text, alert_open, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_button_color]
            else:
                # Open the confirmation modal
                if create_mode == 'add':
                    confirmation_modal_open = True
                    confirmation_modal_message = "Are you sure you want to create this ISO Facilitator profile?"
                    confirm_button_color = "success"
                elif create_mode == 'edit':
                    confirmation_modal_open = True
                    confirmation_modal_message = "Are you sure you want to update this ISO Facilitator profile?"
                    confirm_button_color = "success"
                    if removerecord:
                        confirmation_modal_message = "Are you sure you want to delete this ISO Facilitator profile?"
                        confirm_button_color = 'danger'
                
        elif eventid == 'iso_faci_confirmation_modal_confirm' and confirm:
            if create_mode == 'add':
                # SQL for creating a new facilitator profile
                sql = """
                    INSERT INTO iqateam.iso_facilitators (
                        isofaci_fname, isofaci_mname, isofaci_sname, isofaci_upmail,
                        isofaci_unit_type_id, isofaci_cluster_id, isofaci_college_id, 
                        isofaci_deg_unit_id,
                        isofaci_fac_posn_name, 
                        isofaci_fac_posn_number, isofaci_facadmin_posn, isofaci_staff_posn,
                        isofaci_rolecuqa, isofaci_cuposition_id, isofaci_cdqao_id, 
                        isofaci_remarks, isofaci_dr, isofaci_hc, isofaci_mn, isofaci_ss,
                        isofaci_del_ind
                    )
                    VALUES (%s, %s, %s, %s, 
                            %s, %s, %s, %s,
                            %s, %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s, %s, %s,
                            %s)
                """

                values = (
                    isofaci_fname, isofaci_mname, isofaci_sname, isofaci_upmail,
                    isofaci_unit_type_id, isofaci_cluster_id, isofaci_college_id, 
                    isofaci_deg_unit_id,
                    isofaci_fac_posn_name, isofaci_fac_posn_number,
                    isofaci_facadmin_posn, isofaci_staff_posn,
                    isofaci_rolecuqa, isofaci_cuposition_id, isofaci_cdqao_id, 
                    isofaci_remarks, isofaci_dr, isofaci_hc, isofaci_mn, isofaci_ss,
                    False
                )

                db.modifydatabase(sql, values) 
                final_modal_open = True
                final_modal_header = "ISO Facilitator profile created successfully."
               
            elif create_mode == 'edit':
                # Update existing facilitator profile
                isofaci_id = parse_qs(parsed.query).get('id', [None])[0]
                
                if isofaci_id is None:
                    raise PreventUpdate
                
                sqlcode = """
                UPDATE iqateam.iso_facilitators
                SET
                    isofaci_fname = %s, 
                    isofaci_mname = %s, 
                    isofaci_sname = %s,
                    isofaci_upmail = %s,
                    isofaci_unit_type_id = %s,
                    isofaci_cluster_id = %s, 
                    isofaci_college_id = %s, 
                    isofaci_deg_unit_id = %s,
                    isofaci_fac_posn_name = %s, 
                    isofaci_fac_posn_number = %s,
                    isofaci_facadmin_posn = %s, 
                    isofaci_staff_posn = %s,
                    isofaci_rolecuqa = %s,
                    isofaci_cuposition_id = %s, 
                    isofaci_cdqao_id = %s, 
                    isofaci_remarks = %s,
                    isofaci_dr = %s,
                    isofaci_hc = %s,
                    isofaci_mn = %s,
                    isofaci_ss = %s,
                    isofaci_del_ind = %s
                WHERE 
                    isofaci_id = %s
                """
                to_delete = bool(removerecord) 
                
                values = [ 
                    isofaci_fname, isofaci_mname, isofaci_sname,
                    isofaci_upmail, isofaci_unit_type_id, isofaci_cluster_id, isofaci_college_id, 
                    isofaci_deg_unit_id, isofaci_fac_posn_name, isofaci_fac_posn_number,
                    isofaci_facadmin_posn, isofaci_staff_posn, isofaci_rolecuqa,
                    isofaci_cuposition_id, isofaci_cdqao_id, isofaci_remarks,
                    isofaci_dr, isofaci_hc, isofaci_mn, isofaci_ss,
                    to_delete, isofaci_id
                ]
                db.modifydatabase(sqlcode, values)
                
                final_modal_open = True
                final_modal_header = "ISO Facilitator Profile Updated."
        elif eventid == 'iso_faci_confirmation_modal_cancel' and cancel:
            confirmation_modal_open = False
            confirmation_modal_message = ''
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, confirmation_modal_open, confirmation_modal_message, final_modal_open, final_modal_header, confirm_button_color]  


@app.callback(
    [
        Output('isofaci_fname', 'value'),
        Output('isofaci_mname', 'value'),
        Output('isofaci_sname', 'value'),
        Output('isofaci_upmail', 'value'),
        Output('isofaci_unit_type_id', 'value'),
        Output('isofaci_cluster_id', 'value'),
        Output('isofaci_college_id', 'value'),
        Output('isofaci_deg_unit_id', 'value'),
        Output('isofaci_fac_posn_name', 'value'),
        Output('isofaci_fac_posn_number', 'value'),
        Output('isofaci_facadmin_posn', 'value'),
        Output('isofaci_staff_posn', 'value'),
        Output('isofaci_rolecuqa', 'value'),
        Output('isofaci_cuposition_id', 'value'),
        Output('isofaci_cdqao_id', 'value'),
        Output('isofaci_remarks', 'value'),   
        Output('isofaci_dr', 'value'),
        Output('isofaci_hc', 'value'),
        Output('isofaci_mn', 'value'),
        Output('isofaci_ss', 'value'),
    ],
    [  
        Input('isofaci_toload', 'modified_timestamp')
    ],
    [
        State('isofaci_toload', 'data'),
        State('url', 'search')
    ]
)
def isofaci_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        isofaci_id = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                    isofaci_fname, isofaci_mname, 
                    isofaci_sname, isofaci_upmail,
                    isofaci_unit_type_id,
                    isofaci_cluster_id,
                    isofaci_college_id, 
                    isofaci_deg_unit_id,
                    isofaci_fac_posn_name, 
                    isofaci_fac_posn_number,
                    isofaci_facadmin_posn, isofaci_staff_posn,
                    isofaci_rolecuqa,
                    isofaci_cuposition_id, isofaci_cdqao_id, 
                    isofaci_remarks,
                    isofaci_dr, isofaci_hc, isofaci_mn, isofaci_ss              
            FROM iqateam.iso_facilitators
            WHERE isofaci_id = %s
        """
        values = [isofaci_id]

        cols = ['isofaci_fname', 'isofaci_mname', 
                'isofaci_sname', 'isofaci_upmail',
                'isofaci_unit_type_id',
                'isofaci_cluster_id',
                'isofaci_college_id', 
                'isofaci_deg_unit_id',
                'isofaci_fac_posn_name', 
                'isofaci_fac_posn_number',
                'isofaci_facadmin_posn', 'isofaci_staff_posn',
                'isofaci_rolecuqa',
                'isofaci_cuposition_id', 'isofaci_cdqao_id', 
                'isofaci_remarks',
                'isofaci_dr', 'isofaci_hc', 'isofaci_mn', 'isofaci_ss'
                ]

        df = db.querydatafromdatabase(sql, values, cols)

        isofaci_fname = df['isofaci_fname'][0]
        isofaci_mname = df['isofaci_mname'][0]
        isofaci_sname = df['isofaci_sname'][0]
        isofaci_upmail = df['isofaci_upmail'][0]
        isofaci_unit_type_id = df['isofaci_unit_type_id'][0]
        isofaci_cluster_id = df['isofaci_cluster_id'][0]
        isofaci_college_id = df['isofaci_college_id'][0]
        isofaci_deg_unit_id = df['isofaci_deg_unit_id'][0]
        isofaci_fac_posn_name = df['isofaci_fac_posn_name'][0]
        isofaci_fac_posn_number = df['isofaci_fac_posn_number'][0]
        isofaci_facadmin_posn = df['isofaci_facadmin_posn'][0]
        isofaci_staff_posn = df['isofaci_staff_posn'][0]
        isofaci_rolecuqa = df['isofaci_rolecuqa'][0]
        isofaci_cuposition_id = df['isofaci_cuposition_id'][0]
        isofaci_cdqao_id = df['isofaci_cdqao_id'][0]
        isofaci_remarks = df['isofaci_remarks'][0]
        isofaci_dr = df['isofaci_dr'][0]
        isofaci_hc = df['isofaci_hc'][0]
        isofaci_mn = df['isofaci_mn'][0]
        isofaci_ss = df['isofaci_ss'][0]

        
        return [isofaci_fname, isofaci_mname, 
                    isofaci_sname, isofaci_upmail,
                    isofaci_unit_type_id,
                    isofaci_cluster_id,
                    isofaci_college_id, 
                    isofaci_deg_unit_id,
                    isofaci_fac_posn_name, 
                    isofaci_fac_posn_number,
                    isofaci_facadmin_posn, isofaci_staff_posn,
                    isofaci_rolecuqa,
                    isofaci_cuposition_id, isofaci_cdqao_id, 
                    isofaci_remarks,
                    isofaci_dr, isofaci_hc, isofaci_mn, isofaci_ss ]
    
    else:
        raise PreventUpdate
    