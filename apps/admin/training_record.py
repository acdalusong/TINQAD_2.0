import dash_bootstrap_components as dbc
from dash import dash, html, dcc 

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import os

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

# Using the corrected path
UPLOAD_DIRECTORY = r".\assets\database\admin\trainings"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H1("TRAINING LIST"),
                                    style={"marginRight": "auto"}  
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Training Document", color="primary", 
                                        href='/training_documents?mode=add',  
                                    ),
                                    width="auto",    
                                ),
                            ],
                            style={"marginBottom": "-10px"}
                        ),
                        html.Hr(),
                        
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    html.Label(
                                        "Name:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='name_filter',
                                        placeholder='Search by Name, Faculty Position, Training Type, Cluster',
                                        className='ml-auto'   
                                    ),
                                    width="4",
                                ),
                                dbc.Col(  
                                    html.Label(
                                        "Faculty Position:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dcc.Dropdown(
                                    id="faculty_position_filter",
                                    options=[],
                                    placeholder=" Select Faculty Position"
                                    ),
                                    width=4,
                                ), 
                            ],
                            className="align-items-center",    
                        ),
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    html.Label(
                                        "Training Type:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dcc.Dropdown(
                                    id="training_type_filter",
                                    options=[],
                                    placeholder=" Select Training Type"
                                    ),
                                    width=4,
                                ),
                                dbc.Col(  
                                    html.Label(
                                        "Cluster:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                            "width": "100%"}
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dcc.Dropdown(
                                    id="cluster_filter",
                                    options=[],
                                    placeholder=" Select Cluster"
                                    ),
                                    width=4,
                                ),
                            ],
                            className="align-items-center mb-2",   
                        ),
                        
 
                        html.Div(
                            id='traininglist_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto', 
                                'overflowY': 'auto',   
                                'maxHeight': '1000px',
                            }
                        ),

                        html.Br(),
                        html.Br(),

                    ], width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        )
    ]
)


#faculty positions dropdown
@app.callback(
    Output('faculty_position_filter', 'options'),
    Input('url', 'pathname')
)

def facultypositions_filter_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/training_record':
        sql = """
        SELECT fac_posn_name as label, fac_posn_name  as value
        FROM public.fac_posns
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        fac_posns_types = df.to_dict('records')
        return fac_posns_types
    else:
        raise PreventUpdate
    
#qa training dropdown
@app.callback(
    Output('training_type_filter', 'options'),
    Input('url', 'pathname')
)
def trainings_filter_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/training_record':
        sql = """
        SELECT trainingtype_name as label, trainingtype_id as value
        FROM qaofficers.training_type
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qa_training_options = df.to_dict('records')
        return qa_training_options
    else:
        raise PreventUpdate
    
#cluster_filter dropdown
@app.callback(
    Output('cluster_filter', 'options'),
    Input('url', 'pathname')
)
def cluster_filter_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/training_record':
        sql = """
            SELECT cluster_name as label, cluster_id  as value
            FROM public.clusters
            
            WHERE cluster_del_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        cluster_options = df.to_dict('records')
        return cluster_options
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('traininglist_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('name_filter', 'value'),
        Input('faculty_position_filter', 'value'),
        Input('training_type_filter', 'value'),
        Input('cluster_filter', 'value')
    ]
)
def traininglist_loadlist(pathname, searchterm, position, trainingtype, cluster):
    if pathname == '/training_record':
        sql = """
            SELECT 
                training_documents_id AS "ID",
                complete_name AS "QAO Name",
                fac_posn AS "Faculty Position",
                clu.cluster_name AS "Cluster",
                col.college_name AS "College",
                qt.trainingtype_name AS "QA Training",
                departure_date AS "Departure Date",
                return_date AS "Return Date",
                venue AS "Venue",
                pacert_path AS "Participant Attendance Cert. path",
                pacert_name AS "Participant Attendance Cert.",
                orcert_path AS "Official Receipt path",
                orcert_name AS "Official Receipt",
                otrcert_path AS "Official Travel Report path",
                otrcert_name AS "Official Travel Report",
                others_path AS "Other Receipts path",
                others_name AS "Other Receipts",
                recert_path AS "Receiving Copy path",
                recert_name AS "Receiving Copy"
            FROM 
                adminteam.training_documents td
            LEFT JOIN 
                public.clusters clu ON td.cluster_id = clu.cluster_id
            LEFT JOIN 
                public.college col ON td.college_id = col.college_id
            LEFT JOIN 
                qaofficers.training_type qt ON td.qa_training_id = qt.trainingtype_id
        """
        filters = ["train_docs_del_ind IS FALSE"]
        values = []

        if searchterm: 
            filters.append("td.complete_name ILIKE %s")
            values.append(f"%{searchterm}%")

        if position:
            filters.append("td.fac_posn ILIKE %s")
            values.append(f"%{position}%")

        if trainingtype:
            filters.append("td.qa_training_id = %s")
            values.append(trainingtype)
        
        if cluster:
            filters.append("td.cluster_id = %s")
            values.append(cluster)
        
        # Append filters if any exist
        if filters:
            sql += " WHERE " + " AND ".join(filters)

         # Append ORDER BY after filters
        sql += " ORDER BY train_docs_timestamp DESC"

        cols = ["ID","QAO Name","Faculty Position","Cluster","College",
                "QA Training", "Departure Date", "Return Date","Venue",
                "Participant Attendance Cert. path",
                "Participant Attendance Cert.",
                "Official Receipt path",
                "Official Receipt",
                "Official Travel Report path",
                "Official Travel Report",
                "Other Receipts path",
                "Other Receipts",
                "Receiving Copy path",
                "Receiving Copy"
            ]

        df = db.querydatafromdatabase(sql, values, cols) 

        if not df.empty: 
            df["Action"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('Edit', href=f'training_documents?mode=edit&id={x}', size='sm', color='warning'),
                    style={'text-align': 'center'}
                )
            )
            df = df[["QAO Name","Faculty Position","Cluster","College",
                    "QA Training", "Departure Date", "Return Date","Venue",
                    "Participant Attendance Cert.", "Official Receipt",
                    "Official Travel Report", "Other Receipts",
                    "Receiving Copy", 'Action' ]]
                 
            df['Participant Attendance Cert.'] = df.apply(lambda row: html.A(row['Participant Attendance Cert.'], href=os.path.join(UPLOAD_DIRECTORY, row['Participant Attendance Cert.']) if row['Participant Attendance Cert.'] else ''), axis=1)
            df['Official Receipt'] = df.apply(lambda row: html.A(row['Official Receipt'], href=os.path.join(UPLOAD_DIRECTORY, row['Official Receipt']) if row['Official Receipt'] else ''), axis=1)
            df['Official Travel Report'] = df.apply(lambda row: html.A(row['Official Travel Report'], href=os.path.join(UPLOAD_DIRECTORY, row['Official Travel Report']) if row['Official Travel Report'] else ''), axis=1)
            df['Other Receipts'] = df.apply(lambda row: html.A(row['Other Receipts'], href=os.path.join(UPLOAD_DIRECTORY, row['Other Receipts']) if row['Other Receipts'] else ''), axis=1)
            df['Receiving Copy'] = df.apply(lambda row: html.A(row['Receiving Copy'], href=os.path.join(UPLOAD_DIRECTORY, row['Receiving Copy']) if row['Receiving Copy'] else ''), axis=1)
                
        

        
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        
        else:
            return [html.Div("No records to display")]

    return [html.Div("Query could not be processed")]
    
