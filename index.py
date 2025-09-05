from dash import dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
 
import dash 
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate 

import webbrowser 
from urllib.parse import urlparse, parse_qs

from app import app
from apps import commonmodules as cm
from apps import home
from apps import blankpage  
from apps import dbconnect as db

from apps.maindashboard import homepage, peer_evaluation_landing, peer_evaluation_form_entry, user_profile, register_user, search_users, password, about_TINQAD, basichome
from apps.director import peer_evaluation_settings, peer_evaluation_form, peer_evaluation_responses, evaluation_summary, remove_periods, director_dashboard
from apps.admin import add_inventory, administration_dashboard, expensetype_add, inventory_tracker, record_expenses, staff_profiles_management, staff_profiles, training_instructions, instructions, training_documents, add_expenses, training_record, viewexpense_list, viewtraining_list
from apps.iqa import iqa_dashboard, more_details, acad_heads_directory, acadheads_profile, iso_facilitator_directory, iso_facilitator_profile
from apps.eqa import eqa_dashboard, assessment_reports, assessment_details, accreditation_tracker, program_list, program_details, sar_details, program_info
from apps.eqa import program_page, reports_details
from apps.km import (km_dashboard, add_criteria, sdglist, sdg_form_1, sdg_form_2, sdg_form_3, sdg_form_4, sdg_form_5, sdg_form_6, sdg_form_7, sdg_form_8, sdg_form_9, sdg_form_10, sdg_form_11, sdg_form_12, sdg_form_13, sdg_form_14, sdg_form_15, sdg_form_16, sdg_form_17, qsrankings, qsrankingsprovider, sdg_QAO_view, sdg_1_evidence, sdg_2_evidence,
                     sdg_3_evidence, sdg_4_evidence, sdg_5_evidence, sdg_6_evidence, sdg_7_evidence, sdg_8_evidence, sdg_9_evidence, sdg_10_evidence, sdg_11_evidence, sdg_12_evidence,
                     sdg_13_evidence, sdg_14_evidence, sdg_15_evidence, sdg_16_evidence, sdg_17_evidence)
from apps.qaofficers import qa_directory, qaofficers_profile, training_details, qa_dashboard, faculty_cdf   


 
CONTENT_STYLE = {
    "margin-top": "4em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

server = app.server

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),

        # LOGIN DATA
        # 1 current_user_id -- stores user_id
        dcc.Store(id='sessionlogout', data = True, storage_type='local'),
        dcc.Store(id='currentuserid', data=-1, storage_type='local'),
        
        # 2 currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=0, storage_type='local'),
        
        # Page mode and user id for viewing for those that have any
        dcc.Store(id='page_mode', data=-1, storage_type='memory'),
        dcc.Store(id='view_id', data=-1, storage_type='memory'),

        cm.navbar,
        html.Div(id='page-content', style=CONTENT_STYLE),
        html.Link(rel='icon', href='/assets/icons/TINQAD.png')
    ]
)



