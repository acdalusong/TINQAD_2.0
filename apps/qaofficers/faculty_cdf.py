import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime 

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db


# Get the current year
current_year = datetime.now().year

facultycdfcard = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='qatraininglist_filter',
                                placeholder='🔎 Search by Name, UP Mail, Competency Level, etc',
                                className='ml-auto'
                            ),
                            width="6",
                        ),
                    ],
                    className="align-items-center",
                    style={
                        "margin-right": "2px",
                        "margin-bottom": "15px",
                    }
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                id='qatraininglist_list',
                                style={
                                    'overflowX': 'auto',
                                    # 'overflowY': 'auto',
                                    'maxHeight': 'none',
                                }
                            ),
                        )
                    ]
                ),
            ]
        ),
    ], 
    className="mb-3"
)


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("QA OFFICERS COMPETENCY LEVEL"),
                        html.Hr(),
                        html.Br(),
                        facultycdfcard,
                        html.Br(),
                        html.Br(),
                        
                    ], 
                    width=9, style={'marginLeft': '15px'}
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
    Output('qatraininglist_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('qatraininglist_filter', 'value'),
    ]
)
def traininglist_loadlist(pathname, searchterm):
    if pathname == '/qaofficers_faculty_cdf': 
        sql = """
        -- Your updated SQL query with Competency Level logic
        SELECT 
            qo.qaofficer_id AS "ID",
            clv.competency_name AS "Competency Level", -- Competency level added here
            qo.qaofficer_full_name AS "Name",
            qo.qaofficer_upmail AS "UP Mail",
            cp.cuposition_name AS "Rank/Designation",
            clus.cluster_name AS "Academic Cluster",
            cl.college_name AS "Main Unit",
            du.deg_unit_name AS "Sub-unit",
            COUNT(CASE WHEN tt.trainingtype_name = 'iAADS' THEN 1 ELSE NULL END) AS "iAADS",
            COUNT(CASE WHEN tt.trainingtype_name = 'PBMS Training' THEN 1 ELSE NULL END) AS "PBMS Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'AUNQA Tier 1 Training' THEN 1 ELSE NULL END) AS "AUNQA Tier 1 Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'UPD System SAR' THEN 1 ELSE NULL END) AS "UPD System SAR",
            COUNT(CASE WHEN tt.trainingtype_name = 'UPD SAR' THEN 1 ELSE NULL END) AS "UPD SAR",
            COUNT(CASE WHEN tt.trainingtype_name = 'External Reviewers Training' THEN 1 ELSE NULL END) AS "External Reviewers Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'AUNQA Tier 2 Training' THEN 1 ELSE NULL END) AS "AUNQA Tier 2 Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'ISO 21001:2018 Awareness Orientation' THEN 1 ELSE NULL END) AS "ISO 21001:2018 Awareness Orientation",
            COUNT(CASE WHEN tt.trainingtype_name = 'ISO 21001:2018 Risk Management Training' THEN 1 ELSE NULL END) AS "ISO 21001:2018 Risk Management Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'ISO 21001:2018 Process Mapping and Risk Management Coaching' THEN 1 ELSE NULL END) AS "ISO 21001:2018 Process Mapping and Risk Management Coaching",
            COUNT(CASE WHEN tt.trainingtype_name = 'ISO 21001:2018 Document Control' THEN 1 ELSE NULL END) AS "ISO 21001:2018 Document Control",
            COUNT(CASE WHEN tt.trainingtype_name = 'ISO 21001:2018 Internal Audit Training' THEN 1 ELSE NULL END) AS "ISO 21001:2018 Internal Audit Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'DAP PQA Training' THEN 1 ELSE NULL END) AS "DAP PQA Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'GQMP Training' THEN 1 ELSE NULL END) AS "GQMP Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'AUNQA Tier 3 Training' THEN 1 ELSE NULL END) AS "AUNQA Tier 3 Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'Others' THEN 1 ELSE NULL END) AS "Others"
        FROM 
            qaofficers.qa_officer AS qo
        LEFT JOIN 
            qaofficers.qa_training_details AS qtd
            ON qo.qaofficer_id = qtd.qatr_officername_id AND qtd.qatr_training_del_ind IS False
        LEFT JOIN 
            qaofficers.training_type AS tt
            ON qtd.qatr_training_type = tt.trainingtype_id
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
        LEFT JOIN (
            SELECT
                qtr.qatr_officername_id,
                MAX(tt.trainingtype_competency_id) AS max_competency_id
            FROM qaofficers.qa_training_details qtr
            JOIN qaofficers.training_type tt
                ON qtr.qatr_training_type = tt.trainingtype_id
            WHERE qtr.qatr_training_del_ind = false
            GROUP BY qtr.qatr_officername_id
        ) AS max_comp ON qo.qaofficer_id = max_comp.qatr_officername_id
        LEFT JOIN qaofficers.competency_levels clv
            ON max_comp.max_competency_id = clv.competency_id
        WHERE qo.qaofficer_del_ind IS False
        """
        
        values = []
        if searchterm:
            sql += """
                AND (
                    qo.qaofficer_full_name ILIKE %s OR
                    qo.qaofficer_upmail ILIKE %s OR                    
                    cp.cuposition_name ILIKE %s OR
                    clv.competency_name ILIKE %s OR
                    du.deg_unit_name ILIKE %s OR
                    cl.college_name ILIKE %s OR
                    clus.cluster_name ILIKE %s OR
                    qtd.qatr_training_name ILIKE %s
                )
            """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern] * 8

        sql += """
        GROUP BY 
            qo.qaofficer_id, clv.competency_name, qo.qaofficer_full_name,
             qo.qaofficer_upmail, cp.cuposition_name,
            du.deg_unit_name, cl.college_name, clus.cluster_name
        ORDER BY
            qo.qaofficer_full_name
        """

        cols = ["ID", "Competency Level", "Name", "UP Mail", "Rank/Designation", "Academic Cluster", "Main Unit", "Sub-unit",
                 "iAADS", "PBMS Training", "AUNQA Tier 1 Training", "UPD System SAR", "UPD SAR",
        "External Reviewers Training", "AUNQA Tier 2 Training", "ISO Awareness", "ISO Risk Mgmt",
        "ISO Process Mapping", "ISO Doc Control", "ISO Internal Audit", "DAP PQA", "GQMP",
        "AUNQA Tier 3 Training", "Others"]

        df = db.querydatafromdatabase(sql, values, cols)


        if not df.empty:
            df = df.drop(columns=['ID'])  # Optional: drop ID if not needed
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]

    return [html.Div("Query could not be processed")]
