<template>
  <main class="main-content">
    <div class="container">
      <div class="form-header">
        <button @click="goBack" class="back-button">← Voltar</button>
        <h1 class="page-title">Criar Novo Curso</h1>
      </div>
      
      <div class="form-container">
        <v-form ref="form" v-model="valid" lazy-validation>
          <div class="form-row">
            <v-text-field
              v-model="nomeCurso"
              label="Nome do Curso"
              :rules="nomeRules"
              required
              outlined
              dense
              class="custom-text-field"
            ></v-text-field>
          </div>
          
          <div class="form-row">
            <v-text-field
              v-model="cargaHoraria"
              label="Carga Horária"
              :rules="cargaRules"
              required
              outlined
              dense
              type="number"
              class="custom-text-field"
            ></v-text-field>
          </div>
          
          <div class="form-row">
            <v-select
              v-model="fases"
              :items="fasesOptions"
              label="Fases"
              outlined
              dense
              class="custom-select"
            ></v-select>
          </div>
          
          <div class="form-actions">
            <v-btn 
              @click="salvarCurso" 
              :disabled="!valid || isLoading"
              :loading="isLoading"
              color="primary"
              large
              class="save-button"
            >
              {{ isLoading ? 'Criando...' : 'Criar Curso' }}
            </v-btn>
          </div>
        </v-form>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { cursosAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const router = useRouter()
const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()

// Form data
const valid = ref(false)
const nomeCurso = ref('')
const cargaHoraria = ref('')
const fases = ref('')

// Form validation rules
const nomeRules = [
  v => !!v || 'Nome do curso é obrigatório',
  v => (v && v.length >= 3) || 'Nome deve ter pelo menos 3 caracteres'
]

const cargaRules = [
  v => !!v || 'Carga horária é obrigatória',
  v => (v && v > 0) || 'Carga horária deve ser maior que 0'
]

// Select options
const fasesOptions = [
  'Fase 1',
  'Fase 2', 
  'Fase 3',
  'Fase 4'
]

// Methods
const goBack = () => {
  router.push('/novo-cadastro')
}

const salvarCurso = async () => {
  if (!valid.value) {
    showError('Por favor, preencha todos os campos obrigatórios')
    return
  }

  try {
    const dadosCurso = {
      nome: nomeCurso.value,
      carga_horaria: parseInt(cargaHoraria.value),
      fases: fases.value
    }

    await withLoading(
      () => cursosAPI.criar(dadosCurso),
      'Criando curso...'
    )

    showSuccess('Curso criado com sucesso!')
    router.push('/novo-cadastro')
  } catch (error) {
    console.error('Erro ao criar curso:', error)
    showError(error.message || 'Erro ao criar curso')
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
}

.container {
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  background-color: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 3rem;
}

.back-button {
  background: none;
  border: none;
  color: #4F46E5;
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: rgba(79, 70, 229, 0.1);
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.form-container {
  max-width: 600px;
}

.form-row {
  margin-bottom: 2rem;
}

.form-actions {
  margin-top: 3rem;
  display: flex;
  justify-content: flex-end;
}

.save-button {
  min-width: 150px;
}

/* Vuetify overrides para garantir texto preto */
:deep(.v-text-field input) {
  color: black !important;
}

:deep(.v-text-field .v-field__input) {
  color: black !important;
}

:deep(.v-text-field .v-field__field .v-field__input) {
  color: black !important;
}

:deep(.v-select .v-field__input) {
  color: black !important;
}

:deep(.v-select .v-select__selection) {
  color: black !important;
}

:deep(.v-text-field input::placeholder) {
  color: #000000 !important;
  opacity: 1 !important;
}

:deep(.v-text-field .v-field__input::placeholder) {
  color: #000000 !important;
  opacity: 1 !important;
}

:deep(.v-label) {
  color: #000000 !important;
  font-size: 0.9rem !important;
  font-weight: 400 !important;
}

:deep(.v-select .v-label) {
  color: #000000 !important;
}

/* Responsive design */
@media (max-width: 768px) {
  .main-content {
    padding: 2rem 1rem;
  }
  
  .container {
    padding: 2rem 1.5rem;
  }
  
  .form-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .form-actions {
    justify-content: stretch;
  }
  
  .save-button {
    width: 100%;
  }
}
</style> 