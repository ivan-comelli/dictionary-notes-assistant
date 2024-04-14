import dash_bootstrap_components as dbc
from dash import html

class BidirectionalListItem:
    @staticmethod
    def create(name, value, is_selected, item_index):
        return dbc.ListGroupItem([
            html.Div(
                [
                    html.H5(name, className="mb-1"),
                    dbc.Button("+", outline=True, color="success", className="me-1", 
                               style=None if is_selected else {'display': 'none'}, 
                               id={'type': 'increment-button', 'index': item_index}),
                    dbc.Button("-", outline=True, color="warning", className="me-1", 
                               style=None if not is_selected else {'display': 'none'}, 
                               id={'type': 'decrement-button', 'index': item_index}),
                ],
                className="d-flex w-100 justify-content-between",
            ),
            html.P("Cambio", className="mb-1"),
            html.Small(value, className="text-muted"),
        ])
