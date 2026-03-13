import axios from 'axios'
import type { Paciente, PacienteCreate } from '../types/paciente'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor para tratar erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // Pacientes
  getPacientes: async (): Promise<Paciente[]> => {
    const { data } = await api.get('/pacientes/')
    return data
  },

  getPaciente: async (id: number): Promise<Paciente> => {
    const { data } = await api.get(`/pacientes/${id}`)
    return data
  },

  createPaciente: async (paciente: PacienteCreate): Promise<Paciente> => {
    const { data } = await api.post('/pacientes/', paciente)
    return data
  },

  updatePaciente: async (id: number, paciente: Partial<PacienteCreate>): Promise<Paciente> => {
    const { data } = await api.put(`/pacientes/${id}`, paciente)
    return data
  },

  deletePaciente: async (id: number): Promise<void> => {
    await api.delete(`/pacientes/${id}`)
  },

  // Sessões
  getSessoes: async (pacienteId: number) => {
    const { data } = await api.get(`/sessoes/paciente/${pacienteId}`)
    return data
  },

  createSessao: async (sessao: { paciente_id: number; observacoes?: string }) => {
    const { data } = await api.post('/sessoes/', sessao)
    return data
  },

  // Análise
  getAngulosReferencia: async () => {
    const { data } = await api.get('/analise/referencias')
    return data
  },

  analisarFrame: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    const { data } = await api.post('/analise/frame', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return data
  },

  // Auth
  login: async (username: string, password: string) => {
    const { data } = await api.post('/auth/login',
      new URLSearchParams({ username, password }),
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    )
    return data
  },

  getCurrentUser: async () => {
    const { data } = await api.get('/auth/me')
    return data
  },
}
