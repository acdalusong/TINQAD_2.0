import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.dependencies import MATCH
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

from dash import ALL, no_update
from datetime import datetime, timedelta
import calendar
import pytz

from dash import Output, Input, State, callback_context




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



#----------------------------------- Team Messages Content
team_messages_content = html.Div(
    [
        html.Div(id="teammsgs_display",
                 style={
                    'overflowX': 'auto', 
                    'overflowY': 'auto',   
                    'maxHeight': '400px',
                    }),  
        html.Br(),
        html.Div(
            [
                html.Div(id="teammsgs_status"),  
                dbc.Textarea(
                    id="teammsgs_content",
                    placeholder="Type a message...",
                    style={"resize": "vertical"},
                    rows=5,
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button("Post", id="teammsgspost_button", color="success", className="mt-2"),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Button("Cancel", id="teammsgscancel_button", color="warning", className="mt-2"),
                            width="auto",
                        ),
                    ],
                    style={"justify-content": "flex-end"},
                ),
            ],
            id="teammsgs_id",
            style={"display": "none"},  # Initially hidden
        ),
    ]
)

team_messages_footer = html.Div(
    [
        dbc.Button(
            "Add Message",
            id="teammsgs_footer_button",
            className="mt-2",
            color="success",
        ),
    ],
    className="d-flex justify-content-end",
)
app.layout = html.Div([team_messages_content, team_messages_footer, dcc.Location(id="url", refresh=False)])




# Callback to control visibility of the message input area
@app.callback(
    Output("teammsgs_id", "style"),
    [Input("teammsgs_footer_button", "n_clicks"), 
     Input("teammsgscancel_button", "n_clicks")],   
    [State("teammsgs_id", "style")],   
)
def toggle_message_input_area(add_clicks, cancel_clicks, current_style):
    ctx = callback_context

    add_clicks = add_clicks or 0   
    cancel_clicks = cancel_clicks or 0  
 
    if not ctx.triggered:
        raise PreventUpdate
 
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
 
    if trigger_id == "teammsgs_footer_button" and add_clicks > 0:
        return {"display": "block"}   
 
    elif trigger_id == "teammsgscancel_button" and cancel_clicks > 0:
        return {"display": "none"}   
 
    raise PreventUpdate












# Callback to insert a new message into the database
@app.callback(
    Output("teammsgs_status", "children"),   
    [Input("teammsgspost_button", "n_clicks")],
    [State("teammsgs_content", "value"),
     State("currentuserid", "data")]  # Add current user ID state
)
def insert_team_message(n_clicks, message_content, current_userid):
    if not n_clicks or not message_content:
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

        # Insert the message with the user's full name
        sql = """
            INSERT INTO maindashboard.teammessages (teammsgs_content, teammsgs_user)
            VALUES (%s, %s)
        """
        
        values = (message_content, user_fullname)

        # Insert the message into the database
        db.modifydatabase(sql, values)
        
        return ["Message posted successfully!"]

    except Exception as e:
        return [f"Error: {str(e)}"]
 


