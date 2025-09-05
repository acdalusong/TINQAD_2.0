import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, dash_table
from dash import callback_context, no_update

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import base64
import os
from urllib.parse import urlparse, parse_qs

UPLOAD_DIRECTORY = r".\assets\database\admin\staff_profiles"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Define the highlight colors
highlight_colors = {
    'primary': "#0a4323",    # Used for main headers
    'secondary': "#7a0911",  # Used for section titles
    'accent': "#f8b237"      # Accent color for borders and emphasis
}

First_Header = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        id="profile_image",
                        style={
                            "object-fit": "cover",
                            "maxWidth": "2.5in",
                            "maxHeight": "2.5in"
                        },
                        className="rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            dcc.Dropdown(
                                id="user_id",
                                options=[],  # populate as needed
                                placeholder="Select User/Staff",
                                disabled=False,
                            ),
                            dbc.Input(
                                type="text",
                                id="position",
                                disabled=True,
                                style={
                                    "border": "none",
                                    "color": "gray",
                                    "backgroundColor": "transparent",
                                    "opacity": "1",  # override the default reduced opacity
                                },
                            ),
                            dcc.Upload(
                                id="staff_image",
                                children=html.Div([html.A("Upload an Image")]),
                                style={
                                    "width": "auto",
                                    "height": "auto",
                                    "lineHeight": "auto",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px 0",
                                },
                                multiple=True,
                            ),
                            html.H6(
                                "Image Uploaded",
                                id="staff_image_output",
                                className="card-text text-muted",
                            ),
                            html.Small(
                                "save changes to view the most updated submissions",
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3 shadow-lg card-hover",
    style={"maxWidth": "600px"},
)


