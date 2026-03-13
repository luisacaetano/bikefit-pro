# Guia de Documentação de Projetos

Este guia ensina as melhores práticas de documentação utilizadas em projetos de software modernos.

---

## 1. Por Que Documentar?

- **Para você**: Lembrar o que fez daqui a 6 meses
- **Para outros**: Permitir que pessoas entendam e contribuam
- **Para avaliadores**: Facilitar a compreensão do TCC
- **Para o mercado**: Projetos bem documentados impressionam recrutadores

---

## 2. Estrutura Padrão de Projeto

```
projeto/
├── README.md           # Porta de entrada do projeto
├── LICENSE             # Licença de uso
├── requirements.txt    # Dependências (Python)
├── .gitignore         # Arquivos ignorados pelo Git
├── setup.py           # Instalação do pacote (opcional)
│
├── docs/              # Documentação detalhada
│   ├── index.md
│   └── ...
│
├── src/               # Código fonte
│   └── ...
│
├── tests/             # Testes automatizados
│   └── ...
│
├── data/              # Dados (não versionar dados grandes!)
│
└── assets/            # Imagens, ícones, etc.
```

---

## 3. O README.md

O README é o arquivo mais importante. É a primeira coisa que as pessoas leem.

### Estrutura Recomendada:

```markdown
# Nome do Projeto

> Uma frase que resume o projeto

## Badges (opcional)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Sobre
Descrição mais detalhada do projeto.

## Funcionalidades
- Feature 1
- Feature 2

## Instalação
Passos para instalar.

## Como Usar
Exemplos de uso.

## Tecnologias
Lista de tecnologias usadas.

## Estrutura do Projeto
Árvore de diretórios.

## Contribuindo
Como contribuir (para projetos open source).

## Licença
Tipo de licença.

## Autor
Informações de contato.
```

---

## 4. Documentação de Código

### 4.1 Docstrings (Python)

```python
def funcao(parametro1: str, parametro2: int) -> bool:
    """
    Breve descrição da função.

    Descrição mais detalhada se necessário.

    Args:
        parametro1: Descrição do primeiro parâmetro
        parametro2: Descrição do segundo parâmetro

    Returns:
        Descrição do que a função retorna

    Raises:
        ValueError: Quando ocorre tal erro

    Example:
        >>> funcao("teste", 42)
        True
    """
    pass
```

### 4.2 Comentários

```python
# BOM: Explica o "porquê"
# Usamos busca binária porque a lista já está ordenada
resultado = busca_binaria(lista, alvo)

# RUIM: Explica o "o quê" (óbvio pelo código)
# Incrementa i em 1
i += 1
```

### 4.3 Type Hints

```python
from typing import List, Dict, Optional

def processar_dados(
    items: List[str],
    config: Dict[str, int],
    limite: Optional[int] = None
) -> List[Dict]:
    ...
```

---

## 5. Commits Semânticos

Padrão de mensagens de commit que facilita entendimento do histórico:

```
<tipo>: <descrição curta>

[corpo opcional]

[rodapé opcional]
```

### Tipos Comuns:

| Tipo | Uso |
|------|-----|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação (não altera código) |
| `refactor` | Refatoração |
| `test` | Testes |
| `chore` | Tarefas de manutenção |

### Exemplos:

```bash
git commit -m "feat: adiciona detecção de placas Mercosul"
git commit -m "fix: corrige erro de OCR em placas escuras"
git commit -m "docs: atualiza README com instruções de instalação"
```

---

## 6. Versionamento Semântico

Formato: `MAJOR.MINOR.PATCH` (ex: 1.2.3)

- **MAJOR**: Mudanças incompatíveis com versão anterior
- **MINOR**: Nova funcionalidade compatível
- **PATCH**: Correção de bugs compatível

---

## 7. Markdown - Sintaxe Básica

### Títulos
```markdown
# Título 1
## Título 2
### Título 3
```

### Formatação
```markdown
**negrito**
*itálico*
`código inline`
~~riscado~~
```

### Listas
```markdown
- Item 1
- Item 2
  - Subitem

1. Primeiro
2. Segundo
```

### Links e Imagens
```markdown
[Texto do link](https://url.com)
![Alt da imagem](caminho/imagem.png)
```

### Código
````markdown
```python
def hello():
    print("Hello, World!")
```
````

### Tabelas
```markdown
| Coluna 1 | Coluna 2 |
|----------|----------|
| Valor 1  | Valor 2  |
```

### Citações
```markdown
> Isso é uma citação
```

### Tarefas
```markdown
- [x] Tarefa concluída
- [ ] Tarefa pendente
```

---

## 8. Ferramentas de Documentação

### Para Código Python
- **Sphinx**: Gera documentação HTML a partir de docstrings
- **MkDocs**: Documentação em Markdown
- **pdoc**: Simples e automático

### Para APIs
- **Swagger/OpenAPI**: APIs REST
- **Postman**: Coleções de requisições

### Para Diagramas
- **Mermaid**: Diagramas em Markdown
- **Draw.io**: Diagramas visuais
- **PlantUML**: Diagramas de código

---

## 9. Checklist de Documentação

### Projeto
- [ ] README.md completo
- [ ] LICENSE definida
- [ ] .gitignore configurado
- [ ] requirements.txt atualizado
- [ ] Estrutura de pastas organizada

### Código
- [ ] Funções com docstrings
- [ ] Type hints nas funções
- [ ] Comentários onde necessário
- [ ] Nomes de variáveis descritivos

### Repositório
- [ ] Commits semânticos
- [ ] Branches organizados
- [ ] Tags de versão

---

## 10. Dicas Finais

1. **Documente enquanto desenvolve**, não depois
2. **Menos é mais**: Documentação concisa é melhor que extensa
3. **Mantenha atualizado**: Documentação desatualizada é pior que nenhuma
4. **Use exemplos**: Código de exemplo vale mais que explicações
5. **Pense no leitor**: Escreva para quem não conhece o projeto

---

## Recursos para Aprender Mais

- [Documentação do GitHub sobre READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [Guia de Markdown](https://www.markdownguide.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
