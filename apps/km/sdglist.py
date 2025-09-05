import dash_bootstrap_components as dbc
from dash import dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import os
import json

from urllib.parse import urlparse, parse_qs

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

# Ensure upload directory exists
UPLOAD_DIRECTORY = r".\assets\database\km\sdg"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
# ─── 1. Define a mapping of SDG number → hex color ────────────────────────────
sdg_colors = {
    1: "#e5233d",  2: "#dda73a",  3: "#4ca146",  4: "#c7212f",
    5: "#ef402d",  6: "#27bfe6",  7: "#fbc412",  8: "#a31c44",
    9: "#f26a2e", 10: "#e01483", 11: "#f89d2a", 12: "#bf8d2c",
   13: "#407f46", 14: "#1f97d4", 15: "#59ba47", 16: "#136a9f",
   17: "#14496b",
}

# ─── 2. Build an initial list of Tabs; we'll override via callback ────────────
sdg_tabs = [
    dbc.Tab(label=f"SDG {i}", tab_id=f"tab-{i}", active_label_style={"color": sdg_colors[i]}, tabClassName="me-3")
    for i in range(1, 18)
]

layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        # Header
                        dbc.Row(
                            [dbc.Col(html.H1("SDG EVIDENCES SUBMISSION"), style={"marginRight": "auto"})],
                            style={"marginBottom": "-10px"},
                        ),
                        html.Hr(),
                        dbc.Alert(
                            [
                                html.H5("IMPORTANT NOTE WHEN SUBMITTING EVIDENCE:", className="alert-heading"),
                                html.P(
                                    'Please select the appropriate SDG Tab for your submission, then CLICK the "Add SDG Evidence" button.',
                                    className="mb-0",
                                ),
                            ],
                            color="warning",
                            className="mt-3 mb-4"
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    dbc.Tabs(
                                        sdg_tabs, id="sdg-tabs", active_tab="tab-1",
                                        className="mt-2", persistence=True, persistence_type="session",
                                    )
                                ),
                                dbc.CardBody(html.Div(id="sdg-card-content", className="p-4")),
                            ],
                            className="mt-3",
                        ),
                        html.Br(), html.Br(),
                    ],
                    width=9,
                    style={"marginLeft": "15px"},
                ),
            ]
        ),
        dbc.Row(dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0})),
    ]
)


# ─── A. Utility function to generate an HTML table with fixed column widths ──
def generate_sdg_table(df: pd.DataFrame) -> html.Table:
    # Now includes an Alert column
    columns = ["Submitted By", "Office", "View", "Edit", "Alert"]
    widths = {
        "Submitted By": "25%",
        "Office": "25%",
        "View": "20%",
        "Edit": "20%",
        "Alert": "10%",
    }

    # Header row
    header = [html.Th(col, style={"width": widths[col], "textAlign": "center"}) for col in columns]

    # Body rows
    rows = []
    for _, row in df.iterrows():
        cells = []
        for col in columns:
            cells.append(html.Td(row[col], style={"width": widths[col], "textAlign": "center"}))
        rows.append(html.Tr(cells))

    return html.Table(
        [html.Thead(html.Tr(header)), html.Tbody(rows)],
        className="table table-striped table-bordered table-hover table-sm",
        style={"width": "100%", "tableLayout": "fixed"},
    )


