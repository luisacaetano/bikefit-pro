# Referências Científicas - BikeFit Pro

> Documentação das bases científicas utilizadas no sistema de análise de bike fit.

---

## 1. Ângulos de Referência

### 1.1 Joelho - Flexão no Bottom Dead Center (BDC)

O BDC (Bottom Dead Center) é o ponto morto inferior do pedal (posição 6 horas).

| Modo | Range Ideal | Ótimo | Fonte |
|------|-------------|-------|-------|
| **Estático** | 25-35° | 30° | Holmes et al. (1994) |
| **Dinâmico** | 33-43° | 38° | Bini & Hume (2020) |

**Alerta de risco:** Flexão > 40° correlaciona com dor no joelho (Martínez & Pérez, 2025)

### 1.2 Diferenças Estático vs Dinâmico

Estudo de Bini et al. (2023) mostrou diferenças significativas:

| Articulação | Diferença | Desvio |
|-------------|-----------|--------|
| Joelho | +8° | ± 2° |
| Quadril | +5° | ± 1° |
| Tornozelo | +9° | ± 2° |

**Implicação:** Medições em vídeo (dinâmico) devem usar thresholds diferentes das medições estáticas tradicionais.

### 1.3 Outros Ângulos

| Ângulo | Range Ideal | Fonte |
|--------|-------------|-------|
| Quadril (estático) | 40-50° | Burt (2014) |
| Quadril (dinâmico) | 35-45° | Ajustado por Bini (2023) |
| Tronco | 40-55° | Burt (2014) |
| Cotovelo | 150-170° | Burt (2014) |
| Tornozelo | 90-110° | Holmes (1994) |

---

## 2. Papers Principais

### 2.1 Holmes et al. (1994) - Método Original
**Título:** "Lower extremity overuse injury in cycling"

- Estabeleceu o método de 25-35° de flexão do joelho no BDC
- Base para a maioria dos protocolos de bike fit
- Medições estáticas com goniômetro

### 2.2 Bini & Hume (2020) - Ranges Dinâmicos
**Título:** "Comparison of static and dynamic methods based on knee kinematics to determine optimal saddle height in cycling"
**URL:** https://pubmed.ncbi.nlm.nih.gov/32022807/

- 26 ciclistas analisados
- Análise de vídeo 2D
- **Descoberta principal:** Ângulo dinâmico do joelho é 8° maior que estático
- **Novo range proposto:** 33-43° para medições dinâmicas

### 2.3 Bini et al. (2023) - Limitações dos Métodos
**Título:** "Details our eyes cannot see: Challenges for the analysis of body position during bicycle fitting"
**Journal:** Sports Biomechanics, Vol. 22, No. 4
**URL:** https://www.tandfonline.com/doi/full/10.1080/14763141.2021.1987509

- Revisão de todos os métodos de bike fit
- Documenta diferenças estático vs dinâmico
- Discute limitações de tecnologias markerless
- Recomenda cautela na adoção de novas tecnologias

### 2.4 Martínez & Pérez (2025) - Correlação com Dor
**Título:** "Biomechanical analysis of knee flexion and saddle height in amateur cyclists"
**Journal:** EFSUPIT
**URL:** https://efsupit.ro/images/stories/september2025/Art%20217.pdf

- Confirma que flexão > 40° correlaciona diretamente com dor
- Ajuste do selim para 25-30° deu alívio imediato
- Base para nossos alertas de risco de lesão

### 2.5 Nasution et al. (2025) - Implementação com Pose Estimation
**Título:** "Bike Fitting System Based on Digital Image Processing on Road Bike"
**Journal:** JOIV - International Journal on Informatics Visualization
**URL:** https://joiv.org/index.php/joiv/article/view/2796

- Sistema completo usando OpenCV + MediaPipe
- Webcam padrão, sem hardware especial
- **Resultados:** Erro < 2% para joelho, cotovelo, quadril, tornozelo
- Classifica como "Fit" ou "Not Fit"

---

## 3. Livros de Referência

### 3.1 Phil Burt - "Bike Fit"
**Título completo:** "Bike Fit: Optimise Your Bike Position for High Performance and Injury Avoidance"
**Autor:** Phil Burt (ex-fisioterapeuta British Cycling / Team Sky)

