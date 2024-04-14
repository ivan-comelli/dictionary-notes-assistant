from dash import html
import dash_bootstrap_components as dbc
from ..Components.header_status_save import status_save  # Asegúrate de que la ruta de importación sea correcta

def create_dictionary_view():
    return html.Div([
        status_save.create(),
        dbc.Card(
            [
                dbc.CardHeader(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Ver Tabla", tab_id="tab-1"),
                            dbc.Tab(label="Ver Arbol", tab_id="tab-2"),
                            dbc.Tab(label="Versiones", tab_id="tab-3"),
                        ],
                        id="card-tabs",
                        active_tab="tab-1",
                    )
                ),
                dbc.CardBody(html.P(id="card-content", className="card-text"), style={"height": "80vh", "overflowY": "auto"}),
            ]
        ),
        html.P("El diccionario es importante para poder entender descriptivamente y categoricamente áreas del conocimiento con atributos en sus ramas finales. Con este recurso se puede lograr tokenizar por entidades un texto y así desglosar en la información manteniendo el contexto de la misma."),
    ])

dbc.Textarea(className="mb-3", placeholder="Ingresa el CSV Aqui"),
            html.Div([
                        dbc.Button("Guarda los Cambios", color="primary", id="open-xl", n_clicks=0),
                    ], className="d-grid gap-2 col-6 mx-auto"),