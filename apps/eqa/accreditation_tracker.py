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
    SELECT DISTINCT EXTRACT(YEAR FROM arep_sched_assessdate) AS year
    FROM eqateam.assess_report
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
                        html.H1("EQA TRACKER"),
                        html.Hr(),
 
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='accreditationtracker_filter',
                                        placeholder='🔎 Search by degree program or assessment title',
                                        className='ml-auto'   
                                    ),
                                    width="6",
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
                                        multi=True  # Allow multiple year selection if needed
                                    ),
                                    width="2"
                                ),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.P(html.B("Filter by EQA Type", className="mr-1")),
                                    width="auto"  # Adjust the width to fit the content
                                ),
                                dbc.Col(
                                    dcc.Checklist(
                                        id='accred_approv_eqa',
                                        options=[],
                                        inline=True,
                                        labelStyle={'marginRight': '10px'}  # Adjust the margin as needed
                                    ),
                                    width="auto"  # Adjust the width to fit the content
                                ),
                                dbc.Col(
                                    dbc.Button("Deselect EQA type filters", id="deselect_button", color="danger", size="sm"),
                                    width="auto",  # Adjust the width to fit the content
                                    style={"margin-left": "auto"}  # Align the button to the right
                                ),
                            ]
                        ),
 
                        html.Div(
                            id='accreditationtracker_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                            }
                        ),
                         

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















#eqa types dropdown
@app.callback(
    Output('accred_approv_eqa', 'options'),
    Input('url', 'pathname')
)
def populate_approvedeqa_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessment_tracker':
        sql ="""
        SELECT approv_eqa_name as label, approv_eqa_id as value
        FROM eqateam.approv_eqa
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        accred_approvedeqa_types = [{'label': row['label'], 'value': row['value']} for _, row in df.iterrows()]
        return accred_approvedeqa_types
    else:
        raise PreventUpdate

#eqa deselect
@app.callback(
    Output('accred_approv_eqa', 'value'),
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
    Output('accreditationtracker_list', 'children'),
    [
        Input('url', 'pathname'), 
        Input('accreditationtracker_filter', 'value'), 
        Input('accred_approv_eqa', 'value'),
        Input('month_dropdown', 'value'),  # Add input for the month dropdown
        Input('year_dropdown', 'value')
    ]
)


def accreditationtracker_loadlist(pathname, searchterm, eqa_types, selected_month, selected_years):
    if pathname == '/assessment_tracker': 
        sql = """  
            SELECT 
                TO_CHAR(arep_sched_assessdate, 'FMMonth FMDD, YYYY') AS "Start Assessment Date", 
                arep_sched_assessduration AS "Assessment Duration", 
                arep_title AS "Assessment Title",
                arep_degree_programs_id AS "Degree Program", 
                eqa.approv_eqa_name AS "EQA Type"
            FROM 
                eqateam.assess_report AS a 
            JOIN 
                eqateam.approv_eqa AS eqa ON a.arep_approv_eqa = eqa.approv_eqa_id
            WHERE
                arep_del_ind IS FALSE
        """

        cols = ['Start Assessment Date', "Assessment Duration", 'Assessment Title','Degree Program' , 'EQA Type']   
        
        values = []
        
        if eqa_types:
            sql += " AND arep_approv_eqa IN %s"
            values.append(tuple(eqa_types))

        if selected_month:  # Add condition to filter by selected month
            sql += " AND EXTRACT(MONTH FROM arep_sched_assessdate) = %s"
            values.append(selected_month)

        if selected_years:  # selected_years will be a list of selected years
            sql += " AND EXTRACT(YEAR FROM arep_sched_assessdate) IN %s"
            values.append(tuple(selected_years))

        if searchterm:
            # Adding search condition for arep_title and arep_degree_programs_id
            sql += " AND (arep_title ILIKE %s OR arep_degree_programs_id ILIKE %s)"
            values.extend(['%' + searchterm + '%', '%' + searchterm + '%'])


        df = db.querydatafromdatabase(sql, values, cols) 

        # Generate the table from the DataFrame
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No records to display")
    else:
        raise PreventUpdate