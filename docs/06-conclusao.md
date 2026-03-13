# 6. Conclusão

Este capítulo apresenta as conclusões do trabalho, sintetizando as contribuições, limitações identificadas e sugestões para trabalhos futuros.

## 6.1 Síntese do Trabalho

Este trabalho teve como objetivo desenvolver um sistema de reconhecimento automático de placas veiculares brasileiras (ALPR) utilizando técnicas de visão computacional e aprendizado profundo.

O sistema desenvolvido é composto por dois módulos principais:

1. **Módulo de Detecção**: Utiliza a arquitetura YOLOv8 para localizar placas veiculares em imagens e vídeos, alcançando [X]% de precisão.

2. **Módulo de OCR**: Emprega a biblioteca EasyOCR combinada com técnicas de pré-processamento para extrair os caracteres das placas, obtendo [X]% de acurácia.

A integração dos módulos resultou em um sistema capaz de processar imagens em [X] ms, viabilizando aplicações em tempo real.

## 6.2 Objetivos Alcançados

### 6.2.1 Objetivo Geral

✅ **Alcançado**: Foi desenvolvido um sistema funcional de reconhecimento automático de placas veiculares brasileiras, capaz de detectar e extrair caracteres de placas nos padrões antigo e Mercosul.

### 6.2.2 Objetivos Específicos

| Objetivo | Status | Observações |
|----------|--------|-------------|
| Realizar revisão bibliográfica | ✅ | Capítulo 2 |
| Coletar e preparar dataset | ✅ | Seção 3.3.2 |
| Implementar modelo de detecção | ✅ | Seção 4.3 |
| Implementar módulo de OCR | ✅ | Seção 4.4 |
| Desenvolver interface de usuário | ✅ | Seção 4.6 |
| Avaliar desempenho do sistema | ✅ | Capítulo 5 |
| Documentar resultados | ✅ | Este documento |

## 6.3 Contribuições do Trabalho

### 6.3.1 Contribuições Técnicas

1. **Pipeline integrado**: Sistema completo que combina detecção e OCR de forma otimizada para placas brasileiras.

2. **Pré-processamento otimizado**: Conjunto de técnicas de pré-processamento que melhoram a acurácia do OCR em [X]%.

3. **Pós-processamento inteligente**: Algoritmo de correção de caracteres baseado nas regras de formação de placas brasileiras.

4. **Código aberto**: Todo o código fonte está disponível para a comunidade acadêmica.

### 6.3.2 Contribuições Acadêmicas

1. Documentação detalhada do processo de desenvolvimento
2. Análise comparativa de técnicas de detecção e OCR
3. Identificação de desafios específicos para placas brasileiras
4. Base para trabalhos futuros na área

## 6.4 Limitações do Trabalho

As seguintes limitações foram identificadas durante o desenvolvimento:

1. **Dataset limitado**: O treinamento foi realizado com um conjunto restrito de imagens, o que pode afetar a generalização.

2. **Condições adversas**: O sistema apresenta dificuldades em condições de baixa iluminação e placas muito sujas ou danificadas.

3. **Hardware**: Para processamento em tempo real com alta resolução, é necessária GPU dedicada.

4. **Escopo**: O sistema foi testado apenas com placas brasileiras, não sendo validado para outros padrões.

## 6.5 Trabalhos Futuros

Sugere-se as seguintes direções para continuidade desta pesquisa:

### 6.5.1 Melhorias no Sistema Atual

- [ ] Aumentar o dataset com mais imagens em condições variadas
- [ ] Implementar data augmentation mais agressivo
- [ ] Testar outras arquiteturas de OCR (TrOCR, PaddleOCR)
- [ ] Otimizar para execução em dispositivos embarcados (Raspberry Pi, Jetson Nano)

### 6.5.2 Novas Funcionalidades

- [ ] Reconhecimento de múltiplas placas simultâneas
- [ ] Integração com banco de dados de veículos
- [ ] Aplicativo mobile para consulta em campo
- [ ] API REST para integração com outros sistemas
- [ ] Módulo de tracking para seguir veículos em vídeo

### 6.5.3 Extensões de Pesquisa

- [ ] Estudo comparativo entre diferentes arquiteturas YOLO (v5, v8, v9)
- [ ] Aplicação de técnicas de domain adaptation para diferentes câmeras
- [ ] Investigação de métodos de super-resolução para placas distantes
- [ ] Detecção de placas clonadas ou adulteradas

## 6.6 Considerações Finais

O reconhecimento automático de placas veiculares é uma tecnologia com grande potencial de aplicação em segurança, fiscalização e gestão de tráfego. Este trabalho demonstrou que é possível desenvolver um sistema funcional utilizando ferramentas open source e técnicas modernas de Deep Learning.

Os resultados obtidos são promissores e indicam que, com refinamentos adicionais, o sistema pode alcançar níveis de desempenho adequados para aplicações reais.

Espera-se que este trabalho contribua para o avanço da pesquisa em visão computacional aplicada ao contexto brasileiro e sirva como base para desenvolvimentos futuros na área.

---

> "A tecnologia é melhor quando aproxima as pessoas."
> — Matt Mullenweg
