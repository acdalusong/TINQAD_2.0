import json
import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, ALL, MATCH, callback_context, no_update
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import os
from urllib.parse import urlparse, parse_qs

# Ensure upload directory exists
UPLOAD_DIRECTORY = r".\assets\database\km\sdg"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
 

# ────────────────────────────────────────────────────────────────────────────────
# 1) Dynamically fetch all SDG-13 metrics (code + description) from the database
# ────────────────────────────────────────────────────────────────────────────────

metrics_df = db.querydatafromdatabase(
    """
    SELECT code, description
    FROM kmteam.metric
    WHERE sdg_number = 13
    ORDER BY metric_id
    """,
    [],
    ["code", "description"],
)

# Build a list of AccordionItem components, one per metric
accordion_items = []
for _, row in metrics_df.iterrows():
    metric_code = row["code"]
    metric_desc = row["description"]

    inner_div = html.Div(
        id={"type": "sdg13_list", "index": metric_code},
        style={
            "marginTop": "20px",
            "overflowX": "auto",
            "overflowY": "auto",
            "maxHeight": "400px",
        },
    )

    # AccordionItem with an initially hidden “Attention Required” icon
    accordion_items.append(
        dbc.AccordionItem(
            [inner_div],
            title=html.Div(
                [
                    html.Span(metric_desc, style={"fontWeight": "bold"}),
                    html.Div(
                        dbc.Alert(
                            ["Attention Required", html.I(className="bi bi-exclamation-triangle-fill ms-2")],
                            color="danger",
                            className="d-inline-flex align-items-center p-1 m-0",
                            style={"border": "none", "background": "transparent"},
                        ),
                        id={"type": "sdg13_header_alert", "index": metric_code},
                        style={"display": "none"},
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "width": "100%",
                },
            ),
        )
    )


# ────────────────────────────────────────────────────────────────────────────────
# 2) Assemble the overall layout, including stores and the modal
# ────────────────────────────────────────────────────────────────────────────────

sdg13_accordion = html.Div([
    dcc.Store(id="sdg13_admin_toload", storage_type="memory", data=None),
    dcc.Store(id="sdg13_update_counter", storage_type="memory", data=0),

    dbc.Accordion(
        accordion_items,
        start_collapsed=True,
        always_open=True,
    ),

    dbc.Modal([
        dbc.ModalHeader("Evaluate Evidence", id="sdg13_admin_modal_header"),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col(html.Label("Status"), width=4),
                dbc.Col(dbc.Select(id="sdg13_admin_modal_status", placeholder="Select status"), width=8),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Textarea(
                    id="sdg13_admin_modal_comments",
                    placeholder="Enter comments...",
                    style={"width": "100%", "minHeight": "120px"}
                ), width=12),
            ], className="mb-3"),
        ]),
        dbc.ModalFooter([
            dbc.Button("Save", id="sdg13_admin_modal_save", color="primary"),
            dbc.Button("Cancel", id="sdg13_admin_modal_cancel", color="secondary", className="ms-2"),
        ]),
    ], id="sdg13_admin_modal", is_open=False, centered=True, backdrop="static"),
])


# SDG color buttons at the bottom
sdg_colors = {
    1: "#e5233d", 2: "#dda73a", 3: "#4ca146", 4: "#c7212f",
    5: "#ef402d", 6: "#27bfe6", 7: "#fbc412", 8: "#a31c44",
    9: "#f26a2e", 10: "#e01483", 11: "#f89d2a", 12: "#bf8d2c",
    13: "#407f46", 14: "#1f97d4", 15: "#59ba47", 16: "#136a9f",
    17: "#14496b",
}
sdg_buttons = [
    dbc.Col(
        dbc.Button(
            f"SDG {i}",
            href=f"/SDG_evidencelist/sdg{i}",
            external_link=True,
            style={
                "backgroundColor": sdg_colors[i],
                "color": "white",
                "width": "100%",
                "height": "80px",
                "fontSize": "1.25rem",
                "marginBottom": "1rem",
            },
            className="d-flex justify-content-center align-items-center",
        ),
        width=2
    )
    for i in range(1,18)
]

layout = dbc.Container([
    dbc.Row([
        cm.sidebar,
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col(html.H1("SDG 13 Evidences"), width=8),
                    dbc.Col(dbc.Button("Back", color="success", href="/SDG_evidencelist"),
                            width=4, style={"display": "flex", "justifyContent": "flex-end"}),
                ], align="center"),
            ], className="mb-0"),
            html.Hr(),
            dbc.Alert(id="sdg13_admin_alert", is_open=False, duration=3000),
            sdg13_accordion,
            html.Br(),
            dbc.Card([
                dbc.CardHeader(html.H5("Click a particular SDG to view its evidence submissions."),
                               style={"backgroundColor": "#f8f9fa"}),
                dbc.CardBody(dbc.Row(sdg_buttons, justify="start", align="stretch")),
            ], className="mb-4"),
        ], width=9, style={"marginLeft": "15px"}),
    ]),
    html.Br(), html.Br(),
    dbc.Row(dbc.Col(cm.generate_footer(), width=12)),
], fluid=True)


