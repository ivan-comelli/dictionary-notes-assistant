import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
from dash.dependencies import Input, Output

class DictionaryChart:
    def __init__(self, app):
        self.expected_columns = ['node', 'classe', 'description', 'level', 'is_endpoint']
        @app.callback(
            Output("sunburst_chart", "figure"),
            [Input("domain-datatable", "data")],
            prevent_initial_call=True)
        def update(datatable):
            if datatable is not None:
                df_dictionary = pd.DataFrame(datatable)
            else: 
                df_dictionary = pd.DataFrame(columns=self.expected_columns)
            
            # Aquí debes rellenar ids, labels y parents con los datos de df_dictionary
            ids = df_dictionary['node']
            labels = df_dictionary['node']
            parents = df_dictionary['classe']  # Aquí asegúrate de ajustar según la estructura de tus datos
            
            # Actualiza los datos del gráfico
            updated_figure = go.Figure(
                data=[go.Sunburst(
                    ids=ids,
                    labels=labels,
                    parents=parents
                )],
                layout=go.Layout(
                    margin=dict(t=0, l=0, r=0, b=0)  # Ajusta los márgenes si es necesario
                )
            )
            
            return updated_figure
    
    def render(self):
        template = dcc.Graph(
            id='sunburst_chart',
            figure=go.Figure(
                data=[go.Sunburst(
                    ids=[],
                    labels=[],
                    parents=[]
                )
                ],
                layout=go.Layout(
                    margin=dict(t=0, l=0, r=0, b=0)  # Ajusta los márgenes si es necesario
                )
            ),
            config={
                'autosizable': True,
                'responsive': True
            }
        )
        
        return template
