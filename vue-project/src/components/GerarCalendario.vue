<template>
  <main class="main-content">
    <div class="container">
      <div class="stepper-header">
        <h2 class="page-title">{{ currentStep === 3 ? 'Visualização do calendário' : 'Gera calendário Escolar Curso' }}</h2>
        
        <!-- Botão para visualizar calendário direto -->
        <div class="header-actions" v-if="currentStep !== 3">
          <v-btn 
            @click="visualizarCalendarioDireto" 
            color="primary" 
            variant="outlined"
            prepend-icon="mdi-calendar-month"
            :loading="loadingCalendario"
          >
            <template v-if="!loadingCalendario">
              Visualizar Calendário
              <v-chip 
                v-if="totalEventos > 0" 
                class="ml-2" 
                size="small" 
                color="primary"
                variant="flat"
              >
                {{ totalEventos }}
              </v-chip>
            </template>
            <template v-else>
              Carregando...
            </template>
          </v-btn>
        </div>
      </div>
      
      <v-stepper 
        v-model="currentStep" 
        class="custom-stepper"
        :items="stepperItems"
        hide-actions
        non-linear
      >
        <!-- Step 1: Escolher Curso -->
        <template v-slot:item.1>
          <div class="step-content">
            <div class="step-circles">
              <div class="step-circle active">
                <span class="circle-icon">📚</span>
                <span class="circle-label">Curso</span>
              </div>
              <div class="step-circle">
                <span class="circle-icon">📅</span>
                <span class="circle-label">Fases</span>
              </div>
              <div class="step-circle">
                <span class="circle-icon">🗓️</span>
                <span class="circle-label">Calendário</span>
              </div>
            </div>
            
            <div v-if="loadingCourses" class="loading-container">
              <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
              <p>Carregando cursos...</p>
            </div>
            
            <div v-else class="courses-grid">
              <div 
                v-for="course in courses" 
                :key="course.id"
                class="course-card"
                :class="{ active: selectedCourse === course.id }"
                @click="selectCourse(course.id)"
              >
                <div class="course-icon" :class="course.iconClass">{{ course.icon }}</div>
                <span class="course-name">{{ course.name }}</span>
              </div>
            </div>
          </div>
        </template>

        <!-- Step 2: Escolher Fases -->
        <template v-slot:item.2>
          <div class="step-content">
            <div class="step-circles">
              <div class="step-circle">
                <span class="circle-icon">📚</span>
                <span class="circle-label">Curso</span>
              </div>
              <div class="step-circle active">
                <span class="circle-icon">📅</span>
                <span class="circle-label">Fases</span>
              </div>
              <div class="step-circle">
                <span class="circle-icon">🗓️</span>
                <span class="circle-label">Calendário</span>
              </div>
            </div>
            
            <div class="fases-content">
              <h3 class="section-title">Selecione as fases do curso</h3>
              <div class="fases-grid">
                <div 
                  v-for="fase in fases" 
                  :key="fase.id"
                  class="fase-card"
                  :class="{ active: selectedFases.includes(fase.id) }"
                  @click="toggleFase(fase.id)"
                >
                  <div class="fase-header">
                    <h4>{{ fase.nome }}</h4>
                    <v-checkbox 
                      :model-value="selectedFases.includes(fase.id)"
                      @click.stop
                      color="primary"
                      hide-details
                    ></v-checkbox>
                  </div>
                  <p class="fase-description">{{ fase.description }}</p>
                  <div class="fase-duration">{{ fase.duration }}</div>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- Step 3: Calendário -->
        <template v-slot:item.3>
          <div class="step-content">
            <div class="step-circles">
              <div class="step-circle">
                <span class="circle-icon">📚</span>
                <span class="circle-label">Curso</span>
              </div>
              <div class="step-circle">
                <span class="circle-icon">📅</span>
                <span class="circle-label">Fases</span>
              </div>
              <div class="step-circle active">
                <span class="circle-icon">🗓️</span>
                <span class="circle-label">Calendário</span>
              </div>
            </div>
            
            <div class="calendar-content">
              <div class="calendar-header">
                <div class="calendar-nav">
                  <!-- Removido navegação de mês -->
                  <h3 class="month-year">{{ monthNames[currentMonth] }} {{ currentYear }}</h3>
                </div>
                
                <div class="calendar-actions">
                  <v-chip 
                    v-if="totalEventos > 0" 
                    color="success" 
                    variant="outlined"
                    prepend-icon="mdi-calendar-check"
                    size="small"
                  >
                    {{ totalEventos }} evento{{ totalEventos > 1 ? 's' : '' }}
                  </v-chip>
                  
                  <v-chip 
                    v-else
                    color="info" 
                    variant="outlined"
                    prepend-icon="mdi-calendar-blank"
                    size="small"
                  >
                    Nenhum evento
                  </v-chip>
                  
                  <v-btn 
                    v-if="totalEventos > 0"
                    variant="outlined" 
                    color="error" 
                    size="small"
                    @click="limparTodosEventos"
                  >
                    <v-icon class="btn-icon">mdi-delete</v-icon>
                    <span class="btn-text">Limpar Todos</span>
                  </v-btn>
                  
                  <v-btn 
                    variant="outlined" 
                    color="success" 
                    size="small"
                    @click="gerarAlocacaoAutomatica"
                    :loading="gerandoAlocacao"
                  >
                    <v-icon class="btn-icon">mdi-auto-fix</v-icon>
                    <span class="btn-text">Alocar Mês Automaticamente</span>
                  </v-btn>
                  
                  <v-btn 
                    v-if="totalEventos > 0"
                    variant="outlined" 
                    color="info" 
                    size="small"
                    @click="mostrarResumoAlocacao"
                  >
                    <v-icon class="btn-icon">mdi-information</v-icon>
                    <span class="btn-text">Resumo Alocação</span>
                  </v-btn>
                  
                  <v-btn variant="outlined" color="primary" size="small" class="export-btn">
                    <span class="btn-text">Exportar Documento</span>
                    <v-icon class="btn-icon">mdi-file-export</v-icon>
                  </v-btn>
                </div>
              </div>
              
              <!-- Mensagem informativa quando não há eventos -->
              <v-alert 
                v-if="totalEventos === 0" 
                type="info" 
                variant="tonal"
                class="mb-4"
                icon="mdi-information"
              >
                <strong>Como usar o calendário:</strong><br>
                • Clique em qualquer dia para programar uma aula<br>
                • Clique nos eventos existentes para editá-los<br>
                • Use os ícones de navegação para mudar de mês
              </v-alert>
              
              <div class="calendar-table-container">
                <div class="calendar-table">
                  <div class="calendar-days-header">
                    <div v-for="day in dayNames" :key="day" class="day-header">{{ day }}</div>
                  </div>
                  <div class="calendar-grid">
                    <div 
                      v-for="day in calendarDays" 
                      :key="day.date" 
                      class="calendar-day"
                      :class="{ 
                        'other-month': !day.isCurrentMonth,
                        'selectable': day.isCurrentMonth,
                        'has-events': day.events.length > 0
                      }"
                      @click="day.isCurrentMonth ? selecionarDia(day) : null"
                    >
                      <div class="day-number">{{ day.day }}</div>
                      <div v-if="day.events.length > 0" class="day-events">
                        <div 
                          v-for="event in day.events" 
                          :key="event.id" 
                          class="event-card"
                          :class="[event.type, { 'evento-automatico': event.geradoAutomaticamente }]"
                          @click.stop="editarEvento(event)"
                        >
                          <div class="event-title">
                            {{ event.title }}
                            <v-icon v-if="event.geradoAutomaticamente" size="12" color="white">mdi-auto-fix</v-icon>
                          </div>
                          <div class="event-subtitle">{{ event.subtitle }}</div>
                          <div class="event-docente" v-if="event.docenteNome">
                            👨‍🏫 {{ event.docenteNome }}
                          </div>
                          <div class="event-time">
                            {{ event.horarioInicio }} - {{ event.horarioFim }}
                          </div>
                        </div>
                      </div>
                      
                      <!-- Indicador de dia clicável -->
                      <div v-if="day.isCurrentMonth && day.events.length === 0" class="add-event-hint">
                        <v-icon size="small" color="primary">mdi-plus-circle-outline</v-icon>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </v-stepper>

      <!-- Dialog para programar aula -->
      <v-dialog v-model="showAulaDialog" max-width="600">
        <v-card>
          <v-card-title>
            <span class="text-h5">
              {{ editandoEvento ? 'Editar Aula' : 'Programar Aula' }}
            </span>
            <v-spacer></v-spacer>
            <span class="text-subtitle-1 text-primary">
              {{ diaSelecionado ? formatarDataCompleta(diaSelecionado) : '' }}
            </span>
          </v-card-title>
          
          <v-card-text>
            <v-form ref="aulaForm">
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="novaAula.titulo"
                    label="Título da Aula *"
                    variant="outlined"
                    :rules="[v => !!v || 'Título é obrigatório']"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-textarea
                    v-model="novaAula.descricao"
                    label="Descrição"
                    variant="outlined"
                    rows="3"
                  ></v-textarea>
                </v-col>
                
                <v-col cols="6">
                  <v-text-field
                    v-model="novaAula.horarioInicio"
                    label="Horário de Início *"
                    type="time"
                    variant="outlined"
                    :rules="[v => !!v || 'Horário é obrigatório']"
                    @update:model-value="verificarDisponibilidadeDocente"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="6">
                  <v-text-field
                    v-model="novaAula.horarioFim"
                    label="Horário de Término *"
                    type="time"
                    variant="outlined"
                    :rules="[v => !!v || 'Horário é obrigatório']"
                    @update:model-value="verificarDisponibilidadeDocente"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-select
                    v-model="novaAula.tipo"
                    :items="tiposAula"
                    label="Tipo de Aula"
                    variant="outlined"
                  ></v-select>
                </v-col>
                
                <v-col cols="12">
                  <v-select
                    v-model="novaAula.ucId"
                    :items="ucsDisponiveis"
                    item-title="nome"
                    item-value="id"
                    label="UC (Opcional)"
                    variant="outlined"
                    clearable
                  ></v-select>
                </v-col>

                <v-col cols="12">
                  <v-select
                    v-model="novaAula.docenteId"
                    :items="docentesDisponiveis"
                    item-title="nome"
                    item-value="id"
                    label="Docente *"
                    variant="outlined"
                    :rules="[v => !!v || 'Docente é obrigatório']"
                    @update:model-value="verificarDisponibilidadeDocente"
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item v-bind="props">
                        <template v-slot:prepend>
                          <v-avatar size="32" color="primary">
                            {{ item.raw.nome.split(' ').map(word => word[0]).join('').substring(0, 2).toUpperCase() }}
                          </v-avatar>
                        </template>
                        <v-list-item-subtitle>
                          {{ item.raw.email || 'Sem email' }}
                          <span v-if="item.raw.especialidade"> • {{ item.raw.especialidade }}</span>
                        </v-list-item-subtitle>
                      </v-list-item>
                    </template>
                  </v-select>
                </v-col>

                <!-- Alerta de disponibilidade do docente -->
                <v-col cols="12" v-if="alertaDisponibilidade">
                  <v-alert
                    :type="alertaDisponibilidade.tipo"
                    :text="alertaDisponibilidade.mensagem"
                    variant="tonal"
                    closable
                    @click:close="alertaDisponibilidade = null"
                  ></v-alert>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn 
              v-if="editandoEvento"
              color="error" 
              text 
              @click="excluirEvento"
              :loading="salvandoAula"
            >
              Excluir
            </v-btn>
            <v-btn color="grey" text @click="fecharDialogAula">
              Cancelar
            </v-btn>
            <v-btn 
              color="primary" 
              text 
              @click="salvarAula"
              :loading="salvandoAula"
              :disabled="!novaAula.titulo || !novaAula.horarioInicio || !novaAula.horarioFim || !novaAula.docenteId || (alertaDisponibilidade && alertaDisponibilidade.tipo === 'error')"
            >
              {{ editandoEvento ? 'Atualizar' : 'Salvar' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      
      <!-- Dialog para resumo da alocação -->
      <v-dialog v-model="showResumoDialog" max-width="800">
        <v-card>
          <v-card-title class="text-h5">
            <v-icon left color="info">mdi-information</v-icon>
            Resumo da Alocação Automática
          </v-card-title>
          
          <v-card-text>
            <div v-if="resumoAlocacao">
              <v-row>
                <v-col cols="12" md="4">
                  <v-card variant="outlined" class="text-center pa-4">
                    <v-icon size="48" color="primary">mdi-calendar-check</v-icon>
                    <h3 class="mt-2">{{ resumoAlocacao.totalAulas }}</h3>
                    <p class="text-grey">Total de Aulas</p>
                  </v-card>
                </v-col>
                
                <v-col cols="12" md="4">
                  <v-card variant="outlined" class="text-center pa-4">
                    <v-icon size="48" color="success">mdi-account-group</v-icon>
                    <h3 class="mt-2">{{ resumoAlocacao.docentesUtilizados }}</h3>
                    <p class="text-grey">Docentes Utilizados</p>
                  </v-card>
                </v-col>
                
                <v-col cols="12" md="4">
                  <v-card variant="outlined" class="text-center pa-4">
                    <v-icon size="48" color="warning">mdi-clock-outline</v-icon>
                    <h3 class="mt-2">{{ resumoAlocacao.horasSemanais }}</h3>
                    <p class="text-grey">Horas por Semana</p>
                  </v-card>
                </v-col>
              </v-row>
              
              <v-divider class="my-4"></v-divider>
              
              <h4 class="mb-3">Distribuição por Docente:</h4>
              <v-list>
                <v-list-item 
                  v-for="docente in resumoAlocacao.distribuicaoDocentes" 
                  :key="docente.nome"
                  class="mb-2"
                >
                  <template v-slot:prepend>
                    <v-avatar color="primary">
                      {{ docente.nome.split(' ').map(word => word[0]).join('').substring(0, 2).toUpperCase() }}
                    </v-avatar>
                  </template>
                  
                  <v-list-item-title>{{ docente.nome }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ docente.totalAulas }} aulas • {{ docente.especialidade || 'Sem especialidade' }}
                  </v-list-item-subtitle>
                  
                  <template v-slot:append>
                    <v-chip size="small" color="primary">
                      {{ docente.diasSemana.join(', ') }}
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </div>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="showResumoDialog = false">
              Fechar
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      
      <div class="actions">
        <v-btn 
          variant="outlined" 
          size="large" 
          class="btn-voltar"
          @click="voltar"
        >
          <v-icon left>mdi-chevron-left</v-icon>
          {{ currentStep === 1 ? 'Voltar' : 'Anterior' }}
        </v-btn>
        
        <v-btn 
          v-if="currentStep < 3"
          variant="flat" 
          size="large" 
          color="primary"
          class="btn-continuar"
          :disabled="!canContinue || isLoading"
          :loading="isLoading"
          @click="continuar"
        >
          {{ isLoading ? 'Gerando...' : 'Continuar' }}
          <v-icon right>mdi-chevron-right</v-icon>
        </v-btn>
        
        <v-btn 
          v-else
          variant="flat" 
          size="large" 
          color="success"
          class="btn-finalizar"
          @click="finalizar"
        >
          Finalizar
          <v-icon right>mdi-check</v-icon>
        </v-btn>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { cursosAPI, calendarioAPI, ucsAPI, docentesAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const router = useRouter()
const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()

const currentStep = ref(1)
const selectedCourse = ref(null)
const selectedFases = ref([])
const currentMonth = ref(3) // Abril (0-based)
const currentYear = ref(2025)
const loadingCourses = ref(false)
const loadingCalendario = ref(false)
const gerandoAlocacao = ref(false)
const calendarioGerado = ref(null)

// Dialog de programação de aulas
const showAulaDialog = ref(false)
const showResumoDialog = ref(false)
const resumoAlocacao = ref(null)
const diaSelecionado = ref(null)
const editandoEvento = ref(false)
const salvandoAula = ref(false)
const novaAula = ref({
  titulo: '',
  descricao: '',
  horarioInicio: '',
  horarioFim: '',
  tipo: 'aula-teorica',
  ucId: null,
  docenteId: null
})

// Dados para o formulário
const ucsDisponiveis = ref([])
const docentesDisponiveis = ref([])
const alertaDisponibilidade = ref(null)
const tiposAula = [
  { title: 'Aula Teórica', value: 'aula-teorica' },
  { title: 'Aula Prática', value: 'aula-pratica' },
  { title: 'Laboratório', value: 'laboratorio' },
  { title: 'Projeto', value: 'projeto' },
  { title: 'Avaliação', value: 'avaliacao' },
  { title: 'Apresentação', value: 'apresentacao' }
]

const stepperItems = [
  { title: 'Escolher Curso', value: 1 },
  { title: 'Escolher Fases', value: 2 },
  { title: 'Visualizar Calendário', value: 3 }
]

const courses = ref([])

// Carregar cursos ao montar o componente
onMounted(async () => {
  await carregarCursos()
  await carregarUCs()
  await carregarDocentes()
  carregarEventosDoStorage()
})

const carregarCursos = async () => {
  loadingCourses.value = true
  try {
    const cursosData = await cursosAPI.listar()
    courses.value = cursosData.map(curso => ({
      id: curso.id,
      name: curso.nome,
      icon: curso.nome.split(' ').map(word => word[0]).join('').substring(0, 2).toUpperCase(),
      iconClass: 'curso-icon',
      carga_horaria: curso.carga_horaria,
      fases: curso.fases
    }))
  } catch (error) {
    console.error('Erro ao carregar cursos:', error)
    showError('Erro ao carregar lista de cursos')
  } finally {
    loadingCourses.value = false
  }
}

const carregarUCs = async () => {
  try {
    const ucsData = await ucsAPI.listar()
    ucsDisponiveis.value = ucsData
  } catch (error) {
    console.error('Erro ao carregar UCs:', error)
    // Se não conseguir carregar UCs, continua sem elas
    ucsDisponiveis.value = []
  }
}

const carregarDocentes = async () => {
  try {
    const docentesData = await docentesAPI.listar()
    docentesDisponiveis.value = docentesData
  } catch (error) {
    console.error('Erro ao carregar docentes:', error)
    showError('Erro ao carregar lista de docentes')
    docentesDisponiveis.value = []
  }
}

const verificarDisponibilidadeDocente = () => {
  if (!novaAula.value.docenteId || !diaSelecionado.value) {
    alertaDisponibilidade.value = null
    return
  }
  
  const docente = docentesDisponiveis.value.find(d => d.id === novaAula.value.docenteId)
  if (!docente) {
    alertaDisponibilidade.value = null
    return
  }
  
  // Mapear dias da semana (0=domingo, 1=segunda, ..., 6=sábado)
  const diasSemana = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
  const diaSemana = new Date(diaSelecionado.value).getDay()
  const nomeDia = diasSemana[diaSemana]
  
  // Verificar se o docente está disponível neste dia
  const disponivel = docente.disponibilidade?.[nomeDia] || false
  
  if (!disponivel) {
    alertaDisponibilidade.value = {
      tipo: 'error',
      mensagem: `O docente ${docente.nome} não está disponível para ${nomeDia.charAt(0).toUpperCase() + nomeDia.slice(1).replace('_', '-feira')}. Por favor, escolha outro dia ou outro docente.`
    }
    return
  }
  
  // Verificar se o horário está dentro da disponibilidade do docente
  const horariosDocente = docente.horarios?.[nomeDia]
  if (horariosDocente && novaAula.value.horarioInicio && novaAula.value.horarioFim) {
    const inicioDocente = horariosDocente.inicio
    const fimDocente = horariosDocente.fim
    
    if (inicioDocente && fimDocente) {
      const aulaInicio = novaAula.value.horarioInicio
      const aulaFim = novaAula.value.horarioFim
      
      // Verificar se o horário da aula está dentro do horário disponível do docente
      if (aulaInicio < inicioDocente || aulaFim > fimDocente) {
        // Mostrar horário específico baseado no dia da semana
        const horarioInfo = nomeDia === 'sabado' 
          ? 'das 10:00 às 12:00' 
          : 'das 19:00 às 23:00'
        
        alertaDisponibilidade.value = {
          tipo: 'warning',
          mensagem: `O docente ${docente.nome} está disponível ${nomeDia.charAt(0).toUpperCase() + nomeDia.slice(1).replace('_', '-feira')} ${horarioInfo}. Ajuste o horário da aula.`
        }
        return
      }
    }
  }
  
  // Se chegou até aqui, o docente está disponível
  alertaDisponibilidade.value = {
    tipo: 'success',
    mensagem: `Docente ${docente.nome} está disponível para esta data e horário! ✅`
  }
}

const fases = [
  { 
    id: 1, 
    nome: 'Fase 1 - Fundamentos', 
    description: 'Introdução aos conceitos básicos e fundamentos do curso',
    duration: '4 meses'
  },
  { 
    id: 2, 
    nome: 'Fase 2 - Desenvolvimento', 
    description: 'Desenvolvimento de projetos práticos e aplicações',
    duration: '6 meses'
  },
  { 
    id: 3, 
    nome: 'Fase 3 - Especialização', 
    description: 'Foco em áreas específicas e tecnologias avançadas',
    duration: '4 meses'
  },
  { 
    id: 4, 
    nome: 'Fase 4 - Projeto Final', 
    description: 'Desenvolvimento do projeto de conclusão do curso',
    duration: '2 meses'
  }
]

const monthNames = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

const dayNames = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab']

const canContinue = computed(() => {
  if (currentStep.value === 1) return selectedCourse.value !== null
  if (currentStep.value === 2) return selectedFases.value.length > 0
  return true
})

const totalEventos = computed(() => {
  return calendarioGerado.value?.eventos?.length || 0
})

const calendarDays = computed(() => {
  const days = []
  const firstDay = new Date(currentYear.value, currentMonth.value, 1)
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)
  const startDate = new Date(firstDay)
  startDate.setDate(startDate.getDate() - firstDay.getDay())
  
  // Gerar eventos baseados no calendário gerado pela API
  const events = []
  if (calendarioGerado.value && calendarioGerado.value.eventos) {
    // Converter eventos da API para o formato esperado pelo calendário
    calendarioGerado.value.eventos.forEach(evento => {
      const eventDate = new Date(evento.date)
      if (eventDate.getMonth() === currentMonth.value && eventDate.getFullYear() === currentYear.value) {
        events.push({
          id: evento.id,
          date: evento.date, // Manter a data completa para edição
          day: eventDate.getDate(), // Dia para exibição
          title: evento.title,
          subtitle: evento.subtitle,
          type: evento.type || 'course-event',
          horarioInicio: evento.horarioInicio,
          horarioFim: evento.horarioFim,
          ucId: evento.ucId,
          docenteId: evento.docenteId,
          docenteNome: evento.docenteNome,
          geradoAutomaticamente: evento.geradoAutomaticamente || false
        })
      }
    })
  }
  
  for (let i = 0; i < 42; i++) {
    const date = new Date(startDate)
    date.setDate(startDate.getDate() + i)
    
    const dayEvents = events.filter(e => e.day === date.getDate() && date.getMonth() === currentMonth.value)
    
    days.push({
      date: date.toISOString(),
      day: date.getDate(),
      isCurrentMonth: date.getMonth() === currentMonth.value,
      events: dayEvents
    })
  }
  
  return days
})

const selectCourse = (courseId) => {
  selectedCourse.value = courseId
}

const toggleFase = (faseId) => {
  const index = selectedFases.value.indexOf(faseId)
  if (index > -1) {
    selectedFases.value.splice(index, 1)
  } else {
    selectedFases.value.push(faseId)
  }
}

const previousMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}



