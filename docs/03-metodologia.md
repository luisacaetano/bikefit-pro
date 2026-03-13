# 3. Metodologia

Este capítulo descreve a metodologia adotada para o desenvolvimento do sistema de reconhecimento automático de placas veiculares, incluindo a classificação da pesquisa, materiais utilizados, procedimentos metodológicos e métricas de avaliação.

## 3.1 Classificação da Pesquisa

### 3.1.1 Quanto à Natureza

Esta pesquisa é classificada como **aplicada**, pois visa gerar conhecimentos para aplicação prática, dirigidos à solução de um problema específico: o reconhecimento automático de placas veiculares.

### 3.1.2 Quanto à Abordagem

A abordagem é **quantitativa**, uma vez que os resultados são expressos em métricas numéricas como acurácia, precisão, recall e tempo de processamento.

### 3.1.3 Quanto aos Objetivos

Trata-se de uma pesquisa **exploratória e experimental**, envolvendo:
- Levantamento bibliográfico
- Experimentação com diferentes configurações e parâmetros
- Análise comparativa de resultados

### 3.1.4 Quanto aos Procedimentos

Os procedimentos técnicos incluem:
- Pesquisa bibliográfica
- Desenvolvimento de software
- Experimentos computacionais

## 3.2 Materiais e Ferramentas

### 3.2.1 Hardware

| Componente | Especificação |
|------------|---------------|
| Processador | Intel Core i7 / AMD Ryzen 7 (ou equivalente) |
| Memória RAM | 16 GB |
| GPU | NVIDIA com CUDA (para treinamento) |
| Armazenamento | SSD 256 GB+ |
| Câmera | Webcam 720p / Smartphone (para testes) |

**Nota**: Para treinamento, será utilizado o Google Colab (GPU gratuita) quando necessário.

### 3.2.2 Software

| Software | Versão | Finalidade |
|----------|--------|------------|
| Sistema Operacional | Windows 10/11, Linux ou macOS | Ambiente de desenvolvimento |
| Python | 3.9+ | Linguagem de programação |
| OpenCV | 4.x | Processamento de imagens |
| Ultralytics YOLOv8 | latest | Detecção de objetos |
| EasyOCR | 1.x | Reconhecimento de caracteres |
| PyTorch | 2.x | Framework de Deep Learning |
| Streamlit | 1.x | Interface web |
| Git | latest | Controle de versão |
| VS Code | latest | IDE de desenvolvimento |

### 3.2.3 Datasets

| Dataset | Descrição | Uso |
|---------|-----------|-----|
| UFPR-ALPR | 4.500+ imagens de placas brasileiras | Treinamento e teste |
| Roboflow License Plates | Datasets variados de placas | Pré-treinamento |
| Dataset próprio | Imagens coletadas localmente | Validação |

## 3.3 Procedimentos Metodológicos

O desenvolvimento do trabalho seguirá as etapas ilustradas no fluxograma abaixo:

```
┌──────────────────┐
│ 1. Revisão       │
│    Bibliográfica │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 2. Coleta e      │
│    Preparação    │
│    de Dados      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 3. Desenvolvimento│
│    do Módulo de  │
│    Detecção      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 4. Desenvolvimento│
│    do Módulo de  │
│    OCR           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 5. Integração    │
│    dos Módulos   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 6. Avaliação e   │
│    Testes        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 7. Documentação  │
│    e Escrita     │
└──────────────────┘
```

### 3.3.1 Etapa 1: Revisão Bibliográfica

**Objetivo**: Fundamentar teoricamente o trabalho e identificar o estado da arte.

**Atividades**:
- Pesquisa em bases científicas (IEEE, ACM, Google Scholar)
- Estudo de trabalhos relacionados
- Análise de técnicas e ferramentas disponíveis

**Entregáveis**:
- Capítulo de Fundamentação Teórica
- Lista de referências bibliográficas

### 3.3.2 Etapa 2: Coleta e Preparação de Dados

**Objetivo**: Obter e preparar o dataset para treinamento e avaliação.

**Atividades**:
- Solicitação de acesso ao dataset UFPR-ALPR
- Coleta de imagens adicionais (opcional)
- Anotação das imagens no formato YOLO
- Divisão do dataset (treino/validação/teste: 70/15/15)
- Aplicação de data augmentation

