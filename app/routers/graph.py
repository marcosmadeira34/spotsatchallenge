# app/routers/graph.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import graph
from app.controllers.graph import create_graph, get_graph, find_all_routes, delete_graph_by_id, find_shortest_route
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

@router.put("/{graph_id}", response_model=graph.GraphResponse)
def update_graph(graph_id: int, graph: graph.GraphCreate, db: Session = Depends(get_db)):
    update_graph = create_graph(graph, db)    
    if not update_graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return update_graph

# rota de deleção de grafo
@router.delete("/{graph_id}", response_model=graph.GraphDelete)
def remove_graph(graph_id: int, db: Session = Depends(get_db)):
    graph = delete_graph_by_id(graph_id, db)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph


@router.get("/graph/{graph_id}/routes", response_model=List[graph.RouteResponse])
def get_all_routes(graph_id: int, start_node: str, end_node: str, max_stops: Optional[int] = None, db: Session = Depends(get_db)):
    return find_all_routes(graph_id, start_node, end_node, max_stops, db)



@router.get("/graph/{graph_id}/shortest_route", response_model=graph.RouteResponse)
def get_shortest_route(graph_id: int, start_node: str, end_node: str, db: Session = Depends(get_db)):
    return find_shortest_route(graph_id, start_node, end_node, db)