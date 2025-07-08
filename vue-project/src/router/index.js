import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import NovoCadastro from '../components/NovoCadastro.vue'
import MeusCadastros from '../components/MeusCadastros.vue'
import EditandoCurso from '../components/EditandoCurso.vue'
import EditandoUC from '../components/EditandoUC.vue'
import EditandoDocente from '../components/EditandoDocente.vue'
import EditarCursoForm from '../components/EditarCursoForm.vue'
import EditarUCForm from '../components/EditarUCForm.vue'
import EditarDocenteForm from '../components/EditarDocenteForm.vue'
import CriarCursoForm from '../components/CriarCursoForm.vue'
import CriarUCForm from '../components/CriarUCForm.vue'
import CriarDocenteForm from '../components/CriarDocenteForm.vue'
import GerarCalendario from '../components/GerarCalendario.vue'
import Sobre from '../components/Sobre.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/novo-cadastro',
    name: 'novo-cadastro',
    component: NovoCadastro
  },
  {
    path: '/meus-cadastros',
    name: 'meus-cadastros',
    component: MeusCadastros
  },
  {
    path: '/editando-curso',
    name: 'editando-curso',
    component: EditandoCurso
  },
  {
    path: '/editando-uc',
    name: 'editando-uc',
    component: EditandoUC
  },
  {
    path: '/editando-docente',
    name: 'editando-docente',
    component: EditandoDocente
  },
  {
    path: '/editar-curso-form',
    name: 'editar-curso-form',
    component: EditarCursoForm
  },
  {
    path: '/editar-uc-form',  
    name: 'editar-uc-form',
    component: EditarUCForm
  },
  {
    path: '/editar-docente-form',
    name: 'editar-docente-form',
    component: EditarDocenteForm
  },
  {
    path: '/criar-curso-form',
    name: 'criar-curso-form',
    component: CriarCursoForm
  },
  {
    path: '/criar-uc-form',
    name: 'criar-uc-form',
    component: CriarUCForm
  },
  {
    path: '/criar-docente-form',
    name: 'criar-docente-form',
    component: CriarDocenteForm
  },
  {
    path: '/gerar-calendario',
    name: 'gerar-calendario',
    component: GerarCalendario
  },
  {
    path: '/sobre',
    name: 'sobre',
    component: Sobre
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 