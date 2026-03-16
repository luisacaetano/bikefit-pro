export interface Sessao {
  id: number
  paciente_id: number
  data: string
  angulos_antes: Record<string, number> | null
  angulos_depois: Record<string, number> | null
  ajustes: Record<string, string> | null
  foto_antes_path: string | null
  foto_depois_path: string | null
  video_path: string | null
  relatorio_pdf_path: string | null
  observacoes: string | null
  status: 'em_andamento' | 'finalizada' | 'cancelada'
  criado_em: string
  finalizado_em: string | null
}

export interface SessaoCreate {
  paciente_id: number
  observacoes?: string
}

export interface SessaoFinalizar {
  angulos_depois: Record<string, number>
  ajustes: Record<string, string>
  observacoes?: string
}
