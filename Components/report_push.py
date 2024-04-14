from dash import Dash, html, Input, Output, ALL, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from bidirectional_list_item import BidirectionalListItem  # Asegúrate de que esta importación coincida con la ubicación de tu archivo

class ReportPush:
    def __init__(self, app: Dash, data):
        self.app = app
        self.report_items = pd.DataFrame({
            'name': data.names,
            'type': data.types,
            'level': data.levels,
            'prev_value': data.prev_values,
            'new_value': data.new_values,
            'is_selected': False 
        })
        self.initialize_callbacks()

    def render(self):
        # Generación del layout de report_push
        return html.Div([
            html.Div([
                dbc.InputGroup([
                    dbc.DropdownMenu([
                        dbc.DropdownMenuItem("Marketing", id="dropdown-menu-item-1"),
                        dbc.DropdownMenuItem("Mecanica", id="dropdown-menu-item-2"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Agregar Nuevo", id="dropdown-menu-item-clear"),
                    ], label="Generate"),
                    dbc.Input(id="input-group-dropdown-input", placeholder="name"),
                ]),
            ]),
            html.Hr(),
            html.Div([
                html.H1("Seleccionados"),
                dbc.ListGroup(id="group_selected", children=[
                    BidirectionalListItem.create(row['new_value'].name, row['prev_value'].name, row['is_selected'], i) 
                    for i, row in self.report_items.iterrows()
                ])
            ]),
            html.Hr(),
            html.Div([
                html.H1("Cambios Nuevos"),
                dbc.ListGroup(id="group_selected", children=[
                    BidirectionalListItem.create(row['new_value'].name, row['prev_value'].name, row['is_selected'], i) 
                    for i, row in self.report_items.iterrows()
                ])
            ]),
        ])

    def initialize_callbacks(self):
        @self.app.callback(
            Output('output-component', 'children'),
            [Input({'type': 'increment-button', 'index': ALL}, 'n_clicks'),
            Input({'type': 'decrement-button', 'index': ALL}, 'n_clicks')],
            prevent_initial_call=True
        )
        def button_click(n_clicks_increment, n_clicks_decrement):
            ctx = callback_context

            if not ctx.triggered:
                button_id = 'No buttons have been clicked yet'
                button_type = 'No type'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
                button_type = eval(button_id)['type']

            return f'Button {button_id} of type {button_type} was clicked'
