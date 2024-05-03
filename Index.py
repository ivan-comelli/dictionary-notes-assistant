import dash
from dash import html, dash_table, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import os
from datetime import datetime
import dash_bootstrap_components as dbc
from Views.manager_dictionary_view import DictionaryView
from Store.store import Store
from Views.daily_view import DailyView

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, subqueryload
from sqlalchemy.ext.declarative import declarative_base

sprint_data = [{'id': '', 'sprint': '', 'tarea': '', 'descripcion': ''}]
note_data = [{'id': '', 'fecha': '', 'nota': ''}]
deleted_sprint_rows = [{'id': '', 'sprint': '', 'tarea': '', 'descripcion': ''}]
deleted_note_rows = [{'id': '', 'fecha': '', 'nota': ''}]

sidebar = html.Div(
    [
        html.H2("Hola, Ivan", className="display-4"),
        html.Hr(),
        html.P(
            "Acción hoy, éxito mañana.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Diario", href="/", active="exact"),
                dbc.NavLink("Diccionario", href="/dictionary", active="exact"),
                dbc.NavLink("Libro de Notas", href="/notebook", disabled=True),
            ],
            vertical=True,
            pills=True,
        ),
    ], id="sidebar-nav-app")

if __name__ == '__main__':
    app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)
    content = html.Div(id="page-content")
    store = Store(app)
    app.layout = html.Div([
        dcc.Interval(
            id='interval-component',
            interval=50000,  # en milisegundos
            n_intervals=0
        ),
        *store.render(),
        sidebar,
        content], className="container")
    dictionary_view = DictionaryView(app)
    daily_view = DailyView(app)

    status_save = html.Div([
        dbc.Spinner(color="primary", type="grow"),
        html.H3("Guardado")
    ])

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return daily_view.render()
        elif pathname == "/dictionary":
            return dictionary_view.render()
        elif pathname == "/notebook":
            return html.H1("404: Not found", className="text-danger")
        # If the user tries to reach a different page, return a 404 message
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            className="p-3 bg-light rounded-3",
        )

    app.run_server(debug=True)
