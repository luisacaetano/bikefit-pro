export interface Paciente {
  id: number
  nome: string
  idade?: number
  sexo?: string
  altura_cm?: number
  peso_kg?: number
  telefone?: string
  email?: string
  tipo_bike?: string
  experiencia?: string
  km_semana?: number
  objetivo?: string
  lesoes?: string
  dores?: string
  observacoes?: string
  criado_em: string
  atualizado_em: string
}

export interface PacienteCreate {
  nome: string
  idade?: number
  sexo?: string
  altura_cm?: number
  peso_kg?: number
  telefone?: string
  email?: string
  tipo_bike?: string
  experiencia?: string
  km_semana?: number
  objetivo?: string
  lesoes?: string
  dores?: string
  observacoes?: string
}
