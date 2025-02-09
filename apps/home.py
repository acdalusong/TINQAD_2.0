import hashlib

import dash
from dash import callback_context, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = dbc.Row(
    [
        dbc.Col(
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Store(id='user_id_store', storage_type='session', data=0),
                        ]
                    ),
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url('icons/qao-logo-block.png'),
                                style={
                                    'max-width': '25vw',
                                    'margin': 'auto',  # Center the image horizontally
                                    'display': 'block'  # Display as block element
                                },
                            ),
                            html.H5("Total Integrated Network for Quality Assurance and Development", className="fw-bolder text-center"),
                            html.P("Copyright (c) 2024. Quality Assurance Office, University of the Philippines", className="text-center"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.A("About TINQAD", href="/about-us", className="link-style"), " | ",
                                            html.A("Main Website", href="https://qa.upd.edu.ph/", className="link-style"), " | ",
                                            html.A("Facebook", href="https://www.facebook.com/QAODiliman", className="link-style"), " | ",
                                            html.A("LinkedIn", href="https://www.linkedin.com/company/quality-assurance-office/about/", className="link-style")
                                        ],
                                        width="auto"
                                    ),
                                ],
                                style={'margin': 'auto'},
                                align='center',
                                justify='center'
                            ),
                        ],
                        style={
                            'top': '10rem',
                            'right': '25rem',
                            'position': 'relative',
                            'z-index': 1,
                            'max-width': '70vw',
                            'margin': 'auto',
                            'text-align': 'center',
                            'padding': '2em',
                        }
                    ),
                    html.Div(
                        [
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H4("Welcome to TINQAD", className="fw-bolder text-left")),
                                        dbc.CardBody(
                                            [
                                                html.H2("LOG IN", className="card-title fw-bolder"),
                                                html.Br(),

                                                dbc.Alert(id='login_alert', is_open=False),

                                                dbc.Label("Registered Email"),
                                                dbc.Input(type="text", id="login_username", className='form-control'),
                                                html.Br(),
                                                
                                                dbc.Label("Password"),
                                                dbc.Input(type="password", id="login_password",className='form-control'),
                                                html.Br(),
                                                dbc.Checklist(
                                                    options=[
                                                        {"label": "Show Password", "value": 1}
                                                    ],
                                                    value=[],
                                                    id="show_password",
                                                    inline=True,
                                                ),
                                                html.Br(),
                                                dbc.Row(
                                                    dbc.Col(
                                                        dbc.Button("Log in",
                                                                color="primary",
                                                                className="fw-bolder",
                                                                id='login_loginbtn'),
                                                        width={'size': 4, 'offset': 8},
                                                        className="d-flex justify-content-end"
                                                    )
                                                ),
                                                html.Br(),
                                                html.Br(),
                                                html.H4("Total Integrated Network for Quality Assurance and Development", className="fw-bolder text-danger"),
                                                html.P("The Total Integrated Network for Quality Assurance and Development (TINQAD) is a centralized network that allows the singular monitoring of the Quality Assurance teams activities."),
                                            ]
                                        ),
                                    ],
                                ),
                                width={"size": 6, "offset": 1},
                                style={
                                    'position': 'fixed',
                                    'right': '2rem',    # Position the div at the right of the screen
                                    'width': '45%',    # Set the width of the div
                                    'bottom': '0rem',   # Adjust bottom margin
                                    'top': '5rem',
                                    'padding': '1rem',
                                    'border-radius': '10px', # TRY SWITCHING
                                    'box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.1)',    # Add box shadow, # TRY SWITCHING
                                }
                            ),
                        ],
                    ),
                ],        
                    id='bg',
                    style={
                        'position': 'fixed',
                        'top': '3.5rem',    # Adjust top margin as needed
                        'left': '0',
                        'width': '100%',
                        'height': '100%',
                        'min-height': 'calc(100% + 20rem)',  # Ensure content is scrollable
                        'background-image': 'url("' + app.get_asset_url('icons/bg.png') + '")',
                        'background-size': 'cover',
                        'background-position': 'center bottom',
                        'mask-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 1.0) 50%, transparent 100%)',
                    },
            ),
        ),
    ],
)


# Client-side callback to handle Enter key presses on both username and password fields.
app.clientside_callback(
    """
    function(n_key_presses_password, n_key_presses_username) {
        // Get the login button element
        var loginBtn = document.getElementById('login_loginbtn');

        // Helper function to attach the Enter key event listener to a field.
        function attachEnterListener(fieldId) {
            var field = document.getElementById(fieldId);
            if (field && !field.hasAttribute('data-listener-attached')) {
                field.addEventListener('keypress', function(event) {
                    if (event.key === 'Enter') {
                        event.preventDefault();
                        loginBtn.click();
                    }
                });
                // Mark this field so that we don't attach multiple listeners
                field.setAttribute('data-listener-attached', 'true');
            }
        }

        // Attach listeners to both the password and email fields.
        attachEnterListener('login_password');
        attachEnterListener('login_username');

        // Since this callback is just for side-effects, return no update.
        return window.dash_clientside.no_update;
    }
    """,
    Output('login_loginbtn', 'n_clicks'),
    [Input('login_password', 'n_key_presses'),
     Input('login_username', 'n_key_presses')],
    [State('login_loginbtn', 'n_clicks')]
)
# Toggle password visibility.
@app.callback(
    Output('login_password', 'type'),
    [Input('show_password', 'value')]
)
def toggle_password_visibility(checked_values):
    if checked_values:
        return 'text'
    else:
        return 'password'

# Combined login process and routing callback.
@app.callback(
    [
        Output('login_alert', 'color'),
        Output('login_alert', 'children'),
        Output('login_alert', 'is_open'),
        Output('login_username', 'className'),
        Output('login_password', 'className'),
        Output('currentuserid', 'data'),
        Output('currentrole', 'data'),
        Output('url', 'pathname')  # Redirect output.
    ],
    [
        Input('login_loginbtn', 'n_clicks')
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value')
    ]
)
def loginprocess(loginbtn, useremail, password):
    ctx = callback_context
    
    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    if ctx.triggered:
        # Set default outputs.
        accesstype = 0
        alert_open = False 
        alert_color = ""
        alert_text = ""
        username_class = 'red-border' if not useremail else 'form-control'
        password_class = 'red-border' if not password else 'form-control'
        currentuserid = 0
        pathname = dash.no_update  # Do not change URL unless login is successful.

        if eventid == 'login_loginbtn':
            if loginbtn and useremail and password:
                sql = """
                    SELECT user_id, user_access_type
                    FROM maindashboard.users
                    WHERE user_email = %s AND user_password = %s
                """

                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
                values = [useremail, encrypt_string(password)]
                cols = ['user_id', 'user_access_type']

                # Assuming db.querydatafromdatabase returns a DataFrame
                df = db.querydatafromdatabase(sql, values, cols)
                if df.shape[0]: # Login successful.
                    currentuserid = df['user_id'][0]
                    accesstype = df['user_access_type'][0]
                    pathname = '/homepage'
                else:
                    currentuserid = -1
                    alert_color = 'danger'
                    alert_text = 'Incorrect username or password.'
                    alert_open = True
            elif not all([useremail, password]):
                alert_color = 'danger'
                alert_text = 'Please enter your username and password.'
                alert_open = True
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate

    return [alert_color, alert_text, alert_open, username_class, password_class, currentuserid, accesstype, pathname]
