""" from pydantic import BaseModel
from typing import List

class EdgeCreate(BaseModel):
    start_node_id: int
    end_node_id: int
    coordinates: List[tuple]

class Edge(BaseModel):
    id: int
    start_node_id: int
    end_node_id: int
    coordinates: List[tuple]

    class Config:
        orm_mode = True

         """