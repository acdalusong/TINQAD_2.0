from dash import dash, html, Input, Output, State
import dash_bootstrap_components as dbc
 
import dash 
from dash.exceptions import PreventUpdate
import pandas as pd
import os

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db
 
# Using the corrected path
UPLOAD_DIRECTORY = r".\assets\database\km"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

                        


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("SDG MANAGE EVIDENCE LIST"),
                        html.Hr(), 

                        dbc.Row(   
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "➕ Add Submission",
                                        color="primary",
                                        href='/SDGimpactrankings/SDG_submission?mode=add',
                                    ),
                                    width="auto",
                                    className="mb-0",
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "✍🏻 Add Revision",
                                        color="warning",
                                        href='/SDGimpactrankings/SDG_revision?mode=add',
                                    ),
                                    width="auto",
                                    className="mb-0",
                                ),
                            ]
                        ),

                         

                        html.Br(), 

                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Submissions for Checking"),
                                        dbc.CardBody(
                                            html.Div(
                                                id='checking_list', 
                                                style={
                                                    'marginTop': '20px',
                                                    'overflowX': 'auto',
                                                    'overflowY': 'auto',
                                                    'maxHeight': '300px', 
                                                }
                                            )
                                        )
                                    ],
                                    color="light"
                                ),
                                width="12"
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Submissions in need of Revisions"),
                                        dbc.CardBody(
                                            html.Div(
                                                id='revisions_list', 
                                                style={
                                                    'marginTop': '20px',
                                                    'overflowX': 'auto',
                                                    'overflowY': 'auto',
                                                    'maxHeight': '300px',
                                                }
                                            )
                                        )
                                    ],
                                    color="light"
                                ),
                                width="12"
                            )
                        ),
                         

                        html.Br(),
                        html.Hr(),
 

                        html.Div(
                            [
                                 
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H5(html.B("View Revised Evidence")),
                                            width=8,
                                        ),
                                    ],
                                    justify="between",  
                                ),
                                html.Br(),   
                                
                                dbc.Row(
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Approved Revisions"),
                                                dbc.CardBody(
                                                    html.Div(
                                                        id='checkedrevisions_list', 
                                                        style={
                                                            'marginTop': '20px',
                                                            'overflowX': 'auto',
                                                            'overflowY': 'auto',
                                                            'maxHeight': '500px',
                                                        }
                                                    )
                                                )
                                            ],
                                            color="light"
                                        ),
                                        width="12"
                                    )
                                ),

                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Confirm Removal"),
                                        dbc.ModalBody("Remove evidence from list of revisions?"),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Cancel", id="sdgrevision_cancel_remove", color="secondary"),
                                                dbc.Button("Confirm", id="sdgrevision_confirm_remove", color="danger")
                                            ]
                                        ),
                                    ],
                                    centered=True,
                                    id='sdgrevision_confirmmodal',
                                    backdrop=True,   
                                    className="modal-success"  
                                )

                            ],
                        ),
                        html.Br(),    
                        html.Br(),    



                    ], width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        )
    ]
)







@app.callback(
    [
        Output('checking_list', 'children')
    ],
    [
        Input('url', 'pathname'),
    ]
)

def checking_list (pathname):
    if pathname == '/SDG_evidencelist':   
         
        sql = """ 
            SELECT 
                sdgsubmission_id AS "ID", 
                sdg_evidencename AS "Evidence Name",
                (SELECT office_name FROM maindashboard.offices WHERE office_id = sdg_office_id) AS "Office",
                (SELECT deg_unit_name FROM public.deg_unit WHERE deg_unit_id  = sdg_deg_unit_id) AS "Department",
                sdg_description AS "Description",
                (SELECT ranking_body_name FROM kmteam.ranking_body WHERE ranking_body_id = sdg_rankingbody) AS "Ranking Body",
                sdg_file_name AS "File",
                sdg_file_path AS "File Path",
                sdg_link AS "Link",
                (
                    SELECT json_agg(sdgcriteria_code)
                    FROM kmteam.SDGCriteria
                    WHERE sdgcriteria_id IN (
                        SELECT CAST(jsonb_array_elements_text(sdg_applycriteria) AS INTEGER)
                    )
                ) AS "Applicable Criteria"
            FROM  
                kmteam.SDGSubmission
            WHERE
                sdg_checkstatus = '1'   
                AND sdg_del_ind IS FALSE
        """
        cols = ['ID', 'Evidence Name', 'Office','Department', 'Description', 'Ranking Body', 'File', 'File Path',  'Link',  "Applicable Criteria"]

        df = db.querydatafromdatabase(sql, [], cols)

        if df.shape[0] > 0:
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('Edit', href=f'/SDGimpactrankings/SDG_submission?mode=edit&id={x}', size='sm', color='warning'),
                    style={'text-align': 'center'}
                )
            )

            df = df[['Evidence Name', 'Office', 'Department','Description', 'Ranking Body', 'File', "Link", "Applicable Criteria", 'Action']]

            df['File'] = df.apply(lambda row: html.A(row['File'], href=os.path.join(UPLOAD_DIRECTORY, row['File']) if row['File'] else ''), axis=1)
            
        if not df.empty:
            df["Applicable Criteria"] = df["Applicable Criteria"].apply(
                lambda x: ", ".join(x) if x else "None"
            )
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No submissions for checking")]
    else:
        raise PreventUpdate







@app.callback(
    [
        Output('revisions_list', 'children')
    ],
    [
        Input('url', 'pathname'),  
    ]
)

