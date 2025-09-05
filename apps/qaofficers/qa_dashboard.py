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

# Function to fetch the total count of Arts and Letters QA Officers
@app.callback(
    Output('get_total_asl', 'children'),
    [Input('url', 'pathname')]
)
def get_total_asl(pathname):
    total_count = None
    if pathname == '/QAOfficers_dashboard': 
        sql = """
            SELECT COUNT(*) 
            FROM qaofficers.qa_officer 
            WHERE 
                qaofficer_cluster_id = 1
                AND qaofficer_del_ind IS False
                AND EXISTS (
                    SELECT 1
                    FROM qaofficers.qa_training_details 
                    WHERE 
                        qatr_officername_id = qaofficers.qa_officer.qaofficer_id
                        AND qatr_training_del_ind IS FALSE
                );
        """ 
        total_count = db.query_single_value(sql)
    return total_count


# Function to fetch the total count of Management and Economics QA Officers
@app.callback(
    Output('get_total_mae', 'children'),
    [Input('url', 'pathname')]
)
def get_total_mae(pathname):
    total_count = None
    if pathname == '/QAOfficers_dashboard': 
        sql = """
            SELECT COUNT(*) 
            FROM qaofficers.qa_officer 
            WHERE 
                qaofficer_cluster_id = 2
                AND qaofficer_del_ind IS False
                AND EXISTS (
                    SELECT 1
                    FROM qaofficers.qa_training_details 
                    WHERE 
                        qatr_officername_id = qaofficers.qa_officer.qaofficer_id
                        AND qatr_training_del_ind IS FALSE
                );
        """ 
        total_count = db.query_single_value(sql)
    return total_count
 


# Function to fetch the total count of Science and Technology QA Officers
@app.callback(
    Output('get_total_sat', 'children'),
    [Input('url', 'pathname')]
)
def get_total_sat(pathname):
    total_count = None
    if pathname == '/QAOfficers_dashboard': 
        sql = """
            SELECT COUNT(*) 
            FROM qaofficers.qa_officer 
            WHERE 
                qaofficer_cluster_id = 3
                AND qaofficer_del_ind IS False
                AND EXISTS (
                    SELECT 1
                    FROM qaofficers.qa_training_details 
                    WHERE 
                        qatr_officername_id = qaofficers.qa_officer.qaofficer_id
                        AND qatr_training_del_ind IS FALSE
                );
        """ 
        total_count = db.query_single_value(sql)
    return total_count
 
 
# Function to fetch the total count of Social Scieneces and Law Qa Officers
@app.callback(
    Output('get_total_ssl', 'children'),
    [Input('url', 'pathname')]
)
def get_total_ssl(pathname):
    total_count = None
    if pathname == '/QAOfficers_dashboard': 
        sql = """
            SELECT COUNT(*) 
            FROM qaofficers.qa_officer 
            WHERE 
                qaofficer_cluster_id = 4
                AND qaofficer_del_ind IS False
                AND EXISTS (
                    SELECT 1
                    FROM qaofficers.qa_training_details 
                    WHERE 
                        qatr_officername_id = qaofficers.qa_officer.qaofficer_id
                        AND qatr_training_del_ind IS FALSE
                );
        """ 
        total_count = db.query_single_value(sql)
    return total_count
 
