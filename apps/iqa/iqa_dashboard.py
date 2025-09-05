import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime, timedelta

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db





@app.callback(
    Output('acad_unitheadstotal_count', 'children'),
    [Input('url', 'pathname')]
)
def acad_unitheadscount(pathname):
    if pathname == '/iqa_dashboard':
        today = datetime.today()
        twomonthsfromnow = today + timedelta(days=60)
        sql = """
            SELECT COUNT(*) 
            FROM iqateam.acad_unitheads  
            WHERE 
                unithead_del_ind IS False 
                AND unithead_appointment_end BETWEEN %s AND %s;
        """
        params = (today, twomonthsfromnow)
        acad_unitheadstotal_count = db.query_single_value_db(sql, params)
        return acad_unitheadstotal_count

@app.callback(
    Output('qa_officerstotal_count', 'children'),
    [Input('url', 'pathname')]
)
def qa_officerscount(pathname):
    if pathname == '/iqa_dashboard':
        today = datetime.today()
        twomonthsfromnow = today + timedelta(days=60)
        sql = """
            SELECT COUNT(*) 
            FROM qaofficers.qa_officer 
            WHERE 
                qaofficer_del_ind = False
                AND qaofficer_remarks NOT IN ('Replaced','Dual Role')

                -- AND qaofficer_appointment_end BETWEEN %s AND %s;
        """
        params = (today, twomonthsfromnow)
        qa_officerstotal_count = db.query_single_value_db(sql, params)
        return qa_officerstotal_count


@app.callback(
    Output('iso_facitotal_count', 'children'),
    [Input('url', 'pathname')]
)
def iso_facilitatorscount(pathname):
    if pathname == '/iqa_dashboard':
        sql = """
            SELECT COUNT(*) 
            FROM iqateam.iso_facilitators
            WHERE isofaci_del_ind = False;
        """
        params = ()
        iso_facitotal_count = db.query_single_value_db(sql, params)
        return iso_facitotal_count



layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("IQA DASHBOARD"),
                        html.Hr(),
                        html.Br(),

                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H3("Academic Unit Heads")),
                                        dbc.CardBody(
                                            [ 
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Strong("Total =", style={"margin-right": "3px", "margin-top": "10px"}),
                                                            width="auto"
                                                        ),
                                                        dbc.Col(
                                                            html.Span(id='acad_unitheadstotal_count', style={"font-weight": "bold"}),
                                                            width={"size": 2, "sm": 2, "l": 1},
                                                            style={
                                                                "backgroundColor": "#A9CD46",
                                                                "borderRadius": "10px",
                                                                "padding": "5px",
                                                                "textAlign": "center",
                                                                "marginLeft": "-10px" 
                                                            }
                                                        ),   
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.A(
                                                                dbc.Button("More details..", color="link"),
                                                                href="/dashboard/more_details",
                                                                style={"text-align": "right"}
                                                            ),
                                                            width={"size": 2, "offset": 10}  # Adjust width and offset for alignment
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    id='acadheadsdashboard_list',
                                                    style={
                                                        'marginTop': '20px',
                                                        'overflowX': 'auto',
                                                        'overflowY': 'auto',
                                                        'maxHeight': '300px',
                                                    }
                                                )
                                            ]
                                        )
                                    ],
                                    color="light"
                                ),
                                width=12
                            )
                        ),
html.Br(),
dbc.Row(
    dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader(html.H3("ISO Facilitators")),
                dbc.CardBody(
                    [ 
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Strong("Total =", style={"margin-right": "3px", "margin-top": "10px"}),
                                    width="auto"
                                ),
                                dbc.Col(
                                    html.Span(id='iso_facitotal_count', style={"font-weight": "bold"}),
                                    width={"size": 2, "sm": 2, "l": 1},
                                    style={
                                        "backgroundColor": "#A9CD46",
                                        "borderRadius": "10px",
                                        "padding": "5px",
                                        "textAlign": "center",
                                        "marginLeft": "-10px" 
                                    }
                                ),   
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                        dbc.Button("More details..", color="link"),
                                        href="/dashboard/more_details",
                                        style={"text-align": "right"}
                                    ),
                                    width={"size": 2, "offset": 10} 
                                ),
                            ],
                        ),
                        html.Div(
                            id='isofacidashboard_list',
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto',
                                'overflowY': 'auto',
                                'maxHeight': '300px',
                            }
                        )
                    ]
                )
            ],
            color="light"
        ),
        width=12
    )
),

                        html.Br(),
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H3("Quality Assurance Officers")),
                                        dbc.CardBody(
                                            [ 
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Strong("Total =", style={"margin-right": "3px", "margin-top": "10px"}),
                                                            width="auto"
                                                        ),
                                                        dbc.Col(
                                                            html.Span(id='qa_officerstotal_count', style={"font-weight": "bold"}),
                                                            width={"size": 2, "sm": 2, "l": 1},
                                                            style={
                                                                "backgroundColor": "#A9CD46",
                                                                "borderRadius": "10px",
                                                                "padding": "5px",
                                                                "textAlign": "center",
                                                                "marginLeft": "-10px" 
                                                            }
                                                        ),   
                                                        
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.A(
                                                                dbc.Button("More details..", color="link"),
                                                                href="/dashboard/more_details",
                                                                style={"text-align": "right"}
                                                            ),
                                                            width={"size": 2, "offset": 10}  # Adjust width and offset for alignment
                                                        ),
                                                    ],
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Div(
                                                            id='qaofficersdashboard_list',
                                                            style={
                                                                'marginTop': '20px',
                                                                # 'overflowX': 'auto',
                                                                # 'overflowY': 'auto',
                                                                # 'maxHeight': '300px',
                                                            }
                                                        )
                                                    ],
                                                ),
                                                
                                            ]
                                        )
                                    ],
                                    color="light"
                                ),
                                width=12
                            )
                        ),
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(), html.Br(), html.Br(),
        dbc.Row(
            dbc.Col(
                cm.generate_footer(),
                width={"size": 12, "offset": 0}
            )
        )
    ]
)


