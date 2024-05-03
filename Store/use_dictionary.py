from dash import dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from Components.Dictionary.aspect_modal import AspectModal
from Data.domain import mechanics
from Services.dataDictionary import set_domain, get_domain
from Store.utils import get_changes_to_commit

class UseDiccionary:
    def __init__(self, app):
        self.master_domain = get_domain()
        @app.callback(
            Output('master-domain', 'data'),
            [Input('commit-domain-datatable', 'data'), Input('url', 'pathname')],
            [State('domain-datatable', 'data')]
        )
        def push_changes(commit_data, path, domain_data):
            if ctx.triggered_id != "url":
                if commit_data is None or domain_data is None:
                    return dash.no_update
                [upd_row, del_row] = get_changes_to_commit(commit_data, domain_data)
                set_domain(upd_row, del_row)
            self.master_domain = get_domain()
            self.master_domain.loc[len(self.master_domain)] = [pd.NA] * len(self.master_domain.columns)
            return self.master_domain.to_dict('records')

        @app.callback(
            Output('domain-datatable', 'data'),
            [Input('status-filters', 'data'), Input('master-domain', 'data')],
            [State('domain-datatable', 'data')])
        def set_datatable(status, new_data, current_data):
            filtered_data = pd.DataFrame(new_data).copy()
            search = status.get('search', '')
            if search is not None:
                search = search.lower()
            else:
                search = ''
            filtered_data = filtered_data[
                ((filtered_data['classe'].astype(str).str.lower().str.contains(search)) |
                (filtered_data['node'].astype(str).str.lower().str.contains(search)) |
                (filtered_data['description'].astype(str).str.lower().str.contains(search)))
            ]
            data_by_classe = status.get('by-classe')
            if data_by_classe:
                filtered_data = filtered_data[filtered_data['classe'] == data_by_classe]
            order_level = status.get('order-level')
            if order_level is not None:
                reverse = not order_level  
                filtered_data = filtered_data.sort_values(by='level', ascending=reverse)
            only_endpoint = status.get('only-endpoint', False)
            if only_endpoint is not False:
                filtered_data = filtered_data[filtered_data['is_endpoint'] == only_endpoint]
            if new_data != current_data:
                return new_data
            return filtered_data.to_dict('records')

    def render(self):
        template = (
            dcc.Store("commit-domain-datatable"),
            dcc.Store("domain-datatable"),
            dcc.Store("master-domain", data=self.master_domain.to_dict('records')),
            dcc.Store("selected-focus-node"),
            dcc.Store("selected-focus-classe"),
            dcc.Store("status-filters", data= {
                "search": "",
                "by-classe": "",
                "order-level": "",
                "only-endpoint": False
            })
        )

        return template