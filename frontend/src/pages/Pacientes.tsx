import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Search, Edit, Trash2, User, History, Camera } from 'lucide-react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import type { Paciente, PacienteCreate } from '../types/paciente'

export default function Pacientes() {
  const [showForm, setShowForm] = useState(false)
  const [search, setSearch] = useState('')
  const [editingPaciente, setEditingPaciente] = useState<Paciente | null>(null)
  const queryClient = useQueryClient()

  const { data: pacientes = [], isLoading } = useQuery({
    queryKey: ['pacientes'],
    queryFn: api.getPacientes,
  })

  const createMutation = useMutation({
    mutationFn: api.createPaciente,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pacientes'] })
      setShowForm(false)
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<PacienteCreate> }) =>
      api.updatePaciente(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pacientes'] })
      setEditingPaciente(null)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: api.deletePaciente,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pacientes'] })
    },
  })

  const filteredPacientes = pacientes.filter((p: Paciente) =>
    p.nome.toLowerCase().includes(search.toLowerCase())
  )

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const data = {
      nome: formData.get('nome') as string,
      idade: Number(formData.get('idade')) || undefined,
      tipo_bike: formData.get('tipo_bike') as string || undefined,
      objetivo: formData.get('objetivo') as string || undefined,
    }
    createMutation.mutate(data)
  }

  const handleEditSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!editingPaciente) return

    const formData = new FormData(e.currentTarget)
    const data = {
      nome: formData.get('nome') as string,
      idade: Number(formData.get('idade')) || undefined,
      sexo: formData.get('sexo') as string || undefined,
      altura_cm: Number(formData.get('altura_cm')) || undefined,
      peso_kg: Number(formData.get('peso_kg')) || undefined,
      telefone: formData.get('telefone') as string || undefined,
      email: formData.get('email') as string || undefined,
      tipo_bike: formData.get('tipo_bike') as string || undefined,
      experiencia: formData.get('experiencia') as string || undefined,
      km_semana: Number(formData.get('km_semana')) || undefined,
      objetivo: formData.get('objetivo') as string || undefined,
      lesoes: formData.get('lesoes') as string || undefined,
      dores: formData.get('dores') as string || undefined,
      observacoes: formData.get('observacoes') as string || undefined,
    }
    updateMutation.mutate({ id: editingPaciente.id, data })
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Pacientes</h1>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
          <Plus size={20} />
          Novo Paciente
        </button>
      </div>

      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
        <input
          type="text"
          placeholder="Buscar paciente..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
      </div>

      {/* Create Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold mb-4">Novo Paciente</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nome *</label>
                <input
                  name="nome"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Idade</label>
                <input
                  name="idade"
                  type="number"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tipo de Bike</label>
                <select
                  name="tipo_bike"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Selecione...</option>
                  <option value="road">Road</option>
                  <option value="mtb">MTB</option>
                  <option value="triathlon">Triathlon</option>
                  <option value="gravel">Gravel</option>
                  <option value="urban">Urbano</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Objetivo</label>
                <select
                  name="objetivo"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Selecione...</option>
                  <option value="performance">Performance</option>
                  <option value="conforto">Conforto</option>
                  <option value="reabilitacao">Reabilitação</option>
                </select>
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={createMutation.isPending}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
                >
                  {createMutation.isPending ? 'Salvando...' : 'Salvar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Form Modal */}
      {editingPaciente && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-semibold mb-4">Editar Paciente</h2>
            <form onSubmit={handleEditSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Nome *</label>
                  <input
                    name="nome"
                    required
                    defaultValue={editingPaciente.nome}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Idade</label>
                  <input
                    name="idade"
                    type="number"
                    defaultValue={editingPaciente.idade || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Sexo</label>
                  <select
                    name="sexo"
                    defaultValue={editingPaciente.sexo || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="">Selecione...</option>
                    <option value="M">Masculino</option>
                    <option value="F">Feminino</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Altura (cm)</label>
                  <input
                    name="altura_cm"
                    type="number"
                    step="0.1"
                    defaultValue={editingPaciente.altura_cm || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Peso (kg)</label>
                  <input
                    name="peso_kg"
                    type="number"
                    step="0.1"
                    defaultValue={editingPaciente.peso_kg || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Telefone</label>
                  <input
                    name="telefone"
                    defaultValue={editingPaciente.telefone || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    name="email"
                    type="email"
                    defaultValue={editingPaciente.email || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Tipo de Bike</label>
                  <select
                    name="tipo_bike"
                    defaultValue={editingPaciente.tipo_bike || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="">Selecione...</option>
                    <option value="road">Road</option>
                    <option value="mtb">MTB</option>
                    <option value="triathlon">Triathlon</option>
                    <option value="gravel">Gravel</option>
                    <option value="urban">Urbano</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Experiência</label>
                  <select
                    name="experiencia"
                    defaultValue={editingPaciente.experiencia || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="">Selecione...</option>
                    <option value="iniciante">Iniciante</option>
                    <option value="intermediario">Intermediário</option>
                    <option value="avancado">Avançado</option>
                    <option value="profissional">Profissional</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Km/Semana</label>
                  <input
                    name="km_semana"
                    type="number"
                    step="0.1"
                    defaultValue={editingPaciente.km_semana || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Objetivo</label>
                  <select
                    name="objetivo"
                    defaultValue={editingPaciente.objetivo || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="">Selecione...</option>
                    <option value="performance">Performance</option>
                    <option value="conforto">Conforto</option>
                    <option value="reabilitacao">Reabilitação</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Lesões</label>
                <textarea
                  name="lesoes"
                  rows={2}
                  defaultValue={editingPaciente.lesoes || ''}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Histórico de lesões..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Dores</label>
                <textarea
                  name="dores"
                  rows={2}
                  defaultValue={editingPaciente.dores || ''}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Dores atuais ou recorrentes..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Observações</label>
                <textarea
                  name="observacoes"
                  rows={2}
                  defaultValue={editingPaciente.observacoes || ''}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Outras observações..."
                />
              </div>
              <div className="flex gap-2 justify-end pt-4 border-t">
                <button
                  type="button"
                  onClick={() => setEditingPaciente(null)}
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={updateMutation.isPending}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
                >
                  {updateMutation.isPending ? 'Salvando...' : 'Salvar Alterações'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* List */}
      {isLoading ? (
        <div className="text-center py-8 text-gray-500">Carregando...</div>
      ) : filteredPacientes.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          {search ? 'Nenhum paciente encontrado' : 'Nenhum paciente cadastrado'}
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Idade</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bike</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Objetivo</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredPacientes.map((paciente: Paciente) => (
                <tr key={paciente.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                        <User className="text-primary-600" size={20} />
                      </div>
                      <span className="font-medium text-gray-900">{paciente.nome}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-500">{paciente.idade || '-'}</td>
                  <td className="px-6 py-4 text-gray-500">{paciente.tipo_bike || '-'}</td>
                  <td className="px-6 py-4 text-gray-500">{paciente.objetivo || '-'}</td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end gap-1">
                      <Link
                        to={`/sessao/${paciente.id}`}
                        className="text-gray-400 hover:text-green-600 p-1"
                        title="Nova Sessão"
                      >
                        <Camera size={18} />
                      </Link>
                      <Link
                        to={`/pacientes/${paciente.id}/sessoes`}
                        className="text-gray-400 hover:text-blue-600 p-1"
                        title="Histórico"
                      >
                        <History size={18} />
                      </Link>
                      <button
                        onClick={() => setEditingPaciente(paciente)}
                        className="text-gray-400 hover:text-primary-600 p-1"
                        title="Editar"
                      >
                        <Edit size={18} />
                      </button>
                      <button
                        onClick={() => {
                          if (confirm('Excluir paciente?')) {
                            deleteMutation.mutate(paciente.id)
                          }
                        }}
                        className="text-gray-400 hover:text-red-600 p-1"
                        title="Excluir"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
