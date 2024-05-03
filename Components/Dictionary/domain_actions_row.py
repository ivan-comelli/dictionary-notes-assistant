from dash import dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from Components.Dictionary.aspect_modal import AspectModal
# ROW FILTER BAR FOR DICTIONARY TABLE
class DomainActionRow: 
    def __init__(self, app):
        @app.callback(
            Output('modal-xl', 'is_open'),
            [Input('selected-focus-node', 'data'), Input('open-modal', 'n_clicks')],
            [State('modal-xl', 'is_open')],
            prevent_initial_call=True)
        def open_modal_node(focus_node, click_open, is_open):
            click = ctx.triggered_id
            if focus_node and click == "open-modal":
                return not is_open
            return is_open

        @app.callback(
            Output('trigged-focus-classe', 'data'),
            [Input('trigger-by-classe', 'n_clicks')],
            [State('selected-focus-classe', 'data')],
            prevent_initial_call=True)
        def set_focus_classe(click, selected):
            if selected != "" and click % 2 != 0:
                return selected
            return ""

        @app.callback(
            [Output('status-level-order', 'data'), Output('last-status-level-order', 'data')],
            [Input('upward-button', 'n_clicks'), Input('downward-button', 'n_clicks')],
            [State('last-status-level-order', 'data')],
            prevent_initial_call=True)
        def watch_level_order(click_upward, click_downward, last_click):
            new_click = ctx.triggered_id
            if new_click == 'upward-button':
                new_click =  True
            elif new_click == 'downward-button':
                new_click = False 
            if last_click == new_click:
                return [None, None]
            else:
                return [new_click, new_click]

        @app.callback(
            Output('status-filters', 'data'),
            [Input('trigged-focus-classe', 'data'), Input('search', 'value'), Input('status-level-order', 'data'), Input('is-endpoint-button', 'n_clicks')],
            [State('status-filters', 'data')],
            prevent_initial_call=True)
        def watch_update(filter_by, search, order_level, is_endpoint, status):
            update_status = status
            
            update_status['by-classe'] = filter_by

            update_status['search'] = search

            update_status['order-level'] = order_level

            if is_endpoint is not None:
                update_status['only-endpoint'] = (is_endpoint % 2) != 0
            else:
                update_status['only-endpoint'] = False

            return update_status


    def render(self):
        init_status_filters = {
            "search": "",
            "by-classe": "",
            "order-level": "",
            "only-endpoint": False
        }
        template=html.Div([
            html.Div([
                dbc.Input(
                    type="text",
                    id="search",
                    placeholder="Buscar por coincidencia",
                ),
            ], className="left"),
            html.Div([
                dbc.Button(html.I(className="fa-solid fa-circle-nodes"), id="trigger-by-classe", color="primary", className="me-1", n_clicks=0),
                dbc.Button(html.I(className="fa-solid fa-arrow-up-right-from-square"), id="open-modal", color="primary", className="me-1", disabled=True, n_clicks=0),
            ], className="medium"),
            html.Div([
                    dbc.Label("Orden de Niveles", html_for="example-email-grid"),
                    dbc.Button(html.I(className="fa-solid fa-up-long"), outline=True, id="upward-button", color="primary", className="me-1"),
                    dbc.Button(html.I(className="fa-solid fa-down-long"), outline=True, id="downward-button", color="primary", className="me-1"),
            ], id="level-order"),
            html.Div([
                dbc.Button("Endpoints", id="is-endpoint-button", outline=True, color="primary", className="me-1"),
                dbc.Button(html.I(className="fa-solid fa-floppy-disk"), id="trigger-save-changes", className="btn btn-primary"),
                dbc.Button(html.I(className="fa-solid fa-trash"), id="trigger-remove-rows", className="btn btn-primary"),
            ], className="right"),           
            dcc.Store(id="trigged-focus-classe", data= ""),
            dcc.Store(id="status-level-order", data= None),
            dcc.Store(id="last-status-level-order", data= None),
        ], id="row-actions")

        return template