**Técnicas de Data Augmentation**:
- Rotação (-15° a +15°)
- Variação de brilho e contraste
- Adição de ruído gaussiano
- Espelhamento horizontal

### 3.3.3 Etapa 3: Desenvolvimento do Módulo de Detecção

**Objetivo**: Implementar modelo capaz de localizar placas em imagens.

**Atividades**:
- Configuração do ambiente de treinamento
- Fine-tuning do YOLOv8 com dataset de placas
- Otimização de hiperparâmetros
- Exportação do modelo treinado

**Hiperparâmetros a serem testados**:

| Parâmetro | Valores a testar |
|-----------|-----------------|
| Epochs | 50, 100, 150 |
| Batch size | 8, 16, 32 |
| Learning rate | 0.001, 0.0001 |
| Image size | 416, 640 |

### 3.3.4 Etapa 4: Desenvolvimento do Módulo de OCR

**Objetivo**: Implementar reconhecimento dos caracteres das placas.

**Atividades**:
- Implementação de pré-processamento da região da placa
- Integração com EasyOCR
- Pós-processamento (validação de formato, correção)
- Testes de acurácia do OCR

**Pré-processamento da placa**:
1. Conversão para escala de cinza
2. Aplicação de filtro bilateral (redução de ruído)
3. Binarização adaptativa (threshold de Otsu)
4. Correção de perspectiva (se necessário)

### 3.3.5 Etapa 5: Integração dos Módulos

**Objetivo**: Unificar detecção e OCR em um sistema funcional.

**Atividades**:
- Desenvolvimento do pipeline completo
- Implementação de interface de usuário
- Otimização de performance
- Tratamento de erros e exceções

### 3.3.6 Etapa 6: Avaliação e Testes

**Objetivo**: Medir o desempenho do sistema desenvolvido.

**Atividades**:
- Execução de testes com conjunto de teste
- Cálculo de métricas de desempenho
- Análise de casos de falha
- Comparação com trabalhos relacionados

### 3.3.7 Etapa 7: Documentação

**Objetivo**: Registrar todo o processo e resultados.

**Atividades**:
- Escrita dos capítulos do TCC
- Elaboração de diagramas e figuras
- Revisão e formatação ABNT
- Preparação da apresentação

## 3.4 Métricas de Avaliação

### 3.4.1 Métricas para Detecção

| Métrica | Descrição | Fórmula |
|---------|-----------|---------|
| **Precision** | Proporção de detecções corretas | TP / (TP + FP) |
| **Recall** | Proporção de placas detectadas | TP / (TP + FN) |
| **F1-Score** | Média harmônica de Precision e Recall | 2 × (P × R) / (P + R) |
| **mAP@0.5** | Mean Average Precision com IoU ≥ 0.5 | Média de AP por classe |
| **mAP@0.5:0.95** | mAP em diferentes thresholds de IoU | Média de mAP |

### 3.4.2 Métricas para OCR

| Métrica | Descrição |
|---------|-----------|
| **Acurácia por caractere** | % de caracteres reconhecidos corretamente |
| **Acurácia por placa** | % de placas com todos caracteres corretos |
| **CER (Character Error Rate)** | Taxa de erro por caractere |
| **Edit Distance** | Número de edições para corrigir predição |

### 3.4.3 Métricas de Performance

| Métrica | Descrição | Meta |
|---------|-----------|------|
| **FPS** | Frames por segundo processados | ≥ 10 FPS |
| **Latência** | Tempo de processamento por imagem | ≤ 500ms |
| **Uso de memória** | RAM utilizada durante execução | ≤ 4 GB |

## 3.5 Considerações Éticas

- Imagens de placas utilizadas apenas para fins acadêmicos
- Não serão armazenados dados pessoais dos proprietários
- Dataset será manipulado conforme termos de uso
- Código fonte será disponibilizado para reprodutibilidade

## 3.6 Considerações do Capítulo

Este capítulo apresentou a metodologia que guiará o desenvolvimento do sistema ALPR. A abordagem científica adotada, combinada com ferramentas modernas e métricas bem definidas, permitirá avaliar objetivamente os resultados obtidos. O próximo capítulo detalhará a implementação do sistema.