const voltar = () => {
  if (currentStep.value === 1) {
    router.push('/')
  } else {
    currentStep.value--
  }
}

const continuar = async () => {
  if (currentStep.value < 3) {
    currentStep.value++
    
    // Se chegou na etapa 3 (visualizar calendário), gerar o calendário
    if (currentStep.value === 3) {
      await gerarCalendario()
    }
  }
}

const gerarCalendario = async () => {
  try {
    const dadosGeracao = {
      curso_id: selectedCourse.value,
      mes: currentMonth.value + 1, // API espera 1-12, não 0-11
      ano: currentYear.value,
      fases_selecionadas: selectedFases.value
    }

    calendarioGerado.value = await withLoading(
      () => calendarioAPI.gerar(dadosGeracao),
      'Gerando calendário...'
    )

    showSuccess('Calendário gerado com sucesso!')
  } catch (error) {
    console.error('Erro ao gerar calendário:', error)
    showError(error.message || 'Erro ao gerar calendário')
  }
}

const finalizar = () => {
  showSuccess('Calendário finalizado!')
  router.push('/')
}

// Função para visualizar calendário direto
const visualizarCalendarioDireto = async () => {
  loadingCalendario.value = true
  try {
    // Forçar recarregamento dos eventos do localStorage
    carregarEventosDoStorage()
    
    // Simular carregamento
    await new Promise(resolve => setTimeout(resolve, 500))
    
    currentStep.value = 3
    
    const totalEventosCarregados = calendarioGerado.value?.eventos?.length || 0
    if (totalEventosCarregados > 0) {
      showSuccess(`Calendário carregado com ${totalEventosCarregados} evento${totalEventosCarregados > 1 ? 's' : ''}!`)
    } else {
      showSuccess('Calendário carregado! Clique nos dias para programar aulas.')
    }
  } catch (error) {
    console.error('Erro ao carregar calendário:', error)
    showError('Erro ao carregar calendário')
  } finally {
    loadingCalendario.value = false
  }
}

