from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from ..Components.header_status_save import status_save  # Ajusta la ruta de importación según la estructura de tu proyecto

def create_daily_view(sprint_data):
    return html.Div([
        status_save.create(),
        html.H1("Registro de Sprint de Trabajo"),
        html.P("Los sprint le dan contexto a las notas, por eso tienen que ser estrictos en cuanto a los registros de las notas considerando el planteo del contexto. Llegado el caso de una excepcion, ser detallado en el registro de la nota y si es recurrente en el tema, planteo de agregar cambios en sprint o crear otra instancia"),
        dash_table.DataTable(
            id='sprint-table',
            columns=[
                {'name': 'ID', 'id': 'id'},
                {'name': 'Sprint', 'id': 'sprint'},
                {'name': 'Tarea', 'id': 'tarea'},
                {'name': 'Descripción', 'id': 'descripcion'}
            ],
            data=pd.DataFrame(sprint_data).to_dict('records'),
            editable=True,
            row_deletable=True,
            style_table={'padding-bottom': '50px', "height": "60vh", "overflowY": "auto"},
        ),
        dbc.InputGroup(
            [
                dbc.Input(id="input-group-button-input", placeholder="Escribe tu Nota..."),
                dbc.Button("Guardar", id="input-group-button", n_clicks=0),
            ]
        ),
        dcc.Store(id='isSaved', data={'status': False})
    ])
