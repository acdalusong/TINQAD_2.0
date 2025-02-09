import dash
import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd
import dash

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db


checklist_card = dbc.Col(
    dbc.Card(
        dbc.CardBody(
            dcc.Checklist(
                id='criteria_list',
                options=[],
                inline=True,
                labelStyle={'marginRight': '10px'}  # Adjust the margin as needed
            )
        ),
        style={
            'border': '1px solid #ccc',  # Optional: custom border styling
            'padding': '10px',  # Optional: custom padding for the card body
            'background-color': '#f9f9f9'  # Optional: background color
        },
    ),
    width=12  # Adjust the column width to fit the content
)




layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("SDG IMPACT RANKINGS"),
                        html.Hr(), 

                        dbc.Row(   
                            [
                                
                                
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='add_criteria_filter',
                                        placeholder='🔎 Search by Criteria ID, Criteria Code, Description',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),

                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Criteria", color="primary", 
                                        href='/add_criteria', 
                                    ),
                                    width="auto",    
                                    
                                )
                            ],
                            className="align-items-center",   
                            justify="between",  
                        ),

                        html.Div(
                            id='add_criteria_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                            }
                        ),
                        html.Br(),

                        html.Div(
                            [
                                html.Hr(),   
                                # Heading with a button on the same row
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H5(html.B("Manage Approved Evidence")),
                                            width=8,
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Deselect Criteria Checkboxes",
                                                id="deselect_button",
                                                color="secondary",
                                                size="sm",
                                            ),
                                            width="auto",
                                            style={"textAlign": "right"},   
                                        ),
                                    ],
                                    justify="between",  
                                ),
                                html.Br(),   
                                
                                dbc.Row(
                                    [
                                        checklist_card,  
                                    ],
                                ),
                                
                                
                            ],
                        ),

                        html.Div(
                            id='manageevidence_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto',# This CSS property adds a horizontal scrollbar
                                'overflowY': 'auto',   
                                'maxHeight': '200px',
                            }
                        ),
                         

                        html.Br(),
                        html.Hr(),

                        dbc.Row(
                            dbc.Col(
                                html.H5(html.B("Approved Revisions")),
                                width=8,
                                ),
                            
                        ),
                        html.Div(
                            id='managerevision_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto',# This CSS property adds a horizontal scrollbar
                                'overflowY': 'auto',   
                                'maxHeight': '200px',
                            }
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