// Funções de persistência
const salvarEventosNoStorage = () => {
  try {
    const eventos = calendarioGerado.value?.eventos || []
    localStorage.setItem('senai_calendario_eventos', JSON.stringify(eventos))
    console.log('Eventos salvos no storage:', eventos.length, eventos)
  } catch (error) {
    console.error('Erro ao salvar eventos:', error)
  }
}

const carregarEventosDoStorage = () => {
  try {
    const eventosString = localStorage.getItem('senai_calendario_eventos')
    if (eventosString) {
      const eventos = JSON.parse(eventosString)
      if (!calendarioGerado.value) {
        calendarioGerado.value = { eventos: [] }
      }
      calendarioGerado.value.eventos = eventos
      console.log('Eventos carregados do storage:', eventos.length)
    } else {
      // Inicializar com array vazio se não houver eventos salvos
      if (!calendarioGerado.value) {
        calendarioGerado.value = { eventos: [] }
      }
    }
  } catch (error) {
    console.error('Erro ao carregar eventos:', error)
    // Em caso de erro, inicializar com array vazio
    calendarioGerado.value = { eventos: [] }
  }
}

// Funções para programação de aulas
const selecionarDia = (day) => {
  diaSelecionado.value = new Date(day.date)
  editandoEvento.value = false
  
  // Obter horários padrão baseado no dia da semana
  const horariosPadrao = obterHorariosPadrao(day.date)
  
  novaAula.value = {
    titulo: '',
    descricao: '',
    horarioInicio: horariosPadrao.inicio,
    horarioFim: horariosPadrao.fim,
    tipo: 'aula-teorica',
    ucId: null
  }
  showAulaDialog.value = true
}

