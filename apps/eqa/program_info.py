import dash_bootstrap_components as dbc
from dash import html, dcc 

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
                        "Select which Program Info to add",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=5
                ),
               dbc.Col(
                    dcc.Dropdown(
                        id='select_programinfo',
                        placeholder="Cluster / College / Department",
                        options=[
                            {'label': 'Cluster', 'value': 'Cluster'},
                            {'label': 'College', 'value': 'College'},
                            {'label': 'Department', 'value': 'Department'}
                        ]
                    ),
                    width=7,
                ),
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label("Add New Cluster", width=5),
                dbc.Col(
                    dbc.Input(
                        id="cluster_name",
                        placeholder="Management and Economics",
                        type="text",
                        disabled=True,
                    ),
                    width=7,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Cluster short name",width=5),
                dbc.Col(
                    dbc.Input(
                        id="cluster_shortname",
                        placeholder="MAE",
                        type="text",
                        disabled=True,
                    ),
                    width=7,
                ),
            ],
            className="mb-2",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
              [
               dbc.Label("Select Cluster",width=5),
               dbc.Col(
                   dcc.Dropdown(
                       id='newcluster_id',
                       placeholder="Select Cluster",
                       disabled=True,
                   ),
                   width=7,
               ),
           ],
           className="mb-2",
        ),
         
        dbc.Row(
            [
                dbc.Label("Add New College",width=5),
                dbc.Col(
                    dbc.Input(
                        id="college_name",
                        placeholder="College of Engineering",
                        type="text",
                        disabled=True,
                    ),
                    width=7,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("College short name",width=5),
                dbc.Col(
                    dbc.Input(
                        id="college_shortname",
                        placeholder="COE",
                        type="text",
                        disabled=True,
                    ),
                    width=7,
                ),
            ],
            className="mb-2",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
              [
               dbc.Label("Select College",width=5),  
               dbc.Col(
                   dcc.Dropdown(
                       id='newcollege_id',
                       placeholder="Select College",
                       disabled=True,
                   ),
                   width=7,
               ),
           ],
           className="mb-2",
        ),
         
        dbc.Row(
            [
                dbc.Label("Add New Department",width=5),
                dbc.Col(
                    dbc.Input(
                        id="deg_unit_name",
                        placeholder="Department of Industrial Engineering",
                        type="text",
                        disabled=True,
                    ),
                    width=7,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Department short name",width=5),
                dbc.Col(
                    dbc.Input(
                        id="deg_unit_shortname",
                        placeholder="DIEOR",
                        type="text",
                        disabled=True,
                    ),
                    width=7,
                ),
            ],
            className="mb-2",
        ),
        html.Hr(),
        html.Br(), 
        dbc.Row(
            [ 
                
                dbc.Col(
                    dbc.Button("Save", color="primary",  id="programinfo_save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="warning", id="programinfo_cancel_button", n_clicks=0, href="/program_list"),  
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
                    html.H4("New program info added."),
                ),
                dbc.ModalFooter(
                    dbc.Button("Proceed", href='/program_list', id="proceed_button", className="ml-auto"),
                ),
            ],
            centered=True,
            id="programinfo_successmodal",
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
                        html.H1("Add Program Info Type"),
                        html.Hr(),
                        html.Br(),
                        dbc.Alert(id="programinfo_alert", is_open=False), 
                        form,
                         
                    ],
                    width=7,
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
 

@app.callback(
    Output('cluster_name', 'disabled'),
    Output('cluster_shortname', 'disabled'),

    Output('newcluster_id', 'disabled'),
    Output('college_name', 'disabled'),
    Output('college_shortname', 'disabled'),

    Output('newcollege_id', 'disabled'),
    Output('deg_unit_name', 'disabled'),
    Output('deg_unit_shortname', 'disabled'),

    Input('select_programinfo', 'value')
)
def update_input_fields(selected_option):
    cluster_disabled = True if selected_option != 'Cluster' else False
    college_disabled = True if selected_option != 'College' else False
    department_disabled = True if selected_option != 'Department' else False
    return cluster_disabled, cluster_disabled, college_disabled, college_disabled, college_disabled, department_disabled, department_disabled, department_disabled








#cluster dropdown
@app.callback(
    Output('newcluster_id', 'options'),
    Input('url', 'pathname')
)

def populate_clustertype_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/program_info':
        sql = """
        SELECT cluster_name as label,  cluster_id as value
        FROM public.clusters
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        clustertype = df.to_dict('records')
        return clustertype
    else:
        raise PreventUpdate
 
#college dropdown 
@app.callback(
    Output('newcollege_id', 'options'),
    Input('url', 'pathname')
)

def populate_collegeid_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/program_info':
        sql = """
        SELECT college_name as label, college_id as value
        FROM public.college
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        collegetype = df.to_dict('records')
        return collegetype
    else:
        raise PreventUpdate
    



@app.callback(
    [
        Output('programinfo_alert', 'color'),
        Output('programinfo_alert', 'children'),
        Output('programinfo_alert', 'is_open'),
        Output('programinfo_successmodal', 'is_open')
    ],
    [
        Input('programinfo_save_button', 'n_clicks')
    ],
    [
        State('select_programinfo', 'value'),
        State('cluster_name', 'value'),
        State('cluster_shortname', 'value'),
        State('college_name', 'value'),
        State('newcluster_id', 'value'),
        State('college_shortname', 'value'),
        State('newcollege_id', 'value'),
        State('deg_unit_name', 'value'),
        State('deg_unit_shortname', 'value'), 
    ]
)
def add_programinfo (submitbtn, select_programinfo, cluster_name, cluster_shortname, college_name, newcluster_id, college_shortname,newcollege_id,deg_unit_name, deg_unit_shortname):
    if not submitbtn:
        raise PreventUpdate

    # Default values
    alert_open = False
    modal_open = False
    alert_color = ""
    alert_text = ""

    if select_programinfo == 'Cluster':
        if not cluster_name or not cluster_shortname:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please add a Cluster Name and Cluster short name."
            return [alert_color, alert_text, alert_open, modal_open]

        try:
            sql = """
                INSERT INTO public.clusters (
                    cluster_name, cluster_shortname 
                )
                VALUES (%s, %s)
            """
            values = (cluster_name, cluster_shortname)
            db.modifydatabase(sql, values)
            modal_open = True
            alert_color = "success"
            alert_text = "New cluster added successfully."
        except Exception as e:
            alert_color = "danger"
            alert_text = "An error occurred while saving the data."
            alert_open = True

    elif select_programinfo == 'College':
        if not college_shortname or not newcluster_id:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please select a Cluster and add a College short name."
            return [alert_color, alert_text, alert_open, modal_open]

        try:
            sql = """
                INSERT INTO public.college(
                    cluster_id, college_name, college_shortname 
                )
                VALUES (%s, %s, %s)
            """
            values = (newcluster_id, college_name, college_shortname)
            db.modifydatabase(sql, values)
            modal_open = True
            alert_color = "success"
            alert_text = "New college added successfully."
        except Exception as e:
            alert_color = "danger"
            alert_text = "An error occurred while saving the data."
            alert_open = True

    elif select_programinfo == 'Department':
        if not deg_unit_shortname or not newcollege_id:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please select a College and add a Department short name."
            return [alert_color, alert_text, alert_open, modal_open]

        try:
            sql = """
                INSERT INTO public.deg_unit (
                    college_id, deg_unit_name, deg_unit_shortname 
                )
                VALUES (%s, %s, %s)
            """
            values = (newcollege_id, deg_unit_name, deg_unit_shortname)
            db.modifydatabase(sql, values)
            modal_open = True
            alert_color = "success"
            alert_text = "New department added successfully."
        except Exception as e:
            alert_color = "danger"
            alert_text = "An error occurred while saving the data."
            alert_open = True

    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open]