import { useState, useRef, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Camera, Play, Pause, Save, RotateCcw, AlertTriangle, ImageIcon, Check } from 'lucide-react'
import api from '../services/api'

// Tipos
type AnalysisMode = 'static' | 'dynamic'
type CyclingDiscipline = 'road' | 'mtb' | 'triathlon' | 'gravel' | 'urban'

interface SpineData {
  spine_top: { x: number; y: number; label: string }
  spine_mid: { x: number; y: number; label: string }
  spine_low: { x: number; y: number; label: string }
  spine_angle: number
  curvature_type: 'neutral' | 'kyphosis' | 'lordosis'
  curvature_severity: 'normal' | 'mild' | 'moderate' | 'severe'
  spine_length: number
}

interface InjuryRisk {
  type: string
  joint: string
  severity: string
  message: string
  reference: string
}

interface AnalysisResult {
  keypoints: Record<string, { x: number; y: number; confidence: number }> | null
  angles: {
    knee: number | null
    knee_extension: number | null
    knee_flexion_bdc: number | null
    hip: number | null
    ankle: number | null
    elbow: number | null
    trunk: number | null
    spine: SpineData | null
    analysis_mode: string
    discipline: string
  } | null
  recommendations: {
    overall_status: string
    summary: string
    priority_adjustments: Array<{ angle: string; severity: string; action: string }>
    injury_risks: InjuryRisk[]
    mode: string
    discipline: string
  } | null
  frame: string | null
}

interface CapturedFrame {
  image: string
  angles: Record<string, number>
  timestamp: Date
}

const disciplineLabels: Record<CyclingDiscipline, string> = {
  road: 'Road (Estrada)',
  mtb: 'Mountain Bike',
  triathlon: 'Triathlon/TT',
  gravel: 'Gravel',
  urban: 'Urbano/Commute'
}

