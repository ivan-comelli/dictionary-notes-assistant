# Importamos las librerías necesarias
import dash
from dash import html, dcc
import plotly.graph_objects as go

class DictionaryChart:
    def __init__(self, app, df_dictionary):
        self.app = app
        expected_columns = ['node', 'classe', 'description', 'level', 'is_endpoint']
        if not all(column in df_dictionary.columns for column in expected_columns):
            raise ValueError("El DataFrame no contiene las columnas esperadas.")
        self.df_dictionary = df_dictionary

    def build_chart(self):
        figure=go.Figure(
            data=[go.Sunburst(
                ids=self.df_dictionary['node'],
                labels=self.df_dictionary['node'],
                parents=self.df_dictionary['classe']
            )
            ],
            layout=go.Layout(
                margin=dict(t=0, l=0, r=0, b=0)  # Ajusta los márgenes si es necesario
            )
        )
        return figure
    
    def render(self):
        return dcc.Graph(
            id='sunburst_chart',
            figure=self.build_chart(),
            style={'height': '100%', 'width': '100%'},  # Asegura que el gráfico se expanda para llenar el contenedor
            config={
                'autosizable': True,
                'responsive': True
            }
        )
