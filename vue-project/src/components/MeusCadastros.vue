<template>
  <main class="main-content">
    <div class="container">
      <h1 class="page-title">Meus Cadastros</h1>
      
      <div v-if="isLoading" class="loading-container">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        <p>Carregando dados...</p>
      </div>
      
      <div v-else class="cards-grid">
        <div class="card" @click="openSection('curso')">
          <div class="card-icon">C</div>
          <div class="card-content">
            <div class="card-label">Cursos</div>
            <div class="card-count">{{ totalCursos }} cadastrados</div>
          </div>
        </div>
        
        <div class="card" @click="openSection('uc')">
          <div class="card-icon">U</div>
          <div class="card-content">
            <div class="card-label">UCs</div>
            <div class="card-count">{{ totalUCs }} cadastradas</div>
          </div>
        </div>
        
        <div class="card" @click="openSection('docentes')">
          <div class="card-icon">D</div>
          <div class="card-content">
            <div class="card-label">Docentes</div>
            <div class="card-count">{{ totalDocentes }} cadastrados</div>
          </div>
        </div>
        
        <div class="card" @click="openSection('calendario')">
          <div class="card-icon">📅</div>
          <div class="card-content">
            <div class="card-label">Calendários</div>
            <div class="card-count">{{ totalCalendarios }} gerados</div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { cursosAPI, docentesAPI, ucsAPI, calendarioAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const router = useRouter()
const { isLoading, withLoading } = useLoading()
const { showError } = useNotification()

// Contadores dos cadastros
const totalCursos = ref(0)
const totalDocentes = ref(0)
const totalUCs = ref(0)
const totalCalendarios = ref(0)

// Carregar totais ao montar o componente
onMounted(async () => {
  await carregarTotais()
})

const carregarTotais = async () => {
  try {
    await withLoading(async () => {
      // Carregar todos os dados em paralelo
      const [cursos, docentes, ucs, calendarios] = await Promise.all([
        cursosAPI.listar().catch(() => []),
        docentesAPI.listar().catch(() => []),
        ucsAPI.listar().catch(() => []),
        calendarioAPI.listar().catch(() => [])
      ])

      totalCursos.value = cursos.length
      totalDocentes.value = docentes.length
      totalUCs.value = ucs.length
      totalCalendarios.value = calendarios.length
    }, 'Carregando dados...')
  } catch (error) {
    console.error('Erro ao carregar totais:', error)
    showError('Erro ao carregar dados dos cadastros')
  }
}

// Function to handle card clicks
const openSection = (section) => {
  console.log(`Opening ${section} section`)
  
  if (section === 'curso') {
    router.push('/editando-curso')
  } else if (section === 'uc') {
    router.push('/editando-uc')
  } else if (section === 'docentes') {
    router.push('/editando-docente')
  } else if (section === 'calendario') {
    router.push('/gerar-calendario')
  } else {
    console.log(`${section} section not implemented yet`)
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
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  background-color: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 3.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 4rem;
  text-align: left;
}

.cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 2rem;
  max-width: 900px;
  width: 100%;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 2.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  min-height: 120px;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-count {
  font-size: 0.9rem;
  color: #666;
  font-weight: 400;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  gap: 1rem;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  border-color: #4F46E5;
}

.card-icon {
  width: 50px;
  height: 50px;
  background-color: #9CA3AF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  border-radius: 8px;
  flex-shrink: 0;
}

.card-label {
  font-size: 1.2rem;
  font-weight: 500;
  color: #333;
}

/* Responsive design - Tablet */
@media (max-width: 1024px) {
  .main-content {
    padding: 3rem 2rem;
  }
  
  .container {
    padding: 2rem;
  }
  
  .page-title {
    font-size: 3rem;
  }
  
  .cards-grid {
    max-width: 700px;
    gap: 1.5rem;
  }
  
  .card {
    padding: 2rem;
    min-height: 100px;
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

  .page-title {
    font-size: 2.5rem;
    margin-bottom: 3rem;
    text-align: center;
  }
  
  .cards-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    max-width: 100%;
  }
  
  .card {
    padding: 1.5rem;
    min-height: 80px;
  }
}

/* Small mobile */
@media (max-width: 480px) {
  .page-title {
    font-size: 2rem;
  }
  
  .card {
    padding: 1rem;
    gap: 1rem;
    min-height: 70px;
  }
  
  .card-icon {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }
  
  .card-label {
    font-size: 1rem;
  }
}
</style> 