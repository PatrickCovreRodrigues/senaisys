# 🎓 SENAI Frontend - Sistema de Gestão Acadêmica

Sistema completo para gerenciamento de cursos, docentes, unidades curriculares (UCs) e calendários acadêmicos do SENAI.

## 🏗️ Arquitetura

- **Frontend**: Vue.js 3 + Vuetify 3 + Vite
- **Backend**: Python FastAPI + SQLite + SQLAlchemy
- **API**: REST com documentação automática (Swagger/ReDoc)

## 🚀 Quick Start

### 1. **Backend** (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
python populate_db.py    # Popular com dados de exemplo
python run.py           # Servidor na porta 8000
```

### 2. **Frontend** (Terminal 2)
```bash
cd vue-project
npm install
npm run dev            # Dev server na porta 5173
```

### 3. **Acessar**
- **Frontend**: http://localhost:5173
- **API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

## 📱 Funcionalidades

### ✅ **CRUD Completo**
- **Cursos**: Criar, listar, editar, deletar cursos
- **Docentes**: Gestão de professores com disponibilidade semanal
- **UCs**: Unidades curriculares com vinculação docente/curso
- **Calendários**: Geração automática de calendários acadêmicos

### ✅ **Interface Moderna**
- Design responsivo com Vuetify
- Loading states em todas as operações
- Notificações de sucesso/erro em tempo real
- Validação de formulários

### ✅ **API Robusta**
- Documentação automática com Swagger
- Validação de dados com Pydantic
- Tratamento de erros consistente
- CORS configurado para desenvolvimento

## 🗂️ Estrutura do Projeto

```
senaifront/
├── backend/                    # API FastAPI
│   ├── main.py                # App principal
│   ├── database.py            # Configuração SQLite
│   ├── models.py              # Modelos do banco
│   ├── schemas.py             # Validação Pydantic
│   ├── populate_db.py         # Dados de exemplo
│   ├── test_api.py            # Testes automatizados
│   └── routers/               # Endpoints por entidade
│       ├── cursos.py
│       ├── docentes.py
│       ├── ucs.py
│       └── calendario.py
│
├── vue-project/               # Frontend Vue.js
│   ├── src/
│   │   ├── components/        # Componentes Vue
│   │   │   ├── CriarCursoForm.vue
│   │   │   ├── CriarDocenteForm.vue
│   │   │   ├── CriarUCForm.vue
│   │   │   ├── GerarCalendario.vue
│   │   │   └── GlobalNotification.vue
│   │   ├── services/
│   │   │   └── api.js          # Cliente HTTP centralizado
│   │   ├── composables/
│   │   │   ├── useLoading.js   # Estados de carregamento
│   │   │   └── useNotification.js
│   │   └── docs/              # Documentação técnica
│   └── package.json
│
└── README.md                  # Este arquivo
```

## 🔗 Endpoints da API

### **Cursos** `/api/cursos/`
```
GET    /                    # Listar cursos
POST   /                    # Criar curso
GET    /{id}                # Obter curso
PUT    /{id}                # Atualizar curso
DELETE /{id}                # Deletar curso
GET    /{id}/ucs            # UCs do curso
```

### **Docentes** `/api/docentes/`
```
GET    /                    # Listar docentes
POST   /                    # Criar docente
GET    /{id}                # Obter docente
PUT    /{id}                # Atualizar docente
DELETE /{id}                # Deletar docente
GET    /{id}/disponibilidade # Ver disponibilidade
GET    /{id}/ucs            # UCs do docente
```

### **UCs** `/api/ucs/`
```
GET    /                    # Listar UCs
POST   /                    # Criar UC
GET    /{id}                # Obter UC
PUT    /{id}                # Atualizar UC
DELETE /{id}                # Deletar UC
GET    /por-curso/{curso_id} # UCs por curso
GET    /por-docente/{docente_id} # UCs por docente
PUT    /{id}/vincular-docente/{docente_id} # Vincular docente
```

### **Calendários** `/api/calendario/`
```
GET    /                    # Listar calendários
POST   /                    # Criar calendário
POST   /gerar              # Gerar calendário automático
GET    /{id}                # Obter calendário
PUT    /{id}                # Atualizar calendário
DELETE /{id}                # Deletar calendário
GET    /calendario-mes/{curso_id}/{ano}/{mes} # Calendário específico
```

## 📊 Modelo de Dados

### **Curso**
```json
{
  "id": 1,
  "nome": "Análise e Desenvolvimento de Sistemas",
  "carga_horaria": 2400,
  "fases": "Fase 1,Fase 2,Fase 3,Fase 4",
  "created_at": "2025-01-21T10:00:00",
  "updated_at": "2025-01-21T10:00:00"
}
```

### **Docente**
```json
{
  "id": 1,
  "nome": "Prof. João Silva",
  "disciplinas": ["Lógica de Programação", "Python"],
  "disponibilidade": {
    "segunda": true,
    "terca": true,
    "quarta": false,
    "quinta": true,
    "sexta": true,
    "sabado": false
  },
  "horarios": {
    "segunda": {"inicio": "08:00", "fim": "17:00"},
    "terca": {"inicio": "08:00", "fim": "17:00"}
  }
}
```

### **UC (Unidade Curricular)**
```json
{
  "id": 1,
  "nome": "Lógica de Programação",
  "carga_horaria": 80,
  "docente_id": 1,
  "curso_id": 1
}
```

### **Calendário**
```json
{
  "id": 1,
  "curso_id": 1,
  "mes": 4,
  "ano": 2025,
  "fases_selecionadas": [1, 2],
  "eventos": [
    {
      "id": "evento_1",
      "title": "Início das Aulas",
      "subtitle": "Fase 1",
      "date": "2025-04-07",
      "type": "inicio"
    }
  ]
}
```

## 🧪 Testes

### **Backend**
```bash
cd backend
python test_api.py          # Testes automatizados da API
```

### **Frontend**
```bash
cd vue-project
npm run test                 # Testes unitários (se configurado)
```

### **Teste Manual**
1. Iniciar backend e frontend
2. Abrir http://localhost:5173
3. Navegar para "Novo Cadastro"
4. Criar curso, docente e UC
5. Testar geração de calendário
6. Verificar notificações de sucesso/erro

## 🛠️ Desenvolvimento

### **Adicionar nova funcionalidade:**

1. **Backend** (se necessário):
   ```bash
   # Adicionar modelo em models.py
   # Adicionar schema em schemas.py
   # Criar router em routers/
   # Incluir router em main.py
   ```

2. **Frontend**:
   ```bash
   # Adicionar método em services/api.js
   # Criar/atualizar componente
   # Usar composables useLoading e useNotification
   ```

### **Estrutura de componente:**
```vue
<template>
  <div>
    <v-btn 
      :loading="isLoading" 
      @click="salvar"
    >
      Salvar
    </v-btn>
  </div>
