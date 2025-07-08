<template>
  <main class="main-content">
    <div class="container">
      <v-form @submit.prevent="salvar">
        <div class="form-container">
          <v-text-field
            v-model="formData.nomeUC"
            label="Nome UC"
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

          <div class="vincular-docente-field mb-6">
            <v-select
              v-model="formData.vinculoDocente"
              label="Vincular Docente"
              :items="professoresOptions"
              variant="outlined"
              color="indigo"
              hide-details
              placeholder="Selecione um docente"
            >
              <template v-slot:prepend-inner>
                <div class="docente-icon">VD</div>
              </template>
            </v-select>
          </div>
        </div>

        <div class="action-buttons">
          <v-btn
            @click="sair"
            variant="outlined"
            size="large"
            class="btn-sair"
          >
            Sair
          </v-btn>
          <v-btn
            @click="salvar"
            variant="flat"
            size="large"
            class="btn-salvar"
          >
            Salvar
          </v-btn>
        </div>
      </v-form>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Form data
const formData = ref({
  nomeUC: 'Lógica de Programação',
  cargaHoraria: '180',
  vinculoDocente: ''
})

// Opções de professores (vazio por enquanto como solicitado)
const professoresOptions = [
  // { title: 'Prof. João Silva', value: 'joao' },
  // { title: 'Prof. Maria Santos', value: 'maria' },
  // Vazio pois não tem nenhum professor ainda
]

const sair = () => {
  router.push('/editando-uc')
}

const salvar = () => {
  console.log('Salvando UC:', formData.value)
  // Após salvar, redireciona para editando uc
  router.push('/editando-uc')
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

.vincular-docente-field {
  position: relative;
}

.docente-icon {
  width: 40px;
  height: 40px;
  background-color: #6B7280;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: bold;
  border-radius: 6px;
  margin-right: 0.5rem;
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

:deep(.v-select .v-field) {
  border-radius: 8px !important;
}

:deep(.v-text-field .v-field__input) {
  padding: 16px !important;
  font-size: 1.1rem !important;
  color: #000000 !important;
}

:deep(.v-select .v-field__input) {
  padding: 16px !important;
  font-size: 1.1rem !important;
  color: #000000 !important;
}

:deep(.v-label) {
  color: #9CA3AF !important;
  font-size: 0.9rem !important;
  font-weight: 400 !important;
}

/* Placeholder styles - Mais específicos para sobrescrever Vuetify */
:deep(.v-select .v-field__input input::placeholder),
:deep(.v-select .v-field__input input::-webkit-input-placeholder),
:deep(.v-select .v-field__input input::-moz-placeholder),
:deep(.v-select .v-field__input input:-ms-input-placeholder) {
  color: #1f2937 !important;
  opacity: 1 !important;
  font-weight: 500 !important;
}

:deep(.v-select .v-field__placeholder),
:deep(.v-select .v-field__overlay),
:deep(.v-select .v-field__input .v-field__placeholder) {
  color: #1f2937 !important;
  opacity: 1 !important;
  font-weight: 500 !important;
}

:deep(.v-text-field .v-field__input input::placeholder),
:deep(.v-text-field .v-field__input input::-webkit-input-placeholder),
:deep(.v-text-field .v-field__input input::-moz-placeholder),
:deep(.v-text-field .v-field__input input:-ms-input-placeholder) {
  color: #1f2937 !important;
  opacity: 1 !important;
  font-weight: 500 !important;
}

/* Estilo específico para o select quando não há valor selecionado */
:deep(.v-select .v-field__input),
:deep(.v-select .v-field__input .v-field__input),
:deep(.v-select:not(.v-select--selected) .v-field__input) {
  color: #1f2937 !important;
}

:deep(.v-select .v-select__selection-text),
:deep(.v-select .v-select__selection),
:deep(.v-select .v-field__field .v-field__input) {
  color: #1f2937 !important;
}

/* Força o placeholder a sempre ser visível */
:deep(.v-select:not(.v-select--active) .v-field__input),
:deep(.v-select .v-field__input[placeholder]) {
  color: #1f2937 !important;
  opacity: 1 !important;
}

/* Sobrescreve qualquer estilo do Vuetify */
:deep(.v-field__input input) {
  color: #000000 !important;
}

:deep(.v-field__input input:placeholder-shown) {
  color: #1f2937 !important;
}

/* Estilos para os botões */
.btn-sair {
  border-color: #D1D5DB !important;
  color: #374151 !important;
  background-color: #D1D5DB !important;
  padding: 1rem 3rem !important;
  min-width: 150px !important;
}

.btn-sair:hover {
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
  
  .btn-sair,
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
  
  .docente-icon {
    width: 35px;
    height: 35px;
    font-size: 0.8rem;
  }
}

/* Texto dos inputs sempre preto */
:deep(.v-text-field input) {
  color: #000000 !important;
}

:deep(.v-select input) {
  color: #000000 !important;
}

/* Texto selecionado no select */
:deep(.v-select .v-select__selection-text) {
  color: #000000 !important;
}

:deep(.v-select .v-select__selection) {
  color: #000000 !important;
}
</style> 