import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, dash_table
from dash import callback_context

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import base64
import os
from urllib.parse import urlparse, parse_qs
import flask

# Define the highlight colors for styling
highlight_colors = {
    'primary': "#0a4323",    # Main headers
    'secondary': "#7a0911",  # Section titles
    'accent': "#f8b237"      # Accent for borders/emphasis
}

# Function to generate a custom table with fixed column widths.
def generate_table(df):
    # Define the column order and their widths.
    columns = ['Full Name', 'Position', 'QAO Team', 'View', 'Edit']
    widths = {
        'Full Name': '40%',
        'Position': '20%',
        'QAO Team': '20%',
        'View': '10%',
        'Edit': '10%'
    }
    
    # Create table header with fixed widths.
    header = [html.Th(col, style={'width': widths[col], 'textAlign': 'center'}) for col in columns]
    
    # Build the table rows.
    rows = []
    for i, row in df.iterrows():
        cells = []
        for col in columns:
            cells.append(html.Td(row[col], style={'width': widths[col], 'textAlign': 'center'}))
        rows.append(html.Tr(cells))
    
    return html.Table(
        [html.Thead(html.Tr(header))] + [html.Tbody(rows)],
        className="table table-striped table-bordered table-hover table-sm",
        style={'width': '100%', 'tableLayout': 'fixed'}
    )

# Define the layout for the Peer Evaluation Form
allowed_layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H1("PEER EVALUATION"),
                                    style={"marginRight": "auto"}
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "➕ Add Peer Evaluation", color="primary",
                                        href='/peer_evaluation_form_entry?mode=add',
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
                                        id='eval_name_filter',
                                        placeholder='Search by Name',
                                        className='ml-auto'
                                    ),
                                    width="4",
                                ),
                            ],
                            className="align-items-center",
                        ),

                        html.Div(
                            "No peer evaluations submitted for the current period",
                            id='eval_list',
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

@app.callback(
    Output('eval_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('eval_name_filter', 'value'),
    ],
    [
        State('currentuserid', 'data'),
    ]
)
def staffprofiles_loaduserlist(pathname, searchterm, currentuserid):
    if pathname == '/peer_evaluation_landing':
        sql = """  
            SELECT 
                pe.evaluation_id AS "ID",
                CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS "Full Name",
                q.qao_team_names as "QAO Team",
                u.user_position AS "Position"
            FROM director.peer_evaluations pe
            LEFT JOIN maindashboard.users u ON u.user_id = pe.evaluatee_id
            LEFT JOIN maindashboard.offices o ON u.user_office = o.office_id
            LEFT JOIN maindashboard.qao_teams q ON u.user_qao_team_id = q.qao_team_id
            WHERE o.office_name = 'Quality Assurance Office' 
            AND evaluator_id = %s
			AND evaluation_period_id = (
			SELECT period_id   AS value
				FROM director.evaluation_periods 
				WHERE active_status = TRUE
            	AND period_del_ind = FALSE
			)
            AND pe.peer_eval_delete_ind =FALSE
        """
        values = [currentuserid]
        cols = ['ID', 'Full Name', 'QAO Team', 'Position']

        if searchterm:
            sql += """ AND (u.user_sname ILIKE %s OR u.user_fname ILIKE %s OR u.user_mname ILIKE %s) """
            like_pattern = f"%{searchterm}%"
            values += [like_pattern, like_pattern, like_pattern]
        else:
            values += []

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0] > 0:
            # Create separate "View" and "Edit" buttons for each evaluation.
            view_buttons = []
            edit_buttons = []
            for evaluation_id in df['ID']:
                view_buttons.append(
                    dbc.Button(
                        'View',
                        href=f'/peer_evaluation_form_entry?mode=view&id={evaluation_id}',
                        size='sm',
                        color='warning'
                    )
                )
                edit_buttons.append(
                    dbc.Button(
                        'Edit',
                        href=f'/peer_evaluation_form_entry?mode=edit&id={evaluation_id}',
                        size='sm',
                        color='danger'
                    )
                )
            df['View'] = view_buttons
            df['Edit'] = edit_buttons
            # Rearrange dataframe columns as desired.
            df = df[['Full Name', 'Position', 'QAO Team', 'View', 'Edit']]

            # Retrieve teams with their ordering using both columns.
            sql_teams = """
                SELECT DISTINCT qao_team_id, qao_team_names 
                FROM maindashboard.qao_teams q 
                WHERE qao_team_id != 1
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
            return html.Div("No peer evaluations submitted for the current period")
    else:
        raise PreventUpdate

not_allowed_layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("Peer Evaluation Form Submission is not yet available."),
                        html.Hr(),

                        html.P("Wait for the evaluation period to start."),    
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ],
)


main_layout = html.Div(
    [
        dbc.Row(
            [
                dcc.Store(id='layout_load', storage_type='memory', data=0),
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("Peer Evaluation Form Submission is not yet available."),
                        html.Hr(),

                        html.P("Wait for the evaluation period to start."),  
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ],
    id="main_layout"
)

@app.callback(
    Output('layout_load', 'data'),
    Input('url', 'pathname'),
)
def layout_options(pathname):
    if pathname == '/peer_evaluation_landing':
        sql = """
            SELECT COUNT(*)
            FROM director.main_decision
            WHERE decision_bool = 'True'
        """
        values = []
        cols = ['count']
        df = db.querydatafromdatabase(sql, values, cols)

        main_decision_result = int(df['count'][0])

        if main_decision_result > 0:
            layout_value = 1
        else:
            layout_value = -1

        return layout_value

    raise PreventUpdate

@app.callback(
    Output('main_layout', 'children'),
    Input('layout_load', 'data')
)
def final_layout_options(value):
    if value > 0:
        return allowed_layout
    else:
        return not_allowed_layout