# Callback to fetch team messages and display them
@app.callback(
    Output("teammsgs_display", "children"),
    [Input("url", "pathname")],   
)
def fetch_team_messages(pathname):
    if pathname != "/homepage":
        raise PreventUpdate

    try:
        start_of_month, end_of_month = get_month_range()
        
        sql = """
            SELECT teammsgs_content, teammsgs_user, teammsgs_timestamp
            FROM maindashboard.teammessages
            WHERE teammsgs_timestamp BETWEEN %s AND %s
            ORDER BY teammsgs_timestamp DESC
        """
         
        values = (start_of_month, end_of_month)
        dfcolumns = ["teammsgs_content", "teammsgs_user", "teammsgs_timestamp"]

        df = db.querydatafromdatabase(sql, values, dfcolumns)

        if df.empty:
            return [html.Div("No messages this month")]

        formatted_messages = [] 
        for row in df.itertuples(index=False): 
            content = getattr(row, "teammsgs_content")
            user = getattr(row, "teammsgs_user")
            timestamp = getattr(row, "teammsgs_timestamp")

            formatted_timestamp = datetime.strftime(timestamp, "%d %B %Y, %I:%M:%S %p")

            formatted_messages.append(
                html.Div(
                    [
                        html.P(content),  # The main message content
                        html.Small(
                            f"{user or 'Anonymous'}, {formatted_timestamp}",
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
        
        return formatted_messages  

    except Exception as e:
        return [html.Div(f"Error retrieving messages: {str(e)}")]




# -----------------------------------Announcements Content  
announcement_content = html.Div(
    [
        html.Div(
            id="anmsgs_display",
            style={
                "overflowX": "auto",
                "overflowY": "auto",
                "maxHeight": "400px",
            },
        ),
        html.Div(
            [
                html.Div(id="anmsgs_status"),
                html.Br(),
                dbc.Input(
                    id="anmsgs_header",
                    placeholder="Format: [TEAM NAME] Deadline Date, if urgent type URGENT. ex. [KM TEAM] May 05, 2024 URGENT.",
                    type="text",
                ),
                dbc.Textarea(
                    id="anmsgs_content",
                    placeholder="Type a message...",
                    style={"resize": "vertical"},
                    rows=5,
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button("Post", id="anmsgspost_button", color="primary", className="mt-2"),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Button("Cancel", id="anmsgscancel_button", color="secondary", className="mt-2"),
                            width="auto",
                        ),
                    ],
                    style={"justify-content": "flex-end"},
                ),
            ],
            id="anmsgs_id",
            style={"display": "none"},
        ),
    ]
)

announcement_footer = html.Div(
    [
        dbc.Button(
            "Add Message",
            id="anmsgs_footer_button",
            className="mt-2",
            color="success",
        ),
    ],
    className="d-flex justify-content-end",
)

app.layout = html.Div([announcement_content, announcement_footer, dcc.Location(id="url", refresh=False)])



# Callback to control visibility of the message input area
@app.callback(
    Output("anmsgs_id", "style"),
    [Input("anmsgs_footer_button", "n_clicks"), 
     Input("anmsgscancel_button", "n_clicks")],
    [State("anmsgs_id", "style")],  
)
def toggle_announcement_form(footer_clicks, cancel_clicks, current_style):
    ctx = callback_context  

    footer_clicks = footer_clicks or 0
    cancel_clicks = cancel_clicks or 0

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "anmsgs_footer_button" and footer_clicks > 0:
        return {"display": "block"}

    elif trigger_id == "anmsgscancel_button" and cancel_clicks > 0:
        return {"display": "none"}

    raise PreventUpdate



# Callback to insert a new message into the database
@app.callback(
    [
        Output("anmsgs_status", "children"),
        Output("new_homeannouncement_alert", "children"),
        Output("new_homeannouncement_alert", "is_open"), 
    ],
    [
        Input("anmsgspost_button", "n_clicks"),
        Input("new_homeannouncement_alert", "n_dismiss") 
    ],  
    [
        State("anmsgs_header", "value"),   
        State("anmsgs_content", "value"),
        State("currentuserid", "data")
    ]
)
def insert_announcement(n_clicks, n_dismiss, anmsgs_header, anmsgs_content, current_userid):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate 
 
    if ctx.triggered[0]['prop_id'] == 'new_homeannouncement_alert.n_dismiss':
        return ["", "", False]

    if not n_clicks or not anmsgs_header or not anmsgs_content: 
        return ["", "", False]

    try: 
        user_sql = """
            SELECT username
            FROM maindashboard.users
            WHERE user_id = %s
        """
        user_df = db.querydatafromdatabase(user_sql, [current_userid], ["username"])

        if user_df.empty:
            raise Exception("User not found")

        username = user_df.iloc[0]['username'] 

        # Insert the announcement with the username
        sql = """
            INSERT INTO maindashboard.announcements (anmsgs_header, anmsgs_content, anmsgs_user)
            VALUES (%s, %s, %s)
        """
        db.modifydatabase(sql, (anmsgs_header, anmsgs_content, username)) 
        
        # Record the alert in the alerts table
        alert_sql = """
            INSERT INTO maindashboard.alerts (alert_userid, alert_message)
            VALUES (%s, %s)
        """
        db.modifydatabase(alert_sql, (current_userid, f"{username} has a new announcement!")) 

        return ["", "Announcement posted!", True]

    except Exception as e: 
        return [f"Error: {str(e)}", "", False] 





# Callback to fetch announcements and display them
@app.callback(
    Output("anmsgs_display", "children"),
    [Input("url", "pathname")],
)
def fetch_announcements(pathname):
    if pathname != "/homepage":
        raise PreventUpdate

    try:
        start_of_month, end_of_month = get_month_range()

        sql = """
            SELECT anmsgs_header, anmsgs_content, anmsgs_user, anmsgs_timestamp
            FROM maindashboard.announcements
            WHERE anmsgs_timestamp BETWEEN %s AND %s
            ORDER BY anmsgs_timestamp DESC
        """

        values = (start_of_month, end_of_month)
        dfcolumns = ["anmsgs_header", "anmsgs_content", "anmsgs_user", "anmsgs_timestamp"]
        df = db.querydatafromdatabase(sql, values, dfcolumns)

        if df.empty:
            return [html.Div("No announcements this month")]

        formatted_announcements = []
        for row in df.itertuples(index=False):
            announcement_header = getattr(row, "anmsgs_header")
            announcement_content = getattr(row, "anmsgs_content")
            announcement_user = getattr(row, "anmsgs_user")
            announcement_timestamp = getattr(row, "anmsgs_timestamp")

            formatted_announcements.append(
                html.Div(
                    [
                        html.P(announcement_header),
                        html.P(announcement_content),
                        html.Small(
                            f"{announcement_user or 'Anonymous'}, {announcement_timestamp}",
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


 



# Callback to display the alerts container
@app.callback(
    Output("alerts_container", "children"),
    [Input('url', 'pathname')],  
)
def display_alerts(pathname):
    if pathname == '/homepage':  
         
        # Fetch alerts data within the last 15 days
        fifteen_days_ago = datetime.now() - timedelta(days=15)
        sql = """
            SELECT u.username AS user, a.alert_message, a.alert_timestamp
            FROM maindashboard.alerts a
            INNER JOIN maindashboard.users u ON a.alert_userid = u.user_id
            WHERE a.alert_timestamp >= %s
            ORDER BY a.alert_timestamp DESC
        """
        cols = ["user", "alert_message", "alert_timestamp"]

        df = db.querydatafromdatabase(sql, (fifteen_days_ago,), cols) 
        
        if not df.empty:
            alerts = []
            for index, row in df.iterrows():
                alert_message = row['alert_message']
                alert_timestamp = row['alert_timestamp']
                formatted_date = alert_timestamp.strftime("%B %d, %Y %I:%M %p")
                alert_html = html.Div([
                    html.P(alert_message, className="alert-message"),
                    html.P(formatted_date, 
                           className="alert-timestamp", 
                           style={
                               "font-size": "smaller", 
                               "font-style": "italic", 
                               "text-align": "right"
                               }
                            )
                ], className="alert-container")
                alerts.append(alert_html)
            return alerts
        else:
            return [html.Div("No new announcements since 15 days ago")]
    else:
        raise PreventUpdate







 

















card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="|   Monthly Team Messages   |", tab_id="tab-team-msg"),
                    dbc.Tab(label="|   Monthly Announcements   |", tab_id="tab-announcements"), 
                ],
                id="card-tabs",
                active_tab="tab-team-msg",
            )
        ),
        dbc.CardBody(id="card-body-content"),   
        dbc.CardFooter(id="card-footer-content"),   
    ] 
)



