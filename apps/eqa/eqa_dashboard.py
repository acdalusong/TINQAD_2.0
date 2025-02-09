import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import plotly.graph_objs as go 

 




def get_total_checked():
    sql = f"""
        SELECT COUNT(*) 
        FROM eqateam.assess_report 
        WHERE  
            arep_review_status = 1
            AND arep_del_ind IS FALSE;   
    """
    total_count = db.query_single_value(sql)
    return total_count

def get_total_ongoing():
    sql = f"""
        SELECT COUNT(*) 
        FROM eqateam.sar_report 
        WHERE sarep_del_ind IS FALSE;   
    """
    total_count = db.query_single_value(sql)
    return total_count

def get_total_unchecked():
    sql = f"""
        SELECT COUNT(*) 
        FROM eqateam.sar_report 
        WHERE sarep_del_ind IS FALSE;  
    """

    sar_total_count = db.query_single_value(sql)

    sql = f"""
        SELECT COUNT(*) 
        FROM eqateam.program_details 
        WHERE pro_del_ind IS FALSE;
    """
    prog_total_count = db.query_single_value(sql)

    difference = prog_total_count - sar_total_count
    
    return difference















def tot_certificate_programs():
    sql = f"""
        SELECT COUNT(*)
        FROM eqateam.program_details pd
        JOIN eqateam.sar_report sr ON pd.programdetails_id = sr.sarep_degree_programs_id
        WHERE pd.pro_program_type_id = 1 
        AND sr.sarep_del_ind IS FALSE; 
    """
    certificatetotal_count = db.query_single_value(sql)
    return certificatetotal_count
certificate_programs_count = tot_certificate_programs()


def tot_diploma_programs():
    sql = f"""
        SELECT COUNT(*)
        FROM eqateam.program_details pd
        JOIN eqateam.sar_report sr ON pd.programdetails_id = sr.sarep_degree_programs_id
        WHERE pd.pro_program_type_id = 2 
        AND sr.sarep_del_ind IS FALSE; 
    """
    diplomatotal_count = db.query_single_value(sql)
    return diplomatotal_count
diploma_programs_count = tot_diploma_programs()


def tot_associate_programs():
    sql = f"""
        SELECT COUNT(*)
        FROM eqateam.program_details pd
        JOIN eqateam.sar_report sr ON pd.programdetails_id = sr.sarep_degree_programs_id
        WHERE pd.pro_program_type_id = 3
        AND sr.sarep_del_ind IS FALSE; 
    """
    associatetotal_count = db.query_single_value(sql)
    return associatetotal_count
associate_programs_count = tot_associate_programs()



def tot_undergrad_programs():
    sql = f"""
        SELECT COUNT(*)
        FROM eqateam.program_details pd
        JOIN eqateam.sar_report sr ON pd.programdetails_id = sr.sarep_degree_programs_id
        WHERE pd.pro_program_type_id = 4 
        AND sr.sarep_del_ind IS FALSE; 
    """
    undergradtotal_count = db.query_single_value(sql)
    return undergradtotal_count
undergrad_programs_count = tot_undergrad_programs()



def tot_masters_programs():
    sql = f"""
        SELECT COUNT(*)
        FROM eqateam.program_details pd
        JOIN eqateam.sar_report sr ON pd.programdetails_id = sr.sarep_degree_programs_id
        WHERE pd.pro_program_type_id = 5 
        AND sr.sarep_del_ind IS FALSE; 
    """
    masterstotal_count = db.query_single_value(sql)
    return masterstotal_count
masters_programs_count = tot_masters_programs()



def tot_doctorate_programs():
    sql = f"""
        SELECT COUNT(*)
        FROM eqateam.program_details pd
        JOIN eqateam.sar_report sr ON pd.programdetails_id = sr.sarep_degree_programs_id
        WHERE pd.pro_program_type_id = 6 
        AND sr.sarep_del_ind IS FALSE; 
    """
    doctoratetotal_count = db.query_single_value(sql)
    return doctoratetotal_count
doctorate_programs_count = tot_doctorate_programs()












def generate_donut_chart():
    # Call the functions to get the counts
    checked_count = get_total_checked()
    ongoing_count = get_total_ongoing()
    unchecked_count = get_total_unchecked()
    
    # Create the data for the pie chart
    labels = ['For Next Update', 'Ongoing', 'Not Yet Started']
    values = [checked_count, ongoing_count, unchecked_count]
    
    # Define colors for the pie chart
    colors = ['#39B54A','#F8B237','#E4E4E4']
    
    # Create the pie chart trace
    trace = go.Pie(labels=labels, values=values, hole=0.4, marker=dict(colors=colors))
    
    # Define layout for the pie chart
    layout = go.Layout(showlegend=False)
    
    # Return the figure
    return {'data': [trace], 'layout': layout}

