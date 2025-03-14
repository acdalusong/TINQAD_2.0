import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, no_update
from dash import callback_context

import dash

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db 

import datetime
import locale
import re

import base64
import os
from urllib.parse import urlparse, parse_qs

UPLOAD_DIRECTORY = r".\assets\database\admin"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


form = dbc.Form(
    [
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
                        id='exp_date',
                        date=str(pd.to_datetime("today").date()),
                        className='SingleDatePicker'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Payee ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_payee', placeholder="First Name Last Name"),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Expense Main Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='main_expense_id',
                        options=[]
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Expense Sub Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='sub_expense_id',
                        options=[]
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Particulars ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                   dbc.Textarea(
                        id='exp_particulars', 
                        placeholder="Enter particulars"),
                   width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Amount ",
                        html.Span("*", style={"color": "#F8B237"}) 
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_amount', placeholder="0,000.00"),
                    width=6,
                ),
                dbc.Col(
                    html.Div(id='amount-copy', style={"color": "#C4BDBD"}),
                    width=2,
                )
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Status ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='exp_status',
                        options=[ 
                            {"label": "Approved", "value": 1},
                            {"label": "Pending", "value": 2},
                            {"label": "Denied", "value": 3},
                        ]
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "BUR No. ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_bur_no', placeholder="0000-00-00000", maxLength=11),
                    width=6,
                ),
                dbc.Col(
                    html.Div(id='bur-no-copy', style={"color": "#C4BDBD"}),
                    width=2,
                )
            ],
            className="mb-3",
        ),
 
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Submitted by ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],  
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id = 'exp_submitted_by'),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "File Submissions",
                        
                    ],
                    width=4,
                ),
                dbc.Col(
                    dcc.Upload(
                        id="exp_receipt",
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
            className="mb-3",
        ),

        dbc.Row(
            [dbc.Label("",width=4),
             dbc.Col(id="expense_name_output",style={"color": "#F8B237"}, width=6)],  # Output area for uploaded file names
            className="mb-3",
        ),
  
        
        html.Br(), 
    ],
    className="g-2",
)


 


# Callback to display the names of the uploaded files
@app.callback(
    Output("expense_name_output", "children"),
    [Input("exp_receipt", "filename")],  # Use filename to get uploaded file names
)
def display_uploaded_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"📑 {file_names_str}"
 
    return f"📑 {filenames}"













 

#sub expense dropdown
@app.callback(
    Output('sub_expense_id', 'options'),
    Input('main_expense_id', 'value')
)
def update_subexpenses_options(selected_main_expense):
    if selected_main_expense is None:
        return []  # Return empty options if no main expense is selected
    
    try:
        # Query to fetch sub-expenses based on the selected main expense
        sql = """
        SELECT sub_expense_name as label, sub_expense_id as value
        FROM adminteam.sub_expenses
        WHERE main_expense_id = %s
        """
        values = [selected_main_expense]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        sub_expense_options = df.to_dict('records')
        return sub_expense_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 

#amount
locale.setlocale(locale.LC_ALL, '')

@app.callback(
    Output('amount-copy', 'children'),
    Input('exp_amount', 'value')
)
def update_amount_copy(value):
    if value is None:
        return None   

    try: 
        float_value = float(str(value).replace(',', ''))
        # Format the float value with commas and two decimal places
        formatted_value = locale.format_string("%0.2f", float_value, grouping=True)
        return formatted_value
    except (ValueError, TypeError): 
        return None




#bur
@app.callback(
    Output('bur-no-copy', 'children'),
    Input('exp_bur_no', 'value')
)
def update_bur_no_copy(value):
    if value:
        # Remove any non-digit characters
        cleaned_value = re.sub(r'\D', '', value)
        # Format the cleaned value as ####-##-#####
        formatted_value = '-'.join([cleaned_value[:4], cleaned_value[4:6], cleaned_value[6:]])
        return formatted_value
    else:
        return ''

 
 













layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                [
                    html.H1(id="expenses_header"),
                    html.Hr(),
                    html.Div(  
                            [
                                dcc.Store(id='recordexpenses_toload', storage_type='memory', data=0),
                            ]
                        ),
                    dbc.Alert(id='recordexpenses_alert', is_open=False), # For feedback purpose
                    form, 
                    html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='recordexpenses_removerecord',
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
                            id='recordexpenses_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="recordexpenses_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="recordexpenses_cancel_button", n_clicks=0, href="/record_expenses"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-3",
                            justify="end",
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='confirmation_modal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="confirmation_modal_cancel", color="warning"),
                                            dbc.Button("Confirm", id="confirmation_modal_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='confirmation_modal',
                            backdrop="static",   
                            className="modal-success"    
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H5(id="final_modal_header"), close_button=False, className="bg-success"),
                                dbc.ModalBody(html.H3("Click Proceed to continue.")),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        href="/record_expenses",
                                        color="success", 
                                    ),
                                ),
                            ],
                            centered=True,
                            id='final_modal',
                            backdrop='static',
                            keyboard=False,
                        ),  
                ],
                width=8,
                style={"marginLeft": "15px"},
                )
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
        ), 
    ]
)



