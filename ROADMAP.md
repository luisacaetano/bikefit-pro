# Roadmap de Desenvolvimento - BikeFit Pro

> Guia passo a passo para não se perder

---

## Comandos Git (Push para ambas contas)

```bash
# Push rápido (alias configurado)
git pushall

# Ou manualmente
git push origin main && git push lluisa main

# Commit + Push
git add .
git commit -m "feat: descrição"
git pushall
```

**Repositórios:**
- `origin` → https://github.com/luisacaetano/bikefit-pro
- `lluisa` → https://github.com/lluisacaetano/bikefit-pro

---

## Visão Geral das Fases

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FASE 1          FASE 2          FASE 3          FASE 4          FASE 5│
│  Setup           Backend         Frontend        Integração      TCC   │
│  ─────           ───────         ────────        ──────────      ───   │
│  Ambiente        API REST        Interface       Tudo junto      Docs  │
│  Docker          YOLOv8          React           WebSocket       Teste │
│  PostgreSQL      Banco           Componentes     Validação       PDF   │
│                                                                        │
│  [██████]        [██████]        [██████]        [██████]        [░░░░]│
│  ✅ COMPLETO     ✅ COMPLETO     ✅ COMPLETO     ✅ COMPLETO           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## FASE 1: Setup do Ambiente ✅ COMPLETO
**Concluído em: 13/03/2026**

### 1.1 Pré-requisitos
- [x] Docker Desktop instalado
- [x] Node.js 20+ instalado
- [x] Python 3.11+ (Mac M3)
- [x] App Camo no celular

### 1.2 Projeto configurado
- [x] Estrutura criada em ~/Desktop/TCC/
- [x] Repositórios Git configurados

### 1.3 Banco de dados
- [x] PostgreSQL rodando via Docker
- [x] Conexão testada

### 1.4 Backend configurado
- [x] Virtual environment criado
- [x] Dependências instaladas
- [x] Arquivo .env configurado

### 1.5 Frontend configurado
- [x] Dependências npm instaladas
- [x] Vite + React + TypeScript

### 1.6 Setup testado
- [x] Backend rodando em http://localhost:8000
- [x] Frontend rodando em http://localhost:3000
- [x] Swagger docs funcionando

---

## FASE 2: Backend Core ✅ COMPLETO
**Concluído em: 14/03/2026**

### 2.1 Banco de Dados
- [x] Models SQLAlchemy (Paciente, Sessao, Medidas)
- [x] Alembic configurado
- [x] Migrations funcionando
- [x] CRUD implementado

### 2.2 YOLOv8 Pose Detection
- [x] YOLOv8-pose testado com imagens
- [x] Classe PoseDetector implementada
- [x] Testado com webcam/Camo
- [x] 17 keypoints detectados corretamente

### 2.3 Cálculo de Ângulos ✅ ATUALIZADO COM LITERATURA CIENTÍFICA
- [x] AngleCalculator implementado
- [x] Ângulo de extensão do joelho (knee_extension)
- [x] **NOVO:** Ângulo de flexão no BDC (knee_flexion_bdc) - Bini & Hume 2020
- [x] Ângulo do quadril
- [x] Ângulo do tornozelo
- [x] Ângulo do tronco
- [x] Ângulo do cotovelo
- [x] **NOVO:** Detecção de coluna vertebral (3 pontos: C7/T1, T12/L1, L5/S1)
- [x] **NOVO:** Classificação de curvatura (neutra/cifose/lordose)
- [x] **NOVO:** Modo estático vs dinâmico (Bini et al. 2023)
- [x] **NOVO:** Suporte a modalidades (road, mtb, triathlon, gravel, urban)

### 2.4 Sistema de Recomendações
- [x] RecommendationEngine implementado
- [x] Regras baseadas em literatura científica
- [x] **NOVO:** Alertas de risco de lesão (Martínez & Pérez 2025)
- [x] **NOVO:** Referências a papers em cada recomendação

### 2.5 API REST Completa
- [x] CRUD de Pacientes
- [x] CRUD de Sessões
- [x] Endpoint de análise de frame
- [x] Endpoints testados no Swagger

### 2.6 WebSocket para Streaming
- [x] Endpoint WebSocket implementado
- [x] Recebe frames do frontend
- [x] Processa e retorna ângulos em tempo real
- [x] **NOVO:** Suporte a configuração de modo/modalidade em tempo real
- [x] Latência testada (~38ms - excelente!)

---

## FASE 3: Frontend React ✅ COMPLETO
**Concluído em: 15/03/2026**

