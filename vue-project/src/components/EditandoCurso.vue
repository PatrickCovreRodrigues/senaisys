<template>
  <main class="main-content">
    <div class="container">
      <h1 class="page-title">Editando Curso</h1>
      
      <div v-if="isLoading" class="loading-container">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        <p>Carregando cursos...</p>
      </div>

      <div v-else-if="cursos.length === 0" class="empty-state">
        <div class="empty-icon">📚</div>
        <h3>Nenhum curso cadastrado</h3>
        <p>Cadastre seu primeiro curso para começar!</p>
        <v-btn @click="criarNovoCurso" color="primary" variant="flat">
          Criar Primeiro Curso
        </v-btn>
      </div>

      <div v-else class="cards-grid">
        <div class="card" v-for="curso in cursos" :key="curso.id" @click="editarCurso(curso)">
          <div class="card-icon">{{ curso.nome.split(' ').map(word => word[0]).join('').substring(0, 2).toUpperCase() }}</div>
          <div class="card-content">
            <div class="card-label">{{ curso.nome }}</div>
            <div class="card-subtitle">{{ curso.carga_horaria }}h • {{ curso.fases || 'Sem fases' }}</div>
          </div>
          <div class="card-actions">
            <button class="delete-btn" @click.stop="confirmarDelete(curso)" :title="`Deletar ${curso.nome}`">
              🗑️
            </button>
          </div>
        </div>
      </div>

      <!-- Dialog de confirmação de delete -->
      <v-dialog v-model="showDeleteDialog" max-width="400">
        <v-card>
          <v-card-title class="text-h5">Confirmar Exclusão</v-card-title>
          <v-card-text>
            Tem certeza que deseja deletar o curso "{{ cursoParaDelete?.nome }}"?
            Esta ação não pode ser desfeita.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="grey" text @click="showDeleteDialog = false">Cancelar</v-btn>
            <v-btn color="red" text @click="deletarCurso" :loading="deletingCurso">Deletar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      
      <div class="action-buttons">
        <button class="btn-voltar" @click="goBack">Voltar</button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { cursosAPI } from '@/services/api'
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'

const router = useRouter()
const { isLoading, withLoading } = useLoading()
const { showSuccess, showError } = useNotification()

// Dados dos cursos
const cursos = ref([])
const showDeleteDialog = ref(false)
const cursoParaDelete = ref(null)
const deletingCurso = ref(false)

// Carregar cursos ao montar o componente
onMounted(async () => {
  await carregarCursos()
})

const carregarCursos = async () => {
  try {
    cursos.value = await withLoading(
      () => cursosAPI.listar(),
      'Carregando cursos...'
    )
  } catch (error) {
    console.error('Erro ao carregar cursos:', error)
    showError('Erro ao carregar cursos')
  }
}

const goBack = () => {
  router.push('/meus-cadastros')
}

const editarCurso = (curso) => {
  console.log('Editando curso:', curso)
  // Navegar para formulário de edição passando os dados do curso
  router.push({
    path: '/editar-curso-form',
    query: { id: curso.id }
  })
}

const criarNovoCurso = () => {
  router.push('/criar-curso')
}

const confirmarDelete = (curso) => {
  cursoParaDelete.value = curso
  showDeleteDialog.value = true
}

const deletarCurso = async () => {
  if (!cursoParaDelete.value) return

  deletingCurso.value = true
  try {
    await cursosAPI.deletar(cursoParaDelete.value.id)
    showSuccess(`Curso "${cursoParaDelete.value.nome}" deletado com sucesso!`)
    
    // Remover da lista local
    cursos.value = cursos.value.filter(c => c.id !== cursoParaDelete.value.id)
    
    // Fechar dialog
    showDeleteDialog.value = false
    cursoParaDelete.value = null
  } catch (error) {
    console.error('Erro ao deletar curso:', error)
    showError(error.message || 'Erro ao deletar curso')
  } finally {
    deletingCurso.value = false
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
  gap: 2rem;
  max-width: 900px;
  width: 100%;
  margin-bottom: 4rem;
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
  border: 2px solid #e5e7eb;
  min-height: 120px;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  border-color: #4F46E5;
}

.card-icon {
  width: 60px;
  height: 60px;
  background-color: #6B7280;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  border-radius: 8px;
  flex-shrink: 0;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-label {
  font-size: 1.3rem;
  font-weight: 500;
  color: #333;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #666;
  font-weight: 400;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.delete-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  opacity: 0.7;
}

.delete-btn:hover {
  background-color: #fee2e2;
  opacity: 1;
  transform: scale(1.1);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  gap: 1rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  gap: 1rem;
  text-align: center;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.empty-state p {
  font-size: 1rem;
  color: #666;
  margin: 0;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
  max-width: 900px;
  width: 100%;
}

.btn-voltar,
.btn-continuar {
  padding: 1rem 3rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 150px;
}

.btn-voltar {
  background-color: #E5E7EB;
  color: #374151;
}

.btn-voltar:hover {
  background-color: #D1D5DB;
  transform: translateY(-1px);
}

.btn-continuar {
  background-color: #4F46E5;
  color: white;
}

.btn-continuar:hover {
  background-color: #3730A3;
  transform: translateY(-1px);
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
    margin-bottom: 3rem;
  }
  
  .card {
    padding: 1.5rem;
    min-height: 80px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 1rem;
  }
  
  .btn-voltar,
  .btn-continuar {
    width: 100%;
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
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }
  
  .card-label {
    font-size: 1rem;
  }
}
</style> 