#main expense dropdown
@app.callback(
    [
        Output('expenses_header', 'children'),
        Output('main_expense_id', 'options'),
        Output('recordexpenses_toload', 'data'),
        Output('recordexpenses_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)

def populate_mainexpenses_dropdown(pathname, search):
    # Check if the pathname matches if necessary
    if pathname == '/record_expenses/add_expense':
        sql = """
            SELECT main_expense_name as label,  main_expense_id  as value
            FROM adminteam.main_expenses

            WHERE main_expense_del_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        main_expense_types = df.to_dict('records')
         
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        header = 'Add Expense Record' if create_mode == 'add' else 'Edit Expense Record'
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [header, main_expense_types, to_load, removediv_style]



@app.callback(
    [
        # Check if all fields are filled
        Output('recordexpenses_alert', 'is_open'),
        Output('recordexpenses_alert', 'color'),
        Output('recordexpenses_alert', 'children'),
        Output('exp_date', 'className'),
        Output('exp_payee', 'className'),
        Output('main_expense_id', 'className'),
        Output('sub_expense_id', 'className'),
        Output('exp_particulars', 'className'),
        Output('exp_amount', 'className'),
        Output('exp_status', 'className'),
        Output('exp_bur_no', 'className'),
        Output('exp_submitted_by', 'className'),
        # Open confirmation modal
        Output('confirmation_modal', 'is_open'), 
        Output('confirmation_modal_message', 'children'),
        # Button Colors Change When in Edit Mode
        Output("confirmation_modal_confirm", "color"),
        # Open success modal
        Output('final_modal', 'is_open'),
        Output('final_modal_header', 'children'),
    ],
    [
        Input('recordexpenses_save_button', 'n_clicks'),
        Input('confirmation_modal_confirm', 'n_clicks'),
        Input('confirmation_modal_cancel', 'n_clicks'),
    ], 
    [   
        State('recordexpenses_removerecord', 'value'),
        State('confirmation_modal', 'is_open'),
        State('exp_date', 'date'),
        State('exp_payee', 'value'),
        State('main_expense_id', 'value'),
        State('sub_expense_id', 'value'),
        State('exp_particulars', 'value'),
        State('exp_amount', 'value'),
        State('exp_status', 'value'),
        State('exp_bur_no', 'value'),
        State('exp_submitted_by', 'value'),
        State('exp_receipt', 'contents'), 
        State('exp_receipt', 'filename'), 
        State('url', 'search')
    ]
)
def save_expense(submitbtn, confirmbtn, cancelbtn, removerecord,confirmationmodal,
                 exp_date, exp_payee, main_expense_id, sub_expense_id,
                 exp_particulars, exp_amount, exp_status, 
                 exp_bur_no, exp_submitted_by,  
                 exp_receipt_contents, exp_receipt_names, search):

    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    # Set default outputs
    alert_open = False
    alert_color = ''
    alert_text = ''
    date_class = 'SingleDatePicker'
    payee_class= ''
    main_expense_id_class = ''
    sub_expense_id_class = ''
    particulars_class = ''
    amount_class = ''
    status_class = ''
    bur_no_class = ''
    submitted_by_class = ''
    confirmation_modal_open = False
    confirmation_message = ''
    btn_color = 'success'
    final_modal_open = False
    final_modal_header = ''
    
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]
    
    if eventid == 'recordexpenses_save_button' and submitbtn:
        # Ensure required fields are filled
        def get_input_class(value):
            return 'red-border' if not value else 'form-control'
        if not all([exp_date, exp_payee, main_expense_id, sub_expense_id,
                exp_particulars, exp_amount, exp_status, exp_bur_no, exp_submitted_by]) and not removerecord:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            date_class = 'SingleDatePicker red-border' if not exp_date else 'SingleDatePicker'
            payee_class= get_input_class(exp_payee)
            main_expense_id_class = get_input_class(main_expense_id)
            sub_expense_id_class = get_input_class(sub_expense_id)
            particulars_class = get_input_class(exp_particulars)
            amount_class = get_input_class(exp_amount)
            status_class = get_input_class(exp_status)
            bur_no_class = get_input_class(exp_bur_no)
            submitted_by_class = get_input_class(exp_submitted_by)
        else: # all inputs are valid
            if create_mode == 'add':
                confirmation_modal_open = True
                confirmation_message = "Are you sure you want to add this expense record?"
            elif create_mode == 'edit':
                confirmation_modal_open = True
                confirmation_message = "Are you sure you want to save changes to this expense record?"
                if removerecord:
                    confirmation_message = "Are you sure you want to delete this expense record?"
                    btn_color = 'danger'

    elif eventid == 'confirmation_modal_confirm' and confirmbtn:
        if confirmationmodal:
            if create_mode == 'add':
                if exp_receipt_contents is None or exp_receipt_names is None:
                    exp_receipt_contents = ["1"]
                    exp_receipt_names = ["1"]

                file_data = []
                if exp_receipt_contents and exp_receipt_names:
                    for content, filename in zip(exp_receipt_contents, exp_receipt_names):
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
                            return [alert_open, alert_color, alert_text]
                
                sql = """ 
                    INSERT INTO adminteam.expenses (
                        exp_date, exp_payee, main_expense_id, sub_expense_id,
                        exp_particulars, exp_amount, exp_status, 
                        exp_bur_no, exp_submitted_by,  
                        exp_receipt_path, exp_receipt_name, exp_receipt_type, exp_receipt_size 
                    ) 
                            
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    exp_date, exp_payee, main_expense_id, sub_expense_id, 
                    exp_particulars, exp_amount, exp_status, exp_bur_no, 
                    exp_submitted_by, 
                    file_data[0]["path"] if file_data else None,
                    file_data[0]["name"] if file_data else None,
                    file_data[0]["type"] if file_data else None,
                    file_data[0]["size"] if file_data else None,
                )    
                try:
                    db.modifydatabase(sql, values)
                    final_modal_open = True
                    final_modal_header = html.H5("Expense Record Successfully Added.")
                        
                except Exception as e:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = f'Error copying record: {e}'
                    return [alert_open, alert_color, alert_text]
        
            elif create_mode == 'edit': 
                expid = parse_qs(parsed.query).get('id', [None])[0]
                
                if expid is None:
                    raise PreventUpdate
                
                sqlcode = """
                    UPDATE adminteam.expenses
                    SET
                        exp_date = %s,
                        exp_payee = %s, 
                        exp_particulars = %s, 
                        exp_status = %s,
                        exp_bur_no = %s,
                        exp_submitted_by = %s, 
                        exp_timestamp = CURRENT_TIMESTAMP,
                        exp_del_ind = %s
                    WHERE 
                        exp_id = %s
                """
                to_delete = bool(removerecord) 

                values = [
                    exp_date, exp_payee, exp_particulars,
                    exp_status, exp_bur_no, exp_submitted_by,
                    to_delete, expid
                ]
                db.modifydatabase(sqlcode, values)

                final_modal_open = True
                final_modal_header = html.H5("Expense Record Edited Successfully.")
            else:
                raise PreventUpdate

    elif eventid == 'confirmation_modal_cancel' and cancelbtn:
        if confirmationmodal:
            confirmation_modal_open = False
            confirmation_message = ''

    else:
        raise PreventUpdate   

    return [alert_open, alert_color, alert_text, date_class, payee_class, main_expense_id_class, sub_expense_id_class, particulars_class, amount_class,
            status_class, bur_no_class, submitted_by_class, confirmation_modal_open, confirmation_message, btn_color, final_modal_open, final_modal_header]
    


@app.callback(
    [
        Output('exp_date', 'date'),
        Output('exp_payee', 'value'),
        Output('main_expense_id', 'value'),
        Output('sub_expense_id', 'value'),
        Output('exp_particulars', 'value'),
        Output('exp_amount', 'value'),
        Output('exp_status', 'value'),
        Output('exp_bur_no', 'value'),
        Output('exp_submitted_by', 'value'),
        Output('exp_receipt', 'filename') 
    ],
    [
        Input('recordexpenses_toload', 'modified_timestamp')
    ],
    [
        State('recordexpenses_toload', 'data'),
        State('url', 'search')
    ]
)
def recordexpenses_load(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        expidd = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                exp_date, exp_payee, main_expense_id, sub_expense_id,
                exp_particulars, exp_amount, exp_status, 
                exp_bur_no, exp_submitted_by,  
                exp_receipt_path
            FROM adminteam.expenses
            WHERE exp_id = %s
        """
        values = [expidd]

        cols = [
            'exp_date', 'exp_payee',  'main_expense_id', 'sub_expense_id',
            'exp_particulars', 'exp_amount', 'exp_status', 
            'exp_bur_no', 'exp_submitted_by',  
            'exp_receipt_name'
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        exp_date = df['exp_date'][0]
        exp_payee = df['exp_payee'][0]
        main_expense_id = df['main_expense_id'][0]
        sub_expense_id = df['sub_expense_id'][0]
        exp_particulars = df['exp_particulars'][0]
        exp_amount = df['exp_amount'][0]
        exp_status = df['exp_status'][0]
        exp_bur_no = df['exp_bur_no'][0]
        exp_submitted_by = df['exp_submitted_by'][0]
        exp_receipt_name = df['exp_receipt_name'][0]
         
        return [
            exp_date, exp_payee,
            main_expense_id, sub_expense_id, exp_particulars,
            exp_amount, exp_status,
            exp_bur_no, exp_submitted_by, exp_receipt_name
        ]

    else:
        raise PreventUpdate
    

@app.callback(
    [ 
        Output('main_expense_id', 'disabled'),
        Output('sub_expense_id', 'disabled'),
        Output('exp_amount', 'disabled'),
        Output('exp_receipt', 'disabled') 
    ],
    [Input('url', 'search')]
)
def addexpense_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 4
    return [False] * 4