@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
        State('currentrole', 'data'),
        State('url', 'search')
    ]
)
def displaypage(pathname, sessionlogout, user_id, accesstype, search):
    # Default return layout is a blank page
    returnlayout = blankpage.layout
    logout_conditions = [
        pathname in ['/', '/logout'],
        user_id == -1,
        not user_id
    ]
    sessionlogout = any(logout_conditions)

    # Parse mode from the URL search string if present
    mode = None
    parsed = urlparse(search)
    if parse_qs(parsed.query):
        mode = parse_qs(parsed.query).get('mode', [None])[0]

    # Check if the callback was triggered by the URL input
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid == 'url': 
        # Public pages accessible to everyone
        if pathname in ['/', '/home', '/logout']:
            returnlayout = home.layout
        # Pages accessible only to logged-in users
        elif user_id != -1:
            if accesstype >= 2:
                if pathname == '/homepage':
                    returnlayout = homepage.layout  # Layout for full access users
                elif pathname == '/profile':
                    returnlayout = user_profile.layout
                elif pathname == '/register_user':
                    returnlayout = register_user.layout
                elif pathname == '/search_users':
                    returnlayout = search_users.layout
                elif pathname == '/password':
                    returnlayout = password.layout
                elif pathname == '/About_TINQAD':
                    returnlayout = about_TINQAD.layout

                #admin team
                elif pathname == '/administration_dashboard':
                    returnlayout = administration_dashboard.layout
                elif pathname == '/record_expenses':
                    returnlayout = record_expenses.layout
                elif pathname == '/record_expenses/add_expense':
                    returnlayout = add_expenses.layout
                elif pathname == '/expense_list':
                    returnlayout = viewexpense_list.layout
                elif pathname == '/expense_list/add_expensetype':
                    returnlayout = expensetype_add.layout
                elif pathname == '/instructions':
                    returnlayout = instructions.layout
                elif pathname == '/training_instructions':
                    returnlayout = training_instructions.layout 
                elif pathname == '/training_documents':
                    returnlayout = training_documents.layout
                elif pathname == '/training_record':
                    returnlayout = training_record.layout
                elif pathname == '/training_record/mode=view':
                    returnlayout = viewtraining_list.layout
                elif pathname == '/inventory_tracker':
                    returnlayout = inventory_tracker.layout
                elif pathname == '/inventory_tracker_management':
                    returnlayout = add_inventory.layout
                elif pathname == '/staff_profiles':
                    if accesstype == 3:
                        returnlayout = staff_profiles.layout
                elif pathname == '/staff_profiles_management':
                    if accesstype == 3:
                        returnlayout = staff_profiles_management.layout
                
                #director's view
                elif pathname == '/director_dashboard':
                    if accesstype == 2:
                        returnlayout = director_dashboard.layout
                elif pathname == '/peer_evaluation_settings':
                    if accesstype == 2:
                        returnlayout = peer_evaluation_settings.layout
                elif pathname == '/peer_evaluation_settings/peer_evaluation_forms':
                    if accesstype == 2:
                        returnlayout = peer_evaluation_form.layout
                elif pathname == '/peer_evaluation_responses':
                    if accesstype == 2:
                        returnlayout = peer_evaluation_responses.layout
                elif pathname == '/peer_evaluation_responses/evaluation_summary':
                    if accesstype == 2:
                        returnlayout = evaluation_summary.layout
                elif pathname == '/peer_evaluation_settings/remove_evaluation_periods':
                    if accesstype == 2:
                        returnlayout = remove_periods.layout

                #for everyone
                elif pathname == '/peer_evaluation_landing':
                    returnlayout = peer_evaluation_landing.main_layout
                elif pathname == '/peer_evaluation_form_entry':
                    returnlayout = peer_evaluation_form_entry.main_layout

                #iqa team
                elif pathname == '/iqa_dashboard':
                    returnlayout = iqa_dashboard.layout
                elif pathname == '/dashboard/more_details':
                    returnlayout = more_details.layout  
                elif pathname == '/acad_heads_directory':
                    returnlayout = acad_heads_directory.layout
                elif pathname == '/acadheads_profile':
                    returnlayout = acadheads_profile.layout
                elif pathname == '/iso_facilitator_directory':
                    returnlayout = iso_facilitator_directory.layout
                elif pathname == '/iso_facilitator_profile':
                    returnlayout = iso_facilitator_profile.layout

                #eqa team/sdglist/sdg1submission
                elif pathname == '/eqa_dashboard':
                    returnlayout = eqa_dashboard.layout
                elif pathname == '/assessment_reports':
                    returnlayout = assessment_reports.layout
                elif pathname == '/assessment_tracker/assessment_details':
                    returnlayout = assessment_details.layout
                elif pathname == '/assessmentreports/sar_details':
                    returnlayout = sar_details.layout
                elif pathname == '/assessmentreports/reports_details':
                    returnlayout = reports_details.layout
                elif pathname == '/assessment_tracker':
                    returnlayout = accreditation_tracker.layout
                elif pathname == '/program_list':
                    returnlayout = program_list.layout
                elif pathname == '/program_details':
                    returnlayout = program_details.layout
                elif pathname == '/program_info':
                    returnlayout = program_info.layout
                elif pathname == '/program_page':
                    returnlayout = program_page.layout

                #km team
                elif pathname == '/km_dashboard':
                    returnlayout = km_dashboard.layout 
                elif pathname == '/add_criteria':
                    returnlayout = add_criteria.layout 
                elif pathname == '/sdglist':
                    returnlayout = sdglist.layout
                elif pathname == '/SDG_evidencelist':
                    returnlayout = sdg_QAO_view.layout
                elif pathname == '/SDG_evidencelist/sdg1':
                    returnlayout = sdg_1_evidence.layout  
                elif pathname == '/SDG_evidencelist/sdg2':
                    returnlayout = sdg_2_evidence.layout  
                elif pathname == '/SDG_evidencelist/sdg3':
                    returnlayout = sdg_3_evidence.layout  
                elif pathname == '/SDG_evidencelist/sdg4':
                    returnlayout = sdg_4_evidence.layout
                elif pathname == '/SDG_evidencelist/sdg5':
                    returnlayout = sdg_5_evidence.layout  
                elif pathname == '/SDG_evidencelist/sdg6':
                    returnlayout = sdg_6_evidence.layout
                elif pathname == '/SDG_evidencelist/sdg7':
                    returnlayout = sdg_7_evidence.layout  
                elif pathname == '/SDG_evidencelist/sdg8':
                    returnlayout = sdg_8_evidence.layout
                elif pathname == '/SDG_evidencelist/sdg9':
                    returnlayout = sdg_9_evidence.layout  
                elif pathname == '/SDG_evidencelist/sdg10':
                    returnlayout = sdg_10_evidence.layout
                elif pathname == '/SDG_evidencelist/sdg11':
                    returnlayout = sdg_11_evidence.layout  
                elif pathname == '/SDG_evidencelist/sdg12':
                    returnlayout = sdg_12_evidence.layout
                elif pathname == '/SDG_evidencelist/sdg13':
                    returnlayout = sdg_13_evidence.layout  
                elif pathname == '/SDG_evidencelist/sdg14':
                    returnlayout = sdg_14_evidence.layout
                elif pathname == '/SDG_evidencelist/sdg15':
                    returnlayout = sdg_15_evidence.layout  
                elif pathname == '/SDG_evidencelist/sdg16':
                    returnlayout = sdg_16_evidence.layout
                elif pathname == '/SDG_evidencelist/sdg17':
                    returnlayout = sdg_17_evidence.layout   
                elif pathname == "/qs_rankings":
                    returnlayout = qsrankings.layout   
                
                #qa officers
                elif pathname == '/QAOfficers_dashboard':
                    returnlayout = qa_dashboard.layout
                elif pathname == '/qaofficers_profile':
                    returnlayout = qaofficers_profile.layout  
                elif pathname == '/qaofficers_training':
                    returnlayout = training_details.layout 
                elif pathname == '/qaofficers_directory':
                    returnlayout = qa_directory.layout 
                elif pathname == '/qaofficers_faculty_cdf':
                    returnlayout = faculty_cdf.layout

                #sdg evidences
                elif pathname == '/sdglist/sdg1submission':
                    returnlayout = sdg_form_1.layout
                elif pathname == '/sdglist/sdg2submission':
                    returnlayout = sdg_form_2.layout
                elif pathname == '/sdglist/sdg3submission':
                    returnlayout = sdg_form_3.layout
                elif pathname == '/sdglist/sdg4submission':
                    returnlayout = sdg_form_4.layout
                elif pathname == '/sdglist/sdg5submission':
                    returnlayout = sdg_form_5.layout
                elif pathname == '/sdglist/sdg6submission':
                    returnlayout = sdg_form_6.layout
                elif pathname == '/sdglist/sdg7submission':
                    returnlayout = sdg_form_7.layout
                elif pathname == '/sdglist/sdg8submission':
                    returnlayout = sdg_form_8.layout
                elif pathname == '/sdglist/sdg9submission':
                    returnlayout = sdg_form_9.layout
                elif pathname == '/sdglist/sdg10submission':
                    returnlayout = sdg_form_10.layout
                elif pathname == '/sdglist/sdg11submission':
                    returnlayout = sdg_form_11.layout
                elif pathname == '/sdglist/sdg12submission':
                    returnlayout = sdg_form_12.layout
                elif pathname == '/sdglist/sdg13submission':
                    returnlayout = sdg_form_13.layout
                elif pathname == '/sdglist/sdg14submission':
                    returnlayout = sdg_form_14.layout
                elif pathname == '/sdglist/sdg15submission':
                    returnlayout = sdg_form_15.layout
                elif pathname == '/sdglist/sdg16submission':
                    returnlayout = sdg_form_16.layout
                elif pathname == '/sdglist/sdg17submission':
                    returnlayout = sdg_form_17.layout

                else:
                    returnlayout = blankpage.layout
                
                
            elif accesstype == 1:
                if pathname == '/homepage':
                    returnlayout = basichome.layout  # Layout for full access users
                elif pathname == '/profile':
                    returnlayout = user_profile.layout
                elif pathname == '/About_TINQAD':
                    returnlayout = about_TINQAD.layout
                elif pathname == '/training_instructions':
                    returnlayout = training_instructions.layout
                elif pathname == '/training_documents':
                    returnlayout = training_documents.layout 
                elif pathname == '/km_dashboard':
                    returnlayout = km_dashboard.layout 
                elif pathname == "/qs_rankings_provider":
                    returnlayout = qsrankingsprovider.layout
                elif pathname == '/sdglist':
                    returnlayout = sdglist.layout
                elif pathname == '/sdglist/sdg1submission':
                    returnlayout = sdg_form_1.layout
                elif pathname == '/sdglist/sdg2submission':
                    returnlayout = sdg_form_2.layout
                elif pathname == '/sdglist/sdg3submission':
                    returnlayout = sdg_form_3.layout
                elif pathname == '/sdglist/sdg4submission':
                    returnlayout = sdg_form_4.layout
                elif pathname == '/sdglist/sdg5submission':
                    returnlayout = sdg_form_5.layout
                elif pathname == '/sdglist/sdg6submission':
                    returnlayout = sdg_form_6.layout
                elif pathname == '/sdglist/sdg7submission':
                    returnlayout = sdg_form_7.layout
                elif pathname == '/sdglist/sdg8submission':
                    returnlayout = sdg_form_8.layout
                elif pathname == '/sdglist/sdg9submission':
                    returnlayout = sdg_form_9.layout
                elif pathname == '/sdglist/sdg10submission':
                    returnlayout = sdg_form_10.layout
                elif pathname == '/sdglist/sdg11submission':
                    returnlayout = sdg_form_11.layout
                elif pathname == '/sdglist/sdg12submission':
                    returnlayout = sdg_form_12.layout
                elif pathname == '/sdglist/sdg13submission':
                    returnlayout = sdg_form_13.layout
                elif pathname == '/sdglist/sdg14submission':
                    returnlayout = sdg_form_14.layout
                elif pathname == '/sdglist/sdg15submission':
                    returnlayout = sdg_form_15.layout
                elif pathname == '/sdglist/sdg16submission':
                    returnlayout = sdg_form_16.layout
                elif pathname == '/sdglist/sdg17submission':
                    returnlayout = sdg_form_17.layout

                else:
                    returnlayout = blankpage.layout
            else:
                returnlayout = blankpage.layout

    return [returnlayout, sessionlogout]
if __name__ == '__main__':
   webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
   app.run(debug=False)

# if __name__ == '__main__':
#     # Open the web browser to the correct URL 
#     url = 'http://10.206.100.41:8050/'
#     webbrowser.open(url, new=0, autoraise=True)
    
#     # Run the Dash app on all network interfaces (0.0.0.0) on port 8050
#     app.run_server(host='10.206.100.41', port=8050, debug=False)