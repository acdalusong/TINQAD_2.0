
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import time

from app import app
from apps import dbconnect as db
from apps import commonmodules as cm

# =============================================================================
# 1. TOTAL_CHILD_MAP (used when recomputing totals)
#    — Must match exactly the metric_code values you inserted.
# =============================================================================
TOTAL_CHILD_MAP = {
    # — FACULTY DATA —
    "TOTAL_FACULTY":        ["FACULTY_MALE",        "FACULTY_FEMALE"],
    "TOTAL_INTL_FAC_STAFF": ["INTL_FAC_INBOUND",    "INTL_FAC_OUTBOUND"],
    "TOTAL_FAC_PHDD":       ["FAC_PHDD_MALE",       "FAC_PHDD_FEMALE"],

    # — UNDERGRAD / GRADUATE —
    "TOTAL_UNDERGRAD":      ["UG_MALE",             "UG_FEMALE"],
    "TOTAL_GRAD_POSTGRAD":  ["GRAD_MALE",           "GRAD_FEMALE"],

    # — EXCHANGE STUDENTS —
    "TOTAL_UG_EXCHANGE_INB":  ["UG_EXC_MALE_INB",   "UG_EXC_FEMALE_INB"],
    "TOTAL_UG_EXCHANGE_OUTB": ["UG_EXC_MALE_OUTB",  "UG_EXC_FEMALE_OUTB"],
    "TOTAL_GRAD_EXCHANGE_INB":  ["GRAD_EXC_MALE_INB",    "GRAD_EXC_FEMALE_INB"],
    "TOTAL_GRAD_EXCHANGE_OUTB": ["GRAD_EXC_MALE_OUTB",   "GRAD_EXC_FEMALE_OUTB"],

    # — INTERNATIONAL STUDENTS —
    "TOTAL_INTL":           ["INTL_MALE",    "INTL_FEMALE"],

    # — STUDENT CLASSIFICATION —
    "TOTAL_GRADUATING":     ["GRADUATING_MALE",   "GRADUATING_FEMALE"],
    "TOTAL_FIRSTGEN":       ["FIRSTGEN_MALE",     "FIRSTGEN_FEMALE"],
    "TOTAL_FIRSTYEAR":      ["FIRSTYEAR_MALE",    "FIRSTYEAR_FEMALE"],
    "TOTAL_FIRSTYEAR_4YR":  ["FIRSTYEAR_4YR_COUNT"],
    "TOTAL_FIRSTYEAR_5YR":  ["FIRSTYEAR_5YR_COUNT"],
    "SECONDYEAR_REENROLL":  ["SECONDYEAR_MALE",   "SECONDYEAR_FEMALE"],
    "TOTAL_GRADUATES_REF":  ["GRADUATES_4YR_REF", "GRADUATES_5YR_REF"],
    # PG_PROGRESS_* are stand-alone:
    "PG_PROGRESS_4YR":      [],
    "PG_PROGRESS_5YR":      [],
    "PG_PROGRESS_2YR":      [],

    # — STUDENT PROGRESS OUTCOMES METRICS —
    "RETENTION_RATE":       [],
    "COMPLETION_4YR_RATE":  [],
    "COMPLETION_5YR_RATE":  [],
    "COMPLETION_RATE":      [],
    "CONTINUATION_RATE":    [],

    # — SCHOLARSHIPS & ENROLLMENT —
    "TOTAL_SCHOLARSHIPS":   ["COUNT_SCHOLARSHIPS", "SCHOLARSHIP_51_100", "SCHOLARSHIP_LT50"],

    # — UNIVERSITY METRICS — (all stand-alone)
    "AVG_TUITION_UG_DOM":       [],
    "AVG_TUITION_UG_INTL":      [],
    "AVG_TUITION_GRAD_DOM":     [],
    "AVG_TUITION_GRAD_INTL":    [],
    "AVG_FEES_OVERALL_DOM":     [],
    "AVG_FEES_OVERALL_INTL":    [],
    "NUM_DEG_UG":               [],
    "NUM_DEG_POSTGRAD":         [],
    "NUM_DEG_UG_ONLINE":        [],
    "NUM_DEG_POSTGRAD_ONLINE":  [],
    "NUM_NONDEG_COURSES_ONLINE":[]
}

# =============================================================================
# 2. SINGLE-COLUMN SECTIONS
# =============================================================================
SINGLE_COL_SECTIONS = {
    'AVERAGE TUITION FEES',
    'UNIVERSITY METRICS',
    'UNIVERSITY DEGREES OFFERED'
}

