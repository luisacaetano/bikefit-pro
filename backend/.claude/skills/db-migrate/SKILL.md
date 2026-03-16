---
name: db-migrate
description: Gerencia migracoes do banco de dados Alembic (create, upgrade, downgrade, history)
argument-hint: [create|up|down|history] [mensagem]
disable-model-invocation: true
allowed-tools: Bash(alembic *), Bash(cd *)
---

# Skill: Gerenciar Migracoes Alembic

Quando o usuario invocar `/db-migrate`, interprete o argumento e execute o comando apropriado.

## Comandos Disponiveis

### `/db-migrate create <mensagem>`
Cria uma nova migracao com autogenerate:
```bash
cd /Users/luisacaetano/Desktop/TCC/backend && source venv/bin/activate && alembic revision --autogenerate -m "$1"
```

### `/db-migrate up` ou `/db-migrate upgrade`
Aplica todas as migracoes pendentes:
```bash
cd /Users/luisacaetano/Desktop/TCC/backend && source venv/bin/activate && alembic upgrade head
```

### `/db-migrate down` ou `/db-migrate downgrade`
Reverte a ultima migracao:
```bash
cd /Users/luisacaetano/Desktop/TCC/backend && source venv/bin/activate && alembic downgrade -1
```

### `/db-migrate history`
Mostra historico de migracoes:
```bash
cd /Users/luisacaetano/Desktop/TCC/backend && source venv/bin/activate && alembic history
```

### `/db-migrate current`
Mostra a migracao atual:
```bash
cd /Users/luisacaetano/Desktop/TCC/backend && source venv/bin/activate && alembic current
```

## Exemplos de Uso

- `/db-migrate create add_user_table` - Cria migracao para nova tabela
- `/db-migrate up` - Aplica migracoes
- `/db-migrate down` - Reverte ultima migracao
- `/db-migrate history` - Ve historico

## Notas

- Certifique-se que o banco PostgreSQL esta rodando antes de aplicar migracoes
- As migracoes ficam em `backend/alembic/versions/`
