---
name: test-api
description: Testa endpoints da API REST do BikeFit Pro usando curl
argument-hint: [endpoint] [GET|POST|PUT|DELETE]
allowed-tools: Bash(curl *)
---

# Skill: Testar Endpoints da API

Quando o usuario invocar `/test-api`, execute requests HTTP para testar a API.

## Uso

```
/test-api <endpoint> [metodo]
```

- `endpoint`: Caminho do endpoint (ex: /health, /api/pacientes/)
- `metodo`: GET, POST, PUT, DELETE (default: GET)

## Endpoints Disponiveis

### Health Check
```bash
curl -s http://localhost:8000/health | jq
```

### Pacientes
```bash
# Listar todos
curl -s http://localhost:8000/api/pacientes/ | jq

# Criar novo
curl -s -X POST http://localhost:8000/api/pacientes/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Teste", "email": "teste@email.com"}' | jq

# Buscar por ID
curl -s http://localhost:8000/api/pacientes/1 | jq
```

### Sessoes
```bash
# Listar sessoes de um paciente
curl -s http://localhost:8000/api/sessoes/?paciente_id=1 | jq
```

### Analise
```bash
# Referencias de angulos
curl -s http://localhost:8000/api/analise/referencias | jq
```

### Autenticacao
```bash
# Login
curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@email.com", "senha": "123456"}' | jq
```

## Exemplos

- `/test-api /health` - Testa health check
- `/test-api /api/pacientes/ GET` - Lista pacientes
- `/test-api /api/pacientes/ POST` - Cria paciente (pede dados)

## Notas

- O backend deve estar rodando em http://localhost:8000
- Use `jq` para formatar JSON (ja incluido nos comandos)
- Swagger UI disponivel em http://localhost:8000/docs
