import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, no_update, callback_context
from dash.dependencies import MATCH
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import base64
import os
from urllib.parse import urlparse, parse_qs
import flask
import json

# Highlight colors
highlight_colors = {
    'primary': "#0a4323",
    'secondary': "#7a0911",
    'accent': "#f8b237"
}

def generate_table(df):
    """Builds the HTML table, injecting per-row modals & alerts keyed by user_id."""
    columns = ['Full Name','Position','QAO Team','View','Edit','Mark as Done']
    widths = {'Full Name':'30%','Position':'20%','QAO Team':'20%',
              'View':'10%','Edit':'10%','Mark as Done':'10%'}

    header = [html.Th(col, style={'width':widths[col],'textAlign':'center'}) for col in columns]
    rows = []
    for i, row in df.iterrows():
        uid = row['ID']
        modal = dbc.Modal(
            [
                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary", close_button=False),
                dbc.ModalBody(
                    html.H5(id={'type':'done-modal-body','user_id':uid}),
                ),
                dbc.ModalFooter([
                    dbc.Button("Cancel", id={'type':'done-modal-cancel','user_id':uid}, n_clicks=0, color="secondary"),
                    dbc.Button("Confirm", id={'type':'done-modal-confirm','user_id':uid}, n_clicks=0, color="primary")
                ])
            ],
            id={'type':'done-confirm-modal','user_id':uid},
            is_open=False,
            backdrop="static",
            className="modal-success"
        )
        alert = dbc.Alert(
            id={'type':'done-alert','user_id':uid},
            is_open=False,
            duration=3000,
        )

        cells = []
        for col in columns:
            if col == 'Mark as Done':
                comp = dbc.Checklist(
                    id={'type':'done-checklist','user_id':uid},
                    options=[{"label":"","value":True}],
                    value=[True] if row['Mark as Done'] else [],
                    inline=True,
                    label_checked_style={"color":"green"},
                    input_checked_style={"backgroundColor":"lightgreen","borderColor":"green"},
                )
                cells.append(html.Td([comp, modal, alert], style={'width':widths[col],'textAlign':'center'}))
            else:
                cells.append(html.Td(row[col], style={'width':widths[col],'textAlign':'center'}))
        rows.append(html.Tr(cells))

    return html.Table(
        [html.Thead(html.Tr(header))] + [html.Tbody(rows)],
        className="table table-striped table-bordered table-hover table-sm",
        style={'width':'100%','tableLayout':'fixed'}
    )

layout = html.Div([
    dbc.Row([
        cm.sidebar,
        dbc.Col([
            html.H1("PEER EVALUATION RESPONSES"),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.Label("Name:", style={"fontSize":"18px","fontWeight":"bold"}), width=1),
                dbc.Col(dbc.Input(type='text', id='responses_eval_name_filter',
                                  placeholder='Search by Name'), width=4),
            ], className="align-items-center"),
            html.Div(id='responses_eval_list', style={'marginTop':20}),
        ], width=9, style={'marginLeft':15})
    ]),
    dbc.Row(dbc.Col(cm.generate_footer(), width=12))
])

