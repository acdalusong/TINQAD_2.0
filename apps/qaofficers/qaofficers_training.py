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


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("Edit QA Officers Training List"),
                        html.Hr(), 
                        
                        html.Div(
                            id='qatraininglist_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  
                            }
                        ),

                        dbc.Modal(
                            [ 
                                dbc.ModalBody(
                                    html.H4('Are you sure you want to remove the training?'),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button(
                                            "Confirm", id='qatraininglist_confirm_button', color="danger", className='ml-auto'), 
                                        dbc.Button(
                                            "Cancel", id='qatraininglist_cancel_button', color="secondary", className='ml-auto'), 
                                    ]
                                )
                                
                            ],
                            centered=True,
                            id='qatraininglist_successmodal',
                            backdrop=True,    
                        ), 

                    ], width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(), html.Br(), html.Br(),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        )
    ]
)
 



@app.callback(
    Output('qatraininglist_list', 'children'),
    [Input('url', 'search')]
)
def qatraininglist_loadlist(search): 
    query_params = parse_qs(search.lstrip('?'))
    mode = query_params.get('mode', [None])[0]
    qaofficer_id = query_params.get('id', [None])[0]
    
    if mode == 'edit' and qaofficer_id:
        sql = """
            SELECT 
                qo.qaofficer_id AS "ID",
                qo.qaofficer_full_name AS "Name",
                cp.cuposition_name AS "Rank/Designation",
                du.deg_unit_name AS "Department",
                cl.college_name AS "College",
                clus.cluster_name AS "Academic Cluster"
            FROM 
                qaofficers.qa_officer AS qo
            LEFT JOIN 
                qaofficers.qa_training_details AS qtd
                ON qo.qaofficer_id = qtd.qatr_officername_id
            LEFT JOIN 
                qaofficers.cuposition AS cp
                ON qo.qaofficer_cuposition_id = cp.cuposition_id
            LEFT JOIN 
                public.deg_unit AS du
                ON qo.qaofficer_deg_unit_id = du.deg_unit_id
            LEFT JOIN 
                public.college AS cl
                ON qo.qaofficer_college_id = cl.college_id
            LEFT JOIN 
                public.clusters AS clus
                ON qo.qaofficer_cluster_id = clus.cluster_id
            WHERE
                qaofficer_del_ind IS False AND
                qo.qaofficer_id = %s
            GROUP BY 
                qo.qaofficer_id, qo.qaofficer_full_name, cp.cuposition_name, du.deg_unit_name, cl.college_name, clus.cluster_name
        """
        cols = ["ID", 'Name', 'Rank/Designation', 'Department', 'College', 'Academic Cluster']

        # Execute the query
        df = db.querydatafromdatabase(sql, [qaofficer_id], cols)

        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    
    return [html.Div("Query could not be processed")]
