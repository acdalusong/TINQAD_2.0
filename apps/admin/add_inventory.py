import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, dash_table
from dash import callback_context, no_update

import dash
from dash.exceptions import PreventUpdate
import pandas as pd
import re

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import base64
import os
from urllib.parse import urlparse, parse_qs

UPLOAD_DIRECTORY = r".\assets\database\admin\inventory_tracker"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Define the highlight colors
highlight_colors = {
    'primary': "#0a4323",    # Used for main headers
    'secondary': "#7a0911",  # Used for section titles
    'accent': "#f8b237"      # Accent color for borders and emphasis
}


# Build the form as a vertical stack of Cards
form = dbc.Form(
    [

        # 1) BASIC ITEM INFORMATION
        dbc.Card(
            [
                dbc.CardHeader(html.H5("Basic Item Information"), className="bg-secondary text-white"),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col([dbc.Label("Item Name"), dbc.Input(id="item_name", type="text", required=True)]),
                                dbc.Col([
                                    dbc.Label("Image Upload"),
                                    dcc.Upload(
                                        id="item_image",
                                        children=html.Div(["Drag & drop or click to select image"]),
                                        style={
                                            "width": "100%", "height": "80px",
                                            "lineHeight": "80px", "borderWidth": "1px",
                                            "borderStyle": "dashed", "borderRadius": "5px",
                                            "textAlign": "center",
                                        },
                                        multiple=True,
                                    ),
                                    html.Br(),
                                    html.Img(id="image_preview", style={"maxWidth": "100%", "height": "auto"}),
                                    html.Div(id="item_image_output")  
                                ], width=4),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col([dbc.Label("S/N or Barcode"), dbc.Input(id="item_barcode_number", type="text", required=True)]),
                                dbc.Col([dbc.Label("Brand"),          dbc.Input(id="item_brand",         type="text", required=True)]),
                                dbc.Col([dbc.Label("QA Property No. (Initial)"), dbc.Input(id="item_qa_initial_property_no", type="text", required=True)]),
                                dbc.Col([dbc.Label("QA Property No. (Updated)"), dbc.Input(id="item_qa_updated_property_no", type="text")]),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            dbc.Col([dbc.Label("Description"), dbc.Input(id="item_description", type="text", required=True)], width=12),
                            className="mb-3",
                        ),
                    ]
                ),
            ],
            id="card_1",
            className="mb-4",
        ),


        # 2) PROCUREMENT AND SUPPLIER DETAILS
        dbc.Card(
            [
                dbc.CardHeader(html.H5("Procurement and Supplier Details"), className="bg-primary text-white"),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col([dbc.Label("PO Number"),     dbc.Input(id="item_po_number", type="text", required=True)]),
                                dbc.Col([dbc.Label("Supplier"),      dbc.Input(id="item_supplier", type="text", required=True)]),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col([dbc.Label("Company Name"),      dbc.Input(id="item_company_name", type="text", required=True)]),
                                dbc.Col([dbc.Label("Contact Number"),    dbc.Input(id="item_company_contact_number", type="text", required=True)]),
                                dbc.Col([dbc.Label("Email"),             dbc.Input(id="item_company_email", type="text", required=True)]),
                            ],
                            className="mb-3",
                        )
                    ]
                ),
            ],
            id="card_2",
            className="mb-4",            
        ),

        # 3) COST/QUANTITY
        dbc.Card(
            [
                dbc.CardHeader(html.H5("Cost / Quantity"), className="bg-success text-white"),
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Label("Unit Cost"),
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText("₱"),
                                            dbc.Input(id="item_unit_cost", required=True, min=0, step=0.01),
                                        ]
                                    ),
                                ],
                                width=6,
                            ),
                        ],
                        className="mb-3",
                    )
                ),
            ],
            id="card_3",
            className="mb-4",            
        ),

        # 4) USAGE & ASSIGNMENT
        dbc.Card(
            [
                dbc.CardHeader(html.H5("Usage & Assignment"), className="bg-danger text-white"),
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Label("Staff Responsible"),
                                    dbc.Select(id="item_staff_responsibile", options=[], required=True),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Assigned To"),
                                    dbc.Select(id="item_assigned_to", options=[], required=True),
                                ],
                                width=6,
                            ),
                        ],
                        className="mb-3",
                    )
                ),
            ],
            id="card_4",
            className="mb-4",
        ),

    ],
    # by default this is a vertical form :contentReference[oaicite:7]{index=7}
)
# Callback to display the names of the uploaded files
@app.callback(
    [
        Output("item_image_output", "children"),
    ],
    [
        Input("item_image", "filename"),
        Input("url", "search")
    ],
)
def display_item_image_file(filenames, search):
    if not filenames:
        return ["No file uploaded"]
    
    # Parse the query parameter to check for mode
    parsed = urlparse(search)
    mode = parse_qs(parsed.query).get('mode', [None])[0]
    
    # Calculate relative path for linking the file in edit mode
    assets_folder = os.path.normpath("./assets")
    upload_relative_path = os.path.relpath(UPLOAD_DIRECTORY, assets_folder)
    upload_relative_path = upload_relative_path.replace(os.path.sep, "/")
    
    def build_file_message(fname):
        base_name = os.path.basename(fname)
        message = f"📑File Uploaded: {base_name}"
        if mode == "edit":
            file_url = f"/assets/{upload_relative_path}/{base_name}"
            return html.A(message, href=file_url, target="_blank")
        return message
    
    if isinstance(filenames, list):
        # Process each uploaded file
        children = [ build_file_message(fname) for fname in filenames ]
        return [children]
    else:
        return [ build_file_message(filenames) ]

