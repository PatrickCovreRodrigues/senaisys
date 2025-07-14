# 🚀 Instruções para Iniciar o Sistema de Alocação Semestral

## 📋 Problema Identificado e Solucionado

O problema era que a rota estava sendo registrada com prefixo duplo:
- Router: `/alocacao` + Main.py: `/api` = `/api/alocacao`
- Mas o endpoint `/processar-semestre` ficava como `/api/processar-semestre`

**✅ CORREÇÃO APLICADA:**
- Removido prefixo duplicado no router
- Ajustado main.py para usar `/api/alocacao` 
- Agora a rota correta é: `/api/alocacao/processar-semestre`

## 🛠️ Como Iniciar o Servidor

### 1. Abra o Terminal/PowerShell
```powershell
cd "c:\Users\Patrick Covre\OneDrive\Área de Trabalho\agrvai\senaisys\backend"
```

### 2. Execute o Servidor
```powershell
python run.py
```

### 3. Verifique se Funcionou
O servidor deve mostrar:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 4. Teste a Conectividade (Opcional)
Em outro terminal, execute:
```powershell
python teste_conectividade.py
```

## 🎯 Como Usar no Frontend

1. **Inicie o servidor backend** (passo acima)
2. **Inicie o frontend Vue.js**:
   ```powershell
   cd "c:\Users\Patrick Covre\OneDrive\Área de Trabalho\agrvai\senaisys\vue-project"
   npm run dev
   ```
3. **Acesse a aplicação** em `http://localhost:5173`
4. **Vá para a seção de Calendário**
5. **Clique em "Gerar Calendário com Alocação Semestral"**
6. **Configure os parâmetros:**
   - Mês de início (ex: 2 = Fevereiro)
   - Ano de início (ex: 2025)
   - Duração em meses (ex: 5 = 5 meses)

## 🔧 Funcionalidades Implementadas

### ✅ Backend (`alocacao_recorrencia.py`)
- Detecção automática de conflitos de horários
- Algoritmo de alternância semanal entre professores
- Geração de eventos de calendário para todo o semestre
- Consideração de feriados e dias úteis

### ✅ Endpoint API (`/api/alocacao/processar-semestre`)
- Recebe parâmetros de configuração do semestre
- Processa alocação para período completo
- Retorna eventos de calendário gerados

### ✅ Frontend (`GerarCalendario.vue`)
- Botão para alocação semestral
- Dialog de configuração
- Integração com API
- Feedback visual do processo

## 🐛 Solução de Problemas

### Erro 404 - Rota não encontrada
- ✅ **RESOLVIDO**: Prefixo de rota corrigido

### Erro 422 - Dados inválidos
- Verifique se os parâmetros estão corretos
- Mês: 1-12, Ano: 4 dígitos, Duração: número positivo

### Erro 500 - Erro interno
- Verifique se há professores e UCs cadastrados
- Verifique se há horários de disponibilidade configurados

### Servidor não inicia
- Verifique se o Python está instalado
- Verifique se as dependências estão instaladas: `pip install -r requirements.txt`
- Verifique se a porta 8000 não está em uso

## 📁 Arquivos Modificados

- `backend/main.py` - Correção do prefixo de rota
- `backend/routers/alocacao.py` - Remoção do prefixo duplicado
- `backend/alocacao_recorrencia.py` - Novo módulo (já existia)
- `vue-project/src/components/GerarCalendario.vue` - Interface
- `vue-project/src/services/api.js` - Método de API

## 🎉 Próximos Passos

1. **Teste o sistema** com dados reais
2. **Ajuste parâmetros** conforme necessário
3. **Monitore logs** para identificar possíveis melhorias
4. **Documente casos de uso** específicos da sua escola

---
**💡 Lembre-se:** O sistema agora detecta automaticamente quando há conflitos de horários e alterna os professores semanalmente ao longo do semestre!
