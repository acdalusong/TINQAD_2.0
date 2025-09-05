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
        dbc.Alert(id="teammsgs_status", is_open=False, duration=3000),
        html.Div(
            [  
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
            n_clicks = 0
        ),
    ],
    className="d-flex justify-content-end",
)






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
            n_clicks = 0
        ),
    ],
    className="d-flex justify-content-end",
)


# Callback to fetch announcements and display them
@app.callback(
    Output("anmsgs_display", "children"),
    [
        Input("url", "pathname"),
        Input("added-ann-trigger","data"),
        Input("deleted-ann-trigger","data"),
        Input("currentuserid", "data")
    ],
)
def fetch_announcements(pathname, trigger_add, trigger_del, current_user_id):
    if pathname != "/homepage":
        raise PreventUpdate

    start_of_month, end_of_month = get_month_range()

    sql = """
        SELECT anmsgs_id, anmsgs_header, anmsgs_content, anmsgs_user, anmsgs_user_id, anmsgs_timestamp
        FROM maindashboard.announcements
        WHERE anmsgs_timestamp BETWEEN %s AND %s
        AND anmsgs_del_ind = FALSE
        ORDER BY anmsgs_timestamp DESC
    """

    values = (start_of_month, end_of_month)
    dfcolumns = ["anmsgs_id", "anmsgs_header", "anmsgs_content", "anmsgs_user", "anmsgs_user_id", "anmsgs_timestamp"]
    df = db.querydatafromdatabase(sql, values, dfcolumns)

    if df.empty:
        return [html.Div("No announcements this month")]

    out = []
    for row in df.itertuples(index=False):
        aid = row.anmsgs_id  # make sure you SELECT the PK in your query

        # Base message (always shown)
        ann_children = [
            html.H3(row.anmsgs_header),
            html.P(row.anmsgs_content),
            html.Small(
                f"{row.anmsgs_user}, {row.anmsgs_timestamp:%d %B %Y, %I:%M:%S %p}",
                style={"font-style": "italic"}
            ),
        ]

        # Only append edit/delete if this message belongs to current user
        if row.anmsgs_user_id == current_user_id:
            ann_children.append(
                html.Div(
                [
                    html.Span(
                        "edit",
                        id={'type': 'an-edit-link', 'index': aid},
                        style={"cursor": "pointer", "margin-right": "10px", "color": "#337ab7"}
                    ),
                    html.Span(
                        "delete",
                        id={'type': 'an-delete-link', 'index': aid},
                        style={"cursor": "pointer", "fontWeight": "bold", "color": "#ff4d4d"}
                    ),
                ],
                style={
                    "position": "absolute",  # takes it out of normal flow :contentReference[oaicite:4]{index=4}
                    "top": "0.5rem",         # adjust to align vertically
                    "right": "0"             # sticks to right edge of parent :contentReference[oaicite:5]{index=5}
                }
                ),
            )
        # finalize
        ann_children.append(html.Hr()),
        out.append(
            html.Div(ann_children, style={"margin-bottom": "1rem", "position": "relative"})
        )
    return out