### 3.1 Setup e Estrutura
- [x] TailwindCSS configurado
- [x] React Router configurado
- [x] Layout base criado
- [x] React Query (TanStack Query)

### 3.2 Página de Login
- [x] Tela de login básica
- [x] Integrar com API de auth
- [x] Token no localStorage
- [x] Redirect após login
- [x] **NOVO:** AuthGuard para proteção de rotas

### 3.3 Página de Pacientes
- [x] Lista de pacientes
- [x] Formulário de cadastro
- [x] Edição de paciente (modal)
- [x] Busca/filtro
- [x] Integração com API
- [x] **NOVO:** Botões de ação (Nova Sessão, Histórico, Editar, Excluir)

### 3.4 Página de Nova Sessão (CORE) ✅ FUNCIONAL
- [x] Captura de vídeo da webcam
- [x] Envio de frames via WebSocket
- [x] Exibição do skeleton sobre o vídeo
- [x] Ângulos em tempo real
- [x] Seleção de modo (estático/dinâmico)
- [x] Seleção de modalidade (road, mtb, etc.)
- [x] Exibição de knee_flexion_bdc
- [x] Alertas de risco de lesão
- [x] Alertas (verde/amarelo/vermelho)
- [x] Recomendações
- [x] Análise da coluna vertebral
- [x] **NOVO:** Botão Salvar Análise

### 3.5 Comparativo Antes/Depois ✅
- [x] Capturar frame "antes"
- [x] Capturar frame "depois"
- [x] Exibir lado a lado
- [x] Mostrar diferença nos ângulos
- [x] **NOVO:** Formulário de ajustes (selim, recuo, guidão)

### 3.6 Histórico de Sessões ✅
- [x] Lista de sessões por paciente
- [x] Detalhes de cada sessão (ângulos, ajustes, observações)
- [x] Botão Download PDF (aguardando integração backend)
- [x] Continuar sessão em andamento
- [x] **NOVO:** Página HistoricoSessoes.tsx

---

## FASE 4: Integração e Polimento ✅ COMPLETO
**Concluído em: 16/03/2026**

### 4.1 Integração Completa ✅
- [x] Fluxo completo implementado (criar sessão → capturar → salvar → histórico)
- [x] Salvamento de ângulos antes/depois
- [x] Endpoint de finalização de sessão corrigido
- [x] Testado com dados reais via API

### 4.2 Geração de PDF ✅
- [x] Template criado (pdf_generator.py)
- [x] Endpoint GET /sessoes/{id}/pdf implementado
- [x] Dados da sessão (ângulos, ajustes) no PDF
- [x] Download funcionando no frontend
- [x] **NOVO:** Imagens antes/depois no PDF
- [x] **NOVO:** Salvamento de imagens em /uploads/sessoes/

### 4.3 Validação com Especialista
- [ ] Testar com fisioterapeuta (Prof. Andrei Pernambuco)
- [ ] Testar com especialista em bike fit
- [ ] Coletar feedback
- [ ] Ajustar parâmetros

### 4.4 Otimizações ✅
- [x] WebSocket funcionando (~1.76ms latência)
- [x] Loading states nos botões
- [x] Tratamento de erros com mensagens ao usuário
- [x] Build do frontend otimizado (1.14s)

---

## FASE 5: Documentação e TCC
**Status: Não iniciado**

### 5.1 Documentação Técnica
- [ ] README completo
- [ ] Documentação da API
- [ ] Instruções de instalação
- [x] ROADMAP.md atualizado

### 5.2 Documentação Acadêmica
- [ ] Fundamentação Teórica
- [ ] Metodologia
- [ ] Desenvolvimento
- [ ] Resultados
- [ ] Conclusão

### 5.3 Preparação da Apresentação
- [ ] Slides
- [ ] Demo ao vivo
- [ ] Vídeo de backup

---

## Skills do Claude Code Disponíveis

Skills implementadas em `backend/.claude/skills/`:

| Comando | Função |
|---------|--------|
| `/dev` | Inicia ambiente completo (Docker + Backend + Frontend) |
| `/db-migrate` | Gerencia migrações Alembic |
| `/test-api` | Testa endpoints da API |
| `/analyze` | Analisa imagem de ciclista com YOLOv8 |
| `/format` | Formata código Python (black + isort) |
| `/logs` | Mostra logs dos containers Docker |

---

## Referências Científicas Utilizadas

Ver documento completo em: `docs/REFERENCIAS_CIENTIFICAS.md`

