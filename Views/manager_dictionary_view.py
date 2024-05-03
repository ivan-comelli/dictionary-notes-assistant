from dash import html
import dash_bootstrap_components as dbc
from Components.header_status_save import StatusSave  # Asegúrate de que la ruta de importación sea correcta
from dash import Dash, html, dcc, Input, Output, State, callback, exceptions, ctx
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc
import pandas as pd
from Components.Dictionary.domain_datatable import DomainDatatable
from Components.Dictionary.domain_sunburst_chart import DictionaryChart
from Components.Dictionary.domain_actions_row import DomainActionRow

class DictionaryView:
    def __init__(self, app):
        self.dictionary_table_component = DomainDatatable(app)
        self.action_row_component = DomainActionRow(app)
        self.dictionary_chart_component = DictionaryChart(app)
        self.app = app
        @self.app.callback(
            Output('card-content', 'children'),
            [Input("card-tabs", "active_tab")]
        )
        def render_datatable(active_tab):
            #Falta el if que selecciona el contenido segun active_tab
            if active_tab == "tab-1":
                template = html.Div([
                    html.Div([
                            self.action_row_component.render(),
                            self.dictionary_table_component.render()
                        ])
                ])
            elif active_tab == "tab-2":
                template = html.Div([
                    html.Div([
                        self.dictionary_chart_component.render()
                    ], id='Container'),
                ])
            return template 
            

    def render(self):
        layout = html.Div([
            StatusSave.create(),
            dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Ver Tabla", tab_id="tab-1"),
                                dbc.Tab(label="Ver Arbol", tab_id="tab-2"),
                                #dbc.Tab(label="Versiones", tab_id="tab-3" ),
                            ],
                            id="card-tabs",
                            active_tab="tab-1",
                        )
                    ),
                    dbc.CardBody(id="card-content"),
                ]
            )
        ])

        return layout
            
    