@app.callback(
    [
        Output("anmsgs_id", "style"),
        Output("anmsgs_header", "value"),
        Output("anmsgs_content", "value"),
        Output("ann-to-edit", "data"),
        Output("added-ann-trigger", "data"),
        Output("new_homeannouncement_alert", "is_open"),
        Output("new_homeannouncement_alert", "color"),
        Output("new_homeannouncement_alert", "children"),
    ],
    [
        Input("anmsgs_footer_button", "n_clicks"),
        Input({'type': 'an-edit-link', 'index': ALL}, "n_clicks"),
        Input("anmsgscancel_button", "n_clicks"),
        Input("anmsgspost_button", "n_clicks"),
    ],
    [
        State("anmsgs_header", "value"),
        State("anmsgs_content", "value"),
        State("currentuserid", "data"),
        State("ann-to-edit", "data"),
        State("added-ann-trigger", "data"),
    ],
    prevent_initial_call=True
)
def handle_team_message(
    footer_clicks, edit_clicks, cancel_clicks, post_clicks,
    header, content, user_id, edit_id, trigger_count
):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # only proceed if one of our four controls actually triggered
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    allowed = {
        "anmsgs_footer_button",
        "anmsgscancel_button",
        "anmsgspost_button",
    }
    if not (trigger in allowed or trigger.startswith("{")):
        raise PreventUpdate

    new_trigger = trigger_count or 0

    # Cancel: hide form
    if trigger == "anmsgscancel_button" and cancel_clicks:
        return {"display": "none"}, "", "", None, new_trigger, False, no_update, no_update

    # Add Message button: show empty form
    if trigger == "anmsgs_footer_button" and footer_clicks:
        return {"display": "block"}, "", "", None, new_trigger, False, no_update, no_update

    # Edit link clicked: load existing and show form
    if trigger.startswith("{"):
        for i, c in enumerate(edit_clicks):
            if c:
                idx_b = ctx.triggered_id["index"]
                df = db.querydatafromdatabase(
                    "SELECT anmsgs_header, anmsgs_content FROM maindashboard.announcements WHERE anmsgs_id = %s",
                    [idx_b],
                    ["anmsgs_header", "anmsgs_content"],
                )
                if df.empty:
                    raise PreventUpdate
                return {"display": "block"}, df.at[0, "anmsgs_header"], df.at[0, "anmsgs_content"], idx_b, new_trigger, False, no_update, no_update

    # Post button clicked: either insert or update
    if trigger == "anmsgspost_button" and post_clicks:
        # Validate
        if not content or not content.strip():
            return {"display": "block"}, header, content, edit_id, new_trigger, True, "danger", "Announcement cannot be blank."

        if edit_id:
            # Update existing announcement
            db.modifydatabase(
                "UPDATE maindashboard.announcements SET anmsgs_header = %s, anmsgs_content = %s, anmsgs_timestamp = CURRENT_TIMESTAMP WHERE anmsgs_id = %s",
                (header, content, edit_id),
            )
            ann = "Announcement updated successfully!"
            user_df = db.querydatafromdatabase(
                "SELECT user_fname, user_sname FROM maindashboard.users WHERE user_id = %s",
                [user_id],
                ["user_fname", "user_sname"]
            )
            full_name = f"{user_df.at[0, 'user_fname']} {user_df.at[0, 'user_sname']}"
            
            db.modifydatabase(
                "UPDATE maindashboard.alerts SET alert_message = %s, alert_timestamp = CURRENT_TIMESTAMP WHERE alert_ann_id = %s",
                (f"{full_name} has updated an announcement!", edit_id))

            
        else:
            # Insert new announcement
            user_df = db.querydatafromdatabase(
                "SELECT user_fname, user_sname FROM maindashboard.users WHERE user_id = %s",
                [user_id],
                ["user_fname", "user_sname"]
            )
            full_name = f"{user_df.at[0, 'user_fname']} {user_df.at[0, 'user_sname']}"
            sql_ann = """
                INSERT INTO maindashboard.announcements (anmsgs_header, anmsgs_content, anmsgs_user, anmsgs_user_id) 
                VALUES (%s, %s, %s, %s)
                RETURNING anmsgs_id
            """
            values_ann = [header, content, full_name, user_id]
            result_df = db.execute_returning(sql_ann, values_ann, dfcolumns=['anmsgs_id'])
            announcement_id = int(result_df['anmsgs_id'][0])

            # Record the alert in the alerts table
            alert_sql = """
                INSERT INTO maindashboard.alerts (alert_userid, alert_message, alert_ann_id)
                VALUES (%s, %s, %s)
            """
            db.modifydatabase(alert_sql, (user_id, f"{full_name} has a new announcement!", announcement_id)) 

            ann = "Announcement posted successfully!"

        new_trigger += 1
        # Hide form, clear content, clear edit state, bump trigger, show success
        return {"display": "none"}, "", "", None, new_trigger, True, "success", ann

    # Fallback
    raise PreventUpdate