# ✅ Static table-rendering callback (no wildcards)
@app.callback(
    Output('responses_eval_list', 'children'),
    [Input('url', 'pathname'),
     Input('responses_eval_name_filter', 'value')],
)
def render_table(pathname, searchterm):
    if pathname != '/peer_evaluation_responses':
        raise PreventUpdate

    # --- 1) Fetch raw columns ---
    sql = """
        SELECT u.user_id AS "ID",
               CONCAT(u.user_fname,' ',LEFT(u.user_mname,1),'. ',u.user_sname) AS "Full Name",
               q.qao_team_names AS "QAO Team",
               u.user_position AS "Position",
               COALESCE(es.summary_done,FALSE) AS "Done"
          FROM maindashboard.users u
     LEFT JOIN maindashboard.offices o ON u.user_office=o.office_id
     LEFT JOIN maindashboard.qao_teams q ON u.user_qao_team_id=q.qao_team_id
     LEFT JOIN director.evaluation_summaries es
            ON es.summary_evaluatee_id=u.user_id
           AND es.summary_evaluation_period=(
                SELECT period_id FROM director.evaluation_periods
                 WHERE active_status=TRUE AND period_del_ind=FALSE
           )
         WHERE o.office_name='Quality Assurance Office'
         AND u.user_id NOT IN(
                SELECT u.user_id 
                FROM maindashboard.users u
                WHERE u.user_office = 1
                AND
                u.user_qao_team_id = 1
            )
    """
    values = []
    if searchterm:
        sql += " AND (u.user_sname ILIKE %s OR u.user_fname ILIKE %s)"
        values = [f"%{searchterm}%"] * 2

    cols = ['ID','Full Name','QAO Team','Position','Done']
    df = db.querydatafromdatabase(sql, values, cols)

    # --- 2) Build View/Edit buttons ---
    view_buttons = []
    edit_buttons = []
    for uid in df['ID']:
        view_buttons.append(
            dbc.Button(
                "View",
                href=f"/peer_evaluation_responses/evaluation_summary?mode=view&id={uid}",
                size="sm", color="warning"
            )
        )
        edit_buttons.append(
            dbc.Button(
                "Edit",
                href=f"/peer_evaluation_responses/evaluation_summary?mode=edit&id={uid}",
                size="sm", color="danger"
            )
        )

    # --- 3) Inject into DataFrame ---
    df['View'] = view_buttons
    df['Edit'] = edit_buttons
    # Rename 'Done' to 'Mark as Done' so generate_table sees it
    df = df.rename(columns={'Done':'Mark as Done'})

    # --- 4) Re-order columns for generate_table ---
    df = df[['ID','Full Name','Position','QAO Team','View','Edit','Mark as Done']]

    # Pass to your generator (which ignores the ID column internally)
    return generate_table(df)

# ✅ Wildcard-only callback for toggling and alerts
@app.callback(
    [
        Output({'type':'done-checklist','user_id':MATCH}, "value"),
        Output({'type':'done-confirm-modal','user_id':MATCH}, "is_open"),
        Output({'type':'done-modal-body','user_id':MATCH}, "children"),
        Output({'type':'done-alert','user_id':MATCH}, "is_open"),
        Output({'type':'done-alert','user_id':MATCH}, "color"),
        Output({'type':'done-alert','user_id':MATCH}, "children"),
    ],
    [
        Input({'type':'done-checklist','user_id':MATCH}, "value"),
        Input({'type':'done-modal-confirm','user_id':MATCH}, "n_clicks"),
        Input({'type':'done-modal-cancel','user_id':MATCH}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def handle_toggle(checklist_val, n_confirm, n_cancel):
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    id_dict      = json.loads(triggered_id.replace("'", '"'))
    comp_type    = id_dict['type']
    user_id      = id_dict['user_id']

    # 1) User clicked the checklist
    if comp_type == 'done-checklist':
        df = db.querydatafromdatabase(
            """
            SELECT COUNT(*) AS cnt
              FROM director.evaluation_summaries
             WHERE summary_evaluatee_id=%s
               AND summary_evaluation_period = (
                   SELECT period_id
                     FROM director.evaluation_periods
                    WHERE active_status=TRUE 
                      AND period_del_ind=FALSE
               )
            """,
            [user_id], ['cnt']
        )
        if int(df['cnt'][0]) < 1:
            return [], False, "", True, "danger", "Please save evaluation first."

        body = ("Do you really want to mark this entry as done?"
                if checklist_val
                else "Do you really want to mark this entry as undone?")
        return dash.no_update, True, body, False, no_update, no_update

    # 2) User clicked “Cancel” in the modal
    elif comp_type == 'done-modal-cancel' and n_cancel:
        old_state = [True] if not checklist_val else []
        return old_state, False, "", False, no_update, no_update

    # 3) User clicked “Confirm” in the modal
    elif comp_type == 'done-modal-confirm' and n_confirm:
        new_done = True in checklist_val
        db.modifydatabase(
            """
            UPDATE director.evaluation_summaries
               SET summary_done = %s
             WHERE summary_evaluatee_id = %s
               AND summary_evaluation_period = (
                   SELECT period_id
                     FROM director.evaluation_periods
                    WHERE active_status = TRUE
                      AND period_del_ind = FALSE
               )
            """,
            [new_done, user_id]
        )
        final_val = [True] if new_done else []
        return final_val, False, "", True, "success", "Action Completed!"

    raise PreventUpdate
