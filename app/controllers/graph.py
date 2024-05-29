# app/controllers/graph.py
from sqlalchemy.orm import Session
from app.models.graph import Graph, Node, Edge
from app.schemas.graph import GraphCreate, GraphResponse, NodeResponse, EdgeResponse, GraphDelete
from geoalchemy2.shape import to_shape
from typing import List, Optional

def create_graph(graph: GraphCreate, db: Session) -> GraphResponse:
    # Primeiro, criar o gráfico
    db_graph = Graph(name=graph.name)
    db.add(db_graph)
    db.commit()
    db.refresh(db_graph)

    node_id_map = {}  # Mapeamento de nomes de nós para IDs

    # Em seguida, criar os nós
    for node in graph.nodes:
        db_node = Node(name=node.name, geom=f'POINT({node.longitude} {node.latitude})', graph_id=db_graph.id)
        db.add(db_node)
        db.commit()
        db.refresh(db_node)
        node_id_map[node.name] = db_node.id  # Mapeie o nome do nó para o ID gerado

    # Finalmente, criar as arestas
    for edge in graph.edges:
        from_node_name = node_id_map.get(edge.from_node_name)  # Use o nome do nó para encontrar o ID correto
        to_node_name = node_id_map.get(edge.to_node_name)  # Use o nome do nó para encontrar o ID correto
        if from_node_name is None or to_node_name is None:
            raise ValueError(f"Invalid node names in edge: {edge.from_node_name} -> {edge.to_node_name}")

        db_edge = Edge(graph_id=db_graph.id, from_node_name=from_node_name, to_node_name=to_node_name, weight=edge.weight)
        db.add(db_edge)
    
    db.commit()

    return GraphResponse(id=db_graph.id, name=db_graph.name, 
                         nodes=[NodeResponse(id=n.id, name=n.name, longitude=n.geom.x, latitude=n.geom.y) 
                                for n in db_graph.nodes], 
                                edges=[EdgeResponse(id=e.id, from_node_name=e.from_node_name, to_node_name=e.to_node_name, weight=e.weight) 
                                       for e in db_graph.edges])


def get_graph(graph_id: int, db: Session) -> GraphResponse:
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
    edges = db.query(Edge).filter(Edge.graph_id == graph_id).all()

    node_responses = [
        NodeResponse(
            id=node.id,
            name=node.name,
            longitude=to_shape(node.geom).x,
            latitude=to_shape(node.geom).y
        ) for node in nodes
    ]

    edge_responses = [
        EdgeResponse(
            id=edge.id,
            from_node_name=edge.from_node_name,
            to_node_name=edge.to_node_name,
            weight=edge.weight
        ) for edge in edges
    ]

    return GraphResponse(
        id=graph.id,
        name=graph.name,
        nodes=node_responses,
        edges=edge_responses
    )

def update_graph_by_id(graph_id: int, graph: GraphCreate, db: Session) -> GraphResponse:
    delete_graph_by_id(graph_id, db)
    return create_graph(graph, db)

def delete_graph_by_id(graph_id: int, db: Session) -> GraphDelete:
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
    edges = db.query(Edge).filter(Edge.graph_id == graph_id).all()

    for edge in edges:
        db.delete(edge)
        db.commit()

    for node in nodes:
        db.delete(node)
        db.commit()

    db.delete(graph)
    db.commit()

    return GraphDelete(
        id=graph.id,
        name=graph.name,
        nodes=[NodeResponse(
            id=node.id,
            name=node.name,
            longitude=to_shape(node.geom).x,
            latitude=to_shape(node.geom).y
        ) for node in nodes],
        edges=[EdgeResponse(
            id=edge.id,
            from_node_name=edge.from_node_name,
            to_node_name=edge.to_node_name,
            weight=edge.weight
        ) for edge in edges]
    )















def get_routes(graph_id: int, from_node_name: int, to_node_name: int, max_stops: Optional[int], db: Session) -> List[List[int]]:
    # Lógica para encontrar todas as rotas de from_node_name para to_node_name com até max_stops
    pass

def get_shortest_route(graph_id: int, from_node_name: int, to_node_name: int, db: Session) -> List[int]:
    # Lógica para encontrar a rota mais curta de from_node_name para to_node_name
    pass