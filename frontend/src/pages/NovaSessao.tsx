import { useState, useRef, useEffect, useCallback } from 'react'
import { Camera, Play, Pause, Save, RotateCcw } from 'lucide-react'

interface AnalysisResult {
  keypoints: Record<string, { x: number; y: number; confidence: number }> | null
  angles: {
    knee: number | null
    hip: number | null
    ankle: number | null
    elbow: number | null
    trunk: number | null
  } | null
  recommendations: {
    overall_status: string
    summary: string
    priority_adjustments: Array<{ angle: string; severity: string; action: string }>
  } | null
  frame: string | null
}

export default function NovaSessao() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const wsRef = useRef<WebSocket | null>(null)

  const [isStreaming, setIsStreaming] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [side, setSide] = useState<'left' | 'right'>('right')

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
      })
    )
  }, [side])

  // Loop de análise
  useEffect(() => {
    let intervalId: number | null = null

    if (isAnalyzing && isStreaming) {
      connectWebSocket()
      intervalId = window.setInterval(sendFrame, 100) // ~10 FPS
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

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Nova Sessão de Análise</h1>

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

              {error && (
                <div className="absolute bottom-4 left-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg">
                  {error}
                </div>
              )}
            </div>

            {/* Controls */}
            <div className="flex items-center justify-between mt-4">
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">Lado:</span>
                <select
                  value={side}
                  onChange={(e) => setSide(e.target.value as 'left' | 'right')}
                  className="border border-gray-300 rounded px-2 py-1"
                >
                  <option value="right">Direito</option>
                  <option value="left">Esquerdo</option>
                </select>
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
            <div className="space-y-3">
              {[
                { key: 'knee', label: 'Joelho', optimal: 145, tolerance: 5 },
                { key: 'hip', label: 'Quadril', optimal: 45, tolerance: 5 },
                { key: 'trunk', label: 'Tronco', optimal: 47, tolerance: 7 },
                { key: 'elbow', label: 'Cotovelo', optimal: 160, tolerance: 10 },
              ].map((item) => {
                const value = analysis?.angles?.[item.key as keyof typeof analysis.angles]
                return (
                  <div key={item.key} className="flex items-center justify-between">
                    <span className="text-gray-600">{item.label}</span>
                    <div className="flex items-center gap-2">
                      <div
                        className={`w-3 h-3 rounded-full ${getAngleStatus(
                          value ?? null,
                          item.optimal,
                          item.tolerance
                        )}`}
                      />
                      <span className="font-mono font-medium w-16 text-right">
                        {value !== null && value !== undefined ? `${value.toFixed(1)}°` : '--'}
                      </span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

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

          {/* Save Button */}
          <button
            disabled={!analysis}
            className="w-full flex items-center justify-center gap-2 bg-primary-600 text-white px-4 py-3 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save size={20} />
            Salvar Análise
          </button>
        </div>
      </div>

      {/* Hidden canvas for frame capture */}
      <canvas ref={canvasRef} className="hidden" />
    </div>
  )
}