def revisions_list (pathname):
    if pathname == '/SDG_evidencelist':  
         
        sql = """
            SELECT 
                sdgsubmission_id AS "ID", 
                sdg_evidencename AS "Evidence Name",
                (SELECT office_name FROM maindashboard.offices WHERE office_id = sdg_office_id) AS "Office",
                (SELECT deg_unit_name FROM public.deg_unit WHERE deg_unit_id  = sdg_deg_unit_id) AS "Department",
                sdg_description AS "Description", 
                (SELECT ranking_body_name FROM kmteam.ranking_body WHERE ranking_body_id = sdg_rankingbody) AS "Ranking Body",
                sdg_file_name AS "File",
                sdg_file_path AS "File Path",
                sdg_link AS "Link",
                (
                    SELECT json_agg(sdgcriteria_code)
                    FROM kmteam.SDGCriteria
                    WHERE sdgcriteria_id IN (
                        SELECT CAST(jsonb_array_elements_text(sdg_applycriteria) AS INTEGER)
                    )
                ) AS "Applicable Criteria"
            FROM  
                kmteam.SDGSubmission
            WHERE
                sdg_checkstatus = '3'   AND sdg_del_ind IS FALSE
        """ 
        cols = ['ID', 'Evidence Name', 'Office', 'Department','Description', 'Ranking Body', 'File', 'File Path',  'Link', "Applicable Criteria"]

        df = db.querydatafromdatabase(sql, [], cols)

        if df.shape[0] > 0:
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('Remove', id={'type': 'remove-button', 'index': x}, 
                               size='sm', color='danger'), style={'text-align': 'center'})
            )

            df = df[['Evidence Name', 'Office', 'Department', 'Description', 'Ranking Body', 'File', "Link",  "Applicable Criteria", 'Action']]

            df['File'] = df.apply(lambda row: html.A(row['File'], href=os.path.join(UPLOAD_DIRECTORY, row['File']) if row['File'] else ''), axis=1)
            
        if not df.empty:
            df["Applicable Criteria"] = df["Applicable Criteria"].apply(
                lambda x: ", ".join(x) if x else "None"
            )
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No submissions for revision")]
    else:
        raise PreventUpdate




 
@app.callback(
    Output('revisions_list', 'children', allow_duplicate=True),
    [Input({'type': 'remove-button', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State({'type': 'remove-button', 'index': dash.dependencies.ALL}, 'id')],
    prevent_initial_call=True
)
def remove_submission(n_clicks_list, button_id_list):
    if not n_clicks_list or not any(n_clicks_list):
        raise PreventUpdate

    outputs = []
    for n_clicks, button_id in zip(n_clicks_list, button_id_list):
        if n_clicks:
            submission_id = button_id['index']
            update_sql = """
                UPDATE kmteam.SDGSubmission
                SET sdg_del_ind = TRUE
                WHERE sdgsubmission_id = %s
            """
            db.modifydatabase(update_sql, [submission_id])
            # Append the updated table to outputs list
            outputs.append(revisions_list('/SDG_evidencelist')[0])

    return outputs

 


@app.callback(
    [
        Output('checkedrevisions_list', 'children')
    ],
    [
        Input('url', 'pathname'),  
    ]
)

def checkedrevisions_list (pathname):
    if pathname == '/SDG_evidencelist':  
         
        sql = """
            SELECT 
                sdgrevision_id AS "ID", 
                sdgr_evidencename AS "Evidence Name",
                (SELECT office_name FROM maindashboard.offices WHERE office_id = sdgr_office_id) AS "Office",
                (SELECT deg_unit_name FROM public.deg_unit WHERE deg_unit_id  = sdgr_deg_unit_id) AS "Department",
                sdgr_description AS "Description",
                (SELECT checkstatus_name FROM kmteam.checkstatus WHERE checkstatus_id  = sdgr_checkstatus) AS "Status",
                (SELECT ranking_body_name FROM kmteam.ranking_body WHERE ranking_body_id = sdgr_rankingbody) AS "Ranking Body",
                sdgr_file_name AS "File",
                sdgr_file_path AS "File Path",
                sdgr_link AS "Link",
                (
                    SELECT json_agg(sdgcriteria_code)
                    FROM kmteam.SDGCriteria
                    WHERE sdgcriteria_id IN (
                        SELECT CAST(jsonb_array_elements_text(sdgr_applycriteria) AS INTEGER)
                    )
                ) AS "Applicable Criteria"
            FROM  
                kmteam.SDGRevision
            WHERE
                sdgr_del_ind IS FALSE
            
        """ 
        cols = ['ID', 'Evidence Name', 'Office', 'Department','Description', 'Status','Ranking Body', 'File', 'File Path',  'Link',"Applicable Criteria"]

        df = db.querydatafromdatabase(sql, [], cols)

        if df.shape[0] > 0:
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('Edit', href=f'/SDGimpactrankings/SDG_revision?mode=edit&id={x}', size='sm', color='warning'),
                    style={'text-align': 'center'}
                )
            )

            df = df[['Evidence Name', 'Office', 'Department', 'Description', 'Status', 'Ranking Body', 'File', 'Link',"Applicable Criteria", 'Action']]

            df['File'] = df.apply(lambda row: html.A(row['File'], href=os.path.join(UPLOAD_DIRECTORY, row['File']) if row['File'] else ''), axis=1)
            

        if not df.empty:
            df["Applicable Criteria"] = df["Applicable Criteria"].apply(
                lambda x: ", ".join(x) if x else "None"
            )
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No currently revised submissions")]
    else:
        raise PreventUpdate