@app.callback(
    Output('acadheadsdashboard_list', 'children'),
    [Input('url', 'pathname')]
)
def acadheadsmoredetails_loadlist(pathname):
    if pathname == '/iqa_dashboard':
        today = datetime.today() 

        sql = f"""
            SELECT 
                c.college_name AS "Main Unit",
                COUNT(*) AS "Terms Expiring in 2 Months"
            FROM iqateam.acad_unitheads a
            JOIN public.college c ON a.unithead_college_id = c.college_id
            WHERE 
                a.unithead_appointment_end BETWEEN '{today}' AND '{today + timedelta(days=60)}'
                AND a.unithead_del_ind IS False
            GROUP BY a.unithead_college_id, c.college_name; 
        """
         
        cols = ['Main Unit', 'Terms Expiring in 2 Months']
        
        # Query the database
        df = db.querydatafromdatabase(sql, [], cols)
        
        # Process the DataFrame if not empty
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return (table)
        else:
            return ("No records to display")
    else:
        raise PreventUpdate
    
 
@app.callback(
    Output('isofacidashboard_list', 'children'),
    [Input('url', 'pathname')]
)
def isofacilitatorsmoredetails_loadlist(pathname):
    if pathname == '/iqa_dashboard': 
        sql = """
            SELECT cl.cluster_name AS "Academic Cluster/OCES Group",
                   COUNT(*) AS "ISO Facilitators"
            FROM iqateam.iso_facilitators i
            LEFT JOIN public.clusters cl ON i.isofaci_cluster_id = cl.cluster_id
            WHERE i.isofaci_del_ind = False
            GROUP BY i.isofaci_cluster_id, cl.cluster_name
            ORDER BY cl.cluster_name;
        """
 
        cols = ['Academic Cluster/OCES Group', 'ISO Facilitators']
         
        df = db.querydatafromdatabase(sql, [], cols)
        
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return "No records to display"
    else:
        raise PreventUpdate

        
