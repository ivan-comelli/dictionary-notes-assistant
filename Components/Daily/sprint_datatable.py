from dash import dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from Components.table_utils import update_data, watch_save

class SprintDatatable:
    def __init__(self, app):
        self.init_data = pd.DataFrame({'id':[None], 'sprint':[None], 'task':[None], 'description':[None]})
        
        @app.callback(
            Output("sprint-table", "data"),
            [Input("sprint-table", "data"), Input('trigger-remove-rows', 'n_clicks'), Input('sprint-table', 'selected_rows'), Input("sprint-datatable", "data")]
        )
        def call_to(current, del_clicks, selected, new_data):
            print(new_data)
            return update_data(new_data, selected, current, 'sprint-datatable')
        
        @app.callback(
            Output("commit-sprint-datatable", "data"),
            [Input('trigger-save-changes', 'n_clicks'), Input('interval-component', 'n_intervals')],
            [State('sprint-table', 'data'), State('sprint-table', 'active_cell')]
        )
        def call_to(click_save, n, datatable, active_cell):
            return watch_save(click_save, n, datatable, active_cell)

    def render(self):
        template = dash_table.DataTable(
            id='sprint-table',
            columns=[
                {'name': 'ID', 'id': 'id'},
                {'name': 'Sprint', 'id': 'sprint'},
                {'name': 'Tarea', 'id': 'tarea'},
                {'name': 'Descripción', 'id': 'descripcion'}
            ],
            editable=True,
            row_selectable= 'multi',
            data=self.init_data.to_dict('records')
        )

        return template