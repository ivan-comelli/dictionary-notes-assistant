#import all hooks
from Store.use_dictionary import UseDiccionary
from Store.use_daily import UseDaily
from dash import dash, html, dcc


class Store:
    def __init__(self, app):
        self.use_dictionary = UseDiccionary(app)
        self.use_daily = UseDaily(app)

    def render(self):
        return (dcc.Location(id="url"), dcc.Store(id='isSaved', data={'status': False}), *self.use_dictionary.render(), *self.use_daily.render())
        