main_dashboard = dbc.Container(
    [
        First_Header,

        # TABBED NAVIGATION (Anchor Links)
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        dbc.NavLink("Personal Information", href="#personal-info", external_link=True, style={"margin": "0 5px"}),
                        html.Span("|", style={"color": highlight_colors['accent'], "margin": "0 5px"}),
                        dbc.NavLink("Current Address", href="#current-address", external_link=True, style={"margin": "0 5px"}),
                        html.Span("|", style={"color": highlight_colors['accent'], "margin": "0 5px"}),
                        dbc.NavLink("Government Identification Numbers", href="#govt-ids", external_link=True, style={"margin": "0 5px"}),
                        html.Span("|", style={"color": highlight_colors['accent'], "margin": "0 5px"}),
                        dbc.NavLink("Degrees Earned", href="#degrees-earned", external_link=True, style={"margin": "0 5px"}),
                        html.Span("|", style={"color": highlight_colors['accent'], "margin": "0 5px"}),
                        dbc.NavLink("Eligibility", href="#eligibility", external_link=True, style={"margin": "0 5px"}),
                        html.Span("|", style={"color": highlight_colors['accent'], "margin": "0 5px"}),
                        dbc.NavLink("Land Bank Account", href="#landbank-account", external_link=True, style={"margin": "0 5px"}),
                        html.Span("|", style={"color": highlight_colors['accent'], "margin": "0 5px"}),
                        dbc.NavLink("Emergency Contact", href="#emergency-contact", external_link=True, style={"margin": "0 5px"}),
                        html.Span("|", style={"color": highlight_colors['accent'], "margin": "0 5px"}),
                        dbc.NavLink("Orientation/Training Checklist", href="#orientation-checklist", external_link=True, style={"margin": "0 5px"}),
                        html.Span("|", style={"color": highlight_colors['accent'], "margin": "0 5px"}),
                        dbc.NavLink("Resume Information", href="#resume-info", external_link=True, style={"margin": "0 5px"})
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "flexWrap": "wrap"
                    }
                ),
                width=12,
                className="mb-4"
            )
        ),

        # SECTIONS

        # 1. PERSONAL INFORMATION
        dbc.Card(
            id="personal_info",
            children=[
                dbc.CardHeader(
                    "Personal Information",
                    style={
                        "backgroundColor": highlight_colors['secondary'],
                        "color": "white"
                    }
                ),
                dbc.CardBody(
                        [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Last Name"),
                                        dcc.Input(
                                            id="last_name",
                                            disabled = True,
                                            type="text",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("First Name"),
                                        dcc.Input(
                                            id="first_name",
                                            disabled = True,
                                            type="text",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Middle Name"),
                                        dcc.Input(
                                            id="middle_name",
                                            disabled = True,
                                            type="text",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Suffix Name"),
                                        dcc.Input(
                                            id="suffix_name",
                                            disabled = True,
                                            type="text",
                                            placeholder="",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Lived Name"),
                                        dcc.Input(
                                            id="lived_name",
                                            disabled = True,
                                            type="text",
                                            placeholder="",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Date of Birth"),
                                        dcc.Input(
                                            id="date_of_birth",
                                            disabled = True,
                                            type="date",
                                            placeholder="",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Sex at Birth"),
                                        dcc.Input(
                                            id="sex_at_birth",
                                            disabled = True,
                                            type="text",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Place of Birth"),
                                        dcc.Input(
                                            id="place_of_birth",
                                            disabled = True,
                                            type="text",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Blood Type"),
                                        dcc.Input(
                                            id="blood_type",
                                            disabled = True,
                                            type="text",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Preferred Pronouns"),
                                        dcc.Input(
                                            id="preferred_pronouns",
                                            disabled = True,
                                            type="text",
                                            placeholder="",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Email Address"),
                                        dcc.Input(
                                            id="email_address",
                                            disabled = True,
                                            type="email",
                                            placeholder="",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Mobile Number"),
                                        dcc.Input(
                                            id="mobile_number",
                                            disabled = True,
                                            type="text",
                                            placeholder="",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        )
                    ]
                ),
            ],
            className="mb-4"
        ),

        # 2. CURRENT ADDRESS
        dbc.Card(
            id="current_address",
            children=[
                dbc.CardHeader(
                    "Current Address",
                    style={
                        "backgroundColor": highlight_colors['secondary'],
                        "color": "white"
                    }
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Country"),
                                        dcc.Dropdown(
                                            id="country",
                                            options=[],
                                            placeholder="Select Country",
                                            disabled = False,
                                            className="mb-2",
                                            style={"width": "100%"}
                                        ),
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Region"),
                                        dcc.Dropdown(
                                            id="region",
                                            options=[],
                                            placeholder="Select Region",
                                            disabled = False,
                                            className="mb-2",
                                            style={"width": "100%"}
                                        ),
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Province"),
                                        dcc.Dropdown(
                                            id="province",
                                            options=[],
                                            placeholder="Select Province",
                                            disabled = False,
                                            className="mb-2",
                                            style={"width": "100%"}
                                        ),
                                    ],
                                    md=4
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("City/Municipality"),
                                        dcc.Dropdown(
                                            id="municipality",
                                            options=[],
                                            placeholder="Select City/Municipality",
                                            disabled = False,
                                            className="mb-2",
                                            style={"width": "100%"}
                                        ),
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Barangay"),
                                        dcc.Dropdown(
                                            id="barangay",
                                            options=[],
                                            placeholder="Select Barangay",
                                            disabled = False,
                                            className="mb-2",
                                            style={"width": "100%"}
                                        ),
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Subdivision/Village"),
                                        dcc.Input(
                                            id="subdivision",
                                            type="text",
                                            placeholder="Enter Subdivision/Village",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("House Number"),
                                        dcc.Input(
                                            id="house_number",
                                            type="text",
                                            placeholder="Enter House Number",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Street"),
                                        dcc.Input(
                                            id="street",
                                            type="text",
                                            placeholder="Enter Street",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Zip Code"),
                                        dcc.Input(
                                            id="zip_code",
                                            type="text",
                                            placeholder="Enter Zip Code",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        )
                    ]
                )
            ],
            className="mb-4"
        ),

        # 3. GOVERNMENT IDENTIFICATION NUMBERS
        dbc.Card(
            id="govt_ids",
            children=[
                dbc.CardHeader(
                    "Government Identification Numbers",
                    style={
                        "backgroundColor": highlight_colors['secondary'],
                        "color": "white"
                    }
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("GSIS BP No."),
                                        dcc.Input(
                                            id="gsis_bp_no",
                                            type="text",
                                            placeholder="Enter GSIS BP No.",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=3
                                ),
                                dbc.Col(
                                    [
                                        html.Label("PAG-IBIG ID No."),
                                        dcc.Input(
                                            id="pagibig_id_no",
                                            type="text",
                                            placeholder="Enter PAG-IBIG ID No.",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=3
                                ),
                                dbc.Col(
                                    [
                                        html.Label("SSS No."),
                                        dcc.Input(
                                            id="sss_no",
                                            type="text",
                                            placeholder="Enter SSS No.",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=3
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Philhealth No."),
                                        dcc.Input(
                                            id="philhealth_no",
                                            type="text",
                                            placeholder="Enter Philhealth No.",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=3
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("TIN No."),
                                        dcc.Input(
                                            id="tin_no",
                                            type="text",
                                            placeholder="Enter TIN No.",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Government Valid ID"),
                                        dcc.Input(
                                            id="govt_id",
                                            type="text",
                                            placeholder="Enter Valid Government ID",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Government Valid ID No."),
                                        dcc.Input(
                                            id="govt_id_no",
                                            type="text",
                                            placeholder="Enter Valid Government ID No.",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Date of Issuance"),
                                        dcc.DatePickerSingle(
                                            id='govt_id_date_of_issuance',
                                            placeholder="mm/dd/yyyy",
                                            className='SingleDatePicker mb-2',
                                            style={"width": "100%"},
                                        ),
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Place of Issuance"),
                                        dcc.Input(
                                            id="govt_id_place_of_issuance",
                                            type="text",
                                            placeholder="Enter Place of Issuance",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Scanned Copy of Government ID"),
                                        dcc.Upload(
                                            id="govt_id_photo",
                                            children=html.Div(
                                                [
                                                    "Drag and Drop or ",
                                                    html.A("Select a File")
                                                ]
                                            ),
                                            style={
                                                "width": "100%",
                                                "height": "30px",
                                                "lineHeight": "30px",
                                                "borderWidth": "1px",
                                                "borderStyle": "dashed",
                                                "borderRadius": "5px",
                                                "textAlign": "center"
                                            },
                                            multiple=True
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        ),
                        dbc.Row(
                            [dbc.Label("",width=6),
                            dbc.Col(id="govt_id_photo_output", width="auto")],  # Output area for uploaded file names
                            justify="end",
                            className="mt-0",
                        ),
                    ]
                )
            ],
            className="mb-4"
        ),

        # 4. DEGREES EARNED
        dbc.Card(
            id="degrees_earned",
            children=[
                dbc.CardHeader(
                    html.Div(
                        [
                            html.Span("Degrees Earned"),
                            # Button group aligned to the right
                            html.Div(
                                [
                                    dbc.Button("+", id="add_degree_button",
                                            n_clicks=0, size="sm"),
                                    dbc.Button("–", id="remove_degree_button",
                                            n_clicks=0, size="sm", className="ms-2"),
                                ],
                                className="hstack ms-auto align-items-center"
                            ),
                        ],
                        className="d-flex align-items-center"
                    ),
                    style={
                        "backgroundColor": highlight_colors['secondary'],
                        "color": "white"
                    }
                ),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.Div(
                                    children=[
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Label("Degree/s Earned"),
                                                        dcc.Input(
                                                            id="degrees_earned_a",
                                                            type="text",
                                                            placeholder="Enter Degree/s Earned",
                                                            className="mb-2",
                                                            style={"width": "100%"}
                                                        )
                                                    ],
                                                    md=4
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label("University/School"),
                                                        dcc.Input(
                                                            id="university_school_a",
                                                            type="text",
                                                            placeholder="Enter University/School",
                                                            className="mb-2",
                                                            style={"width": "100%"}
                                                        )
                                                    ],
                                                    md=4
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label("Year Obtained"),
                                                        dcc.Input(
                                                            id="year_obtained_a",
                                                            type="number",
                                                            placeholder="Enter Year",
                                                            className="mb-2",
                                                            style={"width": "100%"}
                                                        )
                                                    ],
                                                    md=4
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Label("Degree/s Earned"),
                                                        dcc.Input(
                                                            id="degrees_earned_b",
                                                            type="text",
                                                            placeholder="Enter Degree/s Earned",
                                                            className="mb-2",
                                                            style={"width": "100%"}
                                                        )
                                                    ],
                                                    md=4
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label("University/School"),
                                                        dcc.Input(
                                                            id="university_school_b",
                                                            type="text",
                                                            placeholder="Enter University/School",
                                                            className="mb-2",
                                                            style={"width": "100%"}
                                                        )
                                                    ],
                                                    md=4
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label("Year Obtained"),
                                                        dcc.Input(
                                                            id="year_obtained_b",
                                                            type="number",
                                                            placeholder="Enter Year",
                                                            className="mb-2",
                                                            style={"width": "100%"}
                                                        )
                                                    ],
                                                    md=4
                                                )
                                            ]
                                        )
                                    ],
                                    id="additional_degrees_b",
                                    style={"display": "none"}  # Initially hidden
                                ),
                                html.Div(
                                    children=[
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Label("Degree/s Earned"),
                                                        dcc.Input(
                                                            id="degrees_earned_c",
                                                            type="text",
                                                            placeholder="Enter Degree/s Earned",
                                                            className="mb-2",
                                                            style={"width": "100%"}
                                                        )
                                                    ],
                                                    md=4
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label("University/School"),
                                                        dcc.Input(
                                                            id="university_school_c",
                                                            type="text",
                                                            placeholder="Enter University/School",
                                                            className="mb-2",
                                                            style={"width": "100%"}
                                                        )
                                                    ],
                                                    md=4
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label("Year Obtained"),
                                                        dcc.Input(
                                                            id="year_obtained_c",
                                                            type="number",
                                                            placeholder="Enter Year",
                                                            className="mb-2",
                                                            style={"width": "100%"}
                                                        )
                                                    ],
                                                    md=4
                                                )
                                            ]
                                        )
                                    ],
                                    id="additional_degrees_c",
                                    style={"display": "none"}  # Initially hidden
                                ),
                            ],
                        ),
                    ]
                )
            ],
            className="mb-4"
        ),

        # 5. Eligibility
        dbc.Card(
            id="eligibility",
            children=[
                dbc.CardHeader(
                    "Eligibility",
                    style={
                        "backgroundColor": highlight_colors['secondary'],
                        "color": "white"
                    }
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Eligibility"),
                                        dcc.Input(
                                            id="eligibility_earned",
                                            type="text",
                                            placeholder="Enter Degree/s Earned",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Eligibility Start Date"),
                                        dcc.DatePickerSingle(
                                            id='eligibility_start_date',
                                            placeholder="mm/dd/yyyy",
                                            className='SingleDatePicker mb-2',
                                            style={"width": "100%"},
                                        ),
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Eligibility End Date"),
                                        dcc.DatePickerSingle(
                                            id='eligibility_end_date',
                                            placeholder="mm/dd/yyyy",
                                            className='SingleDatePicker mb-2',
                                            style={"width": "100%"},
                                        ),
                                    ],
                                    md=4
                                )
                            ]
                        )
                    ]
                )
            ],
            className="mb-4"
        ),


        # 5. LAND BANK ACCOUNT
        dbc.Card(
            id="landbank_account",
            children=[
                dbc.CardHeader(
                    "Land Bank Account",
                    style={
                        "backgroundColor": highlight_colors['secondary'],
                        "color": "white"
                    }
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Land Bank Account Number"),
                                        dcc.Input(
                                            id='landbank_account_number',
                                            type="text",
                                            placeholder="Enter Account Number",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=8
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Photo/Image Attachment"),
                                        dcc.Upload(
                                            id="landbank_photo",
                                            children=html.Div(
                                                [
                                                    "Drag and Drop or ",
                                                    html.A("Select a File")
                                                ]
                                            ),
                                            style={
                                                "width": "100%",
                                                "height": "30px",
                                                "lineHeight": "30px",
                                                "borderWidth": "1px",
                                                "borderStyle": "dashed",
                                                "borderRadius": "5px",
                                                "textAlign": "center"
                                            },
                                            multiple=True
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        ),
                        dbc.Row(
                            [dbc.Label("",width=6),
                            dbc.Col(id="landbank_photo_output", width="auto")],  # Output area for uploaded file names
                            justify="end",
                            className="mt-0",
                        ),
                    ]
                )
            ],
            className="mb-4"
        ),

        # 6. EMERGENCY CONTACT
        dbc.Card(
            id="emergency_contact",
            children=[
                dbc.CardHeader(
                    "Emergency Contact",
                    style={
                        "backgroundColor": highlight_colors['secondary'],
                        "color": "white"
                    }
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Name of Emergency Contact"),
                                        dcc.Input(
                                            id="emergency_contact_name",
                                            type="text",
                                            placeholder="Enter Name",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Contact Number"),
                                        dcc.Input(
                                            id="emergency_contact_number",
                                            type="text",
                                            placeholder="Enter Contact Number",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Address"),
                                        dcc.Input(
                                            id="emergency_contact_address",
                                            type="text",
                                            placeholder="Enter Address",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        )
                    ]
                )
            ],
            className="mb-4"
        ),

        # 7. ORIENTATION/TRAINING CHECKLIST
        dbc.Card(
            id="orientation_checklist",
            children=[
                dbc.CardHeader(
                    "Orientation/Training Checklist",
                    style={
                        "backgroundColor": highlight_colors['secondary'],
                        "color": "white"
                    }
                ),
                dbc.CardBody(
                    [
                        dbc.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [
                                            html.Th("ORIENTATION/TRAINING CHECKLIST", style={"width": "25%"}),
                                            html.Th("Attachments", style={"width": "25%"}),
                                            html.Th("Date of Training"),
                                            html.Th("Link to Certificate", style={"width": "35%"})
                                        ],
                                        style={
                                            "backgroundColor": highlight_colors['accent'],
                                            "color": "white"
                                        }
                                    )
                                ),
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Td("Onboarding with Administrative Team"),
                                                html.Td(
                                                    [
                                                        dcc.Upload(
                                                            id="ob_w_admin",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A("Select a File")
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "30px",
                                                                "lineHeight": "30px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center"
                                                            },
                                                            multiple=True
                                                        ),
                                                        html.Div(id="ob_w_admin_output")
                                                    ]
                                                ),
                                                html.Td(
                                                    dcc.DatePickerSingle(
                                                        id='ob_date_w_admin',
                                                        placeholder="mm/dd/yyyy",
                                                        className='SingleDatePicker mb-2',
                                                        style={"width": "100%"},
                                                    ),
                                                ),
                                                html.Td(
                                                    dcc.Input(
                                                        id="link_ob_w_admin",
                                                        type="text",
                                                        placeholder="Certificate URL",
                                                        style={"width": "100%"}
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Onboarding with Home Team"),
                                                html.Td(
                                                    [
                                                        dcc.Upload(
                                                            id="ob_w_home_team",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A("Select a File")
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "30px",
                                                                "lineHeight": "30px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center"
                                                            },
                                                            multiple=True
                                                        ),
                                                        html.Div(id="ob_w_home_team_output")
                                                    ]
                                                ),
                                                html.Td(
                                                    dcc.DatePickerSingle(
                                                        id='ob_date_w_home',
                                                        placeholder="mm/dd/yyyy",
                                                        className='SingleDatePicker mb-2',
                                                        style={"width": "100%"},
                                                    ),
                                                ),
                                                html.Td(
                                                    dcc.Input(
                                                        id="link_ob_w_home",
                                                        type="text",
                                                        placeholder="Certificate URL",
                                                        style={"width": "100%"}
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Gender and Sensitivity Training"),
                                                html.Td(
                                                    [
                                                        dcc.Upload(
                                                            id="gender_sensitivity_training",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A("Select a File")
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "30px",
                                                                "lineHeight": "30px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center"
                                                            },
                                                            multiple=True
                                                        ),
                                                        html.Div(id="gender_sensitivity_training_output")
                                                    ]
                                                ),
                                                html.Td(
                                                    dcc.DatePickerSingle(
                                                        id='gender_sensitivity_date',
                                                        placeholder="mm/dd/yyyy",
                                                        className='SingleDatePicker mb-2',
                                                        style={"width": "100%"},
                                                    ),
                                                ),
                                                html.Td(
                                                    dcc.Input(
                                                        id="link_gender_sensitivity",
                                                        type="text",
                                                        placeholder="Certificate URL",
                                                        style={"width": "100%"}
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Gender and Development Training"),
                                                html.Td(
                                                    [
                                                        dcc.Upload(
                                                            id="gender_dev_training",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A("Select a File")
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "30px",
                                                                "lineHeight": "30px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center"
                                                            },
                                                            multiple=True
                                                        ),
                                                        html.Div(id="gender_dev_training_output")
                                                    ]
                                                ),
                                                html.Td(
                                                    dcc.DatePickerSingle(
                                                        id='gender_dev_training_date',
                                                        placeholder="mm/dd/yyyy",
                                                        className='SingleDatePicker mb-2',
                                                        style={"width": "100%"},
                                                    ),
                                                ),
                                                html.Td(
                                                    dcc.Input(
                                                        id="link_gender_dev_training",
                                                        type="text",
                                                        placeholder="Certificate URL",
                                                        style={"width": "100%"}
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("[OPEN UP] Fundamental Concepts in Integrity and Service Delivery in Government"),
                                                html.Td(
                                                    [
                                                        dcc.Upload(
                                                            id="open_up_fcisdg",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A("Select a File")
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "30px",
                                                                "lineHeight": "30px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center"
                                                            },
                                                            multiple=True
                                                        ),
                                                        html.Div(id="open_up_fcisdg_output")
                                                    ]
                                                ),
                                                html.Td(
                                                    dcc.DatePickerSingle(
                                                        id='open_up_fcisdg_date',
                                                        placeholder="mm/dd/yyyy",
                                                        className='SingleDatePicker mb-2',
                                                        style={"width": "100%"},
                                                    ),
                                                ),
                                                html.Td(
                                                    dcc.Input(
                                                        id="link_open_up_fcisdg",
                                                        type="text",
                                                        placeholder="Certificate URL",
                                                        style={"width": "100%"}
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("[OPEN UP] Processing of Personal Information"),
                                                html.Td(
                                                    [
                                                        dcc.Upload(
                                                            id="open_up_ppi",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A("Select a File")
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "30px",
                                                                "lineHeight": "30px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center"
                                                            },
                                                            multiple=True
                                                        ),
                                                        html.Div(id="open_up_ppi_output")
                                                    ]
                                                ),
                                                html.Td(
                                                    dcc.DatePickerSingle(
                                                        id='open_up_ppi_date',
                                                        placeholder="mm/dd/yyyy",
                                                        className='SingleDatePicker mb-2',
                                                        style={"width": "100%"},
                                                    ),
                                                ),
                                                html.Td(
                                                    dcc.Input(
                                                        id="link_open_up_ppi",
                                                        type="text",
                                                        placeholder="Certificate URL",
                                                        style={"width": "100%"}
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("[OPEN UP] Introduction to Workplace Safety and Health"),
                                                html.Td(
                                                    [
                                                        dcc.Upload(
                                                            id="open_up_iwsh",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A("Select a File")
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "30px",
                                                                "lineHeight": "30px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center"
                                                            },
                                                            multiple=True
                                                        ),
                                                        html.Div(id="open_up_iwsh_output")
                                                    ]
                                                ),
                                                html.Td(
                                                    dcc.DatePickerSingle(
                                                        id='open_up_iwsh_date',
                                                        placeholder="mm/dd/yyyy",
                                                        className='SingleDatePicker mb-2',
                                                        style={"width": "100%"},
                                                    ),
                                                ),
                                                html.Td(
                                                    dcc.Input(
                                                        id="link_open_up_iwsh",
                                                        type="text",
                                                        placeholder="Certificate URL",
                                                        style={"width": "100%"}
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("[OPEN UP] Introduction to UP Anti-Sexual Harassment Policy"),
                                                html.Td(
                                                    [
                                                        dcc.Upload(
                                                            id="open_up_ashp",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A("Select a File")
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "30px",
                                                                "lineHeight": "30px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center"
                                                            },
                                                            multiple=True
                                                        ),
                                                        html.Div(id="open_up_ashp_output")
                                                    ]
                                                ),
                                                html.Td(
                                                    dcc.DatePickerSingle(
                                                        id='open_up_ashp_date',
                                                        placeholder="mm/dd/yyyy",
                                                        className='SingleDatePicker mb-2',
                                                        style={"width": "100%"},
                                                    ),
                                                ),
                                                html.Td(
                                                    dcc.Input(
                                                        id="link_open_up_ashp",
                                                        type="text",
                                                        placeholder="Certificate URL",
                                                        style={"width": "100%"}
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Others:"),
                                                html.Td(
                                                    [
                                                        dcc.Upload(
                                                            id="others_orientation_trainings",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A("Select a File")
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "30px",
                                                                "lineHeight": "30px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center"
                                                            },
                                                            multiple=True
                                                        ),
                                                        html.Div(id="others_orientation_trainings_output")
                                                    ]
                                                ),
                                                html.Td(
                                                    dcc.DatePickerSingle(
                                                        id='others_orientation_trainings_date',
                                                        placeholder="mm/dd/yyyy",
                                                        className='SingleDatePicker mb-2',
                                                        style={"width": "100%"},
                                                    ),
                                                ),
                                                html.Td(
                                                    dcc.Input(
                                                        id="link_others_orientation_trainings",
                                                        type="text",
                                                        placeholder="Certificate URL",
                                                        style={"width": "100%"}
                                                    )
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ],
                            bordered=True,
                            hover=True,
                            responsive=True,
                            striped=True
                        )
                    ]
                )
            ],
            className="mb-4"
        ),

        # 8. RESUME INFORMATION
        dbc.Card(
            id="resume_info",
            children=[
                dbc.CardHeader(
                    "Resume Information",
                    style={
                        "backgroundColor": highlight_colors['secondary'],
                        "color": "white"
                    }
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("CURRICULUM VITAE"),
                                        dcc.Upload(
                                            id="upload_resume_file",
                                            children=html.Div(
                                                [
                                                    "Drag and Drop or ",
                                                    html.A("Select a File")
                                                ]
                                            ),
                                            style={
                                                "width": "100%",
                                                "height": "30px",
                                                "lineHeight": "30px",
                                                "borderWidth": "1px",
                                                "borderStyle": "dashed",
                                                "borderRadius": "5px",
                                                "textAlign": "center"
                                            },
                                            multiple=True
                                        ),
                                        html.Div(id="upload_resume_file_output"),
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Date of Last Update"),
                                        dcc.DatePickerSingle(
                                            id='resume_last_update',
                                            placeholder="mm/dd/yyyy",
                                            className='SingleDatePicker mb-2',
                                            style={"width": "100%"},
                                        ),
                                    ],
                                    md=4
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Link to CV"),
                                        dcc.Input(
                                            id="cv_link",
                                            type="text",
                                            placeholder="CV URL",
                                            className="mb-2",
                                            style={"width": "100%"}
                                        )
                                    ],
                                    md=4
                                )
                            ]
                        )
                    ]
                )
            ],
            className="mb-5"
        )
    ],
    fluid=True
)



