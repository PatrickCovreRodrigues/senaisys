# SENAI Backend API

Backend em Python com FastAPI para gerenciamento de cursos, docentes, UCs e calendários do SENAI.

## 🚀 Instalação e Execução

### 1. Instalar dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Executar o servidor

```bash
python run.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Acessar a documentação

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📊 Banco de Dados

O backend utiliza SQLite como banco de dados, criado automaticamente no arquivo `senai_database.db`.

### Entidades:

- **Cursos**: nome, carga_horaria, fases
- **Docentes**: nome, disciplinas, disponibilidade, horarios
- **UCs**: nome, carga_horaria, docente_id, curso_id
- **Calendários**: curso_id, fases_selecionadas, mes, ano, eventos

## 🛠️ Endpoints Principais

### Cursos
- `GET /api/cursos/` - Listar cursos
- `POST /api/cursos/` - Criar curso
- `GET /api/cursos/{id}` - Obter curso
- `PUT /api/cursos/{id}` - Atualizar curso
- `DELETE /api/cursos/{id}` - Deletar curso

### Docentes
- `GET /api/docentes/` - Listar docentes
- `POST /api/docentes/` - Criar docente
- `GET /api/docentes/{id}` - Obter docente
- `PUT /api/docentes/{id}` - Atualizar docente
- `DELETE /api/docentes/{id}` - Deletar docente

### UCs
- `GET /api/ucs/` - Listar UCs
- `POST /api/ucs/` - Criar UC
- `GET /api/ucs/{id}` - Obter UC
- `PUT /api/ucs/{id}` - Atualizar UC
- `DELETE /api/ucs/{id}` - Deletar UC

### Calendários
- `GET /api/calendario/` - Listar calendários
- `POST /api/calendario/` - Criar calendário
- `POST /api/calendario/gerar` - Gerar calendário automático
- `GET /api/calendario/{id}` - Obter calendário

## 🔧 Configuração

Copie o arquivo `.env.example` para `.env` e configure as variáveis conforme necessário.

## 📝 Estrutura do Projeto

```
backend/
├── main.py              # Aplicação principal FastAPI
├── database.py          # Configuração do banco de dados
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # Schemas Pydantic
├── run.py              # Script para executar o servidor
├── requirements.txt     # Dependências Python
└── routers/            # Endpoints da API
    ├── cursos.py
    ├── docentes.py
    ├── ucs.py
    └── calendario.py
```

## 🌐 CORS

O backend está configurado para aceitar requests do frontend Vue.js nas seguintes URLs:
- http://localhost:3000
- http://localhost:5173
- http://127.0.0.1:3000
- http://127.0.0.1:5173 