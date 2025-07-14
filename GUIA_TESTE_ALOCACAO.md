# Guia de Teste - Funcionalidade de Alocação Automática

## Pré-requisitos
Antes de testar a funcionalidade, certifique-se de que você tem:

1. **Docentes cadastrados** com disponibilidade configurada
2. **Cursos cadastrados** no sistema
3. **UCs (Unidades Curriculares)** associadas aos cursos
4. **Backend e frontend** funcionando

## Como Testar

### 1. Preparar o Ambiente

#### Backend:
```bash
cd senaisys/backend
python -m uvicorn main:app --reload
```

#### Frontend:
```bash
cd senaisys/vue-project
npm install
npm run dev
```

### 2. Verificar Dados Necessários

#### 2.1 Verificar se há docentes cadastrados:
- Acesse: `http://localhost:8000/api/docentes/`
- Certifique-se de que há pelo menos um docente com:
  - `disponibilidade` configurada (ex: `{"segunda": true, "terca": true}`)
  - `horarios` definidos (ex: `{"segunda": {"inicio": "19:00", "fim": "22:00"}}`)

#### 2.2 Verificar se há cursos cadastrados:
- Acesse: `http://localhost:8000/api/cursos/`
- Anote o `id` do curso que será usado

#### 2.3 Verificar se há UCs associadas:
- Acesse: `http://localhost:8000/api/ucs/`
- Certifique-se de que há UCs com `curso_id` preenchido

### 3. Testar a Funcionalidade

#### 3.1 Pelo Frontend (Recomendado):
1. Acesse: `http://localhost:5173/gerar-calendario`
2. **Passo 1**: Selecione um curso
3. **Passo 2**: Escolha as fases desejadas
4. **Passo 3**: Na tela do calendário, clique no botão **"Gerar Alocação Automática"**
5. Aguarde o processamento
6. Verifique o dialog de estatísticas
7. Observe as aulas geradas no calendário (eventos roxos com borda)

#### 3.2 Pelo API (Teste Direto):
```bash
curl -X POST "http://localhost:8000/api/calendario/gerar-alocacao-automatica" \
  -H "Content-Type: application/json" \
  -d '{
    "curso_id": 1,
    "mes_inicio": 4,
    "ano_inicio": 2025,
    "duracao_semanas": 20
  }'
```

### 4. Verificar Resultados

#### 4.1 No Frontend:
- **Calendário**: Deve mostrar eventos roxos com aulas automáticas
- **Estatísticas**: Dialog deve mostrar números de aulas e docentes
- **Eventos**: Clique nos eventos para ver detalhes (professor, UC, horário)

#### 4.2 No Banco de Dados:
- Tabela `assoc_udd`: Deve ter novos registros de alocação
- Tabela `calendarios`: Deve ter o calendário com eventos JSON

#### 4.3 Esperado:
- **400 aulas** (aprox): 20 semanas × 5 dias × 4 horários = 400 slots
- **Distribuição equilibrada**: Professores alternando semanalmente
- **Horários respeitados**: Apenas nos horários de disponibilidade

### 5. Cenários de Teste

#### 5.1 Cenário Básico:
- 2 professores disponíveis segunda a sexta (19:00-22:00)
- 1 curso com 3 UCs
- Resultado: Professores alternando semanalmente

#### 5.2 Cenário com Restrições:
- Professor A: Disponível segunda/quarta (19:00-21:00)
- Professor B: Disponível terça/quinta (20:00-22:00)
- Resultado: Aulas só nos horários disponíveis

#### 5.3 Cenário Complexo:
- 5 professores com diferentes disponibilidades
- 2 cursos com múltiplas UCs
- Resultado: Distribuição otimizada

### 6. Solução de Problemas

#### Erro: "Nenhum docente encontrado"
- Verificar se há docentes cadastrados
- Verificar se têm disponibilidade configurada

#### Erro: "Nenhuma UC encontrada"
- Verificar se há UCs associadas ao curso
- Verificar se o `curso_id` está correto

#### Calendário vazio:
- Verificar se docentes têm horários configurados
- Verificar se há conflito de horários

#### Poucos eventos gerados:
- Verificar disponibilidade dos docentes
- Verificar se horários batem com os slots (19:00-22:00)

### 7. Validações Importantes

#### 7.1 Alternância de Professores:
- Professor A na semana 1, Professor B na semana 2
- Mesmo slot deve alternar entre professores disponíveis

#### 7.2 Respeito aos Horários:
- Nenhuma aula fora do horário de disponibilidade
- Horários de início/fim respeitados

#### 7.3 Persistência:
- Dados salvos no banco (`assoc_udd`)
- Eventos salvos no localStorage
- Estatísticas disponíveis

### 8. Dados de Exemplo

#### Docente de Exemplo:
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "disponibilidade": {
    "segunda": true,
    "terca": true,
    "quarta": true,
    "quinta": true,
    "sexta": true
  },
  "horarios": {
    "segunda": {"inicio": "19:00", "fim": "22:00"},
    "terca": {"inicio": "19:00", "fim": "22:00"},
    "quarta": {"inicio": "19:00", "fim": "22:00"},
    "quinta": {"inicio": "19:00", "fim": "22:00"},
    "sexta": {"inicio": "19:00", "fim": "22:00"}
  }
}
```

#### Curso de Exemplo:
```json
{
  "nome": "Desenvolvimento Web",
  "carga_horaria": 360,
  "fases": "1,2,3,4"
}
```

#### UC de Exemplo:
```json
{
  "nome": "Programação Web",
  "carga_horaria": 60,
  "curso_id": 1
}
```

### 9. Recursos Adicionais

- **Estatísticas**: Clique em "Ver Estatísticas" para análise detalhada
- **Limpeza**: Use "Limpar Todos" para remover eventos
- **Navegação**: Use setas para navegar entre meses
- **Edição**: Clique em eventos para editar manualmente

### 10. Logs e Debug

Para acompanhar o processamento:
- Backend: Logs aparecem no terminal do uvicorn
- Frontend: Abra DevTools (F12) → Console para logs detalhados
- Banco: Consulte tabelas `assoc_udd` e `calendarios`

---

## Sucesso Esperado

Após executar a funcionalidade, você deve ver:
- ✅ Calendário preenchido com aulas automáticas
- ✅ Professores alternando semanalmente
- ✅ Estatísticas detalhadas
- ✅ Dados persistidos no banco
- ✅ Interface responsiva e intuitiva

**A funcionalidade está pronta para uso!** 🎉
