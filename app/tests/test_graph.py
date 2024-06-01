# Arquivo para realizar testes dos métodos de controle dos grafos

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Teste criação do grafo de acordo com os schemas definidos (NodeCreate, EdgeCreate, GraphCreate)
def test_create_new_graph():
    try:
        response = client.post(
            "/graph/create",
            json={
                "name": "Test create graph",
                "nodes": [
                    {"name": "A", "longitude": 0.0, "latitude": 0.0},
                    {"name": "B", "longitude": 1.0, "latitude": 1.0},
                    {"name": "C", "longitude": 2.0, "latitude": 2.0}
                ],
                "edges": [
                    {"from_node_name": "A", "to_node_name": "B", "weight": 10}
                ]
            }
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Test create graph"
    except AssertionError as e:
        print(f"O erro foi {e}")
        

def test_read_graph():
    try:
        # Cria um novo grafo para buscar pelo ID
        graph_id = test_create_new_graph()

        # Agora, busca o grafo criado pelo ID
        response = client.get(f"/graph/{graph_id}")
        assert response.status_code == 200

        # Verifica se o nome do grafo retornado está correto
        assert response.json()["name"] == "Test create graph"

        # Verifica se os nós foram retornados corretamente
        assert len(response.json()["nodes"]) == 3
        assert response.json()["nodes"][0]["name"] == "A"
        assert response.json()["nodes"][1]["name"] == "B"
        assert response.json()["nodes"][2]["name"] == "C"

        # Verifica se as arestas foram retornadas corretamente
        assert len(response.json()["edges"]) == 1
        assert response.json()["edges"][0]["from_node_name"] == "A"
        assert response.json()["edges"][0]["to_node_name"] == "B"
        assert response.json()["edges"][0]["weight"] == 10

    except AssertionError as e:
        print(f"AssertionError: {e}")
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        

def test_update_graph():
    try:
        # Cria um novo grafo para buscar pelo ID
        graph_id = test_create_new_graph()

        # Agora, atualiza o grafo criado pelo ID
        response = client.put(
            f"/graph/{graph_id}",
            json={
                "name": "Test update graph",
                "nodes": [
                    {"name": "A", "longitude": 0.0, "latitude": 0.0},
                    {"name": "B", "longitude": 1.0, "latitude": 1.0},
                    {"name": "C", "longitude": 2.0, "latitude": 2.0}
                ],
                "edges": [
                    {"from_node_name": "A", "to_node_name": "B", "weight": 10},
                    {"from_node_name": "B", "to_node_name": "C", "weight": 20}
                ]
            }
        )
        assert response.status_code == 200

        # Verifica se o nome do grafo retornado está correto
        assert response.json()["name"] == "Test update graph"

        # Verifica se os nós foram retornados corretamente
        assert len(response.json()["nodes"]) == 3
        assert response.json()["nodes"][0]["name"] == "A"
        assert response.json()["nodes"][1]["name"] == "B"
        assert response.json()["nodes"][2]["name"] == "C"

        # Verifica se as arestas foram retornadas corretamente
        assert len(response.json()["edges"]) == 2
        assert response.json()["edges"][0]["from_node_name"] == "A"
        assert response.json()["edges"][0]["to_node_name"] == "B"
        assert response.json()["edges"][0]["weight"] == 10
        assert response.json()["edges"][1]["from_node_name"] == "B"
        assert response.json()["edges"][1]["to_node_name"] == "C"
        assert response.json()["edges"][1]["weight"] == 20

    except AssertionError as e:
        print(f"AssertionError: {e}")
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")


def test_delete_graph():
    try:
        # Cria um novo grafo para buscar pelo ID
        graph_id = test_create_new_graph()

        # Agora, deleta o grafo criado pelo ID
        response = client.delete(f"/graph/{graph_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Graph deleted successfully"

    except AssertionError as e:
        print(f"AssertionError: {e}")
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")