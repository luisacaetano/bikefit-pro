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

## 8. Links Úteis

### Papers
- Bini 2023: https://www.tandfonline.com/doi/full/10.1080/14763141.2021.1987509
- Bini 2020: https://pubmed.ncbi.nlm.nih.gov/32022807/
- Nasution 2025: https://joiv.org/index.php/joiv/article/view/2796

### Ferramentas
- Kinovea (validação): https://www.kinovea.org
- MediaPipe: https://github.com/google-ai-edge/mediapipe

### Pesquisadores
- Andrei Pernambuco (BR): https://www.researchgate.net/profile/Andrei-Pernambuco
- Rodrigo Bini (NZ/BR): Springer Biomechanics of Cycling

---

## 9. Validação Pendente

### 9.1 Tarefas de Validação
- [ ] Comparar medições com Kinovea em 10+ vídeos
- [ ] Meta: erro < 5% para ângulo do joelho
- [ ] Validar com fisioterapeuta especialista
- [ ] Validar com bike fitter profissional

### 9.2 Metodologia Sugerida (Lafayette et al., 2023)
1. Gravar vídeo de ciclista em perfil
2. Medir ângulos manualmente no Kinovea
3. Processar mesmo vídeo com BikeFit Pro
4. Comparar frame-a-frame
5. Calcular erro médio e desvio padrão

---

*Documento criado em: 14/03/2026*
*Baseado em: bike_fit_research.md*
