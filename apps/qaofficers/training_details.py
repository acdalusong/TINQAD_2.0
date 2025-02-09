import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, ALL
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import datetime  

current_year = datetime.datetime.now().year



form = dbc.Form(
    [ 
        dbc.Row(
            [
                dbc.Label("QA Officer Name", 
                    width=4),
                 
                dbc.Col(
                    dcc.Dropdown(
                        id="qatr_officername_id",
                        placeholder="Select QA Officer",
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Year", 
                    width=4),
                dbc.Col(
                    dbc.Input(id="qatr_training_year", 
                        type="number",
                        value=current_year),
                    width=3,
                    
                ),
                  
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Name of Training", 
                    width=4),
                dbc.Col(
                    dbc.Input(id="qatr_training_name", type="text"),
                    width=6,
                ),
                  
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Training Type", 
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id="qatr_training_type",
                        placeholder="Select Training Type",
                    ),
                    width=6,
                ),
                  
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Other Training type:",
                    width=4),
                dbc.Col(
                    dbc.Input(id="qatr_training_other", type="text", placeholder="Others: Training Name"),
                    width=5,
                ), 
            ],
            className="mb-1",
        ),
 
        html.Br(),
    ]
)



  






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



# QA Officer name dropdown
@app.callback(
    Output('qatr_training_type', 'options'),
    Input('url', 'pathname')
)
def populate_qaofficername_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/qaofficers_training':
        sql = """
        SELECT trainingtype_name as label, trainingtype_id as value
        FROM  qaofficers.training_type 
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
    [
        Output('qatr_alert', 'color'),
        Output('qatr_alert', 'children'),
        Output('qatr_alert', 'is_open'),
        Output('qatr_successmodal', 'is_open'),
        Output('qatr_feedback_message', 'children'),
        Output('qatr_btn_modal', 'href')
    ],
    [
        Input('qatr_save_button', 'n_clicks'),
        Input('qatr_btn_modal', 'n_clicks'),
    ],
    [
        State('qatr_officername_id', 'value'),
        State('qatr_training_year', 'value'), 
        State('qatr_training_name', 'value'),
        State('qatr_training_type', 'value'), 
        State('qatr_training_other', 'value'), 
        State('url', 'search') 
    ]
)
def record_training_details(submitbtn, closebtn, qatr_officername_id, qatr_training_year,
                            qatr_training_name, qatr_training_type, qatr_training_other,
                            search):
    ctx = dash.callback_context 

    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''
    feedbackmessage = None
    okay_href = None

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'qatr_save_button' and submitbtn:
            
            # Input validation
            if not qatr_officername_id:
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add an Officer name.'
                alert_open = True
                return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]
                
            if not qatr_training_year:
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Training Year.'
                alert_open = True
                return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]
                
            if not qatr_training_name:
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Training Name.'
                alert_open = True
                return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]
                
            if not qatr_training_type:
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Training Type.'
                alert_open = True
                return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]
                
            sql = """
                INSERT INTO qaofficers.qa_training_details (
                    qatr_officername_id, qatr_training_year,
                    qatr_training_name, qatr_training_type, qatr_training_other
                )
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                qatr_officername_id, qatr_training_year,
                qatr_training_name, qatr_training_type, qatr_training_other
            )

            db.modifydatabase(sql, values)
            modal_open = True
            feedbackmessage = html.H5("Training registered successfully.")
            okay_href = "/QAOfficers_dashboard"
              
        else:
            raise PreventUpdate

    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]
  

 


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
        
        # Construct HTML table from DataFrame
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return [table]
    else:
        return [html.Div("No training details found for this QA officer")]



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
    for n_clicks, button_id in zip(n_clicks_list, button_id_list):
        if n_clicks:
            qatr_id = button_id['index']
            update_sql = """
                UPDATE qaofficers.qa_training_details 
                SET qatr_training_del_ind = TRUE
                WHERE qatr_id = %s
            """
            db.modifydatabase(update_sql, [qatr_id])  

            outputs.append(training_details_output('/qaofficers_training', searchterm=None)[0])

    return outputs
 