# Callback to display the names of the uploaded files
@app.callback(
    Output("staff_image_output", "children"),
    [Input("staff_image", "filename"),
     Input("url", "search")]
)
def display_staff_image(filenames, search):
    if not filenames:
        return "No files uploaded."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)


@app.callback(
    Output("govt_id_photo_output", "children"),
    [Input("govt_id_photo", "filename"),
     Input('url', 'search'),]
)
def display_govt_id_photo_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)


# Callback to display the names of the uploaded files
@app.callback(
    Output("landbank_photo_output", "children"),
    [Input("landbank_photo", "filename"),
     Input('url', 'search'),]
)
def display_landbank_photo_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)


@app.callback(
    Output("ob_w_admin_output", "children"),
    [Input("ob_w_admin", "filename"),
     Input('url', 'search'),]
)
def display_ob_w_admin_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)


@app.callback(
    Output("ob_w_home_team_output", "children"),
    [Input("ob_w_home_team", "filename"),
     Input('url', 'search'),]
)
def display_ob_w_home_team_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)

@app.callback(
    Output("gender_sensitivity_training_output", "children"),
    [Input("gender_sensitivity_training", "filename"),
     Input('url', 'search'),]
)
def display_gender_sensitivity_training_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)

@app.callback(
    Output("gender_dev_training_output", "children"),
    [Input("gender_dev_training", "filename"),
     Input('url', 'search'),]
)
def display_gender_dev_training_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)

@app.callback(
    Output("open_up_fcisdg_output", "children"),
    [Input("open_up_fcisdg", "filename"),
     Input('url', 'search'),]
)
def display_open_up_fcisdg_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)

@app.callback(
    Output("open_up_ppi_output", "children"),
    [Input("open_up_ppi", "filename"),
     Input('url', 'search'),]
)
def display_open_up_ppi_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)

@app.callback(
    Output("open_up_iwsh_output", "children"),
    [Input("open_up_iwsh", "filename"),
     Input('url', 'search'),]
)
def display_open_up_iwsh_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)


@app.callback(
    Output("open_up_ashp_output", "children"),
    [Input("open_up_ashp", "filename"),
     Input('url', 'search'),]
)
def display_open_up_ashp_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)

@app.callback(
    Output("others_orientation_trainings_output", "children"),
    [Input("others_orientation_trainings", "filename"),
     Input('url', 'search'),]
)
def display_others_orientation_trainings_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)

@app.callback(
    Output("upload_resume_file_output", "children"),
    [Input("upload_resume_file", "filename"),
     Input('url', 'search'),]
)
def display_upload_resume_file(filenames, search):
    if not filenames:
        return "No files uploaded. Compress files first if uploading multiple items."
    
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
        return [build_file_message(fname) for fname in filenames]
    else:
        return build_file_message(filenames)

layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                [
                    html.Div(  
                            [
                                dcc.Store(id='to_load', storage_type='memory', data=0),
                                dcc.Store(id='loaded_country', storage_type='memory'),
                                dcc.Store(id='loaded_region', storage_type='memory'),
                                dcc.Store(id='loaded_province', storage_type='memory'),
                                dcc.Store(id='loaded_municipality', storage_type='memory'),
                                dcc.Store(id='loaded_barangay', storage_type='memory'),
                                dcc.Store(id='degree_count', data=0, storage_type='memory'),
                            ]
                    ),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H1(id="page_header"),
                                        width=8
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            "Back",
                                            color="success",
                                            href="/staff_profiles"
                                        ),
                                        width=4,
                                        id="staff_profiles_back_btn_div",
                                        style={"display": "flex", "justifyContent": "flex-end"}
                                    )
                                ],
                                align="center"
                            ),
                        ],
                        className="mb-0"
                    ),
                    html.Hr(),
                    main_dashboard, 
                    html.Br(),   
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Label("Wish to delete?", width=4),
                                dbc.Col(
                                    dbc.Checklist(
                                        id='remove_record',
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
                        id='remove_record_div'
                    ),

                    html.Br(),
                    dbc.Alert(id='alert', is_open=False), # For feedback purpose
                    html.Div(
                        dbc.Row(
                            [ 
                                
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="cancel_button", n_clicks=0, href="/staff_profiles"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),
                        id="staff_profiles_buttons_div"
                    ),
                    
                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                            dbc.ModalBody(
                                html.H5(id='initial_modal_message'),
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button("Cancel", id= "initial_modal_cancel", color="warning"),
                                    dbc.Button("Confirm", id= "initial_modal_confirm", color="success")
                                ]
                            ),
                        ],
                        centered=True,
                        id="initial_modal",
                        backdrop=True,
                        className="modal-success",
                    ),

                    # Final Modal for Training Documents
                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H3(id='last_modal_header'), close_button=False, className="bg-success", style={"color": "white"}),
                            dbc.ModalBody(
                                html.H5("Click Proceed to continue"),
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button("Proceed", href='/staff_profiles', color="success"),
                                ]
                            ),
                        ],
                        centered=True,
                        id="last_modal",
                        backdrop="static",
                        className="modal-success",
                    ), 
                     
                ],
                width=9, style={'marginLeft': '15px'}
                
                )
            ]
        ),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ),
    ],
)

@app.callback(
    Output('degree_count', 'data'),
    [
        Input('url', 'pathname'),
        Input('url', 'search'),
        Input('add_degree_button', 'n_clicks'),
        Input('remove_degree_button', 'n_clicks'),
    ],
    State('degree_count', 'data'),
)
def update_degree_count(pathname, search, add_clicks, remove_clicks, current_count):
    # Determine who triggered us
    trigger = callback_context.triggered_id

    # Parse mode from URL once
    qs   = urlparse(search or "").query
    mode = parse_qs(qs).get('mode', ['add'])[0]
    staff_id = parse_qs(qs).get('id', [None])[0]


    # ---- B) BUTTON CLICKS (after initial) ----
    # Ensure we have an integer
    count = int(current_count or 0)

    # Add one extra, up to 2
    if trigger == 'add_degree_button':
        return min(count + 1, 2)

    # Remove one extra, down to 0
    if trigger == 'remove_degree_button':
        return max(count - 1, 0)

    else:
        sql = """
            SELECT COUNT(*) AS c
            FROM adminteam.staff_degrees
            WHERE staff_profile_id = %s
        """
        df = db.querydatafromdatabase(sql, [staff_id], ['c'])
        # subtract 1 so that count=0 means just the “base” degree
        loaded = max(int(df['c'][0]) - 1, 0)
        return loaded
        
    
@app.callback(
    Output('additional_degrees_b', 'style'),
    Output('additional_degrees_c', 'style'),
    Input('degree_count', 'data'),
)
def display_additional_degrees(count):
    style_b = {"display": "block"} if count >= 1 else {"display": "none"}
    style_c = {"display": "block"} if count >= 2 else {"display": "none"}
    return style_b, style_c