const editarEvento = (event) => {
  console.log('Editando evento:', event)
  editandoEvento.value = true
  
  // Encontrar a data correta baseada no evento
  const eventDate = new Date(event.date || new Date())
  diaSelecionado.value = eventDate
  
  novaAula.value = {
    id: event.id,
    titulo: event.title || '',
    descricao: event.subtitle || '',
    horarioInicio: event.horarioInicio || '19:00',
    horarioFim: event.horarioFim || '21:00',
    tipo: event.type || 'aula-teorica',
    ucId: event.ucId || null,
    docenteId: event.docenteId || null
  }
  
  showAulaDialog.value = true
  
  // Verificar disponibilidade do docente após carregar os dados
  setTimeout(() => {
    verificarDisponibilidadeDocente()
  }, 100)
}

const fecharDialogAula = () => {
  showAulaDialog.value = false
  diaSelecionado.value = null
  editandoEvento.value = false
  alertaDisponibilidade.value = null
  
  // Limpar formulário
  novaAula.value = {
    titulo: '',
    descricao: '',
    horarioInicio: '',
    horarioFim: '',
    tipo: 'aula-teorica',
    ucId: null,
    docenteId: null
  }
}

// Função para obter horários padrão baseado no dia da semana
const obterHorariosPadrao = (data) => {
  const diasSemana = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
  const diaSemana = new Date(data).getDay()
  const nomeDia = diasSemana[diaSemana]
  
  if (nomeDia === 'sabado') {
    return { inicio: '10:00', fim: '11:00' }
  } else {
    return { inicio: '19:00', fim: '21:00' }
  }
}

