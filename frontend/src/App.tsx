import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import AuthGuard from './components/AuthGuard'
import Home from './pages/Home'
import Pacientes from './pages/Pacientes'
import NovaSessao from './pages/NovaSessao'
import HistoricoSessoes from './pages/HistoricoSessoes'
import Login from './pages/Login'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <AuthGuard>
            <Layout />
          </AuthGuard>
        }
      >
        <Route index element={<Home />} />
        <Route path="pacientes" element={<Pacientes />} />
        <Route path="pacientes/:pacienteId/sessoes" element={<HistoricoSessoes />} />
        <Route path="sessao/:pacienteId?" element={<NovaSessao />} />
      </Route>
    </Routes>
  )
}

export default App
