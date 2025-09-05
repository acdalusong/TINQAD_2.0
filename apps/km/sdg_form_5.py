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
UPLOAD_DIRECTORY = r".\assets\database\km\sdg"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


# Define highlight colors
highlight_colors = {
    'primary': "#0a4323",
    'secondary': "#7a0911",
    'accent': "#f8b237"
}

# fetch mapping metric code → metric_id
all_metrics = db.querydatafromdatabase(
    "SELECT metric_id, code FROM kmteam.metric WHERE sdg_number = %s",
    [5],
    ["metric_id","code"]
)
metrics_map = dict(zip(all_metrics["code"], all_metrics["metric_id"]))

metric_info_df = db.querydatafromdatabase(
    "SELECT code, additional_information FROM kmteam.metric WHERE sdg_number = %s",
    [5],
    ["code","additional_information"],
)
additional_info = dict(
    zip(metric_info_df["code"], metric_info_df["additional_information"])
)

sdg5_form = dbc.Form([
    # ─────────────── Submitter’s Profile ───────────────
    dbc.Card([
        dbc.CardHeader(
            html.H5("Submitter's Profile"),
            style={"backgroundColor": highlight_colors['secondary'], "color": "white"},
        ),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(dbc.Label("Name of Submitter"), width=6),
                dbc.Col(dbc.Input(id="sdg5_submitter", type="text"), width=6),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Label("Submitter's Office"), width=6),
                dbc.Col(dbc.Input(id="sdg5_submitter_office", type="text"), width=6),
            ], className="mb-3"),
        ]),
    ], className="mb-4"),

    # ─────────────── Metrics Accordion ────────────────
    dbc.Accordion([

        # 5.2 Proportion of first-generation female students
        dbc.AccordionItem([
            # Header with Alert
            dbc.Row([
                dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=8),
                dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
            ], className="mb-3"),

            # Total Number of students
            dbc.Row([
                dbc.Col(html.Label("Total Number of students", id="label-2-1",), width=4),
                dbc.Col(dbc.Input(id="sdg5_2_1_total", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_2_1_total_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_2_1_total_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_2_1_total_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Total Number of students starting a degree
            dbc.Row([
                dbc.Col(html.Label("Total Number of students starting a degree", id="label-2-2"), width=4),
                dbc.Col(dbc.Input(id="sdg5_2_2_total", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_2_2_total_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_2_2_total_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_2_2_total_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Number of first-generation students starting a degree
            dbc.Row([
                dbc.Col(html.Label("Number of first-generation students starting a degree", id="label-2-3"), width=4),
                dbc.Col(dbc.Input(id="sdg5_2_3", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_2_3_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_2_3_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_2_3_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Number of women starting a degree
            dbc.Row([
                dbc.Col(html.Label("Number of women starting a degree", id="label-2-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_2_4", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_2_4_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_2_4_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_2_4_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Number of first-generation women starting a degree
            dbc.Row([
                dbc.Col(html.Label("Number of first-generation women starting a degree", id="label-2-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_2_5", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_2_5_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_2_5_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_2_5_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

        ], 
        title=html.Div(
                    [
                        html.Span("5.2 Proportion of first-generation female students", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg5_2_alert",
                            style={"display":"none"}
                        )
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "width": "100%"
                    }
                ),
    ),
        


        # 5.3 Student Access Measures (text‑type with sub‑metrics)
        dbc.AccordionItem([
            # Header with Alert
            dbc.Row([
                dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=4),
                dbc.Col(html.Label("Evidence Link 1", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                dbc.Col(html.Label("Evidence Link 2", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(html.Label("Tracking access measures", id="label-3-1", style={"cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg5_3_1_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_3_1_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_3_1_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_3_1_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_3_1_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(html.Label("Policy for women applications and entry", id="label-3-2", style={"cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg5_3_2_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_3_2_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_3_2_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_3_2_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_3_2_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row(dbc.Col(html.Label("Women's access schemes: Provision", id="label-3-3", style={"fontStyle":"italic"}), width=12), className="mb-2"),
            dbc.Row([
                dbc.Col(html.Label("Provisions", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_3_3_evidence_link_1a", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_3_3_evidence_link_2a", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_3_3_status_a"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_3_3_comment_a", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_3_3_alert_a", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(html.Label("Mentoring", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_3_3_evidence_link_1b", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_3_3_evidence_link_2b", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_3_3_status_b"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_3_3_comment_b", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_3_3_alert_b", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(html.Label("Scholarships", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_3_3_evidence_link_1c", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_3_3_evidence_link_2c", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_3_3_status_c"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_3_3_comment_c", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_3_3_alert_c", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(html.Label("Other Provisions", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_3_3_evidence_link_1d", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_3_3_evidence_link_2d", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_3_3_status_d"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_3_3_comment_d", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_3_3_alert_d", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row(dbc.Col(html.Label("Women's application in underrepresented subjects:", id="label-3-4", style={"fontStyle":"italic", "cursor":"help"}), width=12), className="mb-2"),
            dbc.Row([
                dbc.Col(html.Label("University Outreach", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_3_4_evidence_link_1a", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_3_4_evidence_link_2a", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_3_4_status_a"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_3_4_comment_a", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_3_4_alert_a", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(html.Label("Collaboration", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_3_4_evidence_link_1b", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_3_4_evidence_link_2b", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_3_4_status_b"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_3_4_comment_b", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_3_4_alert_b", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

        ], 
        title=html.Div(
                    [
                        html.Span("5.3 Student Access Measures", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg5_3_alert",
                            style={"display":"none"}
                        )
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "width": "100%"
                    }
                ),
    ),


        # 5.4 Proportion of senior female academics
        dbc.AccordionItem([  
            # Header with Alert  
            dbc.Row([  
                dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=8),  
                dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),  
                dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),  
                dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),  
            ], className="mb-3"),  

            # Number of employees  
            dbc.Row([  
                dbc.Col(html.Label("Number of employees", id="label-4-1"), width=4),  
                dbc.Col(dbc.Input(id="sdg5_4_1", type="number", min=0), width=4),  
                dbc.Col(dbc.Select(id="sdg5_4_1_status"), width=1),  
                dbc.Col(  
                    dbc.Button("View", id="sdg5_4_1_comment", color="warning", size="sm", className="w-100"),  
                    width=2  
                ),  
                dbc.Col(  
                    html.Div(  
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),  
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),  
                        id="sdg5_4_1_alert", style={"display":"none"}  
                    ), width=1  
                ),  
            ], className="mb-3"),  

            # Number of academic staff  
            dbc.Row([  
                dbc.Col(html.Label("Number of academic staff", id="label-4-2"), width=4),  
                dbc.Col(dbc.Input(id="sdg5_4_2", type="number", min=0), width=4),  
                dbc.Col(dbc.Select(id="sdg5_4_2_status"), width=1),  
                dbc.Col(  
                    dbc.Button("View", id="sdg5_4_2_comment", color="warning", size="sm", className="w-100"),  
                    width=2  
                ),  
                dbc.Col(  
                    html.Div(  
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),  
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),  
                        id="sdg5_4_2_alert", style={"display":"none"}  
                    ), width=1  
                ),  
            ], className="mb-3"),  

            # Number of senior academic staff  
            dbc.Row([  
                dbc.Col(html.Label("Number of senior academic staff", id="label-4-3", style={"cursor":"help"}), width=4),  
                dbc.Col(dbc.Input(id="sdg5_4_3", type="number", min=0), width=4),  
                dbc.Col(dbc.Select(id="sdg5_4_3_status"), width=1),  
                dbc.Col(  
                    dbc.Button("View", id="sdg5_4_3_comment", color="warning", size="sm", className="w-100"),  
                    width=2  
                ),  
                dbc.Col(  
                    html.Div(  
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),  
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),  
                        id="sdg5_4_3_alert", style={"display":"none"}  
                    ), width=1  
                ),  
            ], className="mb-3"),  

            # Number of female senior academic staff  
            dbc.Row([  
                dbc.Col(html.Label("Number of female senior academic staff", id="label-4-4", style={"cursor":"help"}), width=4),  
                dbc.Col(dbc.Input(id="sdg5_4_4", type="number", min=0), width=4),  
                dbc.Col(dbc.Select(id="sdg5_4_4_status"), width=1),  
                dbc.Col(  
                    dbc.Button("View", id="sdg5_4_4_comment", color="warning", size="sm", className="w-100"),  
                    width=2  
                ),  
                dbc.Col(  
                    html.Div(  
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),  
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),  
                        id="sdg5_4_4_alert", style={"display":"none"}  
                    ), width=1  
                ),  
            ], className="mb-3"),  

        ],
        title=html.Div(
                    [
                        html.Span("5.4 Proportion of senior female academics", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg5_4_alert",
                            style={"display":"none"}
                        )
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "width": "100%"
                    }
                ),
        ),


        # 5.5 Proportion of women receiving degrees
        dbc.AccordionItem([
            # Header with Alert
            dbc.Row([
                dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=8),
                dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
            ], className="mb-3"),

            # Total Number of graduates (5.5.1)
            dbc.Row([
                dbc.Col(html.Label("Total Number of graduates", id="label-5-1", style={"fontStyle":"italic","cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_1_total", type="number", min=0, disabled=True), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_1_total_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_1_total_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_1_total_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # First Semester
            dbc.Row([
                dbc.Col(html.Label("First Semester", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_1_first", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_1_first_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_1_first_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_1_first_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Second Semester
            dbc.Row([
                dbc.Col(html.Label("Second Semester", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_1_second", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_1_second_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_1_second_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_1_second_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Mid Year
            dbc.Row([
                dbc.Col(html.Label("Mid Year", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_1_mid", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_1_mid_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_1_mid_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_1_mid_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Total graduates by subject area (5.5.2)
            dbc.Row([
                dbc.Col(html.Label("Total graduates by subject area", id="label-5-2", style={"fontStyle":"italic","cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_2_total", type="number", min=0, disabled=True), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_2_total_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_2_total_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_2_total_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Number of graduates: STEM (5.5.3)
            dbc.Row([dbc.Col(html.Label("Number of graduates: STEM", className="ps-4"), width=4)], className="mb-3"),
            dbc.Row([
                dbc.Col(html.Label("Total", className="ps-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_3_total", type="number", min=0, disabled=True), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_3_total_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_3_total_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_3_total_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(html.Label("Male", className="ps-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_3_male", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_3_male_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_3_male_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_3_male_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(html.Label("Female", className="ps-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_3_female", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_3_female_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_3_female_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_3_female_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Number of graduates: Medicine (5.5.4)
            dbc.Row([dbc.Col(html.Label("Number of graduates: Medicine", className="ps-4"), width=4)], className="mb-3"),
            dbc.Row([
                dbc.Col(html.Label("Total", className="ps-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_4_total", type="number", min=0, disabled=True), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_4_total_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_4_total_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_4_total_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(html.Label("Male", className="ps-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_4_male", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_4_male_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_4_male_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_4_male_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(html.Label("Female", className="ps-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_4_female", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_4_female_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_4_female_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_4_female_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Number of graduates: Arts & Humanities / Social Sciences (5.5.5)
            dbc.Row([dbc.Col(html.Label("Number of graduates: Arts & Humanities / Social Sciences", className="ps-4"), width=4)], className="mb-3"),
            dbc.Row([
                dbc.Col(html.Label("Total", className="ps-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_5_total", type="number", min=0, disabled=True), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_5_total_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_5_total_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_5_total_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(html.Label("Male", className="ps-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_5_male", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_5_male_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_5_male_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_5_male_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(html.Label("Female", className="ps-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_5_5_female", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg5_5_5_female_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_5_5_female_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_5_5_female_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

        ],
        title=html.Div(
                    [
                        html.Span("5.5 Proportion of women receiving degrees", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg5_5_alert",
                            style={"display":"none"}
                        )
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "width": "100%"
                    }
                ),
        ),


        # 5.6 Women's progress measures
        dbc.AccordionItem([
            # Header with Alert
            dbc.Row([
                dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=4),
                dbc.Col(html.Label("Evidence Link 1", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                dbc.Col(html.Label("Evidence Link 2", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
            ], className="mb-3"),

            # 5.6.1 Policy of non-discrimination against women
            dbc.Row([
                dbc.Col(html.Label("Policy of non-discrimination against women", id="label-6-1", style={"cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg5_6_1_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_6_1_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_6_1_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_6_1_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_6_1_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 5.6.2 Non-discrimination policies for transgender people
            dbc.Row([
                dbc.Col(html.Label("Non-discrimination policies for transgender people", id="label-6-2", style={"cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg5_6_2_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_6_2_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_6_2_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_6_2_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_6_2_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 5.6.3 Maternity and paternity policies
            dbc.Row([
                dbc.Col(html.Label("Maternity and paternity policies", id="label-6-3", style={"cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg5_6_3_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_6_3_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_6_3_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_6_3_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_6_3_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 5.6.4 Childcare facilities for students
            dbc.Row([
                dbc.Col(html.Label("Childcare facilities for students", id="label-6-4"), width=4),
                dbc.Col(dbc.Input(id="sdg5_6_4_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_6_4_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_6_4_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_6_4_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_6_4_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 5.6.5 Childcare facilities for staff and faculty
            dbc.Row([
                dbc.Col(html.Label("Childcare facilities for staff and faculty", id="label-6-5"), width=4),
                dbc.Col(dbc.Input(id="sdg5_6_5_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_6_5_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_6_5_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_6_5_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_6_5_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 5.6.6 Women's mentoring schemes
            dbc.Row([
                dbc.Col(html.Label("Women's mentoring schemes", id="label-6-6", style={"cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg5_6_6_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_6_6_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_6_6_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_6_6_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_6_6_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 5.6.7 Track women's graduation rate
            dbc.Row([
                dbc.Col(html.Label("Track women's graduation rate",id="label-6-7"), width=4),
                dbc.Col(dbc.Input(id="sdg5_6_7_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_6_7_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_6_7_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_6_7_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_6_7_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 5.6.8 Policies protecting those reporting discrimination
            dbc.Row([
                dbc.Col(html.Label("Policies protecting those reporting discrimination", id="label-6-8", style={"cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg5_6_8_evidence_link_1", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg5_6_8_evidence_link_2", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg5_6_8_status"), width=2),
                dbc.Col(
                    dbc.Button("View", id="sdg5_6_8_comment", color="warning", size="sm", className="w-100"),
                    width=1
                ),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg5_6_8_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

        ],
        title=html.Div(
                    [
                        html.Span("5.6 Women's progress measures", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg5_6_alert",
                            style={"display":"none"}
                        )
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "width": "100%"
                    }
                ),
        ),

    ], start_collapsed=True, always_open=True),
])

@app.callback(
    Output('sdg5_5_1_total', 'value', allow_duplicate=True),
    [Input('sdg5_5_1_first', 'value'),
     Input('sdg5_5_1_second', 'value'),
     Input('sdg5_5_1_mid', 'value')],
    prevent_initial_call=True,
)
def update_1_total(first, second, mid):  # noqa
    # Treat None as 0
    total = sum(v or 0 for v in (first, second, mid))
    return total

@app.callback(
    Output('sdg5_5_3_total', 'value', allow_duplicate=True),
    [Input('sdg5_5_3_male', 'value'),
     Input('sdg5_5_3_female', 'value'),
    ],
    prevent_initial_call=True,
)
def update_2_total(first, second):  # noqa
    total = sum(v or 0 for v in (first, second))
    return total

@app.callback(
    Output('sdg5_5_4_total', 'value', allow_duplicate=True),
    [Input('sdg5_5_4_male', 'value'),
     Input('sdg5_5_4_female', 'value'),
    ],
    prevent_initial_call=True,
)
def update_3_total(first, second):  # noqa
    total = sum(v or 0 for v in (first, second))
    return total

@app.callback(
    Output('sdg5_5_5_total', 'value', allow_duplicate=True),
    [Input('sdg5_5_5_male', 'value'),
     Input('sdg5_5_5_female', 'value'),
    ],
    prevent_initial_call=True,
)
def update_4_total(first, second):  # noqa
    total = sum(v or 0 for v in (first, second))
    return total


@app.callback(
    Output('sdg5_5_2_total', 'value', allow_duplicate=True),
    [Input('sdg5_5_3_total', 'value'),
     Input('sdg5_5_4_total', 'value'),
     Input('sdg5_5_5_total', 'value')],
    prevent_initial_call=True,
)
def update_5_total(first, second, mid):  # noqa
    total = sum(v or 0 for v in (first, second, mid))
    return total

tooltip_3_1 = dbc.Tooltip(
    additional_info.get("3.1", ""),   # your hover-text
    target="label-3-1",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_2 = dbc.Tooltip(
    additional_info.get("3.2", ""),   # your hover-text
    target="label-3-2",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_4 = dbc.Tooltip(
    additional_info.get("3.4a", ""),   # your hover-text
    target="label-3-4",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_4_3 = dbc.Tooltip(
    additional_info.get("4.3", ""),   # your hover-text
    target="label-4-3",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_4_4 = dbc.Tooltip(
    additional_info.get("4.4", ""),   # your hover-text
    target="label-4-4",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_5_1 = dbc.Tooltip(
    additional_info.get("5.1total", ""),   # your hover-text
    target="label-5-1",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_5_2 = dbc.Tooltip(
    additional_info.get("5.2total", ""),   # your hover-text
    target="label-5-2",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_6_1 = dbc.Tooltip(
    additional_info.get("6.1", ""),   # your hover-text
    target="label-6-1",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_6_2 = dbc.Tooltip(
    additional_info.get("6.2", ""),   # your hover-text
    target="label-6-2",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_6_3 = dbc.Tooltip(
    additional_info.get("6.3", ""),   # your hover-text
    target="label-6-3",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_6_6 = dbc.Tooltip(
    additional_info.get("6.6", ""),   # your hover-text
    target="label-6-6",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_6_8 = dbc.Tooltip(
    additional_info.get("6.8", ""),   # your hover-text
    target="label-6-8",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.Div(
                            [
                                dcc.Store(id='sdg5_toload', storage_type='memory', data=0),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H1(id="sdg5_page_header"),
                                            width=8
                                        ),
                                        dbc.Col(
                                            dbc.Button("Back", color="success", href="/sdglist"),
                                            width=4,
                                            id="sdg5_back_btn_div",
                                            style={"display": "flex", "justifyContent": "flex-end"}
                                        )
                                    ],
                                    align="center"
                                ),
                            ],
                            className="mb-0"
                        ),
                        html.Hr(),
                        sdg5_form,
                        tooltip_3_1,
                        tooltip_3_2,
                        tooltip_3_4,
                        tooltip_4_3,
                        tooltip_4_4,
                        tooltip_5_1,
                        tooltip_5_2,
                        tooltip_6_1,
                        tooltip_6_2,
                        tooltip_6_3,
                        tooltip_6_6,
                        tooltip_6_8,
                        html.Div(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H5("Evidence Checking"),
                                            style={
                                                "backgroundColor": highlight_colors['secondary'],
                                                "color": "white"
                                            }
                                        ),
                                        dbc.CardBody(
                                            [
                                                # Row: Label + Select
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dbc.Label("Evidence Status"),
                                                            width=4
                                                        ),
                                                        dbc.Col(
                                                            dbc.Select(
                                                                id="sdg5_evidence_status",
                                                                options=[
                                                                    {"label": "For Checking", "value": "For Checking"},
                                                                    {"label": "For Revision", "value": "For Revision"},
                                                                    {"label": "Accepted", "value": "Accepted"},
                                                                ],
                                                                placeholder="Select status"
                                                            ),
                                                            width=8
                                                        ),
                                                    ],
                                                    className="mb-3",
                                                ),
                                                # Text area for comments (adjustable for long text)
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dbc.Textarea(
                                                                id="sdg5_evidence_comments",
                                                                placeholder="Enter detailed comments here...",
                                                                style={"width": "100%", "minHeight": "100px"}
                                                            ),
                                                            width=12
                                                        ),
                                                    ],
                                                    className="mb-3",
                                                ),
                                            ]
                                        ),
                                    ],
                                    className="mb-4",
                                ),
                            ],
                            id="sdg5_evidence_div",
                            style={"display": "none"},  # hidden initially
                        ),
                        html.Br(),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='sdg5_removerecord',
                                            options=[
                                                {'label': "Mark for Deletion", 'value': 1}
                                            ],
                                            style={'fontWeight': 'bold'},
                                        ),
                                        width=5,
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='sdg5_removerecord_div'
                        ),
                        dbc.Alert(id='sdg5_alert', is_open=False),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H5(id="sdg5_comment_modal_header")),
                                dbc.ModalBody(html.Div(id="sdg5_comment_modal_body")),
                                dbc.ModalFooter(
                                    dbc.Button("Close", id="sdg5_comment_modal_close", color="secondary")
                                ),
                            ],
                            id="sdg5_comment_modal",
                            is_open=False,
                            centered=True,
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id='sdg5_last_modal_header'), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(
                                    html.H5("Click Proceed to continue"),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Proceed", href='/sdglist', color="success"),
                                    ]
                                ),
                            ],
                            centered=True,
                            id="sdg5_last_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), close_button=True, className="bg-primary"),
                                dbc.ModalBody(
                                    html.H5(id="sdg5_initial_modal_message"),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Spinner(color="success", id="sdg5_spinner", spinner_style={"display":"none"}),
                                        dbc.Button("Cancel", id="sdg5_initial_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id="sdg5_initial_modal_confirm", color="success"),
                                    ]
                                ),
                            ],
                            centered=True,
                            id="sdg5_initial_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                        html.Br(),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Button("Save", color="primary", id="sdg5_save_button", n_clicks=0),
                                        width="auto"
                                    ),
                                    dbc.Col(
                                        dbc.Button("Cancel", color="warning", id="sdg5_cancel_button", n_clicks=0, href="/sdglist"),
                                        width="auto"
                                    ),
                                ],
                                className="mb-2",
                                justify="end",
                            ),
                            id="sdg5_buttons_div"
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ],
                    width=8,
                    style={"marginLeft": "15px"},
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(),
                    width={"size": 12, "offset": 0}
                ),
            ]
        ),
    ],
    fluid=True,
)

@app.callback(
    [
        Output('sdg5_spinner', 'spinner_style')
    ],
    [
        Input('sdg5_initial_modal_confirm', 'n_clicks'),
    ]
)
def save_sdg5(confirm):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    if eventid == 'sdg5_initial_modal_confirm' and confirm:
        return [{"display":"block"}]
    else:
        return [{"display":"none"}]


@app.callback(
    [
        # Check if all fields are filled
        Output('sdg5_last_modal', 'is_open'),
        Output('sdg5_last_modal_header', 'children'),
        #Initial Field
        Output('sdg5_initial_modal', 'is_open'),
        Output('sdg5_initial_modal_message', 'children'),
        Output('sdg5_initial_modal_confirm', 'color'),
        Output('sdg5_alert', 'is_open'),
        Output('sdg5_alert', 'color'),
        Output('sdg5_alert', 'children'),
        Output('sdg5_submitter', 'className'),
        Output('sdg5_submitter_office', 'className')
    ],
    [
        Input('sdg5_save_button', 'n_clicks'),
        Input('sdg5_initial_modal_confirm', 'n_clicks'),
        Input('sdg5_initial_modal_cancel', 'n_clicks'),
    ],
    [
        State('sdg5_2_1_total', 'value'),
        State('sdg5_2_2_total', 'value'),
        State('sdg5_2_3', 'value'),
        State('sdg5_2_4', 'value'),
        State('sdg5_2_5', 'value'),
        State('sdg5_3_1_evidence_link_1', 'value'),
        State('sdg5_3_1_evidence_link_2', 'value'),
        State('sdg5_3_2_evidence_link_1', 'value'),
        State('sdg5_3_2_evidence_link_2', 'value'),
        State('sdg5_3_3_evidence_link_1a', 'value'),
        State('sdg5_3_3_evidence_link_2a', 'value'),
        State('sdg5_3_3_evidence_link_1b', 'value'),
        State('sdg5_3_3_evidence_link_2b', 'value'),
        State('sdg5_3_3_evidence_link_1c', 'value'),
        State('sdg5_3_3_evidence_link_2c', 'value'),
        State('sdg5_3_3_evidence_link_1d', 'value'),
        State('sdg5_3_3_evidence_link_2d', 'value'),
        State('sdg5_3_4_evidence_link_1a', 'value'),
        State('sdg5_3_4_evidence_link_2a', 'value'),
        State('sdg5_3_4_evidence_link_1b', 'value'),
        State('sdg5_3_4_evidence_link_2b', 'value'),
        State('sdg5_4_1', 'value'),
        State('sdg5_4_2', 'value'),
        State('sdg5_4_3', 'value'),
        State('sdg5_4_4', 'value'),
        State('sdg5_5_1_total', 'value'),
        State('sdg5_5_1_first', 'value'),
        State('sdg5_5_1_second', 'value'),
        State('sdg5_5_1_mid', 'value'),
        State('sdg5_5_2_total', 'value'),
        State('sdg5_5_3_total', 'value'),
        State('sdg5_5_3_male', 'value'),
        State('sdg5_5_3_female', 'value'),
        State('sdg5_5_4_total', 'value'),
        State('sdg5_5_4_male', 'value'),
        State('sdg5_5_4_female', 'value'),
        State('sdg5_5_5_total', 'value'),
        State('sdg5_5_5_male', 'value'),
        State('sdg5_5_5_female', 'value'),
        State('sdg5_6_1_evidence_link_1', 'value'),
        State('sdg5_6_1_evidence_link_2', 'value'),
        State('sdg5_6_2_evidence_link_1', 'value'),
        State('sdg5_6_2_evidence_link_2', 'value'),
        State('sdg5_6_3_evidence_link_1', 'value'),
        State('sdg5_6_3_evidence_link_2', 'value'),
        State('sdg5_6_4_evidence_link_1', 'value'),
        State('sdg5_6_4_evidence_link_2', 'value'),
        State('sdg5_6_5_evidence_link_1', 'value'),
        State('sdg5_6_5_evidence_link_2', 'value'),
        State('sdg5_6_6_evidence_link_1', 'value'),
        State('sdg5_6_6_evidence_link_2', 'value'),
        State('sdg5_6_7_evidence_link_1', 'value'),
        State('sdg5_6_7_evidence_link_2', 'value'),
        State('sdg5_6_8_evidence_link_1', 'value'),
        State('sdg5_6_8_evidence_link_2', 'value'),
        State('sdg5_submitter', 'value'),
        State('sdg5_submitter_office', 'value'),
        State('url', 'search'),
        State('sdg5_removerecord', 'value'),
        State('currentuserid', 'data')

        
    ],
)
def save_sdg5(
    submit, confirm, cancel, 
    sdg5_2_1_total, sdg5_2_2_total, sdg5_2_3, sdg5_2_4, sdg5_2_5, sdg5_3_1_evidence_link_1, sdg5_3_1_evidence_link_2, 
    sdg5_3_2_evidence_link_1, sdg5_3_2_evidence_link_2, sdg5_3_3_evidence_link_1a, sdg5_3_3_evidence_link_2a, sdg5_3_3_evidence_link_1b, 
    sdg5_3_3_evidence_link_2b, sdg5_3_3_evidence_link_1c, sdg5_3_3_evidence_link_2c, sdg5_3_3_evidence_link_1d, sdg5_3_3_evidence_link_2d, 
    sdg5_3_4_evidence_link_1a, sdg5_3_4_evidence_link_2a, sdg5_3_4_evidence_link_1b, sdg5_3_4_evidence_link_2b, sdg5_4_1, sdg5_4_2, sdg5_4_3, 
    sdg5_4_4, sdg5_5_1_total, sdg5_5_1_first, sdg5_5_1_second, sdg5_5_1_mid, sdg5_5_2_total, sdg5_5_3_total, sdg5_5_3_male, sdg5_5_3_female, 
    sdg5_5_4_total, sdg5_5_4_male, sdg5_5_4_female, sdg5_5_5_total, sdg5_5_5_male, sdg5_5_5_female, sdg5_6_1_evidence_link_1, sdg5_6_1_evidence_link_2, 
    sdg5_6_2_evidence_link_1, sdg5_6_2_evidence_link_2, sdg5_6_3_evidence_link_1, sdg5_6_3_evidence_link_2, sdg5_6_4_evidence_link_1, 
    sdg5_6_4_evidence_link_2, sdg5_6_5_evidence_link_1, sdg5_6_5_evidence_link_2, sdg5_6_6_evidence_link_1, sdg5_6_6_evidence_link_2, 
    sdg5_6_7_evidence_link_1, sdg5_6_7_evidence_link_2, sdg5_6_8_evidence_link_1, sdg5_6_8_evidence_link_2,
    sdg5_submitter, sdg5_submitter_office,
    search, removerecord, currentuserid
):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    # Set default outputs
    final_modal_open = False
    final_modal_header = ''
    initial_modal_open = False
    initial_modal_message = ''
    confirm_button_color = 'success'
    alert_open = False
    alert_color = ''
    alert_text = ''
    sdg_submitter_className = ''
    sdg_submitter_office_className = ''

    if eventid == 'sdg5_save_button' and submit:
        def get_input_class(value):
            return 'red-border' if not value else 'form-control'
        if not all([sdg5_submitter, sdg5_submitter_office]) and not removerecord:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            sdg_submitter_className = get_input_class(sdg5_submitter)
            sdg_submitter_office_className = get_input_class(sdg5_submitter_office)
        else: # all inputs are valid
            if create_mode == 'add':
                initial_modal_open = True
                initial_modal_message = "Are you sure you want to submit this evidence entry?"
            elif create_mode == 'edit':
                initial_modal_open = True
                initial_modal_message = "Are you sure you want to save changes to this evidence entry?"
                if removerecord:
                    initial_modal_message = "Are you sure you want to delete this evidence entry?"
                    confirm_button_color = 'danger'
    elif eventid == 'sdg5_initial_modal_confirm' and confirm:
        if create_mode == 'add':
            sql_sub = """
            INSERT INTO kmteam.submission (submitter, submitter_office, submitter_id, reckoning_period)
            VALUES (
                %s, %s, %s, 
                (SELECT reckoning_period_id
                    FROM kmteam.reckoning_periods
                    WHERE active_status = TRUE
                        AND reckoning_period_del_ind  = FALSE
                    LIMIT 1
                )
            )
            RETURNING submission_id
            """
            df_sub = db.execute_returning(sql_sub, [sdg5_submitter, sdg5_submitter_office, currentuserid], ['submission_id'])
            submission_id = int(df_sub.loc[0, 'submission_id'])

            # 2) Build a list of all evidence to insert
            #    Map each input to its metric code + link_number + status + comment (if any)
            to_insert = []

            def add_ev(code, link_no, val, status=None, comment=None):
                if val not in (None, ""):
                    # metrics_map must be pre-loaded at app start
                    m_id = metrics_map[code]
                    to_insert.append((submission_id, m_id, link_no, str(val), status, comment))

            #numeric metrics — treat each as a single “link 1”
            add_ev('2.1total', 1, sdg5_2_1_total, None, None)
            add_ev('2.2total', 1, sdg5_2_2_total, None, None)
            add_ev('2.3',     1, sdg5_2_3,           None, None)
            add_ev('2.4',     1, sdg5_2_4,           None, None)
            add_ev('2.5',     1, sdg5_2_5,           None, None)
            add_ev('3.1', 1, sdg5_3_1_evidence_link_1, None, None)
            add_ev('3.1', 2, sdg5_3_1_evidence_link_2, None, None)
            add_ev('3.2', 1, sdg5_3_2_evidence_link_1, None, None)
            add_ev('3.2', 2, sdg5_3_2_evidence_link_2, None, None)
            add_ev('3.3a', 1, sdg5_3_3_evidence_link_1a, None, None)
            add_ev('3.3a', 2, sdg5_3_3_evidence_link_2a, None, None)
            add_ev('3.3b', 1, sdg5_3_3_evidence_link_1b, None, None)
            add_ev('3.3b', 2, sdg5_3_3_evidence_link_2b, None, None)
            add_ev('3.3c', 1, sdg5_3_3_evidence_link_1c, None, None)
            add_ev('3.3c', 2, sdg5_3_3_evidence_link_2c, None, None)
            add_ev('3.3d', 1, sdg5_3_3_evidence_link_1d, None, None)
            add_ev('3.3d', 2, sdg5_3_3_evidence_link_2d, None, None)
            add_ev('3.4a', 1, sdg5_3_4_evidence_link_1a, None, None)
            add_ev('3.4a', 2, sdg5_3_4_evidence_link_2a, None, None)
            add_ev('3.4b', 1, sdg5_3_4_evidence_link_1b, None, None)
            add_ev('3.4b', 2, sdg5_3_4_evidence_link_2b, None, None)
            add_ev('4.1', 1, sdg5_4_1, None, None)
            add_ev('4.2', 1, sdg5_4_2, None, None)
            add_ev('4.3', 1, sdg5_4_3, None, None)
            add_ev('4.4', 1, sdg5_4_4, None, None)
            add_ev('5.1total',  1, sdg5_5_1_total,  None, None)
            add_ev('5.1first',  1, sdg5_5_1_first,  None, None)
            add_ev('5.1second', 1, sdg5_5_1_second, None, None)
            add_ev('5.1mid',    1, sdg5_5_1_mid,    None, None)
            add_ev('5.2total', 1, sdg5_5_2_total, None, None)
            add_ev('5.3total',  1, sdg5_5_3_total,  None, None)
            add_ev('5.3male',   1, sdg5_5_3_male,   None, None)
            add_ev('5.3female', 1, sdg5_5_3_female, None, None)
            add_ev('5.4total',  1, sdg5_5_4_total,  None, None)
            add_ev('5.4male',   1, sdg5_5_4_male,   None, None)
            add_ev('5.4female', 1, sdg5_5_4_female, None, None)
            add_ev('5.5total',  1, sdg5_5_5_total,  None, None)
            add_ev('5.5male',   1, sdg5_5_5_male,   None, None)
            add_ev('5.5female', 1, sdg5_5_5_female, None, None)
            add_ev('6.1', 1, sdg5_6_1_evidence_link_1, None, None)
            add_ev('6.1', 2, sdg5_6_1_evidence_link_2, None, None)
            add_ev('6.2', 1, sdg5_6_2_evidence_link_1, None, None)
            add_ev('6.2', 2, sdg5_6_2_evidence_link_2, None, None)
            add_ev('6.3', 1, sdg5_6_3_evidence_link_1, None, None)
            add_ev('6.3', 2, sdg5_6_3_evidence_link_2, None, None)
            add_ev('6.4', 1, sdg5_6_4_evidence_link_1, None, None)
            add_ev('6.4', 2, sdg5_6_4_evidence_link_2, None, None)
            add_ev('6.5', 1, sdg5_6_5_evidence_link_1, None, None)
            add_ev('6.5', 2, sdg5_6_5_evidence_link_2, None, None)
            add_ev('6.6', 1, sdg5_6_6_evidence_link_1, None, None)
            add_ev('6.6', 2, sdg5_6_6_evidence_link_2, None, None)
            add_ev('6.7', 1, sdg5_6_7_evidence_link_1, None, None)
            add_ev('6.7', 2, sdg5_6_7_evidence_link_2, None, None)
            add_ev('6.8', 1, sdg5_6_8_evidence_link_1, None, None)
            add_ev('6.8', 2, sdg5_6_8_evidence_link_2, None, None)


            # 3) Perform all evidence INSERTs
            ev_sql = """
            INSERT INTO kmteam.evidence
                (submission_id, metric_id, link_number, url, status_id, comment)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            for vals in to_insert:
                db.modifydatabase(ev_sql, vals)
            
            final_modal_open = True
            final_modal_header = "SDG 5 Evidences Successfully Submitted."
        
        elif create_mode == 'edit':
            # 1) figure out submission_id from the URL
            sub_id = int(parse_qs(urlparse(search).query).get('id', ['0'])[0])

            # 2) If they ticked “Mark for Deletion”, delete the entire submission:
            if removerecord:
                db.modifydatabase(  
                    """
                    UPDATE kmteam.submission 
                       SET submission_del_ind = TRUE
                     WHERE submission_id = %s
                    """,
                    [sub_id]
                )
                final_modal_open = True
                final_modal_header = "Submission Successfully Deleted."
                return [True, "Submission Successfully Deleted." , initial_modal_open, initial_modal_message, confirm_button_color, alert_open, alert_color, alert_text, sdg_submitter_className, sdg_submitter_office_className]

            # 3) Update only the submission row
            db.modifydatabase(
                """
                UPDATE kmteam.submission
                   SET submitter = %s,
                       submitter_office = %s,
                       submitted_at = CURRENT_TIMESTAMP
                 WHERE submission_id = %s
                """,
                [sdg5_submitter, sdg5_submitter_office, sub_id]
            )

            # 4) Upsert each evidence link: INSERT new ones, UPDATE only URL on conflict
            upsert_sql = """
            INSERT INTO kmteam.evidence
                (submission_id, metric_id, link_number, url, status_id, comment)
            VALUES (%s, %s, %s, %s, NULL, NULL)
            ON CONFLICT (submission_id, metric_id, link_number)
            DO UPDATE
              -- only if URL really changed:
              SET
                url       = EXCLUDED.url,
                status_id = NULL
            WHERE kmteam.evidence.url IS DISTINCT FROM EXCLUDED.url
            """

            clear_other_sql = """
            UPDATE kmteam.evidence
               SET status_id = NULL
             WHERE submission_id = %s
               AND metric_id     = %s
               AND link_number   = %s
            """

            def add_ev(code, link_no, new_url):
                if new_url in (None, ""):
                    return
                m_id = metrics_map[code]

                # 1) fetch original URL:
                df_old = db.querydatafromdatabase(
                    """
                    SELECT url
                      FROM kmteam.evidence
                     WHERE submission_id = %s
                       AND metric_id     = %s
                       AND link_number   = %s
                    """,
                    [sub_id, m_id, link_no],
                    ["url"]
                )
                old_url = df_old.at[0, "url"] if not df_old.empty else None

                # 2) if unchanged, skip entirely
                if old_url == str(new_url):
                    return

                # 3) upsert & clear status on this link
                db.modifydatabase(upsert_sql, [sub_id, m_id, link_no, str(new_url)])

                # 4) clear status on the *other* link of same metric
                other_link = 2 if link_no == 1 else 1
                db.modifydatabase(clear_other_sql, [sub_id, m_id, other_link])
            # numeric metrics — treat each as a single “link 1”
            add_ev('2.1total', 1, sdg5_2_1_total)
            add_ev('2.2total', 1, sdg5_2_2_total)
            add_ev('2.3',     1, sdg5_2_3)
            add_ev('2.4',     1, sdg5_2_4)
            add_ev('2.5',     1, sdg5_2_5)

            add_ev('3.1', 1, sdg5_3_1_evidence_link_1)
            add_ev('3.1', 2, sdg5_3_1_evidence_link_2)
            add_ev('3.2', 1, sdg5_3_2_evidence_link_1)
            add_ev('3.2', 2, sdg5_3_2_evidence_link_2)

            add_ev('3.3a', 1, sdg5_3_3_evidence_link_1a)
            add_ev('3.3a', 2, sdg5_3_3_evidence_link_2a)
            add_ev('3.3b', 1, sdg5_3_3_evidence_link_1b)
            add_ev('3.3b', 2, sdg5_3_3_evidence_link_2b)
            add_ev('3.3c', 1, sdg5_3_3_evidence_link_1c)
            add_ev('3.3c', 2, sdg5_3_3_evidence_link_2c)
            add_ev('3.3d', 1, sdg5_3_3_evidence_link_1d)
            add_ev('3.3d', 2, sdg5_3_3_evidence_link_2d)

            add_ev('3.4a', 1, sdg5_3_4_evidence_link_1a)
            add_ev('3.4a', 2, sdg5_3_4_evidence_link_2a)
            add_ev('3.4b', 1, sdg5_3_4_evidence_link_1b)
            add_ev('3.4b', 2, sdg5_3_4_evidence_link_2b)

            add_ev('4.1', 1, sdg5_4_1)
            add_ev('4.2', 1, sdg5_4_2)
            add_ev('4.3', 1, sdg5_4_3)
            add_ev('4.4', 1, sdg5_4_4)

            add_ev('5.1total',  1, sdg5_5_1_total)
            add_ev('5.1first',  1, sdg5_5_1_first)
            add_ev('5.1second', 1, sdg5_5_1_second)
            add_ev('5.1mid',    1, sdg5_5_1_mid)
            add_ev('5.2total', 1, sdg5_5_2_total)

            add_ev('5.3total',  1, sdg5_5_3_total)
            add_ev('5.3male',   1, sdg5_5_3_male)
            add_ev('5.3female', 1, sdg5_5_3_female)

            add_ev('5.4total',  1, sdg5_5_4_total)
            add_ev('5.4male',   1, sdg5_5_4_male)
            add_ev('5.4female', 1, sdg5_5_4_female)

            add_ev('5.5total',  1, sdg5_5_5_total)
            add_ev('5.5male',   1, sdg5_5_5_male)
            add_ev('5.5female', 1, sdg5_5_5_female)

            add_ev('6.1', 1, sdg5_6_1_evidence_link_1)
            add_ev('6.1', 2, sdg5_6_1_evidence_link_2)
            add_ev('6.2', 1, sdg5_6_2_evidence_link_1)
            add_ev('6.2', 2, sdg5_6_2_evidence_link_2)
            add_ev('6.3', 1, sdg5_6_3_evidence_link_1)
            add_ev('6.3', 2, sdg5_6_3_evidence_link_2)
            add_ev('6.4', 1, sdg5_6_4_evidence_link_1)
            add_ev('6.4', 2, sdg5_6_4_evidence_link_2)
            add_ev('6.5', 1, sdg5_6_5_evidence_link_1)
            add_ev('6.5', 2, sdg5_6_5_evidence_link_2)
            add_ev('6.6', 1, sdg5_6_6_evidence_link_1)
            add_ev('6.6', 2, sdg5_6_6_evidence_link_2)
            add_ev('6.7', 1, sdg5_6_7_evidence_link_1)
            add_ev('6.7', 2, sdg5_6_7_evidence_link_2)
            add_ev('6.8', 1, sdg5_6_8_evidence_link_1)
            add_ev('6.8', 2, sdg5_6_8_evidence_link_2)

            final_modal_open = True
            final_modal_header = "SDG 5 Evidences Successfully Updated."

    elif eventid == 'sdg5_initial_modal_cancel' and cancel:
        initial_modal_open = False
        initial_modal_message = ''
          
    return [final_modal_open, final_modal_header, initial_modal_open, initial_modal_message, confirm_button_color, alert_open, alert_color, alert_text, sdg_submitter_className, sdg_submitter_office_className]

@app.callback(
    [
        Output('sdg5_2_1_total_status', 'options'),
        Output('sdg5_2_2_total_status', 'options'),
        Output('sdg5_2_3_status', 'options'),
        Output('sdg5_2_4_status', 'options'),
        Output('sdg5_2_5_status', 'options'),
        Output('sdg5_3_1_status', 'options'),
        Output('sdg5_3_2_status', 'options'),
        Output('sdg5_3_3_status_a', 'options'),
        Output('sdg5_3_3_status_b', 'options'),
        Output('sdg5_3_3_status_c', 'options'),
        Output('sdg5_3_3_status_d', 'options'),
        Output('sdg5_3_4_status_a', 'options'),
        Output('sdg5_3_4_status_b', 'options'),
        Output('sdg5_4_1_status', 'options'),
        Output('sdg5_4_2_status', 'options'),
        Output('sdg5_4_3_status', 'options'),
        Output('sdg5_4_4_status', 'options'),
        Output('sdg5_5_1_total_status', 'options'),
        Output('sdg5_5_1_first_status', 'options'),
        Output('sdg5_5_1_second_status', 'options'),
        Output('sdg5_5_1_mid_status', 'options'),
        Output('sdg5_5_2_total_status', 'options'),
        Output('sdg5_5_3_total_status', 'options'),
        Output('sdg5_5_3_male_status', 'options'),
        Output('sdg5_5_3_female_status', 'options'),
        Output('sdg5_5_4_total_status', 'options'),
        Output('sdg5_5_4_male_status', 'options'),
        Output('sdg5_5_4_female_status', 'options'),
        Output('sdg5_5_5_total_status', 'options'),
        Output('sdg5_5_5_male_status', 'options'),
        Output('sdg5_5_5_female_status', 'options'),
        Output('sdg5_6_1_status', 'options'),
        Output('sdg5_6_2_status', 'options'),
        Output('sdg5_6_3_status', 'options'),
        Output('sdg5_6_4_status', 'options'),
        Output('sdg5_6_5_status', 'options'),
        Output('sdg5_6_6_status', 'options'),
        Output('sdg5_6_7_status', 'options'),
        Output('sdg5_6_8_status', 'options'),
        Output('sdg5_page_header', 'children'),
        Output('sdg5_toload', 'data'),
        Output('sdg5_removerecord_div', 'style'),
        Output('sdg5_buttons_div', 'style'),
        Output('sdg5_back_btn_div', 'style')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('currentuserid', 'data'),
        State('url', 'search')
    ]
)
def show_qao_other_options_div(pathname, userid, search):
     # Only act when we're on the specific page
    if pathname != '/sdglist/sdg5submission':
        raise PreventUpdate
    
    sql = """
        SELECT 
            checkstatus_name AS label, 
            checkstatus_id AS value
        FROM kmteam.checkstatus
    """
    values = []
    cols = ['label', 'value']
    df = db.querydatafromdatabase(sql, values, cols)
    status_options = df.to_dict('records')

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query)['mode'][0]
    if create_mode == 'add':
        header = 'Add SDG 5 Evidence Submission'
        to_load = 0
        removediv_style = {'display': 'none'}
        buttondiv_style = None
        backbtn_div_style = {'display': 'none'}
    elif create_mode == 'edit':
        header = 'Edit SDG 5 Evidence Submission'
        to_load = 1
        removediv_style = None
        buttondiv_style = None
        backbtn_div_style = {'display': 'none'}
    elif create_mode == 'view':
        header = 'View SDG 5 Evidence Submission'
        to_load = 1
        removediv_style = {'display': 'none'}
        buttondiv_style = {'display': 'none'}
        backbtn_div_style = {"display": "flex", "justifyContent": "flex-end"}


    return [status_options, status_options, status_options, status_options, status_options, 
            status_options, status_options, status_options, status_options, status_options, 
            status_options, status_options, status_options, status_options, status_options, 
            status_options, status_options, status_options, status_options, status_options,
            status_options, status_options, status_options, status_options, status_options,
            status_options, status_options, status_options, status_options, status_options,
            status_options, status_options, status_options, status_options, status_options,
            status_options, status_options, status_options, status_options, 
            header, to_load, removediv_style, buttondiv_style, backbtn_div_style]


@app.callback(
    [
        Output('sdg5_2_1_total', 'value'),
        Output('sdg5_2_2_total', 'value'),
        Output('sdg5_2_3', 'value'),
        Output('sdg5_2_4', 'value'),
        Output('sdg5_2_5', 'value'),
        Output('sdg5_3_1_evidence_link_1', 'value'),
        Output('sdg5_3_1_evidence_link_2', 'value'),
        Output('sdg5_3_2_evidence_link_1', 'value'),
        Output('sdg5_3_2_evidence_link_2', 'value'),
        Output('sdg5_3_3_evidence_link_1a', 'value'),
        Output('sdg5_3_3_evidence_link_2a', 'value'),
        Output('sdg5_3_3_evidence_link_1b', 'value'),
        Output('sdg5_3_3_evidence_link_2b', 'value'),
        Output('sdg5_3_3_evidence_link_1c', 'value'),
        Output('sdg5_3_3_evidence_link_2c', 'value'),
        Output('sdg5_3_3_evidence_link_1d', 'value'),
        Output('sdg5_3_3_evidence_link_2d', 'value'),
        Output('sdg5_3_4_evidence_link_1a', 'value'),
        Output('sdg5_3_4_evidence_link_2a', 'value'),
        Output('sdg5_3_4_evidence_link_1b', 'value'),
        Output('sdg5_3_4_evidence_link_2b', 'value'),
        Output('sdg5_4_1', 'value'),
        Output('sdg5_4_2', 'value'),
        Output('sdg5_4_3', 'value'),
        Output('sdg5_4_4', 'value'),
        Output('sdg5_5_1_total', 'value'),
        Output('sdg5_5_1_first', 'value'),
        Output('sdg5_5_1_second', 'value'),
        Output('sdg5_5_1_mid', 'value'),
        Output('sdg5_5_2_total', 'value'),
        Output('sdg5_5_3_total', 'value'),
        Output('sdg5_5_3_male', 'value'),
        Output('sdg5_5_3_female', 'value'),
        Output('sdg5_5_4_total', 'value'),
        Output('sdg5_5_4_male', 'value'),
        Output('sdg5_5_4_female', 'value'),
        Output('sdg5_5_5_total', 'value'),
        Output('sdg5_5_5_male', 'value'),
        Output('sdg5_5_5_female', 'value'),
        Output('sdg5_6_1_evidence_link_1', 'value'),
        Output('sdg5_6_1_evidence_link_2', 'value'),
        Output('sdg5_6_2_evidence_link_1', 'value'),
        Output('sdg5_6_2_evidence_link_2', 'value'),
        Output('sdg5_6_3_evidence_link_1', 'value'),
        Output('sdg5_6_3_evidence_link_2', 'value'),
        Output('sdg5_6_4_evidence_link_1', 'value'),
        Output('sdg5_6_4_evidence_link_2', 'value'),
        Output('sdg5_6_5_evidence_link_1', 'value'),
        Output('sdg5_6_5_evidence_link_2', 'value'),
        Output('sdg5_6_6_evidence_link_1', 'value'),
        Output('sdg5_6_6_evidence_link_2', 'value'),
        Output('sdg5_6_7_evidence_link_1', 'value'),
        Output('sdg5_6_7_evidence_link_2', 'value'),
        Output('sdg5_6_8_evidence_link_1', 'value'),
        Output('sdg5_6_8_evidence_link_2', 'value'),
        Output('sdg5_2_1_total_status', 'value'),
        Output('sdg5_2_2_total_status', 'value'),
        Output('sdg5_2_3_status', 'value'),
        Output('sdg5_2_4_status', 'value'),
        Output('sdg5_2_5_status', 'value'),
        Output('sdg5_3_1_status', 'value'),
        Output('sdg5_3_2_status', 'value'),
        Output('sdg5_3_3_status_a', 'value'),
        Output('sdg5_3_3_status_b', 'value'),
        Output('sdg5_3_3_status_c', 'value'),
        Output('sdg5_3_3_status_d', 'value'),
        Output('sdg5_3_4_status_a', 'value'),
        Output('sdg5_3_4_status_b', 'value'),
        Output('sdg5_4_1_status', 'value'),
        Output('sdg5_4_2_status', 'value'),
        Output('sdg5_4_3_status', 'value'),
        Output('sdg5_4_4_status', 'value'),
        Output('sdg5_5_1_total_status', 'value'),
        Output('sdg5_5_1_first_status', 'value'),
        Output('sdg5_5_1_second_status', 'value'),
        Output('sdg5_5_1_mid_status', 'value'),
        Output('sdg5_5_2_total_status', 'value'),
        Output('sdg5_5_3_total_status', 'value'),
        Output('sdg5_5_3_male_status', 'value'),
        Output('sdg5_5_3_female_status', 'value'),
        Output('sdg5_5_4_total_status', 'value'),
        Output('sdg5_5_4_male_status', 'value'),
        Output('sdg5_5_4_female_status', 'value'),
        Output('sdg5_5_5_total_status', 'value'),
        Output('sdg5_5_5_male_status', 'value'),
        Output('sdg5_5_5_female_status', 'value'),
        Output('sdg5_6_1_status', 'value'),
        Output('sdg5_6_2_status', 'value'),
        Output('sdg5_6_3_status', 'value'),
        Output('sdg5_6_4_status', 'value'),
        Output('sdg5_6_5_status', 'value'),
        Output('sdg5_6_6_status', 'value'),
        Output('sdg5_6_7_status', 'value'),
        Output('sdg5_6_8_status', 'value'),
        Output('sdg5_submitter', 'value'),
        Output('sdg5_submitter_office', 'value'),
    ],
    Input('sdg5_toload', 'modified_timestamp'),
    [
        State('sdg5_toload', 'data'),
        State('url', 'search')
    ]
)
def sdg5evidences_load(ts, toload, search):
    if not toload:
        raise PreventUpdate

    # parse URL params
    qs = parse_qs(urlparse(search).query)
    mode = qs.get('mode',[''])[0]
    sub_id = int(qs.get('id',['0'])[0])

    # load submission
    sub = db.querydatafromdatabase(
        "SELECT submitter, submitter_office FROM kmteam.submission WHERE submission_id=%s",
        [sub_id],
        ['submitter','office']
    )
    submitter = sub.at[0,'submitter']
    office    = sub.at[0,'office']

    # load evidence rows
    ev_df = db.querydatafromdatabase(
        """
        SELECT m.code, e.link_number AS link, e.url, e.status_id AS status
        FROM kmteam.evidence e
        JOIN kmteam.metric   m ON m.metric_id = e.metric_id
        WHERE e.submission_id = %s
        """,
        [sub_id],
        ['code','link','url','status']
    )

    # map (code,link) → (input_id, status_id)
    comp_map = {
    ('2.1total', 1): ('sdg5_2_1_total',       'sdg5_2_1_total_status'),
    ('2.2total', 1): ('sdg5_2_2_total',       'sdg5_2_2_total_status'),
    ('2.3',       1): ('sdg5_2_3',             'sdg5_2_3_status'),
    ('2.4',       1): ('sdg5_2_4',             'sdg5_2_4_status'),
    ('2.5',       1): ('sdg5_2_5',             'sdg5_2_5_status'),

    # sdg5_3_1 and 5_3_2 (no letter suffix)
    ('3.1', 1): ('sdg5_3_1_evidence_link_1', 'sdg5_3_1_status'),
    ('3.1', 2): ('sdg5_3_1_evidence_link_2', 'sdg5_3_1_status'),
    ('3.2', 1): ('sdg5_3_2_evidence_link_1', 'sdg5_3_2_status'),
    ('3.2', 2): ('sdg5_3_2_evidence_link_2', 'sdg5_3_2_status'),

    # sdg5_3_3 (letters a–d)
    ('3.3a', 1): ('sdg5_3_3_evidence_link_1a', 'sdg5_3_3_status_a'),
    ('3.3a', 2): ('sdg5_3_3_evidence_link_2a', 'sdg5_3_3_status_a'),
    ('3.3b', 1): ('sdg5_3_3_evidence_link_1b', 'sdg5_3_3_status_b'),
    ('3.3b', 2): ('sdg5_3_3_evidence_link_2b', 'sdg5_3_3_status_b'),
    ('3.3c', 1): ('sdg5_3_3_evidence_link_1c', 'sdg5_3_3_status_c'),
    ('3.3c', 2): ('sdg5_3_3_evidence_link_2c', 'sdg5_3_3_status_c'),
    ('3.3d', 1): ('sdg5_3_3_evidence_link_1d', 'sdg5_3_3_status_d'),
    ('3.3d', 2): ('sdg5_3_3_evidence_link_2d', 'sdg5_3_3_status_d'),

    # sdg5_3_4 (letters a–b)
    ('3.4a', 1): ('sdg5_3_4_evidence_link_1a', 'sdg5_3_4_status_a'),
    ('3.4a', 2): ('sdg5_3_4_evidence_link_2a', 'sdg5_3_4_status_a'),
    ('3.4b', 1): ('sdg5_3_4_evidence_link_1b', 'sdg5_3_4_status_b'),
    ('3.4b', 2): ('sdg5_3_4_evidence_link_2b', 'sdg5_3_4_status_b'),

    # sdg5_4_1 to 5_4_4 (single values)
    ('4.1', 1): ('sdg5_4_1', 'sdg5_4_1_status'),
    ('4.2', 1): ('sdg5_4_2', 'sdg5_4_2_status'),
    ('4.3', 1): ('sdg5_4_3', 'sdg5_4_3_status'),
    ('4.4', 1): ('sdg5_4_4', 'sdg5_4_4_status'),

    # sdg5_5_1 (total, first, second, mid)
    ('5.1total', 1): ('sdg5_5_1_total',  'sdg5_5_1_total_status'),
    ('5.1first', 1): ('sdg5_5_1_first',  'sdg5_5_1_first_status'),
    ('5.1second',1): ('sdg5_5_1_second', 'sdg5_5_1_second_status'),
    ('5.1mid',   1): ('sdg5_5_1_mid',    'sdg5_5_1_mid_status'),

    # sdg5_5_2
    ('5.2total', 1): ('sdg5_5_2_total', 'sdg5_5_2_total_status'),

    # sdg5_5_3 and 5_5_4, 5_5_5 (total, male, female)
    ('5.3total',  1): ('sdg5_5_3_total',  'sdg5_5_3_total_status'),
    ('5.3male',   1): ('sdg5_5_3_male',   'sdg5_5_3_male_status'),
    ('5.3female', 1): ('sdg5_5_3_female', 'sdg5_5_3_female_status'),

    ('5.4total',  1): ('sdg5_5_4_total',  'sdg5_5_4_total_status'),
    ('5.4male',   1): ('sdg5_5_4_male',   'sdg5_5_4_male_status'),
    ('5.4female', 1): ('sdg5_5_4_female', 'sdg5_5_4_female_status'),

    ('5.5total',  1): ('sdg5_5_5_total',  'sdg5_5_5_total_status'),
    ('5.5male',   1): ('sdg5_5_5_male',   'sdg5_5_5_male_status'),
    ('5.5female', 1): ('sdg5_5_5_female', 'sdg5_5_5_female_status'),

    # sdg5_6_1 through 5_6_8 (each with two evidence links, no letter suffix)
    ('6.1', 1): ('sdg5_6_1_evidence_link_1', 'sdg5_6_1_status'),
    ('6.1', 2): ('sdg5_6_1_evidence_link_2', 'sdg5_6_1_status'),
    ('6.2', 1): ('sdg5_6_2_evidence_link_1', 'sdg5_6_2_status'),
    ('6.2', 2): ('sdg5_6_2_evidence_link_2', 'sdg5_6_2_status'),
    ('6.3', 1): ('sdg5_6_3_evidence_link_1', 'sdg5_6_3_status'),
    ('6.3', 2): ('sdg5_6_3_evidence_link_2', 'sdg5_6_3_status'),
    ('6.4', 1): ('sdg5_6_4_evidence_link_1', 'sdg5_6_4_status'),
    ('6.4', 2): ('sdg5_6_4_evidence_link_2', 'sdg5_6_4_status'),
    ('6.5', 1): ('sdg5_6_5_evidence_link_1', 'sdg5_6_5_status'),
    ('6.5', 2): ('sdg5_6_5_evidence_link_2', 'sdg5_6_5_status'),
    ('6.6', 1): ('sdg5_6_6_evidence_link_1', 'sdg5_6_6_status'),
    ('6.6', 2): ('sdg5_6_6_evidence_link_2', 'sdg5_6_6_status'),
    ('6.7', 1): ('sdg5_6_7_evidence_link_1', 'sdg5_6_7_status'),
    ('6.7', 2): ('sdg5_6_7_evidence_link_2', 'sdg5_6_7_status'),
    ('6.8', 1): ('sdg5_6_8_evidence_link_1', 'sdg5_6_8_status'),
    ('6.8', 2): ('sdg5_6_8_evidence_link_2', 'sdg5_6_8_status'),
    }

    # initialize all values to None (so missing ones stay blank)
    values = {inp: None for inp,_ in comp_map.values()}
    values.update({st:  None for _,st in comp_map.values()})
    values['sdg5_2_1_total'] = None
    values['sdg5_2_2_total'] = None
    values['sdg5_2_3'] = None
    values['sdg5_2_4'] = None
    values['sdg5_2_5'] = None
    values['sdg5_4_1'] = None
    values['sdg5_4_2'] = None
    values['sdg5_4_3'] = None
    values['sdg5_4_4'] = None
    values['sdg5_5_1_total'] = None
    values['sdg5_5_1_first'] = None
    values['sdg5_5_1_second'] = None
    values['sdg5_5_1_mid'] = None
    values['sdg5_5_2_total'] = None
    values['sdg5_5_3_total'] = None
    values['sdg5_5_3_male'] = None
    values['sdg5_5_3_female'] = None
    values['sdg5_5_4_total'] = None
    values['sdg5_5_4_male'] = None
    values['sdg5_5_4_female'] = None
    values['sdg5_5_5_total'] = None
    values['sdg5_5_5_male'] = None
    values['sdg5_5_5_female'] = None
    values['sdg5_submitter'] = submitter
    values['sdg5_submitter_office'] = office

    # populate from DB
    for _, r in ev_df.iterrows():
        cid = (r['code'], int(r['link']))
        inp_id, st_id = comp_map[cid]
        # numeric metrics go back to float
        if cid[0] in ('2.1total','2.2total', '2.3','2.4', '2.5','4.1', '4.2','4.3', '4.4', '5.1total', '5.1first', '5.1second', '5.1mid', '5.2total', 
                      '5.3total', '5.3male', '5.3female', '5.4total', '5.4male', '5.4female', '5.5total', '5.5male', '5.5female'):
            values[inp_id] = float(r['url'])
        else:
            values[inp_id] = r['url']
        values[st_id] = r['status']

    # return in the exact order of your Outputs
    return [
      values['sdg5_2_1_total'], values['sdg5_2_2_total'], values['sdg5_2_3'], values['sdg5_2_4'], values['sdg5_2_5'], 
      values['sdg5_3_1_evidence_link_1'], values['sdg5_3_1_evidence_link_2'], values['sdg5_3_2_evidence_link_1'], 
      values['sdg5_3_2_evidence_link_2'], values['sdg5_3_3_evidence_link_1a'], values['sdg5_3_3_evidence_link_2a'], 
      values['sdg5_3_3_evidence_link_1b'], values['sdg5_3_3_evidence_link_2b'], values['sdg5_3_3_evidence_link_1c'], 
      values['sdg5_3_3_evidence_link_2c'], values['sdg5_3_3_evidence_link_1d'], values['sdg5_3_3_evidence_link_2d'], 
      values['sdg5_3_4_evidence_link_1a'], values['sdg5_3_4_evidence_link_2a'], values['sdg5_3_4_evidence_link_1b'], 
      values['sdg5_3_4_evidence_link_2b'], values['sdg5_4_1'], values['sdg5_4_2'], values['sdg5_4_3'], values['sdg5_4_4'], 
      values['sdg5_5_1_total'], values['sdg5_5_1_first'], values['sdg5_5_1_second'], values['sdg5_5_1_mid'], values['sdg5_5_2_total'], 
      values['sdg5_5_3_total'], values['sdg5_5_3_male'], values['sdg5_5_3_female'], values['sdg5_5_4_total'], values['sdg5_5_4_male'], 
      values['sdg5_5_4_female'], values['sdg5_5_5_total'], values['sdg5_5_5_male'], values['sdg5_5_5_female'], values['sdg5_6_1_evidence_link_1'], 
      values['sdg5_6_1_evidence_link_2'], values['sdg5_6_2_evidence_link_1'], values['sdg5_6_2_evidence_link_2'], values['sdg5_6_3_evidence_link_1'], 
      values['sdg5_6_3_evidence_link_2'], values['sdg5_6_4_evidence_link_1'], values['sdg5_6_4_evidence_link_2'], values['sdg5_6_5_evidence_link_1'], 
      values['sdg5_6_5_evidence_link_2'], values['sdg5_6_6_evidence_link_1'], values['sdg5_6_6_evidence_link_2'], values['sdg5_6_7_evidence_link_1'], 
      values['sdg5_6_7_evidence_link_2'], values['sdg5_6_8_evidence_link_1'], values['sdg5_6_8_evidence_link_2'], values['sdg5_2_1_total_status'], 
      values['sdg5_2_2_total_status'], values['sdg5_2_3_status'], values['sdg5_2_4_status'], values['sdg5_2_5_status'], values['sdg5_3_1_status'], 
      values['sdg5_3_2_status'], values['sdg5_3_3_status_a'], values['sdg5_3_3_status_b'], values['sdg5_3_3_status_c'], values['sdg5_3_3_status_d'], 
      values['sdg5_3_4_status_a'], values['sdg5_3_4_status_b'], values['sdg5_4_1_status'], values['sdg5_4_2_status'], values['sdg5_4_3_status'], 
      values['sdg5_4_4_status'], values['sdg5_5_1_total_status'], values['sdg5_5_1_first_status'], values['sdg5_5_1_second_status'], values['sdg5_5_1_mid_status'], 
      values['sdg5_5_2_total_status'], values['sdg5_5_3_total_status'], values['sdg5_5_3_male_status'], values['sdg5_5_3_female_status'], 
      values['sdg5_5_4_total_status'], values['sdg5_5_4_male_status'], values['sdg5_5_4_female_status'], values['sdg5_5_5_total_status'], 
      values['sdg5_5_5_male_status'], values['sdg5_5_5_female_status'], values['sdg5_6_1_status'], values['sdg5_6_2_status'], values['sdg5_6_3_status'], 
      values['sdg5_6_4_status'], values['sdg5_6_5_status'], values['sdg5_6_6_status'], values['sdg5_6_7_status'], values['sdg5_6_8_status'],
      values['sdg5_submitter'], values['sdg5_submitter_office']
    ]


@app.callback(
    [
        Output("sdg5_comment_modal", "is_open"),
        Output("sdg5_comment_modal_header", "children"),
        Output("sdg5_comment_modal_body", "children"),
    ],
    # Inputs: all comment-buttons + the modal Close button
    [
        Input("sdg5_2_1_total_comment", "n_clicks"),
        Input("sdg5_2_2_total_comment", "n_clicks"),
        Input("sdg5_2_3_comment", "n_clicks"),
        Input("sdg5_2_4_comment", "n_clicks"),
        Input("sdg5_2_5_comment", "n_clicks"),
        Input("sdg5_3_1_comment", "n_clicks"),
        Input("sdg5_3_2_comment", "n_clicks"),
        Input("sdg5_3_3_comment_a", "n_clicks"),
        Input("sdg5_3_3_comment_b", "n_clicks"),
        Input("sdg5_3_3_comment_c", "n_clicks"),
        Input("sdg5_3_3_comment_d", "n_clicks"),
        Input("sdg5_3_4_comment_a", "n_clicks"),
        Input("sdg5_3_4_comment_b", "n_clicks"),
        Input("sdg5_4_1_comment", "n_clicks"),
        Input("sdg5_4_2_comment", "n_clicks"),
        Input("sdg5_4_3_comment", "n_clicks"),
        Input("sdg5_4_4_comment", "n_clicks"),
        Input("sdg5_5_1_total_comment", "n_clicks"),
        Input("sdg5_5_1_first_comment", "n_clicks"),
        Input("sdg5_5_1_second_comment", "n_clicks"),
        Input("sdg5_5_1_mid_comment", "n_clicks"),
        Input("sdg5_5_2_total_comment", "n_clicks"),
        Input("sdg5_5_3_total_comment", "n_clicks"),
        Input("sdg5_5_3_male_comment", "n_clicks"),
        Input("sdg5_5_3_female_comment", "n_clicks"),
        Input("sdg5_5_4_total_comment", "n_clicks"),
        Input("sdg5_5_4_male_comment", "n_clicks"),
        Input("sdg5_5_4_female_comment", "n_clicks"),
        Input("sdg5_5_5_total_comment", "n_clicks"),
        Input("sdg5_5_5_male_comment", "n_clicks"),
        Input("sdg5_5_5_female_comment", "n_clicks"),
        Input("sdg5_6_1_comment", "n_clicks"),
        Input("sdg5_6_2_comment", "n_clicks"),
        Input("sdg5_6_3_comment", "n_clicks"),
        Input("sdg5_6_4_comment", "n_clicks"),
        Input("sdg5_6_5_comment", "n_clicks"),
        Input("sdg5_6_6_comment", "n_clicks"),
        Input("sdg5_6_7_comment", "n_clicks"),
        Input("sdg5_6_8_comment", "n_clicks"),
        Input("sdg5_comment_modal_close", "n_clicks"),
    ],
    [ State("url", "search") ]  # to get submission_id from the URL
)
def display_comment(
    btn_1, btn_2,
    btn_3, btn_4, btn_5, btn_6, btn_7, btn_8,
    btn_9, btn_10, btn_11, btn_12, btn_13,
    btn_14, btn_15, btn_16, btn_17, btn_18, btn_19, btn_20,
    btn_21, btn_22, btn_23, btn_24, btn_25, btn_26, btn_27, btn_28, btn_29, btn_30,
    btn_31, btn_32, btn_33, btn_34, btn_35, btn_36, btn_37, btn_38, btn_39,
    btn_close,
    search
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # If Close button clicked, just hide
    if clicked_id == "sdg5_comment_modal_close":
        return False, dash.no_update, dash.no_update

    # map button id → (metric_code, link_number)
    btn_map = {
        "sdg5_2_1_total_comment":    ("2.1total",   1),
        "sdg5_2_2_total_comment":    ("2.2total",   1),
        "sdg5_2_3_comment":          ("2.3",        1),
        "sdg5_2_4_comment":          ("2.4",        1),
        "sdg5_2_5_comment":          ("2.5",        1),

        "sdg5_3_1_comment":          ("3.1",        1),
        "sdg5_3_2_comment":          ("3.2",        1),
        "sdg5_3_3_comment_a":        ("3.3a",       1),
        "sdg5_3_3_comment_b":        ("3.3b",       1),
        "sdg5_3_3_comment_c":        ("3.3c",       1),
        "sdg5_3_3_comment_d":        ("3.3d",       1),

        "sdg5_3_4_comment_a":        ("3.4a",       1),
        "sdg5_3_4_comment_b":        ("3.4b",       1),

        "sdg5_4_1_comment":          ("4.1",        1),
        "sdg5_4_2_comment":          ("4.2",        1),
        "sdg5_4_3_comment":          ("4.3",        1),
        "sdg5_4_4_comment":          ("4.4",        1),

        "sdg5_5_1_total_comment":    ("5.1total",   1),
        "sdg5_5_1_first_comment":    ("5.1first",   1),
        "sdg5_5_1_second_comment":   ("5.1second",  1),
        "sdg5_5_1_mid_comment":      ("5.1mid",     1),

        "sdg5_5_2_total_comment":    ("5.2total",   1),

        "sdg5_5_3_total_comment":    ("5.3total",   1),
        "sdg5_5_3_male_comment":     ("5.3male",    1),
        "sdg5_5_3_female_comment":   ("5.3female",  1),

        "sdg5_5_4_total_comment":    ("5.4total",   1),
        "sdg5_5_4_male_comment":     ("5.4male",    1),
        "sdg5_5_4_female_comment":   ("5.4female",  1),

        "sdg5_5_5_total_comment":    ("5.5total",   1),
        "sdg5_5_5_male_comment":     ("5.5male",    1),
        "sdg5_5_5_female_comment":   ("5.5female",  1),

        "sdg5_6_1_comment":          ("6.1",        1),
        "sdg5_6_2_comment":          ("6.2",        1),
        "sdg5_6_3_comment":          ("6.3",        1),
        "sdg5_6_4_comment":          ("6.4",        1),
        "sdg5_6_5_comment":          ("6.5",        1),
        "sdg5_6_6_comment":          ("6.6",        1),
        "sdg5_6_7_comment":          ("6.7",        1),
        "sdg5_6_8_comment":          ("6.8",        1),
    }
    if clicked_id not in btn_map:
        # safety
        raise PreventUpdate

    code, link_no = btn_map[clicked_id] 

    # parse submission_id from URL
    qs = parse_qs(urlparse(search).query)
    sub_id = int(qs.get("id", ["0"])[0])

    # fetch the comment from the DB
    metric_id = metrics_map[code]
    sql = """
        SELECT comment
        FROM kmteam.evidence
        WHERE submission_id = %s
          AND metric_id     = %s
          AND link_number   = %s
    """
    df = db.querydatafromdatabase(sql, [sub_id, metric_id, link_no], ["comment"])

    if df.empty or not df.at[0, "comment"]:
        body = "There are no comments for this evidence."
    else:
        body = df.at[0, "comment"]

    header = f"Comments for this evidence"
    return True, header, body

@app.callback(
    [
        Output('sdg5_2_1_total_status', 'disabled'),
        Output('sdg5_2_2_total_status', 'disabled'),
        Output('sdg5_2_3_status', 'disabled'),
        Output('sdg5_2_4_status', 'disabled'),
        Output('sdg5_2_5_status', 'disabled'),
        Output('sdg5_3_1_status', 'disabled'),
        Output('sdg5_3_2_status', 'disabled'),
        Output('sdg5_3_3_status_a', 'disabled'),
        Output('sdg5_3_3_status_b', 'disabled'),
        Output('sdg5_3_3_status_c', 'disabled'),
        Output('sdg5_3_3_status_d', 'disabled'),
        Output('sdg5_3_4_status_a', 'disabled'),
        Output('sdg5_3_4_status_b', 'disabled'),
        Output('sdg5_4_1_status', 'disabled'),
        Output('sdg5_4_2_status', 'disabled'),
        Output('sdg5_4_3_status', 'disabled'),
        Output('sdg5_4_4_status', 'disabled'),
        Output('sdg5_5_1_total_status', 'disabled'),
        Output('sdg5_5_1_first_status', 'disabled'),
        Output('sdg5_5_1_second_status', 'disabled'),
        Output('sdg5_5_1_mid_status', 'disabled'),
        Output('sdg5_5_2_total_status', 'disabled'),
        Output('sdg5_5_3_total_status', 'disabled'),
        Output('sdg5_5_3_male_status', 'disabled'),
        Output('sdg5_5_3_female_status', 'disabled'),
        Output('sdg5_5_4_total_status', 'disabled'),
        Output('sdg5_5_4_male_status', 'disabled'),
        Output('sdg5_5_4_female_status', 'disabled'),
        Output('sdg5_5_5_total_status', 'disabled'),
        Output('sdg5_5_5_male_status', 'disabled'),
        Output('sdg5_5_5_female_status', 'disabled'),
        Output('sdg5_6_1_status', 'disabled'),
        Output('sdg5_6_2_status', 'disabled'),
        Output('sdg5_6_3_status', 'disabled'),
        Output('sdg5_6_4_status', 'disabled'),
        Output('sdg5_6_5_status', 'disabled'),
        Output('sdg5_6_6_status', 'disabled'),
        Output('sdg5_6_7_status', 'disabled'),
        Output('sdg5_6_8_status', 'disabled'),
    ],
    Input('url', 'pathname')
)
def show_qao_other_options_div(pathname):
    # Only act when we're on the specific page
    if pathname != '/sdglist/sdg5submission':
        raise PreventUpdate

    return [True]*39
            

@app.callback(
    [
        # 5.2
        Output("sdg5_2_1_total_alert", "style"),
        Output("sdg5_2_2_total_alert", "style"),
        Output("sdg5_2_3_alert",       "style"),
        Output("sdg5_2_4_alert",       "style"),
        Output("sdg5_2_5_alert",       "style"),
        # 5.3
        Output("sdg5_3_1_alert",       "style"),
        Output("sdg5_3_2_alert",       "style"),
        Output("sdg5_3_3_alert_a",     "style"),
        Output("sdg5_3_3_alert_b",     "style"),
        Output("sdg5_3_3_alert_c",     "style"),
        Output("sdg5_3_3_alert_d",     "style"),
        Output("sdg5_3_4_alert_a",     "style"),
        Output("sdg5_3_4_alert_b",     "style"),
        # 5.4
        Output("sdg5_4_1_alert",       "style"),
        Output("sdg5_4_2_alert",       "style"),
        Output("sdg5_4_3_alert",       "style"),
        Output("sdg5_4_4_alert",       "style"),
        # 5.5
        Output("sdg5_5_1_total_alert",  "style"),
        Output("sdg5_5_1_first_alert",  "style"),
        Output("sdg5_5_1_second_alert", "style"),
        Output("sdg5_5_1_mid_alert",    "style"),
        Output("sdg5_5_2_total_alert",  "style"),
        Output("sdg5_5_3_total_alert",  "style"),
        Output("sdg5_5_3_male_alert",   "style"),
        Output("sdg5_5_3_female_alert", "style"),
        Output("sdg5_5_4_total_alert",  "style"),
        Output("sdg5_5_4_male_alert",   "style"),
        Output("sdg5_5_4_female_alert", "style"),
        Output("sdg5_5_5_total_alert",  "style"),
        Output("sdg5_5_5_male_alert",   "style"),
        Output("sdg5_5_5_female_alert", "style"),
        # 5.6
        Output("sdg5_6_1_alert",       "style"),
        Output("sdg5_6_2_alert",       "style"),
        Output("sdg5_6_3_alert",       "style"),
        Output("sdg5_6_4_alert",       "style"),
        Output("sdg5_6_5_alert",       "style"),
        Output("sdg5_6_6_alert",       "style"),
        Output("sdg5_6_7_alert",       "style"),
        Output("sdg5_6_8_alert",       "style"),
    ],
    Input('url', 'pathname'),
    State('url', 'search'),
)
def show_alert(pathname, search):
    if pathname != '/sdglist/sdg5submission':
        raise PreventUpdate

    qs = parse_qs(urlparse(search).query)
    try:
        sub_id = int(qs.get('id', [''])[0])
    except:
        return [{"display": "none"}] * 39

    sql = """
        SELECT m.code, e.link_number, e.status_id
          FROM kmteam.evidence e
          JOIN kmteam.metric  m ON e.metric_id = m.metric_id
         WHERE e.submission_id = %s
    """
    df = db.querydatafromdatabase(sql, [sub_id], ["code", "link", "status_id"])
    status_map = {(row.code, row.link): row.status_id for _, row in df.iterrows()}

    groups = [
        # 5.2
        [("2.1total", 1)],
        [("2.2total", 1)],
        [("2.3",      1)],
        [("2.4",      1)],
        [("2.5",      1)],

        # 5.3
        [("3.1",     1), ("3.1",     2)],
        [("3.2",     1), ("3.2",     2)],
        [("3.3a",    1), ("3.3a",    2)],
        [("3.3b",    1), ("3.3b",    2)],
        [("3.3c",    1), ("3.3c",    2)],
        [("3.3d",    1), ("3.3d",    2)],
        [("3.4a",    1), ("3.4a",    2)],
        [("3.4b",    1), ("3.4b",    2)],

        # 5.4
        [("4.1",     1)],
        [("4.2",     1)],
        [("4.3",     1)],
        [("4.4",     1)],

        # 5.5
        [("5.1total", 1)],
        [("5.1first", 1)],
        [("5.1second",1)],
        [("5.1mid",   1)],
        [("5.2total", 1)],
        [("5.3total", 1)],
        [("5.3male",  1)],
        [("5.3female",1)],
        [("5.4total", 1)],
        [("5.4male",  1)],
        [("5.4female",1)],
        [("5.5total", 1)],
        [("5.5male",  1)],
        [("5.5female",1)],

        # 5.6
        [("6.1", 1), ("6.1", 2)],
        [("6.2", 1), ("6.2", 2)],
        [("6.3", 1), ("6.3", 2)],
        [("6.4", 1), ("6.4", 2)],
        [("6.5", 1), ("6.5", 2)],
        [("6.6", 1), ("6.6", 2)],
        [("6.7", 1), ("6.7", 2)],
        [("6.8", 1), ("6.8", 2)],
    ]

    def style_for(group):
        for code, ln in group:
            if status_map.get((code, ln)) in (1, 3):
                return {"display": "block"}
        return {"display": "none"}

    return [style_for(g) for g in groups]


@app.callback(
    [
        Output("header_sdg5_2_alert", "style"),
        Output("header_sdg5_3_alert", "style"),
        Output("header_sdg5_4_alert", "style"),
        Output("header_sdg5_5_alert", "style"),
        Output("header_sdg5_6_alert", "style"),
    ],
    Input('url', 'pathname'),
    State('url', 'search'),
)
def show_section_headers(pathname, search):
    if pathname != '/sdglist/sdg5submission':
        raise PreventUpdate

    qs = parse_qs(urlparse(search).query)
    try:
        sub_id = int(qs.get('id', [''])[0])
    except:
        return [{"display": "none"}] * 5

    df = db.querydatafromdatabase(
        """
        SELECT m.code, e.link_number, e.status_id
          FROM kmteam.evidence e
          JOIN kmteam.metric  m ON e.metric_id = m.metric_id
         WHERE e.submission_id = %s
        """,
        [sub_id],
        ["code", "link", "status_id"],
    )
    status_map = {(row.code, row.link): row.status_id for _, row in df.iterrows()}

    section_groups = {
        "5.2": [
            ("2.1total", 1), ("2.2total", 1), ("2.3", 1), ("2.4", 1), ("2.5", 1),
        ],
        "5.3": [
            ("3.1", 1),("3.1",2),("3.2",1),("3.2",2),
            ("3.3a",1),("3.3a",2),("3.3b",1),("3.3b",2),
            ("3.3c",1),("3.3c",2),("3.3d",1),("3.3d",2),
            ("3.4a",1),("3.4a",2),("3.4b",1),("3.4b",2),
        ],
        "5.4": [
            ("4.1",1),("4.2",1),("4.3",1),("4.4",1),
        ],
        "5.5": [
            ("5.1total",1),("5.1first",1),("5.1second",1),("5.1mid",1),
            ("5.2total",1),
            ("5.3total",1),("5.3male",1),("5.3female",1),
            ("5.4total",1),("5.4male",1),("5.4female",1),
            ("5.5total",1),("5.5male",1),("5.5female",1),
        ],
        "5.6": [
            ("6.1",1),("6.1",2),("6.2",1),("6.2",2),
            ("6.3",1),("6.3",2),("6.4",1),("6.4",2),
            ("6.5",1),("6.5",2),("6.6",1),("6.6",2),
            ("6.7",1),("6.7",2),("6.8",1),("6.8",2),
        ],
    }

    def any_flag(pairs):
        return any(status_map.get(pair) in (1, 3) for pair in pairs)

    def style_for(flag):
        return {"display": "block"} if flag else {"display": "none"}

    return [
        style_for(any_flag(section_groups["5.2"])),
        style_for(any_flag(section_groups["5.3"])),
        style_for(any_flag(section_groups["5.4"])),
        style_for(any_flag(section_groups["5.5"])),
        style_for(any_flag(section_groups["5.6"])),
    ]