@app.callback(
    [
        Output('user_id', 'options'),
        Output('country', 'options'),
        Output('page_header', 'children'),
        Output('to_load', 'data'),
        Output('remove_record_div', 'style'),
        Output('staff_profiles_buttons_div', 'style'),
        Output('staff_profiles_back_btn_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)


def registeruser_loaddropdown(pathname, search):
    if pathname == '/staff_profiles_management':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]

        base_sql = """
            SELECT 
                CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS label, 
                user_id AS value
            FROM maindashboard.users u
            WHERE u.user_del_ind = False 
                AND u.user_office = 1
        """
        if create_mode == 'add':
            # In add mode, exclude all users that already have a profile
            sql = base_sql + """
              AND u.user_id NOT IN (
                    SELECT staff_user_id 
                    FROM adminteam.staff_profiles 
                    WHERE staff_del_ind = False
              )
            """
            values = []
        elif create_mode == 'edit' or create_mode == 'view':
            # In edit mode, get the current staff_profile_id from query string
            staff_profile_id = parse_qs(parsed.query).get('id', [None])[0]
            if not staff_profile_id:
                raise PreventUpdate

            # Retrieve the current staff_user_id for this record
            sql_current = """
                SELECT staff_user_id 
                FROM adminteam.staff_profiles 
                WHERE staff_profile_id = %s
            """
            current_record = db.querydatafromdatabase(sql_current, [staff_profile_id], ['staff_user_id'])
            if len(current_record.index) == 0:
                raise PreventUpdate
            current_user_id = int(current_record['staff_user_id'][0])

            # Exclude all users with profiles except for the one currently selected
            sql = base_sql + """
              AND (
                  u.user_id NOT IN (
                        SELECT staff_user_id 
                        FROM adminteam.staff_profiles 
                        WHERE staff_del_ind = False
                  )
                  OR u.user_id = %s
              )
            """
            values = [current_user_id]
        else:
            raise PreventUpdate

        df = db.querydatafromdatabase(sql, values, ['label', 'value'])
        user_options = df.to_dict('records')


        sql_b = """
            SELECT 
            country_name AS label, 
            country_id AS value
            FROM public.countries
        """
        values_b = []
        cols_b = ['label', 'value']
        df_b = db.querydatafromdatabase(sql_b, values_b, cols_b)
        country_options = df_b.to_dict('records')

        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]

        if create_mode == 'add':
            header = "Add a Staff Profile Data" 
            to_load = 0
            removediv_style = {'display': 'none'}
            button_style = {'display': 'flex', 'justifyContent': 'flex-end'}
            staff_profiles_back_btn_div_style = {'display': 'none'}
        elif create_mode == 'edit':
            header = "Staff Profile Data Editing"
            to_load = 1
            removediv_style = None
            button_style = {'display': 'flex', 'justifyContent': 'flex-end'}
            staff_profiles_back_btn_div_style = {'display': 'none'}
        elif create_mode == 'view':
            header = "Staff Profile Data Viewing"
            to_load = 1
            removediv_style = {'display': 'none'}
            button_style = {'display': 'none'}
            staff_profiles_back_btn_div_style = {'display': 'flex', 'justifyContent': 'flex-end'}

    else:
        raise PreventUpdate
    return [user_options, country_options, header, to_load, removediv_style, button_style, staff_profiles_back_btn_div_style]
    


@app.callback(
    [
        Output('position', 'value'),
        Output('last_name', 'value'),
        Output('first_name', 'value'),
        Output('middle_name', 'value'),
        Output('suffix_name', 'value'),
        Output('lived_name', 'value'),
        Output('date_of_birth', 'value'),
        Output('sex_at_birth', 'value'),
        Output('place_of_birth', 'value'),
        Output('blood_type', 'value'),
        Output('preferred_pronouns', 'value'),
        Output('email_address', 'value'),
        Output('mobile_number', 'value'),
    ],
    Input('user_id', 'value'), 
)
def populate_personal_information(selected_user):
    if not selected_user:  # Simplified None check
        return dash.no_update
    elif selected_user:
        sql = """
            SELECT user_position, user_sname, user_fname, user_mname, user_suffixname, user_livedname, user_bday, user_sexatbirth, user_placeofbirth, user_bloodtype,
            user_preferredpronouns, user_email, user_phone_num
            FROM maindashboard.users
            WHERE user_id = %s
        """
        values = [selected_user]
        cols = [
            'user_position', 'user_sname' , 'user_fname', 'user_mname', 'user_suffixname', 'user_livedname', 'user_bday', 'user_sexatbirth', 'user_placeofbirth', 'user_bloodtype',
            'user_preferredpronouns', 'user_email', 'user_phone_num'
        ]
        df = db.querydatafromdatabase(sql, values, cols)
            
        user_position = df['user_position'][0]
        user_sname = df['user_sname'][0]
        user_fname = df['user_fname'][0]
        user_mname = df['user_mname'][0]
        user_suffixname = df['user_suffixname'][0]
        user_livedname = df['user_livedname'][0]
        user_bday = df['user_bday'][0]
        user_sexatbirth = df['user_sexatbirth'][0]
        user_placeofbirth = df['user_placeofbirth'][0]
        user_bloodtype = df['user_bloodtype'][0]
        user_preferredpronouns = df['user_preferredpronouns'][0]
        user_email = df['user_email'][0]
        user_phone_num = df['user_phone_num'][0]

        return [
            user_position, user_sname, user_fname, user_mname, user_suffixname, user_livedname, user_bday, user_sexatbirth, user_placeofbirth, user_bloodtype,
            user_preferredpronouns, user_email, user_phone_num
            ]
    else:
        raise PreventUpdate
        

#region dropdown
@app.callback(
    Output('region', 'options'),
    Input('country', 'value')
)
def populate_college_dropdown(selected_country):
    if selected_country is None:
        return []  
    
    try: 
        sql = """
        SELECT region_description as label,  region_id  as value
        FROM public.regions
        WHERE country_id = %s
        """
        values = [selected_country]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        region_options = df.to_dict('records')
        return region_options
    
    except Exception as e: 
        return [] 
    
#province dropdown
@app.callback(
    Output('province', 'options'),
    Input('region', 'value')
)
def populate_college_dropdown(selected_region):
    if selected_region is None:
        return []  
    
    try: 
        sql = """
        SELECT province_name as label,  province_id  as value
        FROM public.provinces
        WHERE region_id = %s
        """
        values = [selected_region]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        province_options = df.to_dict('records')
        return province_options
    
    except Exception as e: 
        return [] 
    
#municipality dropdown
@app.callback(
    Output('municipality', 'options'),
    Input('province', 'value')
)
def populate_college_dropdown(selected_province):
    if selected_province is None:
        return []  
    
    try: 
        sql = """
        SELECT municipality_name as label,  municipality_id  as value
        FROM public.municipalities
        WHERE province_id = %s
        """
        values = [selected_province]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        municipality_options = df.to_dict('records')
        return municipality_options
    
    except Exception as e: 
        return [] 
    
#barangay dropdown
@app.callback(
    Output('barangay', 'options'),
    Input('municipality', 'value')
)
def populate_college_dropdown(selected_municipality):
    if selected_municipality is None:
        return []  
    
    try: 
        sql = """
        SELECT barangay_name as label,  barangay_id  as value
        FROM public.barangays
        WHERE municipality_id = %s
        """
        values = [selected_municipality]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        barangay_options = df.to_dict('records')
        return barangay_options
    
    except Exception as e: 
        return [] 

@app.callback(
    [
        # Check if all fields are filled
        Output('alert', 'is_open'),
        Output('alert', 'color'),
        Output('alert', 'children'),
        Output('initial_modal', 'is_open'),
        Output('initial_modal_message', 'children'),
        Output('initial_modal_confirm', 'color'),
        Output('last_modal', 'is_open'),
        Output('last_modal_header', 'children'),
        Output('user_id', 'className'),
        Output('country', 'className'),
        Output('region', 'className'),
        Output('province', 'className'),
        Output('municipality', 'className'),
        Output('barangay', 'className'),
        Output('zip_code', 'className'),
        Output('philhealth_no', 'className'),
        Output('tin_no', 'className'),
        Output('govt_id', 'className'),
        Output('govt_id_no', 'className'),
        Output('emergency_contact_name', 'className'),
        Output('emergency_contact_number', 'className'),
        Output('emergency_contact_address', 'className')
    ],
    [
        Input('save_button', 'n_clicks'),
        Input('initial_modal_cancel', 'n_clicks'),
        Input('initial_modal_confirm', 'n_clicks'),
    ],
    [
        State('remove_record', 'value'),
        State('url', 'search'),
        State('user_id', 'value'),
        State('country', 'value'),
        State('region', 'value'),
        State('province', 'value'),
        State('municipality', 'value'),
        State('barangay', 'value'),
        State('subdivision', 'value'),
        State('house_number', 'value'),
        State('street', 'value'),
        State('zip_code', 'value'),
        State('gsis_bp_no', 'value'),
        State('pagibig_id_no', 'value'),
        State('sss_no', 'value'),
        State('philhealth_no', 'value'),
        State('tin_no', 'value'),
        State('govt_id', 'value'),
        State('govt_id_no', 'value'),
        State('govt_id_date_of_issuance', 'date'),
        State('govt_id_place_of_issuance', 'value'),

        State('govt_id_photo', 'contents'),
        State('govt_id_photo', 'filename'),

        State('degrees_earned_a', 'value'),
        State('university_school_a', 'value'),
        State('year_obtained_a', 'value'),
        State('degrees_earned_b', 'value'),
        State('university_school_b', 'value'),
        State('year_obtained_b', 'value'),
        State('degrees_earned_c', 'value'),
        State('university_school_c', 'value'),
        State('year_obtained_c', 'value'),
        
        State('eligibility_earned', 'value'),
        State('eligibility_start_date', 'date'),
        State('eligibility_end_date', 'date'),
        State('landbank_account_number', 'value'),

        State('landbank_photo', 'contents'),
        State('landbank_photo', 'filename'),

        State('emergency_contact_name', 'value'),
        State('emergency_contact_number', 'value'),
        State('emergency_contact_address', 'value'),
        State('ob_date_w_admin', 'date'),
        
        State('ob_w_admin', 'contents'),
        State('ob_w_admin', 'filename'),

        State('link_ob_w_admin', 'value'),

        State('ob_date_w_home', 'date'),

        State('ob_w_home_team', 'contents'),
        State('ob_w_home_team', 'filename'),

        State('link_ob_w_home', 'value'),
        State('gender_sensitivity_date', 'date'),

        State('gender_sensitivity_training', 'contents'),
        State('gender_sensitivity_training', 'filename'),

        State('link_gender_sensitivity', 'value'),

        State('gender_dev_training_date', 'date'),

        State('gender_dev_training', 'contents'),
        State('gender_dev_training', 'filename'),

        State('link_gender_dev_training', 'value'),

        State('open_up_fcisdg_date', 'date'),

        State('open_up_fcisdg', 'contents'),
        State('open_up_fcisdg', 'filename'),

        State('link_open_up_fcisdg', 'value'),

        State('open_up_ppi_date', 'date'),

        State('open_up_ppi', 'contents'),
        State('open_up_ppi', 'filename'),

        State('link_open_up_ppi', 'value'),
        
        State('open_up_iwsh_date', 'date'),

        State('open_up_iwsh', 'contents'),
        State('open_up_iwsh', 'filename'),

        State('link_open_up_iwsh', 'value'),

        State('open_up_ashp_date', 'date'),

        State('open_up_ashp', 'contents'),
        State('open_up_ashp', 'filename'),

        State('link_open_up_ashp', 'value'),

        State('others_orientation_trainings_date', 'date'),

        State('others_orientation_trainings', 'contents'),
        State('others_orientation_trainings', 'filename'),

        State('link_others_orientation_trainings', 'value'),

        
        State('upload_resume_file', 'contents'),
        State('upload_resume_file', 'filename'),
        State('resume_last_update', 'date'),
        State('cv_link', 'value'),
        State('staff_image', 'contents'),
        State('staff_image', 'filename'),
    ],
)

def save_staff_profile(submitbtn, cancelbtn, confirmbtn, remove_record, search, user_id, country, region, province, municipality, barangay, subdivision, house_number, street, zip_code,
                       gsis_bp_no, pagibig_id_no, sss_no, philhealth_no, tin_no, govt_id, govt_id_no, govt_id_date_of_issuance, govt_id_place_of_issuance,
                       govt_id_photo_contents, govt_id_photo_filename,
                       degrees_earned_a, university_school_a, year_obtained_a, degrees_earned_b, university_school_b, year_obtained_b, degrees_earned_c, university_school_c, year_obtained_c,
                       eligibility_earned, eligibility_start_date, eligibility_end_date,
                       landbank_account_number, 
                       landbank_photo_contents, landbank_photo_filename,
                       emergency_contact_name, emergency_contact_number, emergency_contact_address,
                       ob_date_w_admin, 
                       ob_w_admin_contents, ob_w_admin_filename,
                       link_ob_w_admin, 
                       ob_date_w_home, 
                       ob_w_home_team_contents, ob_w_home_team_filename,
                       link_ob_w_home, 
                       gender_sensitivity_date, 
                       gender_sensitivity_training_contents, gender_sensitivity_training_filename,
                       link_gender_sensitivity, 
                       gender_dev_training_date, 
                       gender_dev_training_contents, gender_dev_training_filename,
                       link_gender_dev_training, 
                       open_up_fcisdg_date,
                       open_up_fcisdg_contents, open_up_fcisdg_filename,
                       link_open_up_fcisdg, 
                       open_up_ppi_date, 
                       open_up_ppi_contents, open_up_ppi_filename,
                       link_open_up_ppi, 
                       open_up_iwsh_date, 
                       open_up_iwsh_contents, open_up_iwsh_filename,
                       link_open_up_iwsh, 
                       open_up_ashp_date,
                       open_up_ashp_contents, open_up_ashp_filename,
                       link_open_up_ashp, 
                       others_orientation_trainings_date, 
                       others_orientation_trainings_contents, others_orientation_trainings_filename,
                       link_others_orientation_trainings, 
                       upload_resume_file_contents, upload_resume_file_filename,
                       resume_last_update,
                       cv_link,
                       staff_image_contents, staff_image_filename
                       ):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]
    
    # Set default outputs
    alert_open = False
    alert_color = ''
    alert_text = ''
    initial_modal_open = False
    initial_modal_message = ""
    btn_color = 'success'
    last_modal_open = False
    last_modal_header = ""
    user_id_class = ""
    country_class = ""
    region_class = ""
    province_class = ""
    municipality_class = ""
    barangay_class = ""
    zip_code_class = ""
    philhealth_no_class = ""
    tin_no_class = ""
    govt_id_class = ""
    govt_id_no_class = ""
    emergency_contact_name_class = ""
    emergency_contact_number_class = ""
    emergency_contact_address_class = ""

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

    if eventid == 'save_button' and submitbtn:
        def get_input_class_sp(value):
            return 'red-border' if not value else 'form-control'
        required_fields = [user_id, country, region, province, municipality, barangay, zip_code, philhealth_no, tin_no, govt_id, govt_id_no,
                           emergency_contact_name, emergency_contact_number, emergency_contact_address]
        
        if not all(required_fields) and not remove_record:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Please fill out missing required fields.'
            user_id_class= 'red-border' if not user_id else ''
            country_class= 'red-border' if not country else ''
            region_class= 'red-border' if not region else ''
            province_class= 'red-border' if not province else ''
            municipality_class= 'red-border' if not municipality else ''
            barangay_class= 'red-border' if not barangay else ''
            zip_code_class= get_input_class_sp(zip_code)
            philhealth_no_class= get_input_class_sp(philhealth_no)
            tin_no_class= get_input_class_sp(tin_no)
            govt_id_class= get_input_class_sp(govt_id)
            govt_id_no_class= get_input_class_sp(govt_id_no)
            emergency_contact_name_class= get_input_class_sp(emergency_contact_name)
            emergency_contact_number_class= get_input_class_sp(emergency_contact_number)
            emergency_contact_address_class= get_input_class_sp(emergency_contact_address)

        else: # all inputs are valid
            if create_mode == 'add':
                initial_modal_open = True
                initial_modal_message  = "Are you sure you want to add this staff profile entry?"
            elif create_mode == 'edit':
                if remove_record:
                    initial_modal_open = True
                    initial_modal_message = "Are you sure you want to delete this staff profile entry?"
                    btn_color = 'danger'
                else:
                    initial_modal_open = True
                    initial_modal_message = "Are you sure you want to update this staff profile entry?"
    elif eventid == 'initial_modal_confirm' and confirmbtn:
        if create_mode == 'add':
            # Process each file upload; if a file group is missing, set default values.
            if govt_id_photo_contents is None or govt_id_photo_filename is None:
                govt_id_photo_contents, govt_id_photo_filename = ["1"], ["1"]
            govt_id_photo_data, error = process_files(govt_id_photo_contents, govt_id_photo_filename)

            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if landbank_photo_contents is None or landbank_photo_filename is None:
                landbank_photo_contents, landbank_photo_filename = ["1"], ["1"]
            landbank_photo_data, error = process_files(landbank_photo_contents, landbank_photo_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if ob_w_admin_contents is None or ob_w_admin_filename is None:
                ob_w_admin_contents, ob_w_admin_filename = ["1"], ["1"]
            ob_w_admin_data, error = process_files(ob_w_admin_contents, ob_w_admin_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error
            
            if ob_w_home_team_contents is None or ob_w_home_team_filename is None:
                ob_w_home_team_contents, ob_w_home_team_filename = ["1"], ["1"]
            ob_w_home_team_data, error = process_files(ob_w_home_team_contents, ob_w_home_team_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if gender_sensitivity_training_contents is None or gender_sensitivity_training_filename is None:
                gender_sensitivity_training_contents, gender_sensitivity_training_filename = ["1"], ["1"]
            gender_sensitivity_training_data, error = process_files(gender_sensitivity_training_contents, gender_sensitivity_training_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error
            
            if gender_dev_training_contents is None or gender_dev_training_filename is None:
                gender_dev_training_contents, gender_dev_training_filename = ["1"], ["1"]
            gender_dev_training_data, error = process_files(gender_dev_training_contents, gender_dev_training_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if open_up_fcisdg_contents is None or open_up_fcisdg_filename is None:
                open_up_fcisdg_contents, open_up_fcisdg_filename = ["1"], ["1"]
            open_up_fcisdg_data, error = process_files(open_up_fcisdg_contents, open_up_fcisdg_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if open_up_ppi_contents is None or open_up_ppi_filename is None:
                open_up_ppi_contents, open_up_ppi_filename = ["1"], ["1"]
            open_up_ppi_data, error = process_files(open_up_ppi_contents, open_up_ppi_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if open_up_iwsh_contents is None or open_up_iwsh_filename is None:
                open_up_iwsh_contents, open_up_iwsh_filename = ["1"], ["1"]
            open_up_iwsh_data, error = process_files(open_up_iwsh_contents, open_up_iwsh_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if open_up_ashp_contents is None or open_up_ashp_filename is None:
                open_up_ashp_contents, open_up_ashp_filename = ["1"], ["1"]
            open_up_ashp_data, error = process_files(open_up_ashp_contents, open_up_ashp_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if others_orientation_trainings_contents is None or others_orientation_trainings_filename is None:
                others_orientation_trainings_contents, others_orientation_trainings_filename = ["1"], ["1"]
            others_orientation_trainings_data, error = process_files(others_orientation_trainings_contents, others_orientation_trainings_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if upload_resume_file_contents is None or upload_resume_file_filename is None:
                upload_resume_file_contents, upload_resume_file_filename = ["1"], ["1"]
            upload_resume_file_data, error = process_files(upload_resume_file_contents, upload_resume_file_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            if staff_image_contents is None or staff_image_filename is None:
                staff_image_contents, staff_image_filename = ["1"], ["1"]
            staff_image_data, error = process_files(staff_image_contents, staff_image_filename)
            if error:
                alert_open = True
                alert_color = 'danger'
                alert_text = error

            insert_profile_sql = """
                INSERT INTO adminteam.staff_profiles(
                    staff_user_id, staff_country, staff_region, staff_province, staff_municipality, staff_barangay, staff_subdivision, staff_house_number, staff_street, staff_zip_code,
                    staff_gsis, staff_pag_ibig, staff_sss, staff_philhealth, staff_tin, staff_govt_id, staff_govt_number, govt_id_date_of_issuance, govt_id_place_of_issuance,
                    govt_id_photo_path, govt_id_photo_name, govt_id_photo_type, govt_id_photo_size,
                    staff_eligibility, staff_eligibility_start, staff_eligibility_end,
                    staff_landbank_acct_num, 
                    landbank_photo_path, landbank_photo_name, landbank_photo_type, landbank_photo_size,
                    staff_emgcy_contact_name, staff_emgcy_contact_number, staff_emgcy_contact_address,
                    ob_w_admin_date, 
                    ob_w_admin_path, ob_w_admin_name, ob_w_admin_type, ob_w_admin_size,
                    ob_w_admin_link, 
                    ob_w_home_team_date, 
                    ob_w_home_team_path, ob_w_home_team_name, ob_w_home_team_type, ob_w_home_team_size,
                    ob_w_home_team_link, 
                    gender_sensitivity_training_date, 
                    gender_sensitivity_training_path, gender_sensitivity_training_name, gender_sensitivity_training_type, gender_sensitivity_training_size,
                    gender_sensitivity_training_link,
                    gender_dev_training_date, 
                    gender_dev_training_path, gender_dev_training_name, gender_dev_training_type, gender_dev_training_size,
                    gender_dev_training_link, 
                    open_up_fcisdg_date,
                    open_up_fcisdg_path, open_up_fcisdg_name, open_up_fcisdg_type, open_up_fcisdg_size, 
                    open_up_fcisdg_link, 
                    open_up_ppi_date,
                    open_up_ppi_path, open_up_ppi_name, open_up_ppi_type, open_up_ppi_size,
                    open_up_ppi_link,
                    open_up_iwsh_date,
                    open_up_iwsh_path, open_up_iwsh_name, open_up_iwsh_type, open_up_iwsh_size,
                    open_up_iwsh_link, 
                    open_up_ashp_date, 
                    open_up_ashp_path, open_up_ashp_name, open_up_ashp_type, open_up_ashp_size,
                    open_up_ashp_link, 
                    others_orientation_trainings_date, 
                    others_orientation_trainings_path, others_orientation_trainings_name, others_orientation_trainings_type, others_orientation_trainings_size,
                    others_orientation_trainings_link,
                    staff_cv_path, staff_cv_name, staff_cv_type, staff_cv_size,
                    staff_cv_update,
                    staff_cv_link,
                    staff_image_path, staff_image_name, staff_image_type, staff_image_size
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, 
                    %s, %s, %s, %s, 
                    %s, %s, %s, 
                    %s,
                    %s, %s, %s, %s, 
                    %s,
                    %s,
                    %s, %s, %s, %s,
                    %s,
                    %s,
                    %s, %s, %s, %s,
                    %s,
                    %s,
                    %s, %s, %s, %s,
                    %s,
                    %s,
                    %s, %s, %s, %s,
                    %s,
                    %s,
                    %s, %s, %s, %s,
                    %s,
                    %s,
                    %s, %s, %s, %s,
                    %s,
                    %s,
                    %s, %s, %s, %s,
                    %s,
                    %s,
                    %s, %s, %s, %s,
                    %s,
                    %s, %s, %s, %s,
                    %s,
                    %s,
                    %s, %s, %s, %s
                )
                RETURNING staff_profile_id;
            """

            profile_vals = (user_id, country, region, province, municipality, barangay, subdivision, house_number, street, zip_code, 
                    gsis_bp_no, pagibig_id_no, sss_no, philhealth_no, tin_no, govt_id, govt_id_no, govt_id_date_of_issuance, govt_id_place_of_issuance,
                    govt_id_photo_data[0]["path"] if govt_id_photo_data else None, govt_id_photo_data[0]["name"] if govt_id_photo_data else None,
                    govt_id_photo_data[0]["type"] if govt_id_photo_data else None, govt_id_photo_data[0]["size"] if govt_id_photo_data else None,
                    eligibility_earned, eligibility_start_date, eligibility_end_date,
                    landbank_account_number,
                    landbank_photo_data[0]["path"] if landbank_photo_data else None, landbank_photo_data[0]["name"] if landbank_photo_data else None,
                    landbank_photo_data[0]["type"] if landbank_photo_data else None, landbank_photo_data[0]["size"] if landbank_photo_data else None, 
                    emergency_contact_name, emergency_contact_number, emergency_contact_address,
                    ob_date_w_admin, 
                    ob_w_admin_data[0]["path"] if ob_w_admin_data else None, ob_w_admin_data[0]["name"] if ob_w_admin_data else None,
                    ob_w_admin_data[0]["type"] if ob_w_admin_data else None, ob_w_admin_data[0]["size"] if ob_w_admin_data else None,
                    link_ob_w_admin, 
                    ob_date_w_home, 
                    ob_w_home_team_data[0]["path"] if ob_w_home_team_data else None, ob_w_home_team_data[0]["name"] if ob_w_home_team_data else None,
                    ob_w_home_team_data[0]["type"] if ob_w_home_team_data else None, ob_w_home_team_data[0]["size"] if ob_w_home_team_data else None,
                    link_ob_w_home, 
                    gender_sensitivity_date, 
                    gender_sensitivity_training_data[0]["path"] if gender_sensitivity_training_data else None, gender_sensitivity_training_data[0]["name"] if gender_sensitivity_training_data else None,
                    gender_sensitivity_training_data[0]["type"] if gender_sensitivity_training_data else None, gender_sensitivity_training_data[0]["size"] if gender_sensitivity_training_data else None,
                    link_gender_sensitivity,
                    gender_dev_training_date, 
                    gender_dev_training_data[0]["path"] if gender_dev_training_data else None, gender_dev_training_data[0]["name"] if gender_dev_training_data else None,
                    gender_dev_training_data[0]["type"] if gender_dev_training_data else None, gender_dev_training_data[0]["size"] if gender_dev_training_data else None,
                    link_gender_dev_training, 
                    open_up_fcisdg_date, 
                    open_up_fcisdg_data[0]["path"] if open_up_fcisdg_data else None, open_up_fcisdg_data[0]["name"] if open_up_fcisdg_data else None,
                    open_up_fcisdg_data[0]["type"] if open_up_fcisdg_data else None, open_up_fcisdg_data[0]["size"] if open_up_fcisdg_data else None,
                    link_open_up_fcisdg, 
                    open_up_ppi_date, 
                    open_up_ppi_data[0]["path"] if open_up_ppi_data else None, open_up_ppi_data[0]["name"] if open_up_ppi_data else None,
                    open_up_ppi_data[0]["type"] if open_up_ppi_data else None, open_up_ppi_data[0]["size"] if open_up_ppi_data else None,
                    link_open_up_ppi, 
                    open_up_iwsh_date, 
                    open_up_iwsh_data[0]["path"] if open_up_iwsh_data else None, open_up_iwsh_data[0]["name"] if open_up_iwsh_data else None,
                    open_up_iwsh_data[0]["type"] if open_up_iwsh_data else None, open_up_iwsh_data[0]["size"] if open_up_iwsh_data else None,
                    link_open_up_iwsh, 
                    open_up_ashp_date,
                    open_up_ashp_data[0]["path"] if open_up_ashp_data else None, open_up_ashp_data[0]["name"] if open_up_ashp_data else None,
                    open_up_ashp_data[0]["type"] if open_up_ashp_data else None, open_up_ashp_data[0]["size"] if open_up_ashp_data else None, 
                    link_open_up_ashp, 
                    others_orientation_trainings_date, 
                    others_orientation_trainings_data[0]["path"] if others_orientation_trainings_data else None, others_orientation_trainings_data[0]["name"] if others_orientation_trainings_data else None,
                    others_orientation_trainings_data[0]["type"] if others_orientation_trainings_data else None, others_orientation_trainings_data[0]["size"] if others_orientation_trainings_data else None,
                    link_others_orientation_trainings,
                    upload_resume_file_data[0]["path"] if upload_resume_file_data else None, upload_resume_file_data[0]["name"] if upload_resume_file_data else None,
                    upload_resume_file_data[0]["type"] if upload_resume_file_data else None, upload_resume_file_data[0]["size"] if upload_resume_file_data else None,
                    resume_last_update, 
                    cv_link,
                    staff_image_data[0]["path"] if staff_image_data else None, staff_image_data[0]["name"] if staff_image_data else None,
                    staff_image_data[0]["type"] if staff_image_data else None, staff_image_data[0]["size"] if staff_image_data else None
            )
             
            new_id_df = db.execute_returning(insert_profile_sql, profile_vals, ['staff_profile_id'])
            if new_id_df.empty:
                raise PreventUpdate
            staff_profile_id = int(new_id_df['staff_profile_id'][0])
            
            # After staff_profile_id is known:
            degree_inserts = []
            degree_sql = """
                INSERT INTO adminteam.staff_degrees
                (staff_profile_id, degree, school, year_obtained)
                VALUES (%s, %s, %s, %s)
            """
            # Collect triplets from inputs
            degree_rows = [
                (degrees_earned_a, university_school_a, year_obtained_a),
                (degrees_earned_b, university_school_b, year_obtained_b),
                (degrees_earned_c, university_school_c, year_obtained_c),
            ]
            for deg, school, year in degree_rows:
                if deg:  # only if user filled
                    degree_inserts.append((staff_profile_id, deg, school or '', year or None))

            # Batch-insert all
            for vals in degree_inserts:
                db.modifydatabase(degree_sql, vals)

            last_modal_open = True
            last_modal_header = "Staff Profile Successfully Added"

        elif create_mode == 'edit':
            staffprofilesid = parse_qs(parsed.query).get('id', [None])[0]
            if staffprofilesid is None:
                raise PreventUpdate

            # Start with the base update fields that are always updated
            update_fields = [
                "staff_country = %s",
                "staff_region = %s",
                "staff_province = %s",
                "staff_municipality = %s",
                "staff_barangay = %s",
                "staff_subdivision = %s",
                "staff_house_number = %s",
                "staff_street = %s",
                "staff_zip_code = %s",
                "staff_gsis = %s",
                "staff_pag_ibig = %s",
                "staff_sss = %s",
                "staff_philhealth = %s",
                "staff_tin = %s",
                "staff_govt_id = %s",
                "staff_govt_number = %s",
                "govt_id_date_of_issuance = %s",
                "govt_id_place_of_issuance = %s",
                "staff_eligibility = %s",
                "staff_eligibility_start = %s",
                "staff_eligibility_end = %s",
                "staff_landbank_acct_num = %s",
                "staff_emgcy_contact_name = %s",
                "staff_emgcy_contact_number = %s",
                "staff_emgcy_contact_address = %s",
                "ob_w_admin_date = %s",
                "ob_w_admin_link = %s",
                "ob_w_home_team_date = %s",
                "ob_w_home_team_link = %s",
                "gender_sensitivity_training_date = %s",
                "gender_sensitivity_training_link = %s",
                "gender_dev_training_date = %s",
                "gender_dev_training_link = %s",
                "open_up_fcisdg_date = %s",
                "open_up_fcisdg_link = %s",
                "open_up_ppi_date = %s",
                "open_up_ppi_link = %s",
                "open_up_iwsh_date = %s",
                "open_up_iwsh_link = %s",
                "open_up_ashp_date = %s",
                "open_up_ashp_link = %s",
                "others_orientation_trainings_date = %s",
                "others_orientation_trainings_link = %s",
                "staff_cv_update = %s",
                "staff_cv_link = %s"
            ]
            values = [
                country, region, province, municipality, barangay, subdivision, house_number, street, zip_code,
                gsis_bp_no, pagibig_id_no, sss_no, philhealth_no, tin_no, govt_id, govt_id_no, govt_id_date_of_issuance, govt_id_place_of_issuance,
                eligibility_earned, eligibility_start_date, eligibility_end_date,
                landbank_account_number, emergency_contact_name, emergency_contact_number, emergency_contact_address,
                ob_date_w_admin, link_ob_w_admin, ob_date_w_home, link_ob_w_home,
                gender_sensitivity_date, link_gender_sensitivity, gender_dev_training_date, link_gender_dev_training,
                open_up_fcisdg_date, link_open_up_fcisdg, open_up_ppi_date, link_open_up_ppi,
                open_up_iwsh_date, link_open_up_iwsh, open_up_ashp_date, link_open_up_ashp,
                others_orientation_trainings_date, link_others_orientation_trainings,
                resume_last_update, cv_link
            ]

            # Now, conditionally add file upload updates:
            # Example for govt_id_photu:
            if govt_id_photo_contents is not None and govt_id_photo_contents != ["1"]:
                govt_id_photo_data, error = process_files(govt_id_photo_contents, govt_id_photo_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "govt_id_photo_path = %s",
                    "govt_id_photo_name = %s",
                    "govt_id_photo_type = %s",
                    "govt_id_photo_size = %s"
                ])
                values.extend([
                    govt_id_photo_data[0]["path"],
                    govt_id_photo_data[0]["name"],
                    govt_id_photo_data[0]["type"],
                    govt_id_photo_data[0]["size"],
                ])

            if landbank_photo_contents is not None and landbank_photo_contents != ["1"]:
                landbank_photo_data, error = process_files(landbank_photo_contents, landbank_photo_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "landbank_photo_path = %s",
                    "landbank_photo_name = %s",
                    "landbank_photo_type = %s",
                    "landbank_photo_size = %s"
                ])
                values.extend([
                    landbank_photo_data[0]["path"],
                    landbank_photo_data[0]["name"],
                    landbank_photo_data[0]["type"],
                    landbank_photo_data[0]["size"],
                ])

            # For ob_w_admin:
            if ob_w_admin_contents is not None and ob_w_admin_contents != ["1"]:
                ob_w_admin_data, error = process_files(ob_w_admin_contents, ob_w_admin_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "ob_w_admin_path = %s",
                    "ob_w_admin_name = %s",
                    "ob_w_admin_type = %s",
                    "ob_w_admin_size = %s"
                ])
                values.extend([
                    ob_w_admin_data[0]["path"],
                    ob_w_admin_data[0]["name"],
                    ob_w_admin_data[0]["type"],
                    ob_w_admin_data[0]["size"],
                ])

            # For ob_w_home_team:
            if ob_w_home_team_contents is not None and ob_w_home_team_contents != ["1"]:
                ob_w_home_team_data, error = process_files(ob_w_home_team_contents, ob_w_home_team_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "ob_w_home_team_path = %s",
                    "ob_w_home_team_name = %s",
                    "ob_w_home_team_type = %s",
                    "ob_w_home_team_size = %s"
                ])
                values.extend([
                    ob_w_home_team_data[0]["path"],
                    ob_w_home_team_data[0]["name"],
                    ob_w_home_team_data[0]["type"],
                    ob_w_home_team_data[0]["size"],
                ])

            # For gender_sensitivity_training:
            if gender_sensitivity_training_contents is not None and gender_sensitivity_training_contents != ["1"]:
                gender_sensitivity_training_data, error = process_files(gender_sensitivity_training_contents, gender_sensitivity_training_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "gender_sensitivity_training_path = %s",
                    "gender_sensitivity_training_name = %s",
                    "gender_sensitivity_training_type = %s",
                    "gender_sensitivity_training_size = %s"
                ])
                values.extend([
                    gender_sensitivity_training_data[0]["path"],
                    gender_sensitivity_training_data[0]["name"],
                    gender_sensitivity_training_data[0]["type"],
                    gender_sensitivity_training_data[0]["size"],
                ])

            # For gender_dev_training:
            if gender_dev_training_contents is not None and gender_dev_training_contents != ["1"]:
                gender_dev_training_data, error = process_files(gender_dev_training_contents, gender_dev_training_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "gender_dev_training_path = %s",
                    "gender_dev_training_name = %s",
                    "gender_dev_training_type = %s",
                    "gender_dev_training_size = %s"
                ])
                values.extend([
                    gender_dev_training_data[0]["path"],
                    gender_dev_training_data[0]["name"],
                    gender_dev_training_data[0]["type"],
                    gender_dev_training_data[0]["size"],
                ])

            # For open_up_fcisdg:
            if open_up_fcisdg_contents is not None and open_up_fcisdg_contents != ["1"]:
                open_up_fcisdg_data, error = process_files(open_up_fcisdg_contents, open_up_fcisdg_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "open_up_fcisdg_path = %s",
                    "open_up_fcisdg_name = %s",
                    "open_up_fcisdg_type = %s",
                    "open_up_fcisdg_size = %s"
                ])
                values.extend([
                    open_up_fcisdg_data[0]["path"],
                    open_up_fcisdg_data[0]["name"],
                    open_up_fcisdg_data[0]["type"],
                    open_up_fcisdg_data[0]["size"],
                ])

            # For open_up_ppi:
            if open_up_ppi_contents is not None and open_up_ppi_contents != ["1"]:
                open_up_ppi_data, error = process_files(open_up_ppi_contents, open_up_ppi_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "open_up_ppi_path = %s",
                    "open_up_ppi_name = %s",
                    "open_up_ppi_type = %s",
                    "open_up_ppi_size = %s"
                ])
                values.extend([
                    open_up_ppi_data[0]["path"],
                    open_up_ppi_data[0]["name"],
                    open_up_ppi_data[0]["type"],
                    open_up_ppi_data[0]["size"],
                ])

            # For open_up_iwsh:
            if open_up_iwsh_contents is not None and open_up_iwsh_contents != ["1"]:
                open_up_iwsh_data, error = process_files(open_up_iwsh_contents, open_up_iwsh_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "open_up_iwsh_path = %s",
                    "open_up_iwsh_name = %s",
                    "open_up_iwsh_type = %s",
                    "open_up_iwsh_size = %s"
                ])
                values.extend([
                    open_up_iwsh_data[0]["path"],
                    open_up_iwsh_data[0]["name"],
                    open_up_iwsh_data[0]["type"],
                    open_up_iwsh_data[0]["size"],
                ])

            # For open_up_ashp:
            if open_up_ashp_contents is not None and open_up_ashp_contents != ["1"]:
                open_up_ashp_data, error = process_files(open_up_ashp_contents, open_up_ashp_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "open_up_ashp_path = %s",
                    "open_up_ashp_name = %s",
                    "open_up_ashp_type = %s",
                    "open_up_ashp_size = %s"
                ])
                values.extend([
                    open_up_ashp_data[0]["path"],
                    open_up_ashp_data[0]["name"],
                    open_up_ashp_data[0]["type"],
                    open_up_ashp_data[0]["size"],
                ])

            # For others_orientation_trainings:
            if others_orientation_trainings_contents is not None and others_orientation_trainings_contents != ["1"]:
                others_orientation_trainings_data, error = process_files(others_orientation_trainings_contents, others_orientation_trainings_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "others_orientation_trainings_path = %s",
                    "others_orientation_trainings_name = %s",
                    "others_orientation_trainings_type = %s",
                    "others_orientation_trainings_size = %s"
                ])
                values.extend([
                    others_orientation_trainings_data[0]["path"],
                    others_orientation_trainings_data[0]["name"],
                    others_orientation_trainings_data[0]["type"],
                    others_orientation_trainings_data[0]["size"],
                ])

            # For upload_resume_file:
            if upload_resume_file_contents is not None and upload_resume_file_contents != ["1"]:
                upload_resume_file_data, error = process_files(upload_resume_file_contents, upload_resume_file_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "staff_cv_path = %s",
                    "staff_cv_name = %s",
                    "staff_cv_type = %s",
                    "staff_cv_size = %s"
                ])
                values.extend([
                    upload_resume_file_data[0]["path"],
                    upload_resume_file_data[0]["name"],
                    upload_resume_file_data[0]["type"],
                    upload_resume_file_data[0]["size"],
                ])

            # For staff_image:
            if staff_image_contents is not None and staff_image_contents != ["1"]:
                staff_image_data, error = process_files(staff_image_contents, staff_image_filename)
                if error:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = error
                    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header]
                update_fields.extend([
                    "staff_image_path = %s",
                    "staff_image_name = %s",
                    "staff_image_type = %s",
                    "staff_image_size = %s"
                ])
                values.extend([
                    staff_image_data[0]["path"],
                    staff_image_data[0]["name"],
                    staff_image_data[0]["type"],
                    staff_image_data[0]["size"],
                ])

            # Finally, add the deletion flag and timestamp
            update_fields.append("staff_del_ind = %s")
            update_fields.append("staff_timestamp = CURRENT_TIMESTAMP")
            values.append(bool(remove_record))

            # Build the dynamic SQL query
            sqlcode = "UPDATE adminteam.staff_profiles SET " + ", ".join(update_fields) + " WHERE staff_profile_id = %s"
            values.append(staffprofilesid)

            db.modifydatabase(sqlcode, values)

            # 0) Remove old degrees for this profile
            del_sql = "DELETE FROM adminteam.staff_degrees WHERE staff_profile_id = %s"
            db.modifydatabase(del_sql, [staffprofilesid])

            degree_sql = """
                INSERT INTO adminteam.staff_degrees
                (staff_profile_id, degree, school, year_obtained)
                VALUES (%s, %s, %s, %s)
            """

            # 1) Re-insert degrees exactly as above
            degree_rows = [
                (degrees_earned_a, university_school_a, year_obtained_a),
                (degrees_earned_b, university_school_b, year_obtained_b),
                (degrees_earned_c, university_school_c, year_obtained_c),
            ]
            for deg, school, year in degree_rows:
                if deg:
                    db.modifydatabase(degree_sql, [staffprofilesid, deg, school or '', year or None])

            last_modal_open = True
            last_modal_header = "Staff Profile Successfully Updated"
    
    elif eventid == 'initial_modal_cancel' and cancelbtn:
        initial_modal_open = False
        initial_modal_message = ""

    return [alert_open, alert_color, alert_text, initial_modal_open, initial_modal_message, btn_color, last_modal_open, last_modal_header, 
            user_id_class, country_class, region_class, province_class, municipality_class, barangay_class, zip_code_class,
            philhealth_no_class, tin_no_class, govt_id_class, govt_id_no_class, emergency_contact_name_class, emergency_contact_number_class, emergency_contact_address_class]

