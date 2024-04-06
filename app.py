from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, pages_folder="pages", external_stylesheets=[dbc.themes.BOOTSTRAP])



app.layout = html.Div([
    #html.Div([
    #    html.Div(
    #        dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
    #    ) for page in dash.page_registry.values()
    #]),
    dash.page_container,

])

if __name__ == '__main__':
    app.run('0.0.0.0', debug=False)