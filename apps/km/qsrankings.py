import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db
from apps import commonmodules as cm

# ============ single-column sections ============
SINGLE_COL_SECTIONS = {
    'AVERAGE TUITION FEES',
    'UNIVERSITY METRICS',
    'UNIVERSITY DEGREES OFFERED'
}

# right under SINGLE_COL_SECTIONS
DATA_ANALYSIS_MAP = {
    # "Display name in table": [list of metric_code values to sum]
    "Total Undergraduate, Graduate, Juris Dr.": [
        "TOTAL_UNDERGRAD", "TOTAL_GRAD_POSTGRAD", "TOTAL_JURIS_DR"
    ],
    "Total Students (Undergrad, Graduate, Post Graduate, International, Exchange)": [
        "TOTAL_UNDERGRAD", "TOTAL_GRAD_POSTGRAD", "TOTAL_INTL", 
        "TOTAL_UG_EXCHANGE_INB", "TOTAL_UG_EXCHANGE_OUTB",
        "TOTAL_GRAD_EXCHANGE_INB", "TOTAL_GRAD_EXCHANGE_OUTB"
    ],
    "Male": [
        "UG_MALE", "GRAD_MALE", "INTL_MALE",
        "UG_EXC_MALE_INB", "UG_EXC_MALE_OUTB",
        "GRAD_EXC_MALE_INB", "GRAD_EXC_MALE_OUTB"
    ],
    "Female": [
        "UG_FEMALE", "GRAD_FEMALE", "INTL_FEMALE",
        "UG_EXC_FEMALE_INB", "UG_EXC_FEMALE_OUTB",
        "GRAD_EXC_FEMALE_INB", "GRAD_EXC_FEMALE_OUTB"
    ],
    "Total Undergraduate Students": ["TOTAL_UNDERGRAD"],
    "Undergraduate Students (Male)": ["UG_MALE"],
    "Undergraduate Students (Female)": ["UG_FEMALE"],
    "Total Graduate/Postgraduate Students": ["TOTAL_GRAD_POSTGRAD"],
    "Graduate/Postgraduate Students (Male)": ["GRAD_MALE"],
    "Graduate/Postgraduate Students (Female)": ["GRAD_FEMALE"],
    "Total Exchange Students": [
        "TOTAL_UG_EXCHANGE_INB", "TOTAL_UG_EXCHANGE_OUTB",
        "TOTAL_GRAD_EXCHANGE_INB","TOTAL_GRAD_EXCHANGE_OUTB"
    ],
    "Total Exchange Students (Inbound)": ["TOTAL_UG_EXCHANGE_INB", "TOTAL_GRAD_EXCHANGE_INB"],
    "Total Exchange Students (Outbound)": ["TOTAL_UG_EXCHANGE_OUTB","TOTAL_GRAD_EXCHANGE_OUTB"],
    "Total Undergraduate Exchange Students": ["TOTAL_UG_EXCHANGE_INB","TOTAL_UG_EXCHANGE_OUTB"],
    "Undergraduate Exchange Students (Male)": ["UG_EXC_MALE_INB","UG_EXC_MALE_OUTB"],
    "Undergraduate Exchange Students (Female)": ["UG_EXC_FEMALE_INB","UG_EXC_FEMALE_OUTB"],
    "Total Graduate/Postgraduate Exchange Students": ["TOTAL_GRAD_EXCHANGE_INB","TOTAL_GRAD_EXCHANGE_OUTB"],
    "Graduate/Postgraduate Exchange Students (Male)": ["GRAD_EXC_MALE_INB","GRAD_EXC_MALE_OUTB"],
    "Graduate/Postgraduate Exchange Students (Female)": ["GRAD_EXC_FEMALE_INB","GRAD_EXC_FEMALE_OUTB"],
    "Total International Students": ["TOTAL_INTL"],
    "Total International Students (Male)": ["INTL_MALE"],
    "Total International Students (Female)": ["INTL_FEMALE"],
}


