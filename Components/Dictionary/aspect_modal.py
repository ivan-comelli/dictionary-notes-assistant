from dash import dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd

class AspectModal:
    def __init__(self, app):
        self.app = app

    def render(self, app):
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
    