""" from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from shapely.geometry import LineString

from ..models.edges import Edge as EdgeModel
from ..schemas.edges import EdgeCreate

def create_edge(edge: EdgeCreate, db: Session):
    coordinates = ", ".join([f"{lon} {lat}" for lon , lat in edge.coordinates])
    geom = f'LINESTRING({coordinates})'
    db_edge = EdgeModel(start_node_id=edge.start_node_id,
                         end_node_id=edge.end_node_id,
                         geom=geom)
    db.add(db_edge)
    db.commit()
    db.refresh(db_edge)
    return db_edge

def get_edges(db: Session):
    return db.query(EdgeModel).all() """