# ============ 1. SQL Helpers ============
def insert_new_submission(submission_year, collection_year, reckoning_period, username):
    conn = db.getdblocation()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO kmteam.QSRankingSubmission
              (submission_year, collection_year, reckoning_period, created_by)
            VALUES (%s, %s, %s, %s)
            RETURNING submission_id
        """, [submission_year, collection_year, reckoning_period, username])
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    finally:
        cur.close()
        conn.close()

def delete_submission(sub_id):
    conn = db.getdblocation()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM kmteam.QSRankingSubmission WHERE submission_id = %s", [sub_id])
        conn.commit()
    finally:
        cur.close()
        conn.close()

def fetch_all_submissions():
    df = db.querydatafromdatabase("""
        SELECT submission_id, submission_year, collection_year, reckoning_period
          FROM kmteam.QSRankingSubmission
         ORDER BY submission_year DESC, collection_year DESC
    """, [], ["submission_id","submission_year","collection_year","reckoning_period"])
    return [
        {
            "label": f"SubYear {r['submission_year']} "
                     f"(Coll {r['collection_year']}, {r['reckoning_period']})",
            "value": r['submission_id']
        }
        for r in df.to_dict('records')
    ]

def fetch_metrics_for_submission(sub_id):
    return db.querydatafromdatabase("""
        SELECT m.metric_owner,
               m.metric_code,
               m.metric_display_name,
               m.section,
               COALESCE(v.part_time_count,0) AS pt,
               COALESCE(v.full_time_count,0) AS ft,
               m.display_order
          FROM kmteam.QSRankingMetric m
     LEFT JOIN kmteam.QSRankingValue v
            ON m.metric_id=v.metric_id AND v.submission_id=%s
         WHERE m.active_ind=TRUE
      ORDER BY m.display_order
    """, [sub_id],
    ["metric_owner","metric_code","metric_display_name","section","pt","ft","display_order"]
    )

def fetch_data_analysis(sub_id):
    """
    Fetch _all_ metric values for this submission, then
    compute each roll‑up defined in DATA_ANALYSIS_MAP.
    Returns a list of dicts: [{
        "metric_display_name": "...",
        "section": "DATA ANALYSIS SECTION (DO NOT EDIT)",
        "total": 1234
    }, ...]
    """
    # 1) grab everything
    sql = """
    SELECT
      m.metric_code,
      COALESCE(v.part_time_count,0) AS pt,
      COALESCE(v.full_time_count,0) AS ft
    FROM kmteam.QSRankingMetric m
    LEFT JOIN kmteam.QSRankingValue v
      ON m.metric_id = v.metric_id
     AND v.submission_id = %s
    WHERE m.active_ind = TRUE
    """
    df = db.querydatafromdatabase(sql, [sub_id], ["metric_code","pt","ft"])

    # 2) build a lookup: code → pt+ft
    totals = {row["metric_code"]: row["pt"] + row["ft"]
              for row in df.to_dict("records")}

    # 3) for each of your analysis items, sum the codes
    results = []
    for display_name, codes in DATA_ANALYSIS_MAP.items():
        val = sum(totals.get(c, 0) for c in codes)
        results.append({
            "metric_display_name": display_name,
            "section": "DATA ANALYSIS SECTION (DO NOT EDIT)",
            "total": val
        })
    return results


# ============ 2. Layout ============
layout = html.Div([
    dcc.Store(id="qs_submission_refresh", data=0),
    dbc.Row([
        cm.sidebar,
        dbc.Col([
            html.H1("QS Rankings"), html.Hr(),

            # Create
            html.H5("Create New Submission"),
            dbc.Row([
                dbc.Col([dbc.Label("Submission Year"),
                         dcc.Input(id="qs_submission_year", type="number", min=2000, max=2100,
                                   placeholder="2025", style={"width":"100%"})],
                        width=3),
                dbc.Col([dbc.Label("Collection Year"),
                         dcc.Input(id="qs_collection_year", type="number", min=2000, max=2100,
                                   placeholder="2024", style={"width":"100%"})],
                        width=3),
                dbc.Col([dbc.Label("Reckoning Period"),
                         dcc.Input(id="qs_reckoning_period", type="text",
                                   placeholder="As of 1st Sem AY 2023–2024",
                                   style={"width":"100%"})],
                        width=6),
            ], className="mb-3"),
            dbc.Button("Create QS Submission", id="qs_create_submit_button", color="primary"),
            html.Div(id="qs_create_feedback", style={"marginTop":"10px"}),
            html.Hr(),

            # View / Delete
            html.H5("View One Submission"),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id="km_select_submission",
                                     placeholder="Pick a submission",
                                     style={"width":"100%"}),
                        width=9),
                dbc.Col(dbc.Button("Delete QS Submission",
                                   id="qs_delete_button", color="danger",
                                   style={"width":"100%"}),
                        width=3),
            ], className="mb-2"),
            html.Div(id="qs_delete_feedback", style={"marginBottom":"10px","color":"red"}),
            html.Div(id="km_metrics_table", style={"marginTop":"10px"}),
            html.Hr(),
            html.H5("Data Analysis Section"),
            dbc.Button("Show Data Analysis", id="qs_data_button", color="info"),
            html.Div(id="qs_data_output", style={"marginTop":"1rem"}),
            html.Hr(),


            # Compare
            html.H5("Compare All Submissions"),
            dbc.Button("Load All Submissions", id="qs_compare_button", color="secondary"),
            html.Div(id="qs_compare_output", style={"marginTop":"20px"}),
        ], width=9)
    ])
])

# ============ 3. Callbacks ============

# Populate the dropdown
@app.callback(
    Output("km_select_submission","options"),
    [Input("url","pathname"), Input("qs_submission_refresh","data")]
)
def _populate(pathname, refresh):
    if pathname.rstrip('/') != '/qs_rankings':
        raise PreventUpdate
    return fetch_all_submissions()

# Create / Delete
@app.callback(
    [Output("qs_create_feedback","children"), Output("qs_create_feedback","style"),
     Output("qs_delete_feedback","children"), Output("qs_delete_feedback","style"),
     Output("qs_submission_refresh","data"),  Output("km_select_submission","value")],
    [Input("qs_create_submit_button","n_clicks"), Input("qs_delete_button","n_clicks")],
    [State("qs_submission_year","value"), State("qs_collection_year","value"),
     State("qs_reckoning_period","value"), State("km_select_submission","value")],
    prevent_initial_call=True
)
def _create_delete(c_clicks, d_clicks, sy, cy, rp, sel):
    ctx = callback_context.triggered[0]['prop_id'].split('.')[0]
    cm_msg = cm_style = dm_msg = dm_style = dash.no_update
    ref = val = dash.no_update

    if ctx == "qs_create_submit_button":
        missing = [f for f,name in [(sy,"Submission Year"),(cy,"Collection Year"),(rp,"Reckoning Period")] if not f]
        if missing:
            cm_msg, cm_style = f"Missing: {', '.join(missing)}", {"color":"red"}
        else:
            sid = insert_new_submission(sy,cy,rp,"km_admin")
            cm_msg, cm_style, ref, val = f"Created submission for {sy}.", {"color":"green"}, c_clicks, None

    elif ctx == "qs_delete_button":
        if not sel:
            dm_msg, dm_style = "No submission selected.", {"color":"red"}
        else:
            # fetch the year for label
            year = db.querydatafromdatabase(
                "SELECT submission_year FROM kmteam.QSRankingSubmission WHERE submission_id=%s",
                [sel], ["submission_year"]
            ).iloc[0]["submission_year"]
            delete_submission(sel)
            dm_msg, dm_style, ref, val = f"Deleted submission for {year}.", {"color":"green"}, d_clicks, None

    else:
        raise PreventUpdate

    return [cm_msg, cm_style, dm_msg, dm_style, ref, val]

# View One Submission
@app.callback(
    Output("km_metrics_table","children"),
    Input("km_select_submission","value")
)
def show_one(sub_id):
    if not sub_id:
        return html.Div()
    df = fetch_metrics_for_submission(sub_id)
    if df.empty:
        return html.Div("No data available.")

    header = html.Thead(html.Tr([
        html.Th("Metric Name"), html.Th("Part Time"), html.Th("Full Time")
    ]))

    rows = []
    last_sec = None

    for _,r in df.iterrows():
        if r.section != last_sec:
            rows.append(html.Tr(html.Td(
                r.section, colSpan=3,
                style={"backgroundColor":"#f0f0f0","fontWeight":"bold","textAlign":"left"}
            )))
            last_sec = r.section

        if r.section in SINGLE_COL_SECTIONS:
            total = r.pt + r.ft
            rows.append(html.Tr([
                html.Td(r.metric_display_name),
                html.Td(str(total), colSpan=2, style={"textAlign":"center"})
            ]))
        else:
            rows.append(html.Tr([
                html.Td(r.metric_display_name),
                html.Td(str(r.pt), style={"textAlign":"center"}),
                html.Td(str(r.ft), style={"textAlign":"center"})
            ]))

    return dbc.Table([header, html.Tbody(rows)], bordered=True, striped=True, size="sm")


@app.callback(
    Output("qs_compare_output", "children"),
    Input("qs_compare_button", "n_clicks"),
    prevent_initial_call=True
)
def compare_all(n_clicks):
    if not n_clicks:
        raise PreventUpdate

    # 1) Fetch all metrics + pt/ft + section + owner + display_order
    sql = """
        SELECT
            s.submission_year,
            s.collection_year,
            s.reckoning_period,
            m.section,
            m.metric_owner,
            m.metric_display_name,
            COALESCE(v.part_time_count,0) AS pt,
            COALESCE(v.full_time_count,0) AS ft,
            m.display_order
        FROM kmteam.QSRankingSubmission s
        LEFT JOIN kmteam.QSRankingValue v 
          ON s.submission_id = v.submission_id
        LEFT JOIN kmteam.QSRankingMetric m
          ON m.metric_id = v.metric_id
        WHERE m.active_ind = TRUE
        ORDER BY s.submission_year DESC, m.display_order
    """
    df = db.querydatafromdatabase(
        sql, [], 
        [
            "submission_year","collection_year","reckoning_period",
            "section","metric_owner","metric_display_name","pt","ft","display_order"
        ]
    )
    if df.empty:
        return html.Div("No data available.")

    # 2) Identify years (descending)
    meta = (
        df[["submission_year","collection_year","reckoning_period"]]
        .drop_duplicates("submission_year")
        .sort_values("submission_year", ascending=False)
    )
    years = list(meta["submission_year"])
    year_to_coll = {r.submission_year: r.collection_year for _, r in meta.iterrows()}
    year_to_reck = {r.submission_year: r.reckoning_period for _, r in meta.iterrows()}

    # 3a) Pivot to multi‑index (pt/ft per year), keep display_order in the index
    pivoted = df.pivot_table(
        index=["section","metric_owner","metric_display_name","display_order"],
        columns="submission_year",
        values=["pt","ft"],
        aggfunc="first",
        fill_value=0
    )

    # 3b) Flatten & sort by display_order
    pivot_df = pivoted.reset_index().sort_values("display_order")

    # 4) Build header rows with inter‑year % change
    hr1 = [
        html.Th("Owner",         rowSpan=4, style={"textAlign":"left","verticalAlign":"middle"}),
        html.Th("Metric Name",   rowSpan=4, style={"textAlign":"left","verticalAlign":"middle"})
    ]
    for i, yr in enumerate(years):
        hr1.append(html.Th(f"For {yr} Submission", colSpan=2, style={"textAlign":"center"}))
        if i < len(years)-1:
            next_year = years[i+1]
            hr1.append(html.Th(f"% Δ {next_year}→{yr}", rowSpan=4,
                               style={"textAlign":"center","verticalAlign":"middle"}))

    hr2 = [html.Th(), html.Th("Collection Year")]
    for i, yr in enumerate(years):
        hr2.extend([ html.Th(year_to_coll[yr]), html.Th("Total") ])
        if i < len(years)-1:
            hr2.append(html.Th())

    hr3 = [html.Th(), html.Th("Reckoning Period")]
    for i, yr in enumerate(years):
        hr3.extend([ html.Th(year_to_reck[yr], colSpan=2) ])
        if i < len(years)-1:
            hr3.append(html.Th())

    hr4 = [html.Th(), html.Th("")]
    for i in range(len(years)):
        hr4.extend([ html.Th("Part Time"), html.Th("Full Time") ])
        if i < len(years)-1:
            hr4.append(html.Th(""))

    # 5) Build body rows, grouping by section (in the order they appear)
    total_cols = 2 + 2*len(years) + (len(years)-1)
    body = []
    for section_name, grp in pivot_df.groupby("section", sort=False):
        # Section header
        body.append(html.Tr(html.Td(
            section_name, colSpan=total_cols,
            style={"backgroundColor":"#f0f0f0","fontWeight":"bold","textAlign":"left"}
        )))
        # Metric rows
        for _, row in grp.iterrows():
            owner = row["metric_owner"]
            key   = row["metric_display_name"]
            display_order = row["display_order"]

            cells = [ html.Td(owner), html.Td(key) ]

            for i, yr in enumerate(years):
                pt = row[("pt", yr)]
                ft = row[("ft", yr)]
                cells.extend([
                    html.Td(str(pt), style={"textAlign":"center"}),
                    html.Td(str(ft), style={"textAlign":"center"})
                ])
                if i < len(years)-1:
                    next_yr = years[i+1]
                    tot_curr = pt + ft
                    tot_prev = row[("pt", next_yr)] + row[("ft", next_yr)]
                    pct = f"{(tot_curr - tot_prev)/tot_prev*100:.2f}%" if tot_prev else ""
                    cells.append(html.Td(pct, style={"textAlign":"center"}))

            body.append(html.Tr(cells))

    # 6) Assemble the final table
    table = dbc.Table(
        [
            html.Thead(html.Tr(hr1)),
            html.Thead(html.Tr(hr2)),
            html.Thead(html.Tr(hr3)),
            html.Thead(html.Tr(hr4)),
            html.Tbody(body),
        ],
        bordered=True, striped=True, size="sm",
        style={"overflowX":"auto", "minWidth": f"{200 + 180*len(years)}px"}
    )

    return html.Div(table, style={"overflowX":"auto"})

@app.callback(
    Output("qs_data_output", "children"),
    Input("qs_data_button", "n_clicks"),
    State("km_select_submission", "value"),
    prevent_initial_call=True
)
def show_data_analysis(n_clicks, sub_id):
    if not n_clicks or not sub_id:
        raise PreventUpdate

    rows = fetch_data_analysis(sub_id)
    if not rows:
        return html.Div("No data available.")

    # build a simple two‑column table
    header = html.Thead(html.Tr([
        html.Th("Metric Name"), html.Th("Total")
    ]))
    body = html.Tbody([
        html.Tr([
            html.Td(r["metric_display_name"]),
            html.Td(str(r["total"]), style={"textAlign":"center"})
        ])
        for r in rows
    ])
    return dbc.Table([header, body],
                     bordered=True, size="sm", striped=True)