# =============================================================================
# 3. Helper Functions
# =============================================================================
def fetch_distinct_owners():
    """Returns a list of all distinct metric_owner values."""
    sql = """
        SELECT DISTINCT metric_owner
        FROM kmteam.QSRankingMetric
        WHERE active_ind = TRUE
        ORDER BY metric_owner
    """
    df = db.querydatafromdatabase(sql, [], ["metric_owner"])
    return [r["metric_owner"] for r in df.to_dict("records")]

def fetch_all_submissions():
    """Returns dropdown options for all submissions."""
    sql = """
        SELECT submission_id, submission_year, collection_year, reckoning_period
        FROM kmteam.QSRankingSubmission
        ORDER BY submission_year DESC, collection_year DESC
    """
    df = db.querydatafromdatabase(sql, [], ["submission_id","submission_year","collection_year","reckoning_period"])
    options = []
    for r in df.to_dict("records"):
        label = f"SubYear {r['submission_year']} (Coll {r['collection_year']}, {r['reckoning_period']})"
        options.append({"label": label, "value": r["submission_id"]})
    return options

def fetch_owner_metrics_for_submission(owner_code, submission_id):
    """Fetch metrics (with section) plus existing PT/FT for an office & submission."""
    sql = """
        SELECT
            m.metric_id,
            m.metric_code,
            m.metric_display_name,
            m.section,
            COALESCE(v.part_time_count, 0) AS existing_pt,
            COALESCE(v.full_time_count, 0) AS existing_ft
        FROM kmteam.QSRankingMetric m
        LEFT JOIN kmteam.QSRankingValue v
          ON m.metric_id = v.metric_id
         AND v.submission_id = %s
        WHERE m.active_ind = TRUE
          AND m.metric_owner = %s
        ORDER BY m.section, m.display_order
    """
    df = db.querydatafromdatabase(sql, [submission_id, owner_code],
        ["metric_id","metric_code","metric_display_name","section","existing_pt","existing_ft"])
    return df.to_dict("records")

def upsert_metric_value(submission_id, metric_id, part_time, full_time):
    """Insert or update a single metric value."""
    sql = """
        INSERT INTO kmteam.QSRankingValue
            (submission_id, metric_id, part_time_count, full_time_count)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (submission_id, metric_id) DO UPDATE
          SET part_time_count = EXCLUDED.part_time_count,
              full_time_count = EXCLUDED.full_time_count
    """
    db.modifydatabase(sql, [submission_id, metric_id, part_time, full_time])

def ensure_total_row_exists(submission_id, total_metric_code):
    """Ensure a TOTAL_* metric row exists (initialized to zero)."""
    sql = """
        INSERT INTO kmteam.QSRankingValue
            (submission_id, metric_id, part_time_count, full_time_count)
        VALUES (
            %s,
            (SELECT metric_id FROM kmteam.QSRankingMetric WHERE metric_code = %s),
            0, 0
        )
        ON CONFLICT (submission_id, metric_id) DO NOTHING
    """
    db.modifydatabase(sql, [submission_id, total_metric_code])

def compute_and_update_total(submission_id, total_metric_code, child_metric_codes):
    """Sum child metrics for this submission and update the TOTAL_* row."""
    ensure_total_row_exists(submission_id, total_metric_code)
    sql = """
        UPDATE kmteam.QSRankingValue AS tgt
        SET
          part_time_count = COALESCE((
            SELECT SUM(v.part_time_count)
              FROM kmteam.QSRankingValue v
              JOIN kmteam.QSRankingMetric m ON v.metric_id = m.metric_id
             WHERE v.submission_id = %s
               AND m.metric_code = ANY(%s)
          ), 0),
          full_time_count = COALESCE((
            SELECT SUM(v.full_time_count)
              FROM kmteam.QSRankingValue v
              JOIN kmteam.QSRankingMetric m ON v.metric_id = m.metric_id
             WHERE v.submission_id = %s
               AND m.metric_code = ANY(%s)
          ), 0)
        WHERE tgt.submission_id = %s
          AND tgt.metric_id = (
            SELECT metric_id FROM kmteam.QSRankingMetric WHERE metric_code = %s
          )
    """
    params = [
        submission_id, child_metric_codes,
        submission_id, child_metric_codes,
        submission_id, total_metric_code
    ]
    db.modifydatabase(sql, params)

