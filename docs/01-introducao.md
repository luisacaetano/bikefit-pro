# 1. Introdução

## 1.1 Contextualização

O crescimento acelerado da frota de veículos no Brasil, que ultrapassou 115 milhões de unidades em 2024 segundo o DENATRAN, trouxe consigo desafios significativos para a gestão do trânsito, controle de acesso e segurança pública. Nesse contexto, sistemas automatizados de identificação veicular tornam-se cada vez mais necessários.

O reconhecimento automático de placas veiculares, conhecido pela sigla ALPR (Automatic License Plate Recognition) ou LPR (License Plate Recognition), é uma tecnologia que utiliza técnicas de visão computacional e processamento de imagens para identificar automaticamente os caracteres alfanuméricos presentes nas placas de veículos.

Esta tecnologia tem aplicações em diversas áreas:

- **Controle de acesso**: Estacionamentos, condomínios, empresas
- **Fiscalização de trânsito**: Identificação de veículos em rodovias e vias urbanas
- **Segurança pública**: Identificação de veículos roubados ou com restrições
- **Pedágios**: Cobrança automática sem necessidade de parada
- **Smart Cities**: Integração com sistemas inteligentes de gestão urbana

## 1.2 Problema de Pesquisa

Apesar dos avanços tecnológicos, o reconhecimento de placas veiculares brasileiras ainda apresenta desafios específicos:

1. **Padrão de placas**: Coexistência do padrão antigo (cinza) e Mercosul
2. **Condições ambientais**: Variações de iluminação, clima e ângulo de captura
3. **Qualidade das imagens**: Câmeras de baixa resolução, movimento, sujeira nas placas
4. **Caracteres similares**: Confusão entre letras e números (O/0, I/1, B/8)

Diante desse cenário, surge a seguinte questão de pesquisa:

> **Como desenvolver um sistema de reconhecimento automático de placas veiculares brasileiras com alta acurácia, utilizando técnicas modernas de Deep Learning?**

## 1.3 Justificativa

A relevância deste trabalho se justifica pelos seguintes aspectos:

### Relevância Tecnológica
- Aplicação prática de técnicas de visão computacional e Deep Learning
- Contribuição para o estado da arte em reconhecimento de padrões
- Utilização de arquiteturas modernas como YOLO e redes neurais para OCR

### Relevância Social
- Auxílio na segurança pública e controle de trânsito
- Automatização de processos que atualmente dependem de intervenção humana
- Potencial redução de custos operacionais

### Relevância Acadêmica
- Integração de múltiplas áreas do conhecimento
- Possibilidade de contribuição com datasets e modelos para a comunidade
- Tema alinhado com as tendências atuais da Ciência da Computação

## 1.4 Objetivos

### 1.4.1 Objetivo Geral

Desenvolver um sistema de reconhecimento automático de placas veiculares brasileiras utilizando técnicas de visão computacional e aprendizado profundo, capaz de detectar e extrair os caracteres de placas nos padrões brasileiro antigo e Mercosul.

### 1.4.2 Objetivos Específicos

1. Realizar revisão bibliográfica sobre técnicas de detecção de objetos e OCR
2. Coletar e preparar um dataset de imagens de placas veiculares brasileiras
3. Implementar e treinar um modelo de detecção de placas baseado em YOLO
4. Implementar módulo de reconhecimento óptico de caracteres (OCR)
5. Desenvolver interface de usuário para demonstração do sistema
6. Avaliar o desempenho do sistema em termos de acurácia e tempo de processamento
7. Documentar os resultados e limitações encontradas

## 1.5 Metodologia Resumida

Este trabalho segue uma metodologia de pesquisa aplicada com abordagem quantitativa, dividida nas seguintes etapas:

1. **Revisão bibliográfica**: Estudo de trabalhos relacionados e fundamentação teórica
2. **Coleta de dados**: Obtenção de dataset de imagens de placas
3. **Pré-processamento**: Tratamento e anotação das imagens
4. **Desenvolvimento**: Implementação dos módulos de detecção e OCR
5. **Treinamento**: Ajuste dos modelos com o dataset preparado
6. **Avaliação**: Testes e métricas de desempenho
7. **Documentação**: Elaboração do documento final

## 1.6 Estrutura do Trabalho

Este trabalho está organizado da seguinte forma:

- **Capítulo 1 - Introdução**: Apresenta o contexto, problema, objetivos e justificativa
- **Capítulo 2 - Fundamentação Teórica**: Aborda os conceitos de visão computacional, Deep Learning, detecção de objetos e OCR
- **Capítulo 3 - Metodologia**: Descreve os métodos, ferramentas e procedimentos utilizados
- **Capítulo 4 - Desenvolvimento**: Detalha a implementação do sistema
- **Capítulo 5 - Resultados**: Apresenta os experimentos realizados e análise dos resultados
- **Capítulo 6 - Conclusão**: Sintetiza as contribuições e sugere trabalhos futuros
