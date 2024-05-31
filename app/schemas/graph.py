from pydantic import BaseModel
from typing import List, Optional

class NodeCreate(BaseModel):
    name: str
    longitude: float
    latitude: float

class NodeResponse(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float

    class Config:
        orm_mode = True


class EdgeCreate(BaseModel):
    from_node_name: str
    to_node_name: str
    weight: int

class EdgeResponse(BaseModel):
    id: int
    from_node_name: str
    to_node_name: str
    weight: int

    class Config:
        orm_mode = True


class GraphCreate(BaseModel):
    name: str
    nodes: List[NodeCreate]
    edges: List[EdgeCreate]

class GraphResponse(BaseModel):
    id: int
    name: str
    nodes: List[NodeResponse]
    edges: List[EdgeResponse]

    class Config:
        orm_mode = True 

class GraphDelete(BaseModel):
    id: int
    

class RouteResponse(BaseModel):
    route: List[NodeResponse]
    

