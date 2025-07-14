# Funcionalidade de Alocação Automática de Professores

## Descrição
Esta funcionalidade permite gerar automaticamente um calendário completo de aulas para um semestre letivo, alocando professores com base em sua disponibilidade e implementando um sistema de alternância para otimizar a distribuição das aulas.

## Características Implementadas

### 1. Alocação Automática por Semestre
- **Duração**: 20 semanas (~5 meses)
- **Período**: Configurável (mês e ano de início)
- **Dias úteis**: Segunda a sexta-feira
- **Horários**: 4 horários noturnos por dia (19:00, 20:00, 21:00, 22:00)

### 2. Sistema de Alternância de Professores
- **Regra principal**: Quando há múltiplos professores disponíveis para o mesmo horário, o sistema alterna entre eles semanalmente
- **Algoritmo**: Escolhe sempre o professor que há mais tempo não deu aula naquele slot específico
- **Controle**: Mantém histórico da última semana em que cada professor foi alocado

### 3. Respeito à Disponibilidade
- **Verificação de dias**: Só aloca professores nos dias em que estão disponíveis
- **Verificação de horários**: Respeita os horários específicos cadastrados para cada professor
- **Fallback**: Se não há horário específico, assume disponibilidade nos horários padrão

### 4. Integração com o Sistema
- **Banco de dados**: Salva automaticamente as alocações na tabela `Assoc_UDD`
- **Calendário visual**: Integra com o calendário existente
- **Persistência**: Salva eventos no localStorage para recuperação posterior

### 5. Estatísticas e Relatórios
- **Total de aulas geradas**
- **Número de docentes utilizados**
- **Média de aulas por docente**
- **Distribuição detalhada por professor**
- **Cobertura por semana**

## Como Usar

### No Frontend (Vue.js)
1. Acesse a página "Gerar Calendário"
2. Selecione um curso na primeira etapa
3. Escolha as fases desejadas na segunda etapa
4. Na terceira etapa (visualização do calendário), clique no botão **"Gerar Alocação Automática"**
5. O sistema irá:
   - Processar a alocação automática
   - Mostrar estatísticas em um dialog
   - Atualizar o calendário com as aulas geradas
   - Salvar no localStorage para persistência

### Via API (Backend)
```javascript
// Exemplo de chamada
const resultado = await calendarioAPI.gerarAlocacaoAutomatica({
  curso_id: 1,
  mes_inicio: 4,      // Abril
  ano_inicio: 2025,
  duracao_semanas: 20  // ~5 meses
})
```

## Estrutura dos Dados

### Evento Gerado
```javascript
{
  id: "auto_20250401_0_1",
  title: "Aula - Programação Web",
  subtitle: "Prof. João Silva",
  date: "2025-04-01",
  type: "aula-automatica",
  horarioInicio: "19:00",
  horarioFim: "20:00",
  ucId: 1,
  docenteId: 1,
  docenteNome: "João Silva",
  gerado_automaticamente: true,
  semana: 1
}
```

### Estatísticas Retornadas
```javascript
{
  total_docentes_utilizados: 5,
  total_aulas_geradas: 400,
  media_aulas_por_docente: 80,
  distribuicao_docentes: {
    1: 85,
    2: 78,
    3: 82,
    // ...
  },
  aulas_por_semana: 20,
  media_aulas_por_semana: 20
}
```

## Algoritmo de Alternância

### Estrutura de Controle
```javascript
alternancia_docentes = {
  (dia_semana, horario): [
    {
      docente: <objeto_docente>,
      ultima_semana: <numero_semana>
    },
    // ...
  ]
}
```

### Lógica de Seleção
1. Para cada slot de aula (dia + horário):
   - Busca docentes disponíveis naquele dia/horário
   - Verifica qual docente foi alocado há mais tempo
   - Seleciona o docente com menor `ultima_semana`
   - Atualiza o registro de `ultima_semana` do docente escolhido

## Vantagens da Implementação

1. **Distribuição Equilibrada**: Evita sobrecarga de alguns professores
2. **Flexibilidade**: Respeita totalmente a disponibilidade cadastrada
3. **Escalabilidade**: Funciona com qualquer número de professores
4. **Rastreabilidade**: Salva no banco para auditoria
5. **Facilidade de Uso**: Interface intuitiva no frontend
6. **Estatísticas**: Permite análise da distribuição

## Observações Técnicas

- O sistema funciona com base nos dados já cadastrados no banco
- Requer pelo menos um professor cadastrado com disponibilidade
- Requer pelo menos uma UC associada ao curso
- A duração padrão é de 20 semanas, mas pode ser configurada
- Os horários seguem o padrão noturno (19:00-23:00)
- O sistema ignora finais de semana automaticamente

## Próximos Passos Sugeridos

1. **Exportação para PDF**: Gerar relatórios em PDF
2. **Configuração de Horários**: Permitir personalizar os horários
3. **Regras Avançadas**: Implementar preferências de professores
4. **Notificações**: Enviar e-mails para professores alocados
5. **Validação de Conflitos**: Verificar sobreposições com outros calendários