# Callback to update card content
@app.callback(
    [Output("card-body-content", "children"),
     Output("card-footer-content", "children")],
    [Input("card-tabs", "active_tab")]
)
def update_card_content(active_tab):
    if active_tab == "tab-team-msg":
        return team_messages_content, team_messages_footer
    elif active_tab == "tab-announcements":
        return announcement_content, announcement_footer
    else:
        return "Tab not found", None  # Fallback case
 
 
 

approval_card = dbc.Card(
    [
        dbc.CardHeader("NEW ANNOUNCEMENTS", className="text-center text-bold"),
        dbc.CardBody(
            [
                dcc.Loading(
                    id="loading-alerts",
                    type="default",
                    children=html.Div(id="alerts_container")
                )
            ]
        ),
    ],
    className="mb-3",
    style={"maxHeight": "200px", "overflowY": "auto"}
)



upcomingevents_card = dbc.Card(
    [
        dbc.CardHeader("UPCOMING EVENTS", className="text-center text-bold"),
        dbc.CardBody(
            [
                html.P("Some exciting event happening soon.", className="card-text"),
            ]
        ),
    ],
    className="mb-3"
)









layout = html.Div(
    [
        dcc.Store(id='stored-messages', storage_type='memory'),
        dcc.Store(id='message-store', data=[]),
        
        html.Div(id='post-trigger', style={'display': 'none'}),

        html.Div(  
                [
                dcc.Store(id='home_id_store', storage_type='session', data=0),
                ]
            ),
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [   
                    dbc.Row(
                        dbc.Col(
                            [
                                dbc.Alert(id = 'greeting_alert', color = 'dark'),
                                dbc.Alert(id="new_homeannouncement_alert", is_open=False, dismissable=True, color="info"),
                            ]
                        )
                    ),
                    html.Br(),

                    dbc.Row(
                        dbc.Col(
                            card, width=12
                        )
                    ),
                    html.Br(),

                    
                    dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.Img(src=app.get_asset_url("icons/admin_icon.png"), style={"height": "100px"})),
                                                        dbc.Col(
                                                            [
                                                                html.Div(style={'background-color': '#31356E', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                html.H5("Administration Team", className="card-title fw-bold text-dark", style={"text-align": "right",'text-decoration': 'none'})
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
                                    href='/administration_dashboard'
                                    ),
                                    width={"size": 6, "md": 12, "sm": 12},
                                ),
                                dbc.Col(
                                    html.A(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.Img(src=app.get_asset_url("icons/eqa_icon.png"), style={"height": "100px"})),
                                                        dbc.Col(
                                                            [
                                                                html.Div(style={'background-color': '#F8B237', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                html.H5("External Quality Assurance Team", className="card-title fw-bold text-dark", style={"text-align": "right",'text-decoration': 'none'})
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
                                    href='/eqa_dashboard'
                                    ),
                                    width={"size": 6, "md": 12, "sm": 12},
                                ),
                            ],
                            className="mb-3"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.Img(src=app.get_asset_url("icons/iqa_icon.png"), style={"height": "100px"})),
                                                        dbc.Col(
                                                            [
                                                                html.Div(style={'background-color': '#D37157', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                html.H5("Internal Quality Assurance Team", className="card-title fw-bold text-dark", style={"text-align": "right",'text-decoration': 'none'})
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
                                    href='/iqa_dashboard'
                                    ),
                                    width={"size": 6, "md": 12, "sm": 12},
                                ),
                                dbc.Col(
                                    html.A(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.Img(src=app.get_asset_url("icons/km_icon.png"), style={"height": "100px"})),
                                                        dbc.Col(
                                                            [
                                                                html.Div(style={'background-color': '#39B54A', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                html.H5("Knowledge Management Team", className="card-title fw-bold text-dark", style={"text-align": "right",'text-decoration': 'none'})
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
                                    href='/km_dashboard'
                                    ),
                                    width={"size": 6, "md": 12, "sm": 12},
                                ),
                            ],
                            className="mb-3"
                        ),
                    ],
                    width=7,  
                ),
                dbc.Col(
                    [   # Right column for the timeline card
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        create_time_date_card(),
                                        dcc.Interval(
                                            id="interval-component",
                                            interval=1*1000,  # in milliseconds
                                            n_intervals=0
                                        )
                                    ]
                                )
                            ],
                            className="mb-3",
                            style={"backgroundColor": "#FFFFFF"},
                        ),
                        dbc.Row([
                            html.A(
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [           
                                                dbc.Row(html.Img(src=app.get_asset_url("icons/qaofficer_icon.png"), style={"height": "100px", "object-fit": "contain"})),  # Adjusted styling
                                                dbc.Row(style={'background-color': '#7A0911', 'width': '100%', 'height': '20px', 'margin': 'auto'}),  # Rectangle
                                                dbc.Row(
                                                    html.H5("Quality Assurance Officers", className="card-title fw-bold text-dark text-center"), 
                                                    style={'text-decoration': 'none'}
                                                )
                                            ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#FFFFFF"},
                                    ),

                                ),
                                href='/QAOfficers_dashboard',
                                style={'text-decoration': 'none'}
                            )
                        ]),
                        approval_card,   
                        #upcomingevents_card,
                    ],
                    width=3,  md=3, sm=12
                ),
            ],
            className="mb-3",
            style={'padding-bottom': '2rem'}
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