def get_undergraduate_count():
    sql = """
    SELECT COUNT(*)
    FROM eqateam.sar_report sr
    JOIN eqateam.program_details pd ON sr.sarep_degree_programs_id = pd.programdetails_id
    WHERE pd.pro_program_type_id = 'Undergraduate'
    AND sr.sarep_del_ind IS FALSE;
    """
    values = []
    cols = ['total']
    df = db.querydatafromdatabase(sql, values, cols)
    return df['total'].iloc[0]





def generate_sar_submissions_chart(): 
    sql = """
        SELECT 
            pro_program_type_id,
            COUNT(*) AS input_count
        FROM 
            eqateam.program_details pd
        WHERE
            pd.pro_del_ind IS FALSE
            AND EXISTS (
                SELECT 1 
                FROM eqateam.sar_report sr 
                WHERE sr.sarep_degree_programs_id = pd.programdetails_id
                AND sr.sarep_del_ind IS FALSE
            )
        GROUP BY 
            pro_program_type_id;
            
    """
    program_data = db.querydatafromdatabase(sql, [], ['pro_program_type_id', 'input_count']) 
    
    if program_data.empty:  # If there are no submissions
        return {'data': [], 'layout': {'annotations': [{'text': 'No SAR Submissions yet', 'xref': 'paper', 'yref': 'paper', 'showarrow': False, 'font': {'size': 20}}]}}
    
    id_to_label = {1: 'C ', 2: 'D ', 3: 'A ', 4: 'U ', 5: 'M ', 6: 'P '} # Map IDs to labels
    program_data['pro_program_type_label'] = program_data['pro_program_type_id'].map(id_to_label)
     
    color_mapping = {
        'C ': '#A9CD46',
        'D ': '#7EADE4',
        'A ': '#D37157',
        'U ': '#39B54A',
        'M ': '#F8B237',
        'P ': '#40BFBC'
    }

    program_data['color'] = program_data['pro_program_type_label'].map(color_mapping) # Assign colors based on program type
    program_order = ['C ', 'D ', 'A ', 'U ', 'M ', 'P '] # Define the order of program types
    
    # Filter and sort program data based on the defined order
    program_data = program_data[program_data['pro_program_type_label'].isin(program_order)]
    program_data['pro_program_type_label'] = pd.Categorical(program_data['pro_program_type_label'], categories=program_order, ordered=True)
    program_data = program_data.sort_values('pro_program_type_label')
    
    # Create bar chart trace with assigned colors and sorted data
    trace = go.Bar(
        x=program_data['input_count'],  # x-axis now represents the number of submissions
        y=program_data['pro_program_type_label'],  # y-axis represents the program types
        orientation='h',
        marker=dict(color=program_data['color'])
    )
     
    layout = go.Layout(
    margin=dict(l=40, r=40, t=40, b=80),  # Adjust bottom margin for axis titles and legend
    xaxis=dict(title='Number of SAR Submissions', tickvals=list(range(int(max(program_data['input_count'])) + 1)), tickformat='d'),  # Setting x-axis title, integer format, and tick values
    yaxis=dict(title='Program Type'),  # Setting y-axis title
    legend=dict(
        x=0.5,  # Centering legend horizontally
        y=-0.2,  # Placing legend below the graph
        orientation="h"
        )
    ) 
    return {'data': [trace], 'layout': layout} # Return the figure