# ────────────────────────────────────────────────────────────────────────────────
# 3) PATTERN‑MATCHING CALLBACK to BUILD A PIVOTED TABLE per submission
# ────────────────────────────────────────────────────────────────────────────────

@app.callback(
    Output({"type": "sdg13_list", "index": MATCH}, "children"),
    [ Input("url", "pathname"), Input("sdg13_update_counter", "data") ],
    [ State({"type": "sdg13_list", "index": MATCH}, "id") ],
)
def load_sdg13_metric_list(pathname, counter_update, id):
    if pathname != "/SDG_evidencelist/sdg13":
        raise PreventUpdate

    metric_code = id["index"]
    sql = """
        SELECT
          e.submission_id,
          e.evidence_id,
          e.link_number,
          e.url,
          e.status_id,            
          s.submitter,
          s.submitter_office,
          c.checkstatus_name AS status,
          e.comment
        FROM kmteam.evidence e
        LEFT JOIN kmteam.submission s ON e.submission_id = s.submission_id
        LEFT JOIN kmteam.metric   m ON e.metric_id     = m.metric_id
        LEFT JOIN kmteam.checkstatus c ON e.status_id  = c.checkstatus_id
        WHERE m.code = %s
          AND m.sdg_number = 13
          AND s.reckoning_period IN (
                SELECT reckoning_period_id
                FROM kmteam.reckoning_periods
                WHERE active_status = TRUE
                    AND reckoning_period_del_ind  = FALSE
                LIMIT 1
            )
          AND s.submission_del_ind = FALSE
        ORDER BY e.submission_id, e.link_number
    """
    df = db.querydatafromdatabase(
        sql, [metric_code],
        ["submission_id","evidence_id","LinkNo","URL","status_id","submitter","submitter_office","Status","Comments"]
    )

    if df.empty:
        return html.Div("No evidence found.", className="text-muted py-3")

    rows = []
    for sub_id, grp in df.groupby("submission_id"):
        urls = {ln: url for ln, url in zip(grp["LinkNo"], grp["URL"])}
        eids = {ln: eid for ln, eid in zip(grp["LinkNo"], grp["evidence_id"])}
        status   = grp.iloc[0]["Status"] or ""
        comments = grp.iloc[0]["Comments"] or ""

        # if any status_id is NULL → pending
        pending = grp["status_id"].isna().any()

        # build the two URL cells with copy buttons
        def make_url_cell(link_no):
            url = urls.get(link_no, "")
            eid = eids.get(link_no)
            if not url or not eid:
                return html.Td("")

            # unique target_id for dcc.Clipboard
            target_id = f"url-{eid}"
            return html.Td(
                html.Div(
                    [
                        # the link itself
                        html.A(url, href=url, target="_blank", id=target_id),

                        # the clipboard icon — clicking this will copy the text of the <A>
                        dcc.Clipboard(
                            target_id=target_id,
                            title="Copy URL to clipboard",
                            style={
                                "cursor": "pointer",
                                "marginLeft": "0.5rem",
                                "fontSize": "1rem",
                                "lineHeight": "1"
                            },
                        ),
                    ],
                    style={"display":"flex","alignItems":"center"}
                )
            )

        btn = dbc.Button(
            "Evaluate",
            id={"type": "eval", "index": json.dumps([eids.get(1), eids.get(2)])},
            size="sm", color="warning",
        )

        rows.append(html.Tr([
            html.Td(grp.iloc[0]["submitter"]),
            html.Td(grp.iloc[0]["submitter_office"]),
            make_url_cell(1),
            make_url_cell(2),
            html.Td(status),
            html.Td(comments),
            # ← new Alert column per row
            html.Td(
                html.Div(
                    dbc.Alert(
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        color="danger",
                        className="d-flex align-items-center justify-content-center p-2 m-0"
                    ),
                    style={"display":"block" if pending else "none"}
                )
            ),
            html.Td(btn),
        ]))

    table = dbc.Table([
        html.Thead(html.Tr([
            html.Th("Submitter"),
            html.Th("Office"),
            html.Th("Evidence 1"),
            html.Th("Evidence 2"),
            html.Th("Status"),
            html.Th("Comments"),
            html.Th("Alert"),      # ← header for new column
            html.Th("Action"),
        ])),
        html.Tbody(rows),
    ], bordered=True, hover=True, size="sm", responsive=True)

    return table


# ────────────────────────────────────────────────────────────────────────────────
# 4) SINGLE CALLBACK to OPEN/CLOSE and SAVE the ADMIN modal for BOTH evidence_ids
# ────────────────────────────────────────────────────────────────────────────────

