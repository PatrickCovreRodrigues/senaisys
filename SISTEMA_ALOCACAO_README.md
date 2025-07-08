# 🎯 Sistema de Gestão Docente (SGD) - Alocação Automática

Sistema completo de alocação automática de docentes para instituições de ensino, implementado com **FastAPI** (backend) e **Vue.js** (frontend).

## 📋 Funcionalidades Implementadas

### 🔧 Sistema de Alocação Principal
- **Matriz 5x4**: 5 dias úteis x 4 horários noturnos (19:00-22:00)
- **Classificação por tipos**:
  - **Tipo 1** (>100h): 2 dias fixos por semana
  - **Tipo 2** (50-99h): 1 dia fixo por semana  
  - **Tipo 3** (<50h): alocação aleatória
- **Integração com feriados nacionais** usando biblioteca `holidays`
- **Detecção automática de conflitos** de horários
- **Redução automática** de 3h20min por alocação do saldo docente

### 🗄️ Estrutura de Banco de Dados
```sql
-- Tabela principal de alocações
Assoc_UDD {
  id: int,
  uc_id: int,           -- Referência à UC
  docente_id: int,      -- Referência ao docente
  dia_semana: int,      -- 0=Segunda, 1=Terça, ..., 4=Sexta
  horario_inicio: str,  -- Ex: "19:00"
  horario_fim: str,     -- Ex: "22:20"
  data_alocacao: datetime,
  mes: int,
  ano: int,
  ativa: bool
}

-- Modelo Docente expandido
Docente {
  // ... campos originais ...
  email: str,
  especialidade: str,
  matricula: int,
  carga_horaria_total: float,
  tipo_docente: int,
  saldo_horas: float,
  restricoes_dias: json  -- Lista de dias restritos
}
```

### 🚀 API Endpoints Implementados

#### Alocação Automática
```bash
POST /api/alocacao/processar
# Processa alocação automática de lista de docentes
```

#### Visualização e Consulta
```bash
GET /api/alocacao/matriz-horarios
# Retorna matriz 5x4 com todas as alocações

GET /api/alocacao/disponibilidade/{docente_id}
# Verifica disponibilidade de docente específico

GET /api/alocacao/alocacoes-existentes
# Lista alocações para dia/horário específico

GET /api/alocacao/estatisticas
# Estatísticas gerais do sistema
```

#### Gestão Manual
```bash
POST /api/alocacao/alocacao-manual
PUT /api/alocacao/alocacao/{id}
DELETE /api/alocacao/alocacao/{id}
# CRUD para alocações manuais
```

#### Relatórios
```bash
GET /api/alocacao/relatorio-docente/{docente_id}
# Relatório completo de um docente
```

### 🎨 Frontend - Integração Vue.js

#### Tela de Criação de Docentes
- **Verificação automática de conflitos** antes de salvar
- **Alerta visual** quando há sobreposições de horários
- **Confirmação do usuário** para prosseguir com conflitos
- **Integração em tempo real** com API de alocação

```javascript
// Verificação de conflitos implementada
const verificarConflitosHorarios = async (dadosDocente) => {
  // Verifica todos os horários disponíveis do docente
  // Consulta alocações existentes via API
  // Retorna lista de conflitos detectados
}
```

### 📊 Exportação e Relatórios
- **CSV automático** com todas as alocações
- **Matriz transposta** para visualização estilo calendário
- **Persistência automática** no banco de dados
- **Estatísticas detalhadas** de utilização

## 🛠️ Instalação e Configuração

### 1. Setup Automático
```bash
cd backend
chmod +x setup_e_teste.sh
./setup_e_teste.sh
```

### 2. Instalação Manual
```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Criar tabelas
python3 -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"

# Frontend
cd ../vue-project
npm install
```

### 3. Executar Sistema
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd vue-project
npm run dev
```

## 🧪 Testes Implementados

### Executar Testes
```bash
cd backend
python3 test_alocacao.py [opcao]

