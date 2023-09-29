import pandas as pd
from pandas import DataFrame

import data_utils
from dash import dash_table, dcc, html
import dash_bootstrap_components as dbc


import plotly.express as px

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
    print(res_df)
    for key in df.keys():
        res_df.loc[len(res_df)] = [key[0], key[1], df[key]]
    return dcc.Graph(
        id='line-chart-all-time-all-oils',
        figure=px.line(data_frame=res_df, x='Дата', y='Средняя цена', color='Тип топлива')
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
