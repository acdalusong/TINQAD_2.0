import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback_context  

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db
 
from datetime import datetime 
import calendar 

def create_time_date_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(id="time", style={"font-size": "2em", "font-weight": "bold", "text-align": "center", "margin-bottom": "0"}),
                html.P(id="date", style={"text-align": "center", "margin-top": "0"}),
            ]
        ),
        className="mb-3",
        style={"backgroundColor": "#FFFFFF"}
    )

def get_month_range():
    today = datetime.today()
    # Get the first day of the current month
    start_of_month = datetime(today.year, today.month, 1)
    # Get the last day of the current month
    end_of_month = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    return start_of_month, end_of_month




# Announcements content card -------------------------------------------------------------------
basickmannounce_content = html.Div(
    [
        html.Div(id="basickmann_display",
            style={
                'overflowX': 'auto',
                'overflowY': 'auto',
                'maxHeight': '300px', 
            }
        ),
    ]
)

@app.callback(
    Output("basickmann_display", "children"),
    [Input("url", "pathname")],
)
def fetch_fromKMannouncements(pathname):
    if pathname != "/homepage":
        raise PreventUpdate

    try:
        start_of_month, end_of_month = get_month_range()

        sql = """
            SELECT kmann_header, kmann_content, kmann_user, kmann_timestamp
            FROM kmteam.announcements
            WHERE kmann_timestamp BETWEEN %s AND %s
            ORDER BY kmann_timestamp DESC
        """

        values = (start_of_month, end_of_month)
        dfcolumns = ["kmann_header", "kmann_content", "kmann_user", "kmann_timestamp"]

        df = db.querydatafromdatabase(sql, values, dfcolumns)

        if df.empty:
            return [html.Div("No KM announcements this month")]

        formatted_announcements = []
        for row in df.itertuples(index=False):
            header = getattr(row, "kmann_header")
            content = getattr(row, "kmann_content")
            user = getattr(row, "kmann_user")
            timestamp = getattr(row, "kmann_timestamp")

            formatted_announcements.append(
                html.Div(
                    [
                        html.P(f"{header}: {content}"),  # The main announcement content
                        html.Small(
                            f"{user or 'Anonymous'}, {timestamp}",
                            style={
                                "text-align": "right",
                                "font-style": "italic",
                            },
                        ),  
                        html.Hr(),
                    ],
                    style={"margin-bottom": "10px"},  
                )
            )

        return formatted_announcements

    except Exception as e:
        return [html.Div(f"Error retrieving announcements: {str(e)}")]

 
# Replies content card -------------------------------------------------------------------
basicreplies_content = html.Div(
    [
        html.Div(id="basicreplies_display",
            style={
                'overflowX': 'auto',
                'overflowY': 'auto',
                'maxHeight': '300px', 
            }),
        html.Br(),
        html.Div(
            [
            html.Div(id="basicreplies_status"),
            html.Br(),
            dbc.Input(
                id="basicreplies_header",
                placeholder="Format: [Office Name] Title.",
                type="text",
            ),
            dbc.Textarea(
                id="basicreplies_content",
                placeholder="Type a message...",
                style={"resize": "vertical"},
                rows=5,
            ),
            dbc.Row(
                [
                    dbc.Col(
                    dbc.Button("Post", id="basicrepliespost_button", color="success",
                        className="mt-2"),
                        width="auto",
                    ),
                    dbc.Col(
                        dbc.Button("Cancel", id="basicrepliescancel_button", color="warning",
                        className="mt-2"),
                        width="auto",
                        ),
                    ],
                    style={"justify-content": "flex-end"},
                ),
            ],
            id="basicreplies_id",
            style={"display": "none"},  # Initially hidden
        ),
    ]
)

# Replies footer card
basicreplies_footer = html.Div(
    [
        dbc.Button(
            "Add Announcement",
            id="basicreplies_footer_button",
            className="mt-2",
            color="success",
        ),
    ],
    className="d-flex justify-content-end",
)

app.layout = html.Div([basicreplies_content, basicreplies_footer, dcc.Location(id="url", refresh=False)])

 


# Callback to control visibility of the announcement input area
@app.callback(
    Output("basicreplies_id", "style"),
    [Input("basicreplies_footer_button", "n_clicks"), 
     Input("basicrepliescancel_button", "n_clicks")],
    [State("basicreplies_id", "style")],  
)
def toggle_announcement_form(footer_clicks, cancel_clicks, current_style):
    ctx = callback_context  

    footer_clicks = footer_clicks or 0
    cancel_clicks = cancel_clicks or 0

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "basicreplies_footer_button" and footer_clicks > 0:
        return {"display": "block"}

    elif trigger_id == "basicrepliescancel_button" and cancel_clicks > 0:
        return {"display": "none"}

    raise PreventUpdate
   

# Callback to insert a new message into the database
@app.callback(
    [
        Output("basicreplies_status", "children"),
        Output("basic_kmann_alert", "children"),
        Output("basic_kmann_alert", "is_open")
    ],
    [   
        Input("basicrepliespost_button", "n_clicks"),
        Input("basic_kmann_alert", "n_dismiss"),
    ],
    [
        State("basicreplies_header", "value"),  
        State("basicreplies_content", "value"),
        State("currentuserid", "data")
    ] 
)

