""" from sqlalchemy.orm import Session
from geoalchemy2 import WKTElement
from ..models.nodes import Node as NodeModel
from ..schemas.nodes import NodeCreate, NodeResponse

def create_node(node: NodeCreate, db: Session) -> NodeResponse:
    geom = WKTElement(f'POINT({node.longitude} {node.latitude})', srid=4326)
    db_node = NodeModel(name=node.name, geom=geom)
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return NodeResponse(
        id=db_node.id,
        name=db_node.name,
        longitude=node.longitude,
        latitude=node.latitude
    )

def get_nodes(db: Session):
    nodes = db.query(NodeModel).all()
    node_list = []
    for node in nodes:
        geom = node.geom
        longitude = db.scalar(geom.ST_X())
        latitude = db.scalar(geom.ST_Y())
        node_list.append(NodeResponse(
            id=node.id,
            name=node.name,
            longitude=longitude,
            latitude=latitude
        ))
    return node_list """

