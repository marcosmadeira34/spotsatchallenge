# app/controllers/graph.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.graph import Graph, Node, Edge
from app.schemas.graph import GraphCreate, GraphResponse, NodeResponse, EdgeResponse, GraphDelete, RouteResponse
from geoalchemy2.shape import to_shape
from typing import List, Optional
from fastapi import HTTPException
import networkx as nx
from shapely.geometry import Point

def create_graph(graph: GraphCreate, db: Session) -> GraphResponse:
    try:
        # Iniciar uma transação
        db.begin()

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
            from_node_id = node_id_map.get(edge.from_node_name)  # Use o nome do nó para encontrar o ID correto
            to_node_id = node_id_map.get(edge.to_node_name)  # Use o nome do nó para encontrar o ID correto
            if from_node_id is None or to_node_id is None:
                raise ValueError(f"Invalid node names in edge: {edge.from_node_name} -> {edge.to_node_name}")

            db_edge = Edge(graph_id=db_graph.id, from_node_name=edge.from_node_name, to_node_name=edge.to_node_name, weight=edge.weight)
            db.add(db_edge)

        # Commitar a transação ao final
        db.commit()

        # Construir a resposta
        nodes_response = [NodeResponse(id=n.id, name=n.name, longitude=to_shape(n.geom).x, latitude=to_shape(n.geom).y) for n in db_graph.nodes]
        edges_response = [EdgeResponse(id=e.id, from_node_name=e.from_node_name, to_node_name=e.to_node_name, weight=e.weight) for e in db_graph.edges]

        return GraphResponse(id=db_graph.id, name=db_graph.name, nodes=nodes_response, edges=edges_response)

    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            # Extrair o nome do nó duplicado da mensagem de erro
            detail = str(e.orig).split("DETAIL:  Key (name)=")[1].split(" already exists.")[0]
            raise HTTPException(status_code=404, detail=f"Node with name '{detail}' already exists.")
        raise HTTPException(status_code=400, detail=f"An integrity error occurred while creating the graph: {str(e)}")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"A database error occurred while creating the graph: {str(e)}")

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        db.close()


def get_graph(graph_id: int, db: Session) -> GraphResponse:
    try:
        # Tentar encontrar o gráfico pelo ID
        graph = db.query(Graph).filter(Graph.id == graph_id).first()
        if not graph:
            raise HTTPException(status_code=404, detail=f"Graph with id {graph_id} not found")

        # Consultar nós e arestas associados ao gráfico
        nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
        edges = db.query(Edge).filter(Edge.graph_id == graph_id).all()

        # Construir a resposta para os nós
        node_responses = [
            NodeResponse(
                id=node.id,
                name=node.name,
                longitude=to_shape(node.geom).x,
                latitude=to_shape(node.geom).y
            ) for node in nodes
        ]

        # Construir a resposta para as arestas
        edge_responses = [
            EdgeResponse(
                id=edge.id,
                from_node_name=edge.from_node_name,
                to_node_name=edge.to_node_name,
                weight=edge.weight
            ) for edge in edges
        ]

        # Retornar a resposta do gráfico completo
        return GraphResponse(
            id=graph.id,
            name=graph.name,
            nodes=node_responses,
            edges=edge_responses
        )

    except SQLAlchemyError as e:
        # Capturar erros do SQLAlchemy e retornar uma resposta HTTP 500
        raise HTTPException(status_code=404, detail=f"A database error occurred while retrieving the graph: {str(e)}")

    except Exception as e:
        # Capturar outras exceções e retornar uma resposta HTTP 500
        raise HTTPException(status_code=404, detail=f"An unexpected error occurred: {str(e)}")


def update_graph_by_id(graph_id: int, graph: GraphCreate, db: Session) -> GraphResponse:
    try:
        # Verifica se o gráfico existe
        existing_graph = db.query(Graph).filter(Graph.id == graph_id).first()
        if not existing_graph:
            raise HTTPException(status_code=404, detail=f"Graph with id {graph_id} not found")
        
        # Atualiza o nome do gráfico, se fornecido
        if graph.name:
            existing_graph.name = graph.name
        
        # Atualiza os nós e arestas do gráfico, se fornecido
        if graph.nodes:
            # Remove todos os nós existentes do gráfico
            existing_graph.nodes.clear()
            for node in graph.nodes:
                existing_graph.nodes.append(node)

        if graph.edges:
            # Remove todas as arestas existentes do gráfico
            existing_graph.edges.clear()
            for edge in graph.edges:
                existing_graph.edges.append(edge)

        # Salva as alterações no banco de dados
        db.commit()

        # Retorna a resposta atualizada
        return GraphResponse(
            id=existing_graph.id,
            name=existing_graph.name,
            nodes=existing_graph.nodes,
            edges=existing_graph.edges
        )

    except HTTPException as e:
        # Re-raise HTTP exceptions to keep their status and detail
        raise e

    except SQLAlchemyError as e:
        # Captura erros do SQLAlchemy e retorna uma resposta HTTP 500
        raise HTTPException(status_code=500, detail=f"A database error occurred while updating the graph: {str(e)}")

    except Exception as e:
        # Captura outras exceções e retorna uma resposta HTTP 500
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