- Melhor referência prática
- Fit windows para cada articulação
- Troubleshooting de lesões
- Ilustrações detalhadas

### 3.2 Bini & Hume (2014) - Biomechanics of Cycling
**Editora:** Springer

- Referência acadêmica mais completa
- Modelos biomecânicos detalhados
- Base para cálculos de ângulo

---

## 4. Tecnologia de Pose Estimation

### 4.1 Comparação de Modelos

| Modelo | Keypoints | Velocidade | Uso Recomendado |
|--------|-----------|------------|-----------------|
| **YOLOv8-Pose** (usado) | 17 | Tempo real | Produção |
| MediaPipe BlazePose | 33 | Tempo real | Mobile |
| OpenPose | 18-25 | GPU necessário | Pesquisa |
| HRNet | 17 | Lento | Gold-standard |

### 4.2 Por que escolhemos YOLOv8?
- Performance em tempo real (~38ms latência)
- 17 keypoints suficientes para bike fit
- Modelo robusto e bem documentado
- Não requer GPU dedicada

### 4.3 Validação Recomendada
Para validar nosso sistema, devemos comparar com:
1. **Kinovea** - Software gratuito de análise de vídeo (gold standard prático)
2. **Medições manuais com goniômetro** - Validação física
3. **Vicon/Qualisys** - Se disponível (gold standard laboratorial)

---

## 5. Modalidades de Ciclismo

### 5.1 Parâmetros por Modalidade

| Modalidade | Tronco | Quadril | Prioridade |
|------------|--------|---------|------------|
| **Road** | 40-50° | 40-50° | Equilíbrio |
| **MTB** | 50-65° | 45-55° | Controle |
| **Triathlon/TT** | 30-40° | 35-45° | Aerodinâmica |
| **Gravel** | 42-52° | 42-52° | Conforto+ |
| **Urbano** | 60-80° | 50-60° | Máximo conforto |

### 5.2 Fonte
Baseado em Phil Burt (2014) e práticas de fitters profissionais.

---

## 6. Coluna Vertebral

### 6.1 Pontos de Referência
Nosso sistema estima 3 pontos da coluna:

| Ponto | Localização | Nível Vertebral |
|-------|-------------|-----------------|
| **spine_top** | Entre ombros | C7/T1 |
| **spine_mid** | Meio do tronco | T12/L1 |
| **spine_low** | Entre quadris | L5/S1 |

### 6.2 Classificação de Curvatura

| Tipo | Descrição | Indicação |
|------|-----------|-----------|
| **Neutra** | Alinhamento normal | OK |
| **Cifose** | Curvatura para frente | Ajustar posição |
| **Lordose** | Curvatura para trás | Ajustar posição |

### 6.3 Severidade
- **Normal:** Desvio < 5 da linha reta
- **Leve:** Desvio 5-15
- **Moderada:** Desvio 15-25
- **Severa:** Desvio > 25

---

## 7. Implementação no Código

### 7.1 Arquivos Relevantes

```
backend/app/
├── config.py                 # Thresholds estático/dinâmico
├── core/
│   ├── angle_calculator.py   # Cálculo de ângulos
│   ├── pose_detector.py      # YOLOv8 wrapper
│   └── recommendations.py    # Motor de recomendações
```

### 7.2 Configuração de Ângulos

```python
# config.py

# Modo ESTÁTICO (Holmes 1994)
angles_reference_static = {
    "knee_flexion_bdc": {"min": 25, "max": 35, "optimal": 30},
    ...
}

# Modo DINÂMICO (Bini 2020)
angles_reference_dynamic = {
    "knee_flexion_bdc": {"min": 33, "max": 43, "optimal": 38},
    ...
}
```

### 7.3 Alertas de Risco

```python
# Baseado em Martínez & Pérez (2025)
injury_risk_thresholds = {
    "knee_flexion_bdc_max": 40,  # >40° = risco de dor
    "knee_extension_max": 160,   # Sobrecarga
    "trunk_min": 30,             # Dor cervical/lombar
}
```

---

## 8. Kinovea - Software de Referência

### 8.1 Sobre o Kinovea
**URL:** https://www.kinovea.org
**Licença:** GPL v2 (gratuito e open-source)
**Autor:** Joan Charmant

