""" from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.edges import EdgeCreate, Edge
from ..controllers.edges import create_edge, get_edges

router = APIRouter()

@router.post("/", response_model=Edge)
def create_edge_endpoint(edge: EdgeCreate, db: Session = Depends(get_db)):
    return create_edge(edge, db)

@router.get("/", response_model=List[Edge])
def get_edges_endpoint(db: Session = Depends(get_db)):
    return get_edges(db)
 """