def insert_announcement(n_clicks, n_dismiss, replies_header, replies_content, current_userid):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # Handle dismissing the alert
    if ctx.triggered[0]['prop_id'] == 'basic_kmann_alert.n_dismiss':
        return ["", "", False]

    if not n_clicks or not replies_header or not replies_content:
        raise PreventUpdate

    try:
        # Fetch the user's full name
        sql = """
            SELECT username
            FROM maindashboard.users
            WHERE user_id = %s
        """
        df = db.querydatafromdatabase(sql, [current_userid], ["username"])

        if df.empty:
            raise Exception("User not found")

        # Insert the announcement with the user's full name
        sql = """
            INSERT INTO kmteam.replies (replies_header, replies_content, replies_user)
            VALUES (%s, %s, %s)   
        """

        values = (replies_header, replies_content, df['username'].iloc[0])

        # Insert the announcement into the database
        db.modifydatabase(sql, values)
        
        alert_message = f"{df['username'].iloc[0]} has a new announcement!"
        return ["Announcement posted successfully!", alert_message, True]

    except Exception as e:
        return [f"Error: {str(e)}", "", False]



@app.callback(
    Output("basicreplies_display", "children"),
    [Input("url", "pathname")],
)
def fetch_basicreplies (pathname):
    if pathname != "/homepage":
        raise PreventUpdate

    try:
        start_of_month, end_of_month = get_month_range()

        sql = """
            SELECT replies_header, replies_content, replies_user, replies_timestamp
            FROM kmteam.replies
            WHERE replies_timestamp BETWEEN %s AND %s
            ORDER BY replies_timestamp DESC
        """

        values = (start_of_month, end_of_month)
        dfcolumns = ["replies_header", "replies_content", "replies_user", "replies_timestamp"]

        df = db.querydatafromdatabase(sql, values, dfcolumns)

        if df.empty:
            return [html.Div("No QA Officer messages yet this month")]

        formatted_announcements = []
        for row in df.itertuples(index=False):
            header = getattr(row, "replies_header")
            content = getattr(row, "replies_content")
            user = getattr(row, "replies_user")
            timestamp = getattr(row, "replies_timestamp")

            formatted_announcements.append(
                html.Div(
                    [
                        html.P(f"{header}: {content}"),  # The main announcement content
                        html.Small(
                            f"{user or 'Anonymous'}, {timestamp}",
                            style={
                                "text-align": "right",
                                "font-style": "italic",
                            },
                        ),  
                        html.Hr(),
                    ],
                    style={"margin-bottom": "10px"},  
                )
            )

        return formatted_announcements

    except Exception as e:
        return [html.Div(f"Error retrieving announcements: {str(e)}")]



layout = html.Div(
    [
        html.Div(  
                [
                dcc.Store(id='homeid_store', storage_type='session', data=0),
                ]
            ),
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1(html.B("👋 Welcome!")), 
                        html.Br(), 
                        dbc.Alert(
                                id="basic_kmann_alert", 
                                is_open=False, 
                                dismissable=True, 
                                duration=None, 
                                color="info"
                            ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3("KM Announcements")),
                                                dbc.CardBody(
                                                    [
                                                        basickmannounce_content
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3("QA Officers Messages")),
                                                dbc.CardBody(
                                                    [
                                                        basicreplies_content,
                                                        basicreplies_footer,
                                                    ]
                                                ),
                                            ]
                                        ),
                                        
                                    ],
                                    width=8,
                                    className="mb-3"
                                ),
                                
                                dbc.Col(
                                    [
                                        create_time_date_card(),
                                        dcc.Interval(
                                        id="interval-component",
                                        interval=1*1000,  # in milliseconds
                                        n_intervals=0
                                        ),

                                        dbc.Col(
                                            html.A(
                                            dbc.Card(
                                                dbc.CardBody(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.Div(style={'background-color': '#D37157', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                        html.H5("Add New Training Document", 
                                                                                className="card-title fw-bold text-dark", 
                                                                                style={"text-align": "right",'text-decoration': 'none'})
                                                                    ]
                                                                )
                                                            ],
                                                            align="center"
                                                        ),
                                                    ]
                                                ),
                                                className="mb-3",
                                                style={"backgroundColor": "#FFFFFF"}
                                            ),
                                            href='/training_instructions'
                                            ),
                                            width="auto"
                                        ),
                                        dbc.Col(
                                            html.A(
                                            dbc.Card(
                                                dbc.CardBody(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.Div(style={'background-color': '#39B54A', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                        html.H5("Add New Evidence for KM",
                                                                                className="card-title fw-bold text-dark", 
                                                                                style={"text-align": "right",'text-decoration': 'none'})
                                                                    ]
                                                                )
                                                            ],
                                                            align="center"
                                                        ),
                                                    ]
                                                ),
                                                className="mb-3",
                                                style={"backgroundColor": "#FFFFFF"}
                                            ),
                                            href='/SDGimpactrankings/SDG_submission?mode=add'
                                            ),
                                            width="auto"
                                        ),
                                    ], width=4,
                                ),

                                
  
                            ],
                            className="mb-3",
                            style={"backgroundColor": "#FFFFFF"},
                        ),
                         
                    ], width=9
                )
            ]
        ),
        
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)

 