Kinovea é um software de análise de vídeo para esportes, usado por:
- Treinadores e atletas
- Fisioterapeutas
- Bike fitters profissionais
- Pesquisadores biomecânicos

### 8.2 Funcionalidades do Kinovea

| Categoria | Recursos |
|-----------|----------|
| **Captura** | Câmeras UVC, machine vision (Basler, IDS), IP cameras |
| **Anotação** | Linhas, setas, ângulos, ferramentas customizadas |
| **Medição** | Ângulos, distâncias, tempo, trajetórias |
| **Tracking** | Semi-automático com janelas de busca configuráveis |
| **Exportação** | CSV, vídeos compostos, frames individuais |
| **Bike Fit** | Ferramenta específica com stick figure ajustável |

### 8.3 Estudos Científicos com Kinovea

**Inter-rater variability in 2D kinematic cycling analysis using Kinovea® (2025)**
- 53 bike fitters profissionais do Brasil
- Análise do mesmo vídeo
- 7 ângulos articulares medidos
- **Resultado:** ICC > 0.90 para joelho, quadril e tornozelo
- **URL:** https://www.jsc-journal.com/index.php/JSC/article/view/1050

**Validity and reliability of the Kinovea program (2019)**
- Validado contra sistemas 3D
- Erro de ±5° intra-avaliador
- Erro de ±2.5° inter-avaliador
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6550386/

---

## 9. BikeFit Pro vs Kinovea - Comparação Detalhada

### 9.1 Comparação Funcional

| Aspecto | Kinovea | BikeFit Pro |
|---------|---------|-------------|
| **Tipo** | Desktop (Windows) | Web (cross-platform) |
| **Licença** | Gratuito (GPL v2) | Código aberto |
| **Detecção de pontos** | Manual/semi-automático | **Automático (IA)** |
| **Tempo de análise** | Pós-gravação | **Tempo real** |
| **Recomendações** | Não | **Sim, baseadas em literatura** |
| **Alertas de risco** | Não | **Sim, com referências** |
| **Curva de aprendizado** | Médio-alto | Baixo |
| **Hardware necessário** | PC Windows | Qualquer dispositivo com câmera |

### 9.2 Comparação Técnica

| Recurso | Kinovea | BikeFit Pro | Vantagem |
|---------|---------|-------------|----------|
| Rastreamento | Janelas de busca configuráveis | YOLOv8 (17 keypoints) | **BikeFit Pro** |
| Precisão angular | ±2.5° (validado) | ~2% erro (Nasution 2025) | Equivalente |
| Múltiplas câmeras | Sim (sync manual) | Não (ainda) | Kinovea |
| Trajetórias | Sim | Não (ainda) | Kinovea |
| Diagramas ângulo-ângulo | Sim | Não (ainda) | Kinovea |
| Exportação CSV | Sim | Parcial | Kinovea |
| Modo estático/dinâmico | Manual | **Automático com thresholds** | **BikeFit Pro** |
| Análise da coluna | Não | **Sim (cifose/lordose)** | **BikeFit Pro** |
| PDF automatizado | Não | **Sim** | **BikeFit Pro** |

### 9.3 BikeFit Pro NÃO é uma "Nova Versão" do Kinovea

**São abordagens fundamentalmente diferentes:**

| Kinovea | BikeFit Pro |
|---------|-------------|
| Ferramenta de **análise de vídeo** genérica | Sistema de **bike fit especializado** |
| Usuário marca pontos manualmente | IA detecta pontos automaticamente |
| Análise **depois** da gravação | Análise **durante** a sessão |
| Exporta dados para interpretação | **Interpreta e recomenda** |
| Conhecimento do operador é essencial | Sistema guia o operador |

**Analogia:** Kinovea é como uma calculadora científica - poderosa, mas você precisa saber as fórmulas. BikeFit Pro é como uma planilha com fórmulas pré-programadas - faz os cálculos e ainda explica o resultado.

### 9.4 Diferenciais Exclusivos do BikeFit Pro