#criteria list dropdown
@app.callback(
    Output('criteria_list', 'options'),
    Input('url', 'pathname')
)
def populate_criteria_list_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpact_rankings':
        sql ="""
        SELECT sdgcriteria_code as label, sdgcriteria_id  as value
        FROM  kmteam.SDGCriteria
        WHERE
            sdgcriteria_del_ind IS FALSE
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        criteria_list_types = [{'label': row['label'], 'value': row['value']} for _, row in df.iterrows()]
        return criteria_list_types
    else:
        raise PreventUpdate

#criteria list  deselect
@app.callback(
    Output('criteria_list', 'value'),
    [Input('deselect_button', 'n_clicks')]
)
def deselect_all_options(n_clicks):
    if n_clicks:
        # Return an empty list to deselect all options
        return []
    else:
        # Return current value if no click event has occurred
        return dash.no_update











@app.callback(
    [
        Output('add_criteria_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('add_criteria_filter', 'value'),
    ]
)

def add_criteria_list(pathname, searchterm=None):
    if pathname == '/SDGimpact_rankings':  
        sql = """
            SELECT 
                sdgcriteria_id AS "ID",
                sdgcriteria_number AS "Criteria ID.",
                sdgcriteria_code AS "Criteria Code",
                sdgcriteria_description AS "Description"
            FROM 
                kmteam.SDGCriteria 
            WHERE
                sdgcriteria_del_ind IS FALSE

        """
        cols = ["ID", 'Criteria ID.' , 'Criteria Code','Description']

        if searchterm:
            sql += """
                AND (
                    sdgcriteria_code ILIKE %s OR
                    CAST(sdgcriteria_number AS VARCHAR) ILIKE %s OR 
                    sdgcriteria_description ILIKE %s
                )
            """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern, like_pattern]  # Define values here
        else:
            values = []

        df = db.querydatafromdatabase(sql, values, cols) 

        if df.shape[0] > 0:
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('❌', id={'type': 'criteria_remove_button', 'index': x}, 
                               size='sm', color='danger'), style={'text-align': 'center'})
            )

            df = df[['Criteria ID.' , 'Criteria Code','Description', 'Action']]

 
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No criteria submitted yet")]
    else:
        raise PreventUpdate
    



@app.callback(
    Output('add_criteria_list', 'children', allow_duplicate=True),
    [Input({'type': 'criteria_remove_button', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State({'type': 'criteria_remove_button', 'index': dash.dependencies.ALL}, 'id')],
    prevent_initial_call=True
)
def remove_criteria(n_clicks_list, button_id_list):
    if not n_clicks_list or not any(n_clicks_list):
        raise PreventUpdate

    outputs = []
    for n_clicks, button_id in zip(n_clicks_list, button_id_list):
        if n_clicks:
            sdgcriteria_id = button_id['index']
            update_sql = """
                UPDATE kmteam.SDGCriteria
                SET sdgcriteria_del_ind = TRUE
                WHERE sdgcriteria_id = %s
            """
            db.modifydatabase(update_sql, [sdgcriteria_id]) 
            # Pass a default searchterm value when calling add_criteria_list
            outputs.append(add_criteria_list('/SDGimpact_rankings', searchterm=None)[0])

    return outputs












 
@app.callback(
    [
        Output('manageevidence_list', 'children')
    ],
    [
        Input('url', 'pathname'), 
        Input('criteria_list', 'value'),
    ]
)

def update_manageevidence_list (pathname, selected_criteria):
    if pathname == '/SDGimpact_rankings':     
        sql = """
            SELECT 
                sdgsubmission_id AS "ID",
                sdg_evidencename AS "Evidence Name",
                (SELECT office_name FROM maindashboard.offices WHERE office_id = sdg_office_id) AS "Office",
                sdg_description AS "Description",
                (SELECT ranking_body_name FROM kmteam.ranking_body WHERE ranking_body_id = sdg_rankingbody) AS "Ranking Body",
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
                sdg_checkstatus = '2'   
                AND sdg_del_ind IS FALSE
        """
        if selected_criteria:
            sql += """
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements_text(sdg_applycriteria) AS e
                    WHERE CAST(e AS INTEGER) = ANY(%s)
                )
            """
            params = [selected_criteria]
        else:
            params = []

        cols = ["ID", "Evidence Name", "Office", "Description", "Ranking Body", "Applicable Criteria"]

        df = db.querydatafromdatabase(sql, params, cols)

        if df.shape[0] > 0:
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('❌', id={'type': 'submission_remove_button', 'index': x}, 
                               size='sm', color='danger'), style={'text-align': 'center'})
            )

            df = df[["Evidence Name", "Office", "Description", "Ranking Body", "Applicable Criteria", 'Action']]


        if not df.empty:
            df["Applicable Criteria"] = df["Applicable Criteria"].apply(lambda x: ", ".join(x) if x else "None")
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No approved evidences yet")]
    else:
        raise PreventUpdate


@app.callback(
    Output('manageevidence_list', 'children', allow_duplicate=True),
    [Input({'type': 'submission_remove_button', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State({'type': 'submission_remove_button', 'index': dash.dependencies.ALL}, 'id')],
    prevent_initial_call=True
)
def manageevidence_list(n_clicks_list, button_id_list, selected_criteria=None):
    if not n_clicks_list or not any(n_clicks_list):
        raise PreventUpdate

    outputs = []
    for n_clicks, button_id in zip(n_clicks_list, button_id_list):
        if n_clicks:
            sdgsubmission_id = button_id['index']
            update_sql = """
                UPDATE  kmteam.SDGSubmission
                SET sdg_del_ind = TRUE
                WHERE sdgsubmission_id = %s
            """
            db.modifydatabase(update_sql, [sdgsubmission_id])
            outputs.append(update_manageevidence_list('/SDGimpact_rankings', selected_criteria)[0])

    return outputs














@app.callback(
    [
        Output('managerevision_list', 'children')
    ],
    [
        Input('url', 'pathname'),  
    ]
)

def update_managerevision_list (pathname):
    if pathname == '/SDGimpact_rankings': 
         
        sql = """
            SELECT 
                sdgrevision_id AS "ID",
                sdgr_evidencename AS "Evidence Name",
                (SELECT office_name FROM maindashboard.offices WHERE office_id = sdgr_office_id) AS "Office",
                sdgr_description AS "Description",
                (SELECT ranking_body_name FROM kmteam.ranking_body WHERE ranking_body_id = sdgr_rankingbody) AS "Ranking Body",
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
                sdgr_checkstatus = '2'   
                AND sdgr_del_ind IS FALSE
        """
        

        cols = ["ID", "Evidence Name", "Office", "Description", "Ranking Body", "Applicable Criteria"]

        df = db.querydatafromdatabase(sql, [], cols)

        if df.shape[0] > 0:
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('❌', id={'type': 'revision_remove_button', 'index': x}, 
                               size='sm', color='danger'), style={'text-align': 'center'})
            )

            df = df[["Evidence Name", "Office", "Description", "Ranking Body", "Applicable Criteria", 'Action']]


        if not df.empty:
            df["Applicable Criteria"] = df["Applicable Criteria"].apply(
                lambda x: ", ".join(x) if x else "None"
            )
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No approved revisions yet")]
    
@app.callback(
    Output('managerevision_list', 'children', allow_duplicate=True),
    [Input({'type': 'revision_remove_button', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State({'type': 'revision_remove_button', 'index': dash.dependencies.ALL}, 'id')],
    prevent_initial_call=True
)
def update_managerevision_list(n_clicks_list, button_id_list):
    if not n_clicks_list or not any(n_clicks_list):
        raise PreventUpdate

    outputs = []
    for n_clicks, button_id in zip(n_clicks_list, button_id_list):
        if n_clicks:
            sdgrevision_id = button_id['index']
            update_sql = """
                UPDATE  kmteam.SDGRevision
                SET sdgr_del_ind = TRUE
                WHERE sdgrevision_id = %s
            """
            db.modifydatabase(update_sql, [sdgrevision_id])  
            outputs.append(update_managerevision_list('/SDGimpact_rankings', button_id_list)[0])

    return outputs
