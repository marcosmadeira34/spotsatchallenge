""" from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.nodes import NodeCreate, NodeResponse
from ..controllers.nodes import create_node, get_nodes

router = APIRouter()

@router.post("/", response_model=NodeResponse)
def create_node_endpoint(node: NodeCreate, db: Session = Depends(get_db)):
    return create_node(node, db)

@router.get("/", response_model=List[NodeResponse])
def get_nodes_endpoint(db: Session = Depends(get_db)):
    return get_nodes(db) """