# Opções:
# basico    - Teste básico completo
# conflitos - Teste de detecção de conflitos
# feriados  - Teste de verificação de feriados
# todos     - Executa todos os testes
```

### Exemplo de Teste
```python
docentes_exemplo = [
    {
        'id': '1',
        'mat': 1001,
        'ch': 120.0,    # Tipo 1 (>100h)
        'saldo': 120.0,
        'rest': [3, 4]  # Não disponível quinta/sexta
    },
    # ... mais docentes
]

resultado = alocar_docentes(docentes_exemplo)
# Retorna matriz completa, estatísticas e CSV
```

## 📋 Dependências Principais

### Backend
```txt
fastapi==0.104.1       # Framework web
uvicorn==0.24.0        # Servidor ASGI
sqlalchemy==2.0.23     # ORM banco de dados
pydantic==2.5.0        # Validação de dados
holidays==0.75         # Feriados nacionais
pandas==2.3.0          # Manipulação de dados/CSV
numpy==2.3.1           # Dependência do pandas
```

### Frontend
```json
{
  "vue": "^3.x",
  "vuetify": "^3.x",
  "vue-router": "^4.x",
  "axios": "^1.x"
}
```

## 🔍 Uso do Sistema

### 1. Criação de Docente com Verificação
1. Acesse a tela "Criar Docente"
2. Preencha dados básicos (nome, email, especialidade)
3. Defina disponibilidade por dia da semana
4. Configure horários de início/fim para cada dia
5. Sistema verifica automaticamente conflitos
6. Confirme criação mesmo com conflitos (se necessário)

### 2. Alocação Automática via API
```bash
curl -X POST "http://localhost:8000/api/alocacao/processar" \
-H "Content-Type: application/json" \
-d '[
  {
    "id": "1",
    "mat": 1001,
    "ch": 120.0,
    "tipo": 1,
    "saldo": 120.0,
    "rest": [3, 4]
  }
]'
```

### 3. Consultar Matriz de Horários
```bash
curl "http://localhost:8000/api/alocacao/matriz-horarios?ano=2025&mes=1"
```

## 📈 Funcionalidades Avançadas

### Algoritmo de Alocação
1. **Classificação automática** por carga horária
2. **Seleção de dias fixos** para tipos 1 e 2
3. **Verificação de restrições** de disponibilidade
4. **Detecção de feriados** e exclusão automática
5. **Prevenção de conflitos** entre docentes
6. **Redução automática** do saldo de horas

### Integração Frontend-Backend
- **Verificação em tempo real** de conflitos
- **Confirmação inteligente** com detalhes dos conflitos
- **Feedback visual** sobre alocações existentes
- **Mensagens contextuais** de sucesso/erro

### Relatórios e Exportação
- **CSV padronizado** com todas as informações
- **Matriz de visualização** em formato calendário
- **Estatísticas de utilização** por docente e UC
- **Relatórios individuais** por docente

## 🔧 Personalização

### Horários e Configurações
```python
# Em alocacao_docentes.py
HORARIOS_NOTURNOS = ['19:00', '20:00', '21:00', '22:00']
DURACAO_AULA = 3.33  # 3h20min

# Modificar conforme necessidade da instituição
```

### Tipos de Docente
```python
# Personalizar critérios de classificação
if docente.ch > 100:
    docente.tipo = 1  # 2 dias fixos
elif 50 <= docente.ch <= 99:
    docente.tipo = 2  # 1 dia fixo
else:
    docente.tipo = 3  # Aleatório
```

## 🎯 Principais Benefícios

✅ **Automação completa** do processo de alocação  
✅ **Detecção inteligente** de conflitos  
✅ **Integração com feriados** nacionais  
✅ **Interface intuitiva** para gestão manual  
✅ **Exportação automática** de relatórios  
✅ **API RESTful** para integrações  
✅ **Código modular** e facilmente extensível  
✅ **Testes automatizados** incluídos  

## 📞 Suporte

- **Documentação da API**: http://localhost:8000/docs
- **Testes**: `python3 test_alocacao.py ajuda`
- **Logs**: Verifique console do backend para detalhes

---

**Desenvolvido para otimizar a gestão acadêmica e eliminar conflitos de horários!** 🎓 