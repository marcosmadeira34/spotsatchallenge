# app/routers/graph.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas import graph_schemas
from app.controllers.graph_controls import create_graph, get_graph, find_all_routes, delete_graph_by_id, find_shortest_route
from app.models.graph_models import User
from app.core.auth_bearer import JWTBearer

router = APIRouter()


@router.post("/create", response_model=graph_schemas.GraphResponse, summary="Create a new graph")
def create_new_graph(graph: graph_schemas.GraphCreate, db: Session = Depends(get_db)):
    """
        Create a new graph in the database with the provided nodes and edges
    """
    return create_graph(graph, db)

@router.get("/{graph_id}", response_model=graph_schemas.GraphResponse, dependencies=[Depends(JWTBearer())], summary="Get a graph by Id" )
def read_graph(graph_id: int, db: Session = Depends(get_db)):
    """
        Get a graph by its ID in the database 
    """
    graph = get_graph(graph_id, db)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph


@router.put("/{graph_id}", response_model=graph_schemas.GraphResponse, summary="Update a graph by Id")
def update_graph(graph_id: int, graph: graph_schemas.GraphCreate, db: Session = Depends(get_db)):
    """
        Update a graph by its ID in the database with the provided nodes and edges
    """
    update_graph = create_graph(graph, db)    
    if not update_graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return update_graph

# rota de deleção de grafo
@router.delete("/{graph_id}", response_model=graph_schemas.GraphDelete, summary="Delete a graph by Id")
def remove_graph(graph_id: int, db: Session = Depends(get_db)):
    """
        Delete a graph by its ID in the database
    """
    graph = delete_graph_by_id(graph_id, db)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph


@router.get("/graph/{graph_id}/routes", response_model=List[graph_schemas.RouteResponse], summary="Get all routes between two nodes")  
def get_all_routes(graph_id: int, start_node: str, end_node: str, max_stops: Optional[int] = None, db: Session = Depends(get_db)):
    """
        Get all routes between two nodes in the graph
    """
    return find_all_routes(graph_id, start_node, end_node, max_stops, db)



@router.get("/graph/{graph_id}/shortest_route", response_model=graph_schemas.RouteResponse, summary="Get the shortest route between two nodes")
def get_shortest_route(graph_id: int, start_node: str, end_node: str, db: Session = Depends(get_db)):
    """
        Get the shortest route between two nodes in the graph
    """
    return find_shortest_route(graph_id, start_node, end_node, db)