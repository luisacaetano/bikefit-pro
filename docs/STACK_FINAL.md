# Stack Final - BikeFit Pro

> Documentação completa das tecnologias e decisões do projeto

---

## Resumo Executivo

| Camada | Tecnologia | Versão |
|--------|------------|--------|
| **Frontend** | React + Vite + TypeScript | React 18+ |
| **Estilização** | TailwindCSS + Shadcn/ui | 3.4+ |
| **Backend** | FastAPI | 0.109+ |
| **Pose Estimation** | YOLOv8-Pose (Ultralytics) | 8.1+ |
| **Banco de Dados** | PostgreSQL | 15+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Relatórios** | ReportLab | 4.0+ |
| **Containerização** | Docker + Docker Compose | 24+ |
| **Linguagens** | Python 3.11+ / TypeScript 5+ | |

---

## Decisões Tecnológicas (Registro)

### 1. Frontend: React + Vite + TypeScript

**Decisão:** Usar React com Vite e TypeScript em vez de Streamlit

**Alternativas consideradas:**
| Opção | Prós | Contras | Status |
|-------|------|---------|--------|
| Streamlit | Rápido, Python puro | Pouco customizável, não escala | ❌ Descartado |
| Next.js | SSR, robusto | Overhead desnecessário | ❌ Descartado |
| **React + Vite** | Rápido, flexível, TypeScript | Mais código | ✅ **Escolhido** |

**Justificativa:**
- Usuária tem experiência com React
- Maior controle sobre a interface
- Escalável para produto comercial
- TypeScript previne erros em tempo de desenvolvimento
- Vite é mais rápido que Create React App

**Bibliotecas adicionais:**
- **TailwindCSS** - Estilização utility-first
- **Shadcn/ui** - Componentes acessíveis e bonitos
- **React Query** - Cache e fetching de dados
- **Zustand** - State management leve
- **React Router** - Navegação SPA

---

### 2. Backend: FastAPI

**Decisão:** Usar FastAPI como framework backend

**Alternativas consideradas:**
| Opção | Prós | Contras | Status |
|-------|------|---------|--------|
| Flask | Simples, conhecido | Lento, sem async nativo | ❌ Descartado |
| Django | Completo, ORM incluso | Pesado, overkill | ❌ Descartado |
| **FastAPI** | Async, rápido, docs auto | Mais recente | ✅ **Escolhido** |

**Justificativa:**
- Suporte nativo a WebSocket (essencial para vídeo em tempo real)
- Async/await para performance
- Documentação automática (Swagger/OpenAPI)
- Validação com Pydantic
- Tipagem forte com Python type hints

---

### 3. Pose Estimation: YOLOv8-Pose

**Decisão:** Usar YOLOv8-Pose em vez de MediaPipe

**Alternativas consideradas:**
| Opção | Keypoints | Precisão | Velocidade | Status |
|-------|-----------|----------|------------|--------|
| MediaPipe | 33 | Boa | 30+ FPS | ❌ Descartado |
| OpenPose | 25 | Excelente | 10-15 FPS | ❌ Descartado |
| **YOLOv8-Pose** | 17 | Muito boa | 25-30 FPS | ✅ **Escolhido** |

**Justificativa:**
- 17 keypoints são suficientes para bike fit
- Melhor precisão que MediaPipe
- Suporte a GPU (futuro)
- Modelo customizável (pode treinar com dados específicos de bike fit)
- Framework Ultralytics bem mantido e documentado

**Keypoints disponíveis (COCO format):**
```
ID  Nome              Uso no BikeFit
──────────────────────────────────────
0   nose              -
1   left_eye          -
2   right_eye         -
3   left_ear          -
4   right_ear         -
5   left_shoulder     ✅ Ângulo tronco/ombro
6   right_shoulder    ✅ Ângulo tronco/ombro
7   left_elbow        ✅ Ângulo cotovelo
8   right_elbow       ✅ Ângulo cotovelo
9   left_wrist        ✅ Posição mãos
10  right_wrist       ✅ Posição mãos
11  left_hip          ✅ Ângulo quadril
12  right_hip         ✅ Ângulo quadril
13  left_knee         ✅ Ângulo joelho
14  right_knee        ✅ Ângulo joelho
15  left_ankle        ✅ Ângulo tornozelo
16  right_ankle       ✅ Ângulo tornozelo
```

---

### 4. Banco de Dados: PostgreSQL

**Decisão:** Usar PostgreSQL com Docker local

**Alternativas consideradas:**
| Opção | Tipo | Prós | Contras | Status |
|-------|------|------|---------|--------|
| SQLite | Local/arquivo | Zero config | Não escala | ❌ Descartado |
| MySQL | Server | Popular | Menos features | ❌ Descartado |
| **PostgreSQL** | Server | Robusto, escalável | Precisa server | ✅ **Escolhido** |

**Ambiente:**
| Ambiente | Solução |
|----------|---------|
| Desenvolvimento | Docker local (docker-compose) |
| Produção | Supabase ou Railway |

**Justificativa:**
- Mais robusto e feature-rich que SQLite
- Suporte a JSON, arrays, full-text search
- Escalável para produção
- Docker simplifica setup local
- Pode migrar facilmente para Supabase (PostgreSQL na nuvem)

**ORM:** SQLAlchemy 2.0
- Async support
- Type hints
- Migrations com Alembic

---

### 5. Geração de Relatórios: ReportLab

**Decisão:** Usar ReportLab para PDFs

**Alternativas consideradas:**
| Opção | Prós | Contras | Status |
|-------|------|---------|--------|
| FPDF2 | Simples, leve | Menos recursos | ❌ Descartado |
| WeasyPrint | HTML → PDF | Dependências pesadas | ❌ Descartado |
| **ReportLab** | Poderoso, profissional | Curva de aprendizado | ✅ **Escolhido** |

