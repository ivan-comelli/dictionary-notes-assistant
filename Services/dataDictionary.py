from models import Base  # Importa la clase Base desde tu módulo models
import pandas as pd
# Importa todos tus modelos para que SQLAlchemy pueda crear las tablas
from models import Domain, Aspect, SprintWork, Note
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

# Crear una sesión para interactuar con la base de datos
def set_domain(modificadas, eliminadas):
    try:
        for fila in modificadas:
            item = session.query(Domain).filter(Domain.id == fila['id']).first()
            domain_ref = session.query(Domain).filter(Domain.node == fila['classe']).first()
            new_data = {
                'id': fila['id'],
                'node': fila['node'],
                'classe_id': domain_ref.id if domain_ref is not None else None,
                'description': fila['description'],
                'level': fila['level'],
            }
            if item is None:
                new_data.pop('id')
                new_domain = Domain(**new_data)
                session.add(new_domain)
            else:
                item.node = new_data['node']
                item.classe_id = new_data['classe_id']
                item.description = new_data['description']
                item.level = new_data['level']
        
        # Eliminar las filas que fueron eliminadas
        for fila in eliminadas:
            id_eliminar = fila['id']
            session.query(Domain).filter(Domain.id == id_eliminar).delete()

        # Confirmar los cambios en la base de datos
        session.commit()

        print("Cambios realizados con éxito")

    except Exception as e:
        # Manejar la excepción e imprimir un mensaje de error
        print("Error al realizar cambios:", str(e))

    finally:
        # Cerrar la sesión
        session.close()

def get_domain():
    try:
        # Obtener los datos de la tabla Domain
        domain_data = session.query(Domain).all()

        # Si no hay datos, retornar las columnas existentes con valores vacíos
        columns = ['id', 'node', 'classe', 'description', 'level', 'is_endpoint']

        # Crear el DataFrame con columnas vacías
        if not domain_data:
            return pd.DataFrame(columns=columns)
  
        domain_formateado = []
        for row in domain_data:
            domain_formateado.append({
                'id': row.id,
                'node': row.node,
                'classe': row.classe.node if row.classe is not None else "",
                'description': row.description,
                'level': row.level,
                'is_endpoint': True
            })
        return pd.DataFrame(domain_formateado)

    except Exception as e:
        # Manejar la excepción e imprimir un mensaje de error
        print("Error al obtener datos de dominio:", str(e))
        return []
