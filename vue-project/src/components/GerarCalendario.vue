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
                  <v-btn icon @click="previousMonth">
                    <v-icon>mdi-chevron-left</v-icon>
                  </v-btn>
                  <h3 class="month-year">{{ monthNames[currentMonth] }} {{ currentYear }}</h3>
                  <v-btn icon @click="nextMonth">
                    <v-icon>mdi-chevron-right</v-icon>
                  </v-btn>
                </div>
                
                <div class="calendar-actions">
                  <v-chip 
                    v-if="totalEventos > 0" 
                    color="success" 
                    variant="outlined"
                    prepend-icon="mdi-calendar-check"
                  >
                    {{ totalEventos }} evento{{ totalEventos > 1 ? 's' : '' }}
                  </v-chip>
                  
                  <v-chip 
                    v-else
                    color="info" 
                    variant="outlined"
                    prepend-icon="mdi-calendar-blank"
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
                    Limpar Todos
                  </v-btn>
                  
                  <v-btn variant="outlined" color="primary" class="export-btn">
                    Exportar Documento
                    <v-icon right>mdi-file-export</v-icon>
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
                        :class="event.type"
                        @click.stop="editarEvento(event)"
                      >
                        <div class="event-title">{{ event.title }}</div>
                        <div class="event-subtitle">{{ event.subtitle }}</div>
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
                  ></v-text-field>
                </v-col>
                
                <v-col cols="6">
                  <v-text-field
                    v-model="novaAula.horarioFim"
                    label="Horário de Término *"
                    type="time"
                    variant="outlined"
                    :rules="[v => !!v || 'Horário é obrigatório']"
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
              :disabled="!novaAula.titulo || !novaAula.horarioInicio || !novaAula.horarioFim"
            >
              {{ editandoEvento ? 'Atualizar' : 'Salvar' }}
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
import { cursosAPI, calendarioAPI, ucsAPI } from '@/services/api'
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
const calendarioGerado = ref(null)

// Dialog de programação de aulas
const showAulaDialog = ref(false)
const diaSelecionado = ref(null)
const editandoEvento = ref(false)
const salvandoAula = ref(false)
const novaAula = ref({
  titulo: '',
  descricao: '',
  horarioInicio: '',
  horarioFim: '',
  tipo: 'aula-teorica',
  ucId: null
})

// Dados para o formulário
const ucsDisponiveis = ref([])
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
          ucId: evento.ucId
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
  novaAula.value = {
    titulo: '',
    descricao: '',
    horarioInicio: '08:00',
    horarioFim: '10:00',
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
    horarioInicio: event.horarioInicio || '08:00',
    horarioFim: event.horarioFim || '10:00',
    tipo: event.type || 'aula-teorica',
    ucId: event.ucId || null
  }
  showAulaDialog.value = true
}

const fecharDialogAula = () => {
  showAulaDialog.value = false
  diaSelecionado.value = null
  editandoEvento.value = false
}

const salvarAula = async () => {
  salvandoAula.value = true
  try {
    // Simular salvamento da aula
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const aulaData = {
      id: editandoEvento.value ? novaAula.value.id : Date.now(),
      title: novaAula.value.titulo,
      subtitle: novaAula.value.descricao,
      date: diaSelecionado.value.toISOString(),
      type: novaAula.value.tipo,
      horarioInicio: novaAula.value.horarioInicio,
      horarioFim: novaAula.value.horarioFim,
      ucId: novaAula.value.ucId
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
</script>

<style scoped>
.main-content {
  padding: 2rem;
  min-height: calc(100vh - 120px);
  background-color: #E8E7E7;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  background-color: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stepper-header {
  margin-bottom: 2rem;
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
  padding: 2rem 0;
}

.step-circles {
  display: flex;
  justify-content: center;
  gap: 4rem;
  margin-bottom: 4rem;
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
  width: 80px;
  height: 80px;
  background-color: #4F46E5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
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
  margin-bottom: 2rem;
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

.calendar-table {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.calendar-days-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background-color: #4F46E5;
}

.day-header {
  padding: 1rem;
  text-align: center;
  font-weight: 600;
  color: white;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}

.calendar-day {
  min-height: 120px;
  border: 1px solid #e5e7eb;
  padding: 0.5rem;
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
  margin-top: 3rem;
  padding-top: 2rem;
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

:deep(.v-stepper) {
  box-shadow: none !important;
}

:deep(.v-stepper-header) {
  display: none !important;
}

/* Responsive design */
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
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .container {
    padding: 1.5rem;
  }
  
  .step-circles {
    gap: 1.5rem;
    margin-bottom: 3rem;
  }
  
  .circle-icon {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }
  
  .circle-label {
    font-size: 0.9rem;
  }
  
  .calendar-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .calendar-actions {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .month-year {
    font-size: 1.2rem;
  }
  
  .calendar-day {
    min-height: 80px;
  }
  
  .event-card {
    font-size: 0.7rem;
  }
  
  .actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .btn-voltar,
  .btn-continuar,
  .btn-finalizar {
    width: 100% !important;
  }
}
</style> 