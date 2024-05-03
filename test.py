from dash import Dash, html, dcc, Input, Output, State, callback, exceptions, ctx
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc
import pandas as pd
from Components.Dictionary.domain_datatable import DomainDatatable
from Components.Dictionary.domain_sunburst_chart import DictionaryChart
from Store.use_dictionary import UseDiccionary
from Components.Dictionary.domain_actions_row import ActionRow

app = Dash(external_stylesheets=[dbc.themes.CERULEAN], suppress_callback_exceptions=True)

use_dictionary_store = UseDiccionary(app)
dictionary_table_component = DomainDatatable(app)
action_row_component = ActionRow(app)
dictionary_chart_component = DictionaryChart(app)
app.layout = html.Div([ 
    use_dictionary_store.render(),
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            action_row_component.render(),
            dictionary_table_component.render()
        ], style={'flex': '1', 'padding': '10px'}),
        html.Div([
            dictionary_chart_component.render()
        ], style={'flex': '1', 'padding': '10px'})
    ], id='Container')
], style={'display': 'flex', 'flex-direction': 'column'})

if __name__ == '__main__':
    app.run_server(debug=True)
