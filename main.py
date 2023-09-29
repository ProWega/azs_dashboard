from dash import Dash, html, dcc, callback, Output, Input, dash_table, ALL, Patch, callback


import pandas as pd
import sqlite3

import datetime
from datetime import date
import charts_utils

import dash_bootstrap_components as dbc

import data_utils
import flask

today = datetime.date.today()
# current_type_oil = db.oil_types_names[0]
# print(current_type_oil)
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
# df = db.GetSingleDayDf(date(today.year, today.month, 24), current_type_oil)
# df.to_csv('test_delete.csv')
# data = GetDataPriceTableFromDB()
external_scripts = ['scripts/card.js']
app = Dash(__name__, assets_ignore='.*ignored.*', external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.server.static_folder = 'static'
data_worker = data_utils.DataWorker()

wink_content = dbc.Card(
    dbc.CardBody(
        dcc.Graph(
            id='wink_last_update_main_bar',
            figure=charts_utils.GetWinkBarPlotLastUpdate()
        )
    )
)
independent_content = dbc.Card(
dbc.CardBody(
        dcc.Graph(
            id='independent_last_update_main_bar',
            figure=charts_utils.GetIndependentBarPlotLastUpdate()
        )
    )
)
all_companies_content = dbc.Card(
dbc.CardBody(
        dcc.Graph(
            id='all_companies_last_update_main_bar',
            figure=charts_utils.GetIndependentBarPlotLastUpdate()
        )
    )
)
azs_count = len(data_worker.main_df['Ссылка'].unique())
#last_refresh_date = data_utils.DateFromTimeStamp(data_worker.main_df['Дата'].values.max())
app.layout = html.Div([
    html.H1(children=f'Цены на топливо в Нижегородской области {data_utils.StringFromDate(pd.to_datetime(data_worker.max_date))} по {azs_count} АЗС', id='test'),
    dbc.Row(children=[
    dbc.Button([
                dbc.Row([

                    dbc.Col(children=[html.H5(children="Тип топлива")], md=3),
                    dbc.Col(children=[html.H5(children="Мин", className="price-value-main-page-card")],
                            md=3),
                    dbc.Col(children=[html.H5(children="Макс", className="price-value-main-page-card")],
                            md=3),
                    dbc.Col(children=[html.H5(children="Средн", className="price-value-main-page-card")],
                            md=3)

                ]),
            charts_utils.CreateFuelMainLInes()
        ], disabled=True, color='light')
    ], style={'margin': "20px"}),
    dbc.Row(children=[
        dbc.Tabs([
            dbc.Tab(wink_content, label='ВИНК компании'),
            dbc.Tab(independent_content, label='Независимые'),
            dbc.Tab(all_companies_content, label='Все компании')
        ]),

    ]),
    dbc.Row(children=[
    #charts_utils.CreateFuelMainLInes(),
    charts_utils.GetPriceDynamicAll()
    ]),
    html.Hr(),
    html.H2(children='Таблица для более детального анализа'),
    dash_table.DataTable(
        data_worker.main_df.to_dict('records'),
        page_current=0,
        page_action='custom',
        sort_action='custom',
        sort_mode='multi',
        sort_by=[],
        page_size=15,
        id='table-multicol-sorting')




    #charts_utils.CreateFuelLine(data_utils.oil_types_names[0], False),
    #charts_utils.CreateFuelLine(data_utils.oil_types_names[0], True)


])


# Add controls to build the interaction


# @callback(Output(component_id='controls-and-graph', component_property='figure', allow_duplicate=True),
#          Input(component_id='my-date-picker-single', component_property='date'))
# def update_oil_prices(date):
#    df = db.GetSingleDayDf(date, current_type_oil)
@callback(
    Output('table-multicol-sorting', "data"),
    Input('table-multicol-sorting', "page_current"),
    Input('table-multicol-sorting', "page_size"),
    Input('table-multicol-sorting', "sort_by"))
def update_table(page_current, page_size, sort_by):
    print(sort_by)
    if len(sort_by):
        dff = data_worker.main_df.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = data_worker.main_df

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

if __name__ == '__main__':
    app.run_server( debug=False)
