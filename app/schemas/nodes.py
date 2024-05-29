""" from pydantic import BaseModel
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
 """