layout = dbc.Container(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                [
                    html.Div(  
                            [
                                dcc.Store(id='inventory_eval_toload', storage_type='memory', data=0),
                            ]
                        ),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H1(id="inventory_page_header"),
                                        width=8
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            "Back",
                                            color="success",
                                            href="/inventory_tracker"
                                        ),
                                        width=4,
                                        id="inventory_tracker_back_btn_div",
                                        style={"display": "flex", "justifyContent": "flex-end"}
                                    )
                                ],
                                align="center"
                            ),
                        ],
                        className="mb-0"
                    ),
                    html.Hr(),
                    html.Div(  
                            [
                                dcc.Store(id='inventory_eval_toload', storage_type='memory', data=0),
                            ]
                        ),
                    form, 
                    html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='inventorytracker_removerecord',
                                            options=[
                                                {
                                                    'label': "Mark for Deletion",
                                                    'value': 1
                                                }
                                            ], 
                                            style={'fontWeight':'bold'},
                                        ),
                                        width=5,
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='inventorytracker_removerecord_div'
                        ),
                    dbc.Alert(id='inventory_tracker_alert', is_open=False), # For feedback purpose
                    html.Div(
                        dbc.Row(
                            [ 
                                
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="inventory_tacker_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="cancel_button", n_clicks=0, href="/inventory_tracker"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),
                        id="inventory_tracker_buttons_div"
                    ),

                    html.Br(),
                    html.Br(),

                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                            dbc.ModalBody(html.H5(id='inventory_eval_modal_message')),
                            dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="inventory_eval_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id="inventory_eval_modal_confirm", color="success"),
                                    ], 
                            )
                                
                        ],
                        centered=True,
                        id='inventory_eval_modal',
                        backdrop=True,   
                        className="modal-success"    
                    ),

                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3(id="inventory_final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                            dbc.ModalBody(html.H5("Click Proceed to continue.")),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Proceed",
                                    href="/inventory_tracker",
                                    color="success", 
                                ),
                            ),
                        ],
                        centered=True,
                        id='inventory_final_modal',
                        backdrop='static',
                        keyboard=False,
                    ),  
                ],
                width=8,
                style={"marginLeft": "15px"},
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ), 
    ], 
    fluid=True,
)


