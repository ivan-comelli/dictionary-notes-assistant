from dash import dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from Components.Dictionary.aspect_modal import AspectModal
from Components.table_utils import watch_save, update_data

class DomainDatatable:
    def __init__(self, app):
        self.init_data = pd.DataFrame({'id':[None], 'node':[None], 'classe':[None], 'description':[None], 'level':[None], 'is_endpoint':[None]})

        @app.callback(
            [Output('selected-focus-classe', 'data'), Output('selected-focus-node', 'data')],
            [Input('domain-table', 'active_cell')],
            [State('selected-focus-classe', 'data'), State('selected-focus-node', 'data'), State('domain-table', 'data')],
            prevent_initial_call=True)
        def watch_active_cell(active_cell, classe, node, data):
            if active_cell:
                if active_cell['column_id'] == 'classe':
                    row_index = active_cell['row']
                    selected_row = data[row_index]
                    return [selected_row['classe'], node]
                if active_cell['column_id'] == 'node':
                    row_index = active_cell['row']
                    selected_row = data[row_index]
                    return [selected_row['node'], selected_row['node']]

            return [classe, node]
       
        @app.callback(
                Output('commit-domain-datatable', 'data'),
                [Input('trigger-save-changes', 'n_clicks'), Input('interval-component', 'n_intervals')],
                [State('domain-table', 'data'), State('domain-table', 'active_cell')],
                prevent_initial_call=True)
        def call_to(click_save, n, datatable, active_cell):
            return watch_save(click_save, n, datatable, active_cell)
       
        @app.callback(
            Output('domain-table', 'data'),
            [Input('domain-datatable', 'data'), Input('trigger-remove-rows', 'n_clicks'), Input('domain-table', 'selected_rows'), Input('domain-table', 'data')],
            prevent_initial_call=True)
        def call_to(data, click_del, selected, current):
            return update_data(data, selected, current, 'domain-datatable')

        @app.callback(
            Output("domain-table", "dropdown"),
            Input('domain-datatable', 'data'),
            prevent_initial_call=True)
        def update_menu(data):
            df_datatable = pd.DataFrame(data)['node']
            df_datatable.replace(pd.NA, "", inplace=True)
            if not df_datatable.isnull().all():
                # Construir las opciones del dropdown solo si la columna no está vacía
                dropdown_options = [{"label": i, "value": i} for i in df_datatable.unique()]
            else:
                # En caso de que la columna "node" esté vacía, establecer las opciones del dropdown como una lista vacía
                dropdown_options = []   
  
            return {"classe": {
                        "options": dropdown_options
                    }}

    def render(self):
        template = html.Div([
            dash_table.DataTable(
                id='domain-table',
                columns=[
                    {"name": "ID", "id": "id"},
                    {"name": "Node", "id": "node"},
                    {"name": "Classe", "id": "classe", 'presentation': 'dropdown'},
                    {"name": "Description", "id": "description"},
                    {"name": "Level", "id": "level"},
                ],
                dropdown= {
                    "classe": {
                        "options": []
                    }
                },
                editable= True,
                row_selectable= 'multi',
                data=self.init_data.to_dict('records')
            )
        ]) 
        return template


