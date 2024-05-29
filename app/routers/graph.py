# app/routers/graph.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import graph
from app.controllers.graph import create_graph, get_graph, get_routes, get_shortest_route, delete_graph_by_id, update_graph_by_id
from app.models.graph import Node, Edge, Graph

router = APIRouter()

@router.post("/", response_model=graph.GraphResponse)
def create_new_graph(graph: graph.GraphCreate, db: Session = Depends(get_db)):
    return create_graph(graph, db)

@router.get("/{graph_id}", response_model=graph.GraphResponse)
def read_graph(graph_id: int, db: Session = Depends(get_db)):
    graph = get_graph(graph_id, db)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph

# rota de deleção de grafo
@router.delete("/{graph_id}", response_model=graph.GraphDelete)
def remove_graph(graph_id: int, db: Session = Depends(get_db)):
    graph = delete_graph_by_id(graph_id, db)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph

@router.put("/{graph_id}", response_model=graph.GraphResponse)
def update_graph(graph_id: int, graph: graph.GraphCreate, db: Session = Depends(get_db)):
    delete_graph_by_id(graph_id, db)
    update_graph = create_graph(graph, db)    
    if not update_graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return update_graph


@router.get("/{graph_id}/routes", response_model=List[List[int]])
def find_routes(graph_id: int, from_node_id: int, to_node_id: int, max_stops: Optional[int] = None, db: Session = Depends(get_db)):
    return get_routes(graph_id, from_node_id, to_node_id, max_stops, db)

@router.get("/{graph_id}/shortest_route", response_model=List[int])
def find_shortest_route(graph_id: int, from_node_id: int, to_node_id: int, db: Session = Depends(get_db)):
    return get_shortest_route(graph_id, from_node_id, to_node_id, db)