def summarylegend(get_total_checked, get_total_ongoing, get_total_unchecked):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Span(get_total_checked(), 
                            style={
                                "font-weight": "bold", "display": "flex", 
                                "align-items": "center",  "justify-content": "center",
                                'backgroundColor': '#39B54A', 'borderRadius': '10px',      
                                'padding': '5px'
                            }
                        ),
                        width=3 
                    ),
                    dbc.Col(
                        [
                            html.B(
                                "For Next Update", 
                                style={'marginLeft': '10px', 'textAlign': 'left', 'marginRight': '15px'}
                            ),
                            html.P(
                                "Units that have accomplished their Post EQA report", 
                                style={'marginLeft': '10px', 'textAlign': 'left', 'marginRight': '15px'}
                            ),
                        ],
                        width=9
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Span(get_total_ongoing(), 
                            style={
                                "font-weight": "bold", "display": "flex", 
                                "align-items": "center",  "justify-content": "center",
                                'backgroundColor': '#F8B237', 'borderRadius': '10px',      
                                'padding': '5px'
                            }
                        ),
                        width=3 
                    ),
                    dbc.Col(
                        [
                            html.B(
                                "Currently Ongoing", 
                                style={'marginLeft': '10px', 'textAlign': 'left', 'marginRight': '15px'}
                            ),
                            html.P(
                                "Units that have passed their SAR and are ongoing assessments", 
                                style={'marginLeft': '10px',  'textAlign': 'left', 'marginRight': '15px'}
                            ),
                        ],
                        width=9
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Span(get_total_unchecked(), 
                            style={
                                "font-weight": "bold", "display": "flex", 
                                "align-items": "center",  "justify-content": "center",
                                'backgroundColor': '#E4E4E4', 'borderRadius': '10px',      
                                'padding': '5px'
                            }
                        ),
                        width=3 
                    ),
                    dbc.Col(
                        [
                            html.B(
                                "Not Yet Started", 
                                style={'marginLeft': '10px', 'textAlign': 'left', 'marginRight': '15px'}
                            ),
                            html.P(
                                "Units yet to pass their self-assessment report", 
                                style={'marginLeft': '10px',  'textAlign': 'left', 'marginRight': '15px'}
                            ),
                        ],
                        width=9
                    )
                ]
            )
        ]
    )

 

def degreesummary(summarylegend):
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H3(html.Strong("Summary of Degree Programs with EQA")),
                    html.A("(External Quality Assessment)")
                ]
            ),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id='donut-chart', 
                                    figure=generate_donut_chart(),
                                    config={'displayModeBar': False},   
                                    style={'height': '400px', 'margin-right': '0px', 'margin-top': '0px'}  
                                ),
                                width=7
                            ),
                            dbc.Col(
                                [
                                    summarylegend(get_total_checked, get_total_ongoing, get_total_unchecked),
                                ],
                                width=5 
                            ),
                        ], 
                    ),
                ],   
            )
        ], style={'margin': '0', 'height': '500px'}  # Set the height of the card to 500px
    )

