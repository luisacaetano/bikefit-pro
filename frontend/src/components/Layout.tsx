import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { Home, Users, Camera, LogOut } from 'lucide-react'

const navItems = [
  { path: '/', icon: Home, label: 'Início' },
  { path: '/pacientes', icon: Users, label: 'Pacientes' },
  { path: '/sessao', icon: Camera, label: 'Nova Sessão' },
]

export default function Layout() {
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  const user = JSON.parse(localStorage.getItem('user') || '{}')

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-64 bg-primary-800 text-white flex flex-col">
        <div className="p-6">
          <h1 className="text-2xl font-bold">BikeFit Pro</h1>
          <p className="text-primary-200 text-sm">Análise Postural</p>
        </div>

        <nav className="mt-6 flex-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-6 py-3 transition-colors ${
                  isActive
                    ? 'bg-primary-700 border-r-4 border-white'
                    : 'hover:bg-primary-700'
                }`}
              >
                <item.icon size={20} />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>

        <div className="p-4 border-t border-primary-700">
          {user.username && (
            <p className="text-primary-200 text-sm mb-2">
              Olá, {user.username}
            </p>
          )}
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 text-primary-200 hover:text-white transition-colors w-full"
          >
            <LogOut size={20} />
            <span>Sair</span>
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 p-8 bg-gray-50 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