**Justificativa:**
- Controle total sobre o layout
- Suporte a gráficos e imagens
- Amplamente usado em produção
- Boa documentação

---

### 6. Comunicação em Tempo Real: WebSocket

**Decisão:** WebSocket nativo do FastAPI para streaming de vídeo

**Fluxo:**
```
Câmera → Backend (processa) → WebSocket → Frontend (exibe)
```

**Justificativa:**
- Baixa latência (~50ms)
- Bidirecional (pode enviar comandos de volta)
- Suportado nativamente pelo FastAPI
- Mais eficiente que polling HTTP

---

### 7. Containerização: Docker

**Decisão:** Usar Docker e Docker Compose para desenvolvimento

**Justificativa:**
- Ambiente consistente
- PostgreSQL sem instalação local
- Fácil onboarding de novos desenvolvedores
- Preparado para deploy

---

### 8. Hardware: Webcam USB / Camo

**Decisão:** Câmera externa via USB (webcam ou celular com Camo)

**Alternativas consideradas:**
| Opção | Prós | Contras | Status |
|-------|------|---------|--------|
| Câmera iPad | Portátil | Difícil posicionar | ❌ Descartado |
| MacBook cam | Já tem | Posição fixa, qualidade média | ❌ Descartado |
| **Webcam USB** | Posição flexível, dedicada | Custo extra | ✅ **Escolhido** |
| Celular + Camo | Ótima câmera, zero custo | Precisa app | ✅ **Alternativa** |

**Setup recomendado:**
- **Desenvolvimento:** Celular + Camo app (gratuito)
- **Produção:** Logitech C920 ou similar (~R$250)

---

## Stack Final Consolidada

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BIKEFIT PRO - STACK FINAL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                            FRONTEND                                   │  │
│  │                                                                       │  │
│  │   React 18          Vite 5           TypeScript 5                     │  │
│  │   TailwindCSS 3     Shadcn/ui        React Query                      │  │
│  │   Zustand           React Router     Axios                            │  │
│  │                                                                       │  │
│  │   Porta: 3000                                                         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                     │                                       │
│                              REST + WebSocket                               │
│                                     │                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                            BACKEND                                    │  │
│  │                                                                       │  │
│  │   FastAPI 0.109     Uvicorn          Python 3.11                      │  │
│  │   SQLAlchemy 2.0    Alembic          Pydantic v2                      │  │
│  │   Python-Jose       ReportLab        Pillow                           │  │
│  │                                                                       │  │
│  │   Porta: 8000                                                         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                     │                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        POSE ESTIMATION                                │  │
│  │                                                                       │  │
│  │   Ultralytics 8.1   YOLOv8n-pose     OpenCV 4.8                       │  │
│  │   NumPy 1.24        (17 keypoints)                                    │  │
│  │                                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                     │                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                          DATABASE                                     │  │
│  │                                                                       │  │
│  │   PostgreSQL 15     Docker           Porta: 5432                      │  │
│  │                                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         INFRAESTRUTURA                                │  │
│  │                                                                       │  │
│  │   Docker 24         Docker Compose   MacBook M3                       │  │
│  │                                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Versões Específicas

### Backend (requirements.txt)
```
# Core
fastapi==0.109.2
uvicorn[standard]==0.27.1
python-multipart==0.0.9

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1

# Validation
pydantic==2.6.1
pydantic-settings==2.1.0

# Auth
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Pose Estimation
ultralytics==8.1.0
opencv-python==4.9.0.80
numpy==1.26.4

# PDF
reportlab==4.1.0
Pillow==10.2.0

# Utils
python-dotenv==1.0.1
```

### Frontend (package.json dependencies)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0",
    "@tanstack/react-query": "^5.18.0",
    "zustand": "^4.5.0",
    "axios": "^1.6.7",
    "tailwindcss": "^3.4.1",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "lucide-react": "^0.323.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.55",
    "@types/react-dom": "^18.2.19",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.1.0",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.35"
  }
}
```

---

## Portas e URLs

| Serviço | URL | Porta |
|---------|-----|-------|
| Frontend (React) | http://localhost:3000 | 3000 |
| Backend (FastAPI) | http://localhost:8000 | 8000 |
| API Docs (Swagger) | http://localhost:8000/docs | 8000 |
| PostgreSQL | localhost:5432 | 5432 |
| WebSocket | ws://localhost:8000/ws/video | 8000 |

---

## Comandos de Desenvolvimento

```bash
# Iniciar tudo com Docker
docker-compose up -d

# Apenas banco de dados
docker-compose up -d db

# Backend (desenvolvimento local)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (desenvolvimento local)
cd frontend
npm install
npm run dev

# Migrations do banco
cd backend
alembic upgrade head

# Criar nova migration
alembic revision --autogenerate -m "descricao"
```

---

## Histórico de Decisões

| Data | Decisão | Motivo |
|------|---------|--------|
| 13/03/2026 | React em vez de Streamlit | Usuária tem experiência, mais escalável |
| 13/03/2026 | YOLOv8 em vez de MediaPipe | Maior precisão, customizável |
| 13/03/2026 | PostgreSQL em vez de SQLite | Escalabilidade, features avançadas |
| 13/03/2026 | Docker local para PostgreSQL | Ambiente consistente |
| 13/03/2026 | ReportLab para PDFs | Controle total, profissional |
| 13/03/2026 | Webcam USB / Camo | Posicionamento flexível, qualidade |
| 13/03/2026 | Público-alvo: Fisioterapeutas | Diferencial de mercado (B2B) |

---

*Última atualização: 13/03/2026*
