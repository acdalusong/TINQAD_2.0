import dash
import dash_bootstrap_components as dbc
from dash import dash, html, dcc 

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
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(
                    html.H4("New expense type added."),
                ),
                dbc.ModalFooter(
                    dbc.Button("Proceed", href='/expense_list', id="proceed_button", className="ml-auto"),
                ),
            ],
            centered=True,
            id="expensetype_successmodal",
            backdrop=True,
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
        Output('expensetype_alert', 'color'),
        Output('expensetype_alert', 'children'),
        Output('expensetype_alert', 'is_open'),
        Output('expensetype_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('select_expense_type', 'value'),
        State('main_expense_name', 'value'),
        State('main_expense_shortname', 'value'),
        State('main_expensetype_id', 'value'),
        State('sub_expense_name', 'value')
    ]
)
def add_expense(submitbtn, expense_type, main_expense_name, main_expense_shortname, main_expense_id, sub_expense_name):
    if not submitbtn:
        raise PreventUpdate

    # Default values
    alert_open = False
    modal_open = False
    alert_color = ""
    alert_text = ""

    if expense_type == 'Main Expense':
        if not main_expense_name or not main_expense_shortname:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please add a Main Expense Name and Short Name."
            return [alert_color, alert_text, alert_open, modal_open]

        try:
            sql = """
                INSERT INTO adminteam.main_expenses(
                    main_expense_name, main_expense_shortname
                )
                VALUES (%s, %s)
            """
            values = (main_expense_name, main_expense_shortname)
            db.modifydatabase(sql, values)
            modal_open = True
            alert_color = "success"
            alert_text = "Main expense type added successfully."
        except Exception as e:
            alert_color = "danger"
            alert_text = "An error occurred while saving the data."
            alert_open = True

    elif expense_type == 'Sub Expense':
        if not sub_expense_name or not main_expense_id:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please select a Main Expense and add a Sub Expense Name."
            return [alert_color, alert_text, alert_open, modal_open]

        try:
            sql = """
                INSERT INTO adminteam.sub_expenses(
                    main_expense_id, sub_expense_name
                )
                VALUES (%s, %s)
            """
            values = (main_expense_id, sub_expense_name)
            db.modifydatabase(sql, values)
            modal_open = True
            alert_color = "success"
            alert_text = "Sub expense type added successfully."
        except Exception as e:
            alert_color = "danger"
            alert_text = "An error occurred while saving the data."
            alert_open = True

    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open]