from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
 
import dash 
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go

from app import app
from apps import commonmodules as cm
from apps import dbconnect as db
from datetime import datetime







def get_year_range():
    current_year = datetime.now().year
    previous_year = current_year - 1
    return f"{previous_year}-{current_year}"


def charts_mainexp():
    current_year = datetime.now().year

    pie_sql = """
        SELECT me.main_expense_shortname, SUM(exp_amount) AS total_amount
        FROM adminteam.expenses AS e
        LEFT JOIN adminteam.main_expenses AS me ON e.main_expense_id = me.main_expense_id
        WHERE EXTRACT(YEAR FROM e.exp_date) = %s
          AND e.exp_del_ind IS FALSE
        GROUP BY me.main_expense_shortname
    """

    pie_df = db.querydatafromdatabase(pie_sql, (current_year,), ['main_expense_shortname', 'total_amount'])

    if pie_df.empty:
        pie_chart = html.Div("No data available for the pie chart")
    else:
        # Set custom legend labels
        custom_legend_labels = dict(zip(pie_df['main_expense_shortname'], pie_df['main_expense_shortname']))

        # Define custom colors
        custom_colors = ['#39B54A', '#F8B237', '#D37157']

        pie_fig = go.Figure(data=[go.Pie(
            labels=pie_df['main_expense_shortname'],
            values=pie_df['total_amount'],
            marker=dict(colors=custom_colors),
            hole=0.4  # Adjust the value to change the size of the hole
        )])
        pie_fig.update_traces(textinfo='percent+label')  # Show percentage and label on pie chart
        pie_fig.update_layout(
            title=f"{get_year_range()}",  # Title with month and year
            title_font=dict(size=18),
            legend=dict(title_font=dict(size=12), orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        pie_chart = dcc.Graph(figure=pie_fig)

    # Fetch data from the database for the bar chart
    bar_sql = """
        SELECT 
            TO_CHAR(exp_date, 'Month') AS month,
            SUM(exp_amount) AS total_amount
        FROM adminteam.expenses
        WHERE EXTRACT(YEAR FROM exp_date) = %s
          AND exp_del_ind IS FALSE
        GROUP BY TO_CHAR(exp_date, 'Month')
        ORDER BY TO_DATE(TO_CHAR(exp_date, 'Month'), 'Month')
    """
    bar_df = db.querydatafromdatabase(bar_sql, (current_year,), ['month', 'total_amount'])

    if bar_df.empty:
        bar_chart = html.Div("No data available for the bar chart")
    else:
        bar_fig = go.Figure([go.Bar(x=bar_df['month'], y=bar_df['total_amount'])])
        bar_fig.update_layout(
            title='Monthly Expenses',
            xaxis_title='Month',
            yaxis_title='Expenses',
            title_x=0.5,
            margin={'l': 50, 'r': 50, 't': 100, 'b': 0},  # Zero bottom margin
            height=400  # Set the height of the bar graph
        )
        bar_fig.update_layout(
            title_font=dict(size=18)  # Fixed font size for the title
        )
        bar_chart = dcc.Graph(figure=bar_fig)

    return dbc.Row(
        [
            dbc.Col(pie_chart, width=6),  # Equal width for both charts
            dbc.Col(bar_chart, width=6)   # Equal width for both charts
        ]
    )




def charts_subexp():
    # Fetch data from the database for the pie chart
    current_year = datetime.now().year

    pie_sql = """
        SELECT se.sub_expense_name, SUM(exp_amount) AS total_amount
        FROM adminteam.expenses AS e
        LEFT JOIN adminteam.sub_expenses AS se ON e.main_expense_id = se.sub_expense_id
        WHERE EXTRACT(YEAR FROM e.exp_date) = %s
          AND e.main_expense_id = 1
          AND e.exp_del_ind IS FALSE
        GROUP BY se.sub_expense_name
    """

    pie_df = db.querydatafromdatabase(pie_sql, (current_year,), ['sub_expense_name', 'total_amount'])

    if pie_df.empty:
        pie_chart = html.Div("No data available for the pie chart")
    else:
        # Set custom legend labels
        custom_legend_labels = dict(zip(pie_df['sub_expense_name'], pie_df['sub_expense_name']))

        # Define custom colors
        custom_colors = ['#39B54A', '#F8B237', '#D37157', '#A9CD46', '#7EADE4', '#40BFBC']

        pie_fig = go.Figure(data=[go.Pie(
            labels=pie_df['sub_expense_name'],
            values=pie_df['total_amount'],
            marker=dict(colors=custom_colors),
            hole=0.4  # Adjust the value to change the size of the hole
        )])
        pie_fig.update_traces(textinfo='percent')  # Show percentage and label on pie chart
        pie_fig.update_layout(
            title=f"{get_year_range()}",  # Title with month and year
            title_font=dict(size=18),
        )
        pie_chart = dcc.Graph(figure=pie_fig)

    legend = dict(title_font=dict(size=12), orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)

    return dbc.Row(
        [
            dbc.Col(pie_chart, width=6),  # Equal width for both charts
            dbc.Col(legend, width=6),  # Equal width for both charts
        ]
    )





def get_main_expenses():
    df = db.querydatafromdatabase("SELECT main_expense_id, main_expense_name FROM adminteam.main_expenses WHERE main_expense_del_ind is FALSE", (), ['main_expense_id', 'main_expense_name'])
    main_expenses = df.to_records(index=False).tolist()
    return main_expenses

def get_sub_expenses(main_expense_id):
    df = db.querydatafromdatabase("SELECT sub_expense_id, sub_expense_name, main_expense_id FROM adminteam.sub_expenses WHERE main_expense_id = %s AND sub_expense_del_ind is FALSE", (main_expense_id,), ['sub_expense_id', 'sub_expense_name', 'main_expense_id'])
    sub_expenses = df.to_records(index=False).tolist()
    return sub_expenses

def populate_accordion():
    main_expenses = get_main_expenses()
    accordion_items = []

    for main_expense in main_expenses:
        main_expense_id, main_expense_name = main_expense
        
        sub_expenses = get_sub_expenses(main_expense_id)
        sub_items = []

        for sub_expense in sub_expenses:
            sub_expense_id, sub_expense_name, _ = sub_expense
            sub_items.append(html.P(sub_expense_name))

        accordion_item = dbc.AccordionItem(
            sub_items,
            title=main_expense_name,
        )
        accordion_items.append(accordion_item)

    return html.Div(dbc.Accordion(accordion_items))

expensetypes = populate_accordion()



layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("ADMIN DASHBOARD"),
                        html.Hr(),
                        html.Div(  
                            [
                                dcc.Store(id='admindashboard_toload', storage_type='memory', data=0),
                            ]
                        ),
                        
                        dbc.Row(
                            [
                                dbc.CardHeader(html.H3("Spending Overview", className="mb-0")),
                                dbc.CardBody(
                                    html.Div(id='charts_mainexp')
                                )
                            ]
                        ),  
                        dbc.Row(
                            [
                                dbc.CardHeader(html.H5("MOOE sub expenses overview", className="mb-0")),
                                dbc.CardBody(
                                    html.Div(id='charts_subexp')
                                )
                            ]
                        ), 

                        dbc.Row(
                            [
                                dbc.CardHeader(html.H3("Expense Types", className="mb-0")),
                                dbc.CardBody(
                                    expensetypes,
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                        dbc.Button("Edit Expense Type List", color="link"),
                                        href="/expense_list",
                                        style={"text-align": "right"}
                                    ),
                                    width={"size": 8}  # Adjust width and offset for alignment
                                ),
                            ],
                        ),
                        html.Br(), html.Br(), html.Br(),
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)




@app.callback(
    [Output('charts_mainexp', 'children'),
     Output('charts_subexp', 'children')],
    [Input('admindashboard_toload', 'modified_timestamp')],
    [State('admindashboard_toload', 'data')]
)
def update_charts(timestamp, toload):
    if toload:
        main_exp_charts = charts_mainexp()
        sub_exp_charts = charts_subexp()
        return main_exp_charts, sub_exp_charts
    else:
        raise PreventUpdate
    

@app.callback(
    Output('admindashboard_toload', 'data'),
    Input('url', 'pathname')
)
def trigger_chart_loading(pathname):
    if pathname == '/administration_dashboard':
        return 1   
    return 0  