def sar_chart():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Graph(
                        id='sar_chart',
                        figure=generate_sar_submissions_chart(),
                        config={'displayModeBar': False},  # Hide the mode bar for a cleaner look
                        style={'height': '250px', 'margin-top': '0px', 'padding-top': '0px'}  # Adjust height and remove top margin
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            html.Div(
                                [
                                    dbc.Col(
                                        html.Span(tot_certificate_programs(), style={"font-weight": "bold",  "display": "flex", "align-items": "center", "justify-content": "center"}),
                                        style={'backgroundColor': '#A9CD46', 'borderRadius': '10px', 'height': '30px', 'width': '20px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', "margin-right": "3px"}
                                    ),
                                    dbc.Col(
                                        html.P("Certificate Programs (C)", 
                                               style={'marginLeft': '5px',  'textAlign': 'left', 'marginRight': '5px'}),
                                        width=10,
                                    )
                                ],
                                style={'marginBottom': '2px', 'display': 'flex', 'alignItems': 'center'}
                            ),
                            html.Div(
                                [
                                    dbc.Col(
                                        html.Span(tot_diploma_programs(), style={"font-weight": "bold",  "display": "flex", "align-items": "center", "justify-content": "center"}),
                                        style={'backgroundColor': '#7EADE4', 'borderRadius': '10px', 'height': '30px', 'width': '20px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', "margin-right": "3px"}
                                    ),
                                    dbc.Col(
                                        html.P("Diploma Programs (D)", 
                                               style={'marginLeft': '5px',  'textAlign': 'left', 'marginRight': '5px'}),
                                        width=10,
                                    )
                                ],
                                style={'marginBottom': '2px', 'display': 'flex', 'alignItems': 'center'}
                            ),
                            html.Div(
                                [
                                    dbc.Col(
                                        html.Span(tot_associate_programs(), style={"font-weight": "bold",  "display": "flex", "align-items": "center", "justify-content": "center"}),
                                        style={'backgroundColor': '#D37157', 'borderRadius': '10px', 'height': '30px', 'width': '20px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', "margin-right": "3px"}
                                    ),
                                    dbc.Col(
                                        html.P("Associate Programs (A)", 
                                               style={'marginLeft': '5px',  'textAlign': 'left', 'marginRight': '5px'}),
                                        width=10,
                                    )
                                ],
                                style={'marginBottom': '2px', 'display': 'flex', 'alignItems': 'center'}
                            ),
                            html.Div(
                                [
                                    dbc.Col(
                                        html.Span(tot_undergrad_programs(), style={"font-weight": "bold",  "display": "flex", "align-items": "center", "justify-content": "center"}),
                                        style={'backgroundColor': '#39B54A', 'borderRadius': '10px', 'height': '30px', 'width': '20px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', "margin-right": "3px"}
                                    ),
                                    dbc.Col(
                                        html.P("Undergraduate Programs (U)", 
                                               style={'marginLeft': '5px',  'textAlign': 'left', 'marginRight': '5px'}),
                                        width=10,
                                    )
                                ],
                                style={'marginBottom': '2px', 'display': 'flex', 'alignItems': 'center'}
                            ),
                            html.Div(
                                [
                                    dbc.Col(
                                        html.Span(tot_masters_programs(), style={"font-weight": "bold",  "display": "flex", "align-items": "center", "justify-content": "center"}),
                                        style={'backgroundColor': '#F8B237', 'borderRadius': '10px', 'height': '30px', 'width': '20px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', "margin-right": "3px"}
                                    ),
                                    dbc.Col(
                                        html.P("Master's Programs (M)", 
                                               style={'marginLeft': '5px',  'textAlign': 'left', 'marginRight': '5px'}),
                                        width=10,
                                    )
                                ],
                                style={'marginBottom': '2px', 'display': 'flex', 'alignItems': 'center'}
                            ),
                            html.Div(
                                [
                                    dbc.Col(
                                        html.Span(tot_doctorate_programs(), style={"font-weight": "bold",  "display": "flex", "align-items": "center", "justify-content": "center"}),
                                        style={'backgroundColor': '#40BFBC', 'borderRadius': '10px', 'height': '30px', 'width': '20px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', "margin-right": "3px"}
                                    ),
                                    dbc.Col(
                                        html.P("Doctorate Programs (P)", 
                                               style={'marginLeft': '5px',  'textAlign': 'left', 'marginRight': '5px'}),
                                        width=10,
                                    )
                                ],
                                style={'marginBottom': '2px', 'display': 'flex', 'alignItems': 'center'}
                            ),
                        ]
                    )  
                ]
            ),
        ]
    )



layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("EQA DASHBOARD"),
                        html.Hr(),
                        html.Div(  
                            [
                                dcc.Store(id='eqadashboard_toload', storage_type='memory', data=0),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.CardBody(
                                                    html.Div(id='degreesummary')
                                                )
                                            ]
                                        ),   
                                        html.H5(html.B("Assessment Schedule")),
                                        dbc.Row(
                                            [
                                                dbc.Col(  
                                                    dbc.Input(
                                                        type='text',
                                                        id='assesschedule_filter',
                                                        placeholder='🔎 Search by degree program, college',
                                                        className='ml-auto'   
                                                    ),
                                                    width=8,
                                                ),
                                                dbc.Col( 
                                                    dcc.Input(
                                                        id='assesschedule_year',
                                                        type='text',
                                                        placeholder='Enter year1,year2',
                                                        style={'border-radius': '5px', 'height': '35px'}
                                                    ),
                                                    width=3
                                                ),
                                            ]
                                        ),

                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        id='assesschedule_list', 
                                                        style={
                                                            'marginTop': '20px',
                                                            'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                                                        }
                                                    ),
                                                    width="auto",
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3("SAR Submissions", className="mb-0")),
                                                dbc.CardBody(
                                                    html.Div(id='sar_chart')
                                                )
                                             
                                            ]
                                        ),
                                          
                                        html.Br(),
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    html.H3(
                                                        [
                                                            html.Strong("For Checking: SAR"),  
                                                        ],
                                                        className="mb-0",  # Remove bottom margin
                                                        style={'fontSize': '1.5rem'}  # Adjust font size
                                                    )
                                                ),
                                                dbc.CardBody(
                                                    html.Div(
                                                        id='sar_forchecking', 
                                                        style={
                                                            'marginTop': '20px',
                                                            'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                                                        }
                                                    ),
                                                ),
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    html.H3(
                                                        [
                                                            html.Strong("For Checking: Assessments"),  
                                                        ],
                                                        className="mb-0",  # Remove bottom margin
                                                        style={'fontSize': '1.5rem'}
                                                    )
                                                ),
                                                dbc.CardBody(
                                                    html.Div(
                                                        id='assessments_forchecking', 
                                                        style={
                                                            'marginTop': '20px',
                                                            'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                                                        }
                                                    ),
                                                ),
                                            ]
                                        ), 
                                    ],  width=4
                                ), 
                            ]
                        ), 
                    ]
                ),
            ]
        ),
        html.Br(), html.Br(), html.Br(),
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
    Output('sar_forchecking', 'children'),
    [Input('url', 'pathname')]
) 
def eqa_sar_forchecking(pathname):
    if pathname == '/eqa_dashboard': 
        sql = """
        SELECT 
            pd.pro_degree_shortname AS "Degree Program",
            sr.sarep_currentdate AS "Date Submitted"
        FROM 
            eqateam.sar_report sr
        JOIN 
            eqateam.program_details pd ON sr.sarep_degree_programs_id = pd.programdetails_id
        WHERE 
            sr.sarep_checkstatus = 'For Checking'
            AND sr.sarep_del_ind IS FALSE

        """

        cols = ['Degree Program', 'Date Submitted']
        values = []
         
        df = db.querydatafromdatabase(sql, values, cols) 
   
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No SAR for checking yet")
    else:
        return html.Div("No SAR for checking yet")

 