</template>

<script setup>
import { cursosAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()

const salvar = async () => {
  try {
    await withLoading(() => cursosAPI.criar(dados))
    showSuccess('Criado com sucesso!')
  } catch (error) {
    showError(error.message)
  }
}
</script>
```

## 📋 Dados de Exemplo

O sistema vem com dados pré-populados:
- **4 Cursos**: ADS, Ciência de Dados, Desenvolvimento Web, Redes
- **3 Docentes**: Com diferentes disponibilidades
- **7 UCs**: Vinculadas aos cursos e docentes
- **2 Calendários**: Com eventos de exemplo

## 🔧 Configuração

### **Variáveis de Ambiente**
```bash
# Backend (.env)
DATABASE_URL=sqlite:///./senai_database.db
API_HOST=127.0.0.1
API_PORT=8000

# Frontend (.env)
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### **CORS**
Configurado para aceitar requests de:
- http://localhost:3000
- http://localhost:5173
- http://127.0.0.1:3000
- http://127.0.0.1:5173

## 📖 Documentação

- [`backend/README.md`](backend/README.md) - Documentação do backend
- [`vue-project/src/docs/api-integration-guide.md`](vue-project/src/docs/api-integration-guide.md) - Guia de integração
- [`vue-project/src/docs/frontend-backend-integration.md`](vue-project/src/docs/frontend-backend-integration.md) - Resumo completo

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Desenvolvedor** - *Implementação inicial* - [SeuUsuario](https://github.com/seuusuario)

## 🙏 Agradecimentos

- SENAI pela inspiração do projeto
- Vue.js e FastAPI pela tecnologia
- Vuetify pelo design system 