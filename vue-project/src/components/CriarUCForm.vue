<template>
  <main class="main-content">
    <div class="container">
      <div class="form-header">
        <button @click="goBack" class="back-button">← Voltar</button>
        <h1 class="page-title">Criar Nova UC</h1>
      </div>
      
      <div class="form-container">
        <v-form ref="form" v-model="valid" lazy-validation>
          <div class="form-row">
            <v-text-field
              v-model="nomeUC"
              label="Nome UC"
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
              label="Carga horária"
              :rules="cargaRules"
              required
              outlined
              dense
              type="number"
              class="custom-text-field"
            ></v-text-field>
          </div>
          
          <div class="form-row">
            <div class="select-with-icon">
              <v-select
                v-model="vincularDocente"
                :items="docenteOptions"
                :loading="loadingOptions"
                label="Vincular Docente (Opcional)"
                outlined
                dense
                clearable
                class="custom-select"
              ></v-select>
              <div class="select-icon">VD</div>
            </div>
          </div>
          
          <div class="form-row">
            <v-select
              v-model="vincularCurso"
              :items="cursoOptions"
              :loading="loadingOptions"
              label="Vincular Curso (Opcional)"
              outlined
              dense
              clearable
              class="custom-select"
            ></v-select>
          </div>
          
          <div class="form-actions">
            <v-btn 
              @click="salvarUC" 
              :disabled="!valid || isLoading"
              :loading="isLoading"
              color="primary"
              large
              class="save-button"
            >
              {{ isLoading ? 'Criando...' : 'Criar UC' }}
            </v-btn>
          </div>
        </v-form>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ucsAPI, docentesAPI, cursosAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const router = useRouter()
const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()

// Form data
const valid = ref(false)
const nomeUC = ref('')
const cargaHoraria = ref('')
const vincularDocente = ref('')
const vincularCurso = ref('')

// Options para selects
const docenteOptions = ref([])
const cursoOptions = ref([])
const loadingOptions = ref(false)

// Form validation rules
const nomeRules = [
  v => !!v || 'Nome da UC é obrigatório',
  v => (v && v.length >= 3) || 'Nome deve ter pelo menos 3 caracteres'
]

const cargaRules = [
  v => !!v || 'Carga horária é obrigatória',
  v => (v && v > 0) || 'Carga horária deve ser maior que 0'
]

// Carregar opções ao montar o componente
onMounted(async () => {
  await carregarOpcoes()
})

const carregarOpcoes = async () => {
  loadingOptions.value = true
  try {
    // Carregar docentes e cursos em paralelo
    const [docentes, cursos] = await Promise.all([
      docentesAPI.listar(),
      cursosAPI.listar()
    ])

    docenteOptions.value = docentes.map(docente => ({
      title: docente.nome,
      value: docente.id
    }))

    cursoOptions.value = cursos.map(curso => ({
      title: curso.nome,
      value: curso.id
    }))
  } catch (error) {
    console.error('Erro ao carregar opções:', error)
    showError('Erro ao carregar lista de docentes e cursos')
  } finally {
    loadingOptions.value = false
  }
}

// Methods
const goBack = () => {
  router.push('/novo-cadastro')
}

const salvarUC = async () => {
  if (!valid.value) {
    showError('Por favor, preencha todos os campos obrigatórios')
    return
  }

  try {
    const dadosUC = {
      nome: nomeUC.value,
      carga_horaria: parseInt(cargaHoraria.value),
      docente_id: vincularDocente.value || null,
      curso_id: vincularCurso.value || null
    }

    await withLoading(
      () => ucsAPI.criar(dadosUC),
      'Criando UC...'
    )

    showSuccess('UC criada com sucesso!')
    router.push('/novo-cadastro')
  } catch (error) {
    console.error('Erro ao criar UC:', error)
    showError(error.message || 'Erro ao criar UC')
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

.select-with-icon {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.select-with-icon .v-select {
  flex: 1;
}

.select-icon {
  width: 40px;
  height: 40px;
  background-color: #9CA3AF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: bold;
  border-radius: 6px;
  flex-shrink: 0;
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
  
  .select-with-icon {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .form-actions {
    justify-content: stretch;
  }
  
  .save-button {
    width: 100%;
  }
}
</style> 