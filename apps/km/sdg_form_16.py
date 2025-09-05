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
    [16],
    ["metric_id","code"]
)
metrics_map = dict(zip(all_metrics["code"], all_metrics["metric_id"]))

metric_info_df = db.querydatafromdatabase(
    "SELECT code, additional_information FROM kmteam.metric WHERE sdg_number = %s",
    [16],
    ["code","additional_information"],
)
additional_info = dict(
    zip(metric_info_df["code"], metric_info_df["additional_information"])
)

sdg16_form = dbc.Form([

    # ─────────────── Submitter’s Profile ───────────────
    dbc.Card([
        dbc.CardHeader(
            html.H5("Submitter's Profile"),
            style={"backgroundColor": highlight_colors['secondary'], "color": "white"}
        ),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(dbc.Label("Name of Submitter"), width=6),
                dbc.Col(dbc.Input(id="sdg16_submitter", type="text"), width=6),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Label("Submitter's Office"), width=6),
                dbc.Col(dbc.Input(id="sdg16_submitter_office", type="text"), width=6),
            ], className="mb-3"),
        ]),
    ], className="mb-4"),


    # ─────────────── Metrics Accordion ────────────────
    dbc.Accordion([

        # 16.2 University governance measures
        dbc.AccordionItem(
            children=[

                # header (text inputs)
                dbc.Row([
                    dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=4),
                    dbc.Col(html.Label("Evidence Link 1", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                    dbc.Col(html.Label("Evidence Link 2", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                    dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                    dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                    dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                ], className="mb-3"),

                # 16.2.1 Elected representation
                dbc.Row([
                    dbc.Col(html.Label("Elected representation", id="label-2-1", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_1_evidence_link_1", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_1_evidence_link_2", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_1_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_1_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_1_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # sub‑section: Students' union
                dbc.Row(
                    dbc.Col(html.Label("Students' union:", id="label-2-2", style={"fontStyle":"italic", "cursor":"help"}), width=12),
                    className="mb-2"
                ),

                # 16.2.2a Union providing governance
                dbc.Row([
                    dbc.Col(html.Label("Union providing governance", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_2_evidence_link_1a", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_2_evidence_link_2a", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_2_status_a"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_2_comment_a", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_2_alert_a", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.2.2b Union providing support for students
                dbc.Row([
                    dbc.Col(html.Label("Union providing support for students", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_2_evidence_link_1b", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_2_evidence_link_2b", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_2_status_b"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_2_comment_b", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_2_alert_b", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.2.2c Union providing social activities
                dbc.Row([
                    dbc.Col(html.Label("Union providing social activities", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_2_evidence_link_1c", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_2_evidence_link_2c", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_2_status_c"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_2_comment_c", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_2_alert_c", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.2.3 Identify and engage with local stakeholders
                dbc.Row([
                    dbc.Col(html.Label("Identify and engage with local stakeholders", id="label-2-3", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_3_evidence_link_1", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_3_evidence_link_2", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_3_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_3_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_3_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.2.4 Participatory bodies for stakeholder engagement
                dbc.Row([
                    dbc.Col(html.Label("Participatory bodies for stakeholder engagement", id="label-2-4", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_4_evidence_link_1", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_4_evidence_link_2", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_4_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_4_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_4_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.2.5 University principles on corruption and bribery
                dbc.Row([
                    dbc.Col(html.Label("University principles on corruption and bribery", id="label-2-5", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_5_evidence_link_1", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_5_evidence_link_2", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_5_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_5_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_5_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # sub‑section: Academic freedom policy
                dbc.Row(
                    dbc.Col(html.Label("Academic freedom policy (Existence of policy):", id="label-2-6", style={"fontStyle":"italic", "cursor":"help"}), width=12),
                    className="mb-2"
                ),

                # 16.2.6a Research freedom for senior academics
                dbc.Row([
                    dbc.Col(html.Label("Research freedom for senior academics", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_6_evidence_link_1a", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_6_evidence_link_2a", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_6_status_a"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_6_comment_a", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_6_alert_a", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.2.6b Research freedom for junior academics
                dbc.Row([
                    dbc.Col(html.Label("Research freedom for junior academics", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_6_evidence_link_1b", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_6_evidence_link_2b", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_6_status_b"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_6_comment_b", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_6_alert_b", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.2.6c Teaching freedom for senior academics
                dbc.Row([
                    dbc.Col(html.Label("Teaching freedom for senior academics", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_6_evidence_link_1c", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_6_evidence_link_2c", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_6_status_c"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_6_comment_c", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_6_alert_c", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.2.6d Teaching freedom for junior academics
                dbc.Row([
                    dbc.Col(html.Label("Teaching freedom for junior academics", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_6_evidence_link_1d", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_6_evidence_link_2d", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_6_status_d"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_6_comment_d", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_6_alert_d", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.2.7 Publish university financial data
                dbc.Row([
                    dbc.Col(html.Label("Publish university financial data", id="label-2-7", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_2_7_evidence_link_1", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_2_7_evidence_link_2", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_2_7_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_2_7_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_2_7_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

            ],
            title=html.Div(
                    [
                        html.Span("16.2 University governance measures", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg16_2_alert",
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


        # 16.3 Working with government
        dbc.AccordionItem(
            children=[

                # header (text inputs)
                dbc.Row([
                    dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=4),
                    dbc.Col(html.Label("Evidence Link 1", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                    dbc.Col(html.Label("Evidence Link 2", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                    dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                    dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                    dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                ], className="mb-3"),

                # sub‑section: Provide expert advice to government
                dbc.Row(
                    dbc.Col(html.Label("Provide expert advice to government:", id="label-3-1", style={"fontStyle":"italic", "cursor":"help"}), width=12),
                    className="mb-2"
                ),

                # 16.3.1a Local government provision
                dbc.Row([
                    dbc.Col(html.Label("Local government provision", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_3_1_evidence_link_1a", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_3_1_evidence_link_2a", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_3_1_status_a"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_3_1_comment_a", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_3_1_alert_a", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.3.1b Regional government provision
                dbc.Row([
                    dbc.Col(html.Label("Regional government provision", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_3_1_evidence_link_1b", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_3_1_evidence_link_2b", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_3_1_status_b"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_3_1_comment_b", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_3_1_alert_b", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.3.1c National government provision
                dbc.Row([
                    dbc.Col(html.Label("National government provision", className="ps-4"), width=4),
                    dbc.Col(dbc.Input(id="sdg16_3_1_evidence_link_1c", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_3_1_evidence_link_2c", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_3_1_status_c"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_3_1_comment_c", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_3_1_alert_c", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.3.2 Policy- and lawmakers outreach and education
                dbc.Row([
                    dbc.Col(html.Label("Policy- and lawmakers outreach and education", id="label-3-2", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_3_2_evidence_link_1", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_3_2_evidence_link_2", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_3_2_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_3_2_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_3_2_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.3.3 Participation in government research
                dbc.Row([
                    dbc.Col(html.Label("Participation in government research", id="label-3-3", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_3_3_evidence_link_1", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_3_3_evidence_link_2", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_3_3_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_3_3_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_3_3_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.3.4 Neutral platform to discuss issues
                dbc.Row([
                    dbc.Col(html.Label("Neutral platform to discuss issues", id="label-3-4", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_3_4_evidence_link_1", type="text"), width=2),
                    dbc.Col(dbc.Input(id="sdg16_3_4_evidence_link_2", type="text"), width=2),
                    dbc.Col(dbc.Select(id="sdg16_3_4_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_3_4_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_3_4_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

            ],
            title=html.Div(
                    [
                        html.Span("16.3 Working with government", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg16_3_alert",
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


        # 16.4 Proportion of graduates in law and civil enforcement
        dbc.AccordionItem(
            children=[

                # header (number inputs)
                dbc.Row([
                    dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=8),
                    dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                    dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                    dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                ], className="mb-3"),

                # 16.4.1 Number of graduates
                dbc.Row([
                    dbc.Col(html.Label("Number of graduates", id="label-4-1", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_4_1", type="number", min=0), width=4),
                    dbc.Col(dbc.Select(id="sdg16_4_1_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_4_1_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_4_1_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

                # 16.4.2 Number of graduates from law and enforcement-related courses
                dbc.Row([
                    dbc.Col(html.Label("Number of graduates from law and enforcement-related courses", id="label-4-2", style={"cursor":"help"}), width=4),
                    dbc.Col(dbc.Input(id="sdg16_4_2", type="number", min=0), width=4),
                    dbc.Col(dbc.Select(id="sdg16_4_2_status"), width=2),
                    dbc.Col(dbc.Button("View", id="sdg16_4_2_comment", color="warning", size="sm", className="w-100"), width=1),
                    dbc.Col(html.Div(
                        dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                  color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                        id="sdg16_4_2_alert", style={"display":"none"}
                    ), width=1),
                ], className="mb-3"),

            ],
            title=html.Div(
                    [
                        html.Span("16.4 Proportion of graduates in law and civil enforcement", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg16_4_alert",
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

tooltip_2_1 = dbc.Tooltip(
    additional_info.get("2.1", ""),   # your hover-text
    target="label-2-1",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_2_2 = dbc.Tooltip(
    additional_info.get("2.2a", ""),   # your hover-text
    target="label-2-2",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_2_3 = dbc.Tooltip(
    additional_info.get("2.3", ""),   # your hover-text
    target="label-2-3",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_2_4 = dbc.Tooltip(
    additional_info.get("2.4", ""),   # your hover-text
    target="label-2-4",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_2_5 = dbc.Tooltip(
    additional_info.get("2.5", ""),   # your hover-text
    target="label-2-5",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_2_6 = dbc.Tooltip(
    additional_info.get("2.6a", ""),   # your hover-text
    target="label-2-6",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_2_7 = dbc.Tooltip(
    additional_info.get("2.7", ""),   # your hover-text
    target="label-2-7",                # must match the Label id
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
    additional_info.get("3.2", ""),   # your hover-text
    target="label-3-2",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_3 = dbc.Tooltip(
    additional_info.get("3.3", ""),   # your hover-text
    target="label-3-3",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_3_4 = dbc.Tooltip(
    additional_info.get("3.4", ""),   # your hover-text
    target="label-3-4",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_4_1 = dbc.Tooltip(
    additional_info.get("4.1", ""),   # your hover-text
    target="label-4-1",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_4_2 = dbc.Tooltip(
    additional_info.get("4.2", ""),   # your hover-text
    target="label-4-2",                # must match the Label id
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
                                dcc.Store(id='sdg16_toload', storage_type='memory', data=0),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H1(id="sdg16_page_header"),
                                            width=8
                                        ),
                                        dbc.Col(
                                            dbc.Button("Back", color="success", href="/sdglist"),
                                            width=4,
                                            id="sdg16_back_btn_div",
                                            style={"display": "flex", "justifyContent": "flex-end"}
                                        )
                                    ],
                                    align="center"
                                ),
                            ],
                            className="mb-0"
                        ),
                        html.Hr(),
                        tooltip_2_1,  
                        tooltip_2_2,  
                        tooltip_2_3,  
                        tooltip_2_4,  
                        tooltip_2_5,  
                        tooltip_2_6,  
                        tooltip_2_7,  
                        tooltip_3_1,  
                        tooltip_3_2,  
                        tooltip_3_3,  
                        tooltip_3_4,  
                        tooltip_4_1,  
                        tooltip_4_2,  
                        sdg16_form,
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
                                                                id="sdg16_evidence_status",
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
                                                                id="sdg16_evidence_comments",
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
                            id="sdg16_evidence_div",
                            style={"display": "none"},  # hidden initially
                        ),
                        html.Br(),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='sdg16_removerecord',
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
                            id='sdg16_removerecord_div'
                        ),
                        dbc.Alert(id='sdg16_alert', is_open=False),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H5(id="sdg16_comment_modal_header")),
                                dbc.ModalBody(html.Div(id="sdg16_comment_modal_body")),
                                dbc.ModalFooter(
                                    dbc.Button("Close", id="sdg16_comment_modal_close", color="secondary")
                                ),
                            ],
                            id="sdg16_comment_modal",
                            is_open=False,
                            centered=True,
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id='sdg16_last_modal_header'), close_button=False, className="bg-success", style={"color": "white"}),
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
                            id="sdg16_last_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), close_button=True, className="bg-primary"),
                                dbc.ModalBody(
                                    html.H5(id="sdg16_initial_modal_message"),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Spinner(color="success", id="sdg16_spinner", spinner_style={"display":"none"}),
                                        dbc.Button("Cancel", id="sdg16_initial_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id="sdg16_initial_modal_confirm", color="success"),
                                    ]
                                ),
                            ],
                            centered=True,
                            id="sdg16_initial_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                        html.Br(),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Button("Save", color="primary", id="sdg16_save_button", n_clicks=0),
                                        width="auto"
                                    ),
                                    dbc.Col(
                                        dbc.Button("Cancel", color="warning", id="sdg16_cancel_button", n_clicks=0, href="/sdglist"),
                                        width="auto"
                                    ),
                                ],
                                className="mb-2",
                                justify="end",
                            ),
                            id="sdg16_buttons_div"
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
        Output('sdg16_spinner', 'spinner_style')
    ],
    [
        Input('sdg16_initial_modal_confirm', 'n_clicks'),
    ]
)
def save_sdg16(confirm):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    if eventid == 'sdg16_initial_modal_confirm' and confirm:
        return [{"display":"block"}]
    else:
        return [{"display":"none"}]


@app.callback(
    [
        # Check if all fields are filled
        Output('sdg16_last_modal', 'is_open'),
        Output('sdg16_last_modal_header', 'children'),
        #Initial Field
        Output('sdg16_initial_modal', 'is_open'),
        Output('sdg16_initial_modal_message', 'children'),
        Output('sdg16_initial_modal_confirm', 'color'),
        Output('sdg16_alert', 'is_open'),
        Output('sdg16_alert', 'color'),
        Output('sdg16_alert', 'children'),
        Output('sdg16_submitter', 'className'),
        Output('sdg16_submitter_office', 'className')
    ],
    [
        Input('sdg16_save_button', 'n_clicks'),
        Input('sdg16_initial_modal_confirm', 'n_clicks'),
        Input('sdg16_initial_modal_cancel', 'n_clicks'),
    ],
    [
        State('sdg16_2_1_evidence_link_1', 'value'),
        State('sdg16_2_1_evidence_link_2', 'value'),
        State('sdg16_2_2_evidence_link_1a', 'value'),
        State('sdg16_2_2_evidence_link_2a', 'value'),
        State('sdg16_2_2_evidence_link_1b', 'value'),
        State('sdg16_2_2_evidence_link_2b', 'value'),
        State('sdg16_2_2_evidence_link_1c', 'value'),
        State('sdg16_2_2_evidence_link_2c', 'value'),
        State('sdg16_2_3_evidence_link_1', 'value'),
        State('sdg16_2_3_evidence_link_2', 'value'),
        State('sdg16_2_4_evidence_link_1', 'value'),
        State('sdg16_2_4_evidence_link_2', 'value'),
        State('sdg16_2_5_evidence_link_1', 'value'),
        State('sdg16_2_5_evidence_link_2', 'value'),
        State('sdg16_2_6_evidence_link_1a', 'value'),
        State('sdg16_2_6_evidence_link_2a', 'value'),
        State('sdg16_2_6_evidence_link_1b', 'value'),
        State('sdg16_2_6_evidence_link_2b', 'value'),
        State('sdg16_2_6_evidence_link_1c', 'value'),
        State('sdg16_2_6_evidence_link_2c', 'value'),
        State('sdg16_2_6_evidence_link_1d', 'value'),
        State('sdg16_2_6_evidence_link_2d', 'value'),
        State('sdg16_2_7_evidence_link_1', 'value'),
        State('sdg16_2_7_evidence_link_2', 'value'),
        State('sdg16_3_1_evidence_link_1a', 'value'),
        State('sdg16_3_1_evidence_link_2a', 'value'),
        State('sdg16_3_1_evidence_link_1b', 'value'),
        State('sdg16_3_1_evidence_link_2b', 'value'),
        State('sdg16_3_1_evidence_link_1c', 'value'),
        State('sdg16_3_1_evidence_link_2c', 'value'),
        State('sdg16_3_2_evidence_link_1', 'value'),
        State('sdg16_3_2_evidence_link_2', 'value'),
        State('sdg16_3_3_evidence_link_1', 'value'),
        State('sdg16_3_3_evidence_link_2', 'value'),
        State('sdg16_3_4_evidence_link_1', 'value'),
        State('sdg16_3_4_evidence_link_2', 'value'),
        State('sdg16_4_1', 'value'),
        State('sdg16_4_2', 'value'),

        State('sdg16_submitter', 'value'),
        State('sdg16_submitter_office', 'value'),
        State('url', 'search'),
        State('sdg16_removerecord', 'value'),
        State('currentuserid', 'data')
        
    ],
)
def save_sdg16(
    submit, confirm, cancel, 
    sdg16_2_1_evidence_link_1, sdg16_2_1_evidence_link_2, sdg16_2_2_evidence_link_1a, sdg16_2_2_evidence_link_2a, 
    sdg16_2_2_evidence_link_1b, sdg16_2_2_evidence_link_2b, sdg16_2_2_evidence_link_1c, sdg16_2_2_evidence_link_2c, 
    sdg16_2_3_evidence_link_1, sdg16_2_3_evidence_link_2, sdg16_2_4_evidence_link_1, sdg16_2_4_evidence_link_2, 
    sdg16_2_5_evidence_link_1, sdg16_2_5_evidence_link_2, sdg16_2_6_evidence_link_1a, sdg16_2_6_evidence_link_2a, 
    sdg16_2_6_evidence_link_1b, sdg16_2_6_evidence_link_2b, sdg16_2_6_evidence_link_1c, sdg16_2_6_evidence_link_2c, 
    sdg16_2_6_evidence_link_1d, sdg16_2_6_evidence_link_2d, sdg16_2_7_evidence_link_1, sdg16_2_7_evidence_link_2, 
    sdg16_3_1_evidence_link_1a, sdg16_3_1_evidence_link_2a, sdg16_3_1_evidence_link_1b, sdg16_3_1_evidence_link_2b,
    sdg16_3_1_evidence_link_1c, sdg16_3_1_evidence_link_2c, sdg16_3_2_evidence_link_1, sdg16_3_2_evidence_link_2, 
    sdg16_3_3_evidence_link_1, sdg16_3_3_evidence_link_2, sdg16_3_4_evidence_link_1, sdg16_3_4_evidence_link_2, sdg16_4_1, sdg16_4_2,
    sdg16_submitter, sdg16_submitter_office,
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

    if eventid == 'sdg16_save_button' and submit:
        def get_input_class(value):
            return 'red-border' if not value else 'form-control'
        if not all([sdg16_submitter, sdg16_submitter_office]) and not removerecord:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            sdg_submitter_className = get_input_class(sdg16_submitter)
            sdg_submitter_office_className = get_input_class(sdg16_submitter_office)
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
    elif eventid == 'sdg16_initial_modal_confirm' and confirm:
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
            df_sub = db.execute_returning(sql_sub, [sdg16_submitter, sdg16_submitter_office, currentuserid], ['submission_id'])
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
            add_ev('2.1', 1, sdg16_2_1_evidence_link_1, None, None)
            add_ev('2.1', 2, sdg16_2_1_evidence_link_2, None, None)
            add_ev('2.2a', 1, sdg16_2_2_evidence_link_1a, None, None)
            add_ev('2.2a', 2, sdg16_2_2_evidence_link_2a, None, None)
            add_ev('2.2b', 1, sdg16_2_2_evidence_link_1b, None, None)
            add_ev('2.2b', 2, sdg16_2_2_evidence_link_2b, None, None)
            add_ev('2.2c', 1, sdg16_2_2_evidence_link_1c, None, None)
            add_ev('2.2c', 2, sdg16_2_2_evidence_link_2c, None, None)
            add_ev('2.3', 1, sdg16_2_3_evidence_link_1, None, None)
            add_ev('2.3', 2, sdg16_2_3_evidence_link_2, None, None)
            add_ev('2.4', 1, sdg16_2_4_evidence_link_1, None, None)
            add_ev('2.4', 2, sdg16_2_4_evidence_link_2, None, None)
            add_ev('2.5', 1, sdg16_2_5_evidence_link_1, None, None)
            add_ev('2.5', 2, sdg16_2_5_evidence_link_2, None, None)
            add_ev('2.6a', 1, sdg16_2_6_evidence_link_1a, None, None)
            add_ev('2.6a', 2, sdg16_2_6_evidence_link_2a, None, None)
            add_ev('2.6b', 1, sdg16_2_6_evidence_link_1b, None, None)
            add_ev('2.6b', 2, sdg16_2_6_evidence_link_2b, None, None)
            add_ev('2.6c', 1, sdg16_2_6_evidence_link_1c, None, None)
            add_ev('2.6c', 2, sdg16_2_6_evidence_link_2c, None, None)
            add_ev('2.6d', 1, sdg16_2_6_evidence_link_1d, None, None)
            add_ev('2.6d', 2, sdg16_2_6_evidence_link_2d, None, None)
            add_ev('2.7', 1, sdg16_2_7_evidence_link_1, None, None)
            add_ev('2.7', 2, sdg16_2_7_evidence_link_2, None, None)
            add_ev('3.1a', 1, sdg16_3_1_evidence_link_1a, None, None)
            add_ev('3.1a', 2, sdg16_3_1_evidence_link_2a, None, None)
            add_ev('3.1b', 1, sdg16_3_1_evidence_link_1b, None, None)
            add_ev('3.1b', 2, sdg16_3_1_evidence_link_2b, None, None)
            add_ev('3.1c', 1, sdg16_3_1_evidence_link_1c, None, None)
            add_ev('3.1c', 2, sdg16_3_1_evidence_link_2c, None, None)
            add_ev('3.2', 1, sdg16_3_2_evidence_link_1, None, None)
            add_ev('3.2', 2, sdg16_3_2_evidence_link_2, None, None)
            add_ev('3.3', 1, sdg16_3_3_evidence_link_1, None, None)
            add_ev('3.3', 2, sdg16_3_3_evidence_link_2, None, None)
            add_ev('3.4', 1, sdg16_3_4_evidence_link_1, None, None)
            add_ev('3.4', 2, sdg16_3_4_evidence_link_2, None, None)
            add_ev('4.1', 1, sdg16_4_1, None, None)
            add_ev('4.2', 1, sdg16_4_2, None, None)

            # 3) Perform all evidence INSERTs
            ev_sql = """
            INSERT INTO kmteam.evidence
                (submission_id, metric_id, link_number, url, status_id, comment)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            for vals in to_insert:
                db.modifydatabase(ev_sql, vals)
            
            final_modal_open = True
            final_modal_header = "SDG 16 Evidences Successfully Submitted."
        
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
                [sdg16_submitter, sdg16_submitter_office, sub_id]
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
            add_ev('2.1', 1, sdg16_2_1_evidence_link_1)
            add_ev('2.1', 2, sdg16_2_1_evidence_link_2)
            add_ev('2.2a', 1, sdg16_2_2_evidence_link_1a)
            add_ev('2.2a', 2, sdg16_2_2_evidence_link_2a)
            add_ev('2.2b', 1, sdg16_2_2_evidence_link_1b)
            add_ev('2.2b', 2, sdg16_2_2_evidence_link_2b)
            add_ev('2.2c', 1, sdg16_2_2_evidence_link_1c)
            add_ev('2.2c', 2, sdg16_2_2_evidence_link_2c)
            add_ev('2.3', 1, sdg16_2_3_evidence_link_1)
            add_ev('2.3', 2, sdg16_2_3_evidence_link_2)
            add_ev('2.4', 1, sdg16_2_4_evidence_link_1)
            add_ev('2.4', 2, sdg16_2_4_evidence_link_2)
            add_ev('2.5', 1, sdg16_2_5_evidence_link_1)
            add_ev('2.5', 2, sdg16_2_5_evidence_link_2)
            add_ev('2.6a', 1, sdg16_2_6_evidence_link_1a)
            add_ev('2.6a', 2, sdg16_2_6_evidence_link_2a)
            add_ev('2.6b', 1, sdg16_2_6_evidence_link_1b)
            add_ev('2.6b', 2, sdg16_2_6_evidence_link_2b)
            add_ev('2.6c', 1, sdg16_2_6_evidence_link_1c)
            add_ev('2.6c', 2, sdg16_2_6_evidence_link_2c)
            add_ev('2.6d', 1, sdg16_2_6_evidence_link_1d)
            add_ev('2.6d', 2, sdg16_2_6_evidence_link_2d)
            add_ev('2.7', 1, sdg16_2_7_evidence_link_1)
            add_ev('2.7', 2, sdg16_2_7_evidence_link_2)
            add_ev('3.1a', 1, sdg16_3_1_evidence_link_1a)
            add_ev('3.1a', 2, sdg16_3_1_evidence_link_2a)
            add_ev('3.1b', 1, sdg16_3_1_evidence_link_1b)
            add_ev('3.1b', 2, sdg16_3_1_evidence_link_2b)
            add_ev('3.1c', 1, sdg16_3_1_evidence_link_1c)
            add_ev('3.1c', 2, sdg16_3_1_evidence_link_2c)
            add_ev('3.2', 1, sdg16_3_2_evidence_link_1)
            add_ev('3.2', 2, sdg16_3_2_evidence_link_2)
            add_ev('3.3', 1, sdg16_3_3_evidence_link_1)
            add_ev('3.3', 2, sdg16_3_3_evidence_link_2)
            add_ev('3.4', 1, sdg16_3_4_evidence_link_1)
            add_ev('3.4', 2, sdg16_3_4_evidence_link_2)
            add_ev('4.1', 1, sdg16_4_1)
            add_ev('4.2', 1, sdg16_4_2)

            final_modal_open = True
            final_modal_header = "SDG 16 Evidences Successfully Updated."

    elif eventid == 'sdg16_initial_modal_cancel' and cancel:
        initial_modal_open = False
        initial_modal_message = ''
          
    return [final_modal_open, final_modal_header, initial_modal_open, initial_modal_message, confirm_button_color, alert_open, alert_color, alert_text, sdg_submitter_className, sdg_submitter_office_className]

@app.callback(
    [
        Output('sdg16_2_1_status', 'options'),
        Output('sdg16_2_2_status_a', 'options'),
        Output('sdg16_2_2_status_b', 'options'),
        Output('sdg16_2_2_status_c', 'options'),
        Output('sdg16_2_3_status', 'options'),
        Output('sdg16_2_4_status', 'options'),
        Output('sdg16_2_5_status', 'options'),
        Output('sdg16_2_6_status_a', 'options'),
        Output('sdg16_2_6_status_b', 'options'),
        Output('sdg16_2_6_status_c', 'options'),
        Output('sdg16_2_6_status_d', 'options'),
        Output('sdg16_2_7_status', 'options'),
        Output('sdg16_3_1_status_a', 'options'),
        Output('sdg16_3_1_status_b', 'options'),
        Output('sdg16_3_1_status_c', 'options'),
        Output('sdg16_3_2_status', 'options'),
        Output('sdg16_3_3_status', 'options'),
        Output('sdg16_3_4_status', 'options'),
        Output('sdg16_4_1_status', 'options'),
        Output('sdg16_4_2_status', 'options'),
        Output('sdg16_page_header', 'children'),
        Output('sdg16_toload', 'data'),
        Output('sdg16_removerecord_div', 'style'),
        Output('sdg16_buttons_div', 'style'),
        Output('sdg16_back_btn_div', 'style')
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
    if pathname != '/sdglist/sdg16submission':
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
        header = 'Add SDG 16 Evidence Submission'
        to_load = 0
        removediv_style = {'display': 'none'}
        buttondiv_style = None
        backbtn_div_style = {'display': 'none'}
    elif create_mode == 'edit':
        header = 'Edit SDG 16 Evidence Submission'
        to_load = 1
        removediv_style = None
        buttondiv_style = None
        backbtn_div_style = {'display': 'none'}
    elif create_mode == 'view':
        header = 'View SDG 16 Evidence Submission'
        to_load = 1
        removediv_style = {'display': 'none'}
        buttondiv_style = {'display': 'none'}
        backbtn_div_style = {"display": "flex", "justifyContent": "flex-end"}


    return [status_options, status_options, status_options, status_options, status_options, 
            status_options, status_options, status_options, status_options, status_options, 
            status_options, status_options, status_options, status_options, status_options, 
            status_options, status_options, status_options, status_options, status_options, 
            header, to_load, removediv_style, buttondiv_style, backbtn_div_style]


@app.callback(
    [
        Output('sdg16_2_1_status', 'disabled'),
        Output('sdg16_2_2_status_a', 'disabled'),
        Output('sdg16_2_2_status_b', 'disabled'),
        Output('sdg16_2_2_status_c', 'disabled'),
        Output('sdg16_2_3_status', 'disabled'),
        Output('sdg16_2_4_status', 'disabled'),
        Output('sdg16_2_5_status', 'disabled'),
        Output('sdg16_2_6_status_a', 'disabled'),
        Output('sdg16_2_6_status_b', 'disabled'),
        Output('sdg16_2_6_status_c', 'disabled'),
        Output('sdg16_2_6_status_d', 'disabled'),
        Output('sdg16_2_7_status', 'disabled'),
        Output('sdg16_3_1_status_a', 'disabled'),
        Output('sdg16_3_1_status_b', 'disabled'),
        Output('sdg16_3_1_status_c', 'disabled'),
        Output('sdg16_3_2_status', 'disabled'),
        Output('sdg16_3_3_status', 'disabled'),
        Output('sdg16_3_4_status', 'disabled'),
        Output('sdg16_4_1_status', 'disabled'),
        Output('sdg16_4_2_status', 'disabled'),
    ],
    Input('url', 'pathname')
)
def show_qao_other_options_div(pathname):
    # Only act when we're on the specific page
    if pathname != '/sdglist/sdg16submission':
        raise PreventUpdate

    return [True]*20


@app.callback(
    [
        Output('sdg16_2_1_evidence_link_1', 'value'),
        Output('sdg16_2_1_evidence_link_2', 'value'),
        Output('sdg16_2_2_evidence_link_1a', 'value'),
        Output('sdg16_2_2_evidence_link_2a', 'value'),
        Output('sdg16_2_2_evidence_link_1b', 'value'),
        Output('sdg16_2_2_evidence_link_2b', 'value'),
        Output('sdg16_2_2_evidence_link_1c', 'value'),
        Output('sdg16_2_2_evidence_link_2c', 'value'),
        Output('sdg16_2_3_evidence_link_1', 'value'),
        Output('sdg16_2_3_evidence_link_2', 'value'),
        Output('sdg16_2_4_evidence_link_1', 'value'),
        Output('sdg16_2_4_evidence_link_2', 'value'),
        Output('sdg16_2_5_evidence_link_1', 'value'),
        Output('sdg16_2_5_evidence_link_2', 'value'),
        Output('sdg16_2_6_evidence_link_1a', 'value'),
        Output('sdg16_2_6_evidence_link_2a', 'value'),
        Output('sdg16_2_6_evidence_link_1b', 'value'),
        Output('sdg16_2_6_evidence_link_2b', 'value'),
        Output('sdg16_2_6_evidence_link_1c', 'value'),
        Output('sdg16_2_6_evidence_link_2c', 'value'),
        Output('sdg16_2_6_evidence_link_1d', 'value'),
        Output('sdg16_2_6_evidence_link_2d', 'value'),
        Output('sdg16_2_7_evidence_link_1', 'value'),
        Output('sdg16_2_7_evidence_link_2', 'value'),
        Output('sdg16_3_1_evidence_link_1a', 'value'),
        Output('sdg16_3_1_evidence_link_2a', 'value'),
        Output('sdg16_3_1_evidence_link_1b', 'value'),
        Output('sdg16_3_1_evidence_link_2b', 'value'),
        Output('sdg16_3_1_evidence_link_1c', 'value'),
        Output('sdg16_3_1_evidence_link_2c', 'value'),
        Output('sdg16_3_2_evidence_link_1', 'value'),
        Output('sdg16_3_2_evidence_link_2', 'value'),
        Output('sdg16_3_3_evidence_link_1', 'value'),
        Output('sdg16_3_3_evidence_link_2', 'value'),
        Output('sdg16_3_4_evidence_link_1', 'value'),
        Output('sdg16_3_4_evidence_link_2', 'value'),
        Output('sdg16_4_1', 'value'),
        Output('sdg16_4_2', 'value'),

        Output('sdg16_2_1_status', 'value'),
        Output('sdg16_2_2_status_a', 'value'),
        Output('sdg16_2_2_status_b', 'value'),
        Output('sdg16_2_2_status_c', 'value'),
        Output('sdg16_2_3_status', 'value'),
        Output('sdg16_2_4_status', 'value'),
        Output('sdg16_2_5_status', 'value'),
        Output('sdg16_2_6_status_a', 'value'),
        Output('sdg16_2_6_status_b', 'value'),
        Output('sdg16_2_6_status_c', 'value'),
        Output('sdg16_2_6_status_d', 'value'),
        Output('sdg16_2_7_status', 'value'),
        Output('sdg16_3_1_status_a', 'value'),
        Output('sdg16_3_1_status_b', 'value'),
        Output('sdg16_3_1_status_c', 'value'),
        Output('sdg16_3_2_status', 'value'),
        Output('sdg16_3_3_status', 'value'),
        Output('sdg16_3_4_status', 'value'),
        Output('sdg16_4_1_status', 'value'),
        Output('sdg16_4_2_status', 'value'),

        Output('sdg16_submitter', 'value'),
        Output('sdg16_submitter_office', 'value'),
    ],
    Input('sdg16_toload', 'modified_timestamp'),
    [
        State('sdg16_toload', 'data'),
        State('url', 'search')
    ]
)
def sdg16evidences_load(ts, toload, search):
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
    # sdg16_2_1 (two links, no suffix)
    ('2.1', 1): ('sdg16_2_1_evidence_link_1', 'sdg16_2_1_status'),
    ('2.1', 2): ('sdg16_2_1_evidence_link_2', 'sdg16_2_1_status'),

    # sdg16_2_2 (suffixes a–c, two links each)
    ('2.2a', 1): ('sdg16_2_2_evidence_link_1a', 'sdg16_2_2_status_a'),
    ('2.2a', 2): ('sdg16_2_2_evidence_link_2a', 'sdg16_2_2_status_a'),
    ('2.2b', 1): ('sdg16_2_2_evidence_link_1b', 'sdg16_2_2_status_b'),
    ('2.2b', 2): ('sdg16_2_2_evidence_link_2b', 'sdg16_2_2_status_b'),
    ('2.2c', 1): ('sdg16_2_2_evidence_link_1c', 'sdg16_2_2_status_c'),
    ('2.2c', 2): ('sdg16_2_2_evidence_link_2c', 'sdg16_2_2_status_c'),

    # sdg16_2_3 through sdg16_2_7 (two links each, no suffix)
    ('2.3', 1): ('sdg16_2_3_evidence_link_1', 'sdg16_2_3_status'),
    ('2.3', 2): ('sdg16_2_3_evidence_link_2', 'sdg16_2_3_status'),
    ('2.4', 1): ('sdg16_2_4_evidence_link_1', 'sdg16_2_4_status'),
    ('2.4', 2): ('sdg16_2_4_evidence_link_2', 'sdg16_2_4_status'),
    ('2.5', 1): ('sdg16_2_5_evidence_link_1', 'sdg16_2_5_status'),
    ('2.5', 2): ('sdg16_2_5_evidence_link_2', 'sdg16_2_5_status'),
    ('2.7', 1): ('sdg16_2_7_evidence_link_1', 'sdg16_2_7_status'),
    ('2.7', 2): ('sdg16_2_7_evidence_link_2', 'sdg16_2_7_status'),

    # sdg16_2_6 (suffixes a–d, two links each)
    ('2.6a', 1): ('sdg16_2_6_evidence_link_1a', 'sdg16_2_6_status_a'),
    ('2.6a', 2): ('sdg16_2_6_evidence_link_2a', 'sdg16_2_6_status_a'),
    ('2.6b', 1): ('sdg16_2_6_evidence_link_1b', 'sdg16_2_6_status_b'),
    ('2.6b', 2): ('sdg16_2_6_evidence_link_2b', 'sdg16_2_6_status_b'),
    ('2.6c', 1): ('sdg16_2_6_evidence_link_1c', 'sdg16_2_6_status_c'),
    ('2.6c', 2): ('sdg16_2_6_evidence_link_2c', 'sdg16_2_6_status_c'),
    ('2.6d', 1): ('sdg16_2_6_evidence_link_1d', 'sdg16_2_6_status_d'),
    ('2.6d', 2): ('sdg16_2_6_evidence_link_2d', 'sdg16_2_6_status_d'),

    # sdg16_3_1 (suffixes a–c, two links each)
    ('3.1a', 1): ('sdg16_3_1_evidence_link_1a', 'sdg16_3_1_status_a'),
    ('3.1a', 2): ('sdg16_3_1_evidence_link_2a', 'sdg16_3_1_status_a'),
    ('3.1b', 1): ('sdg16_3_1_evidence_link_1b', 'sdg16_3_1_status_b'),
    ('3.1b', 2): ('sdg16_3_1_evidence_link_2b', 'sdg16_3_1_status_b'),
    ('3.1c', 1): ('sdg16_3_1_evidence_link_1c', 'sdg16_3_1_status_c'),
    ('3.1c', 2): ('sdg16_3_1_evidence_link_2c', 'sdg16_3_1_status_c'),

    # sdg16_3_2 through sdg16_3_4 (two links each, no suffix)
    ('3.2', 1): ('sdg16_3_2_evidence_link_1', 'sdg16_3_2_status'),
    ('3.2', 2): ('sdg16_3_2_evidence_link_2', 'sdg16_3_2_status'),
    ('3.3', 1): ('sdg16_3_3_evidence_link_1', 'sdg16_3_3_status'),
    ('3.3', 2): ('sdg16_3_3_evidence_link_2', 'sdg16_3_3_status'),
    ('3.4', 1): ('sdg16_3_4_evidence_link_1', 'sdg16_3_4_status'),
    ('3.4', 2): ('sdg16_3_4_evidence_link_2', 'sdg16_3_4_status'),

    # sdg16_4_1 and sdg16_4_2 (stand-alone evidence)
    ('4.1', 1): ('sdg16_4_1', 'sdg16_4_1_status'),
    ('4.2', 1): ('sdg16_4_2', 'sdg16_4_2_status'),
    }

    # initialize all values to None (so missing ones stay blank)
    values = {inp: None for inp,_ in comp_map.values()}
    values.update({st:  None for _,st in comp_map.values()})
    values['sdg16_4_1'] = None
    values['sdg16_4_2'] = None
    values['sdg16_submitter'] = submitter
    values['sdg16_submitter_office'] = office

    # populate from DB
    for _, r in ev_df.iterrows():
        cid = (r['code'], int(r['link']))
        inp_id, st_id = comp_map[cid]
        # numeric metrics go back to float
        if cid[0] in ('4.1', '4.2'):
            values[inp_id] = float(r['url'])
        else:
            values[inp_id] = r['url']
        values[st_id] = r['status']

    # return in the exact order of your Outputs
    return [
      values['sdg16_2_1_evidence_link_1'], values['sdg16_2_1_evidence_link_2'], values['sdg16_2_2_evidence_link_1a'], values['sdg16_2_2_evidence_link_2a'], 
      values['sdg16_2_2_evidence_link_1b'], values['sdg16_2_2_evidence_link_2b'], values['sdg16_2_2_evidence_link_1c'], values['sdg16_2_2_evidence_link_2c'], 
      values['sdg16_2_3_evidence_link_1'], values['sdg16_2_3_evidence_link_2'], values['sdg16_2_4_evidence_link_1'], values['sdg16_2_4_evidence_link_2'], 
      values['sdg16_2_5_evidence_link_1'], values['sdg16_2_5_evidence_link_2'], values['sdg16_2_6_evidence_link_1a'], values['sdg16_2_6_evidence_link_2a'], 
      values['sdg16_2_6_evidence_link_1b'], values['sdg16_2_6_evidence_link_2b'], values['sdg16_2_6_evidence_link_1c'], values['sdg16_2_6_evidence_link_2c'], 
      values['sdg16_2_6_evidence_link_1d'], values['sdg16_2_6_evidence_link_2d'], values['sdg16_2_7_evidence_link_1'], values['sdg16_2_7_evidence_link_2'], 
      values['sdg16_3_1_evidence_link_1a'], values['sdg16_3_1_evidence_link_2a'], values['sdg16_3_1_evidence_link_1b'], values['sdg16_3_1_evidence_link_2b'], 
      values['sdg16_3_1_evidence_link_1c'], values['sdg16_3_1_evidence_link_2c'], values['sdg16_3_2_evidence_link_1'], values['sdg16_3_2_evidence_link_2'], 
      values['sdg16_3_3_evidence_link_1'], values['sdg16_3_3_evidence_link_2'], values['sdg16_3_4_evidence_link_1'], values['sdg16_3_4_evidence_link_2'], 
      values['sdg16_4_1'], values['sdg16_4_2'], values['sdg16_2_1_status'], values['sdg16_2_2_status_a'], values['sdg16_2_2_status_b'], values['sdg16_2_2_status_c'], 
      values['sdg16_2_3_status'], values['sdg16_2_4_status'], values['sdg16_2_5_status'], values['sdg16_2_6_status_a'], values['sdg16_2_6_status_b'], 
      values['sdg16_2_6_status_c'], values['sdg16_2_6_status_d'], values['sdg16_2_7_status'], values['sdg16_3_1_status_a'], values['sdg16_3_1_status_b'], 
      values['sdg16_3_1_status_c'], values['sdg16_3_2_status'], values['sdg16_3_3_status'], values['sdg16_3_4_status'], values['sdg16_4_1_status'], 
      values['sdg16_4_2_status'],
      values['sdg16_submitter'], values['sdg16_submitter_office']
    ]


@app.callback(
    [
        Output("sdg16_comment_modal", "is_open"),
        Output("sdg16_comment_modal_header", "children"),
        Output("sdg16_comment_modal_body", "children"),
    ],
    # Inputs: all comment-buttons + the modal Close button
    [
        Input("sdg16_2_1_comment", "n_clicks"),
        Input("sdg16_2_2_comment_a", "n_clicks"),
        Input("sdg16_2_2_comment_b", "n_clicks"),
        Input("sdg16_2_2_comment_c", "n_clicks"),
        Input("sdg16_2_3_comment", "n_clicks"),
        Input("sdg16_2_4_comment", "n_clicks"),
        Input("sdg16_2_5_comment", "n_clicks"),
        Input("sdg16_2_6_comment_a", "n_clicks"),
        Input("sdg16_2_6_comment_b", "n_clicks"),
        Input("sdg16_2_6_comment_c", "n_clicks"),
        Input("sdg16_2_6_comment_d", "n_clicks"),
        Input("sdg16_2_7_comment", "n_clicks"),
        Input("sdg16_3_1_comment_a", "n_clicks"),
        Input("sdg16_3_1_comment_b", "n_clicks"),
        Input("sdg16_3_1_comment_c", "n_clicks"),
        Input("sdg16_3_2_comment", "n_clicks"),
        Input("sdg16_3_3_comment", "n_clicks"),
        Input("sdg16_3_4_comment", "n_clicks"),
        Input("sdg16_4_1_comment", "n_clicks"),
        Input("sdg16_4_2_comment", "n_clicks"),
        Input("sdg16_comment_modal_close", "n_clicks"),
    ],
    [ State("url", "search") ]  # to get submission_id from the URL
)
def display_comment(
    btn_1, btn_2,
    btn_3, btn_4, btn_5, btn_6, btn_7, btn_8,
    btn_9, btn_10, btn_11, btn_12, btn_13,
    btn_14, btn_15, btn_16, btn_17, btn_18, btn_19, btn_20,
    btn_close,
    search
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # If Close button clicked, just hide
    if clicked_id == "sdg16_comment_modal_close":
        return False, dash.no_update, dash.no_update

    # map button id → (metric_code, link_number)
    btn_map = {
        "sdg16_2_1_comment":      ("2.1",  1),
        "sdg16_2_2_comment_a":    ("2.2a", 1),
        "sdg16_2_2_comment_b":    ("2.2b", 1),
        "sdg16_2_2_comment_c":    ("2.2c", 1),
        "sdg16_2_3_comment":      ("2.3",  1),
        "sdg16_2_4_comment":      ("2.4",  1),
        "sdg16_2_5_comment":      ("2.5",  1),
        "sdg16_2_6_comment_a":    ("2.6a", 1),
        "sdg16_2_6_comment_b":    ("2.6b", 1),
        "sdg16_2_6_comment_c":    ("2.6c", 1),
        "sdg16_2_6_comment_d":    ("2.6d", 1),
        "sdg16_2_7_comment":      ("2.7",  1),

        "sdg16_3_1_comment_a":    ("3.1a", 1),
        "sdg16_3_1_comment_b":    ("3.1b", 1),
        "sdg16_3_1_comment_c":    ("3.1c", 1),
        "sdg16_3_2_comment":      ("3.2",  1),
        "sdg16_3_3_comment":      ("3.3",  1),
        "sdg16_3_4_comment":      ("3.4",  1),

        "sdg16_4_1_comment":      ("4.1",  1),
        "sdg16_4_2_comment":      ("4.2",  1),
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
        # 16.2 University governance measures (12 alerts)
        Output("sdg16_2_1_alert", "style"),       # 2.1
        Output("sdg16_2_2_alert_a", "style"),     # 2.2a
        Output("sdg16_2_2_alert_b", "style"),     # 2.2b
        Output("sdg16_2_2_alert_c", "style"),     # 2.2c
        Output("sdg16_2_3_alert", "style"),       # 2.3
        Output("sdg16_2_4_alert", "style"),       # 2.4
        Output("sdg16_2_5_alert", "style"),       # 2.5
        Output("sdg16_2_6_alert_a", "style"),     # 2.6a
        Output("sdg16_2_6_alert_b", "style"),     # 2.6b
        Output("sdg16_2_6_alert_c", "style"),     # 2.6c
        Output("sdg16_2_6_alert_d", "style"),     # 2.6d
        Output("sdg16_2_7_alert", "style"),       # 2.7

        # 16.3 Working with government (6 alerts)
        Output("sdg16_3_1_alert_a", "style"),     # 3.1a
        Output("sdg16_3_1_alert_b", "style"),     # 3.1b
        Output("sdg16_3_1_alert_c", "style"),     # 3.1c
        Output("sdg16_3_2_alert", "style"),       # 3.2
        Output("sdg16_3_3_alert", "style"),       # 3.3
        Output("sdg16_3_4_alert", "style"),       # 3.4

        # 16.4 Graduates in law & enforcement (2 alerts)
        Output("sdg16_4_1_alert", "style"),       # 4.1
        Output("sdg16_4_2_alert", "style"),       # 4.2
    ],
    Input("url", "pathname"),
    State("url", "search"),
)
def show_sdg16_alerts(pathname, search):
    if pathname != "/sdglist/sdg16submission":
        raise PreventUpdate

    # parse submission_id
    qs = parse_qs(urlparse(search).query)
    try:
        sub_id = int(qs.get("id", [""])[0])
    except:
        return [{"display": "none"}] * 20

    # fetch evidence statuses
    sql = """
        SELECT m.code, e.link_number, e.status_id
          FROM kmteam.evidence e
          JOIN kmteam.metric  m ON e.metric_id = m.metric_id
         WHERE e.submission_id = %s
    """
    df = db.querydatafromdatabase(sql, [sub_id], ["code", "link", "status_id"])
    status_map = {(row.code, row.link): row.status_id for _, row in df.iterrows()}

    groups = [
        # 16.2
        [("2.1", 1), ("2.1", 2)],
        [("2.2a", 1)], [("2.2b", 1)], [("2.2c", 1)],
        [("2.3", 1)], [("2.4", 1)], [("2.5", 1)],
        [("2.6a", 1)], [("2.6b", 1)], [("2.6c", 1)], [("2.6d", 1)],
        [("2.7", 1)],

        # 16.3
        [("3.1a", 1)], [("3.1b", 1)], [("3.1c", 1)],
        [("3.2", 1)], [("3.3", 1)], [("3.4", 1)],

        # 16.4
        [("4.1", 1)], [("4.2", 1)],
    ]

    def style_for(group):
        for code, ln in group:
            if status_map.get((code, ln)) in (1, 3):
                return {"display": "block"}
        return {"display": "none"}

    return [style_for(g) for g in groups]


@app.callback(
    [
        Output("header_sdg16_2_alert", "style"),
        Output("header_sdg16_3_alert", "style"),
        Output("header_sdg16_4_alert", "style"),
    ],
    Input("url", "pathname"),
    State("url", "search"),
)
def show_sdg16_section_headers(pathname, search):
    if pathname != "/sdglist/sdg16submission":
        raise PreventUpdate

    qs = parse_qs(urlparse(search).query)
    try:
        sub_id = int(qs.get("id", [""])[0])
    except:
        return [{"display": "none"}] * 3

    sql = """
        SELECT m.code, e.link_number, e.status_id
          FROM kmteam.evidence e
          JOIN kmteam.metric  m ON e.metric_id = m.metric_id
         WHERE e.submission_id = %s
    """
    
    df = db.querydatafromdatabase(sql, [sub_id], ["code", "link", "status_id"])
    status_map = {(row.code, row.link): row.status_id for _, row in df.iterrows()}

    section_groups = {
        "16.2": [
            ("2.1", 1), ("2.1", 2),
            ("2.2a", 1), ("2.2b", 1), ("2.2c", 1),
            ("2.3", 1), ("2.4", 1), ("2.5", 1),
            ("2.6a", 1), ("2.6b", 1), ("2.6c", 1), ("2.6d", 1),
            ("2.7", 1),
        ],
        "16.3": [
            ("3.1a", 1), ("3.1b", 1), ("3.1c", 1),
            ("3.2", 1), ("3.3", 1), ("3.4", 1),
        ],
        "16.4": [
            ("4.1", 1), ("4.2", 1),
        ],
    }

    def any_flag(pairs):
        return any(status_map.get(pair) in (1, 3) for pair in pairs)

    def to_style(flag):
        return {"display": "block"} if flag else {"display": "none"}

    return [
        to_style(any_flag(section_groups["16.2"])),
        to_style(any_flag(section_groups["16.3"])),
        to_style(any_flag(section_groups["16.4"])),
    ]
