import io
from weasyprint import HTML
from flask import render_template
from apps import dbconnect as db  
from urllib.parse import urlparse, parse_qs

def generate_pdf_bytes(evaluatee_id):
    # — 1) BASIC INFO & REVIEWERS —
    sql_basic = """
        SELECT DISTINCT 
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS full_name,
            to_char(lower(period_details), 'Mon DD, YYYY') ||
            ' to ' ||
            to_char(upper(period_details) - INTERVAL '1 day', 'Mon DD, YYYY')
            AS evaluation_period
        FROM director.peer_evaluations pe
        JOIN maindashboard.users u ON pe.evaluator_id = u.user_id
        JOIN director.evaluation_periods ep ON ep.period_id = pe.evaluation_period_id 
        WHERE pe.evaluatee_id = %s
          AND pe.peer_eval_delete_ind = FALSE
          AND pe.evaluation_period_id = (
            SELECT period_id
            FROM director.evaluation_periods
            WHERE active_status = TRUE
              AND period_del_ind = FALSE
          );
    """
    df_basic = db.querydatafromdatabase(sql_basic, [int(evaluatee_id)], ['full_name','evaluation_period'])
    if df_basic.empty:
        evaluation_period = ""
        reviewers_text = "No peer review evaluations found."
    else:
        evaluation_period = df_basic.at[0, 'evaluation_period']
        reviewers_text = ", ".join(df_basic['full_name'].unique())

    # — 2) SCORES & WEIGHTED AVERAGES —
    sql_scores = """
        SELECT 
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS full_name,
            ed.rubric_id,
            ed.rating_value, 
            COUNT(*) AS rating_count
        FROM maindashboard.users u
        LEFT JOIN director.peer_evaluations pe ON u.user_id = pe.evaluatee_id
        LEFT JOIN director.evaluation_details ed ON pe.evaluation_id = ed.evaluation_id
        WHERE pe.evaluatee_id = %s
          AND pe.peer_eval_delete_ind = FALSE
          AND pe.evaluation_period_id = (
            SELECT period_id
            FROM director.evaluation_periods
            WHERE active_status = TRUE
              AND period_del_ind = FALSE
          )
        GROUP BY full_name, ed.rubric_id, ed.rating_value;
    """
    cols = ['full_name', 'rubric_id', 'rating_value', 'rating_count']
    df_scores = db.querydatafromdatabase(sql_scores, [int(evaluatee_id)], cols)
    # init

    if df_scores.empty:
        evaluatee_name = ""
    else:
        evaluatee_name = df_scores.at[0, 'full_name']

    result = {r: {1:0,2:0,3:0,4:0,'weighted':0} for r in range(1,7)}
    for _, row in df_scores.iterrows():
        rid, val, cnt = int(row['rubric_id']), int(row['rating_value']), int(row['rating_count'])
        result[rid][val] = cnt
    # compute weighted
    for r in result:
        counts = result[r]
        tot = counts[1]+counts[2]+counts[3]+counts[4]
        result[r]['weighted'] = round((1*counts[1] + 2*counts[2] + 3*counts[3] + 4*counts[4]) / tot, 2) if tot else 0
    overall_weighted = round(sum(result[r]['weighted'] for r in result)/6, 2)

    # — 3) REMARKS —
    sql_remarks = """
        SELECT
            ed.rubric_id,
            ed.feedback
        FROM director.peer_evaluations pe
        JOIN director.evaluation_details ed ON pe.evaluation_id = ed.evaluation_id
        JOIN maindashboard.users u ON pe.evaluator_id = u.user_id
        WHERE pe.evaluatee_id = %s
          AND pe.evaluation_period_id = (
            SELECT period_id
            FROM director.evaluation_periods
            WHERE active_status = TRUE
              AND period_del_ind = FALSE
          )
          AND pe.peer_eval_delete_ind = FALSE
          AND ed.feedback IS NOT NULL
        ORDER BY ed.rubric_id, pe.evaluation_date;
    """
    df_remarks = db.querydatafromdatabase(sql_remarks, [int(evaluatee_id)], ['rubric_id','feedback'])
    remarks_by_rubric = {i: [] for i in range(1,7)}
    for _, row in df_remarks.iterrows():
        r = int(row['rubric_id'])
        remarks_by_rubric[r].append(f"{row['feedback'].strip()}")
    for r in remarks_by_rubric:
        remarks_by_rubric[r] = "\n\n".join(remarks_by_rubric[r])

    # — 4) SUMMARY & SIGN-OFF —
    sql_sum = """
        SELECT summary_text, summary_conducted_by, summary_conducted_date,
               summary_received_by, summary_received_date
        FROM director.evaluation_summaries
        WHERE summary_evaluatee_id = %s
          AND summary_evaluation_period = (
            SELECT period_id
            FROM director.evaluation_periods
            WHERE active_status = TRUE
              AND period_del_ind = FALSE
          );
    """
    df_sum = db.querydatafromdatabase(sql_sum, [int(evaluatee_id)],
                                     ['summary_text','summary_conducted_by','summary_conducted_date',
                                      'summary_received_by','summary_received_date'])
    if df_sum.empty:
        summary_text = ""
        conducted_by_id = None
        conducted_date = ""
        received_by_id = None
        received_date = ""
    else:
        row = df_sum.iloc[0]
        summary_text = row['summary_text']
        conducted_by_id = int(row['summary_conducted_by']) if row['summary_conducted_by'] is not None else None
        conducted_date = row['summary_conducted_date']
        received_by_id = int(row['summary_received_by']) if row['summary_received_by'] is not None else None
        received_date = row['summary_received_date']

    # helper to look up names
    def lookup_name(uid):
        if not uid:
            return ""
        q = "SELECT CONCAT(user_fname,' ',LEFT(user_mname,1),'. ',user_sname) AS nm FROM maindashboard.users WHERE user_id = %s"
        df = db.querydatafromdatabase(q, [uid], ['nm'])
        return df.at[0, 'nm'] if not df.empty else ""
    conducted_name = lookup_name(conducted_by_id)
    received_name = lookup_name(received_by_id)

    # — 5) Render and PDF —
    ctx = {
        "full_name": evaluatee_name,
        "period": evaluation_period,
        "dates_conducted": evaluation_period,
        "reviewers": reviewers_text,
        "rubrics": [
            {"label":"Contributions",           "counts":result[1], "weighted":result[1]['weighted'], "remarks":remarks_by_rubric[1]},
            {"label":"Cooperation with Others", "counts":result[2], "weighted":result[2]['weighted'], "remarks":remarks_by_rubric[2]},
            {"label":"Focus and Commitments",   "counts":result[3], "weighted":result[3]['weighted'], "remarks":remarks_by_rubric[3]},
            {"label":"Team Role Fulfillment",   "counts":result[4], "weighted":result[4]['weighted'], "remarks":remarks_by_rubric[4]},
            {"label":"Ability to Communicate",  "counts":result[5], "weighted":result[5]['weighted'], "remarks":remarks_by_rubric[5]},
            {"label":"Completion of Tasks",     "counts":result[6], "weighted":result[6]['weighted'], "remarks":remarks_by_rubric[6]},
        ],
        "overall_weighted": overall_weighted,
        "opportunities": summary_text,
        "conducted_name": conducted_name,
        "conducted_date": conducted_date,
        "received_name": received_name,
        "received_date": received_date
    }

    html_out = render_template('peer_evaluation.html', **ctx)
    return HTML(string=html_out).write_pdf()
