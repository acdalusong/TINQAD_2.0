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


form = dbc.Form(
    [ 
        
        dbc.Row(
              [
               dbc.Label(
                    [
                        "Select which expense type to add",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
               dbc.Col(
                    dcc.Dropdown(
                        id='select_expense_type',
                        placeholder="Main Expense or Sub Expense",
                        options=[
                            {'label': 'Main Expense', 'value': 'Main Expense'},
                            {'label': 'Sub Expense', 'value': 'Sub Expense'}
                        ]
                    ),
                    width=8,
                ),
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    ["Main Expense Name", 
                     html.Span("*", style={"color": "#F8B237"})],
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(
                        id="main_expense_name",
                        placeholder="e.g. Maintenance and Other Operating Expenses",
                        type="text",
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    ["Main Expense short name", 
                     html.Span("*", style={"color": "#F8B237"})],
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(
                        id="main_expense_shortname",
                        placeholder="e.g. MOOE",
                        type="text",
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
              [
               dbc.Label(
                    [
                        "Select Main Expense",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
               dbc.Col(
                   dcc.Dropdown(
                       id='main_expensetype_id',
                       placeholder="Select Main Expense",
                   ),
                   width=8,
               ),
           ],
           className="mb-2",
        ),
         
        dbc.Row(
            [
                dbc.Label(
                    ["Sub Expense Name", 
                     html.Span("*", style={"color": "#F8B237"})],
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(
                        id="sub_expense_name",
                        placeholder="e.g. General office supplies",
                        type="text",
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        
        html.Br(),
        
        # Cancel and Save Buttons
        dbc.Row(
            [ 
                
                dbc.Col(
                    dbc.Button("Save", color="primary",  id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="warning", id="cancel_button", n_clicks=0, href="/expense_list"),  
                    width="auto"
                ),
            ],
            className="mb-2",
            justify="end",
        ),

        # Success Modal
        dbc.Modal(
            [
                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                dbc.ModalBody(
                    html.H5(id='first_modal_message'),
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Cancel", id= "first_modal_cancel", color="warning"),
                        dbc.Button("Confirm", id= "first_modal_confirm", color="success")
                    ]
                ),
            ],
            centered=True,
            id="first_modal",
            backdrop=True,
            className="modal-success",
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(html.H3(id='modal_final_header'), close_button=False, className="bg-success"),
                dbc.ModalBody(
                    html.H5("Click Proceed to continue"),
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Proceed", href='/expense_list', color="success"),
                    ]
                ),
            ],
            centered=True,
            id="modal_final",
            backdrop="static",
            className="modal-success",
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
                        html.H1("Add Expense Type"),
                        html.Hr(),
                        html.Br(),
                        dbc.Alert(id="expensetype_alert", is_open=False), 
                        form,
                         
                    ],
                    width=6,
                    style={"marginLeft": "15px"},
                ),
            ],
        ),
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
 


#main expense dropdown
@app.callback(
    Output('main_expensetype_id', 'options'),
    Input('url', 'pathname')
)

def populate_mainexpensetype_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/expense_list/add_expensetype':
        sql = """
        SELECT main_expense_name as label,  main_expense_id  as value
        FROM adminteam.main_expenses
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        mainexpensetype = df.to_dict('records')
        return mainexpensetype
    else:
        raise PreventUpdate
 


@app.callback(
    [
        Output('main_expense_name', 'disabled'),
        Output('main_expense_shortname', 'disabled'),
        Output('main_expensetype_id', 'disabled'),
        Output('sub_expense_name', 'disabled'),
    ],
    [Input('select_expense_type', 'value')]
)
def toggle_types(expense_type):
    if expense_type == 'Main Expense':
        return False, False, True, True
    elif expense_type == 'Sub Expense':
        return True, True, False, False
    return True, True, True, True

 


@app.callback(
    [
        Output('select_expense_type', 'className'),
        Output('main_expense_name', 'className'),
        Output('main_expense_shortname', 'className'),
        Output('main_expensetype_id', 'className'),
        Output('sub_expense_name', 'className'),
        Output('expensetype_alert', 'is_open'),
        Output('expensetype_alert', 'color'),
        Output('expensetype_alert', 'children'),
        Output('first_modal', 'is_open'),
        Output('first_modal_message', 'children'),
        Output('modal_final', 'is_open'),
        Output('modal_final_header', 'children'),
    ],
    [
        Input('save_button', 'n_clicks'),
        Input('first_modal_cancel', 'n_clicks'),
        Input('first_modal_confirm', 'n_clicks'),
    ],
    [
        State('select_expense_type', 'value'),
        State('main_expense_name', 'value'),
        State('main_expense_shortname', 'value'),
        State('main_expensetype_id', 'value'),
        State('sub_expense_name', 'value')
    ]
)
def add_expense(submitbtn, cancelbtn, confirmbtn, expense_type, main_expense_name, main_expense_shortname, main_expense_id, sub_expense_name):
    
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
    def get_input_class(value):
            return 'red-border' if not value else 'form-control'
    # Set Default values
    select_expense_type_class = ''
    main_expense_name_class = ''
    main_expense_shortname_class = ''
    main_expensetype_id_class = ''
    sub_expense_name_class = ''
    alert_open = False
    alert_color = ""
    alert_text = ""
    first_modal_open = False
    first_modal_message = ""
    final_modal_open = False
    final_modal_header = ''
    
    if eventid == 'save_button' and submitbtn:
        # Ensure required fields are filled
        if expense_type == 'Main Expense':
            if not main_expense_name or not main_expense_shortname:
                alert_open = True
                alert_color = "danger"
                alert_text = "Check your inputs. Please add a Main Expense Name and Short Name."
                main_expense_name_class = get_input_class(main_expense_name)
                main_expense_shortname_class = get_input_class(main_expense_shortname)
            else:
                first_modal_open = True
                first_modal_message = 'Are you sure you want to add this Main Expense?'

        elif expense_type == 'Sub Expense':
            if not sub_expense_name or not main_expense_id:
                alert_open = True
                alert_color = "danger"
                alert_text = "Check your inputs. Please select a Main Expense and add a Sub Expense Name."
                main_expensetype_id_class = get_input_class(main_expense_id)
                sub_expense_name_class = get_input_class(sub_expense_name)
            else:
                first_modal_open = True
                first_modal_message = 'Are you sure you want to add this Sub Expense?'

        else:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please Select an Expense Type."
            select_expense_type_class = get_input_class(expense_type)

    elif eventid == 'first_modal_confirm' and confirmbtn:
        if expense_type == 'Main Expense':
            sql = """
                    INSERT INTO adminteam.main_expenses(
                        main_expense_name, main_expense_shortname
                    )
                    VALUES (%s, %s)
                """
            values = (main_expense_name, main_expense_shortname)
            db.modifydatabase(sql, values)
            final_modal_open = True
            final_modal_header = "Main Expense Successfully Added"

        elif expense_type == 'Sub Expense':
            sql = """
                    INSERT INTO adminteam.sub_expenses(
                        main_expense_id, sub_expense_name
                    )
                    VALUES (%s, %s)
                """
            values = (main_expense_id, sub_expense_name)
            db.modifydatabase(sql, values)
            final_modal_open = True
            final_modal_header = "Sub Expense Successfully Added"

    elif eventid == 'first_modal_cancel' and cancelbtn:
        first_modal_open = False
        first_modal_message = ""
    
    else:
        raise PreventUpdate

    return [select_expense_type_class, main_expense_name_class, main_expense_shortname_class, main_expensetype_id_class, sub_expense_name_class,
            alert_open, alert_color, alert_text, first_modal_open, first_modal_message, final_modal_open, final_modal_header]