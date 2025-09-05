import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

# Function to generate a custom table with fixed column widths.
def generate_table(df):
    # define column order & widths
    columns = ['ID number','Last Name','First Name','QAO Team','Position','View','Edit']
    widths = {
        'ID number': '20%', 'Last Name': '15%', 'First Name': '15%',
        'QAO Team':   '15%', 'Position':  '15%', 'View': '10%', 'Edit': '15%'
    }

    # header
    header = [
        html.Th(col, style={'width': widths[col], 'textAlign': 'center'})
        for col in columns
    ]

    # body rows
    rows = []
    for _, row in df.iterrows():
        cells = []
        for col in columns:
            cells.append(html.Td(row[col], style={'textAlign': 'center'}))
        rows.append(html.Tr(cells))

    return dbc.Table(
        # Assemble thead and tbody
        [html.Thead(html.Tr(header)), html.Tbody(rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )

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
                                    html.H1("STAFF PROFILE"),
                                    style={"marginRight": "auto"}
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "➕ Add Staff Profile", color="primary",
                                        href='/staff_profiles_management?mode=add',
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
                                    width=1,
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='staff_profile_filter',
                                        placeholder='Search by Name',
                                        className='ml-auto'   
                                    ),
                                    width="4",
                                ),
                            ],
                            className="align-items-center",     
                        ),
                        
                        html.Div(
                            id='staffprofile_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto', 
                                'overflowY': 'auto',   
                                'maxHeight': '800px',
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


@app.callback(
    Output('staffprofile_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('staff_profile_filter', 'value'),
    ]
)
def staffprofiles_loaduserlist(pathname, searchterm):
    if pathname == '/staff_profiles':
        sql = """  
            SELECT 
                sp.staff_profile_id AS "ID",
                u.user_id_num AS "ID number",
                u.user_sname AS "Last Name", 
                u.user_fname AS "First Name", 
                q.qao_team_names as "QAO Team",
                u.user_position AS "Position"
            FROM adminteam.staff_profiles sp
            LEFT JOIN maindashboard.users u on u.user_id = sp.staff_user_id
            LEFT JOIN maindashboard.offices o ON u.user_office = o.office_id
            LEFT JOIN maindashboard.qao_teams q ON u.user_qao_team_id = q.qao_team_id
            WHERE o.office_name = 'Quality Assurance Office' 
            AND 
            NOT sp.staff_del_ind
        """
        cols = ['ID', 'ID number', 'Last Name', 'First Name', 'QAO Team', 'Position']

        values = []
        
        if searchterm:
            sql += """ AND (u.user_sname ILIKE %s OR u.user_fname ILIKE %s OR u.user_mname ILIKE %s) """
            like_pattern = f"%{searchterm}%"
            values.extend([like_pattern, like_pattern, like_pattern])
        else:
            values = []

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0] > 0:
            # Create Edit buttons for each user and add as a new column.
            view_buttons = []
            edit_buttons = []
            for staff_profile_id in df['ID']:
                view_buttons.append(
                    html.Div(
                        dbc.Button(
                            'View',
                            href=f'staff_profiles_management?mode=view&id={staff_profile_id}',
                            size='sm',
                            color='warning'
                        ),
                        style={'text-align': 'center'}
                    )
                )
            for staff_profile_id in df['ID']:
                edit_buttons.append(
                    html.Div(
                        dbc.Button(
                            'Edit',
                            href=f'staff_profiles_management?mode=edit&id={staff_profile_id}',
                            size='sm',
                            color='danger'
                        ),
                        style={'text-align': 'center'}
                    )
                )
            df['View'] = view_buttons
            df['Edit'] = edit_buttons
            
            # Rearrange dataframe columns as desired.
            df = df[['ID number', 'Last Name', 'First Name', 'QAO Team', 'Position', 'View', 'Edit']]

            # Retrieve teams with their ordering using both columns.
            sql_teams = """
                SELECT DISTINCT qao_team_id, qao_team_names 
                FROM maindashboard.qao_teams q 
                ORDER BY q.qao_team_id
            """
            teams_df = db.querydatafromdatabase(sql_teams, [], ['qao_team_id', 'qao_team_names'])
            teams_df = teams_df.sort_values('qao_team_id')
            team_names = teams_df['qao_team_names'].tolist()
            
            accordion_items = []

            for team in team_names:
                # Filter records for the current team.
                df_team = df[df["QAO Team"] == team]
                if df_team.shape[0] > 0:
                    team_table = generate_table(df_team)  # Use the custom table.
                else:
                    team_table = html.Div(f"No records to display for {team}", className="text-muted")
                
                # Create an accordion item for this team.
                accordion_item = dbc.AccordionItem(
                    title=team,
                    children=[team_table]
                )
                accordion_items.append(accordion_item)

            # Create the accordion containing all team-specific items.
            accordion = dbc.Accordion(
                accordion_items,
                always_open=True  # adjust this if you prefer single-open behavior
            )
            return accordion
        else:
            return html.Div("No records to display")
    else:
        raise PreventUpdate