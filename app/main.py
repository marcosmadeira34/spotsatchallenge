from fastapi import FastAPI

from .database import engine
""" from .models.nodes import Base as NodeBase
from .models.edges import Base as EdgeBase """
from .models.graph import Base as GraphBase
from .routers import graph

app = FastAPI()

@app.on_event("startup")
def startup():
    """ NodeBase.metadata.create_all(bind=engine)
    EdgeBase.metadata.create_all(bind=engine) """
    GraphBase.metadata.create_all(bind=engine)

""" app.include_router(nodes.router, prefix="/nodes", tags=["nodes"])
app.include_router(edges.router, prefix="/edges", tags=["edges"]) """
app.include_router(graph.router, prefix="/graph", tags=["graph"])
