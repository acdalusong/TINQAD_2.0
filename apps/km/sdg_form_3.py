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
    [3],
    ["metric_id","code"]
)
metrics_map = dict(zip(all_metrics["code"], all_metrics["metric_id"]))

# ─────────────── Load metric additional info ───────────────
metric_info_df = db.querydatafromdatabase(
    "SELECT code, additional_information FROM kmteam.metric WHERE sdg_number = %s",
    [3],
    ["code","additional_information"],
)
additional_info = dict(
    zip(metric_info_df["code"], metric_info_df["additional_information"])
)


# SDG 3 Form layout
sdg3_form = dbc.Form([
    # ─────────────── Submitter’s Profile ───────────────
    dbc.Card([
        dbc.CardHeader(
            html.H5("Submitter's Profile"),
            style={"backgroundColor": highlight_colors['secondary'], "color": "white"},
        ),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(dbc.Label("Name of Submitter"), width=6),
                dbc.Col(dbc.Input(id="sdg3_submitter", type="text"), width=6),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Label("Submitter's Office"), width=6),
                dbc.Col(dbc.Input(id="sdg3_submitter_office", type="text"), width=6),
            ], className="mb-3"),
        ]),
    ], className="mb-4"),

    # ─────────────── 3.2: Proportion of graduates in health professions ───────────────
    dbc.Accordion([
        dbc.AccordionItem([
            # Header with Alert
            dbc.Row([
                dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=8),
                dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
            ], className="mb-3"),

            # Total
            dbc.Row([
                dbc.Col(html.Label("Total Number of graduates", id="label-2-1", style={"fontStyle":"italic", "cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg3_2_1_total", type="number", min=0, disabled=True), width=4),
                dbc.Col(dbc.Select(id="sdg3_2_1_total_status"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_2_1_total_comment", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_2_1_total_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # First Semester
            dbc.Row([
                dbc.Col(html.Label("First Semester", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_2_1_first", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg3_2_1_first_status"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_2_1_first_comment", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_2_1_first_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Second Semester
            dbc.Row([
                dbc.Col(html.Label("Second Semester", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_2_1_second", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg3_2_1_second_status"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_2_1_second_comment", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_2_1_second_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # Mid Year
            dbc.Row([
                dbc.Col(html.Label("Mid Year", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_2_1_mid", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg3_2_1_mid_status"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_2_1_mid_comment", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_2_1_mid_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.2.2: Number of graduates in health professions — Total
            dbc.Row([
                dbc.Col(html.Label("Number of graduates in health professions", id="label-2-2", style={"fontStyle":"italic", "cursor":"help"}), width=4),
                dbc.Col(dbc.Input(id="sdg3_2_2_total", type="number", min=0, disabled=True), width=4),
                dbc.Col(dbc.Select(id="sdg3_2_2_total_status"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_2_2_total_comment", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_2_2_total_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.2.2: First Semester
            dbc.Row([
                dbc.Col(html.Label("First Semester", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_2_2_first", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg3_2_2_first_status"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_2_2_first_comment", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_2_2_first_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.2.2: Second Semester
            dbc.Row([
                dbc.Col(html.Label("Second Semester", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_2_2_second", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg3_2_2_second_status"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_2_2_second_comment", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_2_2_second_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.2.2: Mid Year
            dbc.Row([
                dbc.Col(html.Label("Mid Year", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_2_2_mid", type="number", min=0), width=4),
                dbc.Col(dbc.Select(id="sdg3_2_2_mid_status"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_2_2_mid_comment", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_2_2_mid_alert", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),
        ],
        title=html.Div(
                    [
                        html.Span("3.2 Proportion of graduates in health professions", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg3_2_alert",
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

        # ─────────────── 3.3: Lifelong learning measures ───────────────
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

            dbc.Row(dbc.Col(html.Label("Current collaborations with health institutions:", id="label-3-1", style={"fontStyle":"italic", "cursor":"help"}), width=12), className="mb-2"),
            # 3.3.1 Local health institutions
            dbc.Row([
                dbc.Col(html.Label("Local health institutions", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_1_evidence_link_1a", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_1_evidence_link_2a", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_1_status_a"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_1_comment_a", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_1_alert_a", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.1 National health institutions
            dbc.Row([
                dbc.Col(html.Label("National health institutions", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_1_evidence_link_1b", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_1_evidence_link_2b", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_1_status_b"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_1_comment_b", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_1_alert_b", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.1 Global health institutions
            dbc.Row([
                dbc.Col(html.Label("Global health institutions", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_1_evidence_link_1c", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_1_evidence_link_2c", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_1_status_c"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_1_comment_c", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_1_alert_c", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row(dbc.Col(html.Label("Health outreach programmes:", id="label-3-2", style={"fontStyle":"italic", "cursor":"help"}), width=12), className="mb-2"),
            # 3.3.2 Local communities
            dbc.Row([
                dbc.Col(html.Label("Local communities", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_2_evidence_link_1a", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_2_evidence_link_2a", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_2_status_a"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_2_comment_a", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_2_alert_a", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.2 Disadvantaged people
            dbc.Row([
                dbc.Col(html.Label("Disadvantaged people", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_2_evidence_link_1b", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_2_evidence_link_2b", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_2_status_b"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_2_comment_b", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_2_alert_b", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.2 Refugee immigrant communities
            dbc.Row([
                dbc.Col(html.Label("Refugee immigrant communities", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_2_evidence_link_1c", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_2_evidence_link_2c", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_2_status_c"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_2_comment_c", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_2_alert_c", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row(dbc.Col(html.Label("Shared sports facilities:", id="label-3-3", style={"fontStyle":"italic", "cursor":"help"}), width=12), className="mb-2"),
            # 3.3.3 Free access to ALL facilities
            dbc.Row([
                dbc.Col(html.Label("Free access to ALL facilities", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_3_evidence_link_1a", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_3_evidence_link_2a", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_3_status_a"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_3_comment_a", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_3_alert_a", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.3 Free access to SOME facilities
            dbc.Row([
                dbc.Col(html.Label("Free access to SOME facilities", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_3_evidence_link_1b", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_3_evidence_link_2b", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_3_status_b"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_3_comment_b", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_3_alert_b", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.3 Charged access ONLY
            dbc.Row([
                dbc.Col(html.Label("Charged access ONLY", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_3_evidence_link_1c", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_3_evidence_link_2c", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_3_status_c"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_3_comment_c", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_3_alert_c", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row(dbc.Col(html.Label("Sexual and reproductive health care services for students:", id="label-3-4", style={"fontStyle":"italic", "cursor":"help"}), width=12), className="mb-2"),
            # 3.3.4 Free access
            dbc.Row([
                dbc.Col(html.Label("Free access", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_4_evidence_link_1a", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_4_evidence_link_2a", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_4_status_a"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_4_comment_a", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_4_alert_a", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.4 Charged access
            dbc.Row([
                dbc.Col(html.Label("Charged access", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_4_evidence_link_1b", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_4_evidence_link_2b", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_4_status_b"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_4_comment_b", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_4_alert_b", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row(dbc.Col(html.Label("Mental health support:", id="label-3-5", style={"fontStyle":"italic", "cursor":"help"}), width=12), className="mb-2"),
            # 3.3.5 Active promotion of good mental health
            dbc.Row([
                dbc.Col(html.Label("Active promotion of good mental health", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_5_evidence_link_1a", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_5_evidence_link_2a", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_5_status_a"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_5_comment_a", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_5_alert_a", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.5 Free access to SOME facilities
            dbc.Row([
                dbc.Col(html.Label("Free access to SOME facilities", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_5_evidence_link_1b", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_5_evidence_link_2b", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_5_status_b"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_5_comment_b", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_5_alert_b", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.5 Charged access ONLY
            dbc.Row([
                dbc.Col(html.Label("Charged access ONLY", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_5_evidence_link_1c", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_5_evidence_link_2c", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_5_status_c"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_5_comment_c", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_5_alert_c", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            dbc.Row(dbc.Col(html.Label("Smoke free policy in place by 2022:", id="label-3-6", style={"fontStyle":"italic", "cursor":"help"}), width=12), className="mb-2"),
            # 3.3.6 Existence of policy (Smoke-free campus)
            dbc.Row([
                dbc.Col(html.Label("Existence of policy (Smoke-free campus)", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_6_evidence_link_1a", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_6_evidence_link_2a", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_6_status_a"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_6_comment_a", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_6_alert_a", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),

            # 3.3.6 Existence of policy (partial smoke-free campus)
            dbc.Row([
                dbc.Col(html.Label("Existence of policy (partial smoke-free campus)", className="ps-4"), width=4),
                dbc.Col(dbc.Input(id="sdg3_3_6_evidence_link_1b", type="text"), width=2),
                dbc.Col(dbc.Input(id="sdg3_3_6_evidence_link_2b", type="text"), width=2),
                dbc.Col(dbc.Select(id="sdg3_3_6_status_b"), width=2),
                dbc.Col(dbc.Button("View", id="sdg3_3_6_comment_b", color="warning", size="sm", className="w-100"), width=1),
                dbc.Col(
                    html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg3_3_6_alert_b", style={"display":"none"}
                    ), width=1
                ),
            ], className="mb-3"),
        ],
        title=html.Div(
                    [
                        html.Span("3.3 Lifelong learning measures", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg3_3_alert",
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
    Output('sdg3_2_1_total', 'value', allow_duplicate=True),
    [Input('sdg3_2_1_first', 'value'),
     Input('sdg3_2_1_second', 'value'),
     Input('sdg3_2_1_mid', 'value')],
    prevent_initial_call=True,
)
def update_321_total(first, second, mid):  # noqa
    # Treat None as 0
    total = sum(v or 0 for v in (first, second, mid))
    return total

@app.callback(
    Output('sdg3_2_2_total', 'value', allow_duplicate=True),
    [Input('sdg3_2_2_first', 'value'),
     Input('sdg3_2_2_second', 'value'),
     Input('sdg3_2_2_mid', 'value')],
    prevent_initial_call=True,
)
def update_322_total(first, second, mid):  # noqa
    total = sum(v or 0 for v in (first, second, mid))
    return total

tooltip_2_1 = dbc.Tooltip(
    additional_info.get("2.1total", ""),   # your hover-text
    target="label-2-1",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_2_2 = dbc.Tooltip(
    additional_info.get("2.2total", ""),   # your hover-text
    target="label-2-2",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_1 = dbc.Tooltip(
    additional_info.get("3.1a", ""),   # your hover-text
    target="label-3-1",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_2 = dbc.Tooltip(
    additional_info.get("3.2a", ""),   # your hover-text
    target="label-3-2",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_3 = dbc.Tooltip(
    additional_info.get("3.3a", ""),   # your hover-text
    target="label-3-3",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_4 = dbc.Tooltip(
    additional_info.get("3.4a", ""),   # your hover-text
    target="label-3-4",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_5 = dbc.Tooltip(
    additional_info.get("3.5a", ""),   # your hover-text
    target="label-3-5",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_6 = dbc.Tooltip(
    additional_info.get("3.6a", ""),   # your hover-text
    target="label-3-6",                # must match the Label id
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
                                dcc.Store(id='sdg3_toload', storage_type='memory', data=0),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H1(id="sdg3_page_header"),
                                            width=8
                                        ),
                                        dbc.Col(
                                            dbc.Button("Back", color="success", href="/sdglist"),
                                            width=4,
                                            id="sdg3_back_btn_div",
                                            style={"display": "flex", "justifyContent": "flex-end"}
                                        )
                                    ],
                                    align="center"
                                ),
                            ],
                            className="mb-0"
                        ),
                        html.Hr(),
                        sdg3_form,
                        tooltip_2_1,
                        tooltip_2_2,
                        tooltip_3_1,
                        tooltip_3_2,
                        tooltip_3_3,
                        tooltip_3_4,
                        tooltip_3_5,
                        tooltip_3_6,
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
                                                                id="sdg3_evidence_status",
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
                                                                id="sdg3_evidence_comments",
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
                            id="sdg3_evidence_div",
                            style={"display": "none"},  # hidden initially
                        ),
                        html.Br(),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='sdg3_removerecord',
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
                            id='sdg3_removerecord_div'
                        ),
                        dbc.Alert(id='sdg3_alert', is_open=False),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H5(id="sdg3_comment_modal_header")),
                                dbc.ModalBody(html.Div(id="sdg3_comment_modal_body")),
                                dbc.ModalFooter(
                                    dbc.Button("Close", id="sdg3_comment_modal_close", color="secondary")
                                ),
                            ],
                            id="sdg3_comment_modal",
                            is_open=False,
                            centered=True,
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id='sdg3_last_modal_header'), close_button=False, className="bg-success", style={"color": "white"}),
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
                            id="sdg3_last_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), close_button=True, className="bg-primary"),
                                dbc.ModalBody(
                                    html.H5(id="sdg3_initial_modal_message"),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Spinner(color="success", id="sdg3_spinner", spinner_style={"display":"none"}),
                                        dbc.Button("Cancel", id="sdg3_initial_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id="sdg3_initial_modal_confirm", color="success"),
                                    ]
                                ),
                            ],
                            centered=True,
                            id="sdg3_initial_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                        html.Br(),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Button("Save", color="primary", id="sdg3_save_button", n_clicks=0),
                                        width="auto"
                                    ),
                                    dbc.Col(
                                        dbc.Button("Cancel", color="warning", id="sdg3_cancel_button", n_clicks=0, href="/sdglist"),
                                        width="auto"
                                    ),
                                ],
                                className="mb-2",
                                justify="end",
                            ),
                            id="sdg3_buttons_div"
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
        Output('sdg3_spinner', 'spinner_style')
    ],
    [
        Input('sdg3_initial_modal_confirm', 'n_clicks'),
    ]
)
def save_sdg3(confirm):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    if eventid == 'sdg3_initial_modal_confirm' and confirm:
        return [{"display":"block"}]
    else:
        return [{"display":"none"}]

@app.callback(
    [
        # Check if all fields are filled
        Output('sdg3_last_modal', 'is_open'),
        Output('sdg3_last_modal_header', 'children'),
        #Initial Field
        Output('sdg3_initial_modal', 'is_open'),
        Output('sdg3_initial_modal_message', 'children'),
        Output('sdg3_initial_modal_confirm', 'color'),
        Output('sdg3_alert', 'is_open'),
        Output('sdg3_alert', 'color'),
        Output('sdg3_alert', 'children'),
        Output('sdg3_submitter', 'className'),
        Output('sdg3_submitter_office', 'className')
    ],
    [
        Input('sdg3_save_button', 'n_clicks'),
        Input('sdg3_initial_modal_confirm', 'n_clicks'),
        Input('sdg3_initial_modal_cancel', 'n_clicks'),
    ],
    [
        State('sdg3_2_1_total', 'value'),
        State('sdg3_2_1_first', 'value'),
        State('sdg3_2_1_second', 'value'),
        State('sdg3_2_1_mid', 'value'),
        State('sdg3_2_2_total', 'value'),
        State('sdg3_2_2_first', 'value'),
        State('sdg3_2_2_second', 'value'),
        State('sdg3_2_2_mid', 'value'),
        State('sdg3_3_1_evidence_link_1a', 'value'),
        State('sdg3_3_1_evidence_link_2a', 'value'),
        State('sdg3_3_1_evidence_link_1b', 'value'),
        State('sdg3_3_1_evidence_link_2b', 'value'),
        State('sdg3_3_1_evidence_link_1c', 'value'),
        State('sdg3_3_1_evidence_link_2c', 'value'),
        State('sdg3_3_2_evidence_link_1a', 'value'),
        State('sdg3_3_2_evidence_link_2a', 'value'),
        State('sdg3_3_2_evidence_link_1b', 'value'),
        State('sdg3_3_2_evidence_link_2b', 'value'),
        State('sdg3_3_2_evidence_link_1c', 'value'),
        State('sdg3_3_2_evidence_link_2c', 'value'),
        State('sdg3_3_3_evidence_link_1a', 'value'),
        State('sdg3_3_3_evidence_link_2a', 'value'),
        State('sdg3_3_3_evidence_link_1b', 'value'),
        State('sdg3_3_3_evidence_link_2b', 'value'),
        State('sdg3_3_3_evidence_link_1c', 'value'),
        State('sdg3_3_3_evidence_link_2c', 'value'),
        State('sdg3_3_4_evidence_link_1a', 'value'),
        State('sdg3_3_4_evidence_link_2a', 'value'),
        State('sdg3_3_4_evidence_link_1b', 'value'),
        State('sdg3_3_4_evidence_link_2b', 'value'),
        State('sdg3_3_5_evidence_link_1a', 'value'),
        State('sdg3_3_5_evidence_link_2a', 'value'),
        State('sdg3_3_5_evidence_link_1b', 'value'),
        State('sdg3_3_5_evidence_link_2b', 'value'),
        State('sdg3_3_5_evidence_link_1c', 'value'),
        State('sdg3_3_5_evidence_link_2c', 'value'),
        State('sdg3_3_6_evidence_link_1a', 'value'),
        State('sdg3_3_6_evidence_link_2a', 'value'),
        State('sdg3_3_6_evidence_link_1b', 'value'),
        State('sdg3_3_6_evidence_link_2b', 'value'),
        State('sdg3_submitter', 'value'),
        State('sdg3_submitter_office', 'value'),
        State('url', 'search'),
        State('sdg3_removerecord', 'value'),
        State('currentuserid', 'data')
        
    ],
)
def save_sdg3(
    submit, confirm, cancel, sdg3_2_1_total, sdg3_2_1_first, sdg3_2_1_second, sdg3_2_1_mid, sdg3_2_2_total, 
    sdg3_2_2_first, sdg3_2_2_second, sdg3_2_2_mid, sdg3_3_1_evidence_link_1a, sdg3_3_1_evidence_link_2a, 
    sdg3_3_1_evidence_link_1b, sdg3_3_1_evidence_link_2b, sdg3_3_1_evidence_link_1c, sdg3_3_1_evidence_link_2c, sdg3_3_2_evidence_link_1a, 
    sdg3_3_2_evidence_link_2a, sdg3_3_2_evidence_link_1b, sdg3_3_2_evidence_link_2b, sdg3_3_2_evidence_link_1c, sdg3_3_2_evidence_link_2c, 
    sdg3_3_3_evidence_link_1a, sdg3_3_3_evidence_link_2a, sdg3_3_3_evidence_link_1b, sdg3_3_3_evidence_link_2b, sdg3_3_3_evidence_link_1c, 
    sdg3_3_3_evidence_link_2c, sdg3_3_4_evidence_link_1a, sdg3_3_4_evidence_link_2a, sdg3_3_4_evidence_link_1b, sdg3_3_4_evidence_link_2b, 
    sdg3_3_5_evidence_link_1a, sdg3_3_5_evidence_link_2a, sdg3_3_5_evidence_link_1b, sdg3_3_5_evidence_link_2b, sdg3_3_5_evidence_link_1c, 
    sdg3_3_5_evidence_link_2c, sdg3_3_6_evidence_link_1a, sdg3_3_6_evidence_link_2a, sdg3_3_6_evidence_link_1b, sdg3_3_6_evidence_link_2b,
    sdg3_submitter, sdg3_submitter_office,
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

    if eventid == 'sdg3_save_button' and submit:
        def get_input_class(value):
            return 'red-border' if not value else 'form-control'
        if not all([sdg3_submitter, sdg3_submitter_office]) and not removerecord:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            sdg_submitter_className = get_input_class(sdg3_submitter)
            sdg_submitter_office_className = get_input_class(sdg3_submitter_office)
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
    elif eventid == 'sdg3_initial_modal_confirm' and confirm:
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
            df_sub = db.execute_returning(sql_sub, [sdg3_submitter, sdg3_submitter_office, currentuserid], ['submission_id'])
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
            add_ev('2.1total', 1, sdg3_2_1_total, None, None)
            add_ev('2.1first', 1, sdg3_2_1_first, None, None)
            add_ev('2.1second', 1, sdg3_2_1_second, None, None)
            add_ev('2.1mid', 1, sdg3_2_1_mid, None, None)
            add_ev('2.2total', 1, sdg3_2_2_total, None, None)
            add_ev('2.2first', 1, sdg3_2_2_first, None, None)
            add_ev('2.2second', 1, sdg3_2_2_second, None, None)
            add_ev('2.2mid', 1, sdg3_2_2_mid, None, None)

            # links & statuses
            add_ev('3.1a', 1, sdg3_3_1_evidence_link_1a, None, None)
            add_ev('3.1a', 2, sdg3_3_1_evidence_link_2a, None, None)
            add_ev('3.1b', 1, sdg3_3_1_evidence_link_1b, None, None)
            add_ev('3.1b', 2, sdg3_3_1_evidence_link_2b, None, None)
            add_ev('3.1c', 1, sdg3_3_1_evidence_link_1c, None, None)
            add_ev('3.1c', 2, sdg3_3_1_evidence_link_2c, None, None)

            add_ev('3.2a', 1, sdg3_3_2_evidence_link_1a, None, None)
            add_ev('3.2a', 2, sdg3_3_2_evidence_link_2a, None, None)
            add_ev('3.2b', 1, sdg3_3_2_evidence_link_1b, None, None)
            add_ev('3.2b', 2, sdg3_3_2_evidence_link_2b, None, None)
            add_ev('3.2c', 1, sdg3_3_2_evidence_link_1c, None, None)
            add_ev('3.2c', 2, sdg3_3_2_evidence_link_2c, None, None)

            add_ev('3.3a', 1, sdg3_3_3_evidence_link_1a, None, None)
            add_ev('3.3a', 2, sdg3_3_3_evidence_link_2a, None, None)
            add_ev('3.3b', 1, sdg3_3_3_evidence_link_1b, None, None)
            add_ev('3.3b', 2, sdg3_3_3_evidence_link_2b, None, None)
            add_ev('3.3c', 1, sdg3_3_3_evidence_link_1c, None, None)
            add_ev('3.3c', 2, sdg3_3_3_evidence_link_2c, None, None)

            add_ev('3.4a', 1, sdg3_3_4_evidence_link_1a, None, None)
            add_ev('3.4a', 2, sdg3_3_4_evidence_link_2a, None, None)
            add_ev('3.4b', 1, sdg3_3_4_evidence_link_1b, None, None)
            add_ev('3.4b', 2, sdg3_3_4_evidence_link_2b, None, None)

            add_ev('3.5a', 1, sdg3_3_5_evidence_link_1a, None, None)
            add_ev('3.5a', 2, sdg3_3_5_evidence_link_2a, None, None)
            add_ev('3.5b', 1, sdg3_3_5_evidence_link_1b, None, None)
            add_ev('3.5b', 2, sdg3_3_5_evidence_link_2b, None, None)
            add_ev('3.5c', 1, sdg3_3_5_evidence_link_1c, None, None)
            add_ev('3.5c', 2, sdg3_3_5_evidence_link_2c, None, None)

            add_ev('3.6a', 1, sdg3_3_6_evidence_link_1a, None, None)
            add_ev('3.6a', 2, sdg3_3_6_evidence_link_2a, None, None)
            add_ev('3.6b', 1, sdg3_3_6_evidence_link_1b, None, None)
            add_ev('3.6b', 2, sdg3_3_6_evidence_link_2b, None, None)


            # 3) Perform all evidence INSERTs
            ev_sql = """
            INSERT INTO kmteam.evidence
                (submission_id, metric_id, link_number, url, status_id, comment)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            for vals in to_insert:
                db.modifydatabase(ev_sql, vals)
            
            final_modal_open = True
            final_modal_header = "SDG 3 Evidences Successfully Submitted."
        
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
                [sdg3_submitter, sdg3_submitter_office, sub_id]
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

            #numeric metrics — treat each as a single “link 1”
            add_ev('2.1total', 1, sdg3_2_1_total)
            add_ev('2.1first', 1, sdg3_2_1_first)
            add_ev('2.1second', 1, sdg3_2_1_second)
            add_ev('2.1mid', 1, sdg3_2_1_mid)
            add_ev('2.2total', 1, sdg3_2_2_total)
            add_ev('2.2first', 1, sdg3_2_2_first)
            add_ev('2.2second', 1, sdg3_2_2_second)
            add_ev('2.2mid', 1, sdg3_2_2_mid)

            # links & statuses
            add_ev('3.1a', 1, sdg3_3_1_evidence_link_1a)
            add_ev('3.1a', 1, sdg3_3_1_evidence_link_1a)
            add_ev('3.1a', 2, sdg3_3_1_evidence_link_2a)
            add_ev('3.1b', 1, sdg3_3_1_evidence_link_1b)
            add_ev('3.1b', 2, sdg3_3_1_evidence_link_2b)
            add_ev('3.1c', 1, sdg3_3_1_evidence_link_1c)
            add_ev('3.1c', 2, sdg3_3_1_evidence_link_2c)

            add_ev('3.2a', 1, sdg3_3_2_evidence_link_1a)
            add_ev('3.2a', 2, sdg3_3_2_evidence_link_2a)
            add_ev('3.2b', 1, sdg3_3_2_evidence_link_1b)
            add_ev('3.2b', 2, sdg3_3_2_evidence_link_2b)
            add_ev('3.2c', 1, sdg3_3_2_evidence_link_1c)
            add_ev('3.2c', 2, sdg3_3_2_evidence_link_2c)

            add_ev('3.3a', 1, sdg3_3_3_evidence_link_1a)
            add_ev('3.3a', 2, sdg3_3_3_evidence_link_2a)
            add_ev('3.3b', 1, sdg3_3_3_evidence_link_1b)
            add_ev('3.3b', 2, sdg3_3_3_evidence_link_2b)
            add_ev('3.3c', 1, sdg3_3_3_evidence_link_1c)
            add_ev('3.3c', 2, sdg3_3_3_evidence_link_2c)

            add_ev('3.4a', 1, sdg3_3_4_evidence_link_1a)
            add_ev('3.4a', 2, sdg3_3_4_evidence_link_2a)
            add_ev('3.4b', 1, sdg3_3_4_evidence_link_1b)
            add_ev('3.4b', 2, sdg3_3_4_evidence_link_2b)

            add_ev('3.5a', 1, sdg3_3_5_evidence_link_1a)
            add_ev('3.5a', 2, sdg3_3_5_evidence_link_2a)
            add_ev('3.5b', 1, sdg3_3_5_evidence_link_1b)
            add_ev('3.5b', 2, sdg3_3_5_evidence_link_2b)
            add_ev('3.5c', 1, sdg3_3_5_evidence_link_1c)
            add_ev('3.5c', 2, sdg3_3_5_evidence_link_2c)

            add_ev('3.6a', 1, sdg3_3_6_evidence_link_1a)
            add_ev('3.6a', 2, sdg3_3_6_evidence_link_2a)
            add_ev('3.6b', 1, sdg3_3_6_evidence_link_1b)
            add_ev('3.6b', 2, sdg3_3_6_evidence_link_2b)


            final_modal_open = True
            final_modal_header = "SDG 3 Evidences Successfully Updated."

    elif eventid == 'sdg3_initial_modal_cancel' and cancel:
        initial_modal_open = False
        initial_modal_message = ''
          
    return [final_modal_open, final_modal_header, initial_modal_open, initial_modal_message, confirm_button_color, alert_open, alert_color, alert_text, sdg_submitter_className, sdg_submitter_office_className]

@app.callback(
    [
        Output('sdg3_3_1_status_a', 'options'),
        Output('sdg3_3_1_status_b', 'options'),
        Output('sdg3_3_1_status_c', 'options'),
        Output('sdg3_3_2_status_a', 'options'),
        Output('sdg3_3_2_status_b', 'options'),
        Output('sdg3_3_2_status_c', 'options'),
        Output('sdg3_3_3_status_a', 'options'),
        Output('sdg3_3_3_status_b', 'options'),
        Output('sdg3_3_3_status_c', 'options'),
        Output('sdg3_3_4_status_a', 'options'),
        Output('sdg3_3_4_status_b', 'options'),
        Output('sdg3_3_5_status_a', 'options'),
        Output('sdg3_3_5_status_b', 'options'),
        Output('sdg3_3_5_status_c', 'options'),
        Output('sdg3_3_6_status_a', 'options'),
        Output('sdg3_3_6_status_b', 'options'),
        Output('sdg3_page_header', 'children'),
        Output('sdg3_toload', 'data'),
        Output('sdg3_removerecord_div', 'style'),
        Output('sdg3_buttons_div', 'style'),
        Output('sdg3_back_btn_div', 'style')
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
    if pathname != '/sdglist/sdg3submission':
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
        header = 'Add SDG 3 Evidence Submission'
        to_load = 0
        removediv_style = {'display': 'none'}
        buttondiv_style = None
        backbtn_div_style = {'display': 'none'}
    elif create_mode == 'edit':
        header = 'Edit SDG 3 Evidence Submission'
        to_load = 1
        removediv_style = None
        buttondiv_style = None
        backbtn_div_style = {'display': 'none'}
    elif create_mode == 'view':
        header = 'View SDG 3 Evidence Submission'
        to_load = 1
        removediv_style = {'display': 'none'}
        buttondiv_style = {'display': 'none'}
        backbtn_div_style = {"display": "flex", "justifyContent": "flex-end"}


    return [status_options, status_options, status_options, status_options, status_options, 
            status_options, status_options, status_options, status_options, status_options, 
            status_options, status_options, status_options, status_options, status_options, status_options,
            header, to_load, removediv_style, buttondiv_style, backbtn_div_style]


@app.callback(
    [
        Output('sdg3_2_1_total', 'value'),
        Output('sdg3_2_1_first', 'value'),
        Output('sdg3_2_1_second', 'value'),
        Output('sdg3_2_1_mid', 'value'),
        Output('sdg3_2_2_total', 'value'),
        Output('sdg3_2_2_first', 'value'),
        Output('sdg3_2_2_second', 'value'),
        Output('sdg3_2_2_mid', 'value'),
        Output('sdg3_3_1_evidence_link_1a', 'value'),
        Output('sdg3_3_1_evidence_link_2a', 'value'),
        Output('sdg3_3_1_evidence_link_1b', 'value'),
        Output('sdg3_3_1_evidence_link_2b', 'value'),
        Output('sdg3_3_1_evidence_link_1c', 'value'),
        Output('sdg3_3_1_evidence_link_2c', 'value'),
        Output('sdg3_3_2_evidence_link_1a', 'value'),
        Output('sdg3_3_2_evidence_link_2a', 'value'),
        Output('sdg3_3_2_evidence_link_1b', 'value'),
        Output('sdg3_3_2_evidence_link_2b', 'value'),
        Output('sdg3_3_2_evidence_link_1c', 'value'),
        Output('sdg3_3_2_evidence_link_2c', 'value'),
        Output('sdg3_3_3_evidence_link_1a', 'value'),
        Output('sdg3_3_3_evidence_link_2a', 'value'),
        Output('sdg3_3_3_evidence_link_1b', 'value'),
        Output('sdg3_3_3_evidence_link_2b', 'value'),
        Output('sdg3_3_3_evidence_link_1c', 'value'),
        Output('sdg3_3_3_evidence_link_2c', 'value'),
        Output('sdg3_3_4_evidence_link_1a', 'value'),
        Output('sdg3_3_4_evidence_link_2a', 'value'),
        Output('sdg3_3_4_evidence_link_1b', 'value'),
        Output('sdg3_3_4_evidence_link_2b', 'value'),
        Output('sdg3_3_5_evidence_link_1a', 'value'),
        Output('sdg3_3_5_evidence_link_2a', 'value'),
        Output('sdg3_3_5_evidence_link_1b', 'value'),
        Output('sdg3_3_5_evidence_link_2b', 'value'),
        Output('sdg3_3_5_evidence_link_1c', 'value'),
        Output('sdg3_3_5_evidence_link_2c', 'value'),
        Output('sdg3_3_6_evidence_link_1a', 'value'),
        Output('sdg3_3_6_evidence_link_2a', 'value'),
        Output('sdg3_3_6_evidence_link_1b', 'value'),
        Output('sdg3_3_6_evidence_link_2b', 'value'),
        Output('sdg3_3_1_status_a', 'value'),
        Output('sdg3_3_1_status_b', 'value'),
        Output('sdg3_3_1_status_c', 'value'),
        Output('sdg3_3_2_status_a', 'value'),
        Output('sdg3_3_2_status_b', 'value'),
        Output('sdg3_3_2_status_c', 'value'),
        Output('sdg3_3_3_status_a', 'value'),
        Output('sdg3_3_3_status_b', 'value'),
        Output('sdg3_3_3_status_c', 'value'),
        Output('sdg3_3_4_status_a', 'value'),
        Output('sdg3_3_4_status_b', 'value'),
        Output('sdg3_3_5_status_a', 'value'),
        Output('sdg3_3_5_status_b', 'value'),
        Output('sdg3_3_5_status_c', 'value'),
        Output('sdg3_3_6_status_a', 'value'),
        Output('sdg3_3_6_status_b', 'value'),
        Output('sdg3_submitter', 'value'),
        Output('sdg3_submitter_office', 'value'),
    ],
    Input('sdg3_toload', 'modified_timestamp'),
    [
        State('sdg3_toload', 'data'),
        State('url', 'search')
    ]
)
def sdg3evidences_load(ts, toload, search):
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
      ('2.1total',1): ('sdg3_2_1_total','sdg3_2_1_total_status'),
      ('2.1first',1): ('sdg3_2_1_first','sdg3_2_1_first_status'),
      ('2.1second',1): ('sdg3_2_1_second','sdg3_2_1_second_status'),
      ('2.1mid',1): ('sdg3_2_1_mid','sdg3_2_1_mid_status'),
      ('2.2total',1): ('sdg3_2_2_total','sdg3_2_2_total_status'),
      ('2.2first',1): ('sdg3_2_2_first','sdg3_2_2_first_status'),
      ('2.2second',1): ('sdg3_2_2_second','sdg3_2_2_second_status'),
      ('2.2mid',1): ('sdg3_2_2_mid','sdg3_2_2_mid_status'),
      ('3.1a', 1): ('sdg3_3_1_evidence_link_1a', 'sdg3_3_1_status_a'),
      ('3.1a', 2): ('sdg3_3_1_evidence_link_2a', 'sdg3_3_1_status_a'),
      ('3.1b', 1): ('sdg3_3_1_evidence_link_1b', 'sdg3_3_1_status_b'),
      ('3.1b', 2): ('sdg3_3_1_evidence_link_2b', 'sdg3_3_1_status_b'),
      ('3.1c', 1): ('sdg3_3_1_evidence_link_1c', 'sdg3_3_1_status_c'),
      ('3.1c', 2): ('sdg3_3_1_evidence_link_2c', 'sdg3_3_1_status_c'),

      ('3.2a', 1): ('sdg3_3_2_evidence_link_1a', 'sdg3_3_2_status_a'),
      ('3.2a', 2): ('sdg3_3_2_evidence_link_2a', 'sdg3_3_2_status_a'),
      ('3.2b', 1): ('sdg3_3_2_evidence_link_1b', 'sdg3_3_2_status_b'),
      ('3.2b', 2): ('sdg3_3_2_evidence_link_2b', 'sdg3_3_2_status_b'),
      ('3.2c', 1): ('sdg3_3_2_evidence_link_1c', 'sdg3_3_2_status_c'),
      ('3.2c', 2): ('sdg3_3_2_evidence_link_2c', 'sdg3_3_2_status_c'),

      ('3.3a', 1): ('sdg3_3_3_evidence_link_1a', 'sdg3_3_3_status_a'),
      ('3.3a', 2): ('sdg3_3_3_evidence_link_2a', 'sdg3_3_3_status_a'),
      ('3.3b', 1): ('sdg3_3_3_evidence_link_1b', 'sdg3_3_3_status_b'),
      ('3.3b', 2): ('sdg3_3_3_evidence_link_2b', 'sdg3_3_3_status_b'),
      ('3.3c', 1): ('sdg3_3_3_evidence_link_1c', 'sdg3_3_3_status_c'),
      ('3.3c', 2): ('sdg3_3_3_evidence_link_2c', 'sdg3_3_3_status_c'),

      ('3.4a', 1): ('sdg3_3_4_evidence_link_1a', 'sdg3_3_4_status_a'),
      ('3.4a', 2): ('sdg3_3_4_evidence_link_2a', 'sdg3_3_4_status_a'),
      ('3.4b', 1): ('sdg3_3_4_evidence_link_1b', 'sdg3_3_4_status_b'),
      ('3.4b', 2): ('sdg3_3_4_evidence_link_2b', 'sdg3_3_4_status_b'),

      ('3.5a', 1): ('sdg3_3_5_evidence_link_1a', 'sdg3_3_5_status_a'),
      ('3.5a', 2): ('sdg3_3_5_evidence_link_2a', 'sdg3_3_5_status_a'),
      ('3.5b', 1): ('sdg3_3_5_evidence_link_1b', 'sdg3_3_5_status_b'),
      ('3.5b', 2): ('sdg3_3_5_evidence_link_2b', 'sdg3_3_5_status_b'),
      ('3.5c', 1): ('sdg3_3_5_evidence_link_1c', 'sdg3_3_5_status_c'),
      ('3.5c', 2): ('sdg3_3_5_evidence_link_2c', 'sdg3_3_5_status_c'),

      ('3.6a', 1): ('sdg3_3_6_evidence_link_1a', 'sdg3_3_6_status_a'),
      ('3.6a', 2): ('sdg3_3_6_evidence_link_2a', 'sdg3_3_6_status_a'),
      ('3.6b', 1): ('sdg3_3_6_evidence_link_1b', 'sdg3_3_6_status_b'),
      ('3.6b', 2): ('sdg3_3_6_evidence_link_2b', 'sdg3_3_6_status_b'),
    }

    # initialize all values to None (so missing ones stay blank)
    values = {inp: None for inp,_ in comp_map.values()}
    values.update({st:  None for _,st in comp_map.values()})
    values['sdg3_2_1_total'] = None
    values['sdg3_2_1_first'] = None
    values['sdg3_2_1_second'] = None
    values['sdg3_2_1_mid'] = None
    values['sdg3_2_2_total'] = None
    values['sdg3_2_2_first'] = None
    values['sdg3_2_2_second'] = None
    values['sdg3_2_2_mid'] = None
    values['sdg3_submitter'] = submitter
    values['sdg3_submitter_office'] = office

    # populate from DB
    for _, r in ev_df.iterrows():
        cid = (r['code'], int(r['link']))
        inp_id, st_id = comp_map[cid]
        # numeric metrics go back to float
        if cid[0] in ('2.1total','2.1first', '2.1second','2.1mid', '2.2total','2.2first', '2.2second','2.2mid'):
            values[inp_id] = float(r['url'])
        else:
            values[inp_id] = r['url']
        values[st_id] = r['status']

    # return in the exact order of your Outputs
    return [
      values['sdg3_2_1_total'], values['sdg3_2_1_first'], values['sdg3_2_1_second'], values['sdg3_2_1_mid'], values['sdg3_2_2_total'], values['sdg3_2_2_first'], 
      values['sdg3_2_2_second'], values['sdg3_2_2_mid'], values['sdg3_3_1_evidence_link_1a'], values['sdg3_3_1_evidence_link_2a'], values['sdg3_3_1_evidence_link_1b'], 
      values['sdg3_3_1_evidence_link_2b'], values['sdg3_3_1_evidence_link_1c'], values['sdg3_3_1_evidence_link_2c'], values['sdg3_3_2_evidence_link_1a'], values['sdg3_3_2_evidence_link_2a'], 
      values['sdg3_3_2_evidence_link_1b'], values['sdg3_3_2_evidence_link_2b'], values['sdg3_3_2_evidence_link_1c'], values['sdg3_3_2_evidence_link_2c'], values['sdg3_3_3_evidence_link_1a'], 
      values['sdg3_3_3_evidence_link_2a'], values['sdg3_3_3_evidence_link_1b'], values['sdg3_3_3_evidence_link_2b'], values['sdg3_3_3_evidence_link_1c'], values['sdg3_3_3_evidence_link_2c'], 
      values['sdg3_3_4_evidence_link_1a'], values['sdg3_3_4_evidence_link_2a'], values['sdg3_3_4_evidence_link_1b'], values['sdg3_3_4_evidence_link_2b'], values['sdg3_3_5_evidence_link_1a'], 
      values['sdg3_3_5_evidence_link_2a'], values['sdg3_3_5_evidence_link_1b'], values['sdg3_3_5_evidence_link_2b'], values['sdg3_3_5_evidence_link_1c'], values['sdg3_3_5_evidence_link_2c'], 
      values['sdg3_3_6_evidence_link_1a'], values['sdg3_3_6_evidence_link_2a'], values['sdg3_3_6_evidence_link_1b'], values['sdg3_3_6_evidence_link_2b'],
      values['sdg3_3_1_status_a'], values['sdg3_3_1_status_b'], values['sdg3_3_1_status_c'], values['sdg3_3_2_status_a'], values['sdg3_3_2_status_b'], values['sdg3_3_2_status_c'], 
      values['sdg3_3_3_status_a'], values['sdg3_3_3_status_b'], values['sdg3_3_3_status_c'], values['sdg3_3_4_status_a'], values['sdg3_3_4_status_b'], values['sdg3_3_5_status_a'], 
      values['sdg3_3_5_status_b'], values['sdg3_3_5_status_c'], values['sdg3_3_6_status_a'], values['sdg3_3_6_status_b'],
      values['sdg3_submitter'], values['sdg3_submitter_office']
    ]

@app.callback(
    [
        Output("sdg3_comment_modal", "is_open"),
        Output("sdg3_comment_modal_header", "children"),
        Output("sdg3_comment_modal_body", "children"),
    ],
    # Inputs: all comment-buttons + the modal Close button
    [
        Input("sdg3_2_1_total_comment", "n_clicks"),
        Input("sdg3_2_1_first_comment", "n_clicks"),
        Input("sdg3_2_1_second_comment", "n_clicks"),
        Input("sdg3_2_1_mid_comment", "n_clicks"),
        Input("sdg3_2_2_total_comment", "n_clicks"),
        Input("sdg3_2_2_first_comment", "n_clicks"),
        Input("sdg3_2_2_second_comment", "n_clicks"),
        Input("sdg3_2_2_mid_comment", "n_clicks"),
        Input("sdg3_3_1_comment_a", "n_clicks"),
        Input("sdg3_3_1_comment_b", "n_clicks"),
        Input("sdg3_3_1_comment_c", "n_clicks"),
        Input("sdg3_3_2_comment_a", "n_clicks"),
        Input("sdg3_3_2_comment_b", "n_clicks"),
        Input("sdg3_3_2_comment_c", "n_clicks"),
        Input("sdg3_3_3_comment_a", "n_clicks"),
        Input("sdg3_3_3_comment_b", "n_clicks"),
        Input("sdg3_3_3_comment_c", "n_clicks"),
        Input("sdg3_3_4_comment_a", "n_clicks"),
        Input("sdg3_3_4_comment_b", "n_clicks"),
        Input("sdg3_3_5_comment_a", "n_clicks"),
        Input("sdg3_3_5_comment_b", "n_clicks"),
        Input("sdg3_3_5_comment_c", "n_clicks"),
        Input("sdg3_3_6_comment_a", "n_clicks"),
        Input("sdg3_3_6_comment_b", "n_clicks"),
        Input("sdg3_comment_modal_close", "n_clicks"),
    ],
    [ State("url", "search") ]  # to get submission_id from the URL
)
def display_comment(
    btn_1, btn_2,
    btn_3, btn_4, btn_5, btn_6, btn_7, btn_8,
    btn_9, btn_10, btn_11, btn_12, btn_13,
    btn_14, btn_15, btn_16, btn_17, btn_18, btn_19, btn_20,
    btn_21, btn_22, btn_23, btn_24,
    btn_close,
    search
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # If Close button clicked, just hide
    if clicked_id == "sdg3_comment_modal_close":
        return False, dash.no_update, dash.no_update

    # map button id → (metric_code, link_number)
    btn_map = {
        "sdg3_2_1_total_comment":   ("2.1total", 1),
        "sdg3_2_1_first_comment":   ("2.1first", 1),
        "sdg3_2_1_second_comment":   ("2.1second", 1),
        "sdg3_2_1_mid_comment":   ("2.1mid", 1),
        "sdg3_2_2_total_comment":   ("2.2total", 1),
        "sdg3_2_2_first_comment":   ("2.2first", 1),
        "sdg3_2_2_second_comment":   ("2.2second", 1),
        "sdg3_2_2_mid_comment":   ("2.2mid", 1),
        "sdg3_3_1_comment_a": ("3.1a", 1),
        "sdg3_3_1_comment_b": ("3.1b", 1),
        "sdg3_3_1_comment_c": ("3.1c", 1),
        "sdg3_3_2_comment_a": ("3.2a", 1),
        "sdg3_3_2_comment_b": ("3.2b", 1),
        "sdg3_3_2_comment_c": ("3.2c", 1),
        "sdg3_3_3_comment_a": ("3.3a", 1),
        "sdg3_3_3_comment_b": ("3.3b", 1),
        "sdg3_3_3_comment_c": ("3.3c", 1),
        "sdg3_3_4_comment_a": ("3.4a", 1),
        "sdg3_3_4_comment_b": ("3.4b", 1),
        "sdg3_3_5_comment_a": ("3.5a", 1),
        "sdg3_3_5_comment_b": ("3.5b", 1),
        "sdg3_3_5_comment_c": ("3.5c", 1),
        "sdg3_3_6_comment_a": ("3.6a", 1),
        "sdg3_3_6_comment_b": ("3.6b", 1),
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
        Output('sdg3_3_1_status_a', 'disabled'),
        Output('sdg3_3_1_status_b', 'disabled'),
        Output('sdg3_3_1_status_c', 'disabled'),
        Output('sdg3_3_2_status_a', 'disabled'),
        Output('sdg3_3_2_status_b', 'disabled'),
        Output('sdg3_3_2_status_c', 'disabled'),
        Output('sdg3_3_3_status_a', 'disabled'),
        Output('sdg3_3_3_status_b', 'disabled'),
        Output('sdg3_3_3_status_c', 'disabled'),
        Output('sdg3_3_4_status_a', 'disabled'),
        Output('sdg3_3_4_status_b', 'disabled'),
        Output('sdg3_3_5_status_a', 'disabled'),
        Output('sdg3_3_5_status_b', 'disabled'),
        Output('sdg3_3_5_status_c', 'disabled'),
        Output('sdg3_3_6_status_a', 'disabled'),
        Output('sdg3_3_6_status_b', 'disabled'),
    ],
    Input('url', 'pathname')
)
def show_qao_other_options_div(pathname):
    # Only act when we're on the specific page
    if pathname != '/sdglist/sdg3submission':
        raise PreventUpdate

    return [True, True, True, True, True, 
            True, True, True, True, True, 
            True, True, True, True, True, 
            True]

@app.callback(
    [
        Output("sdg3_2_1_total_alert",  "style"),
        Output("sdg3_2_1_first_alert",  "style"),
        Output("sdg3_2_1_second_alert", "style"),
        Output("sdg3_2_1_mid_alert",    "style"),
        Output("sdg3_2_2_total_alert",  "style"),
        Output("sdg3_2_2_first_alert",  "style"),
        Output("sdg3_2_2_second_alert", "style"),
        Output("sdg3_2_2_mid_alert",    "style"),
        Output("sdg3_3_1_alert_a",      "style"),
        Output("sdg3_3_1_alert_b",      "style"),
        Output("sdg3_3_1_alert_c",      "style"),
        Output("sdg3_3_2_alert_a",      "style"),
        Output("sdg3_3_2_alert_b",      "style"),
        Output("sdg3_3_2_alert_c",      "style"),
        Output("sdg3_3_3_alert_a",      "style"),
        Output("sdg3_3_3_alert_b",      "style"),
        Output("sdg3_3_3_alert_c",      "style"),
        Output("sdg3_3_4_alert_a",      "style"),
        Output("sdg3_3_4_alert_b",      "style"),
        Output("sdg3_3_5_alert_a",      "style"),
        Output("sdg3_3_5_alert_b",      "style"),
        Output("sdg3_3_5_alert_c",      "style"),
        Output("sdg3_3_6_alert_a",      "style"),
        Output("sdg3_3_6_alert_b",      "style"),
    ],
    Input('url', 'pathname'),
    State('url', 'search'),
)
def show_alert(pathname, search):
    if pathname != '/sdglist/sdg3submission':
        raise PreventUpdate

    # parse submission_id
    qs = parse_qs(urlparse(search).query)
    try:
        sub_id = int(qs.get('id', [''])[0])
    except:
        return [{"display": "none"}] * 24

    # fetch status_id
    sql = """
        SELECT m.code, e.link_number, e.status_id
          FROM kmteam.evidence e
          JOIN kmteam.metric  m ON e.metric_id = m.metric_id
         WHERE e.submission_id = %s
    """
    df = db.querydatafromdatabase(sql, [sub_id], ["code", "link", "status_id"])
    status_map = {(row.code, row.link): row.status_id for _, row in df.iterrows()}

    groups = [
        # 3.2.1 Total / First / Second / Mid
        [("2.1total", 1)],
        [("2.1first", 1)],
        [("2.1second", 1)],
        [("2.1mid", 1)],

        # 3.2.2 Total / First / Second / Mid
        [("2.2total", 1)],
        [("2.2first", 1)],
        [("2.2second", 1)],
        [("2.2mid", 1)],

        # 3.3.1 Local/National/Global health institutions
        [("3.1a", 1), ("3.1a", 2)],
        [("3.1b", 1), ("3.1b", 2)],
        [("3.1c", 1), ("3.1c", 2)],

        # 3.3.2 Health outreach programmes
        [("3.2a", 1), ("3.2a", 2)],
        [("3.2b", 1), ("3.2b", 2)],
        [("3.2c", 1), ("3.2c", 2)],

        # 3.3.3 Shared sports facilities
        [("3.3a", 1), ("3.3a", 2)],
        [("3.3b", 1), ("3.3b", 2)],
        [("3.3c", 1), ("3.3c", 2)],

        # 3.3.4 Sexual/reproductive health services
        [("3.4a", 1), ("3.4a", 2)],
        [("3.4b", 1), ("3.4b", 2)],

        # 3.3.5 Mental health support
        [("3.5a", 1), ("3.5a", 2)],
        [("3.5b", 1), ("3.5b", 2)],
        [("3.5c", 1), ("3.5c", 2)],

        # 3.3.6 Smoke‑free policy
        [("3.6a", 1), ("3.6a", 2)],
        [("3.6b", 1), ("3.6b", 2)],
    ]

    def style_for(group):
        for code, ln in group:
            if status_map.get((code, ln)) in (1, 3):
                return {"display": "block"}
        return {"display": "none"}

    return [style_for(g) for g in groups]


@app.callback(
    [
        Output("header_sdg3_2_alert", "style"),
        Output("header_sdg3_3_alert", "style"),
    ],
    Input('url', 'pathname'),
    State('url', 'search'),
)
def show_section_headers(pathname, search):
    if pathname != '/sdglist/sdg3submission':
        raise PreventUpdate

    # parse submission_id
    qs = parse_qs(urlparse(search).query)
    try:
        sub_id = int(qs.get('id', [''])[0])
    except:
        return [{"display": "none"}] * 2

    # fetch status_id
    sql = """
      SELECT m.code, e.link_number, e.status_id
        FROM kmteam.evidence e
        JOIN kmteam.metric  m ON e.metric_id = m.metric_id
       WHERE e.submission_id = %s
    """
    df = db.querydatafromdatabase(sql, [sub_id], ["code", "link", "status_id"])
    status_map = {(row.code, row.link): row.status_id for _, row in df.iterrows()}

    section_groups = {
        "3.2": [
            ("2.1total", 1), ("2.1first", 1), ("2.1second", 1), ("2.1mid", 1),
            ("2.2total", 1), ("2.2first", 1), ("2.2second", 1), ("2.2mid", 1),
        ],
        "3.3": [
            ("3.1a", 1), ("3.1a", 2),
            ("3.1b", 1), ("3.1b", 2),
            ("3.1c", 1), ("3.1c", 2),
            ("3.2a", 1), ("3.2a", 2),
            ("3.2b", 1), ("3.2b", 2),
            ("3.2c", 1), ("3.2c", 2),
            ("3.3a", 1), ("3.3a", 2),
            ("3.3b", 1), ("3.3b", 2),
            ("3.3c", 1), ("3.3c", 2),
            ("3.4a", 1), ("3.4a", 2),
            ("3.4b", 1), ("3.4b", 2),
            ("3.5a", 1), ("3.5a", 2),
            ("3.5b", 1), ("3.5b", 2),
            ("3.5c", 1), ("3.5c", 2),
            ("3.6a", 1), ("3.6a", 2),
            ("3.6b", 1), ("3.6b", 2),
        ],
    }

    def any_flag(pairs):
        return any(status_map.get(pair) in (1, 3) for pair in pairs)

    def style_for(flag):
        return {"display": "block"} if flag else {"display": "none"}

    return [
        style_for(any_flag(section_groups["3.2"])),
        style_for(any_flag(section_groups["3.3"])),
    ]
