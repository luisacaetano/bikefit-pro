# 2. Fundamentação Teórica

Este capítulo apresenta os conceitos fundamentais necessários para a compreensão do trabalho, abordando visão computacional, redes neurais convolucionais, detecção de objetos e reconhecimento óptico de caracteres.

## 2.1 Visão Computacional

### 2.1.1 Definição

Visão Computacional é um campo da Inteligência Artificial que permite aos computadores interpretar e entender o mundo visual. Envolve a aquisição, processamento, análise e compreensão de imagens do mundo real para produzir informações numéricas ou simbólicas (SZELISKI, 2022).

### 2.1.2 Processamento Digital de Imagens

O processamento de imagens envolve técnicas para manipulação e análise de imagens digitais:

- **Aquisição**: Captura da imagem por meio de câmeras ou sensores
- **Pré-processamento**: Redução de ruído, ajuste de contraste, normalização
- **Segmentação**: Divisão da imagem em regiões de interesse
- **Extração de características**: Identificação de padrões relevantes
- **Reconhecimento**: Classificação ou identificação dos objetos

### 2.1.3 Representação de Imagens

Uma imagem digital é representada como uma matriz bidimensional de pixels:

```
Imagem RGB: I(x, y) = [R, G, B]
Imagem Grayscale: I(x, y) = intensidade (0-255)
```

## 2.2 Redes Neurais Artificiais

### 2.2.1 Conceitos Básicos

Redes Neurais Artificiais (RNA) são modelos computacionais inspirados no funcionamento do cérebro humano. São compostas por unidades de processamento (neurônios) organizadas em camadas (GOODFELLOW; BENGIO; COURVILLE, 2016).

**Componentes principais:**
- **Neurônio artificial**: Unidade básica que recebe entradas, aplica pesos e uma função de ativação
- **Camadas**: Entrada, ocultas e saída
- **Pesos e vieses**: Parâmetros ajustáveis durante o treinamento
- **Função de ativação**: ReLU, Sigmoid, Softmax, etc.

### 2.2.2 Redes Neurais Convolucionais (CNN)

As CNNs são um tipo especializado de rede neural projetado para processar dados com topologia de grade, como imagens (LECUN; BENGIO; HINTON, 2015).

**Componentes das CNNs:**

| Camada | Função |
|--------|--------|
| Convolução | Extrai características locais através de filtros |
| Pooling | Reduz dimensionalidade, mantendo características importantes |
| Fully Connected | Classificação final baseada nas características extraídas |
| Dropout | Regularização para evitar overfitting |
| Batch Normalization | Normaliza ativações para acelerar treinamento |

### 2.2.3 Transfer Learning

Transfer Learning é uma técnica que permite utilizar conhecimento adquirido em uma tarefa para melhorar o aprendizado em outra tarefa relacionada. Em visão computacional, é comum utilizar modelos pré-treinados em grandes datasets como ImageNet (YOSINSKI et al., 2014).

**Vantagens:**
- Reduz necessidade de grandes volumes de dados
- Acelera o treinamento
- Melhora performance em datasets pequenos

## 2.3 Detecção de Objetos

### 2.3.1 Definição

Detecção de objetos é a tarefa de identificar e localizar objetos em imagens ou vídeos. Diferente da classificação, a detecção também fornece a posição do objeto através de bounding boxes.

### 2.3.2 Métricas de Avaliação

| Métrica | Descrição | Fórmula |
|---------|-----------|---------|
| IoU (Intersection over Union) | Sobreposição entre predição e ground truth | IoU = Área de Interseção / Área de União |
| Precision | Proporção de detecções corretas | TP / (TP + FP) |
| Recall | Proporção de objetos detectados | TP / (TP + FN) |
| mAP (mean Average Precision) | Média da precisão em diferentes thresholds | Média de AP por classe |

### 2.3.3 Arquitetura YOLO

YOLO (You Only Look Once) é uma família de modelos de detecção de objetos em tempo real proposta por Redmon et al. (2016). Diferente de abordagens anteriores que usavam regiões propostas, YOLO trata a detecção como um problema de regressão único.

**Características do YOLO:**
- Processa a imagem inteira em uma única passada
- Extremamente rápido (tempo real)
- Detecta objetos de diferentes escalas
- Prediz bounding boxes e probabilidades de classe simultaneamente