def delete_graph_by_id(graph_id: int, db: Session) -> GraphDelete:
    try:
        # Tentar encontrar o gráfico pelo ID
        graph = db.query(Graph).filter(Graph.id == graph_id).first()
        if not graph:
            raise HTTPException(status_code=404, detail=f"Graph with id {graph_id} not found")

        # Consultar nós e arestas associados ao gráfico
        nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
        edges = db.query(Edge).filter(Edge.graph_id == graph_id).all()

        # Deletar arestas
        for edge in edges:
            db.delete(edge)
            db.commit()

        # Deletar nós
        for node in nodes:
            db.delete(node)
            db.commit()

        # Deletar o gráfico
        db.delete(graph)
        db.commit()

        # Retornar a resposta do gráfico deletado
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

    except SQLAlchemyError as e:
        # Capturar erros do SQLAlchemy e retornar uma resposta HTTP 500
        raise HTTPException(status_code=500, detail=f"A database error occurred while deleting the graph: {str(e)}")

    except Exception as e:
        # Capturar outras exceções e retornar uma resposta HTTP 500
        raise HTTPException(status_code=404, detail=f"An unexpected error occurred: {str(e)}")


# Função para criar o grafo networkx a partir dos dados do banco de dados
def create_networkx_graph(graph_id: int, db: Session) -> nx.DiGraph:
    graph = nx.DiGraph()
    
    nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
    edges = db.query(Edge).filter(Edge.graph_id == graph_id).all()
    
    for node in nodes:
        graph.add_node(node.name, pos=(node.longitude, node.latitude))
    
    for edge in edges:
        graph.add_edge(edge.from_node_name, edge.to_node_name, weight=edge.weight)
    
    return graph
 

def find_all_routes(graph_id: int, start_node: str, end_node: str, max_stops: Optional[int], db: Session) -> List[RouteResponse]:
    try:
        # Busca o grafo no banco de dados
        graph = db.query(Graph).filter(Graph.id == graph_id).first()
        if not graph:
            raise HTTPException(status_code=404, detail="Graph not found")

        # Busca todos os nós e arestas do grafo
        nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
        edges = db.query(Edge).filter(Edge.graph_id == graph_id).all()

        # Cria um grafo direcionado com NetworkX
        G = nx.DiGraph()

        # Adiciona os nós ao grafo NetworkX
        for node in nodes:
            point: Point = to_shape(node.geom)
            G.add_node(node.name, id=node.id, longitude=point.x, latitude=point.y)

        # Adiciona as arestas ao grafo NetworkX
        for edge in edges:
            G.add_edge(edge.from_node_name, edge.to_node_name, weight=edge.weight)

        all_routes = []

        # Verifica se deve considerar um limite de paradas
        if max_stops is not None:
            for path in nx.all_simple_paths(G, source=start_node, target=end_node):
                if len(path) - 1 <= max_stops:
                    route = []
                    for node_name in path:
                        node = next((n for n in nodes if n.name == node_name), None)
                        if node:
                            point: Point = to_shape(node.geom)
                            route.append(NodeResponse(id=node.id, name=node.name, longitude=point.x, latitude=point.y))
                    all_routes.append(RouteResponse(route=route))
        else:
            for path in nx.all_simple_paths(G, source=start_node, target=end_node):
                route = []
                for node_name in path:
                    node = next((n for n in nodes if n.name == node_name), None)
                    if node:
                        point: Point = to_shape(node.geom)
                        route.append(NodeResponse(id=node.id, name=node.name, longitude=point.x, latitude=point.y))
                all_routes.append(RouteResponse(route=route))

        return all_routes

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    

# Função para encontrar a menor rota possível entre dois pontos
def find_shortest_route(graph_id: int, start_node: str, end_node: str, db: Session) -> RouteResponse:
    try:
        # Busca o grafo no banco de dados
        graph = db.query(Graph).filter(Graph.id == graph_id).first()
        if not graph:
            raise HTTPException(status_code=404, detail="Graph not found")

        # Busca todos os nós e arestas do grafo
        nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
        edges = db.query(Edge).filter(Edge.graph_id == graph_id).all()

        # Cria um grafo direcionado com NetworkX
        G = nx.DiGraph()

        # Adiciona os nós ao grafo NetworkX
        for node in nodes:
            point: Point = to_shape(node.geom)
            G.add_node(node.name, id=node.id, longitude=point.x, latitude=point.y)

        # Adiciona as arestas ao grafo NetworkX
        for edge in edges:
            G.add_edge(edge.from_node_name, edge.to_node_name, weight=edge.weight)

        # Encontra o caminho mais curto usando Bellman-Ford
        shortest_path = nx.dijkstra_path(G, source=start_node, target=end_node)
        
        # Cria a resposta da rota
        route = []
        for node_name in shortest_path:
            node = next((n for n in nodes if n.name == node_name), None)
            if node:
                point: Point = to_shape(node.geom)
                route.append(NodeResponse(id=node.id, name=node.name, longitude=point.x, latitude=point.y))

        return RouteResponse(route=route)

    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No path found between the specified nodes")

    except nx.NodeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")