# ─── 3. Callback to populate CardBody (filters + table) based on active_tab ────
@app.callback(
    Output("sdg-card-content", "children"),
    [ Input("sdg-tabs", "active_tab") ],
    State("currentuserid", "data"),
)
def render_sdg_content(active_tab, currentuserid):
    if not active_tab:
        raise PreventUpdate

    # Which SDG?
    try:
        sdg_index = int(active_tab.split("-")[1])
    except:
        raise PreventUpdate

    # Filter row + Add button
    filter_row = dbc.Row(
        [dbc.Col(
            html.Div(
                html.A(
                    dbc.Button(f"➕ Add SDG Evidence {sdg_index}", color="primary", className="mb-3"),
                    href=f"/sdglist/sdg{sdg_index}submission?mode=add",
                ),
                style={"textAlign": "left"},
            ),
            width=12,
        )]
    )

    # Fetch submissions + whether any evidence needs attention (status_id 1 or 3)
    sql = """
      SELECT
        s.submission_id AS ID,
        s.submitter     AS "Submitted By",
        s.submitter_office AS "Office",
        bool_or(e.status_id IN (1,3)) AS needs_attention
      FROM kmteam.submission s
      JOIN kmteam.evidence   e ON e.submission_id = s.submission_id
      JOIN kmteam.metric     m ON m.metric_id     = e.metric_id
      WHERE m.sdg_number = %s
        AND s.submission_del_ind = FALSE
        AND s.submitter_id = %s
		AND s.reckoning_period IN (
                SELECT reckoning_period_id
                FROM kmteam.reckoning_periods
                WHERE active_status = TRUE
                    AND reckoning_period_del_ind  = FALSE
                LIMIT 1
            )    
      GROUP BY s.submission_id, s.submitter, s.submitter_office
      ORDER BY MAX(s.submitted_at) DESC
    """
    df = db.querydatafromdatabase(
        sql,
        [sdg_index, currentuserid],
        ["ID", "Submitted By", "Office", "needs_attention"],
    )

    if df.empty:
        no_records = html.Div(
            [html.P(f"No submissions found for SDG {sdg_index}.", className="text-muted"), html.Br()],
            className="text-center py-5",
        )
        return dbc.Container([filter_row, no_records], fluid=True, className="py-3")


    # View/Edit buttons
    df["View"] = df["ID"].apply(
        lambda sid: dbc.Button(
            "View",
            href=f"/sdglist/sdg{sdg_index}submission?mode=view&id={sid}",
            size="sm", color="warning",
        )
    )
    df["Edit"] = df["ID"].apply(
        lambda sid: dbc.Button(
            "Edit",
            href=f"/sdglist/sdg{sdg_index}submission?mode=edit&id={sid}",
            size="sm", color="danger",
        )
    )

    # Build Alert column
    def make_alert_cell(flag):
        return html.Div(
            dbc.Alert(
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                color="danger",
                className="d-flex align-items-center justify-content-center p-2 m-0",
            ),
            style={"display": "block"} if flag else {"display": "none"},
        )

    df["Alert"] = df["needs_attention"].apply(make_alert_cell)

    # Keep only our five columns
    df = df[["Submitted By", "Office", "View", "Edit", "Alert"]]

    # Render table
    table_html = generate_sdg_table(df)
    table_container = html.Div(
        table_html,
        style={"marginTop": "20px", "overflowX": "auto", "overflowY": "auto", "maxHeight": "600px"},
    )
    return dbc.Container([filter_row, table_container], fluid=True, className="py-3")


@app.callback(
    Output("sdg-tabs", "children"),
    Input("currentuserid", "data"),
)
def decorate_sdg_tabs(currentuserid):
    if not currentuserid:
        raise PreventUpdate

    tabs = []
    for i in range(1, 18):
        sql = """
            SELECT EXISTS (
              SELECT 1
                FROM kmteam.submission s
                JOIN kmteam.evidence   e ON e.submission_id = s.submission_id
                JOIN kmteam.metric     m ON m.metric_id     = e.metric_id
               WHERE m.sdg_number = %s
                 AND s.submitter_id = %s
                 AND s.submission_del_ind = FALSE
                 AND e.status_id IN (1,3)
                 AND s.reckoning_period IN (
                    SELECT reckoning_period_id
                    FROM kmteam.reckoning_periods
                    WHERE active_status = TRUE
                        AND reckoning_period_del_ind  = FALSE
                    LIMIT 1
                )    
            )
        """
        df = db.querydatafromdatabase(sql, [i, currentuserid], ["needs_attention"])
        needs = bool(df.at[0, "needs_attention"])

        # Use the heavy exclamation mark emoji (❗️) as a red badge
        badge_char = "❗️" if needs else ""
        label_str = f"SDG {i}{badge_char}"

        tabs.append(
            dbc.Tab(
                label=label_str,
                tab_id=f"tab-{i}",
                active_label_style={"color": sdg_colors[i]},
                tabClassName="me-3",
            )
        )

    return tabs
