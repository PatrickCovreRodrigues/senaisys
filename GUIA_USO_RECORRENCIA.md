# 🎯 Guia de Uso - Alocação Automática com Recorrência

## 📝 Resumo

Implementei com sucesso a funcionalidade de **alocação automática de docentes com recorrência semanal** para o seu sistema SENAI. Esta funcionalidade permite que professores sejam automaticamente distribuídos ao longo de um semestre inteiro (5 meses), com resolução inteligente de conflitos através de alternância semanal.

## ✅ O que foi implementado

### 🚀 Backend
1. **Novo módulo**: `alocacao_recorrencia.py` - Sistema completo de alocação
2. **Novo endpoint**: `/api/alocacao/processar-semestre` - API para processar alocação
3. **Algoritmo inteligente**: Detecta conflitos e alterna professores semanalmente
4. **Persistência**: Salva alocações no banco de dados
5. **Validações**: Considera disponibilidade, feriados e horários

### 🎨 Frontend  
1. **Novo botão**: "Alocar Docentes para Semestre" no calendário
2. **Dialog de configuração**: Permite escolher período e duração
3. **Integração**: Eventos aparecem automaticamente no calendário
4. **Feedback visual**: Mostra estatísticas e resultados

## 🎯 Como usar

### 1️⃣ **Pré-requisitos**
- Ter professores cadastrados
- Configurar disponibilidade dos professores (dias e horários)
- Opcionalmente vincular UCs aos professores

### 2️⃣ **Usando a funcionalidade**
1. Acesse **"Gerar Calendário"** no menu
2. Clique no botão verde **"Alocar Docentes para Semestre"**
3. Configure:
   - **Mês de início** (ex: Março)
   - **Ano de início** (ex: 2025)
   - **Duração** (padrão: 5 meses)
4. Clique em **"Iniciar Alocação"**
5. ✅ **Resultado**: Eventos aparecem automaticamente no calendário!

### 3️⃣ **O que acontece automaticamente**

#### 📅 **Sem conflitos**:
- Professor João: Segunda 19h-22h ➜ **Toda segunda do semestre**

#### ⚔️ **Com conflitos** (NOVIDADE!):
- Professor João: Segunda 19h-22h
- Professor Maria: Segunda 19h-22h

**Resultado com alternância**:
```
Semana 1 (03/03): João ministra
Semana 2 (10/03): Maria ministra  
Semana 3 (17/03): João ministra
Semana 4 (24/03): Maria ministra
... (continua por 5 meses)
```

## 📊 Benefícios

✅ **Automático**: Não precisa alocar manualmente cada semana  
✅ **Inteligente**: Resolve conflitos automaticamente  
✅ **Justo**: Distribui igualmente entre professores  
✅ **Completo**: Gera 5 meses de aulas de uma vez  
✅ **Visual**: Resultado aparece no calendário  
✅ **Flexível**: Configura período e duração  

## 🎨 Exemplo Visual

Depois de usar a funcionalidade, seu calendário ficará assim:

```
📅 MARÇO 2025
┌─────────────────────────────────────────┐
│ 03/03 SEG │ 04/03 TER │ 05/03 QUA │ ... │
│ 🟦 João   │ 🟩 Maria  │ 🟨 Carlos │     │
│ 19h-22h   │ 19h-22h   │ 20h-23h   │     │
├─────────────────────────────────────────┤
│ 10/03 SEG │ 11/03 TER │ 12/03 QUA │ ... │
│ 🟩 Maria  │ 🟦 João   │ 🟨 Carlos │     │
│ 19h-22h   │ 19h-22h   │ 20h-23h   │     │
└─────────────────────────────────────────┘
```

## 🔧 Configurações Avançadas

### 📋 **Tipos de eventos gerados**:
- 🟦 **Aula Teórica**: Eventos com recorrência alternada
- 🟩 **Aula Prática**: Eventos sem conflito
- **UC específica**: Se vinculada ao professor
- **Horários**: Respeitam disponibilidade configurada

### ⚙️ **Parâmetros configuráveis**:
- **Mês de início**: 1-12 (Janeiro a Dezembro)
- **Ano**: 2024-2030
- **Duração**: 3-8 meses (padrão: 5)

## 🚨 Observações Importantes

1. **Disponibilidade obrigatória**: Professores SEM disponibilidade configurada não são incluídos
2. **UCs opcionais**: Funciona mesmo sem UCs vinculadas (mostra "Aula")  
3. **Feriados**: Automaticamente excluídos do cronograma
4. **Dias úteis**: Segunda a sexta (19h-23h), Sábado (10h-12h)
5. **Backup**: Eventos são salvos no localStorage também

## 🎉 Resultado Esperado

Após executar a alocação, você terá:
- **~84 eventos** para um semestre de 5 meses
- **~21 semanas** de aulas
- **Professores alternando** automaticamente em conflitos
- **Calendário completo** sem trabalho manual!

---

## 🔥 Esta funcionalidade resolve exatamente o que você pediu:

> *"eu quero que quando tiver os cadastro dele que ja esta funcionado na hora de eu vou clicar para gerar calendario faca algo que consigo alocar os professores ao longo do semestre as aulas dele ali, se caso tiver dois no mesmo dia ou mais no mesmo dia faca que seja uma semana e o professor que da auala e outra semana e outro professor que de aula isso durante todo o semestre"*

✅ **Cadastros funcionando**: Usa professores já cadastrados  
✅ **Gerar calendário**: Botão integrado no calendário  
✅ **Alocar ao longo do semestre**: 5 meses automáticos  
✅ **Conflitos resolvidos**: Alternância semanal entre professores  
✅ **Todo o semestre**: Aproximadamente 21 semanas

**Sua funcionalidade está pronta e funcionando! 🚀**
