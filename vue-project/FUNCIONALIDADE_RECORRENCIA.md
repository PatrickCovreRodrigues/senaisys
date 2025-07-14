# 🔄 Funcionalidade de Recorrência - Alocação de Docentes por Semestre

## 📋 Descrição

Esta funcionalidade implementa um sistema de alocação automática de docentes ao longo de um semestre inteiro (5 meses), gerenciando conflitos de horários através de um sistema de **recorrência semanal alternada**.

## 🎯 Objetivo

Quando múltiplos professores estão disponíveis para o mesmo dia/horário, o sistema:
- **Semana 1**: Professor A ministra a aula
- **Semana 2**: Professor B ministra a aula  
- **Semana 3**: Professor A ministra a aula
- **Semana 4**: Professor B ministra a aula
- E assim sucessivamente...

## ⚙️ Funcionamento

### 1. **Detecção de Conflitos**
- O sistema identifica quando 2 ou mais professores estão disponíveis no mesmo dia/horário
- Considera as configurações de disponibilidade de cada docente (dias da semana + horários)

### 2. **Algoritmo de Alternância**
- Cria um cronograma de 5 meses (aproximadamente 20 semanas letivas)
- Distribui as semanas entre os professores em conflito de forma alternada
- Mantém registro de qual professor ministra em cada semana específica

### 3. **Geração do Calendário**
- Gera eventos no calendário para cada semana do semestre
- Cada evento contém:
  - Data específica da aula
  - Professor responsável naquela semana
  - UC/disciplina (se vinculada)
  - Horário (início e fim)

## 🚀 Como Usar

1. **Cadastre os professores** com suas disponibilidades (dias e horários)
2. **Vincule UCs aos professores** (opcional)
3. **Acesse o Gerar Calendário** 
4. **Clique no botão "Alocar Docentes para Semestre"** (novo botão)
5. **Visualize o resultado** no calendário com as aulas distribuídas

## 📊 Exemplo Prático

**Cenário**: 
- Professor João: disponível Segunda 19h-22h
- Professor Maria: disponível Segunda 19h-22h  
- UC: "Programação Web"

**Resultado**:
```
Semana 1 (03/02): João - Programação Web - 19h-22h
Semana 2 (10/02): Maria - Programação Web - 19h-22h  
Semana 3 (17/02): João - Programação Web - 19h-22h
Semana 4 (24/02): Maria - Programação Web - 19h-22h
... (continua por 5 meses)
```

## 🔧 Funcionalidades Técnicas

- ✅ **Validação de disponibilidade** dos docentes
- ✅ **Detecção automática de conflitos** de horários  
- ✅ **Algoritmo de distribuição justa** entre professores
- ✅ **Geração de eventos recorrentes** no calendário
- ✅ **Suporte a múltiplos professores** no mesmo conflito
- ✅ **Consideração de feriados** e recessos escolares
- ✅ **Persistência no banco de dados** e localStorage

## 📅 Período do Semestre

O sistema considera um semestre de **5 meses letivos**:
- Aproximadamente **20 semanas** de aulas
- Exclui automaticamente feriados nacionais
- Considera apenas dias úteis (segunda a sexta)
- Horários noturnos: 19h às 23h (segunda a sexta)
- Horários matutinos: 10h às 12h (sábados)

## 🎨 Interface

A funcionalidade será integrada ao componente `GerarCalendario.vue` com:
- **Novo botão**: "Alocar Docentes para Semestre"
- **Dialog de configuração**: escolher mês de início e duração
- **Visualização dos resultados**: no calendário existente
- **Feedback visual**: indicadores de professores alternados
