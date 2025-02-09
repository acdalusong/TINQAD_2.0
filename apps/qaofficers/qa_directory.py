import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db




#year dropdown

def get_available_years():
    # Query to get unique years from the database
    sql = """
    SELECT DISTINCT EXTRACT(YEAR FROM qaofficer_appointment_start) AS year
    FROM qaofficers.qa_officer
    ORDER BY year DESC
    """
    # Execute the query and fetch the results
    values = []  # No need for values in this query
    cols = ['year']  # The column name in the result
    df = db.querydatafromdatabase(sql, values, cols)
    # Extract unique years from the dataframe
    years = df['year'].tolist()
    # Convert years to string and return as dropdown options
    return [{'label': str(year), 'value': str(year)} for year in years]

layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("QA OFFICERS DIRECTORY"),
                        html.Hr(),
                        
                        

                        dbc.Row(
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "+ Add New", color="primary", 
                                        href='/qaofficers_profile?mode=add', 
                                    ),
                                    width="auto",    
                                    
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='qadirectory_filter',
                                        placeholder='Search by Name, Faculty Position, With Basic Paper, Remarks',
                                         
                                        className='ml-auto'   
                                    ),
                                    width="5",
                                ),
                                dbc.Col( 
                                     
                                        dcc.Dropdown(
                                            id='month_dropdown',
                                            options=[
                                                {'label': 'January', 'value': '01'},
                                                {'label': 'February', 'value': '02'},
                                                {'label': 'March', 'value': '03'},
                                                {'label': 'April', 'value': '04'},
                                                {'label': 'May', 'value': '05'},
                                                {'label': 'June', 'value': '06'},
                                                {'label': 'July', 'value': '07'},
                                                {'label': 'August', 'value': '08'},
                                                {'label': 'September', 'value': '09'},
                                                {'label': 'October', 'value': '10'},
                                                {'label': 'November', 'value': '11'},
                                                {'label': 'December', 'value': '12'}
                                            ],
                                            placeholder="Filter by month",
                                        ),
                                        width="3",
                                    
                                ),
                                dbc.Col( 
                                    dcc.Dropdown(
                                        id='year_dropdown',
                                        options=get_available_years(),
                                        placeholder="Filter by year", 
                                    ),
                                    width="2"
                                ),
                            ]
                        ),

                        html.Br(),


                        html.Div(
                            id='qadirectory_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                            }
                        )

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
    Output('qadirectory_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('qadirectory_filter', 'value'),
        Input('month_dropdown', 'value'),
        Input('year_dropdown', 'value'),
    ],
)
def qadirectory_loadlist(pathname, searchterm, selected_month, selected_year):
    if pathname == '/qaofficers_directory':
         
        
        # Fetch the data
        sql = """
            SELECT 
                qaofficer_id AS "ID",
                clusters.cluster_shortname AS "Cluster",
                college.college_shortname AS "College",
                qaofficer_deg_unit AS "Unit",
                qaofficer_full_name AS "Full Name",
                qaofficer_upmail AS "UP Mail",
                qaofficer_fac_posn AS "Faculty Position",
                qaofficer_facadmin_posn AS "Admin Position",
                qaofficer_staff_posn AS "Staff Position",
                cuposition_name AS "QA Position",
                qaofficer_basicpaper AS "With Basic Paper",
                qaofficer_remarks AS "Remarks",
                qaofficer_alc AS "ALC",
                qaofficer_appointment_start AS "Start Term",
                qaofficer_appointment_end AS "End Term",
                qaofficer_role AS "CU-Level role"
            FROM 
                qaofficers.qa_officer  
            LEFT JOIN 
                qaofficers.cuposition ON qaofficer_cuposition_id = cuposition.cuposition_id
            LEFT JOIN 
                public.clusters ON qaofficer_cluster_id = clusters.cluster_id
            LEFT JOIN 
                public.college ON qaofficer_college_id = college.college_id
            WHERE
                NOT qaofficer_del_ind    
        """

        cols = [
            'ID', 'Cluster', 'College', 'Unit', 'Full Name', 'UP Mail', 'Faculty Position',
            'Admin Position', 'Staff Position', 'QA Position', 
            'With Basic Paper', 'Remarks', 'ALC', 'Start Term', 'End Term', 
            'CU-Level role'
        ]
        
        
        # Apply search term filter 
        if searchterm: 
            sql += """ AND (qaofficer_full_name ILIKE %s OR qaofficer_fac_posn ILIKE %s OR qaofficer_basicpaper ILIKE %s OR 
                qaofficer_remarks ILIKE %s) """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern, like_pattern, like_pattern]
        else:
            values = []
        df = db.querydatafromdatabase(sql, values, cols)
        
        # Apply additional filters
        df['Start Term'] = pd.to_datetime(df['Start Term'], errors='coerce')  # Handle errors gracefully
        
        if selected_month:
            df = df[df['Start Term'].dt.month == int(selected_month)]
        
        if selected_year:
            df = df[df['Start Term'].dt.year == int(selected_year)]
        
        # Truncate the 'Start Term' column to ensure it doesn't exceed 10 characters
        df['Start Term'] = df['Start Term'].astype(str).str.slice(0, 10)
        
        

        if df.shape[0] > 0:
            buttons = []
            for qaofficer_id in df['ID']:
                buttons.append(
                    html.Div(
                        dbc.Button('Edit',
                                   href=f'qaofficers_profile?mode=edit&id={qaofficer_id}',
                                   size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
            df['Action'] = buttons

            df = df[['Cluster', 'College', 'Unit', 'Full Name', 'UP Mail', 'Faculty Position',
            'Admin Position', 'Staff Position', 'QA Position', 'With Basic Paper', 'Remarks', 
            'ALC', 'Start Term', 'End Term', 'CU-Level role', 'Action']]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No records to display")
    else:
        raise PreventUpdate
