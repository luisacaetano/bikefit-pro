import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Pacientes from './pages/Pacientes'
import NovaSessao from './pages/NovaSessao'
import Login from './pages/Login'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="pacientes" element={<Pacientes />} />
        <Route path="sessao/:pacienteId?" element={<NovaSessao />} />
      </Route>
    </Routes>
  )
}

export default App