# Callback for generating greeting alert content
@app.callback(
    [
        Output('greeting_alert', 'children'),
        Output('greeting_alert', 'color'),
    ],
    [
        Input('url', 'pathname'), 
        Input('currentuserid', 'data')
    ]
)
 
def generate_greeting(pathname, user_id):
    if (pathname == '/homepage') and user_id != -1:
        text = None
        color = None

        sql = """
            SELECT 
                user_livedname AS livedname, 
                user_fname AS fname 
            FROM 
                maindashboard.users 
            WHERE 
                user_id = %s;
        
        """
        values = [user_id]
        cols = ['livedname', 'fname']
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.empty or (df.isnull().all().all()) or (df['livedname'].str.strip().eq("").all() and df['fname'].str.strip().eq("").all()):
            text = html.H5(html.B("?? Welcome!"))
            color = '#F9B236'  # Set default color
        else:
            name = df['livedname'][0] if df['livedname'][0] else df['fname'][0]
            time = datetime.now(pytz.timezone('Asia/Manila')).hour

            if time >= 0 and time < 12:
                text = html.H5(html.B("Good morning, %s!" % name))
                color = '#F9B236'    
            elif time >= 12 and time < 18:
                text = html.H5(html.B("Good afternoon, %s!" % name))
                color = '#D37157'
            elif time >= 18 and time < 22:
                text = html.H5(html.B("Good evening, %s!" % name))
                color = '#A09DCB'
            else:
                text = html.H5(html.B("Good night, %s!" % name))
                color = '#7EADE4'

        return [text, color]
    else: 
        raise PreventUpdate





@app.callback(
    [Output('time', 'children'), Output('date', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_time_date(n):
    # Get the current time in Asia/Manila time zone
    ph_tz = pytz.timezone('Asia/Manila')
    now = datetime.now(ph_tz)
    
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%A, %B %d, %Y")
    return current_time, current_date