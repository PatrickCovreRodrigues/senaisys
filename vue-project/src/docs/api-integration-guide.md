# 🔗 Guia de Integração da API

## 📋 Visão Geral

Este guia mostra como integrar o frontend Vue.js com o backend FastAPI usando os serviços criados.

## 🚀 Configuração Inicial

### 1. Importar os serviços necessários:

```javascript
import { cursosAPI, docentesAPI, ucsAPI, calendarioAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'
```

### 2. Configurar os composables:

```javascript
const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()
```

## 📚 Exemplos de Uso por Entidade

### CURSOS

#### Criar um novo curso:
```javascript
const criarCurso = async () => {
  try {
    const dadosCurso = {
      nome: "Análise e Desenvolvimento de Sistemas",
      carga_horaria: 2400,
      fases: "Fase 1,Fase 2,Fase 3,Fase 4"
    }

    const cursoNovo = await withLoading(
      () => cursosAPI.criar(dadosCurso),
      'Criando curso...'
    )

    showSuccess('Curso criado com sucesso!')
    return cursoNovo
  } catch (error) {
    showError(error.message || 'Erro ao criar curso')
  }
}
```

#### Listar cursos:
```javascript
const carregarCursos = async () => {
  try {
    const cursos = await cursosAPI.listar()
    return cursos.map(curso => ({
      id: curso.id,
      nome: curso.nome,
      carga_horaria: curso.carga_horaria,
      fases: curso.fases
    }))
  } catch (error) {
    showError('Erro ao carregar cursos')
    return []
  }
}
```

#### Atualizar curso:
```javascript
const atualizarCurso = async (id, dadosAtualizados) => {
  try {
    const cursoAtualizado = await withLoading(
      () => cursosAPI.atualizar(id, dadosAtualizados),
      'Atualizando curso...'
    )

    showSuccess('Curso atualizado com sucesso!')
    return cursoAtualizado
  } catch (error) {
    showError(error.message || 'Erro ao atualizar curso')
  }
}
```

### DOCENTES

#### Criar docente com disponibilidade:
```javascript
const criarDocente = async () => {
  try {
    const dadosDocente = {
      nome: "Prof. João Silva",
      disciplinas: ["Lógica de Programação", "Python"],
      disponibilidade: {
        "segunda": true,
        "terca": true,
        "quarta": false,
        "quinta": true,
        "sexta": true,
        "sabado": false
      },
      horarios: {
        "segunda": { "inicio": "08:00", "fim": "17:00" },
        "terca": { "inicio": "08:00", "fim": "17:00" },
        "quarta": { "inicio": "", "fim": "" },
        "quinta": { "inicio": "13:00", "fim": "17:00" },
        "sexta": { "inicio": "08:00", "fim": "12:00" },
        "sabado": { "inicio": "", "fim": "" }
      }
    }

    const docenteNovo = await withLoading(
      () => docentesAPI.criar(dadosDocente),
      'Criando docente...'
    )

    showSuccess('Docente criado com sucesso!')
    return docenteNovo
  } catch (error) {
    showError(error.message || 'Erro ao criar docente')
  }
}
```

#### Carregar opções para select:
```javascript
const carregarDocentesParaSelect = async () => {
  try {
    const docentes = await docentesAPI.listar()
    return docentes.map(docente => ({
      title: docente.nome,
      value: docente.id
    }))
  } catch (error) {
    showError('Erro ao carregar docentes')
    return []
  }
}
```

### UCS

#### Criar UC com vinculações:
```javascript
const criarUC = async () => {
  try {
    const dadosUC = {
      nome: "Lógica de Programação",
      carga_horaria: 80,
      docente_id: 1, // ID do docente (opcional)
      curso_id: 1    // ID do curso (opcional)
    }

    const ucNova = await withLoading(
      () => ucsAPI.criar(dadosUC),
      'Criando UC...'
    )

    showSuccess('UC criada com sucesso!')
    return ucNova
  } catch (error) {
    showError(error.message || 'Erro ao criar UC')
  }
}
```

#### Vincular docente à UC:
```javascript
const vincularDocenteUC = async (ucId, docenteId) => {
  try {
    await withLoading(
      () => ucsAPI.vincularDocente(ucId, docenteId),
      'Vinculando docente...'
    )

    showSuccess('Docente vinculado com sucesso!')
  } catch (error) {
    showError(error.message || 'Erro ao vincular docente')
  }
}
```

### CALENDÁRIOS

#### Gerar calendário:
```javascript
const gerarCalendario = async () => {
  try {
    const dadosGeracao = {
      curso_id: 1,
      mes: 4,
      ano: 2025,
      fases_selecionadas: [1, 2]
    }

    const calendario = await withLoading(
      () => calendarioAPI.gerar(dadosGeracao),
      'Gerando calendário...'
    )

    showSuccess('Calendário gerado com sucesso!')
    return calendario
  } catch (error) {
    showError(error.message || 'Erro ao gerar calendário')
  }
}
```

#### Carregar calendário de um mês específico:
```javascript
const carregarCalendarioMes = async (cursoId, ano, mes) => {
  try {
    const calendario = await calendarioAPI.obterMes(cursoId, ano, mes)
    return calendario
  } catch (error) {
    // Calendário não existe para este período
    return null
  }
}
```

## 🔄 Padrões de Loading e Estados

