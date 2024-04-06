import pandas as pd
from pandas import DataFrame

import data_utils
from dash import dash_table, dcc, html
import dash_bootstrap_components as dbc


import plotly.express as px

import map_figure

data_worker = data_utils.DataWorker()
#import pandas as pd
def GetMainOilTable():
    df = data_utils.GetMainDf()
    return dash_table.DataTable(data=df.to_dict('records'), page_size=15)

def GetWinkBarPlotLastUpdate():
    df = data_worker.GetLastUpdateDf()
    df = df[df['Тип компании'] == 'ВИНК']
    return px.histogram(df, x='Тип топлива', y="Цена", histfunc='avg', color='Брендинг', barmode='group')
def GetIndependentBarPlotLastUpdate():
    df = data_worker.GetLastUpdateDf()
    df = df[df['Тип компании'] == 'Независимая']
    return px.histogram(df, x='Тип топлива', y="Цена", histfunc='avg', color='Брендинг', barmode='group')
def GetAllCompaniesBarPlotLastUpdate():
    df = data_worker.GetLastUpdateDf()
    return px.histogram(df, x='Тип топлива', y="Цена", histfunc='avg', color='Брендинг', barmode='group')

def GetPriceDynamicAll():
    df = data_worker.main_df.groupby(['Дата', 'Тип топлива'])['Цена'].mean()
    res_df = pd.DataFrame(columns=['Дата', "Тип топлива", "Средняя цена"])
    #print(res_df)
    for key in df.keys():
        res_df.loc[len(res_df)] = [key[0], key[1], df[key]]
    return dcc.Graph(
        id='line-chart-all-time-all-oils',
        figure=px.line(data_frame=res_df, x='Дата', y='Средняя цена', color='Тип топлива')
    )
def GetLineChartByOilType(type_oil):
    df = data_worker.GetMainDf()
    dict_replace = {'АИ-98': 'АИ-98/100', 'АИ-100': 'АИ-98/100', "КПГ": "Метан", "СУГ": "Пропан"}
    df.replace({"Тип топлива": dict_replace}, inplace=True)
    df = df[df['Тип топлива'] == type_oil]
    df_mean = df.groupby(['Дата', "Тип компании"])['Цена'].mean()
    df_mean_all = df.groupby(['Дата'])['Цена'].mean()
    res_df = pd.DataFrame(columns=['Дата', 'Тип компании', 'цена'])
    for key in df_mean.keys():
        date = key[0]
        type_company = key[1]
        price = df_mean[key]
        if not date in res_df['Дата'].values:
            mean_price = df_mean_all[date]
            res_df.loc[len(res_df)] = [key[0], 'Все', mean_price]
        res_df.loc[len(res_df)] = [key[0], key[1], df_mean[key]]
    return dcc.Graph(
        id=f'line-chart-{type_oil}',
        figure=px.line(data_frame=res_df, x='Дата', y='цена', color='Тип компании')
    )

def GetMapTodaySituation():
    geo = data_utils.GeoRegion('geo/data/region52.parquet')
    map = map_figure.mapFigure()
    #print(data_worker.main_df.columns)
    #print(data_worker.main_df.groupby(['Район', 'Тип топлива'])['Цена'].mean())
    #for i, r in geo.nn.iterrows():
    #    map.update_traces(selector=dict(name))
    return dcc.Graph(figure=map, id='map-today-situation', config={'scrollZoom':True})

