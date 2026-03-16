---
name: dev
description: Inicia o ambiente de desenvolvimento completo do BikeFit Pro (Docker DB + Backend + Frontend)
disable-model-invocation: true
allowed-tools: Bash(docker-compose *), Bash(uvicorn *), Bash(npm *), Bash(source *)
---

# Skill: Iniciar Ambiente de Desenvolvimento

Quando o usuario invocar `/dev`, execute os seguintes passos:

## Passos

1. **Subir o banco de dados PostgreSQL via Docker:**
   ```bash
   cd /Users/luisacaetano/Desktop/TCC && docker-compose up -d db
   ```

2. **Aguardar o banco estar pronto:**
   ```bash
   sleep 3
   docker exec bikefit_db pg_isready -U bikefit
   ```

3. **Iniciar o backend FastAPI:**
   ```bash
   cd /Users/luisacaetano/Desktop/TCC/backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   > Rode o backend em background ou instrua o usuario a abrir outro terminal.

4. **Iniciar o frontend React (em outro terminal):**
   ```bash
   cd /Users/luisacaetano/Desktop/TCC/frontend && npm run dev
   ```

## URLs de Acesso

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

## Notas

- O banco de dados roda na porta 5432 (usuario: bikefit, senha: bikefit123, db: bikefit_pro)
- Se a porta 5432 estiver ocupada, pare o PostgreSQL local: `brew services stop postgresql@15`
