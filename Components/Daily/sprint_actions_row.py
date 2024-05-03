from dash import dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
# ROW FILTER BAR FOR DICTIONARY TABLE
class SprintActionRow: 
    def __init__(self, app):
        pass

    def render(self):
        init_status_filters = {
            "search": "",
            "by-classe": "",
            "order-level": "",
            "only-endpoint": False
        }
        template=html.Div([
            html.Div([
                dbc.Input(
                    type="text",
                    id="search",
                    placeholder="Buscar por coincidencia",
                ),
            ], className="left"),
            html.Div([
                dbc.Button(html.I(className="fa-solid fa-floppy-disk"), id="trigger-save-changes", className="btn btn-primary"),
                dbc.Button(html.I(className="fa-solid fa-trash"), id="trigger-remove-rows", className="btn btn-primary"),
            ], className="right"),           
        ], id="row-actions")

        return template