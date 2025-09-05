import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate
import pandas as pd
import os

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

# Using the corrected path
UPLOAD_DIRECTORY = r".\assets\database\admin\inventory_tracker"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

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
                                    html.H1("INVENTORY TRACKER"),
                                    style={"marginRight": "auto"}  
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Inventory Entry", color="primary", 
                                        href='/inventory_tracker_management?mode=add',
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
                                        "Item Name:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='item_name_filter',
                                        placeholder='Search by Item Name',
                                        className='ml-auto'   
                                    ),
                                    width="4",
                                ),
                                dbc.Col(  
                                    html.Label(
                                        "PO Number:", 
                                        className="form-label", 
                                        style={
                                            "fontSize": "18px", 
                                            "fontWeight": "bold",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='item_po_no_filter',
                                        placeholder='Search by Item PO Number',
                                        className='ml-auto'   
                                    ),
                                    width="4",
                                ),
                            ],
                            className="align-items-center",     
                        ),
                        html.Div(
                            id='equipment_list', 
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
    Output('equipment_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('item_name_filter', 'value'),
        Input('item_po_no_filter', 'value')
    ]
)
def staffprofiles_loaduserlist(pathname, name_filter, po_no_filter):
    if pathname == '/inventory_tracker':
        sql = """  
            SELECT 
                item_id as "ID",
                item_name as "Item Name", 
                item_barcode_number as "S/N Number/ Barcode Number", 
                item_brand as "Brand", 
                item_qa_initial_property_no as "QA Property No.(Initial)",
                item_qa_updated_property_no as "QA Property No. (Updated)", 
                item_description as "Description", 
                item_supplier as "Supplier", 
                item_po_number as "PO Number", 
                item_unit_cost as "Unit Cost",
                CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) as "Staff Responsible", 
                item_assigned_to as "Assigned To"
            FROM adminteam.inventory_tracker it
            JOIN maindashboard.users u on u.user_id = it.item_staff_responsibile
        """
        filters = ["item_del_ind IS FALSE"]
        values = []

        cols = ['ID', 'Item Name', 'S/N Number/ Barcode Number', 'Brand', 'QA Property No.(Initial)', 'QA Property No. (Updated)', 'Description', 
                'Supplier', 'PO Number', 'Unit Cost', 'Staff Responsible', 'Assigned To']

        if name_filter:
            filters.append("it.item_name ILIKE %s")
            values.append(f"%{name_filter}%")

        if po_no_filter:
            filters.append("it.item_po_number ILIKE %s")
            values.append(f"%{po_no_filter}%")

        # Append filters if any exist
        if filters:
            sql += " WHERE " + " AND ".join(filters)

         # Append ORDER BY after filters
        sql += " ORDER BY item_timestamp DESC"

        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty: 
            df["Unit Cost"] = df["Unit Cost"].apply(
                lambda x: f"₱{float(str(x).lstrip('?₱ ').replace(',', '')):,.2f}"
            )

            df["View"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('View', href=f'inventory_tracker_management?mode=view&id={x}', size='sm', color='warning'),
                    style={'text-align': 'center'}
                )
            )
            
            df["Edit"] = df["ID"].apply(
                lambda x: html.Div(
                    dbc.Button('Edit', href=f'inventory_tracker_management?mode=edit&id={x}', size='sm', color='danger'),
                    style={'text-align': 'center'}
                )
            )
            df = df[["Item Name","S/N Number/ Barcode Number","Brand",
                    "QA Property No.(Initial)", "QA Property No. (Updated)", "Description","Supplier",
                    "PO Number", "Unit Cost",
                    "Staff Responsible", "Assigned To",
                    "View", "Edit" ]]
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
        
    return [html.Div("Query could not be processed")]    