@app.callback(
    [
        Output("an-delete-modal", "is_open"),
        Output("ann-to-delete", "data"),
        Output("deleted-ann-trigger", "data"),
    ],
    [
        Input({'type': 'an-delete-link', 'index': ALL}, "n_clicks"),
        Input("an-delete-cancel", "n_clicks"),
        Input("an-delete-confirm", "n_clicks"),
    ],
    [
        State("ann-to-delete", "data"),
        State("an-delete-modal", "is_open"),
        State("deleted-ann-trigger", "data"),
    ],
    prevent_initial_call=True,
)
def handle_ann_delete(link_clicks, cancel_click, confirm_click, stored_id, is_open, del_trigger):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    prop_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # 1) A delete-link clicked → only if its n_clicks is truthy
    if prop_id.startswith("{") and any(link_clicks):
        # find which index actually incremented
        for i, c in enumerate(link_clicks):
            if c:
                # ctx.triggered_id holds the dict
                idx = ctx.triggered_id['index']
                return True, idx, del_trigger

    # 2) Cancel → close without bump
    if prop_id == "an-delete-cancel":
        return False, stored_id, del_trigger

    # 3) Confirm → soft‐delete + bump
    if prop_id == "an-delete-confirm":
        sql = """
            UPDATE maindashboard.announcements
            SET anmsgs_del_ind = TRUE
            WHERE anmsgs_id = %s
        """
        db.modifydatabase(sql, (stored_id,))
        return False, None, (del_trigger or 0) + 1

    raise PreventUpdate



