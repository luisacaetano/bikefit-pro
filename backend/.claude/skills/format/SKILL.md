---
name: format
description: Formata codigo Python do backend com black e isort
disable-model-invocation: true
allowed-tools: Bash(black *), Bash(isort *), Bash(cd *), Bash(source *)
---

# Skill: Formatar Codigo Python

Quando o usuario invocar `/format`, execute as ferramentas de formatacao no backend.

## Comandos

### Formatar com Black
```bash
cd /Users/luisacaetano/Desktop/TCC/backend && source venv/bin/activate && black app/
```

### Organizar imports com isort
```bash
cd /Users/luisacaetano/Desktop/TCC/backend && source venv/bin/activate && isort app/
```

## Execucao Completa

Execute ambos os comandos em sequencia:

```bash
cd /Users/luisacaetano/Desktop/TCC/backend && \
source venv/bin/activate && \
echo "=== Formatando com Black ===" && \
black app/ && \
echo "" && \
echo "=== Organizando imports com isort ===" && \
isort app/ && \
echo "" && \
echo "Formatacao concluida!"
```

## Opcoes Adicionais

### Verificar sem modificar (dry-run)
```bash
black --check app/
isort --check-only app/
```

### Mostrar diferencas
```bash
black --diff app/
isort --diff app/
```

## Configuracao

O projeto usa as configuracoes padrao do Black e isort. Para customizar, crie um `pyproject.toml`:

```toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100
```

## Notas

- Black: Formatador de codigo opinativo (PEP 8)
- isort: Organiza imports em ordem alfabetica e por tipo
- Ambas as ferramentas ja estao no requirements.txt