const salvarAula = async () => {
  // Verificar novamente a disponibilidade antes de salvar
  if (alertaDisponibilidade.value && alertaDisponibilidade.value.tipo === 'error') {
    showError('Não é possível salvar: docente não está disponível para esta data.')
    return
  }
  
  salvandoAula.value = true
  try {
    // Simular salvamento da aula
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const docente = docentesDisponiveis.value.find(d => d.id === novaAula.value.docenteId)
    
    const aulaData = {
      id: editandoEvento.value ? novaAula.value.id : Date.now(),
      title: novaAula.value.titulo,
      subtitle: novaAula.value.descricao,
      date: diaSelecionado.value.toISOString(),
      type: novaAula.value.tipo,
      horarioInicio: novaAula.value.horarioInicio,
      horarioFim: novaAula.value.horarioFim,
      ucId: novaAula.value.ucId,
      docenteId: novaAula.value.docenteId,
      docenteNome: docente ? docente.nome : 'Docente não encontrado'
    }

    // Adicionar ou atualizar evento no calendário
    if (!calendarioGerado.value) {
      calendarioGerado.value = { eventos: [] }
    }
    
    if (editandoEvento.value) {
      const index = calendarioGerado.value.eventos.findIndex(e => e.id === aulaData.id)
      if (index !== -1) {
        calendarioGerado.value.eventos[index] = aulaData
      }
      showSuccess('Aula atualizada com sucesso!')
    } else {
      calendarioGerado.value.eventos.push(aulaData)
      showSuccess('Aula programada com sucesso!')
    }
    
    // Salvar no localStorage
    salvarEventosNoStorage()
    
    fecharDialogAula()
  } catch (error) {
    console.error('Erro ao salvar aula:', error)
    showError('Erro ao salvar aula')
  } finally {
    salvandoAula.value = false
  }
}

const excluirEvento = async () => {
  salvandoAula.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    if (calendarioGerado.value && calendarioGerado.value.eventos) {
      calendarioGerado.value.eventos = calendarioGerado.value.eventos.filter(
        e => e.id !== novaAula.value.id
      )
    }
    
    // Salvar no localStorage
    salvarEventosNoStorage()
    
    showSuccess('Aula excluída com sucesso!')
    fecharDialogAula()
  } catch (error) {
    console.error('Erro ao excluir aula:', error)
    showError('Erro ao excluir aula')
  } finally {
    salvandoAula.value = false
  }
}

const formatarDataCompleta = (date) => {
  if (!date) return ''
  const options = { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  }
  return date.toLocaleDateString('pt-BR', options)
}

const limparTodosEventos = async () => {
  try {
    calendarioGerado.value = { eventos: [] }
    localStorage.removeItem('senai_calendario_eventos')
    showSuccess('Todos os eventos foram removidos!')
  } catch (error) {
    console.error('Erro ao limpar eventos:', error)
    showError('Erro ao limpar eventos')
  }
}

