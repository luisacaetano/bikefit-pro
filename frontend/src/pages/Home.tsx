import { Link } from 'react-router-dom'
import { Users, Camera, FileText, Activity } from 'lucide-react'

const stats = [
  { label: 'Pacientes', value: '0', icon: Users, color: 'bg-blue-500' },
  { label: 'Sessões Hoje', value: '0', icon: Camera, color: 'bg-green-500' },
  { label: 'Relatórios', value: '0', icon: FileText, color: 'bg-purple-500' },
]

export default function Home() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="bg-white rounded-xl shadow-sm p-6 flex items-center gap-4"
          >
            <div className={`${stat.color} p-3 rounded-lg text-white`}>
              <stat.icon size={24} />
            </div>
            <div>
              <p className="text-gray-500 text-sm">{stat.label}</p>
              <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Ações Rápidas</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            to="/pacientes"
            className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors"
          >
            <Users className="text-primary-600" size={24} />
            <div>
              <p className="font-medium text-gray-800">Gerenciar Pacientes</p>
              <p className="text-sm text-gray-500">Cadastrar ou editar pacientes</p>
            </div>
          </Link>

          <Link
            to="/sessao"
            className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg hover:border-green-500 hover:bg-green-50 transition-colors"
          >
            <Activity className="text-green-600" size={24} />
            <div>
              <p className="font-medium text-gray-800">Iniciar Análise</p>
              <p className="text-sm text-gray-500">Nova sessão de bike fit</p>
            </div>
          </Link>
        </div>
      </div>

      {/* API Status */}
      <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-green-700 font-medium">Backend conectado</span>
        </div>
        <p className="text-green-600 text-sm mt-1">API rodando em http://localhost:8000</p>
      </div>
    </div>
  )
}
