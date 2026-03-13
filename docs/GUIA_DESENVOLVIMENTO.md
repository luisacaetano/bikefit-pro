# Guia de Desenvolvimento - Ferramentas e Práticas

> Como programadores profissionais organizam projetos

---

## 1. Manter Contexto para a IA (Claude)

### CLAUDE.md (Você já tem!)
O arquivo `CLAUDE.md` na raiz do projeto é lido automaticamente pelo Claude Code.

**O que colocar:**
```markdown
# Contexto do Projeto BikeFit Pro

## Resumo
Sistema de análise postural para ciclistas usando YOLOv8-Pose.

## Stack
- Frontend: React + Vite + TypeScript
- Backend: FastAPI + Python 3.11
- Banco: PostgreSQL
- Pose: YOLOv8-Pose

## Status Atual
- [x] Setup do ambiente
- [x] Estrutura de pastas
- [ ] Backend funcionando
- [ ] Frontend funcionando

## Arquivos Importantes
- `backend/app/core/pose_detector.py` - Detecção de pose
- `backend/app/core/angle_calculator.py` - Cálculo de ângulos
- `frontend/src/pages/SessaoAoVivo.tsx` - Página principal

## Decisões Tomadas
- YOLOv8 escolhido por maior precisão que MediaPipe
- WebSocket para streaming em tempo real
- Docker para PostgreSQL

## Próximo Passo
Implementar conexão com banco de dados
```

### .claude/memory (Memória persistente)
Você já tem isso configurado! O Claude salva informações importantes automaticamente.

---

## 2. Controle de Versão (Git)

### Configuração Inicial
```bash
cd ~/Desktop/TCC
git init
git add .
git commit -m "Initial commit: estrutura do projeto"
```

### .gitignore (Criar este arquivo)
```gitignore
# Python
__pycache__/
*.py[cod]
venv/
.env

# Node
node_modules/
dist/

# IDE
.vscode/
.idea/

# Database
*.db

# OS
.DS_Store

# Logs
*.log

# Data
data/sessoes/
data/exports/
```

### Fluxo de Trabalho
```bash
# Antes de começar a trabalhar
git pull

# Depois de cada funcionalidade
git add .
git commit -m "feat: implementar detecção de pose"
git push

# Padrão de mensagens de commit
feat: nova funcionalidade
fix: correção de bug
docs: documentação
refactor: refatoração
test: testes
```

### Branches (para funcionalidades maiores)
```bash
# Criar branch para nova feature
git checkout -b feature/pose-detection

# Trabalhar na feature...

# Voltar para main e fazer merge
git checkout main
git merge feature/pose-detection
```

---

## 3. Organização de Tarefas

### GitHub Issues
Se subir para GitHub, use Issues para rastrear tarefas:
- `[BUG] Webcam não conecta`
- `[FEATURE] Adicionar gráfico de ângulos`
- `[DOCS] Escrever README`

### GitHub Projects (Kanban)
Colunas: `To Do` → `In Progress` → `Done`

### Arquivo TODO.md (Local)
```markdown
# TODO - BikeFit Pro

## Esta Semana
- [ ] Finalizar conexão PostgreSQL
- [ ] Testar YOLOv8 com webcam
- [ ] Criar tela de login

## Próxima Semana
- [ ] Implementar WebSocket
- [ ] Criar página de sessão ao vivo

## Bugs Conhecidos
- [ ] Erro ao conectar banco em Docker (investigar)

## Ideias Futuras
- [ ] App mobile
- [ ] Integração com Strava
```

---

## 4. Documentação no Código

### Docstrings (Python)
```python
def calcular_angulo_joelho(quadril: tuple, joelho: tuple, tornozelo: tuple) -> float:
    """
    Calcula o ângulo do joelho formado pelos três pontos.

    Args:
        quadril: Coordenadas (x, y) do quadril
        joelho: Coordenadas (x, y) do joelho
        tornozelo: Coordenadas (x, y) do tornozelo

    Returns:
        Ângulo em graus (0-180)

    Example:
        >>> calcular_angulo_joelho((0.5, 0.3), (0.5, 0.5), (0.5, 0.7))
        180.0
    """
```

### Comentários (TypeScript)
```typescript
/**
 * Componente de exibição de ângulos em tempo real
 * @param angles - Objeto com ângulos calculados
 * @param reference - Ângulos de referência para comparação
 */
function AngleDisplay({ angles, reference }: AngleDisplayProps) {
  // ...
}
```

### README em cada pasta
```
backend/
├── README.md  ← Explica como rodar o backend
├── app/
│   └── core/
│       └── README.md  ← Explica os módulos core
```

---

## 5. Testes

### Estrutura de Testes
```
backend/
└── tests/
    ├── __init__.py
    ├── test_pose_detector.py
    ├── test_angle_calculator.py
    └── test_recommendations.py
```

### Exemplo de Teste
```python
# tests/test_angle_calculator.py
import pytest
from app.core.angle_calculator import AngleCalculator

def test_angulo_reto():
    """Testa se ângulo de 90 graus é calculado corretamente"""
    calc = AngleCalculator()
    angulo = calc.calculate_angle(
        p1=(0, 0),
        p2=(0, 1),
        p3=(1, 1)
    )
    assert angulo == pytest.approx(90.0, rel=0.1)

def test_angulo_joelho_extensao():
    """Testa cálculo do ângulo do joelho em extensão"""
    # ...
```