# ============ 4. Layout ============
layout = html.Div([
    dbc.Row([
        cm.sidebar,
        dbc.Col([
            html.H1("QS Rankings – Provider Data Entry"),
            html.Hr(),

            # 4.1 Office Selector
            dbc.Row([
                dbc.Col([
                    dbc.Label("Select Your Office / Group", html_for="provider_office"),
                    dcc.Dropdown(
                        id="provider_office",
                        options=[{"label": o, "value": o} for o in fetch_distinct_owners()],
                        placeholder="Choose your Office (e.g. HRDO, OIL, OUR, CRS, KMP)",
                        style={"width": "100%"}
                    )
                ], width=4),
                dbc.Col([
                    dbc.Label("Enter Your Name", html_for="provider_submitter_name"),
                    dcc.Input(
                        id="provider_submitter_name",
                        type="text",
                        placeholder="Type your full name",
                        style={"width": "100%"}
                    )
                ], width=4),

                html.Div(id="submitter_info", className="text-muted mb-3"),


                # 4.2 Submission Selector
                dbc.Col([
                    dbc.Label("Select Submission", html_for="provider_submission"),
                    dcc.Dropdown(
                        id="provider_submission",
                        options=[],
                        placeholder="Pick an existing Submission",
                        style={"width": "100%"}
                    )
                ], width=8),
            ], className="mb-4"),

            # 4.3 Editable Metrics Table
            html.H5("Your Metrics (Part‑Time / Full‑Time)"),
            html.Div(
                id="provider_metrics_table_container",
                style={"overflowX": "auto", "maxHeight": "400px", "overflowY": "scroll"}
            ),

            html.Br(),
            # 4.4 Save Button & Feedback
            dbc.Button("Save My Section", id="provider_submit_button", color="primary"),
            html.Div(id="provider_submit_feedback", style={"marginTop": "15px"}),

            html.Br(), html.Hr(),
            # 4.5 Already‑Entered Data Summary
            html.H5("Already‑Entered Values for This Submission"),
            html.Div(
                id="provider_existing_data",
                style={"overflowX": "auto", "maxHeight": "300px", "overflowY": "scroll"}
            ),

            # Hidden store for table refresh
            dcc.Store(id="prov_save_trigger", data=0, storage_type="memory"),

        ], width=9, style={"marginLeft": "15px"})
    ]),

    # Footer
    html.Br(), html.Br(),
    dbc.Row([dbc.Col(cm.generate_footer(), width={"size": 12})])
])

# ============ 5. Callbacks ============

# 5.1 Populate Editable Table
@app.callback(
    Output("provider_metrics_table_container", "children"),
    [
      Input("provider_office", "value"),
      Input("provider_submission", "value"),
      Input("prov_save_trigger", "data")
    ]
)
def populate_provider_table(selected_office, selected_submission, save_trigger):
    if not selected_office or not selected_submission:
        return html.Div()

    records = fetch_owner_metrics_for_submission(selected_office, selected_submission)
    if not records:
        return html.Div(f"No metrics assigned to office '{selected_office}'.")

    header = html.Thead(html.Tr([
        html.Th("Metric Name"), html.Th("Part-Time"), html.Th("Full-Time")
    ]))
    rows = []
    last_section = None

    for r in records:
        if r["section"] != last_section:
            rows.append(html.Tr(html.Td(r["section"], colSpan=3,
                style={"fontWeight":"bold","backgroundColor":"#f0f0f0","textAlign":"left"})))
            last_section = r["section"]

        name = r["metric_display_name"]
        pt   = r["existing_pt"] or 0
        ft   = r["existing_ft"] or 0
        mid  = r["metric_id"]

        if r["section"] in SINGLE_COL_SECTIONS:
            total_input = dcc.Input(
                id={"type":"prov_total_input","index":mid},
                type="number", min=0, value=pt+ft, style={"width":"100px"}
            )
            rows.append(html.Tr([
                html.Td(name),
                html.Td(total_input, colSpan=2, style={"textAlign":"center"})
            ]))
        else:
            pt_input = dcc.Input(
                id={"type":"prov_pt_input","index":mid},
                type="number", min=0, value=pt, style={"width":"100px"}
            )
            ft_input = dcc.Input(
                id={"type":"prov_ft_input","index":mid},
                type="number", min=0, value=ft, style={"width":"100px"}
            )
            rows.append(html.Tr([
                html.Td(name),
                html.Td(pt_input, style={"textAlign":"center"}),
                html.Td(ft_input, style={"textAlign":"center"})
            ]))

    return dbc.Table([header, html.Tbody(rows)], bordered=True, striped=True, size="sm")

