import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

#unit type (acad or admin) dropdown
def get_unit_types():
    sql = """SELECT unit_type_id, unit_type_name FROM public.unit_type ORDER BY unit_type_name"""
    cols = ['value', 'label']
    df = db.querydatafromdatabase(sql, [], cols)
    return df.to_dict('records')

def get_clusters():
    sql = """SELECT cluster_id, cluster_shortname FROM public.clusters ORDER BY cluster_shortname"""
    cols = ['value', 'label']
    df = db.querydatafromdatabase(sql, [], cols)
    return df.to_dict('records')

layout = html.Div([
    dbc.Row([
        cm.sidebar,
        dbc.Col([
            html.H1("ISO FACILITATORS DIRECTORY"),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                    dbc.Button(
                        "+ Add New", color="primary", 
                        href='/iso_facilitator_profile?mode=add'), 
                        width="auto"),

                dbc.Col(
                    dbc.Input(
                        id='isofaci_filter', type='text', placeholder='Search by Name, Faculty Position, Email, Remarks',
                        className = 'ml-auto',
                        ),
                        width=5),
                dbc.Col(
                    dcc.Dropdown(
                        id='unit_type_dropdown', 
                        options=get_unit_types(), 
                        placeholder="Filter by Unit Type"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id='cluster_dropdown', options=get_clusters(), 
                        placeholder="Filter by Academic Cluster/OCES Group"), width=2),
            ]),
            html.Br(),
            html.Div(
                id='isofaci_list', 
                style={'marginTop': '20px', 'overflowX': 'auto'})
        ], width=9, style={'marginLeft': '15px'}),
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0})])
])


@app.callback(
    Output('isofaci_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('isofaci_filter', 'value'),
        Input('unit_type_dropdown', 'value'),
        Input('cluster_dropdown', 'value')
    ]
)
def load_iso_faci_list(pathname, searchterm, unit_type, cluster_id):
    if pathname == '/iso_facilitator_directory':
        sql = """
            SELECT 
                isofaci_id AS "ID",
                unit_type.unit_type_name AS "Academic/Administrative",
                clusters.cluster_shortname AS "Academic Cluster/OCES Group",
                college.college_shortname AS "Main Unit",
                deg_unit.deg_unit_shortname AS "Sub-unit",
                CONCAT(isofaci_fname, ' ', LEFT(isofaci_mname, 1), '. ', isofaci_sname) AS "Full Name",
                isofaci_upmail AS "UP Mail",
                isofaci_fac_posn AS "Faculty Position",
                isofaci_facadmin_posn AS "Admin Position",
                isofaci_staff_posn AS "Staff/REPS Position",
                isofaci_rolecuqa AS "Role in the CU-Level QA Committee",
                cuposition_name AS "QA Position",
                cdqao_name AS "CQAO/DQAO Level",
                isofaci_remarks AS "Remarks"
            FROM iqateam.iso_facilitators
            LEFT JOIN 
                public.unit_type ON isofaci_unit_type_id = unit_type.unit_type_id
            LEFT JOIN 
                qaofficers.cuposition ON isofaci_cuposition_id = cuposition.cuposition_id
            LEFT JOIN 
                public.clusters ON isofaci_cluster_id = clusters.cluster_id
            LEFT JOIN 
                public.college ON isofaci_college_id = college.college_id
            LEFT JOIN 
                public.cdqao ON isofaci_cdqao_id = cdqao.cdqao_id
            LEFT JOIN public.deg_unit  
              ON isofaci_deg_unit_id = deg_unit.deg_unit_id
            WHERE NOT isofaci_del_ind
        """
        cols = ["ID", "Academic/Administrative", "Academic Cluster/OCES Group", "Main Unit", "Sub-unit",
                "Full Name", "UP Mail", "Faculty Position", "Admin Position", "Staff/REPS Position",
                "Role in the CU-Level QA Committee", "QA Position", "CQAO/DQAO Level", "Remarks"]
        
#apply search filter
        if searchterm:
            sql += """ AND (isofaci_fname ILIKE %s OR isofaci_fac_posn ILIKE %s OR isofaci_upmail ILIKE %s
                    OR isofaci_remarks ILIKE %s)"""
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern, like_pattern, like_pattern]
        else:
            values = []

        if unit_type:
            sql += " AND isofaci_unit_type_id = %s"
            values.append(unit_type)

        if cluster_id:
            sql += " AND isofaci_cluster_id = %s"
            values.append(cluster_id)

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0] > 0:
            buttons = []
            for isofaci_id in df['ID']:
                buttons.append(
                    html.Div(
                    dbc.Button('Edit', href=f'iso_facilitator_profile?mode=edit&id={isofaci_id}', 
                               size='sm', color='warning'),
                    style={'text-align': 'center'}
                )
                )
            df['Action'] = buttons

            df = df[["Academic/Administrative", "Academic Cluster/OCES Group", "Main Unit", "Sub-unit",
                "Full Name", "UP Mail", "Faculty Position", "Admin Position", "Staff/REPS Position",
                "Role in the CU-Level QA Committee", "QA Position", "CQAO/DQAO Level", "Remarks", "Action"]]
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No records to display")
    else:
        raise PreventUpdate