export default function NovaSessao() {
  const { pacienteId } = useParams()
  const navigate = useNavigate()
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const wsRef = useRef<WebSocket | null>(null)

  // Estados principais
  const [isStreaming, setIsStreaming] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [side, setSide] = useState<'left' | 'right'>('right')
  const [mode, setMode] = useState<AnalysisMode>('dynamic')
  const [discipline, setDiscipline] = useState<CyclingDiscipline>('road')

  // Estados para comparativo antes/depois
  const [capturedBefore, setCapturedBefore] = useState<CapturedFrame | null>(null)
  const [capturedAfter, setCapturedAfter] = useState<CapturedFrame | null>(null)
  const [showComparison, setShowComparison] = useState(false)
  const [ajustes, setAjustes] = useState<Record<string, string>>({})
  const [observacoes, setObservacoes] = useState('')
  const [saving, setSaving] = useState(false)

  // Buscar dados do paciente
  const { data: paciente } = useQuery({
    queryKey: ['paciente', pacienteId],
    queryFn: () => api.getPaciente(Number(pacienteId)),
    enabled: !!pacienteId,
  })

  // Iniciar webcam
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 },
      })
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        setIsStreaming(true)
        setError(null)
      }
    } catch (err) {
      setError('Erro ao acessar câmera. Verifique as permissões.')
      console.error(err)
    }
  }

  // Parar webcam
  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks()
      tracks.forEach((track) => track.stop())
      videoRef.current.srcObject = null
      setIsStreaming(false)
    }
  }

  // Conectar WebSocket
  const connectWebSocket = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return

    const ws = new WebSocket('ws://localhost:8000/ws/video')

    ws.onopen = () => {
      console.log('WebSocket conectado')
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'result') {
        setAnalysis(data)
      } else if (data.error) {
        console.error('Erro do servidor:', data.error)
      }
    }

    ws.onerror = (err) => {
      console.error('WebSocket erro:', err)
      setError('Erro de conexão com o servidor')
    }

    ws.onclose = () => {
      console.log('WebSocket desconectado')
      setIsAnalyzing(false)
    }

    wsRef.current = ws
  }, [])

  // Enviar frame para análise
  const sendFrame = useCallback(() => {
    if (!videoRef.current || !canvasRef.current || !wsRef.current) return
    if (wsRef.current.readyState !== WebSocket.OPEN) return

    const canvas = canvasRef.current
    const video = videoRef.current
    const ctx = canvas.getContext('2d')

    if (!ctx) return

    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    ctx.drawImage(video, 0, 0)

    const frameData = canvas.toDataURL('image/jpeg', 0.8)

    wsRef.current.send(
      JSON.stringify({
        type: 'frame',
        data: frameData,
        side: side,
        mode: mode,
        discipline: discipline,
      })
    )
  }, [side, mode, discipline])

  // Capturar frame atual
  const captureFrame = (type: 'before' | 'after') => {
    if (!analysis?.frame || !analysis?.angles) return

    const angles: Record<string, number> = {}
    if (analysis.angles.knee_flexion_bdc) angles.knee_flexion_bdc = analysis.angles.knee_flexion_bdc
    if (analysis.angles.knee_extension) angles.knee_extension = analysis.angles.knee_extension
    if (analysis.angles.hip) angles.hip = analysis.angles.hip
    if (analysis.angles.trunk) angles.trunk = analysis.angles.trunk
    if (analysis.angles.ankle) angles.ankle = analysis.angles.ankle
    if (analysis.angles.elbow) angles.elbow = analysis.angles.elbow

    const captured: CapturedFrame = {
      image: analysis.frame,
      angles,
      timestamp: new Date(),
    }

    if (type === 'before') {
      setCapturedBefore(captured)
    } else {
      setCapturedAfter(captured)
    }
  }

  // Salvar sessão
  const handleSave = async () => {
    if (!pacienteId || !capturedBefore) {
      setError('Capture pelo menos o frame "Antes" para salvar')
      return
    }

    setSaving(true)
    setError(null)
    try {
      // Criar sessão com ângulos antes e imagem
      const sessao = await api.createSessao({
        paciente_id: Number(pacienteId),
        angulos_antes: capturedBefore.angles,
        foto_antes_base64: capturedBefore.image,
        observacoes: observacoes || undefined,
      })

      // Se tiver captura "depois", finalizar a sessão
      if (capturedAfter) {
        await api.finalizarSessao(
          sessao.id,
          capturedAfter.angles,
          ajustes,
          capturedAfter.image
        )
      }

      alert('Sessão salva com sucesso!')
      navigate(`/pacientes/${pacienteId}/sessoes`)
    } catch (err) {
      console.error('Erro ao salvar:', err)
      setError('Erro ao salvar sessão. Tente novamente.')
    } finally {
      setSaving(false)
    }
  }

  // Loop de análise
  useEffect(() => {
    let intervalId: number | null = null

    if (isAnalyzing && isStreaming) {
      connectWebSocket()
      intervalId = window.setInterval(sendFrame, 100)
    }

    return () => {
      if (intervalId) clearInterval(intervalId)
    }
  }, [isAnalyzing, isStreaming, connectWebSocket, sendFrame])

  // Cleanup
  useEffect(() => {
    return () => {
      stopCamera()
      wsRef.current?.close()
    }
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'optimal':
        return 'text-green-600 bg-green-100'
      case 'minor_adjustments':
        return 'text-yellow-600 bg-yellow-100'
      case 'needs_adjustment':
        return 'text-orange-600 bg-orange-100'
      case 'injury_risk':
        return 'text-red-600 bg-red-100'
      default:
        return 'text-gray-600 bg-gray-100'
    }
  }

  const getAngleStatus = (angle: number | null, optimal: number, tolerance: number) => {
    if (angle === null) return 'bg-gray-200'
    const diff = Math.abs(angle - optimal)
    if (diff <= tolerance) return 'bg-green-500'
    if (diff <= tolerance * 2) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const calculateDifference = (before: number | undefined, after: number | undefined) => {
    if (before === undefined || after === undefined) return null
    return after - before
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Nova Sessão de Análise</h1>
          {paciente && (
            <p className="text-gray-500">Paciente: {paciente.nome}</p>
          )}
        </div>
        {(capturedBefore || capturedAfter) && (
          <button
            onClick={() => setShowComparison(!showComparison)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              showComparison
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            <ImageIcon size={20} />
            {showComparison ? 'Voltar à Análise' : 'Ver Comparativo'}
          </button>
        )}
      </div>

      {/* Comparison View */}
      {showComparison ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Before */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-3 h-3 bg-red-500 rounded-full"></span>
                ANTES
              </h3>
              {capturedBefore ? (
                <>
                  <img
                    src={capturedBefore.image}
                    alt="Antes"
                    className="w-full rounded-lg mb-4"
                  />
                  <div className="space-y-2">
                    {Object.entries(capturedBefore.angles).map(([key, value]) => (
                      <div key={key} className="flex justify-between text-sm">
                        <span className="text-gray-600">{key}</span>
                        <span className="font-mono">{value.toFixed(1)}°</span>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
                  Nenhuma captura
                </div>
              )}
            </div>

            {/* After */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                DEPOIS
              </h3>
              {capturedAfter ? (
                <>
                  <img
                    src={capturedAfter.image}
                    alt="Depois"
                    className="w-full rounded-lg mb-4"
                  />
                  <div className="space-y-2">
                    {Object.entries(capturedAfter.angles).map(([key, value]) => {
                      const diff = calculateDifference(
                        capturedBefore?.angles[key],
                        value
                      )
                      return (
                        <div key={key} className="flex justify-between text-sm">
                          <span className="text-gray-600">{key}</span>
                          <div className="flex items-center gap-2">
                            <span className="font-mono">{value.toFixed(1)}°</span>
                            {diff !== null && (
                              <span
                                className={`text-xs ${
                                  diff > 0 ? 'text-red-500' : diff < 0 ? 'text-green-500' : 'text-gray-400'
                                }`}
                              >
                                ({diff > 0 ? '+' : ''}{diff.toFixed(1)}°)
                              </span>
                            )}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </>
              ) : (
                <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
                  Nenhuma captura
                </div>
              )}
            </div>
          </div>

          {/* Adjustments and Notes */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="font-semibold text-gray-800 mb-4">Ajustes Realizados</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Altura do Selim</label>
                <input
                  type="text"
                  value={ajustes.selim || ''}
                  onChange={(e) => setAjustes({ ...ajustes, selim: e.target.value })}
                  placeholder="Ex: +5mm"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Recuo do Selim</label>
                <input
                  type="text"
                  value={ajustes.recuo || ''}
                  onChange={(e) => setAjustes({ ...ajustes, recuo: e.target.value })}
                  placeholder="Ex: -10mm"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Altura do Guidão</label>
                <input
                  type="text"
                  value={ajustes.guidao || ''}
                  onChange={(e) => setAjustes({ ...ajustes, guidao: e.target.value })}
                  placeholder="Ex: +15mm"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Observações</label>
              <textarea
                value={observacoes}
                onChange={(e) => setObservacoes(e.target.value)}
                rows={3}
                placeholder="Observações adicionais sobre a sessão..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          {/* Save Button */}
          <button
            onClick={handleSave}
            disabled={!capturedBefore || saving}
            className="w-full flex items-center justify-center gap-2 bg-primary-600 text-white px-6 py-4 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed text-lg font-medium"
          >
            {saving ? (
              'Salvando...'
            ) : (
              <>
                <Save size={24} />
                Salvar Sessão
              </>
            )}
          </button>
        </div>
      ) : (
        /* Analysis View */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Video Feed */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm p-4">
              <div className="relative aspect-video bg-gray-900 rounded-lg overflow-hidden">
                {analysis?.frame ? (
                  <img
                    src={analysis.frame}
                    alt="Análise"
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-full object-contain"
                  />
                )}

                {!isStreaming && (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <button
                      onClick={startCamera}
                      className="flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700"
                    >
                      <Camera size={24} />
                      Iniciar Câmera
                    </button>
                  </div>
                )}

                {/* Capture indicators */}
                <div className="absolute top-4 right-4 flex gap-2">
                  {capturedBefore && (
                    <div className="bg-red-500 text-white px-2 py-1 rounded text-xs flex items-center gap-1">
                      <Check size={12} />
                      ANTES
                    </div>
                  )}
                  {capturedAfter && (
                    <div className="bg-green-500 text-white px-2 py-1 rounded text-xs flex items-center gap-1">
                      <Check size={12} />
                      DEPOIS
                    </div>
                  )}
                </div>

                {error && (
                  <div className="absolute bottom-4 left-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg">
                    {error}
                  </div>
                )}
              </div>

              {/* Controls */}
              <div className="flex flex-wrap items-center justify-between gap-4 mt-4">
                <div className="flex flex-wrap items-center gap-4">
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600">Lado:</span>
                    <select
                      value={side}
                      onChange={(e) => setSide(e.target.value as 'left' | 'right')}
                      className="border border-gray-300 rounded px-2 py-1 text-sm"
                    >
                      <option value="right">Direito</option>
                      <option value="left">Esquerdo</option>
                    </select>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600">Modo:</span>
                    <select
                      value={mode}
                      onChange={(e) => setMode(e.target.value as AnalysisMode)}
                      className="border border-gray-300 rounded px-2 py-1 text-sm"
                    >
                      <option value="dynamic">Dinâmico (pedalando)</option>
                      <option value="static">Estático (parado)</option>
                    </select>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600">Modalidade:</span>
                    <select
                      value={discipline}
                      onChange={(e) => setDiscipline(e.target.value as CyclingDiscipline)}
                      className="border border-gray-300 rounded px-2 py-1 text-sm"
                    >
                      {Object.entries(disciplineLabels).map(([value, label]) => (
                        <option key={value} value={value}>{label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="flex gap-2">
                  {isStreaming && (
                    <>
                      <button
                        onClick={() => setIsAnalyzing(!isAnalyzing)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                          isAnalyzing
                            ? 'bg-yellow-500 hover:bg-yellow-600 text-white'
                            : 'bg-green-500 hover:bg-green-600 text-white'
                        }`}
                      >
                        {isAnalyzing ? <Pause size={20} /> : <Play size={20} />}
                        {isAnalyzing ? 'Pausar' : 'Analisar'}
                      </button>
                      <button
                        onClick={stopCamera}
                        className="flex items-center gap-2 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
                      >
                        <RotateCcw size={20} />
                        Parar
                      </button>
                    </>
                  )}
                </div>
              </div>

              {/* Capture Buttons */}
              {isAnalyzing && analysis?.frame && (
                <div className="flex gap-4 mt-4 pt-4 border-t">
                  <button
                    onClick={() => captureFrame('before')}
                    className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg transition-colors ${
                      capturedBefore
                        ? 'bg-red-100 text-red-700 border-2 border-red-500'
                        : 'bg-red-500 text-white hover:bg-red-600'
                    }`}
                  >
                    <Camera size={20} />
                    {capturedBefore ? 'Recapturar ANTES' : 'Capturar ANTES'}
                  </button>
                  <button
                    onClick={() => captureFrame('after')}
                    className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg transition-colors ${
                      capturedAfter
                        ? 'bg-green-100 text-green-700 border-2 border-green-500'
                        : 'bg-green-500 text-white hover:bg-green-600'
                    }`}
                  >
                    <Camera size={20} />
                    {capturedAfter ? 'Recapturar DEPOIS' : 'Capturar DEPOIS'}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Analysis Panel */}
          <div className="space-y-4">
            {/* Status */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h3 className="font-semibold text-gray-800 mb-3">Status</h3>
              {analysis?.recommendations ? (
                <div
                  className={`px-4 py-3 rounded-lg ${getStatusColor(
                    analysis.recommendations.overall_status
                  )}`}
                >
                  <p className="font-medium">{analysis.recommendations.summary}</p>
                </div>
              ) : (
                <p className="text-gray-500 text-sm">Inicie a análise para ver o status</p>
              )}
            </div>

            {/* Angles */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h3 className="font-semibold text-gray-800 mb-3">Ângulos Medidos</h3>
              <p className="text-xs text-gray-500 mb-2">
                Modo: {mode === 'dynamic' ? 'Dinâmico' : 'Estático'} | {disciplineLabels[discipline]}
              </p>
              <div className="space-y-3">
                {[
                  { key: 'knee_flexion_bdc', label: 'Flexão Joelho (BDC)', optimal: mode === 'dynamic' ? 38 : 30, tolerance: 5 },
                  { key: 'knee_extension', label: 'Extensão Joelho', optimal: mode === 'dynamic' ? 142 : 150, tolerance: 5 },
                  { key: 'hip', label: 'Quadril', optimal: mode === 'dynamic' ? 40 : 45, tolerance: 5 },
                  { key: 'trunk', label: 'Tronco', optimal: 47, tolerance: 7 },
                  { key: 'elbow', label: 'Cotovelo', optimal: 160, tolerance: 10 },
                ].map((item) => {
                  const value = analysis?.angles?.[item.key as keyof typeof analysis.angles]
                  return (
                    <div key={item.key} className="flex items-center justify-between">
                      <span className="text-gray-600 text-sm">{item.label}</span>
                      <div className="flex items-center gap-2">
                        <div
                          className={`w-3 h-3 rounded-full ${getAngleStatus(
                            typeof value === 'number' ? value : null,
                            item.optimal,
                            item.tolerance
                          )}`}
                        />
                        <span className="font-mono font-medium w-16 text-right">
                          {typeof value === 'number' ? `${value.toFixed(1)}°` : '--'}
                        </span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Spine */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h3 className="font-semibold text-gray-800 mb-3">Coluna Vertebral</h3>
              {analysis?.angles?.spine ? (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Tipo</span>
                    <span className={`px-2 py-1 rounded text-sm font-medium ${
                      analysis.angles.spine.curvature_type === 'neutral'
                        ? 'bg-green-100 text-green-700'
                        : analysis.angles.spine.curvature_type === 'kyphosis'
                        ? 'bg-red-100 text-red-700'
                        : 'bg-blue-100 text-blue-700'
                    }`}>
                      {analysis.angles.spine.curvature_type === 'neutral' && 'Neutra'}
                      {analysis.angles.spine.curvature_type === 'kyphosis' && 'Cifose'}
                      {analysis.angles.spine.curvature_type === 'lordosis' && 'Lordose'}
                    </span>
                  </div>
                  {analysis.angles.spine.curvature_type !== 'neutral' && (
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Severidade</span>
                      <span className={`px-2 py-1 rounded text-sm font-medium ${
                        analysis.angles.spine.curvature_severity === 'mild'
                          ? 'bg-yellow-100 text-yellow-700'
                          : analysis.angles.spine.curvature_severity === 'moderate'
                          ? 'bg-orange-100 text-orange-700'
                          : 'bg-red-100 text-red-700'
                      }`}>
                        {analysis.angles.spine.curvature_severity === 'mild' && 'Leve'}
                        {analysis.angles.spine.curvature_severity === 'moderate' && 'Moderada'}
                        {analysis.angles.spine.curvature_severity === 'severe' && 'Severa'}
                      </span>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">
                  Posicione-se de lado para análise
                </p>
              )}
            </div>

            {/* Injury Risks */}
            {analysis?.recommendations?.injury_risks &&
              analysis.recommendations.injury_risks.length > 0 && (
                <div className="bg-red-50 rounded-xl shadow-sm p-4 border border-red-200">
                  <h3 className="font-semibold text-red-800 mb-3 flex items-center gap-2">
                    <AlertTriangle size={18} />
                    Alertas de Risco
                  </h3>
                  <div className="space-y-2">
                    {analysis.recommendations.injury_risks.map((risk, i) => (
                      <div
                        key={i}
                        className="p-3 rounded-lg text-sm bg-red-100 border border-red-300"
                      >
                        <p className="font-medium text-red-800">{risk.message}</p>
                        <p className="text-xs text-red-600 mt-1">Ref: {risk.reference}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            {/* Recommendations */}
            {analysis?.recommendations?.priority_adjustments &&
              analysis.recommendations.priority_adjustments.length > 0 && (
                <div className="bg-white rounded-xl shadow-sm p-4">
                  <h3 className="font-semibold text-gray-800 mb-3">Ajustes Recomendados</h3>
                  <div className="space-y-2">
                    {analysis.recommendations.priority_adjustments.map((adj, i) => (
                      <div
                        key={i}
                        className={`p-3 rounded-lg text-sm ${
                          adj.severity === 'high'
                            ? 'bg-red-50 border border-red-200'
                            : 'bg-yellow-50 border border-yellow-200'
                        }`}
                      >
                        {adj.action}
                      </div>
                    ))}
                  </div>
                </div>
              )}
          </div>
        </div>
      )}

      {/* Hidden canvas */}
      <canvas ref={canvasRef} className="hidden" />
    </div>
  )
}
