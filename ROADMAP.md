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
│  [██████]        [░░░░░░]        [░░░░░░]        [░░░░░░]        [░░░░]│
│  ATUAL           PRÓXIMA                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## FASE 1: Setup do Ambiente (ATUAL)
**Tempo estimado: 1-2 dias**

### 1.1 Pré-requisitos
- [ ] Instalar Docker Desktop: https://www.docker.com/products/docker-desktop
- [ ] Instalar Node.js 20+: https://nodejs.org/
- [ ] Instalar Python 3.11+: já vem no Mac M3
- [ ] Instalar app Camo no celular (iOS/Android)

### 1.2 Clonar/Configurar projeto
```bash
# Já feito - estrutura criada em ~/Desktop/TCC/
cd ~/Desktop/TCC
```

### 1.3 Subir banco de dados
```bash
# Iniciar PostgreSQL com Docker
docker-compose up -d db

# Verificar se está rodando
docker ps

# Testar conexão
docker exec -it bikefit_db psql -U bikefit -d bikefit_pro -c "SELECT 1;"
```

### 1.4 Configurar Backend
```bash
cd backend

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
```

### 1.5 Configurar Frontend
```bash
cd frontend

# Instalar dependências
npm install
```

### 1.6 Testar setup
```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Acessar:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

**Checkpoint FASE 1:** ✅ Docker rodando, backend responde em /docs, frontend abre

---

## FASE 2: Backend Core
**Tempo estimado: 1 semana**

### 2.1 Banco de Dados
- [ ] Criar models SQLAlchemy (Paciente, Sessao, Medidas)
- [ ] Configurar Alembic para migrations
- [ ] Rodar primeira migration
- [ ] Testar CRUD básico

### 2.2 YOLOv8 Pose Detection
- [ ] Testar YOLOv8-pose com imagem estática
- [ ] Implementar classe PoseDetector
- [ ] Testar com webcam/Camo
- [ ] Validar detecção dos 17 keypoints

### 2.3 Cálculo de Ângulos
- [ ] Implementar AngleCalculator
- [ ] Calcular ângulo do joelho (extensão)
- [ ] Calcular ângulo do joelho (flexão)
- [ ] Calcular ângulo do quadril
- [ ] Calcular ângulo do tornozelo
- [ ] Calcular ângulo do tronco
- [ ] Testar com valores conhecidos

### 2.4 Sistema de Recomendações
- [ ] Implementar RecommendationEngine
- [ ] Definir regras para cada ângulo
- [ ] Categorizar: ajuste necessário / opcional / ok
- [ ] Gerar texto das recomendações

### 2.5 API REST Completa
- [ ] Finalizar CRUD de Pacientes
- [ ] Finalizar CRUD de Sessões
- [ ] Endpoint de análise de frame
- [ ] Testar todos endpoints no Swagger

### 2.6 WebSocket para Streaming
- [ ] Implementar endpoint WebSocket
- [ ] Receber frames do frontend
- [ ] Processar e retornar ângulos em tempo real
- [ ] Testar latência (<100ms ideal)

**Checkpoint FASE 2:** ✅ API funcionando, detecta pose, calcula ângulos, WebSocket ok

---

## FASE 3: Frontend React
**Tempo estimado: 1 semana**

### 3.1 Setup e Estrutura
- [ ] Configurar TailwindCSS
- [ ] Configurar Shadcn/ui
- [ ] Configurar React Router
- [ ] Configurar React Query
- [ ] Criar layout base (navbar, sidebar)

### 3.2 Página de Login
- [ ] Tela de login
- [ ] Integrar com API de auth
- [ ] Guardar token no localStorage
- [ ] Redirect após login

### 3.3 Página de Pacientes
- [ ] Lista de pacientes
- [ ] Formulário de cadastro
- [ ] Edição de paciente
- [ ] Busca/filtro
- [ ] Integrar com API

### 3.4 Página de Nova Sessão (CORE)
- [ ] Selecionar paciente
- [ ] Capturar vídeo da webcam
- [ ] Enviar frames via WebSocket
- [ ] Exibir skeleton sobre o vídeo
- [ ] Mostrar ângulos em tempo real
- [ ] Mostrar alertas (verde/amarelo/vermelho)
- [ ] Mostrar recomendações

### 3.5 Comparativo Antes/Depois
- [ ] Capturar frame "antes"
- [ ] Capturar frame "depois"
- [ ] Exibir lado a lado
- [ ] Mostrar diferença nos ângulos

### 3.6 Histórico de Sessões
- [ ] Lista de sessões por paciente
- [ ] Detalhes de cada sessão
- [ ] Download de PDF

**Checkpoint FASE 3:** ✅ Interface completa, captura webcam, mostra ângulos

---

## FASE 4: Integração e Polimento
**Tempo estimado: 1 semana**

### 4.1 Integração Completa
- [ ] Testar fluxo completo: login → paciente → sessão → relatório
- [ ] Corrigir bugs de integração
- [ ] Testar com dados reais

### 4.2 Geração de PDF
- [ ] Template do relatório
- [ ] Inserir dados da sessão
- [ ] Inserir imagens antes/depois
- [ ] Inserir gráficos
- [ ] Testar download

### 4.3 Validação com Especialista
- [ ] Testar com o professor de fisioterapia da Unifor
- [ ] Testar com o especialista em bike fit (namorado)
- [ ] Coletar feedback
- [ ] Ajustar parâmetros de ângulos se necessário

### 4.4 Otimizações
- [ ] Melhorar performance do WebSocket
- [ ] Otimizar detecção de pose
- [ ] Melhorar UX baseado no feedback
- [ ] Tratar erros e edge cases

**Checkpoint FASE 4:** ✅ Sistema completo funcionando, validado por especialistas

---

## FASE 5: Documentação e TCC
**Tempo estimado: 2 semanas**

### 5.1 Documentação Técnica
- [ ] README completo
- [ ] Documentação da API
- [ ] Instruções de instalação
- [ ] Arquitetura do sistema

### 5.2 Documentação Acadêmica
- [ ] Atualizar Introdução (01-introducao.md)
- [ ] Escrever Fundamentação Teórica (02-fundamentacao-teorica.md)
- [ ] Documentar Metodologia (03-metodologia.md)
- [ ] Documentar Desenvolvimento (04-desenvolvimento.md)
- [ ] Documentar Resultados (05-resultados.md)
- [ ] Escrever Conclusão (06-conclusao.md)
- [ ] Atualizar Referências

### 5.3 Preparação da Apresentação
- [ ] Criar slides
- [ ] Preparar demo ao vivo
- [ ] Ensaiar apresentação
- [ ] Preparar vídeo de backup (caso webcam falhe)

### 5.4 Entrega
- [ ] Revisão final do código
- [ ] Revisão final da documentação
- [ ] Preparar repositório GitHub
- [ ] Entregar TCC

**Checkpoint FASE 5:** ✅ TCC entregue e apresentado!

---

## Ordem de Implementação Detalhada

### Semana 1: Setup + Backend Básico
```
Dia 1: Docker + PostgreSQL + Estrutura
Dia 2: Models + Migrations + CRUD Pacientes
Dia 3: YOLOv8 funcionando isolado
Dia 4: AngleCalculator implementado
Dia 5: API REST completa
```

### Semana 2: Backend Avançado + Frontend Início
```
Dia 1: WebSocket streaming funcionando
Dia 2: Testar latência e otimizar
Dia 3: Setup React + TailwindCSS + Shadcn
Dia 4: Páginas de Login e Layout
Dia 5: Página de Pacientes
```

### Semana 3: Frontend Core
```
Dia 1: Captura de webcam no React
Dia 2: Conexão WebSocket frontend → backend
Dia 3: Exibir skeleton e ângulos
Dia 4: Alertas e recomendações em tempo real
Dia 5: Comparativo antes/depois
```

### Semana 4: Integração + PDF
```
Dia 1: Testar fluxo completo
Dia 2: Geração de PDF
Dia 3: Histórico de sessões
Dia 4: Validação com especialista
Dia 5: Correções e ajustes
```

### Semanas 5-6: Documentação + TCC
```
Escrita do TCC
Preparação da apresentação
```

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

# ===== TESTES =====
cd backend && pytest          # Testes backend
cd frontend && npm test       # Testes frontend

# ===== GIT =====
git add .
git commit -m "mensagem"
git push
```

---

## Arquivos para Criar (Próximos)

Por ordem de prioridade:

1. `backend/app/db/database.py` - Conexão PostgreSQL
2. `backend/app/db/models.py` - Models SQLAlchemy
3. `backend/app/schemas/paciente.py` - Schemas Pydantic
4. `backend/app/core/pose_detector.py` - YOLOv8 wrapper
5. `backend/app/core/angle_calculator.py` - Cálculo de ângulos
6. `frontend/package.json` - Dependências React
7. `frontend/src/App.tsx` - Componente principal

---

## Dúvidas Frequentes

**P: Por onde começar?**
R: Fase 1 (Setup) → Subir Docker → Testar backend básico

**P: E se o YOLOv8 não detectar bem?**
R: Ajustar iluminação, posição da câmera, ou usar modelo maior (yolov8s-pose)

**P: Quanto tempo leva cada fase?**
R: Setup: 1-2 dias, Backend: 1 semana, Frontend: 1 semana, Integração: 1 semana

**P: Preciso fazer tudo sozinha?**
R: Não! O Claude pode ajudar a gerar código, debugar, e tirar dúvidas.

---

*Última atualização: 13/03/2026*
*Próximo passo: Completar setup do ambiente (Fase 1)*