def GetMapTodaySituationByTypeOilName(type_oil_name):
    map = map_figure.mapFigure()
    df = data_worker.GetMainDf()
    dict_replace = {'АИ-98': 'АИ-98/100', 'АИ-100': 'АИ-98/100', "КПГ": "Метан", "СУГ": "Пропан"}
    df.replace({"Тип топлива": dict_replace}, inplace=True)
    df = df[df['Тип топлива']==type_oil_name]

    if len(df) > 0:
        df = df.groupby(['Район'])['Цена'].mean()
        max_price = df.values.max()
        min_price = df.values.min()
        delta = max_price - min_price
        if delta==0:
            delta = 1
        #print(f"DELTA: {delta}")
        for r in df.keys():
            text = f"{r} - {df[r]}"
            #print(r)
            #print(df[r])
            map.update_traces(selector=dict(name=r),
                              text = f'{r} - средн: {round(df[r], 2)}',
                              fillcolor=f'rgb({int(0+((float(df[r]) - min_price)/delta)*255)}, {int(255-((float(df[r]) - min_price)/delta)*255)}, 36)')
        return dcc.Graph(figure=map, id='map-today-situation',
                         #config={'scrollZoom': True}
                         )


def CreateFuelLine(type_oil_name, is_branding):
    df = data_worker.main_df
    df = df[df['Тип топлива'] == type_oil_name]
    max_date = df['Дата'].values.max()
    df = df[df['Дата'] == max_date]
    if is_branding:
        df = df[df['Брендинг'] == "Бренд"]
        min_value_price = round(df['Цена'].values.min(), 2)
        max_value_price = round(df['Цена'].values.max(), 2)
        mean_value_price = round(df['Цена'].values.mean(), 2)
        card = dbc.Card([
        dbc.Row([

            dbc.Col(children=[html.H3(children=type_oil_name+" Бренд")], md=3),
            dbc.Col(children=[html.H3(children=str(min_value_price), className="price-value-main-page-card")], md=3),
            dbc.Col(children=[html.H3(children=str(max_value_price), className="price-value-main-page-card")], md=3),
            dbc.Col(children=[html.H3(children=str(mean_value_price), className="price-value-main-page-card")], md=3)

            ])
        ])
        return card
    else:
        df = df[df['Брендинг'] != "Бренд"]
        min_value_price = round(df['Цена'].values.min(), 2)
        max_value_price = round(df['Цена'].values.max(), 2)
        mean_value_price = round(df['Цена'].values.mean(), 2)
        card = dbc.Button([
            dbc.Row([

                dbc.Col(children=[html.H3(children=type_oil_name)], md=3),
                dbc.Col(children=[html.H3(children=str(min_value_price), className="price-value-main-page-card")],
                        md=3),
                dbc.Col(children=[html.H3(children=str(max_value_price), className="price-value-main-page-card")],
                        md=3),
                dbc.Col(children=[html.H3(children=str(mean_value_price), className="price-value-main-page-card")],
                        md=3)

            ])
        ], id={'type': 'card', 'index': 1})
        return card

def GetClassicTableReview():
    df = data_worker.GetFuelDfLastUpdate()
    return dash_table.DataTable(data=df.to_dict('records'), page_size=25)


def CreateFuelMainLInes():
    lines = []
    df = data_worker.GetFuelDfLastUpdate()

    for i, item in df.iterrows():
        type_oil_name = item['Тип топлива']
        min_value_price = item["Мин"]
        max_value_price = item["Макс"]
        mean_value_price = item["Средн"]
        card = dbc.Button([
            dbc.Row([

                dbc.Col(children=[html.H5(children=type_oil_name)], md=3),
                dbc.Col(children=[html.H5(children=str(min_value_price), className="price-value-main-page-card")],
                        md=3),
                dbc.Col(children=[html.H5(children=str(max_value_price), className="price-value-main-page-card")],
                        md=3),
                dbc.Col(children=[html.H5(children=str(mean_value_price), className="price-value-main-page-card")],
                        md=3)

            ])
        ], color='light', n_clicks=0, className="card-button")
        lines.append(card)
    return dbc.Row(children=lines)
def CreateMainTableHtml():

    fuel_data = data_worker.main_df
    max_rows = 30
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in fuel_data.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(fuel_data.iloc[i][col]) for col in fuel_data.columns
            ], className='main-fuel-table-tr') for i in range(min(len(fuel_data), max_rows))
        ])
    ], className='table-main-fuel')
