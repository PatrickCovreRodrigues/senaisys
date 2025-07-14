import axios from 'axios'

// Configuração base da API
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Erro na API:', error)
    
    // Tratamento de erros específicos
    if (error.response) {
      // Erro do servidor
      const message = error.response.data?.detail || 'Erro no servidor'
      throw new Error(message)
    } else if (error.request) {
      // Erro de rede
      throw new Error('Erro de conexão. Verifique se o backend está rodando.')
    } else {
      // Outro tipo de erro
      throw new Error('Erro inesperado')
    }
  }
)

// ========== CURSOS API ==========
export const cursosAPI = {
  // Listar todos os cursos
  listar: async (skip = 0, limit = 100) => {
    const response = await api.get(`/cursos/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  // Criar novo curso
  criar: async (dadosCurso) => {
    const response = await api.post('/cursos/', dadosCurso)
    return response.data
  },

  // Obter curso por ID
  obter: async (id) => {
    const response = await api.get(`/cursos/${id}`)
    return response.data
  },

  // Atualizar curso
  atualizar: async (id, dadosCurso) => {
    const response = await api.put(`/cursos/${id}`, dadosCurso)
    return response.data
  },

  // Deletar curso
  deletar: async (id) => {
    const response = await api.delete(`/cursos/${id}`)
    return response.data
  },

  // Listar UCs do curso
  listarUCs: async (id) => {
    const response = await api.get(`/cursos/${id}/ucs`)
    return response.data
  }
}

// ========== DOCENTES API ==========
export const docentesAPI = {
  // Listar todos os docentes
  listar: async (skip = 0, limit = 100) => {
    const response = await api.get(`/docentes/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  // Criar novo docente
  criar: async (dadosDocente) => {
    const response = await api.post('/docentes/', dadosDocente)
    return response.data
  },

  // Obter docente por ID
  obter: async (id) => {
    const response = await api.get(`/docentes/${id}`)
    return response.data
  },

  // Atualizar docente
  atualizar: async (id, dadosDocente) => {
    const response = await api.put(`/docentes/${id}`, dadosDocente)
    return response.data
  },

  // Deletar docente
  deletar: async (id) => {
    const response = await api.delete(`/docentes/${id}`)
    return response.data
  },

  // Obter disponibilidade do docente
  disponibilidade: async (id) => {
    const response = await api.get(`/docentes/${id}/disponibilidade`)
    return response.data
  },

  // Listar UCs do docente
  listarUCs: async (id) => {
    const response = await api.get(`/docentes/${id}/ucs`)
    return response.data
  }
}

// ========== UCS API ==========
export const ucsAPI = {
  // Listar todas as UCs
  listar: async (skip = 0, limit = 100) => {
    const response = await api.get(`/ucs/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  // Criar nova UC
  criar: async (dadosUC) => {
    const response = await api.post('/ucs/', dadosUC)
    return response.data
  },

  // Obter UC por ID
  obter: async (id) => {
    const response = await api.get(`/ucs/${id}`)
    return response.data
  },

  // Atualizar UC
  atualizar: async (id, dadosUC) => {
    const response = await api.put(`/ucs/${id}`, dadosUC)
    return response.data
  },

  // Deletar UC
  deletar: async (id) => {
    const response = await api.delete(`/ucs/${id}`)
    return response.data
  },

  // Listar UCs por curso
  porCurso: async (cursoId) => {
    const response = await api.get(`/ucs/por-curso/${cursoId}`)
    return response.data
  },

  // Listar UCs por docente
  porDocente: async (docenteId) => {
    const response = await api.get(`/ucs/por-docente/${docenteId}`)
    return response.data
  },

  // Vincular docente à UC
  vincularDocente: async (ucId, docenteId) => {
    const response = await api.put(`/ucs/${ucId}/vincular-docente/${docenteId}`)
    return response.data
  },

  // Desvincular docente da UC
  desvincularDocente: async (ucId) => {
    const response = await api.put(`/ucs/${ucId}/desvincular-docente`)
    return response.data
  }
}

// ========== CALENDÁRIO API ==========
export const calendarioAPI = {
  // Listar todos os calendários
  listar: async (skip = 0, limit = 100) => {
    const response = await api.get(`/calendario/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  // Criar novo calendário
  criar: async (dadosCalendario) => {
    const response = await api.post('/calendario/', dadosCalendario)
    return response.data
  },

  // Obter calendário por ID
  obter: async (id) => {
    const response = await api.get(`/calendario/${id}`)
    return response.data
  },

  // Atualizar calendário
  atualizar: async (id, dadosCalendario) => {
    const response = await api.put(`/calendario/${id}`, dadosCalendario)
    return response.data
  },

  // Deletar calendário
  deletar: async (id) => {
    const response = await api.delete(`/calendario/${id}`)
    return response.data
  },

  // Gerar calendário automático
  gerar: async (dadosGeracao) => {
    const response = await api.post('/calendario/gerar', null, {
      params: dadosGeracao
    })
    return response.data
  },

  // Obter calendário por curso
  porCurso: async (cursoId) => {
    const response = await api.get(`/calendario/por-curso/${cursoId}`)
    return response.data
  },

  // Obter calendário específico de um mês
  obterMes: async (cursoId, ano, mes) => {
    const response = await api.get(`/calendario/calendario-mes/${cursoId}/${ano}/${mes}`)
    return response.data
  },

  // Listar eventos do curso
  eventos: async (cursoId) => {
    const response = await api.get(`/calendario/eventos/${cursoId}`)
    return response.data
  },

  // Gerar alocação automática de professores
  gerarAlocacaoAutomatica: async (dadosAlocacao) => {
    const response = await api.post('/calendario/gerar-alocacao-automatica', dadosAlocacao)
    return response.data
  }
}

// ========== ALOCAÇÃO API ==========
export const alocacaoAPI = {
  // Processar alocação automática de docentes
  processar: async (docentesInput, ano = null, mes = null) => {
    const response = await api.post('/alocacao/processar', docentesInput, {
      params: { ano, mes }
    })
    return response.data
  },

  // Obter matriz de horários
  obterMatrizHorarios: async (ano = null, mes = null) => {
    const response = await api.get('/alocacao/matriz-horarios', {
      params: { ano, mes }
    })
    return response.data
  },

  // Verificar disponibilidade de docente
  verificarDisponibilidade: async (docenteId, dia, horario, ano = null, mes = null) => {
    const response = await api.get(`/alocacao/disponibilidade/${docenteId}`, {
      params: { dia, horario, ano, mes }
    })
    return response.data
  },

  // Obter alocações existentes
  obterAlocacoesExistentes: async (dia, horario, ano = null, mes = null) => {
    const response = await api.get('/alocacao/alocacoes-existentes', {
      params: { dia, horario, ano, mes }
    })
    return response.data
  },

  // Criar alocação manual
  criarAlocacaoManual: async (dadosAlocacao) => {
    const response = await api.post('/alocacao/alocacao-manual', dadosAlocacao)
    return response.data
  },

  // Atualizar alocação
  atualizarAlocacao: async (alocacaoId, dadosAtualizacao) => {
    const response = await api.put(`/alocacao/alocacao/${alocacaoId}`, dadosAtualizacao)
    return response.data
  },

  // Deletar alocação
  deletarAlocacao: async (alocacaoId) => {
    const response = await api.delete(`/alocacao/alocacao/${alocacaoId}`)
    return response.data
  },

  // Obter relatório de docente
  obterRelatorioDocente: async (docenteId, ano = null, mes = null) => {
    const response = await api.get(`/alocacao/relatorio-docente/${docenteId}`, {
      params: { ano, mes }
    })
    return response.data
  },

  // Obter estatísticas de alocação
  obterEstatisticas: async (ano = null, mes = null) => {
    const response = await api.get('/alocacao/estatisticas', {
      params: { ano, mes }
    })
    return response.data
  }
}

// ========== HEALTH CHECK ==========
export const healthAPI = {
  check: async () => {
    const response = await api.get('/health', { baseURL: 'http://127.0.0.1:8000' })
    return response.data
  }
}

// Export da instância axios configurada para uso direto se necessário
export default api