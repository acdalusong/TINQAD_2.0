import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State
from dash import callback_context
from dash.exceptions import PreventUpdate

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db
from dash.dash_table.Format import Group








layout = html.Div(
    [
        dbc.Row(
            [
                # Navbar
                cm.sidebar,
                
                dbc.Col(
                    dbc.Card(
                        id="instructions-card",
                        children=[
                            dbc.CardBody(
                                [
                                    html.H4(
                                        "Training Document Submission Reminders",
                                        className="card-title",
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        id="trinstructions_display",
                                        style={
                                            "border": "1px solid #ccc",
                                            "padding": "10px",
                                            "borderRadius": "5px",
                                            "minHeight": "150px",
                                            "overflowY": "auto",
                                            "white-space": "pre-wrap",
                                        }, 
                                    ),
                                    
                                    html.Div(
                                        [
                                            html.Div(id="trinstructions_status"),
                                            html.Br(),
                                            
                                            dbc.Textarea(
                                                id="trinstructions_content",
                                                placeholder="Type a new instruction, make sure its complete before saving!",
                                                style={"resize": "vertical"},
                                                rows=5,
                                            ),
                                            html.Br(),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Button("Save", id="save_button", color="primary", className="mt-2 mr-1"),
                                                        width="auto",
                                                    ),
                                                    dbc.Col(
                                                        dbc.Button("Cancel", id="cancel_button", color="secondary", className="mt-2"),
                                                        width="auto",
                                                    ),
                                                ],
                                                style={"justify-content": "flex-end"},
                                            ),
                                        ],
                                        id="trinstructions_id",
                                        style={"display": "none"},
                                    ),

                                    html.Br(),
                                    html.Div(
                                        [
                                            dbc.Button("Edit", id="edit_button", n_clicks=0, color="link"),
                                            dbc.Button("Proceed", id="proceed_button", color="primary", href="/training_documents?mode=add"), 
                                        ],
                                        style={"display": "flex", "justify-content": "flex-end", "gap": "10px"},
                                    ),
                                     
                                ],
                            ),
                        ],
                    ),
                    width=8,
                ),
            ]
        ),
        html.Div(style={"margin-top": "20px"}),
        # Footer
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width=12),
            ],
        ),
    ],
)


 

  
    
# Callback to fetch announcements and display them
@app.callback(
    Output("trinstructions_display", "children"),
    [Input("url", "pathname")],   
)
def fetch_announcements(pathname):
    if pathname == "/instructions": 
        sql = """
            SELECT trinstructions_content
            FROM adminteam.training_instructions
            ORDER BY trinstructions_id DESC
            LIMIT 1;
        """

        values = ()
        dfcolumns = ["trinstructions_content"]  
        df = db.querydatafromdatabase(sql, values, dfcolumns)

        instruction_content = df.loc[0, "trinstructions_content"]
        return instruction_content  
 
 

# Corrected callback for inserting instructions
@app.callback(
    Output("trinstructions_status", "children"),
    [Input("save_button", "n_clicks")],
    [State("trinstructions_content", "value")],   
)
def insert_instructions(n_clicks, trinstructions_content):
    if n_clicks is None or trinstructions_content is None:
        raise PreventUpdate

    try:
        sql = """
            INSERT INTO adminteam.training_instructions (trinstructions_content)
            VALUES (%s)   
        """

        db.modifydatabase(sql, (trinstructions_content,))  
        return ["Instructions updated successfully!"]

    except Exception as e:
        return [(f"Error: {str(e)}")]   
    


# Callback to toggle text area visibility when Edit or Cancel is clicked
@app.callback(
    Output("trinstructions_id", "style"),  # The div that contains the text area and buttons
    [Input("edit_button", "n_clicks"), Input("cancel_button", "n_clicks")],  # Edit and Cancel buttons
    [State("trinstructions_id", "style")],  # Current style
)
def toggle_text_area_visibility(edit_clicks, cancel_clicks, current_style):
    ctx = callback_context

    # Determine which button was last clicked
    if not ctx.triggered:
        raise PreventUpdate

    # Get the ID of the last triggered component
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If Edit was clicked, set style to 'block'
    if trigger_id == "edit_button" and edit_clicks > 0:
        return {"display": "block"}

    # If Cancel was clicked, set style to 'none'
    elif trigger_id == "cancel_button" and cancel_clicks > 0:
        return {"display": "none"}

    # If no relevant action, prevent update
    raise PreventUpdate