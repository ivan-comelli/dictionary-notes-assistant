from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import Enum

'''
    El name de Aspectos necesita un select dinamico para los registros a diferencia del type que es fijo

'''

Base = declarative_base()
#las clases son branch, name es el nodo y estos mismos se pueden relacionar a si mismo. Los endpoint se relacionan con aspectos

class AspectType(enum.Enum):
    KEY = "Aspectos Clave"
    PRODUCTIVE = "Aspectos Productivo"

domain_aspect_association = Table(
    'domain_aspect_association',
    Base.metadata,
    Column('domain_id', Integer, ForeignKey('domains.id')),
    Column('aspect_id', Integer, ForeignKey('aspects.id'))
)

class Domain(Base):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    node = Column(String)
    classe_id = Column(Integer, ForeignKey('domains.id'))  # La columna que almacena el id de la clase padre

    # Definir la relación 'classe'
    classe = relationship("Domain", remote_side=[id], backref='parent')  # Relación consigo misma

    description = Column(String)
    level = Column(Integer)
    aspects = relationship("Aspect",
                           secondary=domain_aspect_association,
                           back_populates="domains")

class Aspect(Base):
    __tablename__ = 'aspects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(Enum(AspectType))
    domains = relationship("Domain",
                           secondary=domain_aspect_association,
                           back_populates="aspects")

class SprintWork(Base):
    __tablename__ = 'sprint_work'

    id = Column(Integer, primary_key=True)
    sprint = Column(String)
    task = Column(String)
    description = Column(String)

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    nota = Column(String)
