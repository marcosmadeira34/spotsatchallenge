from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import database, Graph
import networkx as nx

app = FastAPI()

class GraphCreate(BaseModel):
    name: str
    data: dict

# Função para inserir um grafo no banco de dados
@app.post("/graphs/")
async def create_graph(graph: GraphCreate):
    query = Graph.insert().values(name=graph.name, data=graph.data)
    last_record_id = await database.execute(query)
    return {**graph.model_dump(), "id": last_record_id}

# Função para recuperar um grafo do banco de dados
@app.get("/graphs/{graph_id}")
async def read_graph(graph_id: int):
    query = Graph.select().where(Graph.c.id == graph_id)
    graph = await database.fetch_one(query)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph

# Função para buscar todas as possíveis rotas entre dois pontos
@app.get("/graphs/{graph_id}/paths/")
async def get_all_paths(graph_id: int, start: str, end: str, max_stops: Optional[int] = None):
    query = Graph.select().where(Graph.c.id == graph_id)
    graph = await database.fetch_one(query)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    graph_data = graph["data"]
    paths = find_all_paths(graph_data, start, end, max_stops)
    return {"paths": paths}

# Função para buscar a menor rota entre dois pontos
@app.get("/graphs/{graph_id}/shortest-path/")
async def get_shortest_path(graph_id: int, start: str, end: str):
    query = Graph.select().where(Graph.c.id == graph_id)
    graph = await database.fetch_one(query)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    graph_data = graph["data"]
    path = find_shortest_path(graph_data, start, end)
    if path is None:
        raise HTTPException(status_code=404, detail="No path found")
    return {"path": path}

# Inicialização do banco de dados
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Funções auxiliares para encontrar rotas
def find_all_paths(graph_data, start_node, end_node, max_stops=None):
    graph = nx.DiGraph(graph_data)
    paths = list(nx.all_simple_paths(graph, source=start_node, target=end_node))
    if max_stops is not None:
        paths = [path for path in paths if len(path) - 1 <= max_stops]
    return paths



def find_shortest_path(graph_data, start_node, end_node):
    graph = nx.DiGraph(graph_data)
    try:
        path = nx.shortest_path(graph, source=start_node, target=end_node)
        return path
    except nx.NetworkXNoPath:
        return None
