'''Класс для слоя подложки карты России'''

import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
from shapely.geometry import Point

nn = pd.read_parquet("geo/data/region52_medium.parquet")

def convert_crs(x_arr, y_arr, to_crs='EPSG:32646', from_crs="EPSG:4326"):
    """Преобразование значений координат в массивах x_arr и y_arr
    из географической системы отсчёта from_crs в систему to_crs
    """
    data = [Point(x,y) for x,y in zip(x_arr, y_arr)]
    pts = gpd.GeoSeries(data, from_crs).to_crs(to_crs)
    return x_arr, y_arr
    #return pts.x, pts.y

class mapFigure(go.Figure):
    """ Шаблон фигуры для рисования поверх карты России
    """
    def __init__(self, # дефолтные параметры plotly
        data=None, layout=None, frames=None, skip_invalid=False, 
        **kwargs # аргументы (см. документацию к plotly.graph_objects.Figure())
    ):
        # создаём plotlу фигуру с дефолтными параметрами
        super().__init__(data, layout, frames, skip_invalid, **kwargs)

        # прорисовка регионов
        for i, r in nn.iterrows():
            self.add_trace(go.Scatter(x=r.x, y=r.y,
                                      name=r.district,
                                      text=r.district,
                                      hoverinfo="text",
                                      line_color='grey',
                                      fill='toself',
                                      line_width=1,
                                      fillcolor='lightblue',
                                      showlegend=False
            ))
        
        # не отображать оси, уравнять масштаб по осям
        self.update_xaxes(visible=False)
        self.update_yaxes(visible=False, scaleanchor="x", scaleratio=1)

        # чтобы покрасивее вписывалась карта на поверхности фигуры
        self.update_layout(showlegend=False, dragmode='pan',
                           #width=800, height=450,
                           margin={'l': 10, 'b': 40, 't': 10, 'r': 10},
                           )