facultytrainedcard = dbc.Card(
    [
        dbc.CardHeader(html.H5(html.B("No. of faculty with QA Training"))), 
        dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                        [
                            html.Span(id='get_total_asl', style={"font-weight": "bold"}), 
                            html.Div("Arts and Letters", style={'textAlign': 'center'}),
                        ],
                        width="auto",
                        style={
                            "backgroundColor": "#f8d7da",
                            'height': '70px', 
                            'width': '25%', 
                            "borderRadius": "10px",
                            "padding": "10px",
                            "textAlign": "center",
                            "marginBottom": "10px"
                        }
                    ),   
                    dbc.Col(
                        [
                            html.Span(id='get_total_mae', style={"font-weight": "bold"}), 
                            html.Div("Management and Economics", style={'textAlign': 'center'}),
                        ],
                        width="auto",
                        style={
                            "backgroundColor": "#cce5ff",
                            'height': '70px', 
                            'width': '25%', 
                            "borderRadius": "10px",
                            "padding": "10px",
                            "textAlign": "center",
                            "marginBottom": "10px"
                        }
                    ),   
                    dbc.Col(
                        [
                            html.Span(id='get_total_sat', style={"font-weight": "bold"}), 
                            html.Div("Science and Technology", style={'textAlign': 'center'}),
                        ],
                        width="auto",
                        style={
                            "backgroundColor": "#fff3cd",
                            'height': '70px', 
                            'width': '25%',  
                            "borderRadius": "10px",
                            "padding": "10px",
                            "textAlign": "center",
                            "marginBottom": "10px"
                        }
                    ),   
                    dbc.Col(
                        [
                            html.Span(id='get_total_ssl', style={"font-weight": "bold"}), 
                            html.Div("Social Sciences and Law", style={'textAlign': 'center'}),
                        ],
                        width="auto",
                        style={
                            "backgroundColor": "#d4edda",
                            'height': '70px', 
                            'width': '25%',  
                            "borderRadius": "10px",
                            "padding": "10px",
                            "textAlign": "center",
                            "marginBottom": "10px"
                        }
                    ),    
                ],
                className="g-3"  # Adds gutters (spacing) between columns
            )
        ),   
    ],
    className="mb-3" 
)


@app.callback(
    Output('competency_counts_table', 'children'),
    Input('url', 'pathname')
)
def update_competency_counts(pathname):
    if pathname == '/QAOfficers_dashboard':
        sql = """
        SELECT
            clus.cluster_name AS "Academic Cluster",
            clv.competency_name AS "Competency Level",
            max_comp.max_competency_id  AS "Competency ID",
            COUNT(qo.qaofficer_id) AS "Officer Count"
        FROM qaofficers.qa_officer AS qo
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
        --LEFT JOIN qaofficers.training_type tt
            --ON tt.trainingtype_competency_id = clv.competency_id
        LEFT JOIN public.clusters clus
            ON qo.qaofficer_cluster_id = clus.cluster_id
        WHERE qo.qaofficer_del_ind IS FALSE
        GROUP BY clus.cluster_name, clv.competency_name, max_comp.max_competency_id
        ORDER BY clus.cluster_name, max_comp.max_competency_id;

        """
        cols = ["Academic Cluster", "Competency Level", "Competency ID", "Officer Count"]
        df = db.querydatafromdatabase(sql, [], cols)

        if not df.empty:
            # Sort by Competency ID
            # competency_order = df[['Competency Level', 'Competency ID']].drop_duplicates().sort_values('Competency ID')
            # ordered_levels = competency_order['Competency Level'].tolist()
            competency_order = df[['Competency Level', 'Competency ID']].drop_duplicates().sort_values('Competency ID')
            ordered_levels = [lvl for lvl in competency_order['Competency Level'].tolist() if lvl is not None]

            # Pivot table with ordered columns
            pivot_df = df.pivot_table(
                index="Academic Cluster",
                columns="Competency Level",
                values="Officer Count",
                fill_value=0
            )[ordered_levels]  # Ensure columns are in the correct order

            # Add total row at the bottom
            total_row = pivot_df.sum().to_frame().T
            total_row.index = ["Total"]
            final_df = pd.concat([pivot_df, total_row])

            # Table headers
            header = [html.Th("Academic Cluster")] + [html.Th(col) for col in final_df.columns]

            # Table body
            table_rows = []
            for idx, row in final_df.iterrows():
                row_cells = [html.Td(idx)] + [html.Td(row[col]) for col in final_df.columns]
                style = {'fontWeight': 'bold'} if idx == "Total" else {}
                table_rows.append(html.Tr(row_cells, style=style))

            return dbc.Table(
                [html.Thead(html.Tr(header)), html.Tbody(table_rows)],
                bordered=True,
                hover=True,
                size='sm'
            )
        else:
            return html.Div("No records to display")
    else:
        raise PreventUpdate

