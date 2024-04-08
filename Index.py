import dash
from dash import html, dash_table, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import os
from datetime import datetime
import dash_bootstrap_components as dbc


from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, subqueryload
from sqlalchemy.ext.declarative import declarative_base

sprint_data = [{'id': '', 'sprint': '', 'tarea': '', 'descripcion': ''}]
note_data = [{'id': '', 'fecha': '', 'nota': ''}]
deleted_sprint_rows = [{'id': '', 'sprint': '', 'tarea': '', 'descripcion': ''}]
deleted_note_rows = [{'id': '', 'fecha': '', 'nota': ''}]

###     MODELOS     ###
Base = declarative_base()

class Domain(Base):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    classe = Column(String)
    subclass = Column(String)
    description = Column(String)
    aspects = relationship("Aspect", back_populates="domain")

class Aspect(Base):
    __tablename__ = 'aspects'

    id = Column(Integer, primary_key=True)
    name = Column(String)  # Agrega esta línea para definir la columna 'name'
    type = Column(String)
    domain_id = Column(Integer, ForeignKey('domains.id'))
    domain = relationship("Domain", back_populates="aspects")

class SprintWork(Base):
    __tablename__ = 'sprint_work'

    id = Column(Integer, primary_key=True)
    sprint = Column(String)
    tarea = Column(String)
    descripcion = Column(String)

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    nota = Column(String)


###     CONEXION Y MIGRACIONES      ###

