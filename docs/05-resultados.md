# 5. Resultados e Discussão

Este capítulo apresenta os resultados obtidos nos experimentos realizados, incluindo métricas de desempenho do módulo de detecção, do módulo de OCR e do sistema integrado.

## 5.1 Ambiente de Experimentação

### 5.1.1 Configuração de Hardware

| Componente | Especificação |
|------------|---------------|
| Processador | [Especificar] |
| Memória RAM | [Especificar] GB |
| GPU | [Especificar] |
| Sistema Operacional | [Especificar] |

### 5.1.2 Dataset Utilizado

| Conjunto | Quantidade de Imagens | Descrição |
|----------|----------------------|-----------|
| Treino | [X] | Imagens para treinamento do modelo |
| Validação | [X] | Imagens para ajuste de hiperparâmetros |
| Teste | [X] | Imagens para avaliação final |
| **Total** | **[X]** | |

**Características do dataset:**
- Resolução das imagens: [especificar]
- Condições de iluminação: [variadas/controladas]
- Tipos de placas: [antigo/Mercosul/ambos]
- Distância da câmera: [especificar intervalo]

## 5.2 Resultados da Detecção de Placas

### 5.2.1 Curva de Treinamento

[Inserir gráfico de loss durante treinamento]

**Observações:**
- O modelo convergiu após [X] épocas
- Não foram observados sinais de overfitting
- Early stopping foi acionado na época [X]

### 5.2.2 Métricas de Detecção

| Métrica | Valor |
|---------|-------|
| Precision | [X]% |
| Recall | [X]% |
| F1-Score | [X]% |
| mAP@0.5 | [X]% |
| mAP@0.5:0.95 | [X]% |

### 5.2.3 Matriz de Confusão

```
                    Predito
                 Placa  |  Não-Placa
              ┌────────┼───────────┐
     Placa    │  TP    │    FN     │
Real          ├────────┼───────────┤
     Não-Placa│  FP    │    TN     │
              └────────┴───────────┘

TP (True Positive)  = [X]
FP (False Positive) = [X]
FN (False Negative) = [X]
TN (True Negative)  = [X]
```

### 5.2.4 Exemplos de Detecção

**Detecções Corretas:**

[Inserir imagens de exemplos bem-sucedidos]

**Falhas de Detecção:**

[Inserir imagens de falhas e análise das causas]

| Tipo de Falha | Quantidade | Possível Causa |
|---------------|------------|----------------|
| Falso Negativo | [X] | Placa parcialmente obstruída |
| Falso Negativo | [X] | Iluminação insuficiente |
| Falso Positivo | [X] | Objeto similar à placa |

## 5.3 Resultados do OCR

### 5.3.1 Métricas de Reconhecimento

| Métrica | Valor |
|---------|-------|
| Acurácia por caractere | [X]% |
| Acurácia por placa (exata) | [X]% |
| CER (Character Error Rate) | [X]% |

### 5.3.2 Análise por Tipo de Placa

| Tipo de Placa | Quantidade | Acurácia |
|---------------|------------|----------|
| Padrão Antigo | [X] | [X]% |
| Padrão Mercosul | [X] | [X]% |

### 5.3.3 Caracteres Mais Confundidos

| Caractere Real | Reconhecido Como | Frequência |
|----------------|------------------|------------|
| O | 0 | [X] vezes |
| 0 | O | [X] vezes |
| I | 1 | [X] vezes |
| B | 8 | [X] vezes |
| [outros] | [outros] | [X] vezes |

### 5.3.4 Impacto do Pré-processamento

| Técnica | Acurácia Sem | Acurácia Com | Melhoria |
|---------|--------------|--------------|----------|
| Binarização | [X]% | [X]% | +[X]% |
| Filtro bilateral | [X]% | [X]% | +[X]% |
| Correção de contraste | [X]% | [X]% | +[X]% |
| **Todas combinadas** | [X]% | [X]% | **+[X]%** |

## 5.4 Resultados do Sistema Integrado

### 5.4.1 Pipeline Completo

| Métrica | Valor |
|---------|-------|
| Acurácia end-to-end | [X]% |
| Tempo médio por imagem | [X] ms |
| FPS (vídeo) | [X] |
| Uso de memória RAM | [X] GB |
| Uso de GPU | [X]% |

### 5.4.2 Análise por Condição

| Condição | Quantidade | Acurácia |
|----------|------------|----------|
| Dia (boa iluminação) | [X] | [X]% |
| Dia (sombra) | [X] | [X]% |
| Noite (artificial) | [X] | [X]% |
| Chuva | [X] | [X]% |

### 5.4.3 Análise por Distância

| Distância Estimada | Acurácia Detecção | Acurácia OCR |
|-------------------|-------------------|--------------|
| Próximo (< 3m) | [X]% | [X]% |
| Médio (3-6m) | [X]% | [X]% |
| Longe (> 6m) | [X]% | [X]% |

## 5.5 Comparação com Trabalhos Relacionados

| Trabalho | Dataset | Métrica | Resultado | Este Trabalho |
|----------|---------|---------|-----------|---------------|
| Silva & Jung (2018) | SSIG | Acurácia | 93.53% | [X]% |
| Laroca et al. (2021) | UFPR-ALPR | Acurácia | 96.9% | [X]% |
| [Outro trabalho] | [Dataset] | [Métrica] | [X]% | [X]% |

**Observações sobre a comparação:**
- [Discutir diferenças de dataset]
- [Discutir diferenças de metodologia]
- [Justificar resultados]

## 5.6 Análise de Falhas

### 5.6.1 Principais Causas de Erro

1. **Iluminação inadequada**
   - Descrição: [descrever]
   - Frequência: [X]%
   - Possível solução: [sugestão]

2. **Placa danificada/suja**
   - Descrição: [descrever]
   - Frequência: [X]%
   - Possível solução: [sugestão]

3. **Ângulo extremo**
   - Descrição: [descrever]
   - Frequência: [X]%
   - Possível solução: [sugestão]

4. **Movimento (blur)**
   - Descrição: [descrever]
   - Frequência: [X]%
   - Possível solução: [sugestão]

### 5.6.2 Exemplos de Casos Difíceis

[Inserir imagens de casos problemáticos com análise]

## 5.7 Discussão dos Resultados

### 5.7.1 Pontos Fortes

- [Listar pontos positivos do sistema]
- [Destacar métricas acima da média]
- [Mencionar casos de sucesso]

### 5.7.2 Limitações

- [Listar limitações identificadas]
- [Discutir cenários onde o sistema falha]
- [Mencionar restrições de hardware/software]

### 5.7.3 Contribuições

- [Destacar contribuições do trabalho]
- [Mencionar código/modelo disponibilizado]
- [Citar melhorias propostas]

## 5.8 Considerações do Capítulo

Este capítulo apresentou os resultados experimentais do sistema ALPR desenvolvido. Os experimentos demonstraram que [resumir principais conclusões]. O próximo capítulo apresentará as conclusões finais e sugestões para trabalhos futuros.

---

**Nota**: Os valores marcados com [X] devem ser preenchidos após a realização dos experimentos.