@app.callback(
    [
        Output('user_id', 'value'),
        Output('loaded_country', 'data'),
        Output('loaded_region', 'data'),
        Output('loaded_province', 'data'),
        Output('loaded_municipality', 'data'),
        Output('loaded_barangay', 'data'),
        Output('subdivision', 'value'),
        Output('house_number', 'value'),
        Output('street', 'value'),
        Output('zip_code', 'value'),
        Output('gsis_bp_no', 'value'),
        Output('pagibig_id_no', 'value'),
        Output('sss_no', 'value'),
        Output('philhealth_no', 'value'),
        Output('tin_no', 'value'),
        Output('govt_id', 'value'),
        Output('govt_id_no', 'value'),
        Output('govt_id_date_of_issuance', 'date'),
        Output('govt_id_place_of_issuance', 'value'),
        Output('govt_id_photo', 'filename'),
        Output('eligibility_earned', 'value'),
        Output('eligibility_start_date', 'date'),
        Output('eligibility_end_date', 'date'),
        Output('landbank_account_number', 'value'),
        Output('landbank_photo', 'filename'),
        Output('emergency_contact_name', 'value'),
        Output('emergency_contact_number', 'value'),
        Output('emergency_contact_address', 'value'),
        Output('ob_date_w_admin', 'date'),
        Output('ob_w_admin', 'filename'),
        Output('link_ob_w_admin', 'value'),
        Output('ob_date_w_home', 'date'),
        Output('ob_w_home_team', 'filename'),
        Output('link_ob_w_home', 'value'),
        Output('gender_sensitivity_date', 'date'),
        Output('gender_sensitivity_training', 'filename'),
        Output('link_gender_sensitivity', 'value'),
        Output('gender_dev_training_date', 'date'),
        Output('gender_dev_training', 'filename'),
        Output('link_gender_dev_training', 'value'),
        Output('open_up_fcisdg_date', 'date'),
        Output('open_up_fcisdg', 'filename'),
        Output('link_open_up_fcisdg', 'value'),
        Output('open_up_ppi_date', 'date'),
        Output('open_up_ppi', 'filename'),
        Output('link_open_up_ppi', 'value'),
        Output('open_up_iwsh_date', 'date'),
        Output('open_up_iwsh', 'filename'),
        Output('link_open_up_iwsh', 'value'),
        Output('open_up_ashp_date', 'date'),
        Output('open_up_ashp', 'filename'),
        Output('link_open_up_ashp', 'value'),
        Output('others_orientation_trainings_date', 'date'),
        Output('others_orientation_trainings', 'filename'),
        Output('link_others_orientation_trainings', 'value'),
        Output('upload_resume_file', 'filename'),
        Output('resume_last_update', 'date'),
        Output('cv_link', 'value'),
        Output('staff_image', 'filename'),
        Output('degrees_earned_a', 'value'),
        Output('university_school_a', 'value'),
        Output('year_obtained_a', 'value'),
        Output('degrees_earned_b', 'value'),
        Output('university_school_b', 'value'),
        Output('year_obtained_b', 'value'),
        Output('degrees_earned_c', 'value'),
        Output('university_school_c', 'value'),
        Output('year_obtained_c', 'value'),
    ],
    [  
        Input('to_load', 'modified_timestamp')
    ],
    [
        State('to_load', 'data'),
        State('url', 'search')
    ]
)