### Rodar Testes
```bash
cd backend
pytest                    # Todos os testes
pytest -v                 # Verbose
pytest tests/test_pose.py # Arquivo específico
pytest --cov=app          # Com cobertura
```

---

## 6. Debugging

### Print Debugging (Simples)
```python
print(f"DEBUG: keypoints = {keypoints}")
print(f"DEBUG: ângulo joelho = {angle}")
```

### Logging (Profissional)
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Keypoints detectados: {keypoints}")
logger.info(f"Ângulo calculado: {angle}")
logger.warning(f"Confiança baixa: {confidence}")
logger.error(f"Erro na detecção: {error}")
```

### Breakpoints (VS Code)
1. Clique na linha para adicionar breakpoint (bolinha vermelha)
2. F5 para iniciar debug
3. Inspecione variáveis no painel lateral

### DevTools do navegador
- F12 para abrir
- Console: ver erros JavaScript
- Network: ver requisições HTTP
- React DevTools: inspecionar componentes

---

## 7. Ambiente de Desenvolvimento

### VS Code Extensions Recomendadas
```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "bradlc.vscode-tailwindcss",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense"
  ]
}
```

### VS Code Settings
```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "python.analysis.typeCheckingMode": "basic"
}
```

### Múltiplos Terminais
Manter abertos:
1. Terminal 1: Backend (`uvicorn`)
2. Terminal 2: Frontend (`npm run dev`)
3. Terminal 3: Git e comandos gerais

---

## 8. Variáveis de Ambiente

### .env (não vai para o Git)
```env
# Database
DATABASE_URL=postgresql://bikefit:bikefit123@localhost:5432/bikefit_pro

# Auth
SECRET_KEY=minha-chave-secreta-mude-em-producao
DEBUG=true

# YOLOv8
YOLO_MODEL=yolov8n-pose.pt
CONFIDENCE_THRESHOLD=0.5
```

### .env.example (vai para o Git)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/database

# Auth
SECRET_KEY=change-me-in-production
DEBUG=false

# YOLOv8
YOLO_MODEL=yolov8n-pose.pt
CONFIDENCE_THRESHOLD=0.5
```

---

## 9. Monitoramento durante Desenvolvimento

### Logs do Docker
```bash
docker-compose logs -f db      # Logs do PostgreSQL
docker-compose logs -f backend # Logs do backend
```

### FastAPI - Auto Reload
```bash
uvicorn app.main:app --reload  # Recarrega ao salvar arquivo
```

### Vite - Hot Module Replacement
```bash
npm run dev  # Atualiza browser automaticamente
```

---

## 10. Checkpoints e Backups

### Tags do Git (Marcos importantes)
```bash
git tag -a v0.1.0 -m "Setup inicial completo"
git tag -a v0.2.0 -m "Backend funcionando"
git tag -a v0.3.0 -m "Frontend funcionando"
git tag -a v1.0.0 -m "Versão final TCC"
```

### Backup manual (antes de mudanças grandes)
```bash
cp -r ~/Desktop/TCC ~/Desktop/TCC_backup_20260313
```

---

## 11. Padrões de Código

### Python (PEP 8 + Black)
```bash
# Formatar código automaticamente
black app/

# Verificar estilo
flake8 app/
```

### TypeScript (ESLint + Prettier)
```bash
# Formatar código
npm run format

# Verificar erros
npm run lint
```

---

## 12. Quando Pedir Ajuda ao Claude

**Bom:**
```
Estou implementando o cálculo de ângulo do joelho.
O keypoint 13 é joelho esquerdo, 11 é quadril, 15 é tornozelo.
Como calculo o ângulo entre esses 3 pontos?
```

**Melhor:**
```
Estou no arquivo backend/app/core/angle_calculator.py

Tenho os keypoints do YOLOv8:
- quadril (11): x=0.45, y=0.35
- joelho (13): x=0.42, y=0.55
- tornozelo (15): x=0.40, y=0.78

Preciso calcular o ângulo do joelho.
O código atual está dando erro: [erro]

Pode me ajudar a corrigir?
```

---

## Resumo: O que Fazer Diariamente

```
INÍCIO DO DIA
├── 1. git pull (pegar atualizações)
├── 2. Ler TODO.md (lembrar onde parou)
├── 3. Atualizar CLAUDE.md se necessário
└── 4. Abrir terminais (backend, frontend, git)

DURANTE O DIA
├── 1. Trabalhar em UMA tarefa por vez
├── 2. Commitar a cada funcionalidade pequena
├── 3. Testar antes de continuar
└── 4. Documentar decisões importantes

FIM DO DIA
├── 1. git add . && git commit -m "WIP: ..."
├── 2. Atualizar TODO.md
├── 3. Anotar no CLAUDE.md o próximo passo
└── 4. git push (backup na nuvem)
```

---

*Última atualização: 13/03/2026*
