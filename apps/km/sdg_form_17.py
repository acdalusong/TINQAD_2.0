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
    [17],
    ["metric_id","code"]
)
metrics_map = dict(zip(all_metrics["code"], all_metrics["metric_id"]))

metric_info_df = db.querydatafromdatabase(
    "SELECT code, additional_information FROM kmteam.metric WHERE sdg_number = %s",
    [17],
    ["code","additional_information"],
)
additional_info = dict(
    zip(metric_info_df["code"], metric_info_df["additional_information"])
)

sdg17_form = dbc.Form([

    # ─────────────── Submitter’s Profile ───────────────
    dbc.Card([
        dbc.CardHeader(
            html.H5("Submitter's Profile"),
            style={"backgroundColor": highlight_colors['secondary'], "color": "white"}
        ),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(dbc.Label("Name of Submitter"), width=6),
                dbc.Col(dbc.Input(id="sdg17_submitter", type="text"), width=6),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Label("Submitter's Office"), width=6),
                dbc.Col(dbc.Input(id="sdg17_submitter_office", type="text"), width=6),
            ], className="mb-3"),
        ]),
    ], className="mb-4"),

    dbc.Accordion(
        [
            # ─────────────── 17.2 Relationships to support the goals ───────────────
            dbc.AccordionItem(
                children=[

                    # header
                    dbc.Row([
                        dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=4),
                        dbc.Col(html.Label("Evidence Link 1", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                        dbc.Col(html.Label("Evidence Link 2", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                        dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                        dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                        dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                    ], className="mb-3"),

                    # 17.2.1
                    dbc.Row([
                        dbc.Col(html.Label("Relationships with regional NGOs and government for SDG policy", id="label-2-1", style={"cursor":"help"}), width=4),
                        dbc.Col(dbc.Input(id="sdg17_2_1_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_2_1_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_2_1_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_2_1_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_2_1_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.2.2
                    dbc.Row([
                        dbc.Col(html.Label("Cross-sectoral dialogue about SDGs", id="label-2-2", style={"cursor":"help"}), width=4),
                        dbc.Col(dbc.Input(id="sdg17_2_2_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_2_2_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_2_2_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_2_2_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_2_2_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.2.3
                    dbc.Row([
                        dbc.Col(html.Label("International collaboration data gathering for SDG", id="label-2-3", style={"cursor":"help"}), width=4),
                        dbc.Col(dbc.Input(id="sdg17_2_3_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_2_3_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_2_3_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_2_3_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_2_3_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.2.4
                    dbc.Row([
                        dbc.Col(html.Label("Collaboration for SDG best practice", id="label-2-4", style={"cursor":"help"}), width=4),
                        dbc.Col(dbc.Input(id="sdg17_2_4_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_2_4_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_2_4_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_2_4_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_2_4_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # sub‑section headline
                    dbc.Row(
                        dbc.Col(html.Label("Collaboration with NGOs for SDGs:", id="label-2-5", style={"fontStyle":"italic", "cursor":"help"}), width=12),
                        className="mb-2"
                    ),

                    # 17.2.5a
                    dbc.Row([
                        dbc.Col(html.Label("Student volunteering programmes", className="ps-4"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_2_5_evidence_link_1a", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_2_5_evidence_link_2a", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_2_5_status_a"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_2_5_comment_a", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_2_5_alert_a", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.2.5b
                    dbc.Row([
                        dbc.Col(html.Label("Research programmes", className="ps-4"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_2_5_evidence_link_1b", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_2_5_evidence_link_2b", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_2_5_status_b"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_2_5_comment_b", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_2_5_alert_b", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.2.5c
                    dbc.Row([
                        dbc.Col(html.Label("Development of educational resources", className="ps-4"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_2_5_evidence_link_1c", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_2_5_evidence_link_2c", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_2_5_status_c"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_2_5_comment_c", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_2_5_alert_c", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                ],
                title=html.Div(
                    [
                        html.Span("17.2 Relationships to support the goals", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg17_2_alert",
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


            # ─────────────── 17.3 Publication of SDG reports ───────────────
            dbc.AccordionItem(
                children=[
                    dbc.Row([
                        dbc.Col(html.Label("Guidance:", style={"fontWeight":"bold"}), width=2),
                        dbc.Col(html.Label("Please provide a link to the relevant report for each SDG you publish, either individually or within an annual report."), width=10),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(html.Label("Timeframe:", style={"fontWeight":"bold"}), width=2),
                        dbc.Col(html.Label("The sustainability report should be published in your most recent/ relevant academic year."), width=10),
                    ], className="mb-3"),
                    # header
                    dbc.Row([
                        dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=4),
                        dbc.Col(html.Label("Evidence Link 1", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                        dbc.Col(html.Label("Evidence Link 2", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                        dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                        dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                        dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                    ], className="mb-3"),

                    # 17.3.1 … through 17.3.17, all the same pattern:

                    dbc.Row([
                        dbc.Col(html.Label("SDG 1 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_1_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_1_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_1_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_1_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_1_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    dbc.Row([
                        dbc.Col(html.Label("SDG 2 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_2_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_2_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_2_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_2_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_2_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                                # 17.3.3 SDG 3 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 3 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_3_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_3_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_3_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_3_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_3_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.4 SDG 4 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 4 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_4_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_4_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_4_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_4_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_4_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.5 SDG 5 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 5 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_5_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_5_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_5_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_5_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_5_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.6 SDG 6 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 6 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_6_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_6_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_6_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_6_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_6_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.7 SDG 7 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 7 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_7_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_7_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_7_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_7_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_7_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.8 SDG 8 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 8 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_8_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_8_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_8_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_8_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_8_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.9 SDG 9 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 9 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_9_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_9_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_9_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_9_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_9_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.10 SDG 10 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 10 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_10_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_10_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_10_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_10_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_10_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.11 SDG 11 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 11 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_11_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_11_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_11_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_11_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_11_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.12 SDG 12 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 12 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_12_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_12_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_12_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_12_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_12_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.13 SDG 13 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 13 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_13_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_13_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_13_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_13_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_13_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.14 SDG 14 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 14 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_14_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_14_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_14_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_14_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_14_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.15 SDG 15 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 15 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_15_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_15_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_15_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_15_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_15_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.16 SDG 16 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 16 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_16_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_16_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_16_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_16_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_16_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.3.17 SDG 17 Publication
                    dbc.Row([
                        dbc.Col(html.Label("SDG 17 Publication"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_3_17_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_3_17_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_3_17_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_3_17_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_3_17_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),
                ],
                title=html.Div(
                    [
                        html.Span("17.3 Publication of SDG reports", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg17_3_alert",
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


            # ─────────────── 17.4 Education for SDGs commitment ───────────────
            dbc.AccordionItem(
                children=[

                    # header
                    dbc.Row([
                        dbc.Col(html.Label("Metric", style={"fontWeight":"bold","fontStyle":"italic"}), width=4),
                        dbc.Col(html.Label("Evidence Link 1", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                        dbc.Col(html.Label("Evidence Link 2", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                        dbc.Col(html.Label("Status", style={"fontWeight":"bold","fontStyle":"italic"}), width=2),
                        dbc.Col(html.Label("Comments", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                        dbc.Col(html.Label("Alert", style={"fontWeight":"bold","fontStyle":"italic"}), width=1),
                    ], className="mb-3"),

                    # sub‑section headline
                    dbc.Row(
                        dbc.Col(html.Label("Education for SDGs commitment to meaningful education:", id="label-4-1", style={"fontStyle":"italic", "cursor":"help"}), width=12),
                        className="mb-2"
                    ),

                    # 17.4.1a
                    dbc.Row([
                        dbc.Col(html.Label("Integration across full curriculum", className="ps-4"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_4_1_evidence_link_1a", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_4_1_evidence_link_2a", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_4_1_status_a"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_4_1_comment_a", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_4_1_alert_a", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.4.1b
                    dbc.Row([
                        dbc.Col(html.Label("Mandatory education for all", className="ps-4"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_4_1_evidence_link_1b", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_4_1_evidence_link_2b", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_4_1_status_b"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_4_1_comment_b", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_4_1_alert_b", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.4.1c
                    dbc.Row([
                        dbc.Col(html.Label("Optional education for all", className="ps-4"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_4_1_evidence_link_1c", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_4_1_evidence_link_2c", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_4_1_status_c"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_4_1_comment_c", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_4_1_alert_c", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.4.2
                    dbc.Row([
                        dbc.Col(html.Label("Education for SDGs: specific courses on sustainability",id="label-4-2", style={"cursor":"help"}), width=4),
                        dbc.Col(dbc.Input(id="sdg17_4_2_evidence_link_1", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_4_2_evidence_link_2", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_4_2_status"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_4_2_comment", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_4_2_alert", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # sub‑section: wider community
                    dbc.Row(
                        dbc.Col(html.Label("Education for SDGs in the wider community:", id="label-4-3", style={"fontStyle":"italic", "cursor":"help"}), width=12),
                        className="mb-2"
                    ),

                    # 17.4.3a
                    dbc.Row([
                        dbc.Col(html.Label("Alumni education outreach", className="ps-4"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_4_3_evidence_link_1a", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_4_3_evidence_link_2a", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_4_3_status_a"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_4_3_comment_a", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_4_3_alert_a", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.4.3b
                    dbc.Row([
                        dbc.Col(html.Label("Local community outreach", className="ps-4"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_4_3_evidence_link_1b", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_4_3_evidence_link_2b", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_4_3_status_b"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_4_3_comment_b", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_4_3_alert_b", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                    # 17.4.3c
                    dbc.Row([
                        dbc.Col(html.Label("Displaced people and refugees outreach", className="ps-4"), width=4),
                        dbc.Col(dbc.Input(id="sdg17_4_3_evidence_link_1c", type="text"), width=2),
                        dbc.Col(dbc.Input(id="sdg17_4_3_evidence_link_2c", type="text"), width=2),
                        dbc.Col(dbc.Select(id="sdg17_4_3_status_c"), width=2),
                        dbc.Col(dbc.Button("View", id="sdg17_4_3_comment_c", color="warning", size="sm", className="w-100"), width=1),
                        dbc.Col(html.Div(
                            dbc.Alert(html.I(className="bi bi-exclamation-triangle-fill me-2"),
                                    color="danger", className="d-flex align-items-center justify-content-center p-2 m-0"),
                            id="sdg17_4_3_alert_c", style={"display":"none"}
                        ), width=1),
                    ], className="mb-3"),

                ],
                title=html.Div(
                    [
                        html.Span("17.4 Education for SDGs commitment", style={"fontWeight": "bold"}),
                        html.Div(
                            dbc.Alert(
                                ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                                color="danger",
                                className="d-inline-flex align-items-center p-1 m-0",
                                style={"border":"none","background":"transparent"}
                            ),
                            id="header_sdg17_4_alert",
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
        ], 
        start_collapsed=True, 
        always_open=True
    ),
], className="mb-4") 

tooltip_2_1 = dbc.Tooltip(
    additional_info.get("2.1", ""),   # your hover-text
    target="label-2-1",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_2_2 = dbc.Tooltip(
    additional_info.get("2.2", ""),   # your hover-text
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
    additional_info.get("2.5a", ""),   # your hover-text
    target="label-2-5",                # must match the Label id
    placement="left",                   # options: "top", "right",...
    delay={"show": 300, "hide": 100},
)
tooltip_4_1 = dbc.Tooltip(
    additional_info.get("4.1a", ""),   # your hover-text
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
tooltip_4_3 = dbc.Tooltip(
    additional_info.get("4.3a", ""),   # your hover-text
    target="label-4-3",                # must match the Label id
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
                                dcc.Store(id='sdg17_toload', storage_type='memory', data=0),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H1(id="sdg17_page_header"),
                                            width=8
                                        ),
                                        dbc.Col(
                                            dbc.Button("Back", color="success", href="/sdglist"),
                                            width=4,
                                            id="sdg17_back_btn_div",
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
                        tooltip_4_1,  
                        tooltip_4_2,  
                        tooltip_4_3,  
                        sdg17_form,
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
                                                                id="sdg17_evidence_status",
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
                                                                id="sdg17_evidence_comments",
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
                            id="sdg17_evidence_div",
                            style={"display": "none"},  # hidden initially
                        ),
                        html.Br(),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='sdg17_removerecord',
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
                            id='sdg17_removerecord_div'
                        ),
                        dbc.Alert(id='sdg17_alert', is_open=False),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H5(id="sdg17_comment_modal_header")),
                                dbc.ModalBody(html.Div(id="sdg17_comment_modal_body")),
                                dbc.ModalFooter(
                                    dbc.Button("Close", id="sdg17_comment_modal_close", color="secondary")
                                ),
                            ],
                            id="sdg17_comment_modal",
                            is_open=False,
                            centered=True,
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id='sdg17_last_modal_header'), close_button=False, className="bg-success", style={"color": "white"}),
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
                            id="sdg17_last_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), close_button=True, className="bg-primary"),
                                dbc.ModalBody(
                                    html.H5(id="sdg17_initial_modal_message"),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Spinner(color="success", id="sdg17_spinner", spinner_style={"display":"none"}),
                                        dbc.Button("Cancel", id="sdg17_initial_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id="sdg17_initial_modal_confirm", color="success"),
                                    ]
                                ),
                            ],
                            centered=True,
                            id="sdg17_initial_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                        html.Br(),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Button("Save", color="primary", id="sdg17_save_button", n_clicks=0),
                                        width="auto"
                                    ),
                                    dbc.Col(
                                        dbc.Button("Cancel", color="warning", id="sdg17_cancel_button", n_clicks=0, href="/sdglist"),
                                        width="auto"
                                    ),
                                ],
                                className="mb-2",
                                justify="end",
                            ),
                            id="sdg17_buttons_div"
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
        Output('sdg17_spinner', 'spinner_style')
    ],
    [
        Input('sdg17_initial_modal_confirm', 'n_clicks'),
    ]
)
def save_sdg17(confirm):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    if eventid == 'sdg17_initial_modal_confirm' and confirm:
        return [{"display":"block"}]
    else:
        return [{"display":"none"}]


@app.callback(
    [
        # Check if all fields are filled
        Output('sdg17_last_modal', 'is_open'),
        Output('sdg17_last_modal_header', 'children'),
        #Initial Field
        Output('sdg17_initial_modal', 'is_open'),
        Output('sdg17_initial_modal_message', 'children'),
        Output('sdg17_initial_modal_confirm', 'color'),
        Output('sdg17_alert', 'is_open'),
        Output('sdg17_alert', 'color'),
        Output('sdg17_alert', 'children'),
        Output('sdg17_submitter', 'className'),
        Output('sdg17_submitter_office', 'className')
    ],
    [
        Input('sdg17_save_button', 'n_clicks'),
        Input('sdg17_initial_modal_confirm', 'n_clicks'),
        Input('sdg17_initial_modal_cancel', 'n_clicks'),
    ],
    [
        State('sdg17_2_1_evidence_link_1', 'value'),
        State('sdg17_2_1_evidence_link_2', 'value'),
        State('sdg17_2_2_evidence_link_1', 'value'),
        State('sdg17_2_2_evidence_link_2', 'value'),
        State('sdg17_2_3_evidence_link_1', 'value'),
        State('sdg17_2_3_evidence_link_2', 'value'),
        State('sdg17_2_4_evidence_link_1', 'value'),
        State('sdg17_2_4_evidence_link_2', 'value'),
        State('sdg17_2_5_evidence_link_1a', 'value'),
        State('sdg17_2_5_evidence_link_2a', 'value'),
        State('sdg17_2_5_evidence_link_1b', 'value'),
        State('sdg17_2_5_evidence_link_2b', 'value'),
        State('sdg17_2_5_evidence_link_1c', 'value'),
        State('sdg17_2_5_evidence_link_2c', 'value'),
        State('sdg17_3_1_evidence_link_1', 'value'),
        State('sdg17_3_1_evidence_link_2', 'value'),
        State('sdg17_3_2_evidence_link_1', 'value'),
        State('sdg17_3_2_evidence_link_2', 'value'),
        State('sdg17_3_3_evidence_link_1', 'value'),
        State('sdg17_3_3_evidence_link_2', 'value'),
        State('sdg17_3_4_evidence_link_1', 'value'),
        State('sdg17_3_4_evidence_link_2', 'value'),
        State('sdg17_3_5_evidence_link_1', 'value'),
        State('sdg17_3_5_evidence_link_2', 'value'),
        State('sdg17_3_6_evidence_link_1', 'value'),
        State('sdg17_3_6_evidence_link_2', 'value'),
        State('sdg17_3_7_evidence_link_1', 'value'),
        State('sdg17_3_7_evidence_link_2', 'value'),
        State('sdg17_3_8_evidence_link_1', 'value'),
        State('sdg17_3_8_evidence_link_2', 'value'),
        State('sdg17_3_9_evidence_link_1', 'value'),
        State('sdg17_3_9_evidence_link_2', 'value'),
        State('sdg17_3_10_evidence_link_1', 'value'),
        State('sdg17_3_10_evidence_link_2', 'value'),
        State('sdg17_3_11_evidence_link_1', 'value'),
        State('sdg17_3_11_evidence_link_2', 'value'),
        State('sdg17_3_12_evidence_link_1', 'value'),
        State('sdg17_3_12_evidence_link_2', 'value'),
        State('sdg17_3_13_evidence_link_1', 'value'),
        State('sdg17_3_13_evidence_link_2', 'value'),
        State('sdg17_3_14_evidence_link_1', 'value'),
        State('sdg17_3_14_evidence_link_2', 'value'),
        State('sdg17_3_15_evidence_link_1', 'value'),
        State('sdg17_3_15_evidence_link_2', 'value'),
        State('sdg17_3_16_evidence_link_1', 'value'),
        State('sdg17_3_16_evidence_link_2', 'value'),
        State('sdg17_3_17_evidence_link_1', 'value'),
        State('sdg17_3_17_evidence_link_2', 'value'),
        State('sdg17_4_1_evidence_link_1a', 'value'),
        State('sdg17_4_1_evidence_link_2a', 'value'),
        State('sdg17_4_1_evidence_link_1b', 'value'),
        State('sdg17_4_1_evidence_link_2b', 'value'),
        State('sdg17_4_1_evidence_link_1c', 'value'),
        State('sdg17_4_1_evidence_link_2c', 'value'),
        State('sdg17_4_2_evidence_link_1', 'value'),
        State('sdg17_4_2_evidence_link_2', 'value'),
        State('sdg17_4_3_evidence_link_1a', 'value'),
        State('sdg17_4_3_evidence_link_2a', 'value'),
        State('sdg17_4_3_evidence_link_1b', 'value'),
        State('sdg17_4_3_evidence_link_2b', 'value'),
        State('sdg17_4_3_evidence_link_1c', 'value'),
        State('sdg17_4_3_evidence_link_2c', 'value'),

        State('sdg17_submitter', 'value'),
        State('sdg17_submitter_office', 'value'),
        State('url', 'search'),
        State('sdg17_removerecord', 'value'),
        State('currentuserid', 'data')

    ],
)
def save_sdg17(
    submit, confirm, cancel, 
    sdg17_2_1_evidence_link_1, sdg17_2_1_evidence_link_2, sdg17_2_2_evidence_link_1, sdg17_2_2_evidence_link_2, sdg17_2_3_evidence_link_1, 
    sdg17_2_3_evidence_link_2, sdg17_2_4_evidence_link_1, sdg17_2_4_evidence_link_2, sdg17_2_5_evidence_link_1a, sdg17_2_5_evidence_link_2a,
    sdg17_2_5_evidence_link_1b, sdg17_2_5_evidence_link_2b, sdg17_2_5_evidence_link_1c, sdg17_2_5_evidence_link_2c, sdg17_3_1_evidence_link_1, 
    sdg17_3_1_evidence_link_2, sdg17_3_2_evidence_link_1, sdg17_3_2_evidence_link_2, sdg17_3_3_evidence_link_1, sdg17_3_3_evidence_link_2, 
    sdg17_3_4_evidence_link_1, sdg17_3_4_evidence_link_2, sdg17_3_5_evidence_link_1, sdg17_3_5_evidence_link_2, sdg17_3_6_evidence_link_1, 
    sdg17_3_6_evidence_link_2, sdg17_3_7_evidence_link_1, sdg17_3_7_evidence_link_2, sdg17_3_8_evidence_link_1, sdg17_3_8_evidence_link_2, 
    sdg17_3_9_evidence_link_1, sdg17_3_9_evidence_link_2, sdg17_3_10_evidence_link_1, sdg17_3_10_evidence_link_2, sdg17_3_11_evidence_link_1, 
    sdg17_3_11_evidence_link_2, sdg17_3_12_evidence_link_1, sdg17_3_12_evidence_link_2, sdg17_3_13_evidence_link_1, sdg17_3_13_evidence_link_2, 
    sdg17_3_14_evidence_link_1, sdg17_3_14_evidence_link_2, sdg17_3_15_evidence_link_1, sdg17_3_15_evidence_link_2, sdg17_3_16_evidence_link_1, 
    sdg17_3_16_evidence_link_2, sdg17_3_17_evidence_link_1, sdg17_3_17_evidence_link_2, sdg17_4_1_evidence_link_1a, sdg17_4_1_evidence_link_2a, 
    sdg17_4_1_evidence_link_1b, sdg17_4_1_evidence_link_2b, sdg17_4_1_evidence_link_1c, sdg17_4_1_evidence_link_2c, sdg17_4_2_evidence_link_1, 
    sdg17_4_2_evidence_link_2, sdg17_4_3_evidence_link_1a, sdg17_4_3_evidence_link_2a, sdg17_4_3_evidence_link_1b, sdg17_4_3_evidence_link_2b, 
    sdg17_4_3_evidence_link_1c, sdg17_4_3_evidence_link_2c,
    sdg17_submitter, sdg17_submitter_office,
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

    if eventid == 'sdg17_save_button' and submit:
        def get_input_class(value):
            return 'red-border' if not value else 'form-control'
        if not all([sdg17_submitter, sdg17_submitter_office]) and not removerecord:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            sdg_submitter_className = get_input_class(sdg17_submitter)
            sdg_submitter_office_className = get_input_class(sdg17_submitter_office)
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
    elif eventid == 'sdg17_initial_modal_confirm' and confirm:
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
            df_sub = db.execute_returning(sql_sub, [sdg17_submitter, sdg17_submitter_office, currentuserid], ['submission_id'])
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
            add_ev('2.1', 1, sdg17_2_1_evidence_link_1, None, None)
            add_ev('2.1', 2, sdg17_2_1_evidence_link_2, None, None)
            add_ev('2.2', 1, sdg17_2_2_evidence_link_1, None, None)
            add_ev('2.2', 2, sdg17_2_2_evidence_link_2, None, None)
            add_ev('2.3', 1, sdg17_2_3_evidence_link_1, None, None)
            add_ev('2.3', 2, sdg17_2_3_evidence_link_2, None, None)
            add_ev('2.4', 1, sdg17_2_4_evidence_link_1, None, None)
            add_ev('2.4', 2, sdg17_2_4_evidence_link_2, None, None)
            add_ev('2.5a', 1, sdg17_2_5_evidence_link_1a, None, None)
            add_ev('2.5a', 2, sdg17_2_5_evidence_link_2a, None, None)
            add_ev('2.5b', 1, sdg17_2_5_evidence_link_1b, None, None)
            add_ev('2.5b', 2, sdg17_2_5_evidence_link_2b, None, None)
            add_ev('2.5c', 1, sdg17_2_5_evidence_link_1c, None, None)
            add_ev('2.5c', 2, sdg17_2_5_evidence_link_2c, None, None)
            add_ev('3.1',  1, sdg17_3_1_evidence_link_1,  None, None)
            add_ev('3.1',  2, sdg17_3_1_evidence_link_2,  None, None)
            add_ev('3.2',  1, sdg17_3_2_evidence_link_1,  None, None)
            add_ev('3.2',  2, sdg17_3_2_evidence_link_2,  None, None)
            add_ev('3.3',  1, sdg17_3_3_evidence_link_1,  None, None)
            add_ev('3.3',  2, sdg17_3_3_evidence_link_2,  None, None)
            add_ev('3.4',  1, sdg17_3_4_evidence_link_1,  None, None)
            add_ev('3.4',  2, sdg17_3_4_evidence_link_2,  None, None)
            add_ev('3.5',  1, sdg17_3_5_evidence_link_1,  None, None)
            add_ev('3.5',  2, sdg17_3_5_evidence_link_2,  None, None)
            add_ev('3.6',  1, sdg17_3_6_evidence_link_1,  None, None)
            add_ev('3.6',  2, sdg17_3_6_evidence_link_2,  None, None)
            add_ev('3.7',  1, sdg17_3_7_evidence_link_1,  None, None)
            add_ev('3.7',  2, sdg17_3_7_evidence_link_2,  None, None)
            add_ev('3.8',  1, sdg17_3_8_evidence_link_1,  None, None)
            add_ev('3.8',  2, sdg17_3_8_evidence_link_2,  None, None)
            add_ev('3.9',  1, sdg17_3_9_evidence_link_1,  None, None)
            add_ev('3.9',  2, sdg17_3_9_evidence_link_2,  None, None)
            add_ev('3.10', 1, sdg17_3_10_evidence_link_1, None, None)
            add_ev('3.10', 2, sdg17_3_10_evidence_link_2, None, None)
            add_ev('3.11', 1, sdg17_3_11_evidence_link_1, None, None)
            add_ev('3.11', 2, sdg17_3_11_evidence_link_2, None, None)
            add_ev('3.12', 1, sdg17_3_12_evidence_link_1, None, None)
            add_ev('3.12', 2, sdg17_3_12_evidence_link_2, None, None)
            add_ev('3.13', 1, sdg17_3_13_evidence_link_1, None, None)
            add_ev('3.13', 2, sdg17_3_13_evidence_link_2, None, None)
            add_ev('3.14', 1, sdg17_3_14_evidence_link_1, None, None)
            add_ev('3.14', 2, sdg17_3_14_evidence_link_2, None, None)
            add_ev('3.15', 1, sdg17_3_15_evidence_link_1, None, None)
            add_ev('3.15', 2, sdg17_3_15_evidence_link_2, None, None)
            add_ev('3.16', 1, sdg17_3_16_evidence_link_1, None, None)
            add_ev('3.16', 2, sdg17_3_16_evidence_link_2, None, None)
            add_ev('3.17', 1, sdg17_3_17_evidence_link_1, None, None)
            add_ev('3.17', 2, sdg17_3_17_evidence_link_2, None, None)
            add_ev('4.1a', 1, sdg17_4_1_evidence_link_1a, None, None)
            add_ev('4.1a', 2, sdg17_4_1_evidence_link_2a, None, None)
            add_ev('4.1b', 1, sdg17_4_1_evidence_link_1b, None, None)
            add_ev('4.1b', 2, sdg17_4_1_evidence_link_2b, None, None)
            add_ev('4.1c', 1, sdg17_4_1_evidence_link_1c, None, None)
            add_ev('4.1c', 2, sdg17_4_1_evidence_link_2c, None, None)
            add_ev('4.2', 1, sdg17_4_2_evidence_link_1, None, None)
            add_ev('4.2', 2, sdg17_4_2_evidence_link_2, None, None)
            add_ev('4.3a', 1, sdg17_4_3_evidence_link_1a, None, None)
            add_ev('4.3a', 2, sdg17_4_3_evidence_link_2a, None, None)
            add_ev('4.3b', 1, sdg17_4_3_evidence_link_1b, None, None)
            add_ev('4.3b', 2, sdg17_4_3_evidence_link_2b, None, None)
            add_ev('4.3c', 1, sdg17_4_3_evidence_link_1c, None, None)
            add_ev('4.3c', 2, sdg17_4_3_evidence_link_2c, None, None)

            # 3) Perform all evidence INSERTs
            ev_sql = """
            INSERT INTO kmteam.evidence
                (submission_id, metric_id, link_number, url, status_id, comment)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            for vals in to_insert:
                db.modifydatabase(ev_sql, vals)
            
            final_modal_open = True
            final_modal_header = "SDG 17 Evidences Successfully Submitted."
        
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
                [sdg17_submitter, sdg17_submitter_office, sub_id]
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
            add_ev('2.1', 1, sdg17_2_1_evidence_link_1)
            add_ev('2.1', 2, sdg17_2_1_evidence_link_2)
            add_ev('2.2', 1, sdg17_2_2_evidence_link_1)
            add_ev('2.2', 2, sdg17_2_2_evidence_link_2)
            add_ev('2.3', 1, sdg17_2_3_evidence_link_1)
            add_ev('2.3', 2, sdg17_2_3_evidence_link_2)
            add_ev('2.4', 1, sdg17_2_4_evidence_link_1)
            add_ev('2.4', 2, sdg17_2_4_evidence_link_2)
            add_ev('2.5a', 1, sdg17_2_5_evidence_link_1a)
            add_ev('2.5a', 2, sdg17_2_5_evidence_link_2a)
            add_ev('2.5b', 1, sdg17_2_5_evidence_link_1b)
            add_ev('2.5b', 2, sdg17_2_5_evidence_link_2b)
            add_ev('2.5c', 1, sdg17_2_5_evidence_link_1c)
            add_ev('2.5c', 2, sdg17_2_5_evidence_link_2c)
            add_ev('3.1', 1, sdg17_3_1_evidence_link_1)
            add_ev('3.1', 2, sdg17_3_1_evidence_link_2)
            add_ev('3.2', 1, sdg17_3_2_evidence_link_1)
            add_ev('3.2', 2, sdg17_3_2_evidence_link_2)
            add_ev('3.3', 1, sdg17_3_3_evidence_link_1)
            add_ev('3.3', 2, sdg17_3_3_evidence_link_2)
            add_ev('3.4', 1, sdg17_3_4_evidence_link_1)
            add_ev('3.4', 2, sdg17_3_4_evidence_link_2)
            add_ev('3.5', 1, sdg17_3_5_evidence_link_1)
            add_ev('3.5', 2, sdg17_3_5_evidence_link_2)
            add_ev('3.6', 1, sdg17_3_6_evidence_link_1)
            add_ev('3.6', 2, sdg17_3_6_evidence_link_2)
            add_ev('3.7', 1, sdg17_3_7_evidence_link_1)
            add_ev('3.7', 2, sdg17_3_7_evidence_link_2)
            add_ev('3.8', 1, sdg17_3_8_evidence_link_1)
            add_ev('3.8', 2, sdg17_3_8_evidence_link_2)
            add_ev('3.9', 1, sdg17_3_9_evidence_link_1)
            add_ev('3.9', 2, sdg17_3_9_evidence_link_2)
            add_ev('3.10', 1, sdg17_3_10_evidence_link_1)
            add_ev('3.10', 2, sdg17_3_10_evidence_link_2)
            add_ev('3.11', 1, sdg17_3_11_evidence_link_1)
            add_ev('3.11', 2, sdg17_3_11_evidence_link_2)
            add_ev('3.12', 1, sdg17_3_12_evidence_link_1)
            add_ev('3.12', 2, sdg17_3_12_evidence_link_2)
            add_ev('3.13', 1, sdg17_3_13_evidence_link_1)
            add_ev('3.13', 2, sdg17_3_13_evidence_link_2)
            add_ev('3.14', 1, sdg17_3_14_evidence_link_1)
            add_ev('3.14', 2, sdg17_3_14_evidence_link_2)
            add_ev('3.15', 1, sdg17_3_15_evidence_link_1)
            add_ev('3.15', 2, sdg17_3_15_evidence_link_2)
            add_ev('3.16', 1, sdg17_3_16_evidence_link_1)
            add_ev('3.16', 2, sdg17_3_16_evidence_link_2)
            add_ev('3.17', 1, sdg17_3_17_evidence_link_1)
            add_ev('3.17', 2, sdg17_3_17_evidence_link_2)
            add_ev('4.1a', 1, sdg17_4_1_evidence_link_1a)
            add_ev('4.1a', 2, sdg17_4_1_evidence_link_2a)
            add_ev('4.1b', 1, sdg17_4_1_evidence_link_1b)
            add_ev('4.1b', 2, sdg17_4_1_evidence_link_2b)
            add_ev('4.1c', 1, sdg17_4_1_evidence_link_1c)
            add_ev('4.1c', 2, sdg17_4_1_evidence_link_2c)
            add_ev('4.2', 1, sdg17_4_2_evidence_link_1)
            add_ev('4.2', 2, sdg17_4_2_evidence_link_2)
            add_ev('4.3a', 1, sdg17_4_3_evidence_link_1a)
            add_ev('4.3a', 2, sdg17_4_3_evidence_link_2a)
            add_ev('4.3b', 1, sdg17_4_3_evidence_link_1b)
            add_ev('4.3b', 2, sdg17_4_3_evidence_link_2b)
            add_ev('4.3c', 1, sdg17_4_3_evidence_link_1c)
            add_ev('4.3c', 2, sdg17_4_3_evidence_link_2c)

            final_modal_open = True
            final_modal_header = "SDG 17 Evidences Successfully Updated."

    elif eventid == 'sdg17_initial_modal_cancel' and cancel:
        initial_modal_open = False
        initial_modal_message = ''
          
    return [final_modal_open, final_modal_header, initial_modal_open, initial_modal_message, confirm_button_color, alert_open, alert_color, alert_text, sdg_submitter_className, sdg_submitter_office_className]

@app.callback(
    [
        Output('sdg17_2_1_status', 'options'),
        Output('sdg17_2_2_status', 'options'),
        Output('sdg17_2_3_status', 'options'),
        Output('sdg17_2_4_status', 'options'),
        Output('sdg17_2_5_status_a', 'options'),
        Output('sdg17_2_5_status_b', 'options'),
        Output('sdg17_2_5_status_c', 'options'),
        Output('sdg17_3_1_status', 'options'),
        Output('sdg17_3_2_status', 'options'),
        Output('sdg17_3_3_status', 'options'),
        Output('sdg17_3_4_status', 'options'),
        Output('sdg17_3_5_status', 'options'),
        Output('sdg17_3_6_status', 'options'),
        Output('sdg17_3_7_status', 'options'),
        Output('sdg17_3_8_status', 'options'),
        Output('sdg17_3_9_status', 'options'),
        Output('sdg17_3_10_status', 'options'),
        Output('sdg17_3_11_status', 'options'),
        Output('sdg17_3_12_status', 'options'),
        Output('sdg17_3_13_status', 'options'),
        Output('sdg17_3_14_status', 'options'),
        Output('sdg17_3_15_status', 'options'),
        Output('sdg17_3_16_status', 'options'),
        Output('sdg17_3_17_status', 'options'),
        Output('sdg17_4_1_status_a', 'options'),
        Output('sdg17_4_1_status_b', 'options'),
        Output('sdg17_4_1_status_c', 'options'),
        Output('sdg17_4_2_status', 'options'),
        Output('sdg17_4_3_status_a', 'options'),
        Output('sdg17_4_3_status_b', 'options'),
        Output('sdg17_4_3_status_c', 'options'),
        Output('sdg17_page_header', 'children'),
        Output('sdg17_toload', 'data'),
        Output('sdg17_removerecord_div', 'style'),
        Output('sdg17_buttons_div', 'style'),
        Output('sdg17_back_btn_div', 'style')
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
    if pathname != '/sdglist/sdg17submission':
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
        header = 'Add SDG 17 Evidence Submission'
        to_load = 0
        removediv_style = {'display': 'none'}
        buttondiv_style = None
        backbtn_div_style = {'display': 'none'}
    elif create_mode == 'edit':
        header = 'Edit SDG 17 Evidence Submission'
        to_load = 1
        removediv_style = None
        buttondiv_style = None
        backbtn_div_style = {'display': 'none'}
    elif create_mode == 'view':
        header = 'View SDG 17 Evidence Submission'
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
            status_options,
            header, to_load, removediv_style, buttondiv_style, backbtn_div_style]


@app.callback(
    [
        Output('sdg17_2_1_status', 'disabled'),
        Output('sdg17_2_2_status', 'disabled'),
        Output('sdg17_2_3_status', 'disabled'),
        Output('sdg17_2_4_status', 'disabled'),
        Output('sdg17_2_5_status_a', 'disabled'),
        Output('sdg17_2_5_status_b', 'disabled'),
        Output('sdg17_2_5_status_c', 'disabled'),
        Output('sdg17_3_1_status', 'disabled'),
        Output('sdg17_3_2_status', 'disabled'),
        Output('sdg17_3_3_status', 'disabled'),
        Output('sdg17_3_4_status', 'disabled'),
        Output('sdg17_3_5_status', 'disabled'),
        Output('sdg17_3_6_status', 'disabled'),
        Output('sdg17_3_7_status', 'disabled'),
        Output('sdg17_3_8_status', 'disabled'),
        Output('sdg17_3_9_status', 'disabled'),
        Output('sdg17_3_10_status', 'disabled'),
        Output('sdg17_3_11_status', 'disabled'),
        Output('sdg17_3_12_status', 'disabled'),
        Output('sdg17_3_13_status', 'disabled'),
        Output('sdg17_3_14_status', 'disabled'),
        Output('sdg17_3_15_status', 'disabled'),
        Output('sdg17_3_16_status', 'disabled'),
        Output('sdg17_3_17_status', 'disabled'),
        Output('sdg17_4_1_status_a', 'disabled'),
        Output('sdg17_4_1_status_b', 'disabled'),
        Output('sdg17_4_1_status_c', 'disabled'),
        Output('sdg17_4_2_status', 'disabled'),
        Output('sdg17_4_3_status_a', 'disabled'),
        Output('sdg17_4_3_status_b', 'disabled'),
        Output('sdg17_4_3_status_c', 'disabled'),
    ],
    Input('url', 'pathname')
)
def show_qao_other_options_div(pathname):
    # Only act when we're on the specific page
    if pathname != '/sdglist/sdg17submission':
        raise PreventUpdate

    return [True]*31


@app.callback(
    [
        Output('sdg17_2_1_evidence_link_1', 'value'),
        Output('sdg17_2_1_evidence_link_2', 'value'),
        Output('sdg17_2_2_evidence_link_1', 'value'),
        Output('sdg17_2_2_evidence_link_2', 'value'),
        Output('sdg17_2_3_evidence_link_1', 'value'),
        Output('sdg17_2_3_evidence_link_2', 'value'),
        Output('sdg17_2_4_evidence_link_1', 'value'),
        Output('sdg17_2_4_evidence_link_2', 'value'),
        Output('sdg17_2_5_evidence_link_1a', 'value'),
        Output('sdg17_2_5_evidence_link_2a', 'value'),
        Output('sdg17_2_5_evidence_link_1b', 'value'),
        Output('sdg17_2_5_evidence_link_2b', 'value'),
        Output('sdg17_2_5_evidence_link_1c', 'value'),
        Output('sdg17_2_5_evidence_link_2c', 'value'),
        Output('sdg17_3_1_evidence_link_1', 'value'),
        Output('sdg17_3_1_evidence_link_2', 'value'),
        Output('sdg17_3_2_evidence_link_1', 'value'),
        Output('sdg17_3_2_evidence_link_2', 'value'),
        Output('sdg17_3_3_evidence_link_1', 'value'),
        Output('sdg17_3_3_evidence_link_2', 'value'),
        Output('sdg17_3_4_evidence_link_1', 'value'),
        Output('sdg17_3_4_evidence_link_2', 'value'),
        Output('sdg17_3_5_evidence_link_1', 'value'),
        Output('sdg17_3_5_evidence_link_2', 'value'),
        Output('sdg17_3_6_evidence_link_1', 'value'),
        Output('sdg17_3_6_evidence_link_2', 'value'),
        Output('sdg17_3_7_evidence_link_1', 'value'),
        Output('sdg17_3_7_evidence_link_2', 'value'),
        Output('sdg17_3_8_evidence_link_1', 'value'),
        Output('sdg17_3_8_evidence_link_2', 'value'),
        Output('sdg17_3_9_evidence_link_1', 'value'),
        Output('sdg17_3_9_evidence_link_2', 'value'),
        Output('sdg17_3_10_evidence_link_1', 'value'),
        Output('sdg17_3_10_evidence_link_2', 'value'),
        Output('sdg17_3_11_evidence_link_1', 'value'),
        Output('sdg17_3_11_evidence_link_2', 'value'),
        Output('sdg17_3_12_evidence_link_1', 'value'),
        Output('sdg17_3_12_evidence_link_2', 'value'),
        Output('sdg17_3_13_evidence_link_1', 'value'),
        Output('sdg17_3_13_evidence_link_2', 'value'),
        Output('sdg17_3_14_evidence_link_1', 'value'),
        Output('sdg17_3_14_evidence_link_2', 'value'),
        Output('sdg17_3_15_evidence_link_1', 'value'),
        Output('sdg17_3_15_evidence_link_2', 'value'),
        Output('sdg17_3_16_evidence_link_1', 'value'),
        Output('sdg17_3_16_evidence_link_2', 'value'),
        Output('sdg17_3_17_evidence_link_1', 'value'),
        Output('sdg17_3_17_evidence_link_2', 'value'),
        Output('sdg17_4_1_evidence_link_1a', 'value'),
        Output('sdg17_4_1_evidence_link_2a', 'value'),
        Output('sdg17_4_1_evidence_link_1b', 'value'),
        Output('sdg17_4_1_evidence_link_2b', 'value'),
        Output('sdg17_4_1_evidence_link_1c', 'value'),
        Output('sdg17_4_1_evidence_link_2c', 'value'),
        Output('sdg17_4_2_evidence_link_1', 'value'),
        Output('sdg17_4_2_evidence_link_2', 'value'),
        Output('sdg17_4_3_evidence_link_1a', 'value'),
        Output('sdg17_4_3_evidence_link_2a', 'value'),
        Output('sdg17_4_3_evidence_link_1b', 'value'),
        Output('sdg17_4_3_evidence_link_2b', 'value'),
        Output('sdg17_4_3_evidence_link_1c', 'value'),
        Output('sdg17_4_3_evidence_link_2c', 'value'),

        Output('sdg17_2_1_status', 'value'),
        Output('sdg17_2_2_status', 'value'),
        Output('sdg17_2_3_status', 'value'),
        Output('sdg17_2_4_status', 'value'),
        Output('sdg17_2_5_status_a', 'value'),
        Output('sdg17_2_5_status_b', 'value'),
        Output('sdg17_2_5_status_c', 'value'),
        Output('sdg17_3_1_status', 'value'),
        Output('sdg17_3_2_status', 'value'),
        Output('sdg17_3_3_status', 'value'),
        Output('sdg17_3_4_status', 'value'),
        Output('sdg17_3_5_status', 'value'),
        Output('sdg17_3_6_status', 'value'),
        Output('sdg17_3_7_status', 'value'),
        Output('sdg17_3_8_status', 'value'),
        Output('sdg17_3_9_status', 'value'),
        Output('sdg17_3_10_status', 'value'),
        Output('sdg17_3_11_status', 'value'),
        Output('sdg17_3_12_status', 'value'),
        Output('sdg17_3_13_status', 'value'),
        Output('sdg17_3_14_status', 'value'),
        Output('sdg17_3_15_status', 'value'),
        Output('sdg17_3_16_status', 'value'),
        Output('sdg17_3_17_status', 'value'),
        Output('sdg17_4_1_status_a', 'value'),
        Output('sdg17_4_1_status_b', 'value'),
        Output('sdg17_4_1_status_c', 'value'),
        Output('sdg17_4_2_status', 'value'),
        Output('sdg17_4_3_status_a', 'value'),
        Output('sdg17_4_3_status_b', 'value'),
        Output('sdg17_4_3_status_c', 'value'),

        Output('sdg17_submitter', 'value'),
        Output('sdg17_submitter_office', 'value'),
    ],
    Input('sdg17_toload', 'modified_timestamp'),
    [
        State('sdg17_toload', 'data'),
        State('url', 'search')
    ]
)
def sdg17evidences_load(ts, toload, search):
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
    ('2.1', 1): ('sdg17_2_1_evidence_link_1', 'sdg17_2_1_status'),
    ('2.1', 2): ('sdg17_2_1_evidence_link_2', 'sdg17_2_1_status'),
    ('2.2', 1): ('sdg17_2_2_evidence_link_1', 'sdg17_2_2_status'),
    ('2.2', 2): ('sdg17_2_2_evidence_link_2', 'sdg17_2_2_status'),
    ('2.3', 1): ('sdg17_2_3_evidence_link_1', 'sdg17_2_3_status'),
    ('2.3', 2): ('sdg17_2_3_evidence_link_2', 'sdg17_2_3_status'),
    ('2.4', 1): ('sdg17_2_4_evidence_link_1', 'sdg17_2_4_status'),
    ('2.4', 2): ('sdg17_2_4_evidence_link_2', 'sdg17_2_4_status'),

    # sdg17_2_5 (suffixes a–c, two links each)
    ('2.5a', 1): ('sdg17_2_5_evidence_link_1a', 'sdg17_2_5_status_a'),
    ('2.5a', 2): ('sdg17_2_5_evidence_link_2a', 'sdg17_2_5_status_a'),
    ('2.5b', 1): ('sdg17_2_5_evidence_link_1b', 'sdg17_2_5_status_b'),
    ('2.5b', 2): ('sdg17_2_5_evidence_link_2b', 'sdg17_2_5_status_b'),
    ('2.5c', 1): ('sdg17_2_5_evidence_link_1c', 'sdg17_2_5_status_c'),
    ('2.5c', 2): ('sdg17_2_5_evidence_link_2c', 'sdg17_2_5_status_c'),

    # sdg17_3_1 through sdg17_3_17 (each with two links, no suffix)
    ('3.1',  1): ('sdg17_3_1_evidence_link_1',  'sdg17_3_1_status'),
    ('3.1',  2): ('sdg17_3_1_evidence_link_2',  'sdg17_3_1_status'),
    ('3.2',  1): ('sdg17_3_2_evidence_link_1',  'sdg17_3_2_status'),
    ('3.2',  2): ('sdg17_3_2_evidence_link_2',  'sdg17_3_2_status'),
    ('3.3',  1): ('sdg17_3_3_evidence_link_1',  'sdg17_3_3_status'),
    ('3.3',  2): ('sdg17_3_3_evidence_link_2',  'sdg17_3_3_status'),
    ('3.4',  1): ('sdg17_3_4_evidence_link_1',  'sdg17_3_4_status'),
    ('3.4',  2): ('sdg17_3_4_evidence_link_2',  'sdg17_3_4_status'),
    ('3.5',  1): ('sdg17_3_5_evidence_link_1',  'sdg17_3_5_status'),
    ('3.5',  2): ('sdg17_3_5_evidence_link_2',  'sdg17_3_5_status'),
    ('3.6',  1): ('sdg17_3_6_evidence_link_1',  'sdg17_3_6_status'),
    ('3.6',  2): ('sdg17_3_6_evidence_link_2',  'sdg17_3_6_status'),
    ('3.7',  1): ('sdg17_3_7_evidence_link_1',  'sdg17_3_7_status'),
    ('3.7',  2): ('sdg17_3_7_evidence_link_2',  'sdg17_3_7_status'),
    ('3.8',  1): ('sdg17_3_8_evidence_link_1',  'sdg17_3_8_status'),
    ('3.8',  2): ('sdg17_3_8_evidence_link_2',  'sdg17_3_8_status'),
    ('3.9',  1): ('sdg17_3_9_evidence_link_1',  'sdg17_3_9_status'),
    ('3.9',  2): ('sdg17_3_9_evidence_link_2',  'sdg17_3_9_status'),
    ('3.10', 1): ('sdg17_3_10_evidence_link_1', 'sdg17_3_10_status'),
    ('3.10', 2): ('sdg17_3_10_evidence_link_2', 'sdg17_3_10_status'),
    ('3.11', 1): ('sdg17_3_11_evidence_link_1', 'sdg17_3_11_status'),
    ('3.11', 2): ('sdg17_3_11_evidence_link_2', 'sdg17_3_11_status'),
    ('3.12', 1): ('sdg17_3_12_evidence_link_1', 'sdg17_3_12_status'),
    ('3.12', 2): ('sdg17_3_12_evidence_link_2', 'sdg17_3_12_status'),
    ('3.13', 1): ('sdg17_3_13_evidence_link_1', 'sdg17_3_13_status'),
    ('3.13', 2): ('sdg17_3_13_evidence_link_2', 'sdg17_3_13_status'),
    ('3.14', 1): ('sdg17_3_14_evidence_link_1', 'sdg17_3_14_status'),
    ('3.14', 2): ('sdg17_3_14_evidence_link_2', 'sdg17_3_14_status'),
    ('3.15', 1): ('sdg17_3_15_evidence_link_1', 'sdg17_3_15_status'),
    ('3.15', 2): ('sdg17_3_15_evidence_link_2', 'sdg17_3_15_status'),
    ('3.16', 1): ('sdg17_3_16_evidence_link_1', 'sdg17_3_16_status'),
    ('3.16', 2): ('sdg17_3_16_evidence_link_2', 'sdg17_3_16_status'),
    ('3.17', 1): ('sdg17_3_17_evidence_link_1', 'sdg17_3_17_status'),
    ('3.17', 2): ('sdg17_3_17_evidence_link_2', 'sdg17_3_17_status'),

    # sdg17_4_1 (suffixes a–c, two links each)
    ('4.1a', 1): ('sdg17_4_1_evidence_link_1a', 'sdg17_4_1_status_a'),
    ('4.1a', 2): ('sdg17_4_1_evidence_link_2a', 'sdg17_4_1_status_a'),
    ('4.1b', 1): ('sdg17_4_1_evidence_link_1b', 'sdg17_4_1_status_b'),
    ('4.1b', 2): ('sdg17_4_1_evidence_link_2b', 'sdg17_4_1_status_b'),
    ('4.1c', 1): ('sdg17_4_1_evidence_link_1c', 'sdg17_4_1_status_c'),
    ('4.1c', 2): ('sdg17_4_1_evidence_link_2c', 'sdg17_4_1_status_c'),

    # sdg17_4_2 (two links, no suffix)
    ('4.2', 1): ('sdg17_4_2_evidence_link_1', 'sdg17_4_2_status'),
    ('4.2', 2): ('sdg17_4_2_evidence_link_2', 'sdg17_4_2_status'),

    # sdg17_4_3 (suffixes a–c, two links each)
    ('4.3a', 1): ('sdg17_4_3_evidence_link_1a', 'sdg17_4_3_status_a'),
    ('4.3a', 2): ('sdg17_4_3_evidence_link_2a', 'sdg17_4_3_status_a'),
    ('4.3b', 1): ('sdg17_4_3_evidence_link_1b', 'sdg17_4_3_status_b'),
    ('4.3b', 2): ('sdg17_4_3_evidence_link_2b', 'sdg17_4_3_status_b'),
    ('4.3c', 1): ('sdg17_4_3_evidence_link_1c', 'sdg17_4_3_status_c'),
    ('4.3c', 2): ('sdg17_4_3_evidence_link_2c', 'sdg17_4_3_status_c'),
    }

    # initialize all values to None (so missing ones stay blank)
    values = {inp: None for inp,_ in comp_map.values()}
    values.update({st:  None for _,st in comp_map.values()})
    values['sdg17_submitter'] = submitter
    values['sdg17_submitter_office'] = office

    # populate from DB
    for _, r in ev_df.iterrows():
        cid = (r['code'], int(r['link']))
        inp_id, st_id = comp_map[cid]
        # numeric metrics go back to float
        if cid[0] in ('7.1'):
            values[inp_id] = float(r['url'])
        else:
            values[inp_id] = r['url']
        values[st_id] = r['status']

    # return in the exact order of your Outputs
    return [
      values['sdg17_2_1_evidence_link_1'], values['sdg17_2_1_evidence_link_2'], values['sdg17_2_2_evidence_link_1'], 
      values['sdg17_2_2_evidence_link_2'], values['sdg17_2_3_evidence_link_1'], values['sdg17_2_3_evidence_link_2'], 
      values['sdg17_2_4_evidence_link_1'], values['sdg17_2_4_evidence_link_2'], values['sdg17_2_5_evidence_link_1a'], 
      values['sdg17_2_5_evidence_link_2a'], values['sdg17_2_5_evidence_link_1b'], values['sdg17_2_5_evidence_link_2b'], 
      values['sdg17_2_5_evidence_link_1c'], values['sdg17_2_5_evidence_link_2c'], values['sdg17_3_1_evidence_link_1'],
      values['sdg17_3_1_evidence_link_2'], values['sdg17_3_2_evidence_link_1'], values['sdg17_3_2_evidence_link_2'], 
      values['sdg17_3_3_evidence_link_1'], values['sdg17_3_3_evidence_link_2'], values['sdg17_3_4_evidence_link_1'], 
      values['sdg17_3_4_evidence_link_2'], values['sdg17_3_5_evidence_link_1'], values['sdg17_3_5_evidence_link_2'], 
      values['sdg17_3_6_evidence_link_1'], values['sdg17_3_6_evidence_link_2'], values['sdg17_3_7_evidence_link_1'], 
      values['sdg17_3_7_evidence_link_2'], values['sdg17_3_8_evidence_link_1'], values['sdg17_3_8_evidence_link_2'], 
      values['sdg17_3_9_evidence_link_1'], values['sdg17_3_9_evidence_link_2'], values['sdg17_3_10_evidence_link_1'], 
      values['sdg17_3_10_evidence_link_2'], values['sdg17_3_11_evidence_link_1'], values['sdg17_3_11_evidence_link_2'], 
      values['sdg17_3_12_evidence_link_1'], values['sdg17_3_12_evidence_link_2'], values['sdg17_3_13_evidence_link_1'], 
      values['sdg17_3_13_evidence_link_2'], values['sdg17_3_14_evidence_link_1'], values['sdg17_3_14_evidence_link_2'], 
      values['sdg17_3_15_evidence_link_1'], values['sdg17_3_15_evidence_link_2'], values['sdg17_3_16_evidence_link_1'], 
      values['sdg17_3_16_evidence_link_2'], values['sdg17_3_17_evidence_link_1'], values['sdg17_3_17_evidence_link_2'], 
      values['sdg17_4_1_evidence_link_1a'], values['sdg17_4_1_evidence_link_2a'], values['sdg17_4_1_evidence_link_1b'], 
      values['sdg17_4_1_evidence_link_2b'], values['sdg17_4_1_evidence_link_1c'], values['sdg17_4_1_evidence_link_2c'], 
      values['sdg17_4_2_evidence_link_1'], values['sdg17_4_2_evidence_link_2'], values['sdg17_4_3_evidence_link_1a'], 
      values['sdg17_4_3_evidence_link_2a'], values['sdg17_4_3_evidence_link_1b'], values['sdg17_4_3_evidence_link_2b'], 
      values['sdg17_4_3_evidence_link_1c'], values['sdg17_4_3_evidence_link_2c'], values['sdg17_2_1_status'], values['sdg17_2_2_status'], 
      values['sdg17_2_3_status'], values['sdg17_2_4_status'], values['sdg17_2_5_status_a'], values['sdg17_2_5_status_b'], 
      values['sdg17_2_5_status_c'], values['sdg17_3_1_status'], values['sdg17_3_2_status'], values['sdg17_3_3_status'], 
      values['sdg17_3_4_status'], values['sdg17_3_5_status'], values['sdg17_3_6_status'], values['sdg17_3_7_status'], 
      values['sdg17_3_8_status'], values['sdg17_3_9_status'], values['sdg17_3_10_status'], values['sdg17_3_11_status'], 
      values['sdg17_3_12_status'], values['sdg17_3_13_status'], values['sdg17_3_14_status'], values['sdg17_3_15_status'], 
      values['sdg17_3_16_status'], values['sdg17_3_17_status'], values['sdg17_4_1_status_a'], values['sdg17_4_1_status_b'], 
      values['sdg17_4_1_status_c'], values['sdg17_4_2_status'], values['sdg17_4_3_status_a'], values['sdg17_4_3_status_b'], 
      values['sdg17_4_3_status_c'],
      values['sdg17_submitter'], values['sdg17_submitter_office']
    ]


@app.callback(
    [
        Output("sdg17_comment_modal", "is_open"),
        Output("sdg17_comment_modal_header", "children"),
        Output("sdg17_comment_modal_body", "children"),
    ],
    # Inputs: all comment-buttons + the modal Close button
    [
        Input("sdg17_2_1_comment", "n_clicks"),
        Input("sdg17_2_2_comment", "n_clicks"),
        Input("sdg17_2_3_comment", "n_clicks"),
        Input("sdg17_2_4_comment", "n_clicks"),
        Input("sdg17_2_5_comment_a", "n_clicks"),
        Input("sdg17_2_5_comment_b", "n_clicks"),
        Input("sdg17_2_5_comment_c", "n_clicks"),
        Input("sdg17_3_1_comment", "n_clicks"),
        Input("sdg17_3_2_comment", "n_clicks"),
        Input("sdg17_3_3_comment", "n_clicks"),
        Input("sdg17_3_4_comment", "n_clicks"),
        Input("sdg17_3_5_comment", "n_clicks"),
        Input("sdg17_3_6_comment", "n_clicks"),
        Input("sdg17_3_7_comment", "n_clicks"),
        Input("sdg17_3_8_comment", "n_clicks"),
        Input("sdg17_3_9_comment", "n_clicks"),
        Input("sdg17_3_10_comment", "n_clicks"),
        Input("sdg17_3_11_comment", "n_clicks"),
        Input("sdg17_3_12_comment", "n_clicks"),
        Input("sdg17_3_13_comment", "n_clicks"),
        Input("sdg17_3_14_comment", "n_clicks"),
        Input("sdg17_3_15_comment", "n_clicks"),
        Input("sdg17_3_16_comment", "n_clicks"),
        Input("sdg17_3_17_comment", "n_clicks"),
        Input("sdg17_4_1_comment_a", "n_clicks"),
        Input("sdg17_4_1_comment_b", "n_clicks"),
        Input("sdg17_4_1_comment_c", "n_clicks"),
        Input("sdg17_4_2_comment", "n_clicks"),
        Input("sdg17_4_3_comment_a", "n_clicks"),
        Input("sdg17_4_3_comment_b", "n_clicks"),
        Input("sdg17_4_3_comment_c", "n_clicks"),
        Input("sdg17_comment_modal_close", "n_clicks"),
    ],
    [ State("url", "search") ]  # to get submission_id from the URL
)
def display_comment(
    btn_1, btn_2,
    btn_3, btn_4, btn_5, btn_6, btn_7, btn_8,
    btn_9, btn_10, btn_11, btn_12, btn_13,
    btn_14, btn_15, btn_16, btn_17, btn_18, btn_19, btn_20,
    btn_21, btn_22, btn_23, btn_24, btn_25, btn_26, btn_27,
    btn_28, btn_29, btn_30, btn_31,
    btn_close,
    search
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # If Close button clicked, just hide
    if clicked_id == "sdg17_comment_modal_close":
        return False, dash.no_update, dash.no_update

    # map button id → (metric_code, link_number)
    btn_map = {
        "sdg17_2_1_comment":     ("2.1",   1),
        "sdg17_2_2_comment":     ("2.2",   1),
        "sdg17_2_3_comment":     ("2.3",   1),
        "sdg17_2_4_comment":     ("2.4",   1),
        "sdg17_2_5_comment_a":   ("2.5a",  1),
        "sdg17_2_5_comment_b":   ("2.5b",  1),
        "sdg17_2_5_comment_c":   ("2.5c",  1),

        "sdg17_3_1_comment":     ("3.1",   1),
        "sdg17_3_2_comment":     ("3.2",   1),
        "sdg17_3_3_comment":     ("3.3",   1),
        "sdg17_3_4_comment":     ("3.4",   1),
        "sdg17_3_5_comment":     ("3.5",   1),
        "sdg17_3_6_comment":     ("3.6",   1),
        "sdg17_3_7_comment":     ("3.7",   1),
        "sdg17_3_8_comment":     ("3.8",   1),
        "sdg17_3_9_comment":     ("3.9",   1),
        "sdg17_3_10_comment":    ("3.10",  1),
        "sdg17_3_11_comment":    ("3.11",  1),
        "sdg17_3_12_comment":    ("3.12",  1),
        "sdg17_3_13_comment":    ("3.13",  1),
        "sdg17_3_14_comment":    ("3.14",  1),
        "sdg17_3_15_comment":    ("3.15",  1),
        "sdg17_3_16_comment":    ("3.16",  1),
        "sdg17_3_17_comment":    ("3.17",  1),

        "sdg17_4_1_comment_a":   ("4.1a",  1),
        "sdg17_4_1_comment_b":   ("4.1b",  1),
        "sdg17_4_1_comment_c":   ("4.1c",  1),

        "sdg17_4_2_comment":     ("4.2",   1),

        "sdg17_4_3_comment_a":   ("4.3a",  1),
        "sdg17_4_3_comment_b":   ("4.3b",  1),
        "sdg17_4_3_comment_c":   ("4.3c",  1),
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
        # 17.2 Relationships to support the goals (7 alerts)
        Output("sdg17_2_1_alert",   "style"),
        Output("sdg17_2_2_alert",   "style"),
        Output("sdg17_2_3_alert",   "style"),
        Output("sdg17_2_4_alert",   "style"),
        Output("sdg17_2_5_alert_a", "style"),
        Output("sdg17_2_5_alert_b", "style"),
        Output("sdg17_2_5_alert_c", "style"),

        # 17.3 Publication of SDG reports (17 alerts)
        Output("sdg17_3_1_alert",  "style"),
        Output("sdg17_3_2_alert",  "style"),
        Output("sdg17_3_3_alert",  "style"),
        Output("sdg17_3_4_alert",  "style"),
        Output("sdg17_3_5_alert",  "style"),
        Output("sdg17_3_6_alert",  "style"),
        Output("sdg17_3_7_alert",  "style"),
        Output("sdg17_3_8_alert",  "style"),
        Output("sdg17_3_9_alert",  "style"),
        Output("sdg17_3_10_alert", "style"),
        Output("sdg17_3_11_alert", "style"),
        Output("sdg17_3_12_alert", "style"),
        Output("sdg17_3_13_alert", "style"),
        Output("sdg17_3_14_alert", "style"),
        Output("sdg17_3_15_alert", "style"),
        Output("sdg17_3_16_alert", "style"),
        Output("sdg17_3_17_alert", "style"),

        # 17.4 Education for SDGs commitment (7 alerts)
        Output("sdg17_4_1_alert_a", "style"),
        Output("sdg17_4_1_alert_b", "style"),
        Output("sdg17_4_1_alert_c", "style"),
        Output("sdg17_4_2_alert",   "style"),
        Output("sdg17_4_3_alert_a", "style"),
        Output("sdg17_4_3_alert_b", "style"),
        Output("sdg17_4_3_alert_c", "style"),
    ],
    Input("url", "pathname"),
    State("url", "search"),
)
def show_sdg17_alerts(pathname, search):
    if pathname != "/sdglist/sdg17submission":
        raise PreventUpdate

    # parse submission_id
    qs = parse_qs(urlparse(search).query)
    try:
        sub_id = int(qs.get("id", [""])[0])
    except:
        return [{"display": "none"}] * 31

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
        # 17.2
        [("2.1", 1), ("2.1", 2)],
        [("2.2", 1), ("2.2", 2)],
        [("2.3", 1), ("2.3", 2)],
        [("2.4", 1), ("2.4", 2)],
        [("2.5a", 1), ("2.5a", 2)],
        [("2.5b", 1), ("2.5b", 2)],
        [("2.5c", 1), ("2.5c", 2)],

        # 17.3
        [("3.1", 1),  ("3.1", 2)],
        [("3.2", 1),  ("3.2", 2)],
        [("3.3", 1),  ("3.3", 2)],
        [("3.4", 1),  ("3.4", 2)],
        [("3.5", 1),  ("3.5", 2)],
        [("3.6", 1),  ("3.6", 2)],
        [("3.7", 1),  ("3.7", 2)],
        [("3.8", 1),  ("3.8", 2)],
        [("3.9", 1),  ("3.9", 2)],
        [("3.10", 1), ("3.10", 2)],
        [("3.11", 1), ("3.11", 2)],
        [("3.12", 1), ("3.12", 2)],
        [("3.13", 1), ("3.13", 2)],
        [("3.14", 1), ("3.14", 2)],
        [("3.15", 1), ("3.15", 2)],
        [("3.16", 1), ("3.16", 2)],
        [("3.17", 1), ("3.17", 2)],

        # 17.4
        [("4.1a", 1), ("4.1a", 2)],
        [("4.1b", 1), ("4.1b", 2)],
        [("4.1c", 1), ("4.1c", 2)],
        [("4.2", 1),  ("4.2", 2)],
        [("4.3a", 1), ("4.3a", 2)],
        [("4.3b", 1), ("4.3b", 2)],
        [("4.3c", 1), ("4.3c", 2)],
    ]

    def style_for(group):
        # show if any link is flagged (1=Needs attention or 3=Critical)
        for code, ln in group:
            if status_map.get((code, ln)) in (1, 3):
                return {"display": "block"}
        return {"display": "none"}

    return [style_for(g) for g in groups]


@app.callback(
    [
        Output("header_sdg17_2_alert", "style"),
        Output("header_sdg17_3_alert", "style"),
        Output("header_sdg17_4_alert", "style"),
    ],
    Input("url", "pathname"),
    State("url", "search"),
)
def show_sdg17_section_headers(pathname, search):
    if pathname != "/sdglist/sdg17submission":
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
        "17.2": [
            ("2.1", 1), ("2.1", 2),
            ("2.2", 1), ("2.2", 2),
            ("2.3", 1), ("2.3", 2),
            ("2.4", 1), ("2.4", 2),
            ("2.5a", 1), ("2.5a", 2),
            ("2.5b", 1), ("2.5b", 2),
            ("2.5c", 1), ("2.5c", 2),
        ],
        "17.3": [
            ("3.1",  1), ("3.1",  2),
            ("3.2",  1), ("3.2",  2),
            ("3.3",  1), ("3.3",  2),
            ("3.4",  1), ("3.4",  2),
            ("3.5",  1), ("3.5",  2),
            ("3.6",  1), ("3.6",  2),
            ("3.7",  1), ("3.7",  2),
            ("3.8",  1), ("3.8",  2),
            ("3.9",  1), ("3.9",  2),
            ("3.10", 1), ("3.10", 2),
            ("3.11", 1), ("3.11", 2),
            ("3.12", 1), ("3.12", 2),
            ("3.13", 1), ("3.13", 2),
            ("3.14", 1), ("3.14", 2),
            ("3.15", 1), ("3.15", 2),
            ("3.16", 1), ("3.16", 2),
            ("3.17", 1), ("3.17", 2),
        ],
        "17.4": [
            ("4.1a", 1), ("4.1a", 2),
            ("4.1b", 1), ("4.1b", 2),
            ("4.1c", 1), ("4.1c", 2),
            ("4.2",  1), ("4.2",  2),
            ("4.3a", 1), ("4.3a", 2),
            ("4.3b", 1), ("4.3b", 2),
            ("4.3c", 1), ("4.3c", 2),
        ],
    }

    def any_flag(pairs):
        return any(status_map.get(pair) in (1, 3) for pair in pairs)

    def to_style(flag):
        return {"display": "block"} if flag else {"display": "none"}

    return [
        to_style(any_flag(section_groups["17.2"])),
        to_style(any_flag(section_groups["17.3"])),
        to_style(any_flag(section_groups["17.4"])),
    ]