// Função para gerar alocação automática do mês atual
const gerarAlocacaoAutomatica = async () => {
  if (docentesDisponiveis.value.length === 0) {
    showError('Nenhum docente cadastrado! Cadastre docentes primeiro.')
    return
  }

  const confirmar = confirm(
    'Isso irá gerar automaticamente aulas para o mês atual baseado na disponibilidade dos docentes. Deseja continuar?'
  )
  
  if (!confirmar) return

  gerandoAlocacao.value = true
  try {
    const eventosGerados = []
    
    // Definir período do mês atual
    const inicioMes = new Date(currentYear.value, currentMonth.value, 1)
    const fimMes = new Date(currentYear.value, currentMonth.value + 1, 0)
    
    // Mapear dias da semana
    const diasSemana = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
    
    console.log('Analisando docentes disponíveis:', docentesDisponiveis.value)
    
    // Organizar docentes por dia da semana e horário
    const docentesPorDiaHorario = {}
    
    docentesDisponiveis.value.forEach(docente => {
      console.log(`Analisando docente: ${docente.nome}`)
      console.log('Disponibilidade:', docente.disponibilidade)
      console.log('Horários:', docente.horarios)
      
      // Verificar cada dia da semana
      diasSemana.forEach(dia => {
        // Verificar se o docente está disponível neste dia
        const disponivel = docente.disponibilidade?.[dia]
        console.log(`${docente.nome} - ${dia}: disponível = ${disponivel}`)
        
        if (disponivel && docente.horarios?.[dia]) {
          const horarios = docente.horarios[dia]
          console.log(`Horários do ${docente.nome} para ${dia}:`, horarios)
          
          if (horarios.inicio && horarios.fim && horarios.inicio !== '' && horarios.fim !== '') {
            // Gerar horários de aula baseado na disponibilidade
            const horariosAula = gerarHorariosAula(horarios.inicio, horarios.fim, dia)
            console.log(`Horários de aula gerados para ${docente.nome} em ${dia}:`, horariosAula)
            
            horariosAula.forEach(horario => {
              const chave = `${dia}-${horario.inicio}`
              if (!docentesPorDiaHorario[chave]) {
                docentesPorDiaHorario[chave] = []
              }
              docentesPorDiaHorario[chave].push({
                docente,
                horario,
                dia
              })
              console.log(`Adicionado à chave ${chave}:`, {docente: docente.nome, horario})
            })
          } else {
            console.log(`Horários inválidos para ${docente.nome} em ${dia}:`, horarios)
          }
        }
      })
    })
    
    console.log('Docentes organizados por dia/horário:', docentesPorDiaHorario)
    
    // Gerar eventos para cada dia do mês atual
    let dataAtual = new Date(inicioMes)
    let contadorSemanas = {}
    
    while (dataAtual <= fimMes) {
      const diaSemana = dataAtual.getDay()
      const nomeDia = diasSemana[diaSemana]
      
      // Pular domingos (geralmente não há aulas)
      if (diaSemana !== 0) {
        // Buscar docentes disponíveis para este dia
        Object.entries(docentesPorDiaHorario).forEach(([chave, docentes]) => {
          const [diaChave, horarioInicio] = chave.split('-')
          
          if (diaChave === nomeDia && docentes.length > 0) {
            // Calcular número da semana para alternância
            const numeroSemana = Math.floor((dataAtual.getTime() - inicioMes.getTime()) / (7 * 24 * 60 * 60 * 1000))
            
            // Inicializar contador para esta chave se não existir
            if (!contadorSemanas[chave]) {
              contadorSemanas[chave] = 0
            }
            
            // Selecionar docente baseado na alternância semanal
            const docenteIndex = contadorSemanas[chave] % docentes.length
            const docenteSelecionado = docentes[docenteIndex]
            
            // Incrementar contador apenas quando muda de semana
            if (numeroSemana > (contadorSemanas[chave + '_ultima_semana'] || -1)) {
              contadorSemanas[chave] = (contadorSemanas[chave] + 1) % docentes.length
              contadorSemanas[chave + '_ultima_semana'] = numeroSemana
            }
            
            // Gerar título da aula baseado na especialidade do docente
            const titulo = docenteSelecionado.docente.especialidade 
              ? `Aula de ${docenteSelecionado.docente.especialidade}`
              : 'Aula Programada'
            
            // Criar evento
            const evento = {
              id: `auto_${dataAtual.getTime()}_${horarioInicio}`,
              title: titulo,
              subtitle: `Aula automática - ${docenteSelecionado.docente.nome}`,
              date: dataAtual.toISOString(),
              type: 'aula-teorica',
              horarioInicio: docenteSelecionado.horario.inicio,
              horarioFim: docenteSelecionado.horario.fim,
              docenteId: docenteSelecionado.docente.id,
              docenteNome: docenteSelecionado.docente.nome,
              geradoAutomaticamente: true
            }
            
            eventosGerados.push(evento)
          }
        })
      }
      
      // Avançar para o próximo dia
      dataAtual.setDate(dataAtual.getDate() + 1)
    }
    
    console.log('Eventos gerados:', eventosGerados.length)
    
    // Adicionar eventos gerados ao calendário
    if (!calendarioGerado.value) {
      calendarioGerado.value = { eventos: [] }
    }
    
    // Remover eventos automáticos anteriores
    calendarioGerado.value.eventos = calendarioGerado.value.eventos.filter(
      evento => !evento.geradoAutomaticamente
    )
    
    // Adicionar novos eventos
    calendarioGerado.value.eventos.push(...eventosGerados)
    
    // Salvar no localStorage
    salvarEventosNoStorage()
    
    if (eventosGerados.length > 0) {
      showSuccess(`Alocação automática concluída! ${eventosGerados.length} aulas foram programadas para o mês.`)
    } else {
      showError('Nenhuma aula pôde ser gerada. Verifique se os docentes têm disponibilidade e horários configurados corretamente.')
    }
    
  } catch (error) {
    console.error('Erro ao gerar alocação automática:', error)
    showError('Erro ao gerar alocação automática')
  } finally {
    gerandoAlocacao.value = false
  }
}

// Função auxiliar para gerar horários de aula baseado na disponibilidade
const gerarHorariosAula = (inicio, fim, dia) => {
  const horarios = []
  
  console.log(`Gerando horários para ${dia}: ${inicio} - ${fim}`)
  
  // Converter horários para minutos para facilitar cálculos
  const inicioMinutos = parseInt(inicio.split(':')[0]) * 60 + parseInt(inicio.split(':')[1])
  const fimMinutos = parseInt(fim.split(':')[0]) * 60 + parseInt(fim.split(':')[1])
  
  if (dia === 'sabado') {
    // Sábado: aulas de 1 hora
    let horarioAtual = inicioMinutos
    
    while (horarioAtual + 60 <= fimMinutos) {
      const horaInicio = Math.floor(horarioAtual / 60).toString().padStart(2, '0') + ':' + 
                       (horarioAtual % 60).toString().padStart(2, '0')
      const horaFim = Math.floor((horarioAtual + 60) / 60).toString().padStart(2, '0') + ':' + 
                     ((horarioAtual + 60) % 60).toString().padStart(2, '0')
      
      horarios.push({
        inicio: horaInicio,
        fim: horaFim
      })
      
      horarioAtual += 60 // Próxima hora
    }
  } else {
    // Segunda a sexta: aulas de 2 horas
    let horarioAtual = inicioMinutos
    
    while (horarioAtual + 120 <= fimMinutos) {
      const horaInicio = Math.floor(horarioAtual / 60).toString().padStart(2, '0') + ':' + 
                       (horarioAtual % 60).toString().padStart(2, '0')
      const horaFim = Math.floor((horarioAtual + 120) / 60).toString().padStart(2, '0') + ':' + 
                     ((horarioAtual + 120) % 60).toString().padStart(2, '0')
      
      horarios.push({
        inicio: horaInicio,
        fim: horaFim
      })
      
      horarioAtual += 120 // Próximas 2 horas
    }
  }
  
  console.log(`Horários gerados:`, horarios)
  return horarios
}

