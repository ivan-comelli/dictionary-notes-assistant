                    dbc.Textarea(className="mb-3", placeholder="Ingresa el CSV Aqui"),
                    html.Div([
                        dbc.Button("Guarda los Cambios", color="primary", id="open-xl", n_clicks=0),
                    ], className="d-grid gap-2 col-6 mx-auto"),
# Me gustaria que tenga un selector tambien ya que puede ser el input en distintos formatos