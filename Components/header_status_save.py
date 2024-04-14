from dash import html
import dash_bootstrap_components as dbc

class StatusSave:
    @staticmethod
    def create():
        return html.Div([
            dbc.Spinner(color="primary", type="grow"),
            html.H3("Guardado")
        ])
