from models import Base  # Importa la clase Base desde tu módulo models
import pandas as pd
# Importa todos tus modelos para que SQLAlchemy pueda crear las tablas
from models import SprintWork, Aspect, SprintWork, Note
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Crear una instancia de motor para conectarse a la base de datos
engine = create_engine('sqlite:///Database/data.db', echo=True)  # Cambia 'sqlite:///example.db' con tu URL de conexión
Session = sessionmaker(bind=engine)
session = Session()
# Crear una clase base para definir modelos
try:
    # Crea todas las tablas definidas en los modelos
    #Base.metadata.create_all(engine)
    print("Migraciones realizadas con éxito")
except Exception as e:
    print("Error al realizar migraciones:", str(e))
finally:
    # Cierra la sesión
    session.close()

def set_sprint(modificadas, eliminadas):
    print("AGREGARRRRRRRRRR")
    try:
        for fila in modificadas:
            item = session.query(SprintWork).filter(SprintWork.id == fila['id']).first()
            new_data = {
                'id': fila['id'],
                'sprint': fila['node'],
                'task': fila['task'],
                'description': fila['description'],
            }
            if item is None:
                new_data.pop('id')
                new_domain = SprintWork(**new_data)
                session.add(new_domain)
            else:
                item.sprint = new_data['sprint']
                item.task = new_data['task']
                item.description = new_data['description']
        
        # Eliminar las filas que fueron eliminadas
        for fila in eliminadas:
            id_eliminar = fila['id']
            session.query(SprintWork).filter(SprintWork.id == id_eliminar).delete()

        # Confirmar los cambios en la base de datos
        session.commit()

        print("Cambios realizados con éxito")

    except Exception as e:
        # Manejar la excepción e imprimir un mensaje de error
        print("Error al realizar cambios:", str(e))

    finally:
        # Cerrar la sesión
        session.close()

def get_sprint():
    try:
        # Obtener los datos de la tabla SprintWork
        sprint_data = session.query(SprintWork).all()

        # Si no hay datos, retornar las columnas existentes con valores vacíos
        columns = ['id', 'sprint', 'task', 'description']

        # Crear el DataFrame con columnas vacías
        if not sprint_data:
            return pd.DataFrame(columns=columns)
  
        sprint_formateado = []
        for row in sprint_data:
            sprint_formateado.append({
                'id': row.id,
                'sprint': row.sprint,
                'task': row.task,
                'description': row.description,
            })
        return pd.DataFrame(sprint_formateado)

    except Exception as e:
        # Manejar la excepción e imprimir un mensaje de error
        print("Error al obtener datos de dominio:", str(e))
        return []