engine = create_engine('sqlite:///Database/data.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


###     SYNC CSV DATA       ###
"""
csv_files = [os.path.join('Database', file) for file in os.listdir('Database') if file.endswith('.csv') and ('_classes' in file or '_aspects' in file)]
for file in csv_files:
    table_name = 'domains' if '_classes' in file else 'aspects'
    print(file)
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        unique_col = 'name'
        Model = Domain if table_name == 'domains' else Aspect
        # Verificar si ya existe el registro en la base de datos
        existing_record = session.query(Model).filter(getattr(Model, unique_col) == row[unique_col]).first()
        # Si no existe, agregarlo a la base de datos
        if not existing_record:
            new_record = Model(**row)
            session.add(new_record)
            session.commit()
            print(f"Insertado en {table_name}: {row}")
"""
###     MERGE TABLES FOR DICTIONARY DATATABLE       ###

# Obtener todos los dominios con sus aspectos relacionados
domains_with_aspects = session.query(Domain).options(
    subqueryload(Domain.aspects)).all()
data = []
for domain in domains_with_aspects:
    domain_data = {
        'name': domain.name,
        'classe': domain.classe,
        'subclasse': domain.subclass,
        'description': domain.description
    }
    aspect_names = []
    for aspect in domain.aspects:
        aspect_names.append(aspect.name)
    domain_data['aspecto_productivo'] = ', '.join(aspect_names)
    data.append(domain_data)
df_dictionary = pd.DataFrame(data)

###     APP DASH LAYOUT     ###

app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

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
                dbc.NavLink("Libro de Notas", href="/notebook", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

status_save = html.Div([
    dbc.Spinner(color="primary", type="grow"),
    html.H3("Guardado")
])

daily_view = html.Div([
    status_save,
    html.H1("Registro de Sprint de Trabajo"),
    html.P("Los sprint le dan contexto a las notas, por eso tienen que ser estrictos en cuanto a los registros de las notas considerando el planteo del contexto. Llegado el caso de una excepcion, ser detallado en el registro de la nota y si es recurrente en el tema, planteo de agregar cambios en sprint o crear otra instancia"),
    dash_table.DataTable(
        id='sprint-table',
        columns=[
            {'name': 'ID', 'id': 'id'},
            {'name': 'Sprint', 'id': 'sprint'},
            {'name': 'Tarea', 'id': 'tarea'},
            {'name': 'Descripción', 'id': 'descripcion'}
        ],
        data=pd.DataFrame(sprint_data).to_dict('records'),
        editable=True,
        row_deletable=True,
        style_table={'padding-bottom': '50px', "height": "60vh", "overflowY": "auto"},
    ),
    dbc.InputGroup(
        [
            dbc.Input(id="input-group-button-input", placeholder="Escribe tu Nota..."),
            dbc.Button("Guardar", id="input-group-button", n_clicks=0),
        ]
    ),
    dcc.Store(id='isSaved', data={'status': False})
])

dictionary_view = html.Div([
    status_save,
    dbc.Card(
        [
            dbc.CardHeader(
                dbc.Tabs(
                    [
                        dbc.Tab(label="Ver Tabla", tab_id="tab-1"),
                        dbc.Tab(label="Ver Arbol", tab_id="tab-2"),
                        dbc.Tab(label="Commits", tab_id="tab-3"),
                        dbc.Tab(label="Branchs", tab_id="tab-4"),
                    ],
                    id="card-tabs",
                    active_tab="tab-1",
                )
            ),
            dbc.CardBody(html.P(id="card-content", className="card-text"), style={"height": "80vh", "overflowY": "auto"}),
        ]
    ),
    html.P("El diccionario es importante para poder entender descriptivamnete y categoricamente areas del conocimiento con atributos en sus ramas finales. Con este recurso se puede lograr tokenizar por entidades un texto y asi desglozar en la informacion manteniendo el contexto de la misma."),
])

notebook_view = html.Div([
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

domain_section = html.Div([
    html.H1("Información de Marketing"),
    dash_table.DataTable(
        id='merged-marketing-table',
        columns=[
            {"name": "Name", "id": "name"},
            {"name": "Classe", "id": "classe"},
            {"name": "Subclasse", "id": "subclass"},
            {"name": "Description", "id": "description"},
            {"name": "Aspecto_Productivo", "id": "aspecto_productivo"}
        ],
        data=df_dictionary.to_dict('records'),
        style_table={'padding-bottom': '50px', 'height': '50vh'}
    ),
    dbc.Textarea(className="mb-3", placeholder="Ingresa el CSV Aqui"),
    html.Div([
                dbc.Button("Siguiente Paso Ante de Unir", color="primary", id="open-xl", n_clicks=0),
            ], className="d-grid gap-2 col-6 mx-auto"),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Cada cosa en su lugar")),
            dbc.ModalBody("An extra large modal."),
            html.Div([
                html.Label("Elegi una Rama: "),
                dbc.Select(
                    id="select",
                    options=[
                        {"label": "Marketing", "value": "1"},
                        {"label": "Programacion", "value": "2"},
                        {"label": "Disabled option", "value": "3", "disabled": True},
                    ],
                ),
            ]),
        ],
        id="modal-xl",
        size="xl",
        is_open=False,
    ),
])

@app.callback(
    Output("modal-xl", "is_open"),
    Input("open-xl", "n_clicks"),
    State("modal-xl", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("card-content", "children"), 
    [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == "tab-1":
        return domain_section
    elif active_tab == "tab-2":
        return html.P("Contenido de la Tab 2")
    else:
        return "No hay contenido disponible"


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return daily_view
    elif pathname == "/dictionary":
        return dictionary_view
    elif pathname == "/notebook":
        return notebook_view
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

"""
app.layout = html.Div([
    
    
    html.Button('Agregar Nota', id='add-note-button', n_clicks=0),
    html.Button('Guardar', id='save-button', n_clicks=0),
    dcc.Store(id='prev-sprint-data', data=pd.DataFrame(sprint_data).to_dict('records'),),
    dcc.Store(id='prev-note-data', data=pd.DataFrame(note_data).to_dict('records'),),
    html.Div(id='dummy-div', style={'display': 'none'})
])

###     CALLBACK MANAGEDATA     ###

@app.callback(
    [Output('sprint-table', 'data'), Output('notes-table', 'data'), Output('prev-sprint-data', 'data'), Output('prev-note-data', 'data')],
    [Input('add-sprint-button', 'n_clicks'), Input('add-note-button', 'n_clicks'),
     Input('save-button', 'n_clicks')],
    [State('sprint-table', 'data'), State('notes-table', 'data'),
     State('prev-sprint-data', 'data'), State('prev-note-data', 'data')]
)
def manage_data(add_sprint_clicks, add_note_clicks, save_clicks, sprint_data, note_data, prev_sprint_data, prev_note_data):
    ctx = dash.callback_context

    ###     CONVERSIÓN A DATAFRAMES     ###
    sprint_data = pd.DataFrame(sprint_data)
    note_data = pd.DataFrame(note_data)
    prev_sprint_data = pd.DataFrame(prev_sprint_data)
    prev_note_data = pd.DataFrame(prev_note_data)

    ###     UPDATE ALL DATA     ###
    
    if not ctx.triggered:
        try:
            sprint_data = pd.read_sql(session.query(SprintWork).statement, session.bind)
            note_data = pd.read_sql(session.query(Note).statement, session.bind)
        except Exception as e:
            print("Error al inicializar los datos de la base de datos:", e)
        return [sprint_data.to_dict('records'), note_data.to_dict('records'), sprint_data.to_dict('records'), note_data.to_dict('records')]
            
    ###     CHECK DELETED ROWS      ###
    
    deleted_sprint_rows = []
    deleted_note_rows = []
    for index, row in prev_sprint_data.iterrows():
        if row['id'] not in sprint_data['id'].values:
            deleted_sprint_rows.append(row.to_dict())
    for index, row in prev_note_data.iterrows():
        if row['id'] not in note_data['id'].values:
            deleted_note_rows.append(row.to_dict())
    prev_sprint_data = sprint_data.copy()
    prev_note_data = note_data.copy()
    prev_sprint_data.reset_index(drop=True, inplace=True)
    prev_note_data.reset_index(drop=True, inplace=True)

    ###     SERIAL TRIGGERS      ###

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    ###     ADDSPRINT       ###

    if triggered_id == 'add-sprint-button' and add_sprint_clicks > 0:
        try:
            new_sprint_row = pd.DataFrame({'id': [''], 'sprint': [''], 'tarea': [''], 'descripcion': ['']})
            sprint_data = pd.concat([sprint_data, new_sprint_row], ignore_index=True)
        except Exception as e:
            print("Error al agregar fila de sprint:", e)

    ###     ADDNOTE     ###

    elif triggered_id == 'add-note-button' and add_note_clicks > 0:
        try:
            new_note_row = pd.DataFrame({'id': [''], 'fecha': [''], 'nota': ['']})
            note_data = pd.concat([note_data, new_note_row], ignore_index=True)
        except Exception as e:
            print("Error al agregar fila de nota:", e)

    ###     SAVE        ###

    elif triggered_id == 'save-button' and save_clicks > 0:
        try:
            for row in deleted_sprint_rows:
                sprint_id = row['id']
                session.query(SprintWork).filter(SprintWork.id == sprint_id).delete()
            for row in deleted_note_rows:
                note_id = row['id']
                session.query(Note).filter(Note.id == note_id).delete()

            for index, row in sprint_data.iterrows():
                if row['id'] != '': 
                    session.query(SprintWork).filter(SprintWork.id == row['id']).update(row)
                else: 
                    row['id'] = None
                    register = SprintWork(**row)
                    session.add(register)
                    session.flush()
                    session.refresh(register)
                    sprint_data.at[index, 'id'] = register.id

            for index, row in note_data.iterrows():
                if row['id'] != '':
                    session.query(Note).filter(Note.id == row['id']).update({'nota': row['nota']})
                else: 
                    row['id'] = None
                    row['fecha'] = datetime.now()
                    register = Note(**row)
                    session.add(register)
                    session.flush()
                    session.refresh(register)
                    note_data.at[index, 'id'] = register.id

            session.commit()

            deleted_sprint_rows = [{'id': '', 'sprint': '', 'tarea': '', 'descripcion': ''}]
            deleted_note_rows = [{'id': '', 'fecha': '', 'nota': ''}]

        except Exception as e:
            print("Error al guardar datos en la base de datos:", e)

    return [sprint_data.to_dict('records'), note_data.to_dict('records'), prev_sprint_data.to_dict('records'), prev_note_data.to_dict('records')]
"""

if __name__ == '__main__':
    app.run_server(debug=True)