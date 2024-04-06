import dash
from dash import html, dcc, callback, Input, Output, dash_table, ctx
import charts_utils
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import data_utils


dash.register_page(__name__)

data_worker = data_utils.DataWorker()
print(f"TEST DATE {data_utils.DateFromDate64(data_worker.max_date)}")
oil_types = ['АИ-92', 'АИ-95', 'ДТ', 'Пропан', 'АИ-98/100', 'Метан']
tabs_oil_history = [dbc.Tab(children=charts_utils.GetLineChartByOilType(oil_type), label=oil_type)
                    for oil_type in oil_types
                    ]
tabs_today_map_situation = [dbc.Tab(children=charts_utils.GetMapTodaySituationByTypeOilName(oil_type), label=oil_type)
                            for oil_type in oil_types
                            ]

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

layout = html.Div([
dbc.Container(children=[
        html.H2(children=f'Цены на топливо в Нижегородской области {data_utils.StringFromDate(pd.to_datetime(data_worker.max_date))} по данным {azs_count} АЗС', id='test'),
        charts_utils.GetClassicTableReview(),

    ]),
    html.Hr(),
    dbc.Container(children=[
        html.H2(children='Средние розничные цены на различные виды топлива'),
        dbc.Tabs(children=tabs_oil_history)
    ]),
html.Hr(),
dbc.Container(children=[
        html.H2(f'Карта цен на различные виды топлива в Нижегродской области {data_utils.StringFromDate(data_worker.max_date)}'),
        dbc.Tabs(children=tabs_today_map_situation)
    ]),
    html.Hr(),
    dbc.Container(children=[
        html.H2(children='Создать и выгрузить выборку'),
dbc.Row( children=[
       dbc.Col(children=[
            dbc.Label('Тип топлива'),
           dcc.Dropdown(id='dropdown-select-type-oil', value=data_utils.oil_types_names[0],
                         options=[name for name in data_utils.oil_types_names]+['Все'])],
                        width=3
       ),
       dbc.Col( children=[
            dbc.Label('Брендинг'),
            dcc.Dropdown(id='dropdown-select-branding', value='Все', options=[
               "Бренд",
                "Не бренд",
                "Все"
           ])], width=3
        ),
    dbc.Col( children=[
            dbc.Label('Тип поставщика'),
           dcc.Dropdown(id='dropdown-select-type-company', value='Все', options=[
                type_name
                for type_name in np.unique(data_utils.name_type_company)]
                +["Все"]
            )], width=3
        )
    ]),
        html.Hr(),
        dcc.DatePickerSingle(
            placeholder='DD-MM-YY',
            display_format='DD-MM-YY',
            with_portal=True,
            date= data_utils.DateFromDate64(data_worker.max_date),
            id='calend-oil-date'
        ),
        dbc.Row(children=[
                dbc.Col([
                    dbc.Button(children='Скачать таблицу csv', color='light', id='download-data-oil-csv', n_clicks=0),
                    dbc.Button(children='Скачать таблицу excel', color='light', id='download-data-oil-xls', n_clicks=0),
                    dcc.Download(id='download-data-oil'),
                    dcc.Download(id='download-data-xls-oil')
                    ]),
            ], style={'margin': '20px'}
        ),


    ]),
dbc.Container(children=[
        dash_table.DataTable(id='oil-history-table', page_size=10, page_current=0, sort_by=[], sort_mode='single', sort_action='custom')
    ])
    #dbc.Container(children=[
    #    html.H2('Карта цен на различные виды топлива в Нижегродской области'),
    #    charts_utils.GetMapTodaySituation()
    #]),



])



@callback(Output('oil-history-table', 'data'),
          Input('dropdown-select-type-oil', 'value'),
          Input('dropdown-select-branding', 'value'),
          Input('dropdown-select-type-company', 'value'),
          Input('calend-oil-date', 'date'),
          Input('oil-history-table', "page_current"),
          Input('oil-history-table', "page_size")
          )
def update_table_oil(type_oil, branding, type_company, date, page_current, page_size):
    df = data_worker.GetDfByTypeOilTypeBrandAndTypeCompany(type_oil, branding, type_company)
    date = np.datetime64(date)
    date = data_utils.DateFromDate64(date)
    df = df[df['Дата'] >= np.datetime64(date)]
    sup_date = data_utils.DateFromTimeStamp(data_utils.TimestampFromDate(date) + 24 * 60 * 60)
    df = df[df["Дата"] <= sup_date]
    return df.to_dict("records")
    df = df[df["Дата"]<=sup_date]
    #print(df.head(3))
    return df.to_dict("records")
    #return dff.iloc[
    #    page_current*page_size:(page_current+ 1)*page_size
    #].to_dict('records')

@callback(
    Output("download-data-oil", "data"),
    Input("download-data-oil-csv", "n_clicks"),
Input('dropdown-select-type-oil', 'value'),
          Input('dropdown-select-branding', 'value'),
          Input('dropdown-select-type-company', 'value'),
          Input('calend-oil-date', 'date'),
    prevent_initial_call=True,
)
def download_csv(n_clicks, type_oil, branding, type_company, date):
    button_clicked = ctx.triggered_id
    if button_clicked == 'download-data-oil-csv':
        print('DOWN CSV')
        df = data_worker.GetDfByTypeOilTypeBrandAndTypeCompany(type_oil, branding, type_company)
        date = np.datetime64(date)
        date = data_utils.DateFromDate64(date).date()
        df = df[df['Дата'] >= np.datetime64(date)]
        sup_date = data_utils.DateFromTimeStamp(data_utils.TimestampFromDate(date) + 24 * 60 * 60)
        df = df[df["Дата"] <= sup_date]
        return dcc.send_data_frame(df.to_csv, f"report{date.day}_{date.month}_{date.year}.csv")

@callback(
    Output("download-data-xls-oil", "data"),
    Input("download-data-oil-xls", "n_clicks"),
Input('dropdown-select-type-oil', 'value'),
          Input('dropdown-select-branding', 'value'),
          Input('dropdown-select-type-company', 'value'),
          Input('calend-oil-date', 'date'),
    prevent_initial_call=True,
)
def download_xls(n_clicks, type_oil, branding, type_company, date):
    button_clicked = ctx.triggered_id
    if button_clicked == 'download-data-oil-xls':
        print('DOWN xls')
        df = data_worker.GetDfByTypeOilTypeBrandAndTypeCompany(type_oil, branding, type_company)
        date = np.datetime64(date)
        date = data_utils.DateFromDate64(date).date()
        df = df[df['Дата'] >= np.datetime64(date)]
        sup_date = data_utils.DateFromTimeStamp(data_utils.TimestampFromDate(date) + 24 * 60 * 60)
        df = df[df["Дата"] <= sup_date]
        return dcc.send_data_frame(df.to_excel, f"report{date.day}_{date.month}_{date.year}.xlsx")