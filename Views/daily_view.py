from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from Components.header_status_save import StatusSave  # Ajusta la ruta de importación según la estructura de tu proyecto
from Components.Daily.sprint_datatable import SprintDatatable
from Components.Daily.sprint_actions_row import SprintActionRow

class DailyView:
    def __init__(self, app):
        self.sprint_table = SprintDatatable(app)
        self.sprint_action_row = SprintActionRow(app)
        
    def render(self):
        template = html.Div([
            StatusSave.create(),
            html.H1("Registro de Sprint de Trabajo"),
            self.sprint_action_row.render(),
            self.sprint_table.render(),
            dbc.InputGroup(
                [
                    dbc.Input(id="input-group-button-input", placeholder="Escribe tu Nota..."),
                    dbc.Button("Guardar", id="input-group-button", n_clicks=0),
                ]
            ),
        ])

        return template