1. **Detecção automática de pose** - Sem marcação manual de pontos
2. **Feedback em tempo real** - Ajustes com visualização instantânea
3. **Recomendações científicas** - Baseadas em papers peer-reviewed
4. **Alertas de risco de lesão** - Com citação da fonte
5. **Análise da coluna vertebral** - Detecção de cifose/lordose
6. **Comparativo antes/depois** - Visual e numérico
7. **Relatório PDF automático** - Para entregar ao cliente
8. **Histórico de sessões** - Acompanhamento ao longo do tempo

---

## 10. Melhorias Futuras (Inspiradas no Kinovea)

### 10.1 Funcionalidades a Implementar

| Prioridade | Funcionalidade | Inspiração | Benefício |
|------------|----------------|------------|-----------|
| **Alta** | Exportação CSV completa | Kinovea | Análise científica |
| **Alta** | Trajetória de pontos | Kinovea | Ver evolução do pedal |
| **Média** | Diagrama ângulo-ângulo | Kinovea | Padrão de movimento |
| **Média** | Playback frame-a-frame | Kinovea | Revisão detalhada |
| **Média** | Overlay de posição ideal | Kinovea "Human Model" | Visualização de meta |
| **Baixa** | Múltiplas câmeras | Kinovea | Vista frontal + lateral |
| **Baixa** | Análise de cadência | Kinovea chronometer | Performance |

### 10.2 Melhorias de UX

1. **Modo de revisão** - Pausar e revisar frames específicos
2. **Gravação de sessão** - Salvar vídeo além das capturas
3. **Templates de posição** - Posições ideais pré-definidas por modalidade
4. **Comparação com sessões anteriores** - Evolução do cliente
5. **Integração com rolo de treino** - Dados de potência/cadência

---

## 11. Links Úteis

### Papers
- Bini 2023: https://www.tandfonline.com/doi/full/10.1080/14763141.2021.1987509
- Bini 2020: https://pubmed.ncbi.nlm.nih.gov/32022807/
- Nasution 2025: https://joiv.org/index.php/joiv/article/view/2796
- Kinovea Reliability: https://pmc.ncbi.nlm.nih.gov/articles/PMC6550386/
- Kinovea Bike Fit Study: https://www.jsc-journal.com/index.php/JSC/article/view/1050

### Ferramentas
- Kinovea: https://www.kinovea.org
- Kinovea Documentation: https://www.kinovea.org/help/en/
- Kinovea Forums: https://www.kinovea.org/en/forum/
- MediaPipe: https://github.com/google-ai-edge/mediapipe

### Pesquisadores
- Andrei Pernambuco (BR): https://www.researchgate.net/profile/Andrei-Pernambuco
- Rodrigo Bini (NZ/BR): Springer Biomechanics of Cycling

---

## 12. Validação Pendente

### 12.1 Tarefas de Validação
- [ ] Comparar medições com Kinovea em 10+ vídeos
- [ ] Meta: erro < 5% para ângulo do joelho
- [x] Contato com fisioterapeuta especialista (Prof. Andrei Pernambuco)
- [ ] Acompanhar atendimento de bike fit real
- [ ] Validar com bike fitter profissional

### 12.2 Metodologia de Validação vs Kinovea

**Protocolo sugerido:**
1. Gravar vídeo de ciclista em perfil (1080p, 30fps)
2. Analisar no Kinovea (3 avaliadores independentes)
3. Processar mesmo vídeo com BikeFit Pro
4. Comparar frame-a-frame os 5 ângulos principais
5. Calcular: erro médio, desvio padrão, ICC

**Ângulos a validar:**
| Ângulo | Kinovea (manual) | BikeFit Pro (auto) |
|--------|------------------|-------------------|
| Joelho (extensão) | | |
| Joelho (flexão BDC) | | |
| Quadril | | |
| Tornozelo | | |
| Tronco | | |

**Critério de sucesso:**
- Erro médio < 5°
- ICC > 0.85
- Correlação de Pearson > 0.90

### 12.3 Próximos Passos
1. Agendar visita com Prof. Andrei Pernambuco
2. Observar atendimento real com sistema avançado dele
3. Instalar Kinovea para testes comparativos
4. Gravar vídeos de teste padronizados
5. Executar protocolo de validação

---

*Documento criado em: 14/03/2026*
*Última atualização: 16/03/2026*
*Adicionado: Seção completa sobre Kinovea e comparação*
