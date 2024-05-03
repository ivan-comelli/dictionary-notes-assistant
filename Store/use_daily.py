from dash import dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from Services.dataSprint import set_sprint, get_sprint
from Store.utils import get_changes_to_commit

class UseDaily: 
    def __init__(self, app):
        @app.callback(
            Output("master-sprint", "data"),
            [Input("commit-sprint-datatable", "data"), Input('url', 'pathname')],
            [State("sprint-datatable", "data")]
        )
        def push_change(commit_data, path, current):
            if ctx.triggered_id != "url":
                print(current)
                if commit_data is None or current is None:
                    # Si uno de los datos es None, no se pueden hacer comparaciones, entonces se retorna algo adecuado
                    return dash.no_update
                
                [upd_row, del_row] = get_changes_to_commit(commit_data, current)
                set_sprint(upd_row, del_row)
            new_data = get_sprint()
            if new_data == []:
                new_data = pd.DataFrame(columns=["id", "sprint", "task", "description"])  # Inicializar con columnas vacías
            new_data.loc[len(new_data)] = [pd.NA] * len(new_data.columns)
            return new_data.to_dict("records")

        @app.callback(
            Output('sprint-datatable', 'data'),
            [Input('master-sprint', 'data')],
            [State('sprint-datatable', 'data')])
        def set_datatable(master, origin):
            return master


    def render(self):
        template = (
            dcc.Store("commit-sprint-datatable"),
            dcc.Store("master-sprint"),
            dcc.Store("sprint-datatable")
        )
        
        return template