import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowLeft, Calendar, CheckCircle, Clock, XCircle, Camera, Download } from 'lucide-react'
import { useState } from 'react'
import api from '../services/api'
import type { Sessao } from '../types/sessao'

export default function HistoricoSessoes() {
  const { pacienteId } = useParams()
  const id = Number(pacienteId)
  const [downloadingPdf, setDownloadingPdf] = useState<number | null>(null)

  const handleDownloadPdf = async (sessaoId: number) => {
    try {
      setDownloadingPdf(sessaoId)
      const blob = await api.downloadPdfSessao(sessaoId)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `bikefit_sessao_${sessaoId}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Erro ao baixar PDF:', error)
      alert('Erro ao gerar PDF. Tente novamente.')
    } finally {
      setDownloadingPdf(null)
    }
  }

  const { data: paciente, isLoading: loadingPaciente } = useQuery({
    queryKey: ['paciente', id],
    queryFn: () => api.getPaciente(id),
    enabled: !!id,
  })

  const { data: sessoes = [], isLoading: loadingSessoes } = useQuery({
    queryKey: ['sessoes', id],
    queryFn: () => api.getSessoes(id),
    enabled: !!id,
  })

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'finalizada':
        return <CheckCircle className="text-green-500" size={20} />
      case 'em_andamento':
        return <Clock className="text-yellow-500" size={20} />
      case 'cancelada':
        return <XCircle className="text-red-500" size={20} />
      default:
        return <Clock className="text-gray-400" size={20} />
    }
  }

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'finalizada':
        return 'Finalizada'
      case 'em_andamento':
        return 'Em andamento'
      case 'cancelada':
        return 'Cancelada'
      default:
        return status
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const formatAngle = (value: number | undefined) => {
    if (value === undefined || value === null) return '--'
    return `${value.toFixed(1)}°`
  }

  if (loadingPaciente || loadingSessoes) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Carregando...</div>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <Link
          to="/pacientes"
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft size={24} />
        </Link>
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Histórico de Sessões</h1>
          <p className="text-gray-500">
            Paciente: {paciente?.nome || 'Carregando...'}
          </p>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-4 mb-6">
        <Link
          to={`/sessao/${id}`}
          className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
          <Camera size={20} />
          Nova Sessão
        </Link>
      </div>

      {/* Sessions List */}
      {sessoes.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm p-8 text-center">
          <Calendar className="mx-auto text-gray-300 mb-4" size={48} />
          <h3 className="text-lg font-medium text-gray-700 mb-2">Nenhuma sessão registrada</h3>
          <p className="text-gray-500 mb-4">
            Inicie uma nova sessão de análise para este paciente.
          </p>
          <Link
            to={`/sessao/${id}`}
            className="inline-flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
          >
            <Camera size={20} />
            Iniciar Sessão
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {sessoes.map((sessao: Sessao) => (
            <div
              key={sessao.id}
              className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  {getStatusIcon(sessao.status)}
                  <div>
                    <h3 className="font-semibold text-gray-800">
                      Sessão #{sessao.id}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {formatDate(sessao.criado_em)}
                    </p>
                  </div>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    sessao.status === 'finalizada'
                      ? 'bg-green-100 text-green-700'
                      : sessao.status === 'em_andamento'
                      ? 'bg-yellow-100 text-yellow-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {getStatusLabel(sessao.status)}
                </span>
              </div>

              {/* Angles Comparison */}
              {(sessao.angulos_antes || sessao.angulos_depois) && (
                <div className="grid grid-cols-2 gap-4 mb-4">
                  {sessao.angulos_antes && (
                    <div className="bg-gray-50 rounded-lg p-4">
                      <h4 className="font-medium text-gray-700 mb-2">Ângulos Antes</h4>
                      <div className="space-y-1 text-sm">
                        {Object.entries(sessao.angulos_antes).map(([key, value]) => (
                          <div key={key} className="flex justify-between">
                            <span className="text-gray-600">{key}</span>
                            <span className="font-mono">{formatAngle(value as number)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  {sessao.angulos_depois && (
                    <div className="bg-green-50 rounded-lg p-4">
                      <h4 className="font-medium text-green-700 mb-2">Ângulos Depois</h4>
                      <div className="space-y-1 text-sm">
                        {Object.entries(sessao.angulos_depois).map(([key, value]) => (
                          <div key={key} className="flex justify-between">
                            <span className="text-gray-600">{key}</span>
                            <span className="font-mono">{formatAngle(value as number)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Adjustments */}
              {sessao.ajustes && Object.keys(sessao.ajustes).length > 0 && (
                <div className="bg-blue-50 rounded-lg p-4 mb-4">
                  <h4 className="font-medium text-blue-700 mb-2">Ajustes Realizados</h4>
                  <div className="space-y-1 text-sm">
                    {Object.entries(sessao.ajustes).map(([key, value]) => (
                      <div key={key} className="flex justify-between">
                        <span className="text-gray-600 capitalize">{key.replace('_', ' ')}</span>
                        <span>{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Observations */}
              {sessao.observacoes && (
                <div className="text-sm text-gray-600 mb-4">
                  <strong>Observações:</strong> {sessao.observacoes}
                </div>
              )}

              {/* Actions */}
              <div className="flex gap-2 pt-4 border-t">
                {sessao.status === 'finalizada' && (
                  <button
                    onClick={() => handleDownloadPdf(sessao.id)}
                    disabled={downloadingPdf === sessao.id}
                    className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700 disabled:opacity-50"
                  >
                    {downloadingPdf === sessao.id ? (
                      <>
                        <div className="animate-spin h-4 w-4 border-2 border-primary-600 border-t-transparent rounded-full" />
                        Gerando...
                      </>
                    ) : (
                      <>
                        <Download size={16} />
                        Download PDF
                      </>
                    )}
                  </button>
                )}
                {sessao.status === 'em_andamento' && (
                  <Link
                    to={`/sessao/${id}?sessao=${sessao.id}`}
                    className="flex items-center gap-2 text-sm text-green-600 hover:text-green-700"
                  >
                    <Camera size={16} />
                    Continuar Sessão
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
