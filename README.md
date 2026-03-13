# BikeFit AI - Sistema de Análise Postural para Ciclistas

> Trabalho de Conclusão de Curso em Ciência da Computação

## Sobre o Projeto

Sistema de análise postural automatizada para ciclistas utilizando técnicas de Visão Computacional e Estimativa de Pose (Pose Estimation). O sistema captura vídeos do ciclista pedalando, identifica pontos anatômicos do corpo, calcula ângulos articulares e fornece recomendações de ajuste da bicicleta baseadas nas medidas, flexibilidade e objetivos de cada ciclista.

### Problema

O Bike Fit profissional é um serviço caro (R$300-800) que requer especialistas certificados. Muitos ciclistas não têm acesso a esse tipo de avaliação, resultando em desconforto, lesões e perda de performance. Este projeto propõe uma solução acessível que utiliza apenas uma câmera comum para realizar análises posturais.

### Objetivos

- **Geral**: Desenvolver um sistema de análise postural automatizada para ciclistas utilizando técnicas de visão computacional e estimativa de pose.

- **Específicos**:
  - Implementar detecção de pontos anatômicos usando MediaPipe Pose
  - Calcular ângulos articulares relevantes (joelho, quadril, tornozelo, cotovelo)
  - Comparar medidas com parâmetros ideais de bike fit
  - Gerar relatório com recomendações de ajuste
  - Desenvolver interface para visualização em tempo real

## Estrutura do Projeto

```
TCC/
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências do projeto
├── .gitignore               # Arquivos ignorados pelo Git
│
├── docs/                    # Documentação
│   ├── 01-introducao.md
│   ├── 02-fundamentacao-teorica.md
│   ├── 03-metodologia.md
│   ├── 04-desenvolvimento.md
│   ├── 05-resultados.md
│   ├── 06-conclusao.md
│   ├── referencias.md
│   └── cronograma.md
│
├── src/                     # Código fonte
│   ├── pose/                # Módulo de estimativa de pose
│   ├── analysis/            # Módulo de análise de ângulos
│   ├── recommendations/     # Módulo de recomendações
│   ├── utils/               # Funções utilitárias
│   └── main.py              # Ponto de entrada da aplicação
│
├── data/                    # Datasets
│   ├── videos/              # Vídeos de ciclistas
│   ├── processed/           # Dados processados
│   └── reference/           # Parâmetros de referência
│
├── models/                  # Modelos e configurações
│   └── angles_reference.json # Ângulos ideais por tipo de ciclismo
│
├── tests/                   # Testes automatizados
│
└── assets/                  # Imagens e recursos para documentação
```

## Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| Python | 3.9+ | Linguagem principal |
| OpenCV | 4.x | Processamento de vídeo |
| MediaPipe | 0.10+ | Estimativa de pose (33 pontos) |
| NumPy | 1.x | Cálculos matemáticos |
| Pandas | 2.x | Análise de dados |
| Streamlit | 1.x | Interface web |
| Matplotlib | 3.x | Visualização de gráficos |

## Ângulos Analisados

| Articulação | Ângulo Ideal (Road) | Ângulo Ideal (MTB) | Importância |
|-------------|---------------------|---------------------|-------------|
| Joelho (extensão máxima) | 140-150° | 135-145° | Previne lesões no joelho |
| Joelho (flexão máxima) | 65-75° | 70-80° | Eficiência de pedalada |
| Quadril | 40-50° | 45-55° | Conforto lombar |
| Tornozelo | 90-110° | 90-110° | Estabilidade do pedal |
| Cotovelo | 150-170° | 140-160° | Absorção de impacto |
| Tronco | 40-50° | 50-60° | Aerodinâmica vs conforto |

## Instalação

### Pré-requisitos

- Python 3.9 ou superior
- Webcam ou vídeos gravados
- pip (gerenciador de pacotes)

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/tcc-bikefit.git
cd tcc-bikefit
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

### Analisar vídeo gravado
```bash
python src/main.py --video caminho/para/video.mp4
```

### Análise em tempo real (webcam)
```bash
python src/main.py --webcam
```

### Gerar relatório PDF
```bash
python src/main.py --video video.mp4 --report relatorio.pdf
```

## Pipeline do Sistema

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   Entrada   │────▶│  Estimativa  │────▶│   Cálculo   │────▶│  Relatório   │
│  (Vídeo/    │     │   de Pose    │     │  de Ângulos │     │     com      │
│   Webcam)   │     │ (MediaPipe)  │     │  (NumPy)    │     │ Recomendações│
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
```

## Resultados Esperados

| Métrica | Meta |
|---------|------|
| Precisão na detecção de pose | > 85% |
| Erro nos ângulos calculados | < 5° |
| Tempo de processamento | < 100ms por frame |
| Concordância com especialista | > 80% |

## Validação

O sistema será validado comparando os resultados com avaliações realizadas por especialista em Bike Fit certificado, utilizando dados reais de sessões de ajuste.

## Documentação

A documentação completa do TCC está disponível na pasta `docs/`:

- [Introdução](docs/01-introducao.md)
- [Fundamentação Teórica](docs/02-fundamentacao-teorica.md)
- [Metodologia](docs/03-metodologia.md)
- [Desenvolvimento](docs/04-desenvolvimento.md)
- [Resultados](docs/05-resultados.md)
- [Conclusão](docs/06-conclusao.md)
- [Referências](docs/referencias.md)
- [Cronograma](docs/cronograma.md)

## Potencial Comercial

Este projeto tem potencial para se tornar uma ferramenta de apoio para especialistas em Bike Fit, oferecendo:
- Pré-análise automatizada antes da sessão presencial
- Acompanhamento remoto de ciclistas
- Democratização do acesso à análise postural

## Autor

**Luisa Caetano**
- Curso: Ciência da Computação
- Instituição: Unifor
- Orientador: [Nome do Orientador]
- Ano: 2026

## Colaboradores

- Professor de Fisioterapia (Unifor) - Consultoria técnica
- Especialista em Bike Fit - Fornecimento de dados e validação

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
