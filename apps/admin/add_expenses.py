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
                       date=str(pd.to_datetime("today").date())
                    ),
                    width=8,
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
            className="mb-2",
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
            className="mb-2",
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
                   width=8,
                ),
            ],
            className="mb-2",
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
                    width=5,
                ),
                dbc.Col(
                    html.Div(id='amount-copy', style={"color": "#C4BDBD"}),
                    width=2,
                )
            ],
            className="mb-2",
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
                    width=5,
                ),
            ],
            className="mb-2",
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
                    width=5,
                ),
                dbc.Col(
                    html.Div(id='bur-no-copy', style={"color": "#C4BDBD"}),
                    width=2,
                )
            ],
            className="mb-2",
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
            className="mb-2",
        ),

        dbc.Row(
            [dbc.Label("",width=4),
             dbc.Col(id="expense_name_output",style={"color": "#F8B237"}, width=6)],  # Output area for uploaded file names
            className="mb-2",
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
                    html.H1("ADD EXPENSE"),
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
                            className="mb-2",
                            justify="end",
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['Expense recorded successfully.'
                                    ],id='recordexpenses_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='record_expenses', id='recordexpenses_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='recordexpenses_successmodal',
                            backdrop=True,   
                            className="modal-success"    
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
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [main_expense_types, to_load, removediv_style]








@app.callback(
    [
        Output('recordexpenses_alert', 'color'),
        Output('recordexpenses_alert', 'children'),
        Output('recordexpenses_alert', 'is_open'),
        Output('recordexpenses_successmodal', 'is_open'), 
        Output('recordexpenses_feedback_message', 'children'),
        Output('recordexpenses_btn_modal', 'href')
    ],
    [
        Input('recordexpenses_save_button', 'n_clicks'),
        Input('recordexpenses_btn_modal', 'n_clicks'),
        Input('recordexpenses_removerecord', 'value')
    ], 
    [
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
def save_expense(submitbtn, closebtn, removerecord,
                 exp_date, exp_payee, main_expense_id, sub_expense_id,
                 exp_particulars, exp_amount, exp_status, 
                 exp_bur_no, exp_submitted_by,  
                 exp_receipt_contents, exp_receipt_names, search):

    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'recordexpenses_save_button' or not submitbtn:
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
        if not all([exp_date, exp_payee, main_expense_id, sub_expense_id,
                exp_particulars, exp_amount, exp_status, exp_bur_no, exp_submitted_by]):
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            return [alert_color, alert_text, True, modal_open, feedbackmessage, okay_href]

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
                    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

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
            modal_open = True
            feedbackmessage = html.H5("Expense recorded successfully.")
            okay_href = "/record_expenses"
            
        except Exception as e:
            alert_color = 'danger'
            alert_text = f'Error copying record: {e}'
            return [alert_color, alert_text, True, modal_open, feedbackmessage, okay_href]
 

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

        feedbackmessage = html.H5("Status has been updated.")
        okay_href = "/record_expenses"
        modal_open = True

    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]





@app.callback(
    [
        Output('exp_date', 'value'),
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
