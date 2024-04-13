from dash import dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd


"""
Módulo de Python para la gestión de datos de nodos y aspectos relacionados al dominio.

Este módulo proporciona funcionalidades para la visualización, filtrado y gestión de datos
relacionados con nodos y aspectos dentro de un dominio específico. Se espera que este
componente facilite la manipulación de registros de manera eficiente y organizada.

Estructura de la Tabla:
- ID: Identificador único del registro.
- Node: Nombre del nodo dentro del dominio.
- Classe: Clase a la que pertenece el nodo, que es la relacion con un nodo padre.
- Description: Descripción del nodo.
- Level: Nivel jerárquico del nodo.
- Prop oculta o no is_endpoint: Indicador de si el nodo es un punto final.

Funcionalidades Principales:
- Filtrado: Permite filtrar los registros por nombre de nodo, clase, nivel ascendente o descendente,
  y si es un punto final o no.
- Modal de Aspectos Relacionados: Al hacer clic en un punto final, se abre un modal para agregar o
  quitar registros de aspectos relacionados al dominio.
- Importación de Datos: Permite importar archivos CSV formateados para actualizar los registros y
  generar informes.
- Gestión de Cambios y Commit: El botón "Submit" guarda los cambios en la tabla y permite realizar
  commits en las ramas. Se proporciona la opción de descartar cambios y crear nuevas ramas.

"""
class DictionaryTable:
    def __init__(self, app, df_dictionary):
        self.app = app
        expected_columns = ['node', 'classe', 'description', 'level', 'is_endpoint']
        if not all(column in df_dictionary.columns for column in expected_columns):
            raise ValueError("El DataFrame no contiene las columnas esperadas.")
        self.df_dictionary = df_dictionary

    def aspect_modal(self, app):
        template = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Aspectos Relacionados: ")),
                dbc.ModalBody(id="modal-container"),
                dbc.ModalFooter([
                    dbc.Button("Cerrar", id="close-modal", className="ms-auto", n_clicks=0),
                    dbc.Button("Guardar", id="save-modal", className="ms-auto", n_clicks=0)
                ]),
            ],
            id="modal-xl",
            size="xl",
            is_open=False,
        )
        return template
    
    def filter_bar(self, app):
        init_status_filters = {
            "search": "",
            "by-classe": "",
            "order-level": "",
            "only-endpoint": False
        }
        template=dbc.Row([
                dbc.Col([
                    dbc.Input(
                        type="text",
                        id="search",
                        placeholder="Buscar por coincidencia",
                    ),
                ],
                width=3),
                dbc.Col([
                    dbc.Button("Ver Hijos", id="trigger-by-classe", color="primary", className="me-1", n_clicks=0)
                ], width=1),
                dbc.Col([
                    dbc.Button("Ver Aspectos", id="open-modal", color="primary", className="me-1", n_clicks=0)
                ], width=1),
                dbc.Col([
                    dbc.Label("Orden de Niveles", html_for="example-email-grid"),
                    dbc.Button("Ascendente", outline=True, id="upward-button", color="primary", className="me-1"),
                    dbc.Button("Descendente", outline=True, id="downward-button", color="primary", className="me-1")
                ], width=6),
                dbc.Col([
                    dbc.Button("Solo Endpoints", id="is-endpoint-button", outline=True, color="primary", className="me-1")
                ], width=1),
                dcc.Store(id="selected-focus-classe", data= ""),
                dcc.Store(id="selected-focus-node", data= ""),
                dcc.Store(id="trigged-focus-classe", data= ""),
                dcc.Store(id="status-filters", data= init_status_filters),
                dcc.Store(id="status-level-order", data= None),
                dcc.Store(id="last-status-level-order", data= None),
            ])
        
        @app.callback(
            Output('modal-xl', 'is_open'),
            [Input('selected-focus-node', 'data'), Input('open-modal', 'n_clicks')],
            [State('modal-xl', 'is_open')]
        )
        def open_modal_with_node(focus_node, click_open, is_open):
            click = ctx.triggered_id
            if focus_node and click == "open-modal":
                return not is_open

            return is_open
        

        @app.callback(
            Output('trigged-focus-classe', 'data'),
            [Input('trigger-by-classe', 'n_clicks')],
            [State('selected-focus-classe', 'data')]
        )
        def set_focus_classe(click, selected):
            if selected != "" and click % 2 != 0:
                return selected
            return ""

        @app.callback(
            [Output('status-level-order', 'data'), Output('last-status-level-order', 'data')],
            [Input('upward-button', 'n_clicks'), Input('downward-button', 'n_clicks')],
            [State('last-status-level-order', 'data')]
        )
        def watch_status_level_order(click_upward, click_downward, last_click):
            new_click = ctx.triggered_id
            if new_click == 'upward-button':
                new_click =  True
            elif new_click == 'downward-button':
                new_click = False 
            if last_click == new_click:
                return [None, None]
            else:
                return [new_click, new_click]

        @app.callback(
            Output('status-filters', 'data'),
            [Input('trigged-focus-classe', 'data'), Input('search', 'value'), Input('status-level-order', 'data'), Input('is-endpoint-button', 'n_clicks')],
            [State('status-filters', 'data')]
        )
        def watch_update_for_status(filter_by, search, order_level, is_endpoint, status):
            update_status = status
            
            update_status['by-classe'] = filter_by

            update_status['search'] = search

            update_status['order-level'] = order_level

            if is_endpoint is not None:
                update_status['only-endpoint'] = (is_endpoint % 2) != 0
            else:
                update_status['only-endpoint'] = False

            return update_status

        return template

    def domain_table(self, app):
        template = html.Div([
            dash_table.DataTable(
                id='domain-table',
                columns=[
                    {"name": "ID", "id": "id"},
                    {"name": "Node", "id": "node"},
                    {"name": "Classe", "id": "classe"},
                    {"name": "Description", "id": "description"},
                    {"name": "Level", "id": "level"},
                    {"name": "Endpoint", "id": "is_endpoint"}
                ],
                data=self.df_dictionary.to_dict('records'),
                editable= True,
                row_selectable = 'single',
                style_table={'padding-bottom': '50px'},

            ),
            dcc.Store(id='master-domain-table', data=self.df_dictionary.to_dict('records'))
        ])

        @app.callback(
            [Output('selected-focus-classe', 'data'), Output('selected-focus-node', 'data')],
            [Input('domain-table', 'active_cell')],
            [State('selected-focus-classe', 'data'), State('selected-focus-node', 'data'), State('domain-table', 'data')]
        )
        def target_filter_with_classe(active_cell, classe, node, data):
            if active_cell:
                if active_cell['column_id'] == 'classe':
                    row_index = active_cell['row']
                    selected_row = data[row_index]
                    return [selected_row['classe'], node]
                if active_cell['column_id'] == 'node':
                    row_index = active_cell['row']
                    selected_row = data[row_index]
                    return [classe, selected_row['node']]

            return [classe, node]

        @app.callback(
            Output('domain-table', 'data'),
            [Input('status-filters', 'data')],
            [State('domain-table', 'data'), State('master-domain-table', 'data')]
        )
        def filter_data(status, data, master):
            if data is None:
                # Si no hay datos, devuelve el conjunto maestro como último recurso
                return master

            filtered_data = master.copy()  # Comienza con una copia de los datos originales

            # Filtro de búsqueda
            search = status.get('search')
            if search:
                search = search.lower()
                filtered_data = [row for row in filtered_data if
                                (row['classe'] and search in row['classe'].lower()) or
                                (row['node'] and search in row['node'].lower()) or
                                (row['description'] and search in row['description'].lower())]

            # Filtro por clase
            data_by_classe = status.get('by-classe')
            if data_by_classe != '':
                filtered_data = [row for row in filtered_data if row['classe'] == data_by_classe]

            # Ordenar por nivel
            order_level = status.get('order-level')
            if order_level is not None:
                reverse = not order_level  # True para ascendente, False para descendente
                filtered_data.sort(key=lambda x: x['level'], reverse=reverse)

            # Filtro de solo puntos finales
            only_endpoint = status.get('only-endpoint')
            if only_endpoint is not False:  # Asegúrate de comparar con False ya que None debería ser ignorado
                filtered_data = [row for row in filtered_data if row['is_endpoint'] == only_endpoint]

            return filtered_data  # Devuelve los datos filtrados o master si está vacío
                
        return template

    def render(self):
        template = html.Div([
            html.H1("Diccionario Ontológico", className="mb-4"),  # Margen abajo
            self.filter_bar(self.app),
            html.Div([
                self.domain_table(self.app),
            ], style={'margin-top': '20px', 'padding': '20px'}),  # Añade espacio arriba y padding
            self.aspect_modal(self.app),
        ], style={'padding': '10px'})
        return template