// Função para mostrar resumo da alocação
const mostrarResumoAlocacao = () => {
  if (!calendarioGerado.value || !calendarioGerado.value.eventos.length) {
    showError('Nenhuma alocação encontrada!')
    return
  }
  
  const eventos = calendarioGerado.value.eventos
  const eventosAutomaticos = eventos.filter(e => e.geradoAutomaticamente)
  
  if (eventosAutomaticos.length === 0) {
    showError('Nenhuma alocação automática encontrada!')
    return
  }
  
  // Calcular estatísticas
  const docentesUnicosSet = new Set(eventosAutomaticos.map(e => e.docenteId))
  const distribuicaoDocentes = {}
  
  eventosAutomaticos.forEach(evento => {
    if (!distribuicaoDocentes[evento.docenteId]) {
      const docente = docentesDisponiveis.value.find(d => d.id === evento.docenteId)
      distribuicaoDocentes[evento.docenteId] = {
        nome: evento.docenteNome,
        especialidade: docente?.especialidade,
        totalAulas: 0,
        diasSemana: new Set()
      }
    }
    
    distribuicaoDocentes[evento.docenteId].totalAulas++
    
    // Adicionar dia da semana
    const diasSemana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab']
    const diaSemana = new Date(evento.date).getDay()
    distribuicaoDocentes[evento.docenteId].diasSemana.add(diasSemana[diaSemana])
  })
  
  // Converter Set para Array
  Object.values(distribuicaoDocentes).forEach(docente => {
    docente.diasSemana = Array.from(docente.diasSemana)
  })
  
  // Calcular horas mensais (estimativa)
  const horasMensais = eventosAutomaticos.length * 2 // 2h por aula
  
  resumoAlocacao.value = {
    totalAulas: eventosAutomaticos.length,
    docentesUtilizados: docentesUnicosSet.size,
    horasSemanais: Math.round(horasMensais / 4), // Dividir por 4 semanas para ter valor semanal
    distribuicaoDocentes: Object.values(distribuicaoDocentes)
  }
  
  showResumoDialog.value = true
}
</script>

<style scoped>
.main-content {
  padding: 1rem;
  min-height: calc(100vh - 140px);
  background-color: #E8E7E7;
  overflow-y: auto;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  background-color: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stepper-header {
  margin-bottom: 1.5rem;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
  font-weight: 400;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.custom-stepper {
  box-shadow: none !important;
  background: transparent !important;
}

.step-content {
  padding: 1rem 0;
}

.step-circles {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}

.step-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  opacity: 0.4;
  transition: opacity 0.3s ease;
}

.step-circle.active {
  opacity: 1;
}

.circle-icon {
  width: 60px;
  height: 60px;
  background-color: #4F46E5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.circle-label {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
}

/* Cursos */
.courses-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.course-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.course-card:hover {
  border-color: #4F46E5;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(79, 70, 229, 0.15);
}

.course-card.active {
  border-color: #4F46E5;
  background-color: rgba(79, 70, 229, 0.05);
}

.course-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1rem;
  color: white;
  flex-shrink: 0;
}

.ads-icon {
  background-color: #9CA3AF;
}

.cd-icon {
  background-color: #6B7280;
}

.course-name {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
}

/* Fases */
.fases-content {
  max-width: 800px;
  margin: 0 auto;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  text-align: center;
  margin-bottom: 2rem;
}

