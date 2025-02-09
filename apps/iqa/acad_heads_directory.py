import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import datetime

#year dropdown

def get_available_years():
    # Query to get unique years from the database
    sql = """
    SELECT DISTINCT EXTRACT(YEAR FROM unithead_appointment_start) AS year
    FROM iqateam.acad_unitheads
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
                        html.H1("ACADEMIC UNIT HEADS DIRECTORY"),
                        html.Hr(),
                       

                        dbc.Row(
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "+ Add New", color="primary", 
                                        href='/acadheads_profile?mode=add', 
                                    ),
                                    width="auto",    
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='acadheadsdirectory_filter',
                                        placeholder='Search by Name, Email, Faculty Position, Unit',
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
                                            placeholder="Filter by Start Term month",
                                        ),
                                        width="3",
                                    
                                ),
                                dbc.Col( 
                                    dcc.Dropdown(
                                        id='year_dropdown',
                                        options=get_available_years(),
                                        placeholder="Filter by Start Term year", 
                                    ),
                                    width="2"
                                ),
                            ]
                        ),

                        html.Br(),

                        

                        
  
                        # Placeholder for the users table
                        html.Div(
                            id='acadheadsdirectory_list', 
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
    Output('acadheadsdirectory_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('acadheadsdirectory_filter', 'value'),
        Input('month_dropdown', 'value'),  # Corrected input name
        Input('year_dropdown', 'value')
    ]
)


# Function to fetch data and generate the table
def acadheadsdirectory_loadlist(pathname, searchterm, selected_month, selected_years):
    if pathname == '/acad_heads_directory':
        # SQL query to fetch the data from the database
        sql = """
            SELECT 
                acad_unitheads.unithead_id AS "ID",
                clusters.cluster_shortname AS "Cluster",
                college.college_shortname AS "College",
                acad_unitheads.unithead_deg_unit AS "Unit",
                acad_unitheads.unithead_full_name AS "Full Name",   
                acad_unitheads.unithead_upmail AS "Up Mail",
                acad_unitheads.unithead_fac_posn AS "Faculty Position",
                acad_unitheads.unithead_desig AS "Designation",
                acad_unitheads.unithead_appointment_start AS "Start Term",
                acad_unitheads.unithead_appointment_end AS "End Term"
            FROM
                iqateam.acad_unitheads
                LEFT JOIN public.clusters ON acad_unitheads.unithead_cluster_id = clusters.cluster_id
                LEFT JOIN public.college ON acad_unitheads.unithead_college_id = college.college_id
                WHERE
                    NOT unithead_del_ind
                 
        """

        cols = [
            'ID', 'Cluster', 'College', 'Unit', 'Full Name', 'Up Mail',
            'Faculty Position', 'Designation', 'Start Term', 'End Term'
        ]
        
        df = db.querydatafromdatabase(sql, [], cols)  

        if searchterm:
            search_cols = ['Full Name', 'Up Mail', 'Faculty Position', 'Unit']
            df = df[df[search_cols].apply(lambda row: any(searchterm.lower() in str(cell).lower() for cell in row), axis=1)]

        # Apply additional filters if necessary
        df['Start Term'] = pd.to_datetime(df['Start Term'])

        if selected_month:
            df = df[df['Start Term'].dt.month == int(selected_month)]

        if selected_years:
            df = df[df['Start Term'].dt.year.isin(selected_years)]
        
        # Truncate the 'Start Term' column to ensure it doesn't exceed 10 characters
        df['Start Term'] = df['Start Term'].astype(str).str.slice(0, 10)

        if df.shape[0] > 0:
            buttons = []
            for unithead_id in df['ID']:
                buttons.append(
                    html.Div(
                        dbc.Button('Edit',
                                   href=f'acadheads_profile?mode=edit&id={unithead_id}',
                                   size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
            df['Action'] = buttons

            df = df[['Cluster', 'College', 'Unit', 'Full Name', 'Up Mail',
            'Faculty Position', 'Designation', 'Start Term', 'End Term', 'Action']]


        # Generate the table from the filtered DataFrame
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No records to display")
    else:
        raise PreventUpdate
    
      
 