### Template com loading states:
```vue
<template>
  <div>
    <!-- Botão com loading -->
    <v-btn
      @click="salvar"
      :disabled="isLoading"
      :loading="isLoading"
      color="primary"
    >
      {{ isLoading ? 'Salvando...' : 'Salvar' }}
    </v-btn>

    <!-- Lista com loading -->
    <div v-if="loadingCursos">
      <v-progress-circular indeterminate></v-progress-circular>
      <p>Carregando cursos...</p>
    </div>
    <div v-else>
      <div v-for="curso in cursos" :key="curso.id">
        {{ curso.nome }}
      </div>
    </div>
  </div>
</template>
```

### Script com estados:
```javascript
<script setup>
import { ref, onMounted } from 'vue'
import { cursosAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()

const cursos = ref([])
const loadingCursos = ref(false)

onMounted(async () => {
  await carregarCursos()
})

const carregarCursos = async () => {
  loadingCursos.value = true
  try {
    cursos.value = await cursosAPI.listar()
  } catch (error) {
    showError('Erro ao carregar cursos')
  } finally {
    loadingCursos.value = false
  }
}

const salvar = async () => {
  try {
    await withLoading(
      () => cursosAPI.criar(dadosCurso),
      'Salvando...'
    )
    showSuccess('Salvo com sucesso!')
  } catch (error) {
    showError(error.message)
  }
}
</script>
```

## 🛠️ Validação e Tratamento de Erros

### Validação antes de enviar:
```javascript
const validarDados = (dados) => {
  if (!dados.nome || dados.nome.length < 3) {
    showError('Nome deve ter pelo menos 3 caracteres')
    return false
  }
  
  if (!dados.carga_horaria || dados.carga_horaria <= 0) {
    showError('Carga horária deve ser maior que 0')
    return false
  }
  
  return true
}

const salvar = async () => {
  if (!validarDados(formData.value)) return
  
  // Continuar com o salvamento...
}
```

### Tratamento de erros específicos:
```javascript
const tratarErro = (error) => {
  if (error.message.includes('não encontrado')) {
    showError('Registro não encontrado')
  } else if (error.message.includes('conexão')) {
    showError('Erro de conexão. Verifique se o backend está rodando.')
  } else {
    showError(error.message || 'Erro inesperado')
  }
}
```

## 📱 Exemplo de Componente Completo

```vue
<template>
  <div class="form-container">
    <v-form v-model="valid">
      <v-text-field
        v-model="nome"
        label="Nome"
        :rules="nomeRules"
        required
      ></v-text-field>

      <v-select
        v-model="docenteId"
        :items="docenteOptions"
        :loading="loadingDocentes"
        label="Docente"
        clearable
      ></v-select>

      <v-btn
        @click="salvar"
        :disabled="!valid || isLoading"
        :loading="isLoading"
        color="primary"
      >
        {{ isLoading ? 'Salvando...' : 'Salvar' }}
      </v-btn>
    </v-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ucsAPI, docentesAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()

// Form data
const valid = ref(false)
const nome = ref('')
const docenteId = ref(null)

// Options
const docenteOptions = ref([])
const loadingDocentes = ref(false)

// Validation rules
const nomeRules = [
  v => !!v || 'Nome é obrigatório',
  v => (v && v.length >= 3) || 'Nome deve ter pelo menos 3 caracteres'
]

// Lifecycle
onMounted(async () => {
  await carregarDocentes()
})

// Methods
const carregarDocentes = async () => {
  loadingDocentes.value = true
  try {
    const docentes = await docentesAPI.listar()
    docenteOptions.value = docentes.map(d => ({
      title: d.nome,
      value: d.id
    }))
  } catch (error) {
    showError('Erro ao carregar docentes')
  } finally {
    loadingDocentes.value = false
  }
}

const salvar = async () => {
  if (!valid.value) {
    showError('Preencha todos os campos obrigatórios')
    return
  }

  try {
    const dados = {
      nome: nome.value,
      docente_id: docenteId.value
    }

    await withLoading(
      () => ucsAPI.criar(dados),
      'Salvando UC...'
    )

    showSuccess('UC criada com sucesso!')
    // Limpar form ou navegar
    nome.value = ''
    docenteId.value = null
  } catch (error) {
    showError(error.message || 'Erro ao salvar UC')
  }
}
</script>
```

## 🔧 Configuração da API Base URL

Para usar em diferentes ambientes, configure a URL base:

```javascript
// .env.development
VITE_API_BASE_URL=http://127.0.0.1:8000/api

// .env.production  
VITE_API_BASE_URL=https://sua-api-producao.com/api
```

```javascript
// services/api.js
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  // ...
})
```

## ✅ Checklist de Integração

- [ ] Axios instalado
- [ ] Serviços de API criados
- [ ] Composables de loading e notificação configurados
- [ ] Componente de notificação global adicionado ao App.vue
- [ ] Componentes atualizados para usar API real
- [ ] Loading states implementados
- [ ] Tratamento de erros configurado
- [ ] Validação de formulários implementada
- [ ] Backend rodando na porta 8000

## 🚀 Iniciar Desenvolvimento

1. **Backend**: `cd backend && python run.py`
2. **Frontend**: `cd vue-project && npm run dev`
3. **Teste**: Abrir http://localhost:5173 e testar criação/listagem 