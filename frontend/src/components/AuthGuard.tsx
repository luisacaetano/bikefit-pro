import { Navigate, useLocation } from 'react-router-dom'
import { ReactNode } from 'react'

interface AuthGuardProps {
  children: ReactNode
}

export default function AuthGuard({ children }: AuthGuardProps) {
  const location = useLocation()
  const token = localStorage.getItem('token')

  if (!token) {
    // Redireciona para login, salvando a página que tentou acessar
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <>{children}</>
}
