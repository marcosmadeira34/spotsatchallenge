""" from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    geom = Column(Geometry("POINT", srid=4326)) 

    __table_args__ = {"schema":"public"}
 """