@app.callback(
    Output('assessments_forchecking', 'children'),
    [Input('url', 'pathname')]
) 
def eqa_assessments_forchecking(pathname):
    if pathname == '/eqa_dashboard': 
        sql = """
        SELECT 
            arep_degree_programs_id AS "Degree Program",
            arep_currentdate AS "Date Submitted"
        FROM 
            eqateam.assess_report  
        WHERE 
            arep_checkstatus = 'For Checking'
            AND arep_del_ind IS FALSE

        """

        cols = ['Degree Program', 'Date Submitted']
        values = []
         
        df = db.querydatafromdatabase(sql, values, cols) 
   
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No Assessment for checking yet")
    else:
        return html.Div("No Assessment for checking yet")

 

@app.callback(
    Output('assesschedule_list', 'children'),
    [
        Input('url', 'pathname'), 
        Input('assesschedule_filter', 'value'), 
        Input('assesschedule_year', 'value')
    ]
) 
def assessmentschedule_loadlist(pathname, searchterm, selected_years_text):
    if pathname == '/eqa_dashboard': 
        sql = """  
            SELECT 
                arep_degree_programs_id AS "Degree Program", 
                arep_sched_assessdate AS "Latest Assessment Date",
                EXTRACT(YEAR FROM arep_sched_assessdate + INTERVAL '5 years') AS "Next Assessment Year"
            FROM 
                eqateam.assess_report AS a 
            WHERE
                arep_del_ind IS FALSE
                AND arep_report_type = '2'
                AND arep_review_status = '1'
        """

        cols = ["Degree Program", 'Latest Assessment Date','Next Assessment Year']   
        
        values = []
         
        if selected_years_text:   
            selected_years = selected_years_text.split(',')
            selected_years = [year.strip() for year in selected_years]  # Trim any spaces
            
            # Build the SQL query dynamically to include selected years
            sql += " AND EXTRACT(YEAR FROM arep_sched_assessdate + INTERVAL '5 years') IN %s"
            values.append(tuple(selected_years))
              
        if searchterm:
            sql += " AND (arep_degree_programs_id ILIKE %s)"
            values.extend(['%' + searchterm + '%', '%' + searchterm + '%'])

        df = db.querydatafromdatabase(sql, values, cols)

        
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No recorded assessments yet")
    else:
        raise PreventUpdate






@app.callback(
    [Output('degreesummary', 'children'),
     Output('sar_chart', 'children'),
    ],
    [Input('eqadashboard_toload', 'modified_timestamp')],
    [State('eqadashboard_toload', 'data')]
)
def update_charts(timestamp, toload):
    if toload:
        degreesummary_chart = degreesummary(summarylegend)  # Pass summarylegend here
        sar_chart_component = sar_chart()
        return [degreesummary_chart, sar_chart_component]  # Return both components
    else:
        raise PreventUpdate
    

@app.callback(
    Output('eqadashboard_toload', 'data'),
    Input('url', 'pathname')
)
def trigger_chart_loading(pathname):
    if pathname == '/eqa_dashboard':
        return 1   
    return 0  