@app.callback(
    [
        Output("sdg13_admin_modal",          "is_open"),
        Output("sdg13_admin_modal_status",   "options"),
        Output("sdg13_admin_modal_comments", "value"),
        Output("sdg13_admin_toload",         "data"),
        Output("sdg13_admin_modal_status",   "value"),
        Output("sdg13_admin_alert",          "is_open"),
        Output("sdg13_admin_alert",          "color"),
        Output("sdg13_admin_alert",          "children"),
        Output("sdg13_update_counter",       "data"),
    ],
    [
        Input({"type": "eval",   "index": ALL}, "n_clicks"),
        Input("sdg13_admin_modal_save",    "n_clicks"),
        Input("sdg13_admin_modal_cancel",  "n_clicks"),
    ],
    [
        State("sdg13_admin_modal",         "is_open"),
        State("sdg13_admin_toload",        "data"),
        State("sdg13_admin_modal_status",  "value"),
        State("sdg13_admin_modal_comments","value"),
        State("sdg13_update_counter",      "data"),
    ],
    prevent_initial_call=True,
)
def manage_admin_modal(eval_clicks, save_clicks, cancel_clicks,
                       is_open, toload, sel_status, sel_comments, update_counter):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered = ctx.triggered[0]
    prop_id   = triggered["prop_id"]
    val       = triggered["value"]

    # --- OPEN modal ---
    try:
        evt = json.loads(prop_id.split(".")[0])
    except:
        evt = {}
    if evt.get("type") == "eval" and val:
        ev_ids = json.loads(evt["index"])
        df = db.querydatafromdatabase(
            "SELECT status_id, comment FROM kmteam.evidence WHERE evidence_id = %s",
            [ev_ids[0]], ["status_id","comment"]
        )
        if not df.empty:
            current_status  = df.at[0,"status_id"]
            current_comment = df.at[0,"comment"] or ""
        else:
            current_status, current_comment = None, ""

        opts = db.querydatafromdatabase(
            "SELECT checkstatus_name AS label, checkstatus_id AS value FROM kmteam.checkstatus",
            [], ["label","value"]
        ).to_dict("records")

        return (True, opts, current_comment,
                evt["index"], current_status,
                False, "", "", no_update)

    # --- SAVE to both evidence_ids ---
    if prop_id.startswith("sdg13_admin_modal_save") and toload:
        ev_ids = json.loads(toload)
        for eid in ev_ids:
            db.modifydatabase(
                """
                UPDATE kmteam.evidence
                   SET status_id = %s,
                       comment   = %s
                 WHERE evidence_id = %s
                """,
                [sel_status, sel_comments, eid],
            )
        update_counter = (update_counter or 0) + 1
        return (False, no_update, no_update, None, None,
                True, "success", "Evidence evaluated successfully.",
                update_counter)

    # --- CANCEL ---
    if prop_id.startswith("sdg13_admin_modal_cancel"):
        return (False, no_update, no_update, None, None,
                False, "", "", no_update)

    return (is_open, no_update, no_update, no_update, no_update,
            False, "", "", no_update)


# ────────────────────────────────────────────────────────────────────────────────
# 5) CALLBACK to SHOW/HIDE each **AccordionItem** header icon
# ────────────────────────────────────────────────────────────────────────────────
@app.callback(
    Output({"type": "sdg13_header_alert", "index": ALL}, "style"),
    Input("sdg13_update_counter", "data"),
    State({"type": "sdg13_header_alert", "index": ALL}, "id"),
)
def show_metric_header_alerts(_counter, all_ids):
    # We fire on every admin save, so _counter bumps whenever ANY status changes.

    # 1) Query: for each metric code, do we have at least one evidence with status_id IS NULL?
    sql = """
      SELECT m.code,
             COUNT(*) FILTER (WHERE e.status_id IS NULL) AS pending_count
      FROM kmteam.evidence e
      JOIN kmteam.metric   m ON e.metric_id = m.metric_id
      WHERE m.sdg_number = 13
        AND e.submission_id IN (
             SELECT submission_id
             FROM kmteam.submission
             WHERE submission_del_ind = FALSE
			 AND reckoning_period IN (
                SELECT reckoning_period_id
                FROM kmteam.reckoning_periods
                WHERE active_status = TRUE
                    AND reckoning_period_del_ind  = FALSE
                LIMIT 1
            )
        )
      GROUP BY m.code
    """
    df = db.querydatafromdatabase(sql, [], ["code", "pending_count"])
    pending_map = {row.code: row.pending_count > 0 for _, row in df.iterrows()}

    # 2) For each header-alert component, show if its metric_code has any pending
    out = []
    for id_obj in all_ids:
        code = id_obj["index"]
        if pending_map.get(code, False):
            out.append({"display": "block"})
        else:
            out.append({"display": "none"})
    return out