competency_counts_card = dbc.Card(
    [
        dbc.CardHeader(html.H5(html.B("QA Officers by Competency Level per Cluster"))),
        dbc.CardBody(
            html.Div(id='competency_counts_table')
        )
    ],
    className="mb-3"
)



trainedofficerscard = dbc.Card(
    [
        dbc.CardHeader(html.H5(html.B("Total Trained Officers"))), 
        dbc.CardBody([
            
            dbc.Row(
                [
                    dbc.Col( 
                        html.Div(
                            id='trainedofficers_clusterlist', 
                                style={
                                    'marginTop': '20px',
                                    'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                                    }
                            ),
                        )
                    ]
                ),

            
            dbc.Row(
                [ 
                    dbc.Col(
                        dcc.Input(
                            id='qatr_currentyear',
                            type='number',   
                            value=current_year, 
                            style={'width': '100%'}, 
                        ),
                        width=2,  
                    ),
                ],
                className="my-2"  
            ),
            ]
        ),   
    ],
    className="mb-3" 
)


qaofficerscard = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='qaotraininglist_filter',
                                placeholder='🔎 Search by Name, UP Mail, Training, etc',
                                className='ml-auto'
                            ),
                            width="6",
                        ),
                        dbc.Col(
                            dbc.Button(
                                "➕ Edit QA Trainings", 
                                color="primary", 
                                href='/qaofficers_training',
                            ),
                            width="auto",
                            className="ml-auto",
                        ), 
                         dbc.Col(
                            dbc.Button(
                                "📄 View Faculty CDF", 
                                color="secondary", 
                                href='/qaofficers_faculty_cdf',
                            ),
                            width="auto",
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
                                id='qaotraininglist_list',
                                style={
                                    'overflowX': 'auto',
                                    'overflowY': 'auto',
                                    'maxHeight': '500px',
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
                        html.H1("QA OFFICERS DASHBOARD"),
                        html.Hr(),
                        html.Br(),

                        facultytrainedcard,
                        competency_counts_card,
                        trainedofficerscard,
                        qaofficerscard,
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
    [Output('trainedofficers_clusterlist', 'children')],
    [
        Input('url', 'pathname'),
        Input('qatr_currentyear', 'value')
    ]
    )

def clustertraininglist_loadlist(pathname, search_term):
    if pathname == '/QAOfficers_dashboard':  
        sql = """
        SELECT 
            clus.cluster_name AS "Academic Cluster",
            qtd.qatr_training_year AS "Year",
            COUNT(CASE WHEN tt.trainingtype_name IN ('iAADS', 'PBMS Training') THEN 1 END) AS "iAADS/PBMS Training",
            COUNT(CASE WHEN tt.trainingtype_name IN ('AUNQA Tier 1 Training', 'UPD System SAR', 'UPD SAR') THEN 1 END) AS "AUNQA Tier 1/UPD System SAR/UPD SAR",
            COUNT(CASE WHEN tt.trainingtype_name IN ('External Reviewers Training', 'AUNQA Tier 2 Training') THEN 1 END) AS "External Reviewers/AUNQA Tier 2",
            COUNT(CASE WHEN tt.trainingtype_name IN ('ISO 21001:2018 Awareness Orientation', 'ISO 21001:2018 Risk Management Training', 'ISO 21001:2018 Process Mapping and Risk Management Coaching', 'ISO 21001:2018 Document Control') THEN 1 END) 
            AS "ISO 21001:2018 Awareness Orie/Risk Mngmnt Training/Process Mapping/Doc Control",
            COUNT(CASE WHEN tt.trainingtype_name IN ('ISO 21001:2018 Internal Audit Training', 'DAP PQA Training', 'GQMP Training') THEN 1 END) AS "ISO 21001:2018 Internal Audit/DAP PQA/GQMP Training",
            COUNT(CASE WHEN tt.trainingtype_name = 'AUNQA Tier 3 Training' THEN 1 END) AS "AUNQA Tier 3",
            COUNT(CASE WHEN tt.trainingtype_name = 'Others' THEN 1 END) AS "Others"
        FROM 
            qaofficers.qa_training_details AS qtd
        LEFT JOIN 
            qaofficers.qa_officer AS qo
            ON qtd.qatr_officername_id = qo.qaofficer_id
        LEFT JOIN 
            public.clusters AS clus
            ON qo.qaofficer_cluster_id = clus.cluster_id
        LEFT JOIN
            qaofficers.training_type AS tt
            ON qtd.qatr_training_type = tt.trainingtype_id
        WHERE 
            qatr_training_del_ind IS False
        GROUP BY 
            clus.cluster_name, qtd.qatr_training_year
        ORDER BY 
            clus.cluster_name, qtd.qatr_training_year
        """
        cols = [
            'Academic Cluster', 'Year', 
            'iAADS/PBMS Training', 
            'AUNQA Tier 1/UPD System SAR/UPD SAR',
            'External Reviewers/AUNQA Tier 2',
            'ISO 21001:2018 Awareness Orie/Risk Mngmnt Training/Process Mapping/Doc Control',
            'ISO 21001:2018 Internal Audit/DAP PQA/GQMP Training',
            'AUNQA Tier 3', 'Others'
            ]

 
        df = db.querydatafromdatabase(sql, [], cols)
 
        if search_term is not None:
            df = df[df['Year'] == search_term]  
        
       # Calculate the totals
        totals = df.iloc[:, 2:].sum(axis=0).to_frame().T
        totals['Academic Cluster'] = 'Total'
        totals['Year'] = ''  # Leave the 'Year' column empty for the totals row

        # Append the totals row
        df = pd.concat([df, totals], ignore_index=True)
 
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    else:
        raise PreventUpdate
    

@app.callback(
    Output('qaotraininglist_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('qaotraininglist_filter', 'value'),
    ]
)
def traininglist_loadlist(pathname, searchterm):
    if pathname == '/QAOfficers_dashboard': 
        base_sql = """
            SELECT 
                qo.qaofficer_id AS "ID",
                qo.qaofficer_full_name AS "Name",
                cp.cuposition_name AS "Rank/Designation",
                clus.cluster_name AS "Academic Cluster",
                cl.college_name AS "Main Unit",
                deg_unit.deg_unit_name AS "Sub-unit",
                STRING_AGG(
                    CASE 
                        WHEN NOT qtd.qatr_training_del_ind 
                        THEN qtd.qatr_training_name || ' (' || qtd.qatr_training_year || ')' 
                        ELSE NULL 
                    END,
                    ', '
                ) AS "Trainings"
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
            LEFT JOIN public.deg_unit  
                ON qo.qaofficer_deg_unit_id = deg_unit.deg_unit_id

            WHERE
                qo.qaofficer_del_ind IS False
        """

        values = []
        if searchterm:
            base_sql += """
                AND (
                    qo.qaofficer_full_name ILIKE %s OR
                    cp.cuposition_name ILIKE %s OR
                    du.deg_unit_name ILIKE %s OR
                    cl.college_name ILIKE %s OR
                    clus.cluster_name ILIKE %s OR
                    qtd.qatr_training_name ILIKE %s
                )
            """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern] * 6

        base_sql += """
            GROUP BY 
                qo.qaofficer_id, qo.qaofficer_full_name, cp.cuposition_name, deg_unit.deg_unit_name, cl.college_name, clus.cluster_name
        """

        cols = ["ID", 'Name', 'Rank/Designation', 'Academic Cluster','Main Unit','Sub-unit', 'Trainings']   

        df = db.querydatafromdatabase(base_sql, values, cols) 

        if not df.empty:   
            df = df[['Name', 'Rank/Designation', 'Academic Cluster', 'Main Unit', 'Sub-unit', 'Trainings' ]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]

    return [html.Div("Query could not be processed")]
 