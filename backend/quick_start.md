# 🚀 Guia Rápido - SENAI Backend

## Instalação e Primeira Execução

### 1. Navegue para o diretório do backend
```bash
cd backend
```

### 2. Execute o script de configuração (Linux/Mac)
```bash
./start.sh
```

### 3. Ou execute manualmente:
```bash
# Instalar dependências
pip install -r requirements.txt

# Inicializar banco e popular com dados
python populate_db.py

# Iniciar servidor
python run.py
```

## ✅ Verificar se está funcionando

1. **Acesse a documentação:** http://127.0.0.1:8000/docs
2. **Execute os testes:** `python test_api.py`
3. **Health check:** http://127.0.0.1:8000/health

## 📊 Dados de Exemplo

O banco será populado automaticamente com:
- 4 cursos (ADS, Ciência de Dados, etc.)
- 3 docentes com disponibilidades
- 7 UCs vinculadas aos cursos e docentes
- 2 calendários de exemplo

## 🛠️ Endpoints Principais

### Cursos
- `GET /api/cursos/` - Listar todos os cursos
- `POST /api/cursos/` - Criar novo curso
- `GET /api/cursos/{id}` - Obter curso específico
- `PUT /api/cursos/{id}` - Atualizar curso
- `DELETE /api/cursos/{id}` - Deletar curso

### Docentes
- `GET /api/docentes/` - Listar todos os docentes
- `POST /api/docentes/` - Criar novo docente
- `GET /api/docentes/{id}` - Obter docente específico
- `GET /api/docentes/{id}/disponibilidade` - Ver disponibilidade

### UCs
- `GET /api/ucs/` - Listar todas as UCs
- `POST /api/ucs/` - Criar nova UC
- `GET /api/ucs/por-curso/{curso_id}` - UCs de um curso
- `PUT /api/ucs/{id}/vincular-docente/{docente_id}` - Vincular docente

### Calendários
- `POST /api/calendario/gerar` - Gerar calendário automático
- `GET /api/calendario/calendario-mes/{curso_id}/{ano}/{mes}` - Calendário específico

## 📋 Exemplos de Uso

### Criar um novo curso:
```bash
curl -X POST "http://127.0.0.1:8000/api/cursos/" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Meu Novo Curso",
       "carga_horaria": 1600,
       "fases": "Fase 1,Fase 2"
     }'
```

### Gerar calendário:
```bash
curl -X POST "http://127.0.0.1:8000/api/calendario/gerar" \
     -H "Content-Type: application/json" \
     -d '{
       "curso_id": 1,
       "mes": 5,
       "ano": 2025,
       "fases_selecionadas": [1, 2]
     }'
```

## 🔧 Configuração CORS

O backend está configurado para aceitar requests do frontend Vue.js nas URLs:
- http://localhost:3000
- http://localhost:5173
- http://127.0.0.1:3000
- http://127.0.0.1:5173 