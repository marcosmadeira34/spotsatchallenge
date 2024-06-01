from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from sqlalchemy.orm import declarative_base


Base = declarative_base()

# Definindo a classe Graph
class Graph(Base):
    __tablename__ = "graphs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    nodes = relationship("Node", back_populates="graph")
    edges = relationship("Edge", back_populates="graph")


# Definindo modelos nodes
class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    graph_id = Column(Integer, ForeignKey("graphs.id"))
    geom = Column(Geometry(geometry_type="POINT", srid=4326))

    graph = relationship("Graph", back_populates="nodes")
    edges_from = relationship("Edge", foreign_keys="[Edge.from_node_name]", back_populates="from_node")
    edges_to = relationship("Edge", foreign_keys="[Edge.to_node_name]", back_populates="to_node")


# Definindo modelos edges(arestas)
class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, index=True)
    graph_id = Column(Integer, ForeignKey("graphs.id"))
    from_node_name = Column(String, ForeignKey("nodes.name"))
    to_node_name = Column(String, ForeignKey("nodes.name"))
    weight = Column(Integer)

    graph = relationship("Graph", back_populates="edges")
    from_node = relationship("Node", foreign_keys=[from_node_name], back_populates="edges_from")
    to_node = relationship("Node", foreign_keys=[to_node_name], back_populates="edges_to")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    
    