### Papers Principais:
1. **Holmes et al. (1994)** - Método original de flexão do joelho (25-35° estático)
2. **Bini & Hume (2020)** - Ranges dinâmicos corrigidos (33-43°)
3. **Bini et al. (2023)** - Diferenças estático vs dinâmico
4. **Martínez & Pérez (2025)** - Correlação flexão >40° com dor/lesão
5. **Nasution et al. (2025)** - Sistema de bike fit com MediaPipe

### Diferenças Estático vs Dinâmico (Bini 2023):
- Joelho: +8° ± 2° no modo dinâmico
- Quadril: +5° ± 1° no modo dinâmico
- Tornozelo: +9° ± 2° no modo dinâmico

---

## Comandos Úteis (Cola Rápida)

```bash
# ===== DOCKER =====
docker-compose up -d          # Subir tudo
docker-compose up -d db       # Só banco
docker-compose down           # Parar tudo
docker-compose logs -f        # Ver logs

# ===== BACKEND =====
cd backend
source venv/bin/activate      # Ativar venv
uvicorn app.main:app --reload # Rodar servidor
alembic upgrade head          # Rodar migrations
alembic revision --autogenerate -m "msg"  # Nova migration

# ===== FRONTEND =====
cd frontend
npm run dev                   # Rodar dev server
npm run build                 # Build produção

# ===== GIT =====
git add .
git commit -m "mensagem"
git pushall
```

---

## Próximos Passos

1. **Testar fluxo completo** - Cadastro → Sessão → Captura → Salvar → Histórico
2. **Validação com Kinovea** - Comparar medições com software de referência
3. **Geração de PDF** - Integrar com backend e testar download
4. **Validação com especialista** - Testar com fisioterapeuta/bike fitter
5. **Otimizações de UX** - Baseado em feedback de uso real

---

## Verificação Final (15/03/2026)

### FASE 1 ✅ Verificada e Completa
| Item | Status |
|------|--------|
| Docker Desktop | ✅ v27.3.1 |
| Node.js 20+ | ✅ v24.10.0 |
| Python 3.11+ | ✅ v3.14.0 |
| PostgreSQL (Docker) | ✅ bikefit_db healthy |
| Backend venv | ✅ Configurado |
| Frontend deps | ✅ Instaladas |
| Servidores rodando | ✅ :8000 e :3000 |

### FASE 2 ✅ Verificada e Completa
| Item | Status |
|------|--------|
| Tabelas no banco | ✅ pacientes, sessoes, medidas |
| Migration Alembic | ✅ c37943173b23 aplicada |
| CRUD Pacientes | ✅ Testado via API |
| CRUD Sessões | ✅ Testado via API |
| PoseDetector (YOLOv8) | ✅ Funcionando |
| AngleCalculator | ✅ Com modo estático/dinâmico |
| RecommendationEngine | ✅ Com alertas de risco |
| WebSocket /ws/video | ✅ Latência 1.76ms |

### FASE 3 ✅ Verificada e Completa
| Item | Status |
|------|--------|
| AuthGuard (proteção de rotas) | ✅ Criado AuthGuard.tsx |
| Login com API | ✅ Token no localStorage |
| Edição de Pacientes | ✅ Modal com todos os campos |
| Busca/Filtro de Pacientes | ✅ Já estava implementado |
| Comparativo Antes/Depois | ✅ Captura e exibe lado a lado |
| Formulário de Ajustes | ✅ Selim, recuo, guidão |
| Histórico de Sessões | ✅ HistoricoSessoes.tsx |
| Botão Salvar Análise | ✅ Com API integration |
| Build sem erros | ✅ `npm run build` OK |

### FASE 4 ✅ Verificada e Completa
| Item | Status |
|------|--------|
| Fluxo completo sessão | ✅ Criar → Capturar → Salvar |
| Salvamento de ângulos | ✅ Antes e depois salvos no DB |
| Endpoint finalizar sessão | ✅ PUT /sessoes/{id}/finalizar |
| Geração de PDF | ✅ GET /sessoes/{id}/pdf |
| Download PDF no frontend | ✅ Botão com loading state |
| Imagens no PDF | ✅ Antes/depois incluídas |
| Salvamento de imagens | ✅ /uploads/sessoes/ |
| Tratamento de erros | ✅ Mensagens ao usuário |
| Validação com especialista | ⏳ Próximo passo |

---

*Última atualização: 16/03/2026*
*Status: Fases 1, 2, 3 e 4 completas. Aguardando validação com especialista para ajustes finais.*
