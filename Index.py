import dash
from dash import html, dash_table, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import os
from datetime import datetime

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

app = dash.Dash(__name__)
app.layout = html.Div([
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
        data=df_dictionary.to_dict('records')
    ),
    html.Label("Ingrese el contenido CSV:"),
    dcc.Textarea(
        id='csv-input',
        placeholder='Ingrese el contenido CSV aquí...',
        style={'width': '100%', 'height': 200},
    ),
    html.Label("Mensaje de Commit:"),
    dcc.Input(id='commit-message', type='text', placeholder='Describa los cambios...'),
    html.Button('Commit', id='commit-button'),
    html.Label("Crear Nueva Rama:"),
    dcc.Input(id='new-branch-name', type='text', placeholder='Nombre de la nueva rama...'),
    html.Button('Crear Rama', id='create-branch-button'),
    html.Label("Seleccionar Rama:"),
    dcc.Dropdown(id='branch-selector', options=[{'label': 'main', 'value': 'main'}]),
    html.Label("Historial de Commits:"),
    dash_table.DataTable(id='commits-table'),
    html.Label("Restaurar Versión:"),
    dcc.Dropdown(id='version-selector', options=[]),
    html.Button('Restaurar Versión', id='restore-version-button'),
    html.Hr(),
    html.H1("Registro de Sprint de Trabajo"),
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
        row_deletable=True
    ),
    html.Button('Agregar Registro de Sprint de Trabajo', id='add-sprint-button', n_clicks=0),
    html.Hr(),
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
    ),
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


if __name__ == '__main__':
    app.run_server(debug=True)