# 5.2 Save Provider Data & Recompute Totals
@app.callback(
    [
      Output("provider_submit_feedback","children"),
      Output("provider_submit_feedback","style"),
      Output("prov_save_trigger","data")
    ],
    Input("provider_submit_button","n_clicks"),
    [
      State("provider_office","value"),
      State("provider_submission","value"),
      State({"type":"prov_pt_input","index":dash.dependencies.ALL},"value"),
      State({"type":"prov_ft_input","index":dash.dependencies.ALL},"value"),
      State({"type":"prov_total_input","index":dash.dependencies.ALL},"value"),
      State({"type":"prov_pt_input","index":dash.dependencies.ALL},"id"),
      State({"type":"prov_total_input","index":dash.dependencies.ALL},"id"),
      State("prov_save_trigger","data"),
      State("provider_submitter_name", "value"),
    ]
)
def handle_provider_submission(n_clicks, office, submission_id,
                               pt_values, ft_values, total_values,
                               pt_ids, total_ids, prev_trigger, submitter_name):
    if not n_clicks:
        raise PreventUpdate
    if not office:
        return ["Error: Please select your office.", {"color":"red"}, prev_trigger]
    if not submission_id:
        return ["Error: Please select a Submission.", {"color":"red"}, prev_trigger]
    
        # Save submitter info (if not already recorded)
    db.modifydatabase(
        """
        UPDATE kmteam.QSRankingSubmission
        SET submitter_name = %s,
            submitter_office = %s
        WHERE submission_id = %s
        """,
        [submitter_name or "Anonymous", office, submission_id]
    )


    # two‑col metrics
    for idx, id_obj in enumerate(pt_ids):
        mid = id_obj["index"]
        try:
            upsert_metric_value(submission_id, mid, pt_values[idx] or 0, ft_values[idx] or 0)
        except Exception as e:
            print(f"Error upserting {mid}: {e}")

    # single‑col metrics
    for idx, id_obj in enumerate(total_ids):
        mid = id_obj["index"]
        try:
            upsert_metric_value(submission_id, mid, 0, total_values[idx] or 0)
        except Exception as e:
            print(f"Error upserting total {mid}: {e}")

    # recompute totals
    for total_code, child_codes in TOTAL_CHILD_MAP.items():
        if child_codes:
            try:
                compute_and_update_total(submission_id, total_code, child_codes)
            except Exception as e:
                print(f"Error computing total {total_code}: {e}")

    return [f"Saved data for office '{office}'.", {"color":"green"}, int(time.time()*1000)]

# 5.3 Show Already‑Entered Data (read‑only)
@app.callback(
    Output("provider_existing_data","children"),
    [
      Input("provider_office","value"),
      Input("provider_submission","value"),
      Input("prov_save_trigger","data")
    ]
)
def show_provider_existing_data(office, submission_id, save_trigger):
    if not office or not submission_id:
        return html.Div()

    records = fetch_owner_metrics_for_submission(office, submission_id)
    if not records:
        return html.Div("No data yet.")

    header = html.Thead(html.Tr([
        html.Th("Metric Name"), html.Th("Part‑Time Count"), html.Th("Full‑Time Count")
    ]))
    rows = []
    last_section = None

    for r in records:
        if r["section"] != last_section:
            rows.append(html.Tr(html.Td(r["section"], colSpan=3,
                style={"fontWeight":"bold","backgroundColor":"#f0f0f0","textAlign":"left"})))
            last_section = r["section"]

        pt = r["existing_pt"] or 0
        ft = r["existing_ft"] or 0
        name = r["metric_display_name"]

        if r["section"] in SINGLE_COL_SECTIONS:
            total = pt + ft
            rows.append(html.Tr([
                html.Td(name),
                html.Td(str(total), colSpan=2, style={"textAlign":"center"})
            ]))
        else:
            rows.append(html.Tr([
                html.Td(name),
                html.Td(str(pt), style={"textAlign":"center"}),
                html.Td(str(ft), style={"textAlign":"center"})
            ]))

    return dbc.Table([header, html.Tbody(rows)], bordered=True, size="sm")

# 5.4 Repopulate Submission Dropdown
@app.callback(
    Output("provider_submission","options"),
    Input("url","pathname")
)
def repopulate_provider_submission_dropdown(pathname):
    if pathname != "/qs_rankings_provider":
        raise PreventUpdate
    return fetch_all_submissions()

@app.callback(
    Output("submitter_info", "children"),
    Input("provider_submission", "value")
)
def show_submitter_info(submission_id):
    if not submission_id:
        raise PreventUpdate

    sql = """
        SELECT submitter_name, submitter_office
        FROM kmteam.QSRankingSubmission
        WHERE submission_id = %s
    """
    df = db.querydatafromdatabase(sql, [submission_id], ["submitter_name", "submitter_office"])
    if df.empty:
        return ""

    name = df.at[0, "submitter_name"] or "N/A"
    office = df.at[0, "submitter_office"] or "N/A"
    return f"📝 Submitted by: {name} ({office})"
