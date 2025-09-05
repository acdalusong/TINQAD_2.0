import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, dash_table

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

from dash import ALL, no_update
from datetime import datetime, timedelta
import calendar


from dash import Output, Input, State, callback_context

def create_card(title, content=None):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(content if content else "")
        ],
        className="mb-3",  
    )

def create_table(headers, id):
    return dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in headers],
        style_header={'fontWeight': 'bold'}, 
    )

def get_month_range():
    today = datetime.today()
    # Get the first day of the current month
    start_of_month = datetime(today.year, today.month, 1)
    # Get the last day of the current month
    end_of_month = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    return start_of_month, end_of_month

# Announcements content card
announcements_content = html.Div(
    [
                html.Div(id="kmann_display",
                         style={
                             'overflowX': 'auto',
                             'overflowY': 'auto',
                             'maxHeight': '500px',
                         }),
                html.Br(),
                html.Div(
                    [
                        html.Div(id="kmann_status"),
                        html.Br(),
                        dbc.Input(
                            id="kmann_header",
                            placeholder="Format: Deadline Date, if urgent type URGENT. ex. May 05, 2024 URGENT.",
                            type="text",
                        ),
                        dbc.Textarea(
                            id="kmann_content",
                            placeholder="Type a message...",
                            style={"resize": "vertical"},
                            rows=5,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("Post", id="kmannpost_button", color="success",
                                               className="mt-2"),
                                    width="auto",
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", id="kmanncancel_button", color="warning",
                                               className="mt-2"),
                                    width="auto",
                                ),
                            ],
                            style={"justify-content": "flex-end"},
                        ),
                    ],
                    id="kmann_id",
                    style={"display": "none"},  # Initially hidden
                ),
            ]
        )

# Announcements footer card
announcements_footer = html.Div(
    [
        dbc.Button(
            "Add Announcement",
            id="kmann_footer_button",
            className="mt-2",
            color="success",
        ),
    ],
    className="d-flex justify-content-end",
)

app.layout = html.Div([announcements_content, announcements_footer, dcc.Location(id="url", refresh=False)])


# Callback to control visibility of the announcement input area
@app.callback(
    Output("kmann_id", "style"),
    [Input("kmann_footer_button", "n_clicks"), 
     Input("kmanncancel_button", "n_clicks")],
    [State("kmann_id", "style")],  
)
def toggle_announcement_form(footer_clicks, cancel_clicks, current_style):
    ctx = callback_context  

    footer_clicks = footer_clicks or 0
    cancel_clicks = cancel_clicks or 0

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "kmann_footer_button" and footer_clicks > 0:
        return {"display": "block"}

    elif trigger_id == "kmanncancel_button" and cancel_clicks > 0:
        return {"display": "none"}

    raise PreventUpdate


# Callback to insert a new message into the database
@app.callback(
    [
        Output("kmann_status", "children"),
        Output("new_kmannouncement_alert", "children"),
        Output("new_kmannouncement_alert", "is_open")
    ],
    [   
        Input("kmannpost_button", "n_clicks"),
        Input("new_kmannouncement_alert", "n_dismiss"),
    ],
    [
        State("kmann_header", "value"),  
        State("kmann_content", "value"),
        State("currentuserid", "data")
    ] 
)
def insert_announcement(n_clicks, n_dismiss, kmann_header, kmann_content, current_userid):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # Handle dismissing the alert
    if ctx.triggered[0]['prop_id'] == 'new_announcement_alert.n_dismiss':
        return ["", "", False]

    if not n_clicks or not kmann_header or not kmann_content:
        raise PreventUpdate

    try:
        # Fetch the user's full name
        user_sql = """
            SELECT user_fname, user_sname
            FROM maindashboard.users
            WHERE user_id = %s
        """
        user_df = db.querydatafromdatabase(user_sql, [current_userid], ["user_fname", "user_sname"])

        if user_df.empty:
            raise Exception("User not found")

        user_fullname = f"{user_df.iloc[0]['user_fname']} {user_df.iloc[0]['user_sname']}"

        # Insert the announcement with the user's full name
        sql = """
            INSERT INTO kmteam.announcements (kmann_header, kmann_content, kmann_user)
            VALUES (%s, %s, %s)   
        """

        values = (kmann_header, kmann_content, user_fullname)

        # Insert the announcement into the database
        db.modifydatabase(sql, values)
        
        alert_message = f"{user_fullname} has a new announcement!"
        return ["Announcement posted successfully!", alert_message, True]

    except Exception as e:
        return [f"Error: {str(e)}", "", False]
    

