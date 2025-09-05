import dash_bootstrap_components as dbc
import dash
from dash import html, dcc, Input, Output, State, MATCH, ALL, callback_context
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import datetime  

current_year = datetime.datetime.now().year


def create_training_form(index):
    return html.Div(
        id={'type': 'training_entry_div', 'index': index},
        children=[
            html.Hr(),
            dbc.Row([
                dbc.Label("Year", width=2),
                dbc.Col(dbc.Input(id={'type': 'qatr_training_year', 'index': index}, type="number", value=current_year), width=4),
            ]),
            dbc.Row([
                dbc.Label("Name", width=2),
                dbc.Col(dbc.Input(id={'type': 'qatr_training_name', 'index': index}, type="text"), width=4),
            ]),
            dbc.Row([
                dbc.Label("Type", width=2),
                dbc.Col(dcc.Dropdown(id={'type': 'qatr_training_type', 'index': index}, placeholder="Select Training Type"), width=4),
            ]),
            dbc.Row([
                dbc.Label("Other Type", width=2),
                dbc.Col(dbc.Input(id={'type': 'qatr_training_other', 'index': index}, type="text"), width=4),
            ]),
        ]
    )


form = dbc.Form(
    [ 
        dbc.Card(
    [
        dbc.CardHeader(html.H4("QA Officer Training Form")),
        dbc.CardBody([
            html.Hr(),
            dbc.Row([
                dbc.Label("Officer Name", width=2),
                dbc.Col(dcc.Dropdown(id='qatr_officername_id', placeholder="Select Officer"), width=4),
            ]),
            html.Br(), html.Br(),

            # Add button and dynamic area
            dbc.Button("Add Training", id="add_training_btn", color="success"),
            html.Div(id="training_entries_container", children=[create_training_form(0)]),
            dcc.Store(id="training_entry_count", data=1),
            html.Br(),

        ])
    ]
)
    ]
)


@app.callback(
    Output('training_entries_container', 'children'),
    Output('training_entry_count', 'data'),
    Input('add_training_btn', 'n_clicks'),
    State('training_entries_container', 'children'),
    State('training_entry_count', 'data'),
)
def add_training_entry(n_clicks, children, count):
    if n_clicks:
        children.append(create_training_form(count))
        count += 1
    return children, count


@app.callback(
    Output({'type': 'qatr_training_type', 'index': ALL}, 'options'),
    Input('training_entry_count', 'data'),
)
def populate_training_dropdowns(entry_count):
    sql = """
        SELECT trainingtype_name as label, trainingtype_id as value
        FROM qaofficers.training_type
    """
    values = []
    cols = ['label', 'value']
    df = db.querydatafromdatabase(sql, values, cols)
    options = df.to_dict('records')

    return [options] * entry_count  # return exactly as many as the number of dropdowns

