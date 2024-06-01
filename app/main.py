from fastapi import FastAPI

from app.db.database import engine
from app.models.graph_models import Base as GraphBase
from app.routers import graph_routers, users_routers


app = FastAPI()

GraphBase.metadata.create_all(bind=engine)


app.include_router(users_routers.router, prefix="/users", tags=["users"])
app.include_router(graph_routers.router, prefix="/graph", tags=["graph"])
