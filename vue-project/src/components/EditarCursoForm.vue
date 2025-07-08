<template>
  <main class="main-content">
    <div class="container">
      <v-form @submit.prevent="salvar">
        <div class="form-container">
          <v-text-field
            v-model="formData.nomeCurso"
            label="Nome Curso"
            variant="outlined"
            class="mb-4"
            color="indigo"
            hide-details
          ></v-text-field>

          <v-text-field
            v-model="formData.cargaHoraria"
            label="Carga horária"
            variant="outlined"
            type="number"
            class="mb-4"
            color="indigo"
            hide-details
          ></v-text-field>

          <v-select
            v-model="formData.fases"
            label="Fases"
            :items="fasesOptions"
            variant="outlined"
            class="mb-6"
            color="indigo"
            hide-details
          ></v-select>
        </div>

        <div class="action-buttons">
          <v-btn
            @click="goBack"
            variant="outlined"
            size="large"
            class="btn-voltar"
          >
            Voltar
          </v-btn>
          <v-btn
            @click="salvar"
            variant="flat"
            size="large"
            class="btn-salvar"
            :loading="isLoading"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Salvando...' : 'Salvar' }}
          </v-btn>
        </div>
      </v-form>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { cursosAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const router = useRouter()
const route = useRoute()
const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()

// Form data
const formData = ref({
  nomeCurso: '',
  cargaHoraria: '',
  fases: ''
})
const cursoId = ref(null)

// Opções do select de fases
const fasesOptions = [
  { title: 'Fase 1', value: 1 },
  { title: 'Fase 2', value: 2 },
  { title: 'Fase 3', value: 3 },
  { title: 'Fase 4', value: 4 },
  { title: 'Fase 5', value: 5 }
]

// Carregar dados do curso ao montar o componente
onMounted(async () => {
  await carregarCurso()
})

const carregarCurso = async () => {
  const id = route.query.id
  if (!id) {
    showError('ID do curso não fornecido')
    router.push('/editando-curso')
    return
  }

  try {
    const curso = await withLoading(
      () => cursosAPI.obter(id),
      'Carregando dados do curso...'
    )

    // Preencher formulário com dados do curso
    cursoId.value = curso.id
    formData.value = {
      nomeCurso: curso.nome,
      cargaHoraria: curso.carga_horaria.toString(),
      fases: curso.fases || ''
    }
  } catch (error) {
    console.error('Erro ao carregar curso:', error)
    showError('Erro ao carregar dados do curso')
    router.push('/editando-curso')
  }
}

const goBack = () => {
  router.push('/editando-curso')
}

const salvar = async () => {
  if (!formData.value.nomeCurso || !formData.value.cargaHoraria) {
    showError('Por favor, preencha todos os campos obrigatórios')
    return
  }

  try {
    const dadosCurso = {
      nome: formData.value.nomeCurso,
      carga_horaria: parseInt(formData.value.cargaHoraria),
      fases: formData.value.fases ? parseInt(formData.value.fases) : null
    }

    await withLoading(
      () => cursosAPI.atualizar(cursoId.value, dadosCurso),
      'Salvando alterações...'
    )

    showSuccess('Curso atualizado com sucesso!')
    router.push('/editando-curso')
  } catch (error) {
    console.error('Erro ao atualizar curso:', error)
    showError(error.message || 'Erro ao atualizar curso')
  }
}
</script>

<style scoped>
.main-content {
  padding: 4rem 4rem;
  min-height: calc(100vh - 120px);
  width: 100%;
  margin: 0;
  background-color: #E8E7E7;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  max-width: 650px;
  width: 100%;
  margin: 0 auto;
  background-color: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 3rem;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
}

/* Estilos para os campos Vuetify */
:deep(.v-text-field .v-field),
:deep(.v-select .v-field) {
  border-radius: 8px !important;
}

:deep(.v-text-field .v-field__input),
:deep(.v-select .v-field__input) {
  padding: 16px !important;
  font-size: 1.1rem !important;
  color: #000000 !important;
}

:deep(.v-text-field input::placeholder) {
  color: #000000 !important;
  opacity: 1 !important;
}

:deep(.v-label) {
  color: #000000 !important;
  font-size: 0.9rem !important;
  font-weight: 400 !important;
}

/* Estilos para os botões */
.btn-voltar {
  border-color: #D1D5DB !important;
  color: #374151 !important;
  background-color: #D1D5DB !important;
  padding: 1rem 3rem !important;
  min-width: 150px !important;
}

.btn-voltar:hover {
  background-color: #9CA3AF !important;
  border-color: #9CA3AF !important;
}

.btn-salvar {
  background-color: #6B7280 !important;
  color: white !important;
  padding: 1rem 3rem !important;
  min-width: 150px !important;
}

.btn-salvar:hover {
  background-color: #4B5563 !important;
}

:deep(.v-btn) {
  text-transform: none !important;
  font-weight: 500 !important;
  font-size: 1.1rem !important;
}

/* Responsive design - Tablet */
@media (max-width: 1024px) {
  .main-content {
    padding: 3rem 2rem;
  }
  
  .container {
    padding: 2rem;
  }
}

/* Responsive design - Mobile */
@media (max-width: 768px) {
  .main-content {
    padding: 2rem 1rem;
  }

  .container {
    padding: 1.5rem;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 1rem;
  }
  
  .btn-voltar,
  .btn-salvar {
    width: 100% !important;
  }
}

/* Small mobile */
@media (max-width: 480px) {
  :deep(.v-text-field .v-field__input),
  :deep(.v-select .v-field__input) {
    padding: 12px !important;
    font-size: 1rem !important;
  }
}
</style> 