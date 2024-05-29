""" from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Edge(Base):
    __tablename__ = "edges"
    id = Column(Integer, primary_key=True, index=True)
    start_node_id = Column(Integer)
    end_node_id = Column(Integer)
    geom = Column(Geometry(geometry_type="LINESTRING", srid=4326))

    __table_args__ = {"schema": "public"} """