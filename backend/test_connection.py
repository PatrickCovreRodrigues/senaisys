import requests
import json

# Testar conectividade com o backend
def test_backend_connection():
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Teste básico de saúde
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code}")
        
        # Teste de listagem de docentes
        response = requests.get(f"{base_url}/api/docentes")
        print(f"List docentes: {response.status_code}")
        
        # Teste de OPTIONS (CORS preflight)
        response = requests.options(f"{base_url}/api/docentes/3")
        print(f"OPTIONS request: {response.status_code}")
        print(f"CORS headers: {response.headers}")
        
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao backend. Verifique se está rodando na porta 8000.")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_backend_connection()
