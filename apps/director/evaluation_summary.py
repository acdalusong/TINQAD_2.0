import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, dash_table
from dash import callback_context
from dash import dcc
import io
from weasyprint import HTML
from flask import render_template
from apps.director import pdf_utils
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


highlight_colors = { 
    'primary': "#0a4323",     # Main headers 
    'secondary': "#7a0911",   # Section titles 
    'accent': "#f8b237"       # Accent for borders/emphasis 
}

# A helper style for table borders
border_style = {
    "border": "1px solid #000",
    "padding": "5px"
}

editable_disabled_style = {
        "background-color": "white",
        "color": "black",
        "opacity": "1",
    }

summary = dbc.Container(
    [
        # Basic Information Section (Name, Peer Reviewers, etc.)
        dbc.Row(
            dbc.Col(
                html.Table(
                    children=[
                        html.Colgroup([
                            html.Col(style={"width": "20%"}),   # First column: smallest width
                            html.Col(style={"width": "35%"}), # Second column
                            html.Col(style={"width": "45%"})  # Third column, same as second
                        ]),
                        html.Tbody([
                            # Row 1
                            html.Tr([
                                html.Td("Name", style=border_style),
                                html.Td(
                                    dbc.Input(id="name_input", type="text", placeholder="Enter name", disabled=True, style=editable_disabled_style),
                                    style=border_style
                                ),
                                html.Td("Peer Reviewers", style={**border_style, "text-align": "center"}),
                            ]),
                            # Row 2
                            html.Tr([
                                html.Td("For the period", style=border_style),
                                html.Td(
                                    dbc.Input(id="period_input", type="text", placeholder="e.g. Jan 2025 - Mar 2025", disabled=True, style=editable_disabled_style),
                                    style=border_style
                                ),
                                html.Td(
                                    dbc.Textarea(id="reviewers", placeholder="List of Reviewers", disabled=True, style={**editable_disabled_style, "fontWeight": "bold"}),
                                    rowSpan=2,
                                    style=border_style
                                ),
                            ]),
                            # Row 3
                            html.Tr([
                                html.Td("Dates Conducted", style=border_style),
                                html.Td(
                                    dbc.Input(id="dates_conducted_input", type="text", placeholder="e.g. March 1, 2025", disabled=True, style=editable_disabled_style),
                                    style=border_style
                                ),
                            ]),
                        ])
                    ],
                    style={"width": "100%", "border-collapse": "collapse"}
                ),
                width=12
            ),
            id="basic_info_row",
            style={"margin-bottom": "20px"}
        ),

        # Evaluation Table
        dbc.Row(
            dbc.Col(
                html.Table(
                    children=[
                        # Table Header
                        html.Thead([
                            # First header row
                            html.Tr([
                                html.Th("Evaluation Parameters", rowSpan=2, style={**border_style, "verticalAlign": "middle"}),
                                html.Th("Peer Scores", colSpan=4, style={**border_style, "text-align": "center"}),
                                html.Th("Weighted Average", rowSpan=2, style={**border_style, "verticalAlign": "middle"}),
                            ]),
                            # Second header row (should align under "Peer Scores")
                            html.Tr([
                                html.Th("Beginning (1)", style={**border_style, "text-align": "center"}),
                                html.Th("Progressing (2)", style={**border_style, "text-align": "center"}),
                                html.Th("Competent (3)", style={**border_style, "text-align": "center"}),
                                html.Th("Advanced (4)", style={**border_style, "text-align": "center"}),
                            ])
                        ]),
                        # Table Body (Parameters)
                        html.Tbody([
                            html.Tr([
                                html.Td("Contributions", style=border_style),
                                html.Td(dbc.Input(id="contributions_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="contributions_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="contributions_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="contributions_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="contributions_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Cooperation with Others", style=border_style),
                                html.Td(dbc.Input(id="cooperation_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="cooperation_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="cooperation_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="cooperation_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="cooperation_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Focus and Commitments", style=border_style),
                                html.Td(dbc.Input(id="focus_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="focus_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="focus_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="focus_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="focus_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Team Role Fulfillment", style=border_style),
                                html.Td(dbc.Input(id="teamrole_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="teamrole_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="teamrole_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="teamrole_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="teamrole_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Ability to Communicate", style=border_style),
                                html.Td(dbc.Input(id="communicate_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="communicate_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="communicate_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="communicate_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="communicate_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Completion of Assigned Task", style=border_style),
                                html.Td(dbc.Input(id="completion_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="completion_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="completion_competent", type="number",disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="completion_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="completion_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            # Overall Weighted Average Row
                            html.Tr([
                                html.Td("Overall Weighted Average", colSpan=5, style={**border_style, "font-weight": "bold", "text-align": "right"}),
                                html.Td(dbc.Input(id="overall_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                        ]),
                    ],
                    style={"width": "100%", "border-collapse": "collapse"},
                    id="evaluation_table"
                ),
                width=12
            ),
            id="evaluation_table_row",
            style={"margin-bottom": "20px"}
        ),

        # Opportunities for Improvement
        dbc.Row(
            dbc.Col(
                [
                    html.Div("Opportunities for Improvement", 
                             style={"font-weight": "bold", "margin-bottom": "5px", "color": highlight_colors['secondary']}),
                    dbc.Textarea(
                        id="opportunities_text",
                        placeholder="Enter opportunities for improvement here...",
                        style={**editable_disabled_style, "width": "100%", "height": "100px"},
                    )
                ],
                width=12
            ),
            id="improvement_row",
            style={"margin-bottom": "20px"}
        ),

        # Sign-off Section (Conducted by, Date, Received by, Date)
        dbc.Row(
            dbc.Col(
                html.Table(
                    children=[
                        html.Tbody([
                            html.Tr([
                                html.Td([
                                    html.Div("Conducted by:", style={"margin-bottom": "5px"}),
                                    dbc.Select(id="conducted_by", placeholder="Name", disabled=False, style=editable_disabled_style),
                                ], style=border_style),
                                html.Td([
                                    html.Div("Date:", style={"margin-bottom": "5px"}),
                                    dcc.DatePickerSingle(id="conducted_date", className='SingleDatePicker', date=str(pd.to_datetime("today").date()),
                                                          placeholder="mm/dd/yyyy", disabled=False, style=editable_disabled_style),
                                ], style=border_style),
                                html.Td([
                                    html.Div("Received by:", style={"margin-bottom": "5px"}),
                                    dbc.Select(id="received_by", placeholder="Name", disabled=False, style=editable_disabled_style),
                                ], style=border_style),
                                html.Td([
                                    html.Div("Date:", style={"margin-bottom": "5px"}),
                                    dcc.DatePickerSingle(id="received_date", className='SingleDatePicker', placeholder="mm/dd/yyyy", disabled=False, style=editable_disabled_style),
                                ], style=border_style),
                            ])
                        ])
                    ],
                    style={"width": "100%", "border-collapse": "collapse"}
                ),
                width=12
            ),
            id="sign_off_row",
            style={"margin-bottom": "20px"}
        ),

    ],
    fluid=True,
    style={"background-color": "#f4f4f4", "padding": "20px"}
)

remarks_section = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Table(
                    children=[
                        # Optional: You can tweak column widths as needed
                        html.Colgroup([
                            html.Col(style={"width": "20%"}),
                            html.Col(style={"width": "80%"}),
                        ]),
                        html.Tbody([
                            # Heading row for Anecdotes/Remarks/Opportunities
                            html.Tr([
                                html.Td(
                                    "Anecdotes / Remarks / Opportunities", 
                                    colSpan=2,
                                    style={
                                        **border_style, 
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "background-color": highlight_colors['accent']
                                    }
                                )
                            ]),
                            # Row for “Contribution”
                            html.Tr([
                                html.Td("Contribution", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="remarks_contribution", 
                                        placeholder="No feedback received for Contribution...", 
                                        disabled=True,  # Set to False if you want it editable
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Cooperation with Others”
                            html.Tr([
                                html.Td("Cooperation with Others", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="remarks_cooperation", 
                                        placeholder="No feedback received for Cooperation with Others...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Focus and Commitments”
                            html.Tr([
                                html.Td("Focus and Commitments", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="remarks_focus", 
                                        placeholder="No feedback received for Focus and Commitments...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Team Role Fulfillment”
                            html.Tr([
                                html.Td("Team Role Fulfillment", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="remarks_team_role", 
                                        placeholder="No feedback received for Team Role Fulfillment...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Ability to Communicate”
                            html.Tr([
                                html.Td("Ability to Communicate", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="remarks_communicate", 
                                        placeholder="No feedback received for Ability to Communicate...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Completion of Tasks”
                            html.Tr([
                                html.Td("Completion of Tasks", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="remarks_completion", 
                                        placeholder="No feedback received for Completion of Tasks...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                        ])
                    ],
                    style={"width": "100%", "border-collapse": "collapse"}
                ),
                width=12
            ),
            style={"margin-bottom": "20px"}
        ),
    ],
    fluid=True,
    style={"background-color": "#f4f4f4", "padding": "20px"}
)


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.Div(  
                            [
                                dcc.Store(id='response_to_load', storage_type='memory', data=0),
                                dcc.Download(id="pdf-download")
                            ]
                        ),
                        html.Div(
                            # Top Header (Organization/Office Title)
                            dbc.Row(
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H3("University of the Philippines", 
                                                    style={"margin-bottom": "0px", "text-align": "center", "color": highlight_colors['secondary'], "font-weight": "bold", "font-size": "2.5rem"}),
                                            html.H4("Quality Assurance Office Diliman", 
                                                    style={"margin-top": "0px", "text-align": "center", "color": highlight_colors['primary'], "font-size": "1.5rem"}),
                                            html.H5("PEER EVALUATION SUMMARY REPORT", 
                                                    style={
                                                        "text-align": "center", 
                                                        "margin-top": "30px",
                                                        "font-weight": "bold",
                                                        "font-size": "1.5rem",
                                                        "color": highlight_colors['accent']
                                                    }
                                            ),
                                        ],
                                        style={"margin-bottom": "0px"}  # reduce bottom margin of the header container
                                    ),
                                    width=12,
                                ),
                            ),
                            style={"margin-bottom": "0px"}  # reduce spacing after the header
                        ),
                        html.Hr(
                            style={
                                "margin-top": "0px",  # remove top margin from HR
                            }
                        ),
                        summary, 
                        html.Br(),
                        remarks_section,
                        html.Br(),
                        dbc.Alert(id='response_summary_alert', is_open=False), # For feedback purpose
                        html.Div(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "Download PDF",
                                        id="download_pdf_btn",
                                        n_clicks=0,
                                        color="secondary",
                                        style={"margin-left": "10px"}
                                    )
                                )
                            ],
                            id="download_style_div"
                        ),
                        html.Div(
                            dbc.Row(
                                [ 
                                    
                                    dbc.Col(
                                        dbc.Button("Save", color="primary",  id="summary_save_button", n_clicks=0),
                                        width="auto"
                                    ),
                                    dbc.Col(
                                        dbc.Button("Cancel", color="warning", id="summary_cancel_button", n_clicks=0, href="/peer_evaluation_responses"),  
                                        width="auto"
                                    ),
                                ],
                                className="mb-2",
                                justify="end",
                            ),
                            id="summary_buttons_div"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Back",
                                                id="back_button",
                                                color="primary",
                                                className="me-2",
                                                href="/peer_evaluation_responses",
                                                style={
                                                    "display": "flex",          # make the button a flex container
                                                    "justifyContent": "center",# center horizontally
                                                    "alignItems": "center",    # center vertically
                                                    "fontWeight": "bold",      # bold text
                                                    "fontSize": "12px"         # at least 12px font size
                                                }
                                            ),
                                        ],
                                        style={
                                            "display": "flex",
                                            "justifyContent": "flex-end"   # keeps the button aligned to the right of its parent
                                        }
                                    ),
                                ),
                            ],
                            justify="end",
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(
                                    html.H5("Are you sure you want to save the changes?"),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id= "summary_initial_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id= "summary_initial_modal_confirm", color="success")
                                    ]
                                ),
                            ],
                            centered=True,
                            id="summary_initial_modal",
                            backdrop=True,
                            className="modal-success",
                        ),

                        # Final Modal for Training Documents
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Changes has been saved"), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(
                                    html.H5("Click Proceed to continue"),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Proceed", href='/peer_evaluation_responses', color="success"),
                                    ]
                                ),
                            ],
                            centered=True,
                            id="summary_last_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                    ],
                    width=9,
                    style={"marginLeft": "15px"},
                )
            ]
        ),
        html.Br(),
        html.Br(),
        # Example Control Buttons (Optional)
        html.Br(),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ), 
    ]
)

@app.callback(
    [   
        Output('conducted_by', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('currentuserid', 'data')
    ]
)

def load_conducted_by(pathname, current_user):
    if pathname == '/peer_evaluation_responses/evaluation_summary':
        sql = """
            SELECT
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) as label,
            u.user_id as value
            FROM maindashboard.users u
            WHERE u.user_id = %s
        """
        values = [current_user]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        conducted_by_options = df.to_dict('records')

    else:
        raise PreventUpdate
    
    return [conducted_by_options]

@app.callback(
    [   
        Output('received_by', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)

def load_conducted_by(pathname, search):
    if pathname == '/peer_evaluation_responses/evaluation_summary':
        parsed = urlparse(search)
        evaluatee_id = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) as label,
            u.user_id as value
            FROM maindashboard.users u
            WHERE u.user_id = %s
        """
        values = [evaluatee_id]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        received_by_options = df.to_dict('records')

    else:
        raise PreventUpdate
    return [received_by_options]


@app.callback(
    [   
        Output('response_to_load', 'data'),
        Output('summary_buttons_div', 'style'),
        Output('back_button', 'style'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search'),
    ]
)
def peereval_get_userid(pathname, search):
    if pathname == '/peer_evaluation_responses/evaluation_summary':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        if create_mode == 'edit':
            to_load = 1
            button_style = {'display': 'flex', 'justifyContent': 'flex-end'}
            back_btn_div_style = {'display': 'none'}
        elif create_mode == 'view':
            to_load = 1
            button_style = {'display': 'none'}
            back_btn_div_style = {'display': 'flex', 'justifyContent': 'flex-end'}
        else:
            to_load = 0
            button_style = {'display': 'flex', 'justifyContent': 'flex-end'}
            back_btn_div_style = {'display': 'none'}
    else:  
        raise PreventUpdate
    
    return [to_load, button_style, back_btn_div_style]

# evaluatee_id = parse_qs(parsed.query).get('id', [None])[0]

@app.callback(
    [
        Output('name_input', 'value'),
        Output('contributions_beginning', 'value'),
        Output('contributions_progressing', 'value'),
        Output('contributions_competent', 'value'),
        Output('contributions_advanced', 'value'),
        Output('contributions_weighted_average', 'value'),
        Output('cooperation_beginning', 'value'),
        Output('cooperation_progressing', 'value'),
        Output('cooperation_competent', 'value'),
        Output('cooperation_advanced', 'value'),
        Output('cooperation_weighted_average', 'value'),
        Output('focus_beginning', 'value'),
        Output('focus_progressing', 'value'),
        Output('focus_competent', 'value'),
        Output('focus_advanced', 'value'),
        Output('focus_weighted_average', 'value'),
        Output('teamrole_beginning', 'value'),
        Output('teamrole_progressing', 'value'),
        Output('teamrole_competent', 'value'),
        Output('teamrole_advanced', 'value'),
        Output('teamrole_weighted_average', 'value'),
        Output('communicate_beginning', 'value'),
        Output('communicate_progressing', 'value'),
        Output('communicate_competent', 'value'),
        Output('communicate_advanced', 'value'),
        Output('communicate_weighted_average', 'value'),
        Output('completion_beginning', 'value'),
        Output('completion_progressing', 'value'),
        Output('completion_competent', 'value'),
        Output('completion_advanced', 'value'),
        Output('completion_weighted_average', 'value'),
        Output('overall_weighted_average', 'value')
    ],
    [
        Input('response_to_load', 'modified_timestamp')
    ],
    [
        State('response_to_load', 'data'),
        State('url', 'search'),
    ]
)
def peereval_load(timestamp, to_load, search):
    if not to_load:
        raise PreventUpdate
    if to_load:
        parsed = urlparse(search)
        evaluatee_id = parse_qs(parsed.query)['id'][0]

    # Run one query for all rubric_ids (1 to 6)
    sql = """
        SELECT 
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS full_name,
            ed.rubric_id,
            ed.rating_value, 
            COUNT(*) AS rating_count
        FROM maindashboard.users u
        LEFT JOIN director.peer_evaluations pe ON u.user_id = pe.evaluatee_id
        LEFT JOIN director.evaluation_details ed ON pe.evaluation_id = ed.evaluation_id
        WHERE pe.evaluatee_id = %s
          AND pe.peer_eval_delete_ind = FALSE
          AND evaluation_period_id = (
            SELECT period_id   AS value
                FROM director.evaluation_periods
                WHERE active_status = TRUE
                AND period_del_ind = FALSE
            )
        GROUP BY full_name, ed.rubric_id, ed.rating_value;
    """
    values = [evaluatee_id]
    cols = ['full_name', 'rubric_id', 'rating_value', 'rating_count']
    df = db.querydatafromdatabase(sql, values, cols)
    
    # If no evaluation data, set default values.
    if df.empty:
        full_name = ""
        # For each rubric (1 to 6): 4 counts and a weighted average, all set to 0.
        result = {rubric: {1: 0, 2: 0, 3: 0, 4: 0, 'weighted': 0} for rubric in range(1, 7)}
    else:
        full_name = df['full_name'].iloc[0]
        # Initialize for all expected rubrics (1 to 6)
        result = {rubric: {1: 0, 2: 0, 3: 0, 4: 0, 'weighted': 0} for rubric in range(1, 7)}
        
        # Populate the result dictionary with counts from the query
        for _, row in df.iterrows():
            rubric = row['rubric_id']
            rating = row['rating_value']
            count = row['rating_count']
            result[rubric][rating] = count

        # Calculate weighted average for each rubric and round to 2 decimals.
        for rubric in range(1, 7):
            counts = result[rubric]
            total = counts[1] + counts[2] + counts[3] + counts[4]
            if total > 0:
                weighted = (1 * counts[1] + 2 * counts[2] + 3 * counts[3] + 4 * counts[4]) / total
            else:
                weighted = 0
            result[rubric]['weighted'] = round(weighted, 2)

    # Map rubric ids to your UI components.
    # Rubric 1: Contributions
    contributions_beginning    = result[1][1]
    contributions_progressing  = result[1][2]
    contributions_competent    = result[1][3]
    contributions_advanced     = result[1][4]
    contributions_weighted     = result[1]['weighted']

    # Rubric 2: Cooperation with Others
    cooperation_beginning      = result[2][1]
    cooperation_progressing    = result[2][2]
    cooperation_competent      = result[2][3]
    cooperation_advanced       = result[2][4]
    cooperation_weighted       = result[2]['weighted']

    # Rubric 3: Focus and Commitments
    focus_beginning            = result[3][1]
    focus_progressing          = result[3][2]
    focus_competent            = result[3][3]
    focus_advanced             = result[3][4]
    focus_weighted             = result[3]['weighted']

    # Rubric 4: Team Role Fulfillment
    teamrole_beginning         = result[4][1]
    teamrole_progressing       = result[4][2]
    teamrole_competent         = result[4][3]
    teamrole_advanced          = result[4][4]
    teamrole_weighted          = result[4]['weighted']

    # Rubric 5: Ability to Communicate
    communicate_beginning      = result[5][1]
    communicate_progressing    = result[5][2]
    communicate_competent      = result[5][3]
    communicate_advanced       = result[5][4]
    communicate_weighted       = result[5]['weighted']

    # Rubric 6: Completion of Assigned Task
    completion_beginning       = result[6][1]
    completion_progressing     = result[6][2]
    completion_competent       = result[6][3]
    completion_advanced        = result[6][4]
    completion_weighted        = result[6]['weighted']

    # Calculate overall weighted average as the average of the six rubric weighted averages.
    overall_weighted = round(
        (contributions_weighted + cooperation_weighted + focus_weighted +
         teamrole_weighted + communicate_weighted + completion_weighted) / 6, 2
    )

    return [
        full_name,
        contributions_beginning,
        contributions_progressing,
        contributions_competent,
        contributions_advanced,
        contributions_weighted,
        cooperation_beginning,
        cooperation_progressing,
        cooperation_competent,
        cooperation_advanced,
        cooperation_weighted,
        focus_beginning,
        focus_progressing,
        focus_competent,
        focus_advanced,
        focus_weighted,
        teamrole_beginning,
        teamrole_progressing,
        teamrole_competent,
        teamrole_advanced,
        teamrole_weighted,
        communicate_beginning,
        communicate_progressing,
        communicate_competent,
        communicate_advanced,
        communicate_weighted,
        completion_beginning,
        completion_progressing,
        completion_competent,
        completion_advanced,
        completion_weighted,
        overall_weighted
    ]


@app.callback(
    [
        Output('period_input', 'value'),
        Output('dates_conducted_input', 'value'),
        Output('reviewers', 'value'),
        Output('reviewers', 'style')
    ],
    [
        Input('response_to_load', 'modified_timestamp')
    ],
    [
        State('response_to_load', 'data'),
        State('url', 'search'),
    ]
)
def update_reviewers(timestamp, to_load, search):

    default_style = {
        "background-color": "white",
        "color": "black",
        "opacity": "1",
    }

    if not to_load:
        raise PreventUpdate

    if to_load:
        parsed = urlparse(search)
        evaluatee_id = parse_qs(parsed.query)['id'][0]

        # SQL query to get the distinct full names of evaluators who have evaluated the chosen evaluatee.
        sql = """
            SELECT DISTINCT 
                CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS full_name,
                to_char(lower(period_details), 'Mon DD, YYYY') ||
                ' to ' ||
                to_char(upper(period_details) - INTERVAL '1 day', 'Mon DD, YYYY')
                AS evaluation_period
            FROM director.peer_evaluations pe
            JOIN maindashboard.users u ON pe.evaluator_id = u.user_id
            JOIN director.evaluation_periods ep on ep.period_id = pe.evaluation_period_id 
            WHERE pe.evaluatee_id = %s
            AND pe.peer_eval_delete_ind = FALSE
            AND evaluation_period_id = (
                SELECT period_id   AS value
                    FROM director.evaluation_periods
                    WHERE active_status = TRUE
                    AND period_del_ind = FALSE
            );
        """
        values = [evaluatee_id]
        cols = ['full_name', 'evaluation_period']
        df = db.querydatafromdatabase(sql, values, cols)

        # If no evaluators are found, return an empty string.
        if df.empty:
            evaluation_period = ""
            dates_conducted = ""
            reviewers_text= "No peer review evaluations found."
            reviewers_style = {
                "background-color": "white",
                "color": "black",
                "opacity": "1",
                "fontWeight": "bold"
            }

        if not df.empty:
            evaluation_period = df['evaluation_period'][0]
            dates_conducted = df['evaluation_period'][0]
            # Combine the distinct evaluator names into a single string, separated by commas.
            evaluator_names = df['full_name'].unique().tolist()
            reviewers_text = ", ".join(evaluator_names)   
            reviewers_style = default_style

    
    return [evaluation_period, dates_conducted, reviewers_text, reviewers_style]

@app.callback(
    [
        Output('remarks_contribution',   'value'),
        Output('remarks_cooperation',    'value'),
        Output('remarks_focus',          'value'),
        Output('remarks_team_role',      'value'),
        Output('remarks_communicate',    'value'),
        Output('remarks_completion',     'value'),
    ],
    [
        Input('response_to_load', 'modified_timestamp')
    ],
    [
        State('response_to_load', 'data'),
        State('url', 'search')
    ]
)
def update_remarks(timestamp, to_load, search):
    # only run after the store is set
    if not to_load:
        raise PreventUpdate
    if to_load:
        # extract evaluatee_id from URL
        parsed = urlparse(search)
        qs = parse_qs(parsed.query)
        evaluatee_id = qs.get('id', [None])[0]
        if evaluatee_id is None:
            raise PreventUpdate

        # grab all feedback + evaluator names for this evaluatee
        sql = """
            SELECT
                ed.rubric_id,
                ed.feedback,
                CONCAT(u.user_fname, ' ', LEFT(u.user_mname,1), '. ', u.user_sname, ' ', u.user_suffixname)
                AS evaluator_name
            FROM director.peer_evaluations pe
            JOIN director.evaluation_details ed
            ON pe.evaluation_id = ed.evaluation_id
            JOIN maindashboard.users u
            ON pe.evaluator_id = u.user_id
            WHERE pe.evaluatee_id = %s
            AND evaluation_period_id = (
                SELECT period_id   AS value
                    FROM director.evaluation_periods
                    WHERE active_status = TRUE
                    AND period_del_ind = FALSE
            )
            AND pe.peer_eval_delete_ind = FALSE
            AND ed.feedback IS NOT NULL
            ORDER BY ed.rubric_id, pe.evaluation_date;
        """
        df = db.querydatafromdatabase(sql, [evaluatee_id], ['rubric_id', 'feedback', 'evaluator_name'])

        # initialize empty lists for each rubric
        remarks_by_rubric = {i: [] for i in range(1,7)}

        # accumulate formatted entries
        for _, row in df.iterrows():
            r = row['rubric_id']
            text = row['feedback'].strip()
            name = row['evaluator_name'].strip()
            remarks_by_rubric[r].append(f"{text} — {name}")

        # join entries with single line breaks, default to empty string
        return [
            "\n\n".join(remarks_by_rubric[1]),
            "\n\n".join(remarks_by_rubric[2]),
            "\n\n".join(remarks_by_rubric[3]),
            "\n\n".join(remarks_by_rubric[4]),
            "\n\n".join(remarks_by_rubric[5]),
            "\n\n".join(remarks_by_rubric[6]),
        ]


@app.callback(
    [
        # Check if all fields are filled
        Output('response_summary_alert', 'is_open'),
        Output('response_summary_alert', 'color'),
        Output('response_summary_alert', 'children'),
        Output('summary_initial_modal', 'is_open'),
        Output('summary_last_modal', 'is_open'),
        Output('opportunities_text', 'className'),
        Output('conducted_by', 'className'),
        Output('received_by', 'className'),
    ],
    [
        Input('summary_save_button', 'n_clicks'),
        Input('summary_initial_modal_cancel', 'n_clicks'),
        Input('summary_initial_modal_confirm', 'n_clicks'),
    ],
    [
        State('url', 'search'),
        State('opportunities_text', 'value'),
        State('conducted_by', 'value'),
        State('conducted_date', 'date'),
        State('received_by', 'value'),
        State('received_date', 'date'),
    ]
)

def save_opportunity_summary(save_button, cancel_button, confirm_button, search, opportunities_text, conducted_by, conducted_date, received_by, received_date):

    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]
    evaluatee_user_id = parse_qs(parsed.query).get('id', [None])[0]

    opportunities_text_class = ''
    conducted_by_class = ''
    received_by_class = ''

    primary_sql = """
        SELECT COUNT(*)
        FROM director.evaluation_summaries
        WHERE summary_evaluatee_id = %s
        AND summary_evaluation_period = (
            SELECT period_id
            FROM director.evaluation_periods
            WHERE active_status = TRUE
            AND period_del_ind = FALSE
        )
    """
    primary_values = [evaluatee_user_id]

    cols = ['count']
    df = db.querydatafromdatabase(primary_sql, primary_values, cols)
    checker = int(df['count'][0])

    # Set default outputs
    alert_open = False
    alert_color = ''
    alert_text = ''
    initial_modal_open = False
    last_modal_open = False

    if eventid == 'summary_save_button' and save_button:
        # Check if all fields are filled
        if not all([opportunities_text, conducted_by, received_by]):
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Please fill in at the "Opportunities for Improvement", "Conducted by:", and "Received by:" sections.'
            opportunities_text_class = 'red-border' if not opportunities_text else ''
            conducted_by_class = 'red-border' if not conducted_by else 'form-control'
            received_by_class = 'red-border' if not received_by else 'form-control'
        else:
            if create_mode == 'edit':
                initial_modal_open = True

    elif eventid == 'summary_initial_modal_confirm' and confirm_button and checker < 1:
        sql = """
            INSERT INTO director.evaluation_summaries (
                summary_evaluatee_id, summary_text, summary_conducted_by, summary_conducted_date, summary_received_by, summary_received_date, summary_evaluation_period
            )
                    
            VALUES (%s, %s, %s, %s, %s, %s,
                (SELECT period_id
                    FROM director.evaluation_periods
                    WHERE active_status = TRUE
                    AND period_del_ind  = FALSE
                )
        )
        """

        values = [evaluatee_user_id, opportunities_text, conducted_by, conducted_date, received_by, received_date]

        db.modifydatabase(sql, values)

        initial_modal_open = False
        last_modal_open = True

    elif eventid == 'summary_initial_modal_confirm' and confirm_button and checker >= 1:
        sql = """
            UPDATE director.evaluation_summaries
            SET summary_text = %s,
                summary_conducted_by = %s,
                summary_conducted_date = %s,
                summary_received_by = %s,
                summary_received_date = %s
            WHERE summary_evaluatee_id = %s
            AND summary_evaluation_period = (
                SELECT period_id
                FROM director.evaluation_periods
                WHERE active_status = TRUE
                AND period_del_ind  = FALSE
            )
        """

        values = [opportunities_text, conducted_by, conducted_date, received_by, received_date, evaluatee_user_id]

        db.modifydatabase(sql, values)

        initial_modal_open = False
        last_modal_open = True

    elif eventid == 'summary_initial_modal_cancel' and cancel_button:
        initial_modal_open = False

    else:
        raise PreventUpdate


    return [alert_open, alert_color, alert_text, initial_modal_open, last_modal_open, opportunities_text_class, conducted_by_class, received_by_class]


@app.callback(
    [
        Output('opportunities_text', 'value'),
        Output('conducted_by', 'value'),
        Output('conducted_date', 'date'),
        Output('received_by', 'value'),
        Output('received_date', 'date'),
    ],
    [
        Input('response_to_load', 'modified_timestamp')
    ],
    [
        State('response_to_load', 'data'),
        State('url', 'search'),
    ]
)

def load_summary(timestamp, to_load, search):
    if to_load:
        parsed = urlparse(search)
        evaluatee_id = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT summary_text, summary_conducted_by, summary_conducted_date, summary_received_by, summary_received_date
            FROM director.evaluation_summaries
            WHERE summary_evaluatee_id = %s
            AND summary_evaluation_period = (
                SELECT period_id
                FROM director.evaluation_periods
                WHERE active_status = TRUE
                AND period_del_ind  = FALSE
            )
        """
        values = [evaluatee_id]
        cols = ['summary_text', 'summary_conducted_by', 'summary_conducted_date', 'summary_received_by', 'summary_received_date']
        df = db.querydatafromdatabase(sql, values, cols)

        if df.empty:
            summary_text = ""
            conducted_by = ""
            conducted_date = dash.no_update
            received_by = ""
            received_date = None  
        else:
            summary_text =df['summary_text'][0]
            conducted_by = df['summary_conducted_by'][0]
            conducted_date = df['summary_conducted_date'][0]
            received_by = df['summary_received_by'][0]
            received_date = df['summary_received_date'][0]

    else:
        raise PreventUpdate
    
    return [summary_text, conducted_by, conducted_date, received_by, received_date]

@app.callback(
    [ 
        Output('conducted_by', 'disabled'),
        Output('conducted_date', 'disabled'),
        Output('received_by', 'disabled'),
        Output('received_date', 'disabled'),
    ],
    [
        Input('url', 'search')
    ]
)
def addexpense_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [False, False, False, False] 
        elif create_mode == 'view':
            return [True, True, True, True] 
        
    return [True, True, True, True]



@app.callback(
    Output("download_style_div", "style"),
    Input('url', 'pathname'),
    State('url', 'search'),
)
def evaluation_summary_downloadbutton(pathname, search):

    download_button_style = {'display': 'none'}

    if pathname == '/peer_evaluation_responses/evaluation_summary':
        parsed = urlparse(search)
        id_evaluatee = parse_qs(parsed.query)['id'][0]
        id_final = int(id_evaluatee)

        if not id_evaluatee:
            raise PreventUpdate
        
        sql = """
            SELECT COUNT(*) as count
        FROM director.evaluation_summaries
        WHERE summary_evaluatee_id = %s
        AND summary_evaluation_period = (
            SELECT period_id
            FROM director.evaluation_periods
            WHERE active_status = TRUE
            AND period_del_ind = FALSE
        )
        """
        values = [id_final]
        cols = ['count']
        df = db.querydatafromdatabase(sql, values, cols)
        sql_checker = int(df['count'][0])

        if sql_checker < 1:
            return {'display': 'none'}
        elif sql_checker > 0:
            return {'display': 'flex'}
        else:
            return download_button_style


@app.callback(
    Output("pdf-download", "data"),
    Input("download_pdf_btn", "n_clicks"),
    State("url", "search"),
    prevent_initial_call=True,
)

def serve_pdf(n_clicks, search):
    parsed = urlparse(search)
    eval_id = parse_qs(parsed.query)['id'][0]
    final_id = int(eval_id)

    if not eval_id:
        raise PreventUpdate
    sql = """
        SELECT
        CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) as "Full_Name"
        FROM maindashboard.users u
        WHERE u.user_id = %s
    """
    values = [final_id]
    cols = ['Full_Name']
    df = db.querydatafromdatabase(sql, values, cols)
    full_name =df['Full_Name'][0]

    pdf = pdf_utils.generate_pdf_bytes(final_id)
    return dcc.send_bytes(lambda buf: buf.write(pdf), filename=f"Peer_Evaluation_Report_{full_name}.pdf")