# QA Officer name dropdown
@app.callback(
    Output('qatr_officername_id', 'options'),
    Input('url', 'pathname')
)
def populate_qaofficername_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/qaofficers_training':
        sql = """
        SELECT qaofficer_full_name as label, qaofficer_id as value
        FROM  qaofficers.qa_officer
        WHERE qaofficer_del_ind IS False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qaofficername = df.to_dict('records')
        return qaofficername
    else:
        raise PreventUpdate



layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("ADD TRAINING"),
                        html.Hr(),
                        dbc.Alert(id='qatr_alert', is_open=False), # For feedback purpose
                        form, 
                        
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("Register", color="primary", className="me-3", id="qatr_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="secondary", id="qatr_cancel_button", href="/QAOfficers_dashboard", n_clicks=0),
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
                                    html.H4(
                                        ['Training registered successfully.'
                                        ],id='qatr_feedback_message'
                                    )
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                    "Proceed", href = '/QAOfficers_dashboard', id='qatr_btn_modal', className='ml-auto'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='qatr_successmodal',
                            backdrop=True,   
                            className="modal-success"  
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(html.H4("New training type added.")),
                            ],
                            centered=True,
                            id="newtype_successmodal",
                            is_open=False,
                            backdrop=True,
                            className="modal-success",
                        ),

                        html.Hr(),
                        html.H4("TRAINING LIST"),
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    id="training_details_output",  # ID for updating the section
                                    children="Select a QA officer to view their training details.",
                                ),
                                width=12,
                            ),
                            className="mb-3",
                        ),
                         
                        
                    ], width=8, style={'marginLeft': '15px'}
                ),   
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
dbc.Modal(
    [
        dbc.ModalHeader("Confirm Deletion"),
        dbc.ModalBody("Are you sure you want to delete this training entry?"),
        dbc.ModalFooter([
            dbc.Button("Yes, delete", id="confirm_delete_btn", color="danger"),
            dbc.Button("Cancel", id="cancel_delete_btn", color="secondary", className="ms-2"),
        ])
    ],
    id="delete_confirm_modal",
    is_open=False,
    backdrop="static",
    centered=True,
),
dcc.Store(id="training_to_delete"),
dbc.Alert(id="delete_success_alert", color="success", is_open=False),

        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)
 

@app.callback(
    Output('qatr_successmodal', 'is_open'),
    Output('qatr_feedback_message', 'children'),
    Input('qatr_save_button', 'n_clicks'),
    State('qatr_officername_id', 'value'),
    State({'type': 'qatr_training_year', 'index': ALL}, 'value'),
    State({'type': 'qatr_training_name', 'index': ALL}, 'value'),
    State({'type': 'qatr_training_type', 'index': ALL}, 'value'),
    State({'type': 'qatr_training_other', 'index': ALL}, 'value'),
)
def save_multiple_trainings(n_clicks, officer_id, years, names, types, others):
    if n_clicks:
        for year, name, type_, other in zip(years, names, types, others):
            if name and type_:  # Required fields
                sql = """
                INSERT INTO qaofficers.qa_training_details (
                    qatr_officername_id, qatr_training_year,
                    qatr_training_name, qatr_training_type, qatr_training_other
                ) VALUES (%s, %s, %s, %s, %s)
                """
                values = (officer_id, year, name, type_, other)
                db.modifydatabase(sql, values)
        return True, "Trainings registered successfully."
    raise PreventUpdate

#----------
# @app.callback(
#     Output("delete_confirm_modal", "is_open"),
#     Output("training_to_delete", "data"),
#     Input({'type': 'training_remove_button', 'index': ALL}, 'n_clicks'),
#     State({'type': 'training_remove_button', 'index': ALL}, 'id'),
#     prevent_initial_call=True
# )
# def show_delete_modal(n_clicks_list, id_list):
#     if not any(n_clicks_list):
#         raise PreventUpdate

#     triggered_index = n_clicks_list.index(next(filter(lambda x: x, n_clicks_list)))
#     training_id = id_list[triggered_index]['index']
#     return True, training_id

# @app.callback(
#     Output("delete_confirm_modal", "is_open", allow_duplicate=True),
#     Output("delete_success_alert", "is_open"),
#     Output("training_details_output", "children"),
#     Input("confirm_delete_btn", "n_clicks"),
#     State("training_to_delete", "data"),
#     State("qatr_officername_id", "value"),
#     prevent_initial_call=True
# )
# def delete_training(confirm_click, training_id, officer_id):
#     if not confirm_click:
#         raise PreventUpdate

#     sql = """
#         UPDATE qaofficers.qa_training_details
#         SET qatr_training_del_ind = TRUE
#         WHERE qatr_id = %s
#     """
#     db.modifydatabase(sql, [training_id])

#     return False, True, training_details_output(officer_id)


@app.callback(
    Output("training_details_output", "children"),
    [Input("qatr_officername_id", "value")]
)
def training_details_output(qatr_officername_id, searchterm=None):
    if not qatr_officername_id:
        raise dash.exceptions.PreventUpdate

    sql = """
        SELECT 
            qatr_id AS "ID",
            qatr_training_year AS "Year",
            qatr_training_name AS "Name",
            tt.trainingtype_name AS "Type"
        FROM 
            qaofficers.qa_training_details qtd
        INNER JOIN 
            qaofficers.training_type tt
        ON 
            qtd.qatr_training_type = tt.trainingtype_id
        WHERE 
            qatr_officername_id = %s 
            AND qatr_training_del_ind IS False
    """
    cols = ["ID", "Year", "Name", "Type"]

    # Execute SQL query
    df = db.querydatafromdatabase(sql, [qatr_officername_id], cols)

    if not df.empty:
        # Add a button for each training detail
        df["Action"] = df["ID"].apply(
            lambda x: html.Div(
                dbc.Button('❌', id={'type': 'training_remove_button', 'index': x}, size='sm', color='danger'),
                style={'text-align': 'center'})
        )
        df = df[["Year", "Name", "Type", "Action"]]
        
        # Construct HTML table from DataFrame
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return [table]
    else:
        return [html.Div("No training details found for this QA officer")]


