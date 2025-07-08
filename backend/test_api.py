"""
Script para testar os endpoints da API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Testar se a API está funcionando"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API está funcionando!")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Certifique-se de que o servidor está rodando.")
        return False

def test_cursos():
    """Testar endpoints de cursos"""
    print("\n📚 Testando endpoints de cursos...")
    
    # Listar cursos
    response = requests.get(f"{BASE_URL}/api/cursos/")
    if response.status_code == 200:
        cursos = response.json()
        print(f"✅ Encontrados {len(cursos)} cursos")
        if cursos:
            print(f"   Primeiro curso: {cursos[0]['nome']}")
    else:
        print(f"❌ Erro ao listar cursos: {response.status_code}")

def test_docentes():
    """Testar endpoints de docentes"""
    print("\n👨‍🏫 Testando endpoints de docentes...")
    
    # Listar docentes
    response = requests.get(f"{BASE_URL}/api/docentes/")
    if response.status_code == 200:
        docentes = response.json()
        print(f"✅ Encontrados {len(docentes)} docentes")
        if docentes:
            print(f"   Primeiro docente: {docentes[0]['nome']}")
    else:
        print(f"❌ Erro ao listar docentes: {response.status_code}")

def test_ucs():
    """Testar endpoints de UCs"""
    print("\n📖 Testando endpoints de UCs...")
    
    # Listar UCs
    response = requests.get(f"{BASE_URL}/api/ucs/")
    if response.status_code == 200:
        ucs = response.json()
        print(f"✅ Encontradas {len(ucs)} UCs")
        if ucs:
            print(f"   Primeira UC: {ucs[0]['nome']}")
    else:
        print(f"❌ Erro ao listar UCs: {response.status_code}")

def test_calendario():
    """Testar endpoints de calendário"""
    print("\n📅 Testando endpoints de calendário...")
    
    # Listar calendários
    response = requests.get(f"{BASE_URL}/api/calendario/")
    if response.status_code == 200:
        calendarios = response.json()
        print(f"✅ Encontrados {len(calendarios)} calendários")
    else:
        print(f"❌ Erro ao listar calendários: {response.status_code}")

def test_criar_curso():
    """Testar criação de um novo curso"""
    print("\n➕ Testando criação de curso...")
    
    novo_curso = {
        "nome": "Curso de Teste API",
        "carga_horaria": 1000,
        "fases": "Teste"
    }
    
    response = requests.post(f"{BASE_URL}/api/cursos/", json=novo_curso)
    if response.status_code == 200:
        curso_criado = response.json()
        print(f"✅ Curso criado com sucesso: {curso_criado['nome']} (ID: {curso_criado['id']})")
        return curso_criado['id']
    else:
        print(f"❌ Erro ao criar curso: {response.status_code}")
        print(f"   Resposta: {response.text}")
        return None

def run_all_tests():
    """Executar todos os testes"""
    print("🧪 Iniciando testes da API SENAI Backend...")
    
    # Testar se API está funcionando
    if not test_health():
        print("\n❌ API não está funcionando. Verifique se o servidor está rodando.")
        return
    
    # Testar endpoints básicos
    test_cursos()
    test_docentes()
    test_ucs()
    test_calendario()
    
    # Testar criação
    curso_id = test_criar_curso()
    
    print("\n🎉 Testes concluídos!")
    print("\n📋 Para ver todos os endpoints disponíveis:")
    print(f"   Swagger UI: {BASE_URL}/docs")
    print(f"   ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    run_all_tests() 