.fases-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.fase-card {
  padding: 1.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.fase-card:hover {
  border-color: #4F46E5;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(79, 70, 229, 0.15);
}

.fase-card.active {
  border-color: #4F46E5;
  background-color: rgba(79, 70, 229, 0.05);
}

.fase-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.fase-header h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.fase-description {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.fase-duration {
  color: #4F46E5;
  font-weight: 500;
  font-size: 0.9rem;
}

/* Calendário */
.calendar-content {
  max-width: 100%;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.calendar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.calendar-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.month-year {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  min-width: 200px;
  text-align: center;
}

.export-btn {
  background-color: #4F46E5 !important;
  color: white !important;
}

.calendar-table-container {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.calendar-table {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  min-width: 100%;
}

.calendar-days-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background-color: #4F46E5;
}

.day-header {
  padding: 0.75rem;
  text-align: center;
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}

.calendar-day {
  min-height: 80px;
  border: 1px solid #e5e7eb;
  padding: 0.4rem;
  position: relative;
  transition: all 0.2s ease;
}

.calendar-day.other-month {
  background-color: #f8fafc;
  opacity: 0.5;
}

.calendar-day.selectable {
  cursor: pointer;
}

.calendar-day.selectable:hover {
  background-color: #f0f9ff;
  border-color: #3b82f6;
}

.calendar-day.has-events {
  background-color: #fef3f2;
}

.calendar-day.has-events:hover {
  background-color: #fef2f2;
}

.day-number {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.day-events {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.event-card {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  line-height: 1.2;
}

.event-card.course-event {
  background-color: #4F46E5;
  color: white;
}

.event-card.course-event-2 {
  background-color: #06B6D4;
  color: white;
}

.event-card.aula-teorica {
  background-color: #3b82f6;
  color: white;
}

.event-card.aula-pratica {
  background-color: #10b981;
  color: white;
}

.event-card.laboratorio {
  background-color: #f59e0b;
  color: white;
}

.event-card.projeto {
  background-color: #8b5cf6;
  color: white;
}

.event-card.avaliacao {
  background-color: #ef4444;
  color: white;
}

.event-card.apresentacao {
  background-color: #ec4899;
  color: white;
}

.event-card.evento-automatico {
  border: 2px solid #10b981;
  position: relative;
}

.event-card.evento-automatico::before {
  content: '';
  position: absolute;
  top: -1px;
  right: -1px;
  width: 8px;
  height: 8px;
  background-color: #10b981;
  border-radius: 50%;
}

.event-card {
  cursor: pointer;
  transition: all 0.2s ease;
}

.event-card:hover {
  transform: scale(1.02);
  opacity: 0.9;
}

.event-title {
  font-weight: 600;
  margin-bottom: 0.1rem;
}

.event-subtitle {
  font-size: 0.7rem;
  opacity: 0.9;
  white-space: pre-line;
}

.event-docente {
  font-size: 0.65rem;
  opacity: 0.8;
  margin-top: 0.1rem;
  color: #34D399;
  font-weight: 500;
}

.event-time {
  font-size: 0.6rem;
  opacity: 0.7;
  margin-top: 0.1rem;
  font-weight: 500;
}

.add-event-hint {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  opacity: 0.5;
  transition: opacity 0.2s ease;
}

.calendar-day.selectable:hover .add-event-hint {
  opacity: 1;
}

.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn-voltar {
  border-color: #D1D5DB !important;
  color: #374151 !important;
  background-color: #F3F4F6 !important;
  padding: 0.75rem 2rem !important;
}

.btn-voltar:hover {
  background-color: #E5E7EB !important;
}

.btn-continuar {
  background-color: #6B7280 !important;
  color: white !important;
  padding: 0.75rem 2rem !important;
}

.btn-continuar:hover {
  background-color: #4B5563 !important;
}

.btn-continuar:disabled {
  background-color: #D1D5DB !important;
  color: #9CA3AF !important;
}

.btn-finalizar {
  background-color: #10B981 !important;
  color: white !important;
  padding: 0.75rem 2rem !important;
}

.btn-finalizar:hover {
  background-color: #059669 !important;
}

:deep(.v-btn) {
  text-transform: none !important;
  font-weight: 500 !important;
}

.calendar-actions .v-btn {
  white-space: nowrap;
}

.calendar-actions .v-btn .btn-text {
  margin-left: 0.5rem;
}

.calendar-actions .v-btn .btn-icon {
  margin-right: 0.5rem;
}

:deep(.v-stepper) {
  box-shadow: none !important;
}

:deep(.v-stepper-header) {
  display: none !important;
}

/* Responsive design */
@media (max-width: 1200px) {
  .container {
    max-width: 95%;
    margin: 0 auto;
  }
  
  .calendar-actions {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .calendar-actions .v-btn {
    font-size: 0.8rem;
  }
  
  .calendar-actions .v-chip {
    font-size: 0.75rem;
  }
}

@media (max-width: 1024px) {
  .stepper-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .step-circles {
    gap: 2rem;
  }
  
  .circle-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .courses-grid,
  .fases-grid {
    grid-template-columns: 1fr;
  }
  
  .calendar-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .calendar-actions {
    justify-content: center;
  }
  
  .calendar-day {
    min-height: 100px;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 0.5rem;
  }
  
  .container {
    padding: 1rem;
    border-radius: 8px;
  }
  
  .stepper-header {
    margin-bottom: 1rem;
  }
  
  .page-title {
    font-size: 1.1rem;
    text-align: center;
  }
  
  .step-circles {
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .circle-icon {
    width: 45px;
    height: 45px;
    font-size: 1rem;
  }
  
  .circle-label {
    font-size: 0.8rem;
  }
  
  .calendar-nav {
    justify-content: center;
  }
  
  .calendar-nav .v-btn {
    min-width: 40px;
  }
  
  .month-year {
    font-size: 1rem;
    min-width: 150px;
  }
  
  .calendar-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .calendar-actions .v-btn {
    font-size: 0.75rem;
    min-width: unset;
    padding: 0.25rem 0.5rem;
  }
  
  .calendar-actions .v-btn .btn-text {
    display: none;
  }
  
  .calendar-actions .v-btn .btn-icon {
    margin: 0;
  }
  
  .calendar-actions .v-chip {
    font-size: 0.7rem;
  }
  
  .calendar-day {
    min-height: 60px;
    padding: 0.25rem;
    font-size: 0.8rem;
  }
  
  .day-number {
    font-size: 0.8rem;
    margin-bottom: 0.25rem;
  }
  
  .event-card {
    font-size: 0.6rem;
    padding: 0.15rem 0.25rem;
    margin-bottom: 0.1rem;
  }
  
  .event-title {
    font-size: 0.6rem;
    margin-bottom: 0.05rem;
  }
  
  .event-subtitle {
    font-size: 0.55rem;
  }
  
  .event-docente {
    font-size: 0.5rem;
  }
  
  .event-time {
    font-size: 0.5rem;
  }
  
  .day-header {
    padding: 0.5rem;
    font-size: 0.8rem;
  }
  
  .actions {
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 1rem;
    padding-top: 1rem;
  }
  
  .btn-voltar,
  .btn-continuar,
  .btn-finalizar {
    width: 100% !important;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 0.25rem;
  }
  
  .container {
    padding: 0.5rem;
    border-radius: 4px;
  }
  
  .step-circles {
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  
  .circle-icon {
    width: 35px;
    height: 35px;
    font-size: 0.8rem;
  }
  
  .circle-label {
    font-size: 0.7rem;
  }
  
  .page-title {
    font-size: 1rem;
  }
  
  .calendar-nav {
    gap: 0.5rem;
  }
  
  .calendar-nav .v-btn {
    min-width: 35px;
    width: 35px;
    height: 35px;
  }
  
  .month-year {
    font-size: 0.9rem;
    min-width: 120px;
  }
  
  .calendar-actions {
    gap: 0.25rem;
  }
  
  .calendar-actions .v-btn {
    font-size: 0.7rem;
    padding: 0.2rem 0.4rem;
  }
  
  .calendar-actions .v-btn .btn-text {
    display: none;
  }
  
  .calendar-actions .v-btn .btn-icon {
    margin: 0;
    font-size: 1rem;
  }
  
  .calendar-actions .v-chip {
    font-size: 0.65rem;
  }
  
  .calendar-table {
    min-width: 450px;
  }
  
  .calendar-day {
    min-width: 60px;
  }
  
  .calendar-day {
    min-height: 45px;
    padding: 0.15rem;
  }
  
  .day-number {
    font-size: 0.7rem;
    margin-bottom: 0.15rem;
  }
  
  .event-card {
    font-size: 0.55rem;
    padding: 0.1rem 0.2rem;
    margin-bottom: 0.05rem;
  }
  
  .event-title {
    font-size: 0.55rem;
    margin-bottom: 0.02rem;
  }
  
  .event-subtitle {
    font-size: 0.5rem;
  }
  
  .event-docente {
    font-size: 0.45rem;
  }
  
  .event-time {
    font-size: 0.45rem;
  }
  
  .day-header {
    padding: 0.25rem;
    font-size: 0.7rem;
  }
  
  .add-event-hint {
    bottom: 0.25rem;
    right: 0.25rem;
  }
  
  .add-event-hint .v-icon {
    font-size: 0.8rem;
  }
  
  .course-card {
    padding: 1rem;
    gap: 0.75rem;
  }
  
  .course-icon {
    width: 40px;
    height: 40px;
    font-size: 0.9rem;
  }
  
  .course-name {
    font-size: 0.95rem;
  }
  
  .fase-card {
    padding: 1rem;
  }
  
  .fase-header h4 {
    font-size: 0.95rem;
  }
  
  .fase-description {
    font-size: 0.8rem;
  }
  
  .fase-duration {
    font-size: 0.8rem;
  }
}

/* Otimizações para calendário em dispositivos móveis */
@media (max-width: 768px) {
  .calendar-table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .calendar-table {
    min-width: 600px;
  }
  
  .calendar-grid {
    min-width: 100%;
  }
  
  .calendar-day {
    position: relative;
    overflow: hidden;
  }
  
  .day-events {
    max-height: calc(100% - 20px);
    overflow-y: auto;
  }
  
  .event-card {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .event-card:hover {
    white-space: normal;
    overflow: visible;
    z-index: 10;
    position: relative;
  }
}

@media (max-width: 480px) {
  .calendar-table {
    min-width: 500px;
  }
  
  .calendar-day {
    min-width: 70px;
  }
}

/* Melhorias para touch em dispositivos móveis */
@media (pointer: coarse) {
  .calendar-day.selectable {
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }
  
  .calendar-day.selectable:active {
    background-color: #e0f2fe;
  }
  
  .event-card {
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }
  
  .event-card:active {
    opacity: 0.8;
  }
  
  .v-btn {
    -webkit-tap-highlight-color: transparent;
  }
}
</style>