@app.callback(
    [
        Output('inventory_page_header', 'children'),
        Output('item_staff_responsibile', 'options'),
        Output('item_assigned_to', 'options'),
        Output('inventory_eval_toload', 'data'),
        Output('inventorytracker_removerecord_div', 'style'),
        Output('inventory_tracker_buttons_div', 'style'),
        Output('inventory_tracker_back_btn_div','style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)
def inventory_tracker_loaddropdown(pathname, search):
    if pathname == '/inventory_tracker_management':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]

        sql = """
            SELECT 
                CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS label, 
                user_id AS value
            FROM maindashboard.users u
            WHERE u.user_del_ind = False 
                AND u.user_office = 1
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        staff_responsible_options = df.to_dict('records')

        sql_b = """
            SELECT
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname,1), '. ', u.user_sname, ' ', u.user_suffixname) AS label,
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname,1), '. ', u.user_sname, ' ', u.user_suffixname) AS value
            FROM maindashboard.users u
            WHERE u.user_del_ind = False
            AND u.user_office = 1

            UNION ALL
            SELECT 'Office Use'   AS label, 'Office Use'   AS value
        """
        values_b = []
        cols_b = ['label', 'value']
        df_b = db.querydatafromdatabase(sql_b, values_b, cols_b)
        assigned_to_options = df_b.to_dict('records')
        
        

        if create_mode == 'add':
            header = 'Add Inventory Record'
            to_load = 0
            removediv_style = {'display': 'none'}
            buttondiv_style = None
            backbtn_div_style = {'display': 'none'}
        elif create_mode == 'edit':
            header = 'Edit Inventory Record'
            to_load = 1
            removediv_style = None
            buttondiv_style = None
            backbtn_div_style = {'display': 'none'}
        elif create_mode == 'view':
            header = 'View Inventory Record'
            to_load = 1
            removediv_style = {'display': 'none'}
            buttondiv_style = {'display': 'none'}
            backbtn_div_style = {"display": "flex", "justifyContent": "flex-end"}
    else:
        raise PreventUpdate
    return [header, staff_responsible_options, assigned_to_options, to_load, removediv_style, buttondiv_style, backbtn_div_style]


@app.callback(
    [
        # Check if all fields are filled
        Output('inventory_tracker_alert', 'is_open'),
        Output('inventory_tracker_alert', 'color'),
        Output('inventory_tracker_alert', 'children'),
        Output('item_name', 'className'),
        Output('item_barcode_number', 'className'),
        Output('item_brand', 'className'),
        Output('item_qa_initial_property_no', 'className'),
        Output('item_qa_updated_property_no', 'className'),
        Output('item_description', 'className'),
        Output('item_supplier', 'className'),
        Output('item_po_number', 'className'),
        Output('item_unit_cost', 'className'),
        Output('item_staff_responsibile', 'className'),
        Output('item_assigned_to', 'className'),
        # Confirmation Modals
        Output('inventory_eval_modal', 'is_open'),
        Output('inventory_eval_modal_message', 'children'),
        # Button Colors Change When in Edit Mode
        Output('inventory_eval_modal_confirm', 'color'),
        # Open success modal
        Output('inventory_final_modal', 'is_open'),
        Output('inventory_final_modal_header', 'children'),
    ],
    [
        Input('inventory_tacker_save_button', 'n_clicks'),
        Input('inventory_eval_modal_confirm', 'n_clicks'),
        Input('inventory_eval_modal_cancel', 'n_clicks'),
    ],
    [
        State('inventorytracker_removerecord', 'value'),
        State('item_name', 'value'),
        State('item_image', 'contents'),
        State('item_image', 'filename'),
        State('item_barcode_number', 'value'),
        State('item_brand', 'value'),
        State('item_qa_initial_property_no', 'value'),
        State('item_qa_updated_property_no', 'value'),
        State('item_description', 'value'),
        State('item_supplier', 'value'),
        State('item_po_number', 'value'),
        State('item_company_name', 'value'),
        State('item_company_contact_number', 'value'),
        State('item_company_email', 'value'),
        State('item_unit_cost', 'value'),
        State('item_staff_responsibile', 'value'),
        State('item_assigned_to', 'value'),
        State('url', 'search')
    ]
)
def save_inventory(submit_button, confirm, cancel, removerecord, name, item_image_contents, item_image_filename, barcode, brand, initial_property_no, updated_property_no, description, supplier, 
                   po_number, company_name, contact_number, email, unit_cost,
                 staff_responsible, assigned_to, search):
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    # Set default outputs
    alert_open = False
    alert_color = ''
    alert_text = ''
    name_class = ''
    barcode_class = ''
    brand_class = ''
    initial_property_class = ''
    updated_property_class = ''
    description_class = ''
    supplier_class = ''
    po_number_class = ''
    unit_cost_class = ''
    staff_responsible_class = ''
    assigned_to_class = ''
    confirmation_modal_open = ''
    confirmation_message = ''
    btn_color = 'success'
    final_modal_open = False
    final_modal_header = ''

    # Helper to process file uploads (same as your current helper)
    def process_files(contents, filenames):
        file_data = []
        for content, filename in zip(contents, filenames):
            if content == "1" and filename == "1":
                continue
            try:
                content_type, content_string = content.split(',')
                decoded_content = base64.b64decode(content_string)

                file_path = os.path.join(UPLOAD_DIRECTORY, filename)
                with open(file_path, 'wb') as f:
                    f.write(decoded_content)

                file_info = {
                    "path": file_path,
                    "name": filename,
                    "type": content_type,
                    "size": len(decoded_content),
                }
                file_data.append(file_info)
                
            except Exception as e:
                return None, f'Error processing file: {e}'
        return file_data, None
    
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    if eventid == 'inventory_tacker_save_button' and submit_button:
        # Ensure required fields are filled
        def get_input_class(value):
            return 'red-border' if not value else 'form-control'
        if not all([name, barcode, brand, initial_property_no, description, supplier, po_number, unit_cost, staff_responsible, assigned_to]) and not removerecord:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            name_class= get_input_class(name_class)
            barcode_class= get_input_class(barcode_class)
            brand_class= get_input_class(brand_class)
            initial_property_class= get_input_class(initial_property_class)
            # updated_property_class= get_input_class(updated_property_class)
            description_class= get_input_class(description_class)
            supplier_class= get_input_class(supplier_class)
            po_number_class= get_input_class(po_number_class)
            unit_cost_class= get_input_class(unit_cost_class)
            staff_responsible_class= get_input_class(staff_responsible_class)
            assigned_to_class= get_input_class(assigned_to_class)
        else: # all inputs are valid
            if create_mode == 'add':
                confirmation_modal_open = True
                confirmation_message = "Are you sure you want to add this inventory record?"
            elif create_mode == 'edit':
                confirmation_modal_open = True
                confirmation_message = "Are you sure you want to save changes to this inventory record?"
                if removerecord:
                    confirmation_message = "Are you sure you want to delete this inventory record?"
                    btn_color = 'danger'
    elif eventid == 'inventory_eval_modal_confirm' and confirm:
        if create_mode == 'add':
            # Process each file upload; if a file group is missing, set default values.
            if item_image_contents is None or item_image_filename is None:
                item_image_contents, item_image_filename = ["1"], ["1"]
            item_image_data, error = process_files(item_image_contents, item_image_filename)

            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            sql = """
                SET lc_monetary = 'en_PH.UTF-8';

                INSERT INTO adminteam.inventory_tracker (
                    item_name, 
                    item_image_path, item_image_name, item_image_type, item_image_size,
                    item_barcode_number, item_brand, item_qa_initial_property_no, item_qa_updated_property_no,
                    item_description, item_supplier, item_po_number, item_unit_cost, item_staff_responsibile, item_assigned_to,
                    item_company_name, item_company_contact_number, item_company_email
                )
                VALUES (
                    %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s
                )
            """

            values = (name, 
                      item_image_data[0]["path"] if item_image_data else None, item_image_data[0]["name"] if item_image_data else None,
                      item_image_data[0]["type"] if item_image_data else None, item_image_data[0]["size"] if item_image_data else None,
                      barcode, brand, initial_property_no, updated_property_no,
                      description, supplier, po_number, unit_cost, staff_responsible, assigned_to,
                      company_name, contact_number, email
            )

            try:
                db.modifydatabase(sql, values)
                final_modal_open = True
                final_modal_header = html.H5("Inventory Record Successfully Added.")
            except Exception as e:
                alert_open = True
                alert_color = 'danger'
                alert_text = f'Error copying record: {e}'
        elif create_mode == 'edit': 
            inventory_id = parse_qs(parsed.query).get('id', [None])[0]

            if inventory_id is None:
                    raise PreventUpdate
            
            update_fields = [
                "item_name = %s",
                "item_barcode_number = %s",
                "item_qa_initial_property_no = %s",
                "item_qa_updated_property_no = %s",
                "item_description = %s",
                "item_supplier = %s",
                "item_po_number = %s",
                "item_unit_cost = %s",
                "item_staff_responsibile = %s",
                "item_assigned_to = %s",
                "item_company_name = %s",
                "item_company_contact_number = %s",
                "item_company_email = %s"            
            ]
            values = [
                name, barcode, initial_property_no, updated_property_no, description, supplier, po_number, unit_cost, staff_responsible, assigned_to, company_name, contact_number, email
            ]

            # Now, conditionally add file upload updates:
            if item_image_contents is not None and item_image_contents != ["1"]:
                item_image_data, error = process_files(item_image_contents, item_image_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                update_fields.extend([
                    "item_image_path = %s",
                    "item_image_name = %s",
                    "item_image_type = %s",
                    "item_image_size = %s"
                ])
                values.extend([
                    item_image_data[0]["path"],
                    item_image_data[0]["name"],
                    item_image_data[0]["type"],
                    item_image_data[0]["size"],
                ])
            
            # Finally, add the deletion flag and timestamp
            update_fields.append("item_del_ind = %s")
            update_fields.append("item_timestamp = CURRENT_TIMESTAMP")
            values.append(bool(removerecord))

            # Build the dynamic SQL query
            sqlcode = "UPDATE adminteam.inventory_tracker SET " + ", ".join(update_fields) + " WHERE item_id = %s"
            values.append(inventory_id)

            db.modifydatabase(sqlcode, values)

            final_modal_open = True
            final_modal_header = "Inventory Record Successfully Updated"
        
    elif eventid == 'inventory_eval_modal_cancel' and cancel:
        confirmation_modal_open = False
        confirmation_message = ""
    else:
        raise PreventUpdate
    
    return[alert_open, alert_color, alert_text, name_class, barcode_class, brand_class, initial_property_class, updated_property_class, description_class, supplier_class,
           po_number_class, unit_cost_class, staff_responsible_class, assigned_to_class, confirmation_modal_open, confirmation_message, btn_color, final_modal_open, final_modal_header]

@app.callback(
    [
        Output('item_name', 'value'),
        Output('item_image', 'filename'),
        Output('item_barcode_number', 'value'),
        Output('item_brand', 'value'),
        Output('item_qa_initial_property_no', 'value'),
        Output('item_qa_updated_property_no', 'value'),
        Output('item_description', 'value'),
        Output('item_supplier', 'value'),
        Output('item_po_number', 'value'),
        Output('item_unit_cost', 'value'),
        Output('item_staff_responsibile', 'value'),
        Output('item_assigned_to', 'value'),
        Output('item_company_name', 'value'),
        Output('item_company_contact_number', 'value'),
        Output('item_company_email', 'value'),
    ],
    [  
        Input('inventory_eval_toload', 'modified_timestamp')
    ],
    [
        State('inventory_eval_toload', 'data'),
        State('url', 'search')
    ]
)
def inventorytracker_load(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        load_item_id = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                item_name, item_image_name as item_image, item_barcode_number, item_brand,
                item_qa_initial_property_no, item_qa_updated_property_no, item_description, 
                item_supplier, item_po_number, item_unit_cost, item_staff_responsibile,
                item_assigned_to, item_company_name, item_company_contact_number, item_company_email
            FROM adminteam.inventory_tracker
            WHERE item_id = %s
        """
        values = [load_item_id]

        cols = [
            'item_name', 'item_image',  'item_barcode_number', 'item_brand',
            'item_qa_initial_property_no', 'item_qa_updated_property_no', 'item_description', 
            'item_supplier', 'item_po_number',  'item_unit_cost', 'item_staff_responsibile',
            'item_assigned_to', 'item_company_name', 'item_company_contact_number', 'item_company_email'
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        


        item_name = df['item_name'][0]
        item_image = df['item_image'][0]
        item_barcode_number = df['item_barcode_number'][0]
        item_brand = df['item_brand'][0]
        item_qa_initial_property_no = df['item_qa_initial_property_no'][0]
        item_qa_updated_property_no = df['item_qa_updated_property_no'][0]
        item_description = df['item_description'][0]
        item_supplier = df['item_supplier'][0]
        item_po_number = df['item_po_number'][0]
        raw_cost = df['item_unit_cost'][0]
        clean_cost_str = re.sub(r"[^\d\.]", "", str(raw_cost))
        parts = clean_cost_str.split('.')
        if len(parts) > 2:
            clean_cost_str = parts[0] + '.' + ''.join(parts[1:])
        item_unit_cost = clean_cost_str
        item_staff_responsibile = df['item_staff_responsibile'][0]
        item_assigned_to = df['item_assigned_to'][0]
        item_company_name = df['item_company_name'][0]
        item_company_contact_number = df['item_company_contact_number'][0]
        item_company_email = df['item_company_email'][0]

        return [item_name, item_image, item_barcode_number, item_brand, item_qa_initial_property_no, item_qa_updated_property_no, item_description, item_supplier,
                item_po_number, item_unit_cost, item_staff_responsibile, item_assigned_to, item_company_name, item_company_contact_number, item_company_email]
    else:
        raise PreventUpdate
    
@app.callback(
    [ 
        Output('card_1', 'style'),
        Output('card_2', 'style'),
        Output('card_3', 'style'),
        Output('card_4', 'style'),
    ],
    [
        Input('url', 'search')
    ]
)

def inventory_tracker_disabled(search):

    editable_disabled_style = {
        "background-color": "white",
        "color": "black",
        "opacity": "1",
        "pointer-events": "none"
    }
    card_1 = card_2 = card_3 = card_4 = {}

    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'add':
            pass
        elif create_mode == 'edit':
            pass
        elif create_mode == 'view':
            card_1 = card_2 = card_3 = card_4 = editable_disabled_style

    return[card_1, card_2, card_3, card_4]


@app.callback(
    Output('image_preview', 'src'),
    [
        Input('item_image', 'contents'),
        Input('item_image', 'filename'),
        Input('url', 'search'),
    ]
)
def update_image_preview(contents, filename, search):
    # 1) New upload: show instantly
    if contents:
        # If list, pick first
        if isinstance(contents, list):
            return contents[0]
        return contents

    # 2) No new upload → maybe in view/edit mode?
    if filename and search:
        # Extract mode from URL
        parsed = urlparse(search)
        mode = parse_qs(parsed.query).get('mode', [None])[0]
        if mode in ('view', 'edit'):
            # If multiple filenames, pick first
            fname = filename[0] if isinstance(filename, list) else filename
            # Build the relative assets path (same logic you used in display callback)
            assets_folder = os.path.normpath("./assets")
            upload_relative = os.path.relpath(UPLOAD_DIRECTORY, assets_folder)
            upload_relative = upload_relative.replace(os.path.sep, "/")
            return f"/assets/{upload_relative}/{fname}"

    # 3) Otherwise, do nothing
    return no_update