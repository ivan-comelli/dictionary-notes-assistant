html.Div([
    status_save,
    html.H1("Registro de Notas"),
    dash_table.DataTable(
        id='notes-table',
        columns=[
            {'name': 'ID', 'id': 'id'},
            {'name': 'Fecha', 'id': 'fecha'},
            {'name': 'Nota', 'id': 'nota'}
        ],
        data=pd.DataFrame(note_data).to_dict('records'),
        editable=True,
        row_deletable=True
    )
])