from fastapi import FastAPI

from app.db.database import engine
""" from .models.nodes import Base as NodeBase
from .models.edges import Base as EdgeBase """
from app.models.graph import Base as GraphBase
from app.routers import graph, users


app = FastAPI()

GraphBase.metadata.create_all(bind=engine)


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(graph.router, prefix="/graph", tags=["graph"])
