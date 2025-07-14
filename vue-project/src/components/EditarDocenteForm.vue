<template>
  <main class="main-content">
    <div class="container">
      <div class="form-header">
        <h1 class="page-title">Editar Docente</h1>
      </div>
      
      <div v-if="isLoading" class="loading-container">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        <p>Carregando dados do docente...</p>
      </div>

      <v-form v-else @submit.prevent="salvar">
        <div class="form-container">
          <!-- Campo Nome Docente -->
          <v-text-field
            v-model="formData.nomeDocente"
            label="Nome Docente *"
            variant="outlined"
            class="mb-4"
            color="indigo"
            hide-details
          ></v-text-field>

          <!-- Campo Email -->
          <v-text-field
            v-model="formData.email"
            label="Email"
            type="email"
            variant="outlined"
            class="mb-4"
            color="indigo"
            hide-details
          ></v-text-field>

          <!-- Campo Especialidade -->
          <v-text-field
            v-model="formData.especialidade"
            label="Especialidade"
            variant="outlined"
            class="mb-6"
            color="indigo"
            hide-details
          ></v-text-field>

          <!-- Seção de UCs/Disciplinas -->
          <div class="disciplinas-section mb-6">
            <h3 class="section-title-small">UCs/Disciplinas do Docente</h3>
            
            <div class="selected-ucs" v-if="ucsVinculadas.length > 0">
              <div class="disciplina-chip" v-for="uc in ucsVinculadas" :key="uc.id">
                <div class="disciplina-icon">{{ uc.nome.split(' ').map(word => word[0]).join('').substring(0, 2).toUpperCase() }}</div>
                <span class="disciplina-text">{{ uc.nome }}</span>
                <button type="button" class="remove-btn" @click="removerUC(uc.id)">×</button>
              </div>
            </div>
            
            <button type="button" class="add-disciplina-btn" @click="abrirDialogUCs" :disabled="loadingUCs">
              <span class="plus-icon" v-if="!loadingUCs">+</span>
              <v-progress-circular v-else indeterminate size="20"></v-progress-circular>
            </button>
            
            <p class="info-text" v-if="ucsVinculadas.length === 0">
              Clique no botão + para vincular UCs ao docente
            </p>
          </div>

          <!-- Dialog para seleção de UCs -->
          <v-dialog v-model="showUCDialog" max-width="600">
            <v-card>
              <v-card-title class="text-h5">Selecionar UC</v-card-title>
              <v-card-text>
                <div v-if="loadingUCs" class="loading-container">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  <p>Carregando UCs...</p>
                </div>
                
                <div v-else-if="ucsDisponiveis.length === 0" class="empty-state">
                  <p>Nenhuma UC disponível.</p>
                </div>
                
                <div v-else>
                   <v-select
                     v-model="ucSelecionada"
                     :items="ucsDisponiveis.filter(uc => !ucsVinculadas.some(vinculada => vinculada.id === uc.id))"
                     item-title="nome"
                     item-value="id"
                     label="Escolha uma UC"
                     variant="outlined"
                     return-object
                   >
                     <template v-slot:item="{ props, item }">
                       <v-list-item v-bind="props">
                         <template v-slot:prepend>
                           <div class="uc-avatar">
                             {{ item.raw.nome.split(' ').map(word => word[0]).join('').substring(0, 2).toUpperCase() }}
                           </div>
                         </template>
                         <v-list-item-subtitle>
                           {{ item.raw.carga_horaria }}h 
                           <span v-if="item.raw.curso_nome">• {{ item.raw.curso_nome }}</span>
                         </v-list-item-subtitle>
                       </v-list-item>
                     </template>
                  </v-select>
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="grey" text @click="showUCDialog = false">Cancelar</v-btn>
                <v-btn color="primary" text @click="adicionarUC" :disabled="!ucSelecionada">Adicionar</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <!-- Seção Disponibilidade -->
          <div class="disponibilidade-section">
            <h3 class="section-title">Disponibilidade</h3>
            
            <div class="table-header">
              <div class="day-column"></div>
              <div class="time-column">Hora de início</div>
              <div class="time-column">Hora de término</div>
            </div>

            <div class="availability-row" v-for="day in diasSemana" :key="day.value">
              <div class="day-checkbox">
                <v-checkbox
                  v-model="formData.disponibilidade[day.value]"
                  :label="day.label"
                  color="indigo"
                  hide-details
                ></v-checkbox>
              </div>
              <div class="time-input">
                <v-select
                  v-model="formData.horarios[day.value].inicio"
                  :items="obterHorariosPorDia(day.value)"
                  variant="outlined"
                  hide-details
                  density="compact"
                ></v-select>
              </div>
              <div class="time-input">
                <v-select
                  v-model="formData.horarios[day.value].fim"
                  :items="obterHorariosPorDia(day.value)"
                  variant="outlined"
                  hide-details
                  density="compact"
                ></v-select>
              </div>
            </div>
          </div>
        </div>

        <div class="action-buttons">
          <v-btn
            @click="voltar"
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
          >
            {{ isSaving ? 'Salvando...' : 'Salvar Alterações' }}
          </v-btn>
        </div>
      </v-form>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { docentesAPI, ucsAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const router = useRouter()
const route = useRoute()
const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()
const isSaving = ref(false)
const docenteId = ref(null)

// Form data
const formData = ref({
  nomeDocente: '',
  email: '',
  especialidade: '',
  disponibilidade: {
    'segunda': false, 'terca': false, 'quarta': false,
    'quinta': false, 'sexta': false, 'sabado': false
  },
  horarios: {
    'segunda': { inicio: '', fim: '' }, 'terca': { inicio: '', fim: '' },
    'quarta': { inicio: '', fim: '' }, 'quinta': { inicio: '', fim: '' },
    'sexta': { inicio: '', fim: '' }, 'sabado': { inicio: '', fim: '' }
  }
})

// Dados das UCs
const ucsDisponiveis = ref([])
const ucsVinculadas = ref([])
const showUCDialog = ref(false)
const ucSelecionada = ref(null)
const loadingUCs = ref(false)

onMounted(async () => {
  docenteId.value = route.query.id
  if (docenteId.value) {
    await carregarDocente()
    await carregarUCs()
  } else {
    showError('ID do docente não fornecido.')
    router.push('/editando-docente')
  }
})

const carregarDocente = async () => {
  try {
    const docente = await withLoading(
      () => docentesAPI.obter(docenteId.value),
      'Carregando dados do docente...'
    )

    // Preencher o formulário com os dados do docente
    formData.value.nomeDocente = docente.nome
    formData.value.email = docente.email || ''
    formData.value.especialidade = docente.especialidade || ''
    
    // Resetar e preencher disponibilidade e horários
    const dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
    dias.forEach(dia => {
      formData.value.disponibilidade[dia] = docente.disponibilidade?.[dia] || false
      formData.value.horarios[dia] = docente.horarios?.[dia] || { inicio: '', fim: '' }
    })
    
    // Carregar UCs vinculadas do docente usando a API específica
    await carregarUCsDoDocente()

  } catch (error) {
    console.error('Erro ao carregar docente:', error)
    showError('Erro ao carregar os dados do docente. Tente novamente.')
    router.push('/editando-docente')
  }
}

const carregarUCs = async () => {
  loadingUCs.value = true
  try {
    ucsDisponiveis.value = await ucsAPI.listar()
  } catch (error) {
    console.error('Erro ao carregar UCs:', error)
    showError('Erro ao carregar a lista de UCs.')
  } finally {
    loadingUCs.value = false
  }
}

const carregarUCsDoDocente = async () => {
  try {
    const ucsDoDocente = await docentesAPI.listarUCs(docenteId.value)
    ucsVinculadas.value = ucsDoDocente || []
  } catch (error) {
    console.error('Erro ao carregar UCs do docente:', error)
    showError('Erro ao carregar as UCs do docente.')
  }
}

const diasSemana = [
  { value: 'segunda', label: 'Segunda-Feira' },
  { value: 'terca', label: 'Terça-Feira' },
  { value: 'quarta', label: 'Quarta-Feira' },
  { value: 'quinta', label: 'Quinta-Feira' },
  { value: 'sexta', label: 'Sexta-Feira' },
  { value: 'sabado', label: 'Sábado' }
]

const horariosOpcoes = ['10:00', '11:00', '12:00', '19:00', '20:00', '21:00', '22:00', '23:00']

// Função para obter horários baseado no dia da semana
const obterHorariosPorDia = (dia) => {
  if (dia === 'sabado') {
    return ['10:00', '11:00', '12:00']
  } else {
    return ['19:00', '20:00', '21:00', '22:00', '23:00']
  }
}

const voltar = () => {
  router.push('/editando-docente')
}

const salvar = async () => {
  if (!formData.value.nomeDocente) {
    showError('O nome do docente é obrigatório.')
    return
  }

  isSaving.value = true
  try {
    const dadosDocente = {
      nome: formData.value.nomeDocente,
      email: formData.value.email.trim() || null,
      especialidade: formData.value.especialidade.trim() || null,
      ucs_ids: ucsVinculadas.value.map(uc => uc.id),
      disponibilidade: formData.value.disponibilidade,
      horarios: formData.value.horarios
    }

    await docentesAPI.atualizar(docenteId.value, dadosDocente)
    showSuccess(`Docente "${formData.value.nomeDocente}" atualizado com sucesso!`)
    router.push('/editando-docente')

  } catch (error) {
    console.error('Erro ao salvar docente:', error)
    showError(error.message || 'Erro ao salvar as alterações.')
  } finally {
    isSaving.value = false
  }
}

const abrirDialogUCs = () => {
  const ucsNaoVinculadas = ucsDisponiveis.value.filter(
    uc => !ucsVinculadas.value.some(v => v.id === uc.id)
  )
  if (ucsNaoVinculadas.length === 0) {
    showError('Todas as UCs disponíveis já foram vinculadas.')
    return
  }
  showUCDialog.value = true
  ucSelecionada.value = null
}

const adicionarUC = () => {
  if (!ucSelecionada.value) return
  
  const jaVinculada = ucsVinculadas.value.some(uc => uc.id === ucSelecionada.value.id)
  if (!jaVinculada) {
    ucsVinculadas.value.push(ucSelecionada.value)
    showSuccess(`UC "${ucSelecionada.value.nome}" adicionada.`)
  }
  showUCDialog.value = false
  ucSelecionada.value = null
}

const removerUC = (ucId) => {
  const uc = ucsVinculadas.value.find(u => u.id === ucId)
  if (uc) {
    ucsVinculadas.value = ucsVinculadas.value.filter(u => u.id !== ucId)
    showSuccess(`UC "${uc.nome}" removida.`)
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
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  background-color: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.form-container {
  margin-bottom: 3rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  gap: 1rem;
}

/* Seção de Disciplinas/UCs */
.disciplinas-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-title-small {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.selected-ucs {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.info-text {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
  font-style: italic;
}

.disciplina-chip {
  display: flex;
  align-items: center;
  background-color: #3B82F6;
  color: white;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  gap: 0.5rem;
}

.disciplina-icon {
  background-color: rgba(255, 255, 255, 0.2);
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: bold;
}

.disciplina-text {
  font-size: 0.9rem;
}

.remove-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  margin-left: 0.5rem;
}

.add-disciplina-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #3B82F6;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.add-disciplina-btn:hover {
  background-color: #2563EB;
}

.add-disciplina-btn:disabled {
  background-color: #9CA3AF;
  cursor: not-allowed;
}

.plus-icon {
  font-size: 1.5rem;
  font-weight: bold;
}

/* Estilos do Dialog */
.empty-state {
  text-align: center;
  padding: 2rem;
}

.empty-state p {
  color: #666;
  margin-bottom: 1rem;
}

.uc-avatar {
  width: 40px;
  height: 40px;
  background-color: #F59E0B;
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: bold;
}

/* Seção Disponibilidade */
.disponibilidade-section {
  margin-top: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
}

.table-header {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 0.5rem 0;
  border-bottom: 2px solid #e5e7eb;
}

.table-header .time-column {
  font-weight: 600;
  color: #666;
  text-align: center;
}

.availability-row {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  gap: 1rem;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.day-checkbox {
  display: flex;
  align-items: center;
}

.time-input {
  display: flex;
  justify-content: center;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
}

/* Estilos para os campos Vuetify */
:deep(.v-text-field .v-field) {
  border-radius: 8px !important;
}

:deep(.v-text-field .v-field__input) {
  padding: 16px !important;
  font-size: 1.1rem !important;
  color: #000000 !important;
}

:deep(.v-text-field input) {
  color: #000000 !important;
}

:deep(.v-label) {
  color: #9CA3AF !important;
  font-size: 0.9rem !important;
  font-weight: 400 !important;
}

:deep(.v-checkbox .v-label) {
  color: #000000 !important;
  font-size: 1rem !important;
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

  .table-header,
  .availability-row {
    grid-template-columns: 160px 1fr 1fr;
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

  .table-header,
  .availability-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .table-header .time-column {
    display: none;
  }

  .time-input {
    justify-content: stretch;
  }
}
</style> 