@app.callback(
    Output("kmann_display", "children"),
    [Input("url", "pathname")],
)
def fetch_announcements(pathname):
    if pathname != "/km_dashboard":
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
            return [html.Div("No announcements this month")]

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
replies_content = html.Div(
    [
        html.Div(id="replies_display",
            style={
                'overflowX': 'auto',
                'overflowY': 'auto',
                'maxHeight': '300px', 
            }
        ),
    ]
)

@app.callback(
    Output("replies_display", "children"),
    [Input("url", "pathname")],
)
def fetch_fromrepliess(pathname):
    if pathname != "/km_dashboard":
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
            return [html.Div("No messages from QA Officers this month")]

        formatted_replies = []
        for row in df.itertuples(index=False):
            header = getattr(row, "replies_header")
            content = getattr(row, "replies_content")
            user = getattr(row, "replies_user")
            timestamp = getattr(row, "replies_timestamp")

            formatted_replies.append(
                html.Div(
                    [
                        html.P(f"{header}: {content}"),  # The main replies content
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

        return formatted_replies

    except Exception as e:
        return [html.Div(f"Error retrieving replies: {str(e)}")]

 














circle_style = {
    "height": "20px",  # Adjust the diameter of the circle
    "width": "20px",
    "borderRadius": "50%",
    "display": "inline-block",
    "marginRight": "10px",
    "verticalAlign": "middle",
}


links = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        [
                            html.Div(style={**circle_style, "backgroundColor": "#39B54A"}),  # Green circle
                            html.Span("Sustainable Development Goals Impact Rankings",
                                style={"verticalAlign": "middle"}),

                        ],
                        href="/SDGimpact_rankings ",
                        style={"color": "black", "textDecoration": "none"}  # Optional style to remove underline and adjust color
                    ),
                    width="auto",
                    align="center",
                ),
            ],
            className="align-items-center mb-2",  
        ),
         
         
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        [
                            html.Div(style={**circle_style, "backgroundColor": "#6495ed"}),  # Blue circle
                            html.Span("QS University Rankings",
                                style={"verticalAlign": "middle"}),
                        ],
                        href="/QSworld_rankings",
                        style={"color": "black", "textDecoration": "none"}   
                    ),
                    width="auto",
                    align="center",
                ),
            ],
            className="align-items-center mb-2",  
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        [
                            html.Div(style={**circle_style, "backgroundColor": "#ffa500"}),  # Orange circle
                            html.Span("THE World University Rankings",
                                style={"verticalAlign": "middle"}),
                        ],
                        href="/THEworld_rankings",
                        style={"color": "black", "textDecoration": "none"}   
                    ),
                    width="auto",
                    align="center",
                ),
            ],
            className="align-items-center mb-2",  
        ), 
    ],
    style={"textAlign": "left"}   
)


layout = html.Div(
    [
        dcc.Store(id='stored-messages', storage_type='memory'),
        dcc.Store(id='message-store', data=[]),

        html.Div(id='post-trigger', style={'display': 'none'}),
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("KM TEAM DASHBOARD", className="my-3"),
                        dbc.Alert(
                                id="new_kmannouncement_alert", 
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
                                                dbc.CardHeader(html.H5("Messages from QA Officers")),
                                                dbc.CardBody(
                                                    [
                                                        replies_content
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Br(),
                                        
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3("Announcements to QA Officers")),
                                                dbc.CardBody(
                                                    [
                                                        announcements_content,
                                                        announcements_footer,
                                                    ]
                                                ),
                                            ]
                                        ),
                                        
                                    ],
                                    width=12,
                                    className="mb-3"
                                ),
                            ]
                        ),
                        html.Br(),
                    ],
                    width=7,
                ),
                dbc.Col(
                    [
                        html.H1("Hi", style={"color": "#FFFFFF"}, className="my-3"),
                        dbc.Row([
                            dbc.Col(
                                create_card(
                                    "Ranking Body Categories",
                                    links
                                ),
                                className="mb-3",
                                style={"backgroundColor": "#FFFFFF"},
                            ),
                            
                        ]),
                    ],
                    width=3, md=3, sm=12
                ),
            ],
            className="mb-3",
            style={'padding-bottom': '2rem'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)