def staff_profiles_load(timestamp, to_load, search):
    if to_load:
        parsed = urlparse(search)
        staff_profile_id = parse_qs(parsed.query)['id'][0]
        if not staff_profile_id:
            raise PreventUpdate
        
        sql = """
            SELECT 
                staff_user_id, staff_country, staff_region, staff_province, staff_municipality, staff_barangay, staff_subdivision, staff_house_number, staff_street, staff_zip_code,
                staff_gsis, staff_pag_ibig, staff_sss, staff_philhealth, staff_tin, staff_govt_id, staff_govt_number, govt_id_date_of_issuance, govt_id_place_of_issuance,
                govt_id_photo_name as govt_id_photo,
                staff_eligibility, staff_eligibility_start, staff_eligibility_end,
                staff_landbank_acct_num, 
                landbank_photo_name as landbank_photo, 
                staff_emgcy_contact_name, staff_emgcy_contact_number, staff_emgcy_contact_address,
                ob_w_admin_date, 
                ob_w_admin_name as ob_w_admin, 
                ob_w_admin_link, 
                ob_w_home_team_date, 
                ob_w_home_team_name as ob_w_home_team,
                ob_w_home_team_link, 
                gender_sensitivity_training_date, 
                gender_sensitivity_training_name as gender_sensitivity_training,
                gender_sensitivity_training_link,
                gender_dev_training_date, 
                gender_dev_training_name as gender_dev_training,
                gender_dev_training_link, 
                open_up_fcisdg_date,
                open_up_fcisdg_name as open_up_fcisdg, 
                open_up_fcisdg_link, 
                open_up_ppi_date,
                open_up_ppi_name as open_up_ppi,
                open_up_ppi_link,
                open_up_iwsh_date,
                open_up_iwsh_name as open_up_iwsh, 
                open_up_iwsh_link, 
                open_up_ashp_date, 
                open_up_ashp_name as open_up_ashp, 
                open_up_ashp_link, 
                others_orientation_trainings_date, 
                others_orientation_trainings_name as others_orientation_trainings, 
                others_orientation_trainings_link,
                staff_cv_name as staff_cv,
                staff_cv_update,
                staff_cv_link,
                staff_image_name as staff_image_name
            FROM adminteam.staff_profiles
            WHERE staff_profile_id = %s
        """
        values = [staff_profile_id]

        cols = [
            'staff_user_id', 'staff_country', 'staff_region', 'staff_province', 'staff_municipality', 'staff_barangay', 'staff_subdivision', 'staff_house_number', 'staff_street', 'staff_zip_code',
            'staff_gsis', 'staff_pag_ibig', 'staff_sss', 'staff_philhealth', 'staff_tin', 'staff_govt_id', 'staff_govt_number', 'govt_id_date_of_issuance', 'govt_id_place_of_issuance',
            'govt_id_photo',
            'staff_eligibility', 'staff_eligibility_start', 'staff_eligibility_end',
            'staff_landbank_acct_num', 
            'landbank_photo',
            'staff_emgcy_contact_name', 'staff_emgcy_contact_number', 'staff_emgcy_contact_address',
            'ob_w_admin_date', 
            'ob_w_admin',
            'ob_w_admin_link', 
            'ob_w_home_team_date', 
            'ob_w_home_team',
            'ob_w_home_team_link', 
            'gender_sensitivity_training_date', 
            'gender_sensitivity_training',
            'gender_sensitivity_training_link',
            'gender_dev_training_date', 
            'gender_dev_training',
            'gender_dev_training_link', 
            'open_up_fcisdg_date',
            'open_up_fcisdg',  
            'open_up_fcisdg_link', 
            'open_up_ppi_date',
            'open_up_ppi',
            'open_up_ppi_link',
            'open_up_iwsh_date',
            'open_up_iwsh', 
            'open_up_iwsh_link', 
            'open_up_ashp_date', 
            'open_up_ashp',
            'open_up_ashp_link', 
            'others_orientation_trainings_date', 
            'others_orientation_trainings', 
            'others_orientation_trainings_link',
            'staff_cv',
            'staff_cv_update',
            'staff_cv_link',
            'staff_image_name'
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        staff_user_id = df['staff_user_id'][0]
        staff_country = int(df['staff_country'][0])
        staff_region = int(df['staff_region'][0])
        staff_province = int(df['staff_province'][0])
        staff_municipality =int( df['staff_municipality'][0])
        staff_barangay = int(df['staff_barangay'][0])
        staff_subdivision = df['staff_subdivision'][0]
        staff_house_number = df['staff_house_number'][0]
        staff_street = df['staff_street'][0]
        staff_zip_code = df['staff_zip_code'][0]
        staff_gsis = df['staff_gsis'][0]
        staff_pag_ibig = df['staff_pag_ibig'][0]
        staff_sss = df['staff_sss'][0]
        staff_philhealth = df['staff_philhealth'][0]
        staff_tin = df['staff_tin'][0]
        staff_govt_id = df['staff_govt_id'][0]
        staff_govt_number = df['staff_govt_number'][0]
        govt_id_date_of_issuance = df['govt_id_date_of_issuance'][0]
        govt_id_place_of_issuance = df['govt_id_place_of_issuance'][0]
        govt_id_photo = df['govt_id_photo'][0]
        staff_eligibility = df['staff_eligibility'][0]
        staff_eligibility_start = df['staff_eligibility_start'][0]
        staff_eligibility_end = df['staff_eligibility_end'][0]
        staff_landbank_acct_num = df['staff_landbank_acct_num'][0]
        landbank_photo = df['landbank_photo'][0]
        staff_emgcy_contact_name = df['staff_emgcy_contact_name'][0]
        staff_emgcy_contact_number = df['staff_emgcy_contact_number'][0]
        staff_emgcy_contact_address = df['staff_emgcy_contact_address'][0]
        ob_w_admin_date = df['ob_w_admin_date'][0]
        ob_w_admin = df['ob_w_admin'][0]
        ob_w_admin_link = df['ob_w_admin_link'][0]
        ob_w_home_team_date = df['ob_w_home_team_date'][0]
        ob_w_home_team = df['ob_w_home_team'][0]
        ob_w_home_team_link = df['ob_w_home_team_link'][0]
        gender_sensitivity_training_date = df['gender_sensitivity_training_date'][0]
        gender_sensitivity_training = df['gender_sensitivity_training'][0]
        gender_sensitivity_training_link = df['gender_sensitivity_training_link'][0]
        gender_dev_training_date = df['gender_dev_training_date'][0]
        gender_dev_training = df['gender_dev_training'][0]
        gender_dev_training_link = df['gender_dev_training_link'][0]
        open_up_fcisdg_date = df['open_up_fcisdg_date'][0]
        open_up_fcisdg = df['open_up_fcisdg'][0]
        open_up_fcisdg_link = df['open_up_fcisdg_link'][0]
        open_up_ppi_date = df['open_up_ppi_date'][0]
        open_up_ppi = df['open_up_ppi'][0]
        open_up_ppi_link = df['open_up_ppi_link'][0]
        open_up_iwsh_date = df['open_up_iwsh_date'][0]
        open_up_iwsh = df['open_up_iwsh'][0]
        open_up_iwsh_link = df['open_up_iwsh_link'][0]
        open_up_ashp_date = df['open_up_ashp_date'][0]
        open_up_ashp = df['open_up_ashp'][0]
        open_up_ashp_link = df['open_up_ashp_link'][0]
        others_orientation_trainings_date = df['others_orientation_trainings_date'][0]
        others_orientation_trainings = df['others_orientation_trainings'][0]
        others_orientation_trainings_link = df['others_orientation_trainings_link'][0]
        staff_cv = df['staff_cv'][0]    
        staff_cv_update = df['staff_cv_update'][0]
        staff_cv_link = df['staff_cv_link'][0]
        staff_image_name = df['staff_image_name'][0]

        # At the end of the function, before returning…
        # 1) Query the degrees table
        deg_sql = """
            SELECT degree, school, year_obtained
            FROM adminteam.staff_degrees
            WHERE staff_profile_id = %s
            ORDER BY created_at
        """
        deg_df = db.querydatafromdatabase(deg_sql, [staff_profile_id], ['degree','school','year_obtained'])

        # 2) Prepare values for A, B, C and compute count
        deg_count = len(deg_df)
        deg_a = deg_df.loc[0,'degree'] if deg_count>0 else None
        sch_a = deg_df.loc[0,'school'] if deg_count>0 else None
        yr_a  = deg_df.loc[0,'year_obtained'] if deg_count>0 else None

        deg_b = deg_df.loc[1,'degree'] if deg_count>1 else None
        sch_b = deg_df.loc[1,'school'] if deg_count>1 else None
        yr_b  = deg_df.loc[1,'year_obtained'] if deg_count>1 else None

        deg_c = deg_df.loc[2,'degree'] if deg_count>2 else None
        sch_c = deg_df.loc[2,'school'] if deg_count>2 else None
        yr_c  = deg_df.loc[2,'year_obtained'] if deg_count>2 else None
       
        return [staff_user_id, staff_country, staff_region, staff_province, staff_municipality, staff_barangay, staff_subdivision, staff_house_number, staff_street, staff_zip_code,
                staff_gsis, staff_pag_ibig, staff_sss, staff_philhealth, staff_tin, staff_govt_id, staff_govt_number, govt_id_date_of_issuance, govt_id_place_of_issuance,
                govt_id_photo,
                staff_eligibility, staff_eligibility_start, staff_eligibility_end,
                staff_landbank_acct_num, 
                landbank_photo,
                staff_emgcy_contact_name, staff_emgcy_contact_number, staff_emgcy_contact_address,
                ob_w_admin_date,
                ob_w_admin,
                ob_w_admin_link, 
                ob_w_home_team_date, 
                ob_w_home_team,
                ob_w_home_team_link, 
                gender_sensitivity_training_date, 
                gender_sensitivity_training,
                gender_sensitivity_training_link,
                gender_dev_training_date, 
                gender_dev_training,
                gender_dev_training_link, 
                open_up_fcisdg_date, 
                open_up_fcisdg,
                open_up_fcisdg_link, 
                open_up_ppi_date, 
                open_up_ppi,
                open_up_ppi_link,
                open_up_iwsh_date, 
                open_up_iwsh,
                open_up_iwsh_link, 
                open_up_ashp_date, 
                open_up_ashp,
                open_up_ashp_link, 
                others_orientation_trainings_date, 
                others_orientation_trainings,
                others_orientation_trainings_link,
                staff_cv,
                staff_cv_update, 
                staff_cv_link,
                staff_image_name,
                deg_a, sch_a, yr_a,
                deg_b, sch_b, yr_b,
                deg_c, sch_c, yr_c,
                ]
    else:
        raise PreventUpdate
    

@app.callback(
    Output('country', 'value'),
    [Input('country', 'options'),  
     Input('loaded_country', 'data')]  
)
def set_country_value(country_options, loaded_country):
    if country_options and loaded_country is not None:
        country_values = [option['value'] for option in country_options]
        if loaded_country in country_values:
            return loaded_country
    return dash.no_update  

@app.callback(
    Output('region', 'value'),
    [Input('region', 'options'),  
     Input('loaded_region', 'data')]  
)
def set_country_value(region_options, loaded_region):
    if region_options and loaded_region is not None:
        country_values = [option['value'] for option in region_options]
        if loaded_region in country_values:
            return loaded_region
    return dash.no_update  

@app.callback(
    Output('province', 'value'),
    [Input('province', 'options'),  
     Input('loaded_province', 'data')]  
)
def set_country_value(province_options, loaded_province):
    if province_options and loaded_province is not None:
        country_values = [option['value'] for option in province_options]
        if loaded_province in country_values:
            return loaded_province
    return dash.no_update  

@app.callback(
    Output('municipality', 'value'),
    [Input('municipality', 'options'),  
     Input('loaded_municipality', 'data')]  
)
def set_country_value(municipality_options, loaded_municipality):
    if municipality_options and loaded_municipality is not None:
        country_values = [option['value'] for option in municipality_options]
        if loaded_municipality in country_values:
            return loaded_municipality
    return dash.no_update  


@app.callback(
    Output('barangay', 'value'),
    [Input('barangay', 'options'),  
     Input('loaded_barangay', 'data')]  
)
def set_country_value(barangay_options, loaded_barangay):
    if barangay_options and loaded_barangay is not None:
        country_values = [option['value'] for option in barangay_options]
        if loaded_barangay in country_values:
            return loaded_barangay
    return dash.no_update  


@app.callback(
    [  
        Output('user_id', 'disabled'),
        Output('staff_image', 'disabled'),
        Output('personal_info', 'style'),
        Output('current_address', 'style'),
        Output('govt_ids', 'style'),
        Output('degrees_earned', 'style'),
        Output('eligibility', 'style'),
        Output('landbank_account', 'style'),
        Output('emergency_contact', 'style'),
        Output('orientation_checklist', 'style'),
        Output('resume_info', 'style'),
    ],
    [Input('url', 'search')]
)
def staff_profile_disabled(search):

    editable_disabled_style = {
        "background-color": "white",
        "color": "black",
        "opacity": "1",
        "width": "100%",
        "pointer-events": "none"
    }

    user_id = True
    staff_image = False
    
    personal_info = current_address = govt_ids = degrees_earned = eligibility = landbank_account = emergency_contact = orientation_checklist = resume_info = {}

    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'add':
            user_id = False
            staff_image = False
        elif create_mode == 'edit':
            user_id = True
            staff_image = False
            
            personal_info = current_address = govt_ids = degrees_earned = eligibility = landbank_account = emergency_contact = orientation_checklist = resume_info = {}

        elif create_mode == 'view':
            user_id = True
            staff_image = True
        
            personal_info = current_address = govt_ids = degrees_earned = eligibility = landbank_account = emergency_contact = orientation_checklist = resume_info = editable_disabled_style

    return [user_id, staff_image, personal_info, current_address, govt_ids, degrees_earned, eligibility, landbank_account, emergency_contact, orientation_checklist, resume_info]

@app.callback(
    Output('profile_image', 'src'),
    [
        Input('staff_image', 'contents'),
        Input('staff_image', 'filename'),
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