**Evolução do YOLO:**

| Versão | Ano | Principais Melhorias |
|--------|-----|---------------------|
| YOLOv1 | 2016 | Conceito original |
| YOLOv3 | 2018 | Multi-scale detection |
| YOLOv5 | 2020 | PyTorch, facilidade de uso |
| YOLOv8 | 2023 | Estado da arte, anchor-free |

### 2.3.4 YOLOv8

YOLOv8 é a versão mais recente desenvolvida pela Ultralytics, oferecendo melhorias em acurácia e velocidade (JOCHER; CHAURASIA; QIU, 2023).

**Características do YOLOv8:**
- Arquitetura anchor-free
- Backbone CSPDarknet modificado
- Suporte a detecção, segmentação e classificação
- Facilidade de treinamento customizado
- Exportação para múltiplos formatos (ONNX, TensorRT, etc.)

## 2.4 Reconhecimento Óptico de Caracteres (OCR)

### 2.4.1 Definição

OCR (Optical Character Recognition) é a tecnologia que converte diferentes tipos de documentos ou imagens contendo texto em dados editáveis e pesquisáveis.

### 2.4.2 Pipeline de OCR

```
Imagem → Pré-processamento → Segmentação → Reconhecimento → Pós-processamento → Texto
```

**Etapas:**
1. **Pré-processamento**: Binarização, remoção de ruído, correção de inclinação
2. **Segmentação**: Identificação de linhas, palavras e caracteres
3. **Reconhecimento**: Classificação de cada caractere
4. **Pós-processamento**: Correção ortográfica, validação de formato

### 2.4.3 Técnicas Modernas de OCR

**Tesseract OCR:**
- Motor de OCR open source desenvolvido pelo Google
- Suporta mais de 100 idiomas
- Utiliza LSTM para reconhecimento

**EasyOCR:**
- Biblioteca Python baseada em Deep Learning
- Suporta mais de 80 idiomas
- Boa performance em textos de cena (scene text)

**Arquiteturas baseadas em Deep Learning:**
- CRNN (Convolutional Recurrent Neural Network)
- Attention-based models
- Transformer-based models

## 2.5 Placas Veiculares Brasileiras

### 2.5.1 Padrão Brasileiro Antigo

O padrão antigo de placas brasileiras possui:
- Fundo cinza
- 3 letras + 4 números (ex: ABC-1234)
- Dimensões: 400mm x 130mm

### 2.5.2 Padrão Mercosul

Implementado a partir de 2018, o padrão Mercosul possui:
- Fundo branco com faixa azul superior
- 4 letras + 3 números intercalados (ex: ABC1D23)
- Dimensões: 400mm x 130mm
- QR Code (opcional)

### 2.5.3 Desafios Específicos

| Desafio | Descrição |
|---------|-----------|
| Dois padrões | Sistema deve reconhecer ambos os formatos |
| Caracteres similares | O/0, I/1, B/8, S/5 podem ser confundidos |
| Variações regionais | Placas de diferentes estados e categorias |
| Condições adversas | Iluminação, sujeira, ângulo, velocidade |

## 2.6 Trabalhos Relacionados

### 2.6.1 ALPR no Contexto Internacional

| Autor(es) | Ano | Abordagem | Resultados |
|-----------|-----|-----------|------------|
| Silva & Jung | 2018 | YOLO + LSTM | 93.53% acurácia |
| Laroca et al. | 2021 | YOLO + CR-NET | 96.9% acurácia |
| Henry et al. | 2020 | SSD + Attention OCR | 91.8% acurácia |

### 2.6.2 ALPR para Placas Brasileiras

O dataset UFPR-ALPR (LAROCA et al., 2018) é uma referência importante para avaliação de sistemas de reconhecimento de placas brasileiras, contendo mais de 4.500 imagens de veículos com placas do padrão brasileiro.

## 2.7 Considerações do Capítulo

Este capítulo apresentou os fundamentos teóricos necessários para o desenvolvimento do sistema ALPR. Os conceitos de visão computacional, CNNs, detecção de objetos com YOLO e OCR formam a base tecnológica do trabalho. O próximo capítulo apresentará a metodologia utilizada para o desenvolvimento do sistema.