# @app.callback(
#     Output('training_details_output', 'children', allow_duplicate=True),
#     Input({'type': 'training_remove_button', 'index': dash.dependencies.ALL}, 'n_clicks'),
#     State({'type': 'training_remove_button', 'index': dash.dependencies.ALL}, 'id'),
#     State('qatr_officername_id', 'value'),  # ✅ Add this state
#     prevent_initial_call=True
# )
# def remove_training(n_clicks_list, button_id_list, officer_id):  # ✅ Accept the officer_id
#     if not n_clicks_list or not any(n_clicks_list):
#         raise PreventUpdate

#     ctx = callback_context
#     if not ctx.triggered:
#         raise PreventUpdate

#     triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     triggered_id = eval(triggered_id)  # Convert string ID to dict
#     qatr_id = triggered_id['index']

#     update_sql = """
#         UPDATE qaofficers.qa_training_details 
#         SET qatr_training_del_ind = TRUE
#         WHERE qatr_id = %s
#     """
#     db.modifydatabase(update_sql, [qatr_id])  

#     return training_details_output(officer_id)

@app.callback(
    Output('training_details_output', 'children', allow_duplicate=True),
    [Input({'type': 'training_remove_button', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State({'type': 'training_remove_button', 'index': dash.dependencies.ALL}, 'id')],
    prevent_initial_call=True
)
def remove_training(n_clicks_list, button_id_list):
    if not n_clicks_list or not any(n_clicks_list):
        raise PreventUpdate

    outputs = []
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    triggered_id = eval(triggered_id)  # Convert string ID to dict
    qatr_id = triggered_id['index']

    update_sql = """
        UPDATE qaofficers.qa_training_details 
        SET qatr_training_del_ind = TRUE
        WHERE qatr_id = %s
    """
    db.modifydatabase(update_sql, [qatr_id])  

    return training_details_output(qatr_officername_id=triggered_id.get('qatr_officername_id', None))

# # Show confirm modal when ❌ clicked
# @app.callback(
#     Output("delete_confirm_modal", "is_open"),
#     Output("delete_training_id", "data"),
#     Input({'type': 'training_remove_button', 'index': ALL}, 'n_clicks'),
#     State({'type': 'training_remove_button', 'index': ALL}, 'id'),
#     prevent_initial_call=True
# )
# def prompt_delete(n_clicks_list, button_ids):
#     ctx = callback_context
#     if not ctx.triggered or not any(n_clicks_list):
#         raise PreventUpdate

#     triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     triggered_id = eval(triggered_id)
#     qatr_id = triggered_id['index']
#     return True, qatr_id


# # Perform deletion if confirmed
# @app.callback(
#     Output("delete_confirm_modal", "is_open"),
#     Output("delete_success_alert", "is_open"),
#     Output("training_details_output", "children"),
#     Input("confirm_delete_btn", "n_clicks"),
#     State("delete_training_id", "data"),
#     State("qatr_officername_id", "value"),
#     prevent_initial_call=True
# )
# def confirm_delete(n_clicks, qatr_id, officer_id):
#     if not n_clicks:
#         raise PreventUpdate

#     sql = """
#         UPDATE qaofficers.qa_training_details 
#         SET qatr_training_del_ind = TRUE
#         WHERE qatr_id = %s
#     """
#     db.modifydatabase(sql, [qatr_id])

#     updated_output = training_details_output(officer_id)
#     return False, True, updated_output


# # Close confirm modal if cancelled
# @app.callback(
#     Output("delete_confirm_modal", "is_open"),
#     Input("cancel_delete_btn", "n_clicks"),
#     prevent_initial_call=True
# )
# def cancel_delete(n):
#     return False

# from dash.exceptions import PreventUpdate

# ...

# def confirm_delete(n_clicks, qatr_id, officer_id):
#     if not n_clicks or not officer_id:
#         raise PreventUpdate