# Callback to display the alerts container
@app.callback(
    Output("alerts_container", "children"),
    [Input('url', 'pathname'),
     Input("added-ann-trigger","data"),
     Input("deleted-ann-trigger","data")],  
)
def display_alerts(pathname, trigger_add, trigger_del):
    if pathname == '/homepage':  
         
        # Fetch alerts data within the last 15 days
        fifteen_days_ago = datetime.now() - timedelta(days=15)
        sql = """
            SELECT u.username AS user, a.alert_message, a.alert_timestamp
            FROM maindashboard.alerts a
            INNER JOIN maindashboard.users u ON a.alert_userid = u.user_id
            WHERE a.alert_timestamp >= %s
			AND alert_ann_id IN (
				SELECT anmsgs_id
				FROM maindashboard.announcements
				WHERE anmsgs_del_ind = FALSE
			)
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
        dcc.Store(id="deleted-msg-trigger", storage_type="memory"),
        dcc.Store(id='msg-to-delete', storage_type='memory'),
        dcc.Store(id='msg-to-edit', storage_type='memory'),
        dcc.Store(id='ann-to-edit', storage_type='memory'),
        dcc.Store(id="added-msg-trigger", storage_type="memory"),
        dcc.Store(id="added-ann-trigger", storage_type="memory", data=0),
        dcc.Store(id="deleted-ann-trigger", storage_type="memory", data=0),
        dcc.Store(id="ann-to-delete", storage_type="memory"),

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
                                dbc.Alert(id="new_homeannouncement_alert", is_open=False, duration=3000, color="info"),
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
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H3("Confirm deletion"), className="bg-primary"),
                        dbc.ModalBody(html.H5("Are you sure you want to delete this message? This action cannot be undone.")),
                        dbc.ModalFooter([
                            dbc.Button("Cancel", id="delete-cancel", color="secondary", className="me-2"),
                            dbc.Button("Delete", id="delete-confirm", color="danger")
                        ]),
                    ],
                    id="delete-modal",
                    centered=True,
                    className="modal-success"
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H3("Confirm deletion"), className="bg-primary"),
                        dbc.ModalBody(html.H5("Are you sure you want to delete this announcement?")),
                        dbc.ModalFooter([
                            dbc.Button("Cancel", id="an-delete-cancel", color="secondary", className="me-2"),
                            dbc.Button("Delete", id="an-delete-confirm", color="danger")
                        ]),
                    ],
                    id="an-delete-modal",
                    centered=True,
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







# Callback to fetch team messages and display them
@app.callback(
    Output("teammsgs_display", "children"),
    [Input("url", "pathname"),
     Input("deleted-msg-trigger", "data"),
     Input("added-msg-trigger", "data"),
     Input("currentuserid", "data")]  
)
def fetch_team_messages(pathname, delete_trigger, added_trigger, current_user_id):
    if pathname != "/homepage":
        raise PreventUpdate

    start_of_month, end_of_month = get_month_range()
    sql = """
        SELECT teammsgs_id, teammsgs_content, teammsgs_user, teammsgs_user_id, teammsgs_timestamp
        FROM maindashboard.teammessages
        WHERE teammsgs_timestamp BETWEEN %s AND %s
          AND teammsgs_del_ind = FALSE
        ORDER BY teammsgs_timestamp DESC
    """
    df = db.querydatafromdatabase(sql, (start_of_month, end_of_month), 
                                  ["teammsgs_id","teammsgs_content","teammsgs_user", "teammsgs_user_id", "teammsgs_timestamp"])
    if df.empty:
        return [html.Div("No messages this month")]
    
    formatted_messages = []
    for row in df.itertuples(index=False):
        mid = row.teammsgs_id
        # Base message (always shown)
        msg_children = [
            html.P(row.teammsgs_content),
            html.Small(
                f"{row.teammsgs_user}, {row.teammsgs_timestamp:%d %B %Y, %I:%M:%S %p}",
                style={"font-style": "italic"}
            ),
        ]

        # Only append edit/delete if this message belongs to current user
        if row.teammsgs_user_id == current_user_id:
            msg_children.append(
                html.Div(
                    [
                        html.Span(
                            "edit",
                            id={'type': 'edit-link', 'index': mid},
                            style={"cursor": "pointer", "margin-right": "10px", "color": "#337ab7"}
                        ),
                        html.Span(
                            "delete",
                            id={'type': 'delete-link', 'index': mid},
                            style={"cursor": "pointer", "fontWeight": "bold", "color": "#ff4d4d"}
                        ),
                    ],
                    style={
                        "position": "absolute",  # takes it out of normal flow :contentReference[oaicite:4]{index=4}
                        "top": "0.5rem",         # adjust to align vertically
                        "right": "0"             # sticks to right edge of parent :contentReference[oaicite:5]{index=5}
                    }
                ),
            )
        # finalize
        msg_children.append(html.Hr()),

        formatted_messages.append(
            html.Div(msg_children, style={"margin-bottom": "1rem", "position": "relative"})   
        )
    return formatted_messages


@app.callback(
    [
        Output("delete-modal", "is_open"),
        Output("msg-to-delete", "data"),
        Output("deleted-msg-trigger", "data"),
    ],
    [
        Input({'type':'delete-link','index': ALL}, "n_clicks"),
        Input("delete-cancel", "n_clicks"),
        Input("delete-confirm", "n_clicks"),
    ],
    [State("msg-to-delete", "data"),
     State("delete-modal", "is_open"),
     State("deleted-msg-trigger", "data")],
    prevent_initial_call=True
)
def handle_delete(all_link_clicks, cancel_click, confirm_click, stored_msg_id, is_open, del_trigger):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    prop_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # 1) A delete-link clicked → only if its n_clicks is truthy
    if prop_id.startswith("{") and any(all_link_clicks):
        # find which index actually incremented
        for i, c in enumerate(all_link_clicks):
            if c:
                # ctx.triggered_id holds the dict
                idx = ctx.triggered_id['index']
                return True, idx, del_trigger

    # 2) Cancel → close without bump
    if prop_id == "delete-cancel":
        return False, stored_msg_id, del_trigger

    # 3) Confirm → soft‐delete + bump
    if prop_id == "delete-confirm":
        sql = """
            UPDATE maindashboard.teammessages
            SET teammsgs_del_ind = TRUE
            WHERE teammsgs_id = %s
        """
        db.modifydatabase(sql, (stored_msg_id,))
        return False, None, (del_trigger or 0) + 1

    raise PreventUpdate

@app.callback(
    [
        Output("teammsgs_id", "style"),
        Output("teammsgs_content", "value"),
        Output("msg-to-edit", "data"),
        Output("added-msg-trigger", "data"),
        Output("teammsgs_status", "is_open"),
        Output("teammsgs_status", "color"),
        Output("teammsgs_status", "children"),
    ],
    [
        Input("teammsgs_footer_button", "n_clicks"),
        Input({'type': 'edit-link', 'index': ALL}, "n_clicks"),
        Input("teammsgscancel_button", "n_clicks"),
        Input("teammsgspost_button", "n_clicks"),
    ],
    [
        State("teammsgs_content", "value"),
        State("currentuserid", "data"),
        State("msg-to-edit", "data"),
        State("added-msg-trigger", "data"),
    ],
    prevent_initial_call=True
)
def handle_team_message(
    footer_clicks, edit_clicks, cancel_clicks, post_clicks,
    content, user_id, edit_id, trigger_count
):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # only proceed if one of our four controls actually triggered
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    allowed = {
        "teammsgs_footer_button",
        "teammsgscancel_button",
        "teammsgspost_button",
    }
    if not (trigger in allowed or trigger.startswith("{")):
        raise PreventUpdate

    new_trigger = trigger_count or 0

    # Cancel: hide form
    if trigger == "teammsgscancel_button" and cancel_clicks:
        return {"display": "none"}, "", None, new_trigger, False, no_update, no_update

    # Add Message button: show empty form
    if trigger == "teammsgs_footer_button" and footer_clicks:
        return {"display": "block"}, "", None, new_trigger, False, no_update, no_update

    # Edit link clicked: load existing and show form
    if trigger.startswith("{"):
        for i, c in enumerate(edit_clicks):
            if c:
                idx = ctx.triggered_id["index"]
                df = db.querydatafromdatabase(
                    "SELECT teammsgs_content FROM maindashboard.teammessages WHERE teammsgs_id = %s",
                    [idx],
                    ["teammsgs_content"],
                )
                if df.empty:
                    raise PreventUpdate
                return {"display": "block"}, df.at[0, "teammsgs_content"], idx, new_trigger, False, no_update, no_update

    # Post button clicked: either insert or update
    if trigger == "teammsgspost_button" and post_clicks:
        # Validate
        if not content or not content.strip():
            return {"display": "block"}, content, edit_id, new_trigger, True, "danger", "Message cannot be blank."

        if edit_id:
            # Update existing message
            db.modifydatabase(
                "UPDATE maindashboard.teammessages SET teammsgs_content = %s, teammsgs_timestamp = CURRENT_TIMESTAMP WHERE teammsgs_id = %s",
                (content, edit_id),
            )
            msg = "Message updated successfully!"
        else:
            # Insert new message
            user_df = db.querydatafromdatabase(
                "SELECT user_fname, user_sname FROM maindashboard.users WHERE user_id = %s",
                [user_id],
                ["user_fname", "user_sname"]
            )
            full_name = f"{user_df.at[0, 'user_fname']} {user_df.at[0, 'user_sname']}"
            db.modifydatabase(
                "INSERT INTO maindashboard.teammessages (teammsgs_content, teammsgs_user, teammsgs_user_id) VALUES (%s, %s, %s)",
                (content, full_name, user_id),
            )
            msg = "Message posted successfully!"

        new_trigger += 1
        # Hide form, clear content, clear edit state, bump trigger, show success
        return {"display": "none"}, "", None, new_trigger, True, "success", msg

    # Fallback
    raise PreventUpdate