@app.callback(
    Output('qaofficersdashboard_list', 'children'),
    [Input('url', 'pathname')]
)
def qaofficers_dashboard_summary(pathname):
    if pathname == '/iqa_dashboard':
        expiry_sql = """
        SELECT 
            qaofficer_full_name AS "QA Officer",
            qaofficer_upmail as "UP Mail",
            qaofficer_appointment_end AS "End Date",
            (qaofficer_appointment_end - CURRENT_DATE) AS "Days Remaining"
        FROM qaofficers.qa_officer
        WHERE 
            qaofficer_del_ind = FALSE
            AND qaofficer_remarks   <> 'Replaced'
            AND qaofficer_appointment_end IS NOT NULL
            AND (qaofficer_appointment_end - CURRENT_DATE) < 60;
        """
        remarks_sql = """
        WITH counts AS (
        SELECT
            -- Active: appointment not ended AND not “Replaced”
            SUM(
            CASE
                WHEN qaofficer_del_ind = FALSE
                AND qaofficer_remarks NOT IN ('Replaced','No record','Dual Role')
                AND qaofficer_appointment_end >= CURRENT_DATE
                    
                THEN 1 ELSE 0
            END
            ) AS active,

            -- Lapse: appointment ended AND not “Replaced”
            SUM(
            CASE
                WHEN qaofficer_del_ind = FALSE
                AND qaofficer_appointment_end < CURRENT_DATE
                AND qaofficer_remarks <> 'Replaced'
                THEN 1 ELSE 0
            END
            ) AS lapse,

            -- No record
            SUM(
            CASE
                WHEN qaofficer_del_ind = FALSE
                AND qaofficer_remarks = 'No record'
                THEN 1 ELSE 0
            END
            ) AS norecord,

            -- Dual Role
            SUM(
            CASE
                WHEN qaofficer_del_ind = FALSE
                AND qaofficer_remarks = 'Dual Role'
                THEN 1 ELSE 0
            END
            ) AS dual
        FROM qaofficers.qa_officer
        )

        SELECT 'Active'                AS "Remarks", active    AS "No. of QA Officers" FROM counts
        UNION ALL
        SELECT 'Lapse'                 AS "Remarks", lapse     AS "No. of QA Officers" FROM counts
        UNION ALL
        SELECT 'No record'             AS "Remarks", norecord  AS "No. of QA Officers" FROM counts
        UNION ALL
        SELECT 'Dual Role'             AS "Remarks", dual      AS "No. of QA Officers" FROM counts
        UNION ALL
        SELECT 
        'Total Unique Headcount'     AS "Remarks",
        (active + lapse + norecord)  AS "No. of QA Officers"
        FROM counts;
         """
        
        cluster_sql = """
        SELECT
            COALESCE(cl.cluster_name, 'Unassigned') AS "Academic Cluster",
            COUNT(*) AS "No. of QA Officers"
        FROM qaofficers.qa_officer q
        LEFT JOIN public.clusters cl 
        ON q.qaofficer_cluster_id = cl.cluster_id
        WHERE 
            q.qaofficer_del_ind = FALSE
            AND UPPER(TRIM(q.qaofficer_remarks)) <> 'REPLACED'
        GROUP BY cl.cluster_name

        UNION ALL

        SELECT
            'Total' AS "Academic Cluster",
            COUNT(*) AS "No. of QA Officers"
        FROM qaofficers.qa_officer
        WHERE 
            qaofficer_del_ind = FALSE
            AND UPPER(TRIM(qaofficer_remarks)) <> 'REPLACED';
        """

        position_sql = """
        SELECT
            COALESCE(cuposition.cuposition_name, 'Unassigned') AS "QA Position in the CU",
            COUNT(*) AS "No. of QA Officers"
        FROM qaofficers.qa_officer q
        LEFT JOIN qaofficers.cuposition 
        ON q.qaofficer_cuposition_id = cuposition.cuposition_id
        WHERE 
            q.qaofficer_del_ind = FALSE
            AND q.qaofficer_remarks <> 'Replaced'
        GROUP BY cuposition.cuposition_name

        UNION ALL

        SELECT
            'Total' AS "QA Position in the CU",
            COUNT(*) AS "No. of QA Officers"
        FROM qaofficers.qa_officer
        WHERE 
            qaofficer_del_ind = FALSE
            AND qaofficer_remarks <> 'Replaced';
        """

        df_remarks = db.querydatafromdatabase(remarks_sql, [], ["Remarks", "No. of QA Officers"])
        df_expiry = db.querydatafromdatabase(expiry_sql, [], ["QA Officer", "UP Mail", "End Date", "Days Remaining"])
        # df_remarks = db.querydatafromdatabase(remarks_sql, [], ["Remarks", "No. of QA Officers"])
        df_cluster = db.querydatafromdatabase( cluster_sql, [], ["Academic Cluster", "No. of QA Officers"])
        df_position = db.querydatafromdatabase(position_sql, [], ["QA Position in the CU", "No. of QA Officers"])

        tables = []

        if not df_expiry.empty:
            total_expiring = len(df_expiry)
            
            tables.append(html.H5("QA Officers with Expiring Appointments (< 60 days)"))
            tables.append(dbc.Table.from_dataframe(df_expiry, striped=True, bordered=True, hover=True, size='sm'))
            tables.append(html.P(f"Total QA Officers near expiry: {total_expiring}", style={'fontWeight': 'bold'}))

            if not df_remarks.empty:
                tables.append(html.H5("Summary by Remarks"))
                tables.append(
                    dbc.Table.from_dataframe(
                        df_remarks, striped=True, bordered=True, hover=True, size="sm"
                    )
                )

        if not df_cluster.empty:
            tables.append(html.H5("Summary by Academic Cluster"))
            tables.append(dbc.Table.from_dataframe(df_cluster, striped=True, bordered=True, hover=True, size='sm'))

        if not df_position.empty:
            tables.append(html.H5("Summary by QA Position in the CU"))
            tables.append(dbc.Table.from_dataframe(df_position, striped=True, bordered=True, hover=True, size='sm